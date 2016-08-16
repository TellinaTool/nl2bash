"""Sequence-to-tree model with an attention mechanism."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import numpy as np
import sys
sys.path.append("../seq2seq")

import tensorflow as tf

import data_utils


class Seq2TreeModel(object):
    """Sequence-to-tree model with attention.
    """

    _NO_EXPAND = tf.constant(data_utils.NO_EXPAND_ID)

    def __init__(self, hyperparams, forward_only=False):
        """
        Create the model.
        :param hyperparams: hyperparameters of learning
        :param use_attention: if set, use attention
        :param forward_only: if set, we do not construct the backward pass.
        """

        self.hyperparams = hyperparams

        self.learning_rate = tf.Variable(float(hyperparams["learning_rate"]), trainable=False)
        self.learning_rate_decay_op = self.learning_rate.assign(
            self.learning_rate * hyperparams["learning_rate_decay_factor"])
        self.global_step = tf.Variable(0, trainable=False)

        # variable sharing
        self.attention_cell_vars = False

        self.create_graph(forward_only)


    def format_example(self, encoder_input, decoder_input):
        """Prepare data to feed in step()"""
        encoder_size = self.max_source_length
        decoder_size = self.max_target_length
        encoder_inputs = []
        decoder_inputs = []

        # Encoder inputs are padded and then reversed
        encoder_pad = [data_utils.PAD_ID] * (encoder_size - len(encoder_input))
        encoder_inputs.append(list(reversed(encoder_input + encoder_pad)))

        # Decoder inputs always start with "ROOT" and are padded
        decoder_pad = [data_utils.PAD_ID] * (decoder_size - len(decoder_inputs))
        decoder_inputs.append(decoder_input + decoder_pad)

        # create batch-major vectors
        batch_encoder_inputs, batch_decoder_inputs, batch_weights = [], [], []

        # Batch encoder inputs are just re-indexed encoder_inputs.
        for length_idx in xrange(encoder_size):
            batch_encoder_inputs.append(
                np.array([encoder_inputs[batch_idx][length_idx]
                        for batch_idx in xrange(self.batch_size)], dtype=np.int32))

        # Batch decoder inputs are re-indexed decoder_inputs, we create weights.
        for length_idx in xrange(decoder_size):
            batch_decoder_inputs.append(
                np.array([decoder_inputs[batch_idx][length_idx]
                        for batch_idx in xrange(self.batch_size)], dtype=np.int32))

            # Create target_weights to be 0 for targets that are padding.
            batch_weight = np.ones(self.batch_size, dtype=np.float32)
            for batch_idx in xrange(self.batch_size):
                # We set weight to 0 if the corresponding target is a PAD symbol.
                # The corresponding target is decoder_input shifted by 1 forward.
                if length_idx < decoder_size - 1:
                    target = decoder_inputs[batch_idx][length_idx + 1]
                if length_idx == decoder_size - 1 or target == data_utils.PAD_ID:
                    batch_weight[batch_idx] = 0.0
            batch_weights.append(batch_weight)

        return batch_encoder_inputs, batch_decoder_inputs, batch_weights


    def step(self, session, encoder_inputs, decoder_inputs, target_weights,
             forward_only):
        """Run a step of the model feeding the given inputs.
        :param session: tensorflow session to use.
        :param encoder_inputs: list of numpy int vectors to feed as encoder inputs.
        :param decoder_inputs: list of numpy int vectors to feed as decoder inputs.
        :param target_weights: list of numpy float vectors to feed as target weights.
        :param forward_only: whether to do the backward step or only forward.
        :return (gradient_norm, average_perplexity, outputs)
        """

        encoder_size = len(encoder_inputs)
        decoder_size = len(decoder_inputs)

        assert(encoder_size == self.max_source_length)
        assert(decoder_size == self.max_target_length)

        # Input feed: encoder inputs, decoder inputs, target_weights, as provided.
        input_feed = {}
        for l in xrange(encoder_size):
            input_feed[self.encoder_inputs[l].name] = encoder_inputs[l]
        for l in xrange(decoder_size):
            input_feed[self.decoder_inputs[l].name] = decoder_inputs[l]
            input_feed[self.target_weights[l].name] = target_weights[l]

        # Since our targets are decoder inputs shifted by one, we need one more.
        last_target = self.decoder_inputs[decoder_size].name
        input_feed[last_target] = np.zeros([self.batch_size], dtype=np.int32)

        # Output feed: depends on whether we do a backward step or not.
        if not forward_only:
            output_feed = [self.updates,            # Update Op that does SGD.
                           self.gradient_norms,     # Gradient norm.
                           self.losses]             # Loss for this batch.
        else:
            output_feed = [self.losses]  # Loss for this batch.
            for l in xrange(decoder_size):  # Output logits.
                output_feed.append(self.outputs[l])

        outputs = session.run(output_feed, input_feed)

        if not forward_only:
            return outputs[1], outputs[2], None  # Gradient norm, loss, no outputs.
        else:
            return None, outputs[0], outputs[1:]  # No gradient norm, loss, outputs.


    def create_graph(self, forward_only):
        # Feeds for inputs.
        self.encoder_inputs = []  # encoder inputs.
        self.decoder_inputs = []  # decoder inputs (always start with "root").
        self.target_weights = []  # weights at each position of the target sequence.
        for i in xrange(self.max_source_length):
            self.encoder_inputs.append(tf.placeholder(tf.int32, shape=[None],
                                                      name="encoder{0}".format(i)))
        for i in xrange(self.max_target_length + 1):
            self.decoder_inputs.append(tf.placeholder(tf.int32, shape=[None],
                                                      name="decoder{0}".format(i)))
            self.target_weights.append(tf.placeholder(tf.float32, shape=[None],
                                                      name="weight{0}".format(i)))

        # Our targets are decoder inputs shifted by one.
        self.targets = [self.decoder_inputs[i + 1]
                        for i in xrange(self.max_target_length)]

        # Training outputs and losses.
        self.forward(forward_only)

        # Gradients and SGD update operation for training the model
        params = tf.trainable_variables()
        if not forward_only:
            self.gradient_norms = []
            self.updates = []

        if self.hyperparams["optimizer"] == "sgd":
            opt = tf.train.GradientDescentOptimizer(self.learning_rate)
        elif self.hyperparams["optimizer"] == "adam":
            opt = tf.train.AdamOptimizer(self.learning_rate, beta1=0.9, beta2=0.999,
                                         epsilon=1e-08)

        gradients = tf.gradients(self.losses, params)
        clipped_gradients, norm = tf.clip_by_global_norm(gradients,
                                                         self.max_gradient_norm)

        self.gradient_norms.append(norm)
        self.updates.append(opt.apply_gradients(zip(clipped_gradients, params),
                                                global_step=self.global_step))

        self.saver = tf.train.Saver(tf.all_variables())

    # Create the multi-layer cell for the tree RNN.
    def create_multilayer_cell(self, type):
        if type == "lstm":
            cell = tf.nn.rnn_cell.BasicLSTMCell(self.dim, state_is_tuple=True)
        if self.num_layers > 1:
            cell = tf.nn.rnn_cell.MultiRNNCell([cell] * self.num_layers)
        if self.input_keep_prob < 1 or self.output_keep_prob < 1:
            cell = tf.nn.rnn_cell.DropoutWrapper(cell,
                                                 input_keep_prob=self.input_keep_prob,
                                                 output_keep_prob=self.output_keep_prob)
        return cell


    def forward(self, forward_only):
        # Encoder.
        encoder_cell = self.create_multilayer_cell("lstm")
        encoder_cell = tf.nn.rnn_cell.EmbeddingWrapper(
            encoder_cell,
            embedding_classes=self.source_vocab_size,
            embedding_size=self.dim)
        encoder_outputs, encoder_state = tf.nn.rnn(encoder_cell,
                                                   self.encoder_inputs,
                                                   dtype=tf.float32)

        if self.use_attention:
            top_states = [tf.reshape(e, [-1, 1, self.dim]) for e in encoder_outputs]
            attention_states = tf.concat(1, top_states)

        # Decoder.
        if self.decoder_topology == "basic":
            if self.use_attention:
                outputs, state = self.basic_tree_decoder(encoder_state,
                                                         attention_states,
                                                         feed_previous=forward_only)
            else:
                outputs, state = self.basic_tree_decoder(encoder_state,
                                                         feed_previous=forward_only)

        # Losses.
        self.losses = self.sequence_loss(outputs, self.softmax_loss())

        # Project decoder outputs for decoding.
        if forward_only:
            W, b = self.output_projection()
            self.outputs = []
            for i in xrange(len(outputs)):
                self.outputs.append((tf.matmul(outputs[i], W) + b))


    def basic_tree_decoder(self, encoder_state, attention_states=None, num_heads=1,
                           initial_state_attention=False, feed_previous=False):
        """
        :param encoder_state: hidden state of the encoder
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

        :return: Output states and final hidden state of the decoder. Need output_projection
                 to obtain distribution over output vocabulary.
        """

        if not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be known %s"
                             % attention_states.get_shape())

        with tf.variable_scope("basic_tree_decoder") as scope:
            embeddings = self.target_embeddings()
            embedding_inputs = [tf.nn.embedding_lookup(embeddings, i) for i in self.decoder_inputs]

            parent_cell = self.create_multilayer_cell("lstm")
            sb_cell = self.create_multilayer_cell("lstm")
            outputs = []

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

            # search control
            init_input = embedding_inputs[0]
            if self.use_attention:
                self.stack = tf.concat(1, [init_input, encoder_state[0], encoder_state[1], attns])
            else:
                self.stack = tf.concat(1, [init_input, encoder_state[0], encoder_state[1]])

            for i, control_symbol in enumerate(self.decoder_inputs):
                if i > 0: scope.reuse_variables()

                if self.use_attention:
                    output, state, attns = \
                        tf.cond(self.is_no_expand(control_symbol),
                                lambda: self.left_to_right_with_attention(
                                    sb_cell, hidden_features, attn_vecs, num_heads, hidden),
                                lambda: self.top_to_bottom_with_attention(
                                    parent_cell, hidden_features, attn_vecs, num_heads, hidden))
                    if i < len(self.decoder_inputs) - 1:
                        if feed_previous:
                            next_input = tf.nn.embedding_lookup(embeddings, tf.argmax(output, 1))
                        else:
                            next_input = embedding_inputs[i+1]
                        self.push([next_input, state[0], state[1], attns])
                else:
                    output, state = tf.cond(self.is_no_expand(control_symbol),
                                            lambda: self.left_to_right(sb_cell),
                                            lambda: self.top_to_bottom(parent_cell))
                    if i < len(self.decoder_inputs) - 1:
                        if feed_previous:
                            next_input = tf.nn.embedding_lookup(embeddings, tf.argmax(output, 1))
                        else:
                            next_input = embedding_inputs[i+1]
                        self.push([next_input, state[0], state[1]])

                outputs.append(output)

        return outputs, state

    def top_to_bottom_with_attention(self, cell, hidden_features, attn_vecs, num_heads, hidden):
        input, state, attns = self.peek()
        output, state, attns = self.attention_cell(cell, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden)
        return output, state, attns

    def top_to_bottom(self, cell):
        input, state = self.peek()
        output, state = cell(input, state)
        return output, state

    def left_to_right_with_attention(self, cell, hidden_features, attn_vecs, num_heads, hidden):
        self.pop()
        input, state, attns = self.peek()
        output, state, attns = self.attention_cell(cell, input, state, attns,
                                                   hidden_features, attn_vecs, num_heads, hidden)
        self.pop()
        return output, state, attns

    def left_to_right(self, cell):
        self.pop()
        input, state = self.peek()
        output, state = cell(input, state)
        self.pop()
        return output, state

    def push(self, states):
        new_top_state = tf.concat(1, states)
        self.stack = tf.concat(0, [self.stack, new_top_state])

    def peek(self):
        top_state = tf.slice(self.stack, [self.stack.get_shape()[0].value-1, 0], [1, self.stack.get_shape()[1].value])
        if self.use_attention:
            return tf.slice(top_state, [0, 0], [1, self.dim]), \
                   (tf.slice(top_state, [0, self.dim], [1, self.dim]),
                    tf.slice(top_state, [0, 2 * self.dim], [1, self.dim])), \
                   tf.slice(top_state, [0, 3 * self.dim], [1, self.stack.get_shape()[1].value - 3 * self.dim])
        else:
            return tf.slice(top_state, [0, 0], [1, self.dim]), \
                   (tf.slice(top_state, [0, self.dim], [1, self.dim]),
                    tf.slice(top_state, [0, 2 * self.dim], [1, self.dim]))

    def pop(self):
        self.stack = tf.slice(self.stack, [0, 0], [self.stack.get_shape()[0].value-1, self.stack.get_shape()[1].value])


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


    def attention_cell(self, cell, input_embedding, state, attns,
                       hidden_features, attn_vecs, num_heads, hidden):
        with tf.variable_scope("AttnInputProjection"):
            if self.attention_cell_vars:
                tf.get_variable_scope().reuse_variables()
            # attention mechanism on cell and hidden states
            x = tf.nn.rnn_cell._linear([input_embedding] + [attns], self.dim, True)
            cell_output, state = cell(x, state)
            attns = self.attention(state, hidden_features, attn_vecs, num_heads, hidden)
        with tf.variable_scope("AttnOutputProjection"):
            if self.attention_cell_vars:
                tf.get_variable_scope().reuse_variables()
            # attention mechanism on output state
            output = tf.nn.rnn_cell._linear([cell_output] + [attns], self.dim, True)
        self.attention_cell_vars = True
        return output, state, attns


    def sequence_loss(self, logits, loss_function):
        if len(self.targets) != len(logits) or len(self.target_weights) != len(logits):
            raise ValueError("Lengths of logits, targets and target_weights must be the same "
                             "%d, %d, %d." % (len(logits), len(self.targets), len(self.target_weights)))
        with tf.variable_scope("sequence_loss"):
            log_perp_list = []
            for logit, target, weight in zip(logits, self.targets, self.target_weights):
                crossent = loss_function(logit, target)
                log_perp_list.append(crossent * weight)
            log_perps = tf.add_n(log_perp_list)
            total_size = tf.add_n(self.target_weights)
            total_size += 1e-12  # Just to avoid division by 0 for all-0 weights.
            log_perps /= total_size
        return log_perps


    def is_no_expand(self, ind):
        return tf.equal(ind, Seq2TreeModel._NO_EXPAND)

    def source_embeddings(self):
        with tf.variable_scope("source_embeddings"):
            sqrt3 = math.sqrt(3)
            initializer = tf.random_normal_initializer(-sqrt3, sqrt3)
            embeddings = tf.get_variable("embedding", [self.source_vocab_size,
                                                       self.dim],
                                         initializer=initializer)
            return embeddings

    def target_embeddings(self):
        with tf.variable_scope("target_embeddings"):
            sqrt3 = math.sqrt(3)
            initializer = tf.random_normal_initializer(-sqrt3, sqrt3)
            embeddings = tf.get_variable("embedding", [self.target_vocab_size,
                                                       self.dim],
                                         initializer=initializer)
            return embeddings

    def output_projection(self):
        with tf.variable_scope("output_projection"):
            w = tf.get_variable("proj_w", [self.dim, self.target_vocab_size])
            b = tf.get_variable("proj_b", [self.target_vocab_size])
            tf.get_variable_scope().reuse_variables()
        return (w, b)

    def softmax_loss(self):
        if self.use_sampled_softmax():
            w_t, b = self.output_projection()

            def sampled_loss(inputs, labels):
                labels = tf.reshape(labels, [-1, 1])
                return tf.nn.sampled_softmax_loss(w_t, b, inputs, labels, self.num_samples,
                                                  self.target_vocab_size)

            loss_function = sampled_loss
        else:
            loss_function = tf.nn.softmax_cross_entropy_with_logits
        return loss_function

    def use_sampled_softmax(self):
        return self.num_samples > 0 and self.num_samples < self.target_vocab_size

    @property
    def use_attention(self):
        return self.hyperparams["attention"]

    @property
    def decoder_topology(self):
        return self.hyperparams["decoder_topology"]

    @property
    def dim(self):
        return self.hyperparams["dim"]

    @property
    def batch_size(self):
        return self.hyperparams["batch_size"]

    @property
    def input_keep_prob(self):
        return self.hyperparams["input_keep_prob"]

    @property
    def output_keep_prob(self):
        return self.hyperparams["output_keep_prob"]

    @property
    def max_gradient_norm(self):
        return self.hyperparams["max_gradient_norm"]

    @property
    def num_samples(self):
        return self.hyperparams["num_samples"]

    @property
    def num_layers(self):
        return self.hyperparams["num_layers"]

    @property
    def source_vocab_size(self):
        return self.hyperparams["source_vocab_size"]

    @property
    def target_vocab_size(self):
        return self.hyperparams["target_vocab_size"]

    @property
    def max_source_length(self):
        return self.hyperparams["max_source_length"]

    @property
    def max_target_length(self):
        return self.hyperparams["max_target_length"]
