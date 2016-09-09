"""A set of tree decoder modules used in the encoder-decoder framework."""

import tensorflow as tf
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "seq2seq"))

import data_utils, graph_utils

class Decoder(object):
    def __init__(self, dim, batch_size, rnn_cell, num_layers,
                 input_keep_prob, output_keep_prob,
                 use_attention, use_copy, output_projection=None):
        self.dim = dim
        self.rnn_cell = rnn_cell
        self.batch_size = batch_size
        self.num_layers = num_layers
        self.input_keep_prob = input_keep_prob
        self.output_keep_prob = output_keep_prob
        self.use_attention = use_attention
        self.use_copy = use_copy

        self.output_projection = output_projection

        # variable sharing
        self.attention_vars = False
        self.attention_cell_vars = False
        self.attention_hidden_vars = False

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
        return output, state, attns

    def attention(self, state, hidden_features, attn_vecs, num_heads, hidden):
        assert(len(attn_vecs) > 0)
        attn_vec_dim = attn_vecs[0].get_shape()[0].value
        attn_length = hidden.get_shape()[1].value
        attn_dim = hidden.get_shape()[3].value
        """Put attention masks on hidden using hidden_features and query."""
        ds = []  # Results of attention reads will be stored here.
        for a in xrange(num_heads):
            with tf.variable_scope("Attention_%d" % a):
                if self.attention_vars:
                    tf.get_variable_scope().reuse_variables()
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
        self.attention_vars = True
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
            with tf.variable_scope("AttnW_%d" % i):
                if self.attention_hidden_vars:
                    tf.get_variable_scope().reuse_variables()
                k = tf.get_variable("AttnW_%d" % i, [1, 1, attn_dim, attn_vec_dim])
                hidden_features.append(tf.nn.conv2d(hidden, k, [1,1,1,1], "SAME"))
                attn_vecs.append(tf.get_variable("AttnV_%d" % i, [attn_vec_dim]))
        self.attention_hidden_vars = True
        return hidden, hidden_features, attn_vecs


    def normal_cell(self, cell, scope, input, state):
        try:
            output, state = cell(input, state, scope)
        except ValueError, e:
            scope.reuse_variables()
            print(state)
            output, state = cell(input, state, scope)
        return output, state


