"""Sequence-to-tree model with an attention mechanism."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
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
        self.encoder_inputs = []        # encoder inputs.
        self.decoder_inputs = []        # decoder inputs (always start with "root").
        self.target_weights = []        # weights at each position of the target sequence.
        for i in xrange(len(self.source)):
            self.encoder_inputs.append(tf.placeholder(tf.int32, shape=[None],
                                                      name="encoder{0}".format(i)))
        for i in xrange(len(self.target) + 1):
            self.decoder_inputs.append(tf.placeholder(tf.int32, shape=[None],
                                                      name="decoder{0}".format(i)))
            self.target_weights.append(tf.placeholder(tf.float32, shape=[None],
                                                      name="weight{0}".format(i)))

        # Our targets are decoder inputs shifted by one.
        self.targets = [self.decoder_inputs[i+1]
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
        for i in xrange(len(self.target)):
            gradients = tf.gradients(self.losses[i], params)
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
                self.outputs, state = self.basic_attention_tree_decoder(encoder_state, attention_states)
            else:
                self.outputs, state = self.basic_tree_decoder(encoder_state)

    def basic_tree_decoder(self, encoder_state):
        embeddings = self.target_embeddings()
        embedding_inputs = (tf.nn.embedding_lookup(embeddings, i) for i in self.decoder_inputs)

        parent_cell = self.create_multilayer_cell("lstm")
        sb_cell = self.create_multilayer_cell("lstm")

        # search control
        stack = [(self.decoder_inputs[0], encoder_state)]

        with tf.variable_scope("basic_tree_decoder") as scope:
            outputs = []
            for i, control_symbol in enumerate(self.decoder_inputs):
                if i > 0: scope.reuse_variables()

                if self.is_no_expand(control_symbol):
                    stack.pop()
                    input, state = stack[-1]
                    # predict right sibling of current node
                    output, state = sb_cell(embedding_inputs[input], state)
                    stack.pop()
                else:
                    input, state = stack[-1]
                    # predict first child of current node
                    output, state = parent_cell(embedding_inputs[input], state)

                outputs.append(output)
                stack.append([self.decoder_inputs[i+1], state])
        return outputs, state

    def basic_attention_tree_decoder(self, encoder_state, attention_states):
        embeddings = self.target_embeddings()
        embedding_inputs = (tf.nn.embedding_lookup(embeddings, i) for i in self.decoder_inputs)

        parent_cell = self.create_multilayer_cell("lstm")
        sb_cell = self.create_multilayer_cell("lstm")

        # search control
        stack = [(self.decoder_inputs[0], encoder_state)]

        with tf.variable_scope("basic_attention_tree_decoder") as scope:
            outputs = []
            for i, control_symbol in enumerate(self.decoder_inputs):
                if i > 0: scope.reuse_variables()

                outputs.append(output)
                stack.append([self.decoder_inputs[i+1], state])
        return outputs, state

    def attention(query, hidden_features, attention_vec, attention_vec_size, attn_length, attn_size,
              num_heads, hidden):
      if not rnn_cell._is_sequence(query):
        shapes = [a.get_shape().as_list() for a in [query]]
      else:
        shapes = [a.get_shape().as_list() for a in query]

      """Put attention masks on hidden using hidden_features and query."""
      ds = []  # Results of attention reads will be stored here.
      for a in xrange(num_heads):
        with variable_scope.variable_scope("Attention_%d" % a):
          y = linear(query, attention_vec_size, True)
          y = array_ops.reshape(y, [-1, 1, 1, attention_vec_size])
          # Attention mask is a softmax of v^T * tanh(...).
          s = math_ops.reduce_sum(
              attention_vec[a] * math_ops.tanh(hidden_features[a] + y), [2, 3])
          a = nn_ops.softmax(s)
          # Now calculate the attention-weighted vector d.
          d = math_ops.reduce_sum(
              array_ops.reshape(a, [-1, attn_length, 1, 1]) * hidden,
              [1, 2])
          ds.append(array_ops.reshape(d, [-1, attn_size]))
      return ds

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