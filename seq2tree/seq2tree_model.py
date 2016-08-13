"""Sequence-to-tree model with an attention mechanism."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

import tensorflow as tf

import data_utils


class Seq2TreeModel(object):
    """Sequence-to-tree model with attention.
    """

    def __init__(self, hyperparams, source, target, forward_only=False):
        """
        Create the model.
        :param hyperparams: hyperparameters of learning
        :param sournce: indexed source input (sequentialized)
        :param target: indexed target input (sequentialized)
        :param use_attention: if set, use attention
        :param forward_only: if set, we do not construct the backward pass.
        """

        self.hyperparams = hyperparams
        self.source = source
        self.target = target

        self.learning_rate = tf.Variable(float(hyperparams["learning_rate"]), trainable=False)
        self.learning_rate_decay_op = self.learning_rate.assign(
            self.learning_rate * hyperparams["learning_rate_decay_factor"])
        self.global_step = tf.Variable(0, trainable=False)

        self.create_graph(forward_only)


    def create_graph(self, forward_only):
        # Create the multi-layer cell for the tree RNN.
        def create_multilayer_cell(type):
            if type == "lstm":
                single_cell = tf.nn.rnn_cell.BasicLSTMCell(self.dim)
            if self.num_layers > 1:
                cell = tf.nn.rnn_cell.MultiRNNCell([single_cell] * self.num_layers)
            if self.input_keep_prob < 1 or self.output_keep_prob < 1:
                cell = tf.nn.rnn_cell.DropoutWrapper(cell,
                                                     input_keep_prob=self.input_keep_prob,
                                                     output_keep_prob=self.output_keep_prob)
            return cell

        # Feeds for inputs.
        self.encoder_inputs = []  # encoder inputs.
        self.decoder_inputs = []  # decoder inputs (always start with "root").
        self.target_weights = []  # weights at each position of the target sequence.
        for i in xrange(len(self.source)):
            self.encoder_inputs.append(tf.placeholder(tf.int32, shape=[None],
                                                      name="encoder{0}".format(i)))
        for i in xrange(len(self.target) + 1):
            self.decoder_inputs.append(tf.placeholder(tf.int32, shape=[None],
                                                      name="decoder{0}".format(i)))
            self.target_weights.append(tf.placeholder(tf.float32, shape=[None],
                                                      name="weight{0}".format(i)))

        # Our targets are decoder inputs shifted by one.
        self.targets = [self.decoder_inputs[i + 1]
                        for i in xrange(len(self.target))]

        # Training outputs and losses.
        self.forward()

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


    def forward(self):
        # Encoder.
        encoder_cell = self.create_multilayer_cell("lstm")
        encoder_cell = tf.nn.rnn_cell.EmbeddingWrapper(
            encoder_cell,
            embedding_classes=self.source_vocab_size,
            embedding_size=self.dim)
        encoder_outputs, encoder_state = tf.nn.rnn(encoder_cell, self.encoder_inputs, dtype=tf.float32)

        if self.use_attention:
            top_states = [tf.reshape(e, [-1, 1, self.dim]) for e in encoder_outputs]
            attention_states = tf.concat(1, top_states)

        # Decoder.
        if self.decoder_topology == "basic":
            if self.use_attention:
                outputs, state = self.basic_tree_decoder(encoder_state, attention_states)
            else:
                outputs, state = self.basic_tree_decoder(encoder_state)

        # Losses.
        self.losses = self.sequence_loss(outputs, self.softmax_loss())

        # Project decoder outputs for decoding.
        W, b = self.output_projection()
        self.outputs = []
        for i in xrange(len(outputs)):
            self.outputs.append((tf.matmul(outputs[i], W) + b))

    def basic_tree_decoder(self, encoder_state, attention_states=None, num_heads=1,
                           initial_state_attention=False):
        """
        :param encoder_state: hidden state of the encoder
        :param attention_states: 3D Tensor [batch_size x attn_length x attn_dim].
        :param num_heads: Number of attention heads that read from from attention_states.
            Dummy field if attention_states is None.
        :param initial_state_attention: If False (default), initial attentions are zero.
            If True, initialize the attentions from the initial state and attention states
            -- useful to resume decoding from a previously stored decoder state and attention
            state.
        :return: Output states and final hidden state of the decoder. Need output_projection
                 to obtain distribution over output vocabulary.
        """

        if not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be known %s"
                             % attention_states.get_shape())

        embeddings = self.target_embeddings()
        embedding_inputs = (tf.nn.embedding_lookup(embeddings, i) for i in self.decoder_inputs)

        parent_cell = self.create_multilayer_cell("lstm")
        sb_cell = self.create_multilayer_cell("lstm")

        with tf.variable_scope("basic_tree_decoder") as scope:
            outputs = []

            if self.use_attention:
                hidden, hidden_features, attn_vecs = \
                    self.attention_hidden_layer(attention_states, num_heads)
                batch_size = attention_states.get_shape()[0].value
                attn_dim = attention_states.get_shape()[2].value
                batch_attn_size = tf.pack([batch_size, attn_dim])
                attns = [tf.zeros(batch_attn_size, dtype=tf.float32)    # initial attention state
                         for _ in xrange(num_heads)]
                if initial_state_attention:
                    attns = self.attention(encoder_state, hidden_features, attn_vecs, num_heads, hidden)

            # search control
            if self.use_attention:
                stack = [(self.decoder_inputs[0], encoder_state, attns)]
            else:
                stack = [(self.decoder_inputs[0], encoder_state)]

            for i, control_symbol in enumerate(self.decoder_inputs):
                if i > 0: scope.reuse_variables()

                if self.is_no_expand(control_symbol):
                    stack.pop()     # remove <no_expand> symbol from the stack
                    # predict right sibling of current node
                    if self.use_attention:
                        input, state, attns = stack[-1]
                        input_embedding = embedding_inputs[input]
                        output, state, attns = self.attention_cell(sb_cell, input_embedding, state,
                                                                   attns, (i == 0 and initial_state_attention),
                                                                   hidden_features, attn_vecs, num_heads, hidden)
                    else:
                        input, attns = stack[-1]
                        input_embedding = embedding_inputs[input]
                        output, state = sb_cell(input_embedding, state)
                    stack.pop()     # remove a state from the stack when we have finished
                                    # generating both its child and right sibling
                else:
                    # predict first child of current node
                    if self.use_attention:
                        input, state, attns = stack[-1]
                        input_embedding = embedding_inputs[input]
                        output, state, attns = self.attention_cell(parent_cell, input_embedding, state,
                                                                   attns, (i == 0 and initial_state_attention),
                                                                   hidden_features, attn_vecs, num_heads, hidden)
                    else:
                        input, state = stack[-1]
                        input_embedding = embedding_inputs[input]
                        output, state = parent_cell(input_embedding, state)

                outputs.append(output)

                if self.use_attention:
                    stack.append([self.decoder_inputs[i + 1], state, attns])
                else:
                    stack.append([self.decoder_inputs[i + 1], state])

        return outputs, state


    def attention(self, state, hidden_features, attn_vecs, num_heads, hidden):
        attn_vec_dim = attn_vecs.get_shape()[0].value
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
        return ds


    def attention_hidden_layer(self, attention_states, num_heads):
        """
        Hidden layer above attention states.
        :param attention_states: 3D Tensor [batch_size x attn_length x attn_dim].
        :param num_heads: Number of attention heads that read from from attention_states.
                         Dummy field if attention_states is None.
        :return:
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


    def attention_cell(self, cell, input_embedding, state, attns, initial_state_attention,
                       hidden_features, attn_vecs, num_heads, hidden):
        # attention mechanism on cell and hidden states
        x = tf.nn.rnn_cell._linear([input_embedding] + attns, self.dim, True)
        cell_output, state = cell(x, state)
        # attention mechanism on output state
        if initial_state_attention:
            with tf.variable_scope(tf.get_variable_scope(), reuse=True):
                attns = self.attention(state, hidden_features, attn_vecs, num_heads, hidden)
        else:
            attns = self.attention(state, hidden_features, attn_vecs, num_heads, hidden)
        with tf.variable_scope("AttnOutputProjection"):
            output = tf.nn.rnn_cell._linear([cell_output] + attns, self.dim, True)
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
        return ind == data_utils._NO_EXPAND

    def source_embeddings(self):
        with tf.variable_scope("source_embeddings"):
            sqrt3 = math.sqrt(3)
            initializer = tf.random_normal_initializer(-sqrt3, sqrt3)
            embeddings = tf.get_variable("embedding", [self.source_vocab_size,
                                                       self.dim],
                                         initializer=initializer)
            tf.get_variable_scope().reuse_variables()
            return embeddings

    def target_embeddings(self):
        with tf.variable_scope("target_embeddings"):
            sqrt3 = math.sqrt(3)
            initializer = tf.random_normal_initializer(-sqrt3, sqrt3)
            embeddings = tf.get_variable("embedding", [self.target_vocab_size,
                                                       self.dim],
                                         initializer=initializer)
            tf.get_variable_scope().reuse_variables()
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
