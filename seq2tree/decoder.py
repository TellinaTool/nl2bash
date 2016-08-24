"""A set of decoder modules used in the encoder-decoder framework."""

import tensorflow as tf
import sys
sys.path.append("../seq2seq")

import data_utils
import graph_utils

class Decoder(object):
    def __init__(self, dim, batch_size, max_num_steps, num_layers, use_attention, use_copy,
                 output_projection=None):
        self.dim = dim
        self.batch_size = batch_size
        self.max_num_steps = max_num_steps
        self.num_layers = num_layers
        self.use_attention = use_attention
        self.use_copy = use_copy

        self.output_projection = output_projection

        # variable sharing
        self.attention_cell_vars = False

    def attention_cell(self, cell, cell_scope, input_embedding, state, attns,
                       hidden_features, attn_vecs, num_heads, hidden):
        with tf.variable_scope("AttnInputProjection"):
            if self.attention_cell_vars:
                tf.get_variable_scope().reuse_variables()
            # attention mechanism on cell and hidden states
            x = tf.nn.rnn_cell._linear([input_embedding] + [attns], self.dim, True)
            try:
                cell_output, state = cell(x, state, cell_scope)
            except ValueError, e:
                cell_scope.reuse_variables()
                cell_output, state = cell(x, state, cell_scope)
            attns = self.attention(state, hidden_features, attn_vecs, num_heads, hidden)
        with tf.variable_scope("AttnOutputProjection"):
            if self.attention_cell_vars:
                tf.get_variable_scope().reuse_variables()
            # attention mechanism on output state
            output = tf.nn.rnn_cell._linear([cell_output] + [attns], self.dim, True)
        self.attention_cell_vars = True
        return output, state[0], state[1], attns

    def attention(self, state, hidden_features, attn_vecs, num_heads, hidden):
        assert(len(attn_vecs) > 0)
        attn_vec_dim = attn_vecs[0].get_shape()[0].value
        attn_length = hidden.get_shape()[1].value
        attn_dim = hidden.get_shape()[3].value
        """Put attention masks on hidden using hidden_features and query."""
        ds = []  # Results of attention reads will be stored here.
        for a in xrange(num_heads):
            with tf.variable_scope("Attention_%d" % a):
                y = tf.nn.rnn_cell._linear(state, attn_vec_dim, True)
                y = tf.reshape(y, [-1, 1, 1, attn_vec_dim])
                # Attention mask is a softmax of v^T * tanh(...).
                s = tf.reduce_sum(
                    attn_vecs[a] * tf.tanh(hidden_features[a] + y), [2, 3])
                a = tf.nn.softmax(s)
                # Now calculate the attention-weighted vector d.
                d = tf.reduce_sum(tf.reshape(a, [-1, attn_length, 1, 1]) * hidden,
                    [1, 2])
                ds.append(tf.reshape(d, [-1, attn_dim]))
        attns = tf.concat(1, ds)
        attns.set_shape([self.batch_size, num_heads * attn_dim])
        return attns

    def attention_hidden_layer(self, attention_states, num_heads):
        """
        Hidden layer above attention states.
        :param attention_states: 3D Tensor [batch_size x attn_length x attn_dim].
        :param num_heads: Number of attention heads that read from from attention_states.
                         Dummy field if attention_states is None.
        """
        attn_length = attention_states.get_shape()[1].value
        attn_dim = attention_states.get_shape()[2].value

        # To calculate W1 * h_t we use a 1-by-1 convolution
        hidden = tf.reshape(attention_states, [-1, attn_length, 1, attn_dim])
        hidden_features = []
        attn_vecs = []
        attn_vec_dim = attn_dim
        for i in xrange(num_heads):
            k = tf.get_variable("AttnW_%d" % i, [1, 1, attn_dim, attn_vec_dim])
            hidden_features.append(tf.nn.conv2d(hidden, k, [1,1,1,1], "SAME"))
            attn_vecs.append(tf.get_variable("AttnV_%d" % i, [attn_vec_dim]))
        return hidden, hidden_features, attn_vecs


    def normal_cell(self, cell, scope, input, state):
        try:
            output, state = cell(input, state, scope)
        except ValueError, e:
            scope.reuse_variables()
            output, state = cell(input, state, scope)
        return output, state[0], state[1]


