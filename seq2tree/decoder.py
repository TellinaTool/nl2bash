"""A set of decoder modules used in the encoder-decoder framework."""

import tensorflow as tf
import sys
sys.path.append("../seq2seq")

import data_utils
import graph_utils

class Decoder(object):
    def __init__(self, dim, batch_size, max_num_steps, num_layers, use_attention,
                 use_copy, output_projection=None):
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
        :param embeddings: target embeddings
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
        self.embeddings = embeddings
        decoder_inputs = tf.split(0, self.batch_size, tf.concat(1, decoder_inputs))

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
            parent_cell, parent_scope = self.parent_cell()
            sb_cell, sb_scope = self.sb_cell()
            outputs = []

            # search control
            self.back_pointers = tf.constant(0, shape=[self.batch_size, 1])
            last_search_left_to_right = [tf.constant(False, dtype=tf.bool)] * self.batch_size

            # continuous stack used for storing LSTM states, synced with self.back_pointers
            if self.use_attention:
                hidden, hidden_features, attn_vecs = \
                    self.attention_hidden_layer(attention_states, num_heads)
                batch_size = tf.shape(attention_states)[0]
                attn_dim = tf.shape(attention_states)[2]
                batch_attn_size = tf.pack([batch_size, attn_dim])
                # initial attention state
                attns = tf.concat(1, [tf.zeros(batch_attn_size, dtype=tf.float32)
                         for _ in xrange(num_heads)])
                attns.set_shape([self.batch_size, num_heads * attention_states.get_shape()[2].value])
                if initial_state_attention:
                    attns = self.attention(encoder_state, hidden_features, attn_vecs, num_heads, hidden)
                init_stack = tf.concat(1, [encoder_state[0], encoder_state[1], attns])
            else:
                init_stack = tf.concat(1, [encoder_state[0], encoder_state[1]])
            self.stack = tf.expand_dims(init_stack, 1)
            self.input = tf.expand_dims(decoder_inputs[0], 1)

            for i in xrange(self.max_num_steps):
                if i > 0: scope.reuse_variables()

                # exam action of current step
                search_left_to_right = []
                batch_stack_indices = []
                batch_input_indices = []
                for j in xrange(self.batch_size):
                    control_symbol = self.is_no_expand(self.input[j, -1, 0])
                    search_left_to_right.append(control_symbol)
                    stack_index = tf.cond(search_left_to_right[j],
                                    lambda: tf.cond(last_search_left_to_right[j],
                                                    lambda: self.grandgrandparent(j),
                                                    lambda: self.grandparent(j)),
                                    lambda: self.parent(j))
                    input_index = tf.cond(search_left_to_right[j],
                                    lambda: tf.cond(last_search_left_to_right[j],
                                                    lambda: self.grandparent(j),
                                                    lambda: self.parent(j)),
                                    lambda: tf.constant([]))
                    batch_stack_indices.append(stack_index)
                    batch_input_indices.append(input_index)

                batch_outputs = []
                batch_cells = []
                batch_hss = []
                if self.use_attention:
                    batch_new_attns = []
                    batch_input, batch_states, batch_attns = self.peek(batch_input_indices,
                                                                       batch_stack_indices)
                    batch_input_embeddings = tf.split(0, self.batch_size,
                        tf.nn.embedding_lookup(self.embeddings, batch_input))
                    for j in xrange(self.batch_size):
                        input = batch_input_embeddings[j]
                        state = batch_states[j]
                        attns = batch_attns[j]
                        output, cell, hs, attns = tf.cond(search_left_to_right[j],
                            lambda: self.attention_cell(parent_cell, parent_scope, input, state, attns,
                                                       hidden_features, attn_vecs, num_heads, hidden),
                            lambda: self.attention_cell(sb_cell, sb_scope, input, state, attns,
                                                       hidden_features, attn_vecs, num_heads, hidden))
                        batch_outputs.append(output)
                        batch_cells.append(cell)
                        batch_hss.append(hs)
                        batch_new_attns.append(attns)
                else:
                    batch_input_indices, batch_states = self.peek()
                    batch_input_embeddings = tf.split(0, self.batch_size,
                        tf.nn.embedding_lookup(self.embeddings, batch_input_indices))
                    for j in xrange(self.batch_size):
                        input = batch_input_embeddings[j]
                        state = batch_states[j]
                        output, cell, hs = tf.cond(search_left_to_right[j],
                            lambda: self.normal_cell(parent_cell, parent_scope, input, state),
                            lambda: self.normal_cell(sb_cell, sb_scope, input, state))
                        batch_outputs.append(output)
                        batch_cells.append(cell)
                        batch_hss.append(hs)

                # storing states
                if feed_previous:
                    # Project decoder output for next state input.
                    batch_output = tf.concat(0, batch_outputs)
                    batch_projected_output = tf.matmul(batch_output, W) + b
                    batch_next_input = tf.argmax(batch_projected_output, 1)
                else:
                    batch_next_input = decoder_inputs[i+1]

                if self.use_attention:
                    self.push([batch_next_input, tf.concat(0, batch_input_indices),
                                                 tf.concat(0, batch_cells),
                                                 tf.concat(0, batch_hss),
                                                 tf.concat(0, batch_new_attns)])
                else:
                    self.push([batch_next_input, tf.concat(0, batch_input_indices),
                                                 tf.concat(0, batch_cells),
                                                 tf.concat(0, batch_hss)])
                last_search_left_to_right = search_left_to_right

                outputs.append(output)

        return outputs, tf.nn.rnn_cell.LSTMStateTuple(cell, hs)


    """def define_beam_decoding_graph(self, encoder_state, embeddings,
                               attention_states, num_heads, initial_state_attention,
                               beam_size, top_k):
        # scope of output_projection is the entire model
        # hence retrieving variables here
        W, b = self.output_projection
        print("basic_tree_encoder: " + W.name)
        print("basic_tree_encoder: " + b.name)

        # share parameters with the basic decoder
        with tf.variable_scope("basic_tree_decoder") as scope:
            init_decoder_input = tf.constant(data_utils.ROOT_ID, shape=[self.batch_size, 1])

            parent_cell, parent_scope = self.parent_cell()
            sb_cell, sb_scope = self.sb_cell()
            outputs = []

            # search control
            init_input = tf.nn.embedding_lookup(embeddings, init_decoder_input)
            control_symbol = init_decoder_input

            # continuous stack used for storing LSTM states, synced with self.back_pointers
            if self.use_attention:
                hidden, hidden_features, attn_vecs = \
                    self.attention_hidden_layer(attention_states, num_heads)
                batch_size = tf.shape(attention_states)[0]
                attn_dim = tf.shape(attention_states)[2]
                batch_attn_size = tf.pack([batch_size, attn_dim])
                attns = tf.concat(1, [tf.zeros(batch_attn_size, dtype=tf.float32)    # initial attention state
                         for _ in xrange(num_heads)])
                attns.set_shape([self.batch_size, num_heads * attention_states.get_shape()[2].value])
                if initial_state_attention:
                    attns = self.attention(encoder_state, hidden_features, attn_vecs, num_heads, hidden)
                init_stack = tf.concat(1, [init_input, encoder_state[0], encoder_state[1], attns])
            else:
                init_stack = tf.concat(1, [init_input, encoder_state[0], encoder_state[1]])
            self.stack = tf.zeros([self.max_num_steps, init_stack.get_shape()[1].value])
            self.stack = tf.concat(0, [self.stack, init_stack])

            for i in xrange(self.max_num_steps):
                if i > 0: scope.reuse_variables()

                # mimick a stack pop if current symbol is <NO_EXPAND>
                self.back_pointers = tf.cond(search_left_to_right, lambda: self.cs_pop(), lambda: self.back_pointers)
                stack = tf.cond(search_left_to_right, lambda: self.pop(), lambda: stack)

                if self.use_attention:
                    input, state, attns = self.peek()
                    output, cell, hs, attns = tf.cond(search_left_to_right,
                        lambda: self.attention_cell(parent_cell, parent_scope, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden),
                        lambda: self.attention_cell(sb_cell, sb_scope, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden))
                else:
                    input, state = self.peek()
                    output, cell, hs = tf.cond(search_left_to_right,
                        lambda: self.normal_cell(parent_cell, parent_scope, input, state),
                        lambda: self.normal_cell(sb_cell, sb_scope, input, state))

                # mimick a stack pop if current symbol is <NO_EXPAND>
                self.back_pointers = tf.cond(search_left_to_right, lambda: self.cs_pop(), lambda: self.back_pointers)
                self.stack = tf.cond(search_left_to_right, lambda: self.pop(), lambda: stack)

                # Project decoder output for next state input.
                projected_output = tf.matmul(output, W) + b
                control_symbol = tf.argmax(projected_output, 1)
                next_input = tf.nn.embedding_lookup(embeddings, control_symbol)
                self.back_pointers = self.cs_push(tf.cast(tf.expand_dims(control_symbol, 1), tf.int32))

                if self.use_attention:
                    self.stack = self.push([next_input, cell, hs, attns])
                else:
                    self.stack = self.push([next_input, cell, hs])

                outputs.append(output)

        return outputs, tf.nn.rnn_cell.LSTMStateTuple(cell, hs)
    """

    def grandgrandparent(self, j):
        return tf.nn.embedding_lookup(self.back_pointers[j, :, 0], self.grandparent[j])

    def grandparent(self, j):
        return tf.nn.embedding_lookup(self.back_pointers[j, :, 0], self.parent[j])

    def parent(self, j):
        return self.back_pointers[j, -1, 0]

    def push(self, batch_states):
        """
        :param batch_states: list of list of state tensors
        """
        self.input = tf.concat(1, [self.input, tf.expand_dims(batch_states[0], 1)])
        self.back_pointers = tf.concat(1, [self.back_pointers, tf.expand(batch_states[1], 1)])
        batch_states = tf.concat(1, batch_states[2:])
        self.stack = tf.concat(1, [self.stack, tf.expand_dims(batch_states, 1)])


    def peek(self, batch_input_indices, batch_stack_indices):
        """
        :param batch_indices: list of stack pointers for each search thread
        :return: batch stack state tuples
                 (batch_parent_states, [batch_attention_states])
        """
        input_array = tf.split(0, self.batch_size, self.input)
        stack_array = tf.split(0, self.batch_size, self.stack)
        batch_input_symbols = tf.nn.embedding_lookup(input_array, batch_input_indices)
        batch_stack_states = tf.nn.embedding_lookup(stack_array, batch_stack_indices)

        batch_stack_cells = batch_stack_states[:, 1:self.dim+1]
        batch_stack_hiddens = batch_stack_states[:, self.dim+1:2*self.dim+1]
        if self.use_attention:
            batch_attention_states = batch_stack_states[:, 2*self.dim+1:]
            return (tf.split(0, self.batch_size, batch_input_symbols),
                    [tf.nn.rnn_cell.LSTMStateTuple(cell, hidden) for (cell, hidden) in
                     zip(tf.split(0, self.batch_size, batch_stack_cells),
                         tf.split(0, self.batch_size, batch_stack_hiddens))],
                    tf.split(0, self.batch_size, batch_attention_states))
        else:
            return (tf.split(0, self.batch_size, batch_input_symbols),
                    [tf.nn.rnn_cell.LSTMStateTuple(cell, hidden) for (cell, hidden) in
                     zip(tf.split(0, self.batch_size, batch_stack_cells),
                         tf.split(0, self.batch_size, batch_stack_hiddens))])


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
