"""Sequence-to-tree model with an attention mechanism."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.python.ops import rnn_cell
from tensorflow.python.ops import variable_scope

class Seq2TreeMode(object):
    """Sequence-to-tree model with attention.
    """

    def __init__(self, source_vocab_size, target_vocab_size, dim,
                 num_layers, max_gradient_norm, batch_size, learning_rate,
                 learning_rate_decay_factor, input_keep_prob, output_keep_prob,
                 decoder_topology="basic", num_samples=512, forward_only=False,
                 decoding_algorithm="greedy"):
        """
        Create the model.
        :param source_vocab_size: size of the source vocabulary.
        :param target_vocab_size: size of the target vocabulary.
        :param dim: dimension of each layer in the model.
        :param num_layers: number of layers in the model.
        :param max_gradient_norm: gradients are clipped to maximally this norm.
        :param batch_size: the size of the batches used during training or decoding.
        :param learning_rate: learning rate to start with.
        :param learning_rate_decay_factor: decay learning rate by this much when needed.
                not import if the adam optimizer is used.
        :param input_keep_prob: proportion of input to keep if dropout is used.
        :param output_keep_prob: proportion of output to keep if dropout is used.
        :param decoder_topology: topology of the tree rnn decoder.
        :param num_samples: number of samples for sampled softmax.
        :param forward_only: if set, we do not construct the backward pass.
        :param decoding_algorithm: decoding algorithm used.
        """

        self.source_vocab_size = source_vocab_size
        self.target_vocab_size = target_vocab_size
        self.dim = dim
        self.batch_size = batch_size
        self.learning_rate = tf.Variable(float(learning_rate), trainable=False)
        self.learning_rate_decay_op = self.learning_rate.assign(
            self.learning_rate * learning_rate_decay_factor)
        self.global_step = tf.Variable(0, trainable=False)

        # Output project for sampled softmax.
        output_projection = None
        softmax_loss_function = None
        if num_samples > 0 and num_samples < self.target_vocab_size:
            try:
                w = tf.get_variable("proj_w", [dim, self.target_vocab_size])
                b = tf.get_variable("proj_b", [self.target_vocab_size])
            except ValueError, e:
                w = [v for v in tf.all_variables() if v.name == "proj_w:0"][0]
                b = [v for v in tf.all_variables() if v.name == "proj_b:0"][0]
            w_t = tf.transpose(w)
            output_projection = (w, b)

            def sampled_loss(inputs, labels):
                labels = tf.reshape(labels, [-1, 1])
                return tf.nn.sampled_softmax_loss(w_t, b, inputs, labels, num_samples,
                        self.target_vocab_size)
            softmax_loss_function = sampled_loss

        # Create the internal multi-layer cell for the tree RNN
        def create_multilayer_cell(type):
            if type == "lstm":
                single_cell = rnn_cell.BasicLSTMCell(dim)
            if num_layers > 1:
                cell = rnn_cell.MultiRNNCell([single_cell] * num_layers)
            if input_keep_prob < 1 or output_keep_prob < 1:
                cell = rnn_cell.DropoutWrapper(cell, input_keep_prob=input_keep_prob,
                                               output_keep_prob=output_keep_prob)
            return cell

            with variable_scope.variable_scope("seq2tree_basic"):
                encoder_cell = create_multilayer_cell("lstm")
                encoder_cell = rnn_cell.EmbeddingWrapper(
                    encoder_cell, embedding_classes=source_vocab_size, embedding_size=dim)
                _, encoder_state = rnn.rnn(encoder_cell, )

        if decoder_topology == "basic":
            decoder_parent_cell = create_multilayer_cell("lstm")
            decoder_lsb_cell = create_multilayer_cell("lstm")