class BasicTreeDecoder(Decoder):

    _NO_EXPAND = tf.constant(data_utils.NO_EXPAND_ID)

    def define_graph(self, encoder_state, decoder_inputs, embeddings,
                     attention_states=None, num_heads=1,
                     initial_state_attention=False, feed_previous=False):
        """
        :param encoder_state: hidden state of the encoder
        :param inputs: placeholders for the discrete inputs of the decoder
        :param embeddings: output token embeddings
        :param attention_states: 3D Tensor [batch_size x attn_length x attn_dim].
        :param num_heads: Number of attention heads that read from from attention_states.
            Dummy field if attention_states is None.
        :param initial_state_attention: If False (default), initial attentions are zero.
            If True, initialize the attentions from the initial state and attention states
            -- useful to resume decoding from a previously stored decoder state and attention
            state.
        :param feed_previous: Boolean; if True, only the first of decoder_inputs will be
            used (the "ROOT" symbol), and all other decoder inputs will be generated by:
            next = embedding_lookup(embedding, argmax(previous_output)),
            In effect, this implements a greedy decoder. It can also be used
            during training to emulate http://arxiv.org/abs/1506.03099.
            If False, decoder_inputs are used as given (the standard decoder case).

        :return: Output states and the final hidden state of the decoder. Need
            output_projection to obtain distribution over output vocabulary.
        """

        def push(states):
            new_top_state = tf.concat(1, states)
            return tf.concat(0, [stack, new_top_state])

        def peek():
            if self.use_attention:
                return stack[-1:, 0:self.dim], \
                       tf.nn.rnn_cell.LSTMStateTuple(stack[-1:, self.dim:2*self.dim],
                                                     stack[-1:, 2*self.dim:3*self.dim]), \
                       stack[-1:, 3*self.dim:]
            else:
                return stack[-1:, 0:self.dim], \
                       tf.nn.rnn_cell.LSTMStateTuple(stack[-1:, self.dim:2*self.dim],
                                                     stack[-1:, 2*self.dim:])

        def pop():
            return stack[:-1, :]

        def cs_push(state):
            return tf.concat(0, [cs_stack, state])

        def cs_peek():
            return cs_stack[-1:, :]

        def cs_pop():
            return cs_stack[:-1, :]

        if self.use_attention and not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be known %s"
                             % attention_states.get_shape())

        if feed_previous:
            # scope of output_projection is the entire model
            # hence retrieving variables here
            W, b = self.output_projection
            print("basic_tree_encoder: " + W.name)
            print("basic_tree_encoder: " + b.name)

        with tf.variable_scope("basic_tree_decoder") as scope:
            embedding_inputs = [tf.nn.embedding_lookup(embeddings, i) for i in decoder_inputs]

            parent_cell, parent_scope = self.parent_cell()
            sb_cell, sb_scope = self.sb_cell()
            outputs = []

            # search control
            init_input = embedding_inputs[0]
            control_symbol = decoder_inputs[0]
            # discrete stack mimicking DFS in a discrete space
            cs_stack = tf.zeros([self.max_num_steps, 1], dtype=tf.int32)
            cs_stack = tf.concat(0, [cs_stack, tf.expand_dims(control_symbol, 1)])

            # continuous stack used for storing LSTM states, synced with cs_stack
            if self.use_attention:
                hidden, hidden_features, attn_vecs = \
                    self.attention_hidden_layer(attention_states, num_heads)
                attn_dim = tf.shape(hidden)[2]
                batch_attn_size = tf.pack([self.batch_size, attn_dim])
                attns = tf.concat(1, [tf.zeros(batch_attn_size, dtype=tf.float32)    # initial attention state
                         for _ in xrange(num_heads)])
                attns.set_shape([self.batch_size, num_heads * attn_dim])
                if initial_state_attention:
                    attns = self.attention(encoder_state, hidden_features, attn_vecs, num_heads, hidden)
                init_stack = tf.concat(1, [init_input, encoder_state[0], encoder_state[1], attns])
            else:
                init_stack = tf.concat(1, [init_input, encoder_state[0], encoder_state[1]])
            stack = tf.zeros([self.max_num_steps, init_stack.get_shape()[1].value])
            stack = tf.concat(0, [stack, init_stack])

            for i, _ in enumerate(decoder_inputs[:-1]):
                if i > 0: scope.reuse_variables()

                if feed_previous:
                    control_symbol = cs_peek()[0]
                else:
                    control_symbol = decoder_inputs[i]

                search_left_to_right = self.is_no_expand(control_symbol[0])

                # mimick a stack pop if current symbol is <NO_EXPAND>
                if feed_previous:
                    cs_stack = tf.cond(search_left_to_right, lambda: cs_pop(), lambda: cs_stack)
                stack = tf.cond(search_left_to_right, lambda: pop(), lambda: stack)

                if self.use_attention:
                    input, state, attns = peek()
                    output, cell, hs, attns = tf.cond(search_left_to_right,
                        lambda: self.attention_cell(parent_cell, parent_scope, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden),
                        lambda: self.attention_cell(sb_cell, sb_scope, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden))
                else:
                    input, state = peek()
                    output, cell, hs = tf.cond(search_left_to_right,
                        lambda: self.normal_cell(parent_cell, parent_scope, input, state),
                        lambda: self.normal_cell(sb_cell, sb_scope, input, state))

                # mimick a stack pop if current symbol is <NO_EXPAND>
                if feed_previous:
                    cs_stack = tf.cond(search_left_to_right, lambda: cs_pop(), lambda: cs_stack)
                stack = tf.cond(search_left_to_right, lambda: pop(), lambda: stack)

                if feed_previous:
                    # Project decoder output for next state input.
                    projected_output = tf.matmul(output, W) + b
                    control_symbol = tf.argmax(projected_output, 1)
                    next_input = tf.nn.embedding_lookup(embeddings, control_symbol)
                    cs_stack = cs_push(tf.cast(tf.expand_dims(control_symbol, 1), tf.int32))
                else:
                    next_input = embedding_inputs[i+1]

                if self.use_attention:
                    stack = push([next_input, cell, hs, attns])
                else:
                    stack = push([next_input, cell, hs])

                outputs.append(output)

        return outputs, tf.nn.rnn_cell.LSTMStateTuple(cell, hs)

    def is_no_expand(self, ind):
        return tf.equal(tf.cast(ind, tf.int32), BasicTreeDecoder._NO_EXPAND)


    def parent_cell(self):
        """Cell that controls transition from parent to child."""
        with tf.variable_scope("decoder_parent_cell") as scope:
            cell = graph_utils.create_multilayer_cell("lstm", scope, self.dim, self.num_layers)
        return cell, scope

    def sb_cell(self):
        """Cell that controls transition from left sibling to right sibling."""
        with tf.variable_scope("decoder_sb_cell") as scope:
            cell = graph_utils.create_multilayer_cell("lstm", scope, self.dim, self.num_layers)
        return cell, scope


    @graph_utils.deprecated
    def top_to_bottom_with_attention(self, cell, hidden_features, attn_vecs, num_heads, hidden):
        input, state, attns = self.peek()
        output, state, attns = self.attention_cell(cell, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden)
        return output, state, attns

    @graph_utils.deprecated
    def left_to_right_with_attention(self, cell, hidden_features, attn_vecs, num_heads, hidden):
        self.pop()
        input, state, attns = self.peek()
        output, state, attns = self.attention_cell(cell, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden)
        self.pop()
        return output, state, attns

    @graph_utils.deprecated
    def top_to_bottom(self, cell):
        input, state = self.peek()
        output, state = cell(input, state)
        return output, state

    @graph_utils.deprecated
    def left_to_right(self, cell):
        self.pop()
        input, state = self.peek()
        output, state = cell(input, state)
        self.pop()
        return output, state