class BasicTreeDecoder(Decoder):

    def __init__(self, dim, batch_size, rnn_cell, num_layers,
                 input_keep_prob, output_keep_prob,
                 use_attention, use_copy, output_projection=None):
        super(BasicTreeDecoder, self).__init__(dim, batch_size, rnn_cell, num_layers,
                                               input_keep_prob, output_keep_prob,
                                               use_attention, use_copy, output_projection)
        self.vertical_cell = self.vertical_cell()
        self.horizontal_cell = self.horizontal_cell()

        self.H_NO_EXPAND = tf.constant(data_utils.H_NO_EXPAND_ID, shape=[self.batch_size])
        self.V_NO_EXPAND = tf.constant(data_utils.V_NO_EXPAND_ID, shape=[self.batch_size])
    
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

        if self.use_attention and not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be known %s"
                             % attention_states.get_shape())

        if feed_previous:
            # scope of output_projection is shared by all decoders
            # hence retrieving variables here
            W, b = self.output_projection

        with tf.variable_scope("basic_tree_decoder") as scope:
            vertical_cell, vertical_scope = self.vertical_cell
            horizontal_cell, horizontal_scope = self.horizontal_cell
            outputs = []

            # search control
            self.back_pointers = tf.constant(-1, shape=[self.batch_size, 1, 1], dtype=tf.int32)

            # continuous stack used for storing LSTM states, synced with self.back_pointers
            if self.rnn_cell == "gru":
                init_state = encoder_state
            else:
                init_state = tf.concat(1, [encoder_state[0], encoder_state[1]])

            if self.use_attention:
                hidden, hidden_features, attn_vecs = \
                    self.attention_hidden_layer(attention_states, num_heads)
                batch_size = tf.shape(attention_states)[0]
                attn_dim = tf.shape(attention_states)[2]
                batch_attn_size = tf.pack([batch_size, attn_dim])
                # initial attention state
                attns = tf.concat(1, [tf.zeros(batch_attn_size, dtype=tf.float32)
                         for _ in xrange(num_heads)])
                if initial_state_attention:
                    attns = self.attention(encoder_state, hidden_features, attn_vecs, num_heads, hidden)
                attns.set_shape([self.batch_size, num_heads * attention_states.get_shape()[2].value])
                init_state = tf.concat(1, [init_state, attns])

            self.state = tf.expand_dims(init_state, 1)
            self.input = tf.expand_dims(decoder_inputs[0], 1)
            self.input = tf.expand_dims(self.input, 1)
            self.input.set_shape([self.batch_size, 1, 1])
            search_left_to_right_next = self.is_no_expand(self.input[:, -1, 0])

            for i in xrange(len(decoder_inputs)):
                # print("decoder step: %d" % i)
                if i > 0: scope.reuse_variables()

                if self.use_attention:
                    input, state, attns = self.peek()
                else:
                    input, state = self.peek()
                
                input_embeddings = tf.squeeze(tf.nn.embedding_lookup(self.embeddings, input),
                                              squeeze_dims=[1])
                search_left_to_right = search_left_to_right_next

                if self.use_attention:
                    v_output, v_state, v_attns = self.attention_cell(
                        vertical_cell, vertical_scope, input_embeddings, state, attns,
                        hidden_features, attn_vecs, num_heads, hidden)
                    h_output, h_state, h_attns = self.attention_cell(
                        horizontal_cell, horizontal_scope, input_embeddings, state, attns,
                        hidden_features, attn_vecs, num_heads, hidden)
                else:
                    v_output, v_state = self.normal_cell(
                        vertical_cell, vertical_scope, input_embeddings, state)
                    h_output, h_state = self.normal_cell(
                        horizontal_cell, horizontal_scope, input_embeddings, state)

                batch_output = graph_utils.map_fn(lambda x: tf.cond(x[0], lambda : x[1], lambda : x[2]),
                                          [search_left_to_right, h_output, v_output])
                print("back_output.get_shape(): {}".format(batch_output.get_shape()))

                if self.rnn_cell == "gru":
                    batch_state = graph_utils.map_fn(lambda x: tf.cond(x[0], lambda : x[1], lambda : x[2]),
                                         [search_left_to_right, h_state, v_state])
                else:
                    batch_cell = graph_utils.map_fn(lambda x: tf.cond(x[0], lambda : x[1], lambda : x[2]),
                                            [search_left_to_right, h_state[0], v_state[0]])
                    batch_hs = graph_utils.map_fn(lambda x: tf.cond(x, lambda : x[1], lambda : x[2]),
                                            [search_left_to_right, h_state[1], v_state[1]])
                    batch_state = tf.concat(1, [batch_cell, batch_hs])

                if self.use_attention:
                    batch_attns = graph_utils.map_fn(lambda x: tf.cond(x, lambda : x[1], lambda : x[2]),
                                            [search_left_to_right, h_attns[1], v_attns[1]])
                    batch_state = tf.concat(1, [batch_state, batch_attns])

                # record output state to compute the loss.
                outputs.append(batch_output)

                if i < len(decoder_inputs) - 1:
                    # storing states
                    if feed_previous:
                        # Project decoder output for next state input.
                        batch_projected_output = tf.matmul(batch_output, W) + b
                        batch_output_symbol = tf.argmax(batch_projected_output, 1)
                        batch_output_symbol = tf.cast(batch_output_symbol, dtype=tf.int32)
                    else:
                        batch_output_symbol = decoder_inputs[i+1]
                    search_left_to_right_next = self.is_no_expand(batch_output_symbol)

                    back_pointer = graph_utils.map_fn(self.back_pointer,
                                             [search_left_to_right_next,
                                              search_left_to_right,
                                              self.grandparent(),
                                              self.parent(),
                                              tf.constant(i, shape=[self.batch_size])],
                                             back_prop=True)
                    print("back_pointer.get_shape(): {}".format(back_pointer.get_shape()))
                    next_input = graph_utils.map_fn(self.next_input,
                                           [search_left_to_right_next,
                                            search_left_to_right,
                                            self.parent_input(),
                                            self.get_input(),
                                            batch_output_symbol],
                                           back_prop=True)
                    print("next_input.get_shape(): {}".format(next_input.get_shape()))
                    next_state = graph_utils.map_fn(self.next_state,
                                           [search_left_to_right_next,
                                            search_left_to_right,
                                            self.parent_state(),
                                            self.get_input(),
                                            batch_state],
                                           back_prop=True)
                    print("next_state.get_shape(): {}".format(next_state.get_shape()))
                    self.push([next_input, back_pointer, next_state])

        if self.rnn_cell == "gru":
            final_batch_state = batch_state
        elif self.rnn_cell == "lstm":
            final_batch_state = tf.nn.rnn_cell.LSTMStateTuple(batch_cell, batch_hs)

        return outputs, final_batch_state


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

            vertical_cell, vertical_scope = self.vertical_cell()
            horizontal_cell, horizontal_scope = self.horizontal_cell()
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
                        lambda: self.attention_cell(vertical_cell, vertical_scope, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden),
                        lambda: self.attention_cell(horizontal_cell, horizontal_scope, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden))
                else:
                    input, state = self.peek()
                    output, cell, hs = tf.cond(search_left_to_right,
                        lambda: self.normal_cell(vertical_cell, vertical_scope, input, state),
                        lambda: self.normal_cell(horizontal_cell, horizontal_scope, input, state))

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

    def back_pointer(self, x):
        h_search_next, h_search, grandparent, parent, current = x
        return tf.cond(h_search_next,
                       lambda : tf.cond(h_search, lambda : grandparent, lambda : parent),
                       lambda : tf.cond(h_search, lambda : parent, lambda : current))

    def next_input(self, x):
        h_search_next, h_search, parent, current, next = x
        return tf.cond(h_search_next,
                       lambda : tf.cond(h_search, lambda : parent, lambda : current),
                       lambda : next)

    def next_state(self, x):
        h_search_next, h_search, parent, current, next = x
        return tf.cond(h_search_next,
                       lambda : tf.cond(h_search, lambda : parent, lambda : current),
                       lambda : next)

    def grandparent(self):
        graph_utils.map_fn(lambda x: tf.nn.embedding_lookup(x[0], x[1]),
                  [self.back_pointers[:, :, 0], self.parent()])

    def parent(self):
        p = self.back_pointers[:, -1, 0]
        # search that went beyond ROOT node will be discarded
        graph_utils.map_fn(lambda x: tf.cond(tf.equal(x, tf.constant(-1)), lambda: x, lambda: tf.constant(0)),
                  [p])

    def parent_input(self):
        graph_utils.map_fn(lambda x: tf.nn.embedding_lookup(x[0], x[1]),
                  [self.input[:, :, 0], self.parent()])

    def parent_state(self):
        graph_utils.map_fn(lambda x: tf.nn.embedding_lookup(x[0], x[1]),
                  [self.state[:, :, :], self.parent()])

    def get_input(self):
        return self.input[:, -1, 0]

    def get_state(self):
        return self.state[:, -1, :]

    def push(self, batch_states):
        """
        :param batch_states: list of list of state tensors
        """
        batch_next_input = batch_states[0]
        # print(batch_next_input.get_shape())
        batch_next_input = tf.expand_dims(batch_next_input, 1)
        batch_next_input = tf.expand_dims(batch_next_input, 1)
        # print(self.input.get_shape())
        self.input = tf.concat(1, [self.input, batch_next_input])

        batch_back_pointers = batch_states[1]
        batch_back_pointers = tf.expand_dims(batch_back_pointers, 1)
        batch_back_pointers = tf.expand_dims(batch_back_pointers, 1)
        self.back_pointers = tf.concat(1, [self.back_pointers, batch_back_pointers])

        batch_states = tf.expand_dims(batch_states[2], 1)
        self.state = tf.concat(1, [self.state, batch_states])


    def peek(self):
        """
        :param batch_indices: list of stack pointers for each search thread
        :return: batch stack state tuples
                 (batch_parent_states, [batch_attention_states])
        """
        batch_input_symbols = self.input[:, -1, :]
        batch_stack_states = self.state[:, -1, :]

        if self.rnn_cell == "gru":
            batch_states = batch_stack_states[:, :self.dim]
            attn_start_pos = self.dim
        elif self.rnn_cell == "lstm":
            batch_stack_cells = batch_stack_states[:, :self.dim]
            batch_stack_hiddens = batch_stack_states[:, self.dim:2*self.dim]
            attn_start_pos = 2 * self.dim
            batch_states = tf.nn.rnn_cell.LSTMStateTuple(batch_stack_cells, batch_stack_hiddens)

        if self.use_attention:
            batch_attention_states = batch_stack_states[:, attn_start_pos:]
            return batch_input_symbols, batch_states, batch_attention_states
        else:
            return batch_input_symbols, batch_states


    def is_no_expand(self, ind):
        return tf.logical_or(self.no_vertical_expand(ind), self.no_horizontal_expand(ind))


    def no_vertical_expand(self, ind):
        return tf.equal(tf.cast(ind, tf.int32), self.V_NO_EXPAND)


    def no_horizontal_expand(self, ind):
        return tf.equal(tf.cast(ind, tf.int32), self.H_NO_EXPAND)


    def vertical_cell(self):
        """Cell that controls transition from parent to child."""
        with tf.variable_scope("vertical_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope, self.dim, self.num_layers,
                                                      self.input_keep_prob, self.output_keep_prob)
        return cell, scope


    def horizontal_cell(self):
        """Cell that controls transition from left sibling to right sibling."""
        with tf.variable_scope("horizontal_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope, self.dim, self.num_layers,
                                                      self.input_keep_prob, self.output_keep_prob)
        return cell, scope
