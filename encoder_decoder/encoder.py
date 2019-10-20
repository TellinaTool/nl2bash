"""A set of encoder modules used in the encoder-decoder framework."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import math
import numpy as np

import tensorflow as tf

from encoder_decoder import graph_utils


class Encoder(graph_utils.NNModel):
    def __init__(self, hyperparameters, input_keep, output_keep):
        super(Encoder, self).__init__(hyperparameters)

        # variable reuse
        self.char_embedding_vars = False
        self.token_embedding_vars = False
        self.char_rnn_vars = False

        self.input_keep = input_keep
        self.output_keep = output_keep

        self.channels = []
        self.dim = 0
        if self.sc_token:
            self.channels.append('token')
            self.dim += self.sc_token_dim
        if self.sc_char:
            self.channels.append('char')
            self.dim += self.sc_char_dim

        assert(len(self.channels) > 0)

    def token_representations(self, channel_inputs):
        """
        Generate token representations based on multi-channel input.

        :param channel_inputs: an array of channel input indices
            1. batch token indices
            2. batch char indices
        """
        channel_embeddings = []
        if self.sc_token:
            token_embeddings = self.token_embeddings()
            token_channel_embeddings = \
                [tf.nn.embedding_lookup(params=token_embeddings, ids=encoder_input)
                 for encoder_input in channel_inputs[0]]
            channel_embeddings.append(token_channel_embeddings)
        if self.sc_char:
            char_channel_embeddings = \
                self.char_channel_embeddings(channel_inputs[1])
            channel_embeddings.append(char_channel_embeddings)
        if len(channel_embeddings) == 1:
            input_embeddings = channel_embeddings[0]
        else:
            input_embeddings = \
                [tf.concat(axis=1, values=[x, y]) for (x, y) in
                    map(lambda x,y:(x,y), channel_embeddings[0],
                        channel_embeddings[1])]
        return input_embeddings

    def token_embeddings(self):
        """
        Generate token representations by plain table look-up

        :return: token embedding matrix [source_vocab_size, dim]
        """
        with tf.compat.v1.variable_scope("encoder_token_embeddings",
                               reuse=self.token_embedding_vars):
            vocab_size = self.source_vocab_size
            print("source token embedding size = {}".format(vocab_size))
            sqrt3 = math.sqrt(3)
            initializer = tf.compat.v1.random_uniform_initializer(-sqrt3, sqrt3)
            embeddings = tf.compat.v1.get_variable("embedding",
                [vocab_size, self.sc_token_dim], initializer=initializer)
            self.token_embedding_vars = True
            return embeddings

    def char_embeddings(self):
        with tf.compat.v1.variable_scope("encoder_char_embeddings",
                               reuse=self.char_embedding_vars):
            sqrt3 = math.sqrt(3)
            initializer = tf.compat.v1.random_uniform_initializer(-sqrt3, sqrt3)
            embeddings = tf.compat.v1.get_variable(
                "embedding", [self.source_char_vocab_size, self.sc_char_dim],
                initializer=initializer)
            self.char_embedding_vars = True
            return embeddings

    def token_channel_embeddings(self):
        input = self.token_features()
        return tf.nn.embedding_lookup(params=self.token_embeddings(), ids=input)

    def char_channel_embeddings(self, channel_inputs):
        """
        Generate token representations by character composition.

        :param channel_inputs: batch input char indices
                [[batch, token_size], [batch, token_size], ...]
        :return: embeddings_char [source_vocab_size, char_channel_dim]
        """
        inputs = [tf.squeeze(x, 1) for x in tf.split(axis=1,
                  num_or_size_splits=self.max_source_token_size,
                  value=tf.concat(axis=0, values=channel_inputs))]
        input_embeddings = [tf.nn.embedding_lookup(params=self.char_embeddings(), ids=input) 
                            for input in inputs]
        if self.sc_char_composition == 'rnn':
            with tf.compat.v1.variable_scope("encoder_char_rnn",
                                   reuse=self.char_rnn_vars) as scope:
                cell = graph_utils.create_multilayer_cell(
                    self.sc_char_rnn_cell, scope,
                    self.sc_char_dim, self.sc_char_rnn_num_layers,
                    variational_recurrent=self.variational_recurrent_dropout)
                rnn_outputs, rnn_states = graph_utils.RNNModel(cell, input_embeddings,
                                                               dtype=tf.float32)
                self.char_rnn_vars = True
        else:
            raise NotImplementedError

        return [tf.squeeze(x, 0) for x in
                tf.split(axis=0, num_or_size_splits=len(channel_inputs),
                    value=tf.reshape(rnn_states[-1],
                        [len(channel_inputs), -1, self.sc_char_dim]))]

    def token_features(self):
        return np.load(self.sc_token_features_path)

    def token_char_index_matrix(self):
        return np.load(self.sc_char_features_path)


class RNNEncoder(Encoder):
    def __init__(self, hyperparameters, input_keep, output_keep):
        super(RNNEncoder, self).__init__(
            hyperparameters, input_keep, output_keep)
        self.cell = self.encoder_cell()
        self.output_dim = self.dim

    def define_graph(self, encoder_channel_inputs, input_embeddings=None):
        # Compute the continuous input representations
        if input_embeddings is None:
            input_embeddings = self.token_representations(encoder_channel_inputs)
        with tf.compat.v1.variable_scope("encoder_rnn"):
            return graph_utils.RNNModel(self.cell, input_embeddings, dtype=tf.float32)

    def encoder_cell(self):
        """RNN cell for the encoder."""
        with tf.compat.v1.variable_scope("encoder_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope,
                self.dim, self.num_layers, self.input_keep, self.output_keep,
                variational_recurrent=self.variational_recurrent_dropout)
        return cell


class BiRNNEncoder(Encoder):
    def __init__(self, hyperparameters, input_keep, output_keep):
        super(BiRNNEncoder, self).__init__(
            hyperparameters, input_keep, output_keep)
        self.fw_cell = self.forward_cell()
        self.bw_cell = self.backward_cell()
        self.output_dim = 2 * self.dim
        print("encoder input dimension = {}".format(self.dim))
        print("encoder output dimension = {}".format(self.output_dim))

    def define_graph(self, channel_inputs, input_embeddings=None):
        # Each rnn in the bi-directional encoder have dimension which is half
        # of that of the decoder.
        # The hidden states of the two rnns are concatenated as the hidden
        # states of the bi-directional encoder.

        # Compute the continuous input representations
        if input_embeddings is None:
            input_embeddings = self.token_representations(channel_inputs)
        with tf.compat.v1.variable_scope("encoder_rnn"):
            return graph_utils.BiRNNModel(self.fw_cell, self.bw_cell, input_embeddings,
                num_cell_layers=self.num_layers, dtype=tf.float32)

    def forward_cell(self):
        """RNN cell for the forward RNN."""
        with tf.compat.v1.variable_scope("forward_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope,
                self.dim, self.num_layers, self.input_keep, self.output_keep,
                variational_recurrent=self.variational_recurrent_dropout)
        return cell

    def backward_cell(self):
        """RNN cell for the backward RNN."""
        with tf.compat.v1.variable_scope("backward_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope,
                self.dim, self.num_layers, self.input_keep, self.output_keep,
                variational_recurrent=self.variational_recurrent_dropout)
        return cell
