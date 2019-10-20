from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import math
import numpy as np
import tensorflow as tf
from tensorflow.python.util import nest

from encoder_decoder import data_utils, graph_utils, beam_search


class Decoder(graph_utils.NNModel):
    def __init__(self, hyperparameters, scope, dim, embedding_dim,
                 use_attention, attention_function, input_keep, output_keep,
                 decoding_algorithm):
        """
        :param hyperparameters: Tellina model hyperparameters.
        :param scope: Scope of the decoder. (There might be multiple decoders
            with the same construction in the neural architecture.)
        :param vocab_size: Output vocabulary size.
        :param dim: Decoder dimension.
        :param embedding_dim: Decoder embedding dimension.
        :param use_attention: Set to True to use attention for decoding.
        :param attention_function: The attention function to use.
        :param input_keep: Dropout parameter for the input of the attention layer.
        :param output_keep: Dropout parameter for the output of the attention layer.
        :param decoding_algorithm: The decoding algorithm to use.
            1. "greedy"
            2. "beam_search"
        """
        super(Decoder, self).__init__(hyperparameters)
        if self.forward_only:
            self.hyperparams['batch_size'] = 1

        self.scope = scope
        self.dim = dim
        self.embedding_dim = embedding_dim
        self.use_attention = use_attention
        self.attention_function = attention_function
        self.input_keep = input_keep
        self.output_keep = output_keep
        self.decoding_algorithm = decoding_algorithm

        self.vocab_size = self.target_vocab_size
        
        # variable sharing
        self.embedding_vars = False
        self.output_project_vars = False

        self.beam_decoder = beam_search.BeamDecoder(
                self.num_layers,
                data_utils.ROOT_ID,
                data_utils.EOS_ID,
                self.batch_size,
                self.beam_size,
                self.use_attention,
                self.use_copy,
                self.copy_fun,
                self.alpha,
                locally_normalized=(self.training_algorithm != "bso")
            ) if self.decoding_algorithm == "beam_search" else None

        self.output_project = self.output_project()

    def embeddings(self):
        with tf.compat.v1.variable_scope(self.scope + "_embeddings", reuse=self.embedding_vars):
            vocab_size = self.target_vocab_size
            print("target token embedding size = {}".format(vocab_size))
            sqrt3 = math.sqrt(3)
            initializer = tf.compat.v1.random_uniform_initializer(-sqrt3, sqrt3)
            embeddings = tf.compat.v1.get_variable("embedding",
                [vocab_size, self.embedding_dim], initializer=initializer)
            self.embedding_vars = True
            return embeddings

    def token_features(self):
        return np.load(self.tg_token_features_path)

    def output_project(self):
        with tf.compat.v1.variable_scope(self.scope + "_output_project",
                               reuse=self.output_project_vars):
            w = tf.compat.v1.get_variable("proj_w", [self.dim, self.vocab_size])
            b = tf.compat.v1.get_variable("proj_b", [self.vocab_size])
            self.output_project_vars = True
        return (w, b)


class CopyCellWrapper(tf.compat.v1.nn.rnn_cell.RNNCell):
    def __init__(self, cell, output_project, num_layers,
                 encoder_copy_inputs, tg_vocab_size):
        self.cell = cell
        self.output_project = output_project
        self.num_layers = num_layers
        self.tg_vocab_size = tg_vocab_size

        self.encoder_size = len(encoder_copy_inputs)
        # [batch_size x max_source_length]
        self.encoder_copy_inputs = \
            tf.concat(axis=1, values=[tf.expand_dims(x, 1) for x in encoder_copy_inputs])

        print("CopyCellWrapper added!")

    def __call__(self, input_embedding, state, scope=None):
        output, state, alignments, attns = \
            self.cell(input_embedding, state, scope)

        # Compute generation/copying mixture

        # <generation probability, copying probability>
        W, b = self.output_project
        gen_logit = tf.matmul(output, W) + b
        copy_logit = alignments[1]

        prob = tf.nn.softmax(tf.concat([gen_logit, copy_logit], axis=1))
        gen_prob = tf.slice(prob, [0, 0], [-1, self.tg_vocab_size])
        copy_prob = tf.slice(prob, [0, self.tg_vocab_size], [-1, -1])
        copy_vocab_prob = tf.squeeze(tf.matmul(tf.expand_dims(copy_prob, 1),
            tf.one_hot(self.encoder_copy_inputs, depth=self.tg_vocab_size+copy_prob.get_shape()[1])), 1)

        # mixture probability
        mix_prob = tf.concat([gen_prob, tf.zeros(tf.shape(input=copy_prob))], 1) + \
                   copy_vocab_prob

        return mix_prob, state, alignments, attns


class AttentionCellWrapper(tf.compat.v1.nn.rnn_cell.RNNCell):
    def __init__(self, cell, attention_states, encoder_attn_masks,
            attention_function, attention_input_keep, attention_output_keep,
            num_heads, dim, num_layers, use_copy, tg_vocab_size=-1):
        """
        Hidden layer above attention states.

        :param attention_states: 3D Tensor [batch_size x attn_length x attn_dim].
        :param encoder_attn_masks: encoder input masks, used for masking out
            padded contents in the encoder inputs
        :param encoder_inputs: encoder input indices, used for generating masks
            for copying probabilities
        :param attention_input_keep: attention input state dropout
        :param attention_output_keep: attention hidden state dropout
        :param num_heads: Number of attention heads that read from from
            attention_states. Dummy field if attention_states is None.
        :param rnn_cell: Type of rnn cells used.
        :param dim: Size of the hidden and output layers of the decoder, which
            we assume to be the same.
        :param num_layers: Number of layers in the RNN cells.

        :param use_copy: Copy source tokens to the target.
        :param copy_fun: Parameterization of the copying function.
        """
        if attention_input_keep < 1:
            print("attention input keep probability = {}"
                  .format(attention_input_keep))
            attention_states = tf.nn.dropout(
                attention_states, 1 - (attention_input_keep))
        attn_length = attention_states.get_shape()[1]
        attn_dim = attention_states.get_shape()[2]

        self.cell = cell
        self.encoder_attn_masks = encoder_attn_masks
        self.vocab_indices = tf.linalg.tensor_diag(tf.ones(tg_vocab_size))
        self.num_heads = num_heads
        self.dim = dim
        self.num_layers = num_layers
        self.attn_length = attn_length
        self.attn_dim = attn_dim
        self.attention_function = attention_function
        self.attention_input_keep = attention_input_keep
        self.attention_output_keep = attention_output_keep

        hidden_features = []
        with tf.compat.v1.variable_scope("attention_cell_wrapper"):
            for a in xrange(num_heads):
                # [batch_size, attn_length, attn_dim]
                hidden_features.append(attention_states)
        self.hidden_features = hidden_features

        self.use_copy = use_copy

        print("AttentionCellWrapper added!")

    def attention(self, state):
        """Put attention masks on hidden using hidden_features and query."""
        ds = []             # Results of attention reads will be stored here.
        alignments = []     # Alignment values for each attention head.
        if nest.is_sequence(state):  # If the query is a tuple, flatten it.
            query_list = nest.flatten(state)
            for q in query_list:  # Check that ndims == 2 if specified.
                ndims = q.get_shape().ndims
                if ndims:
                    assert ndims == 2
            state = tf.concat(axis=1, values=query_list)
        for a in xrange(self.num_heads):
            with tf.compat.v1.variable_scope("Attention_%d" % a):
                y = tf.reshape(state, [-1, 1, 1, self.attn_dim])
                # Attention mask is a softmax of v^T * tanh(...).
                if self.attention_function == 'non-linear':
                    k = tf.compat.v1.get_variable("AttnW_%d" % a,
                                        [1, 1, 2*self.attn_dim, self.attn_dim])
                    l = tf.compat.v1.get_variable("Attnl_%d" % a,
                                        [1, 1, 1, self.attn_dim])
                    z = tf.reshape(self.hidden_features[a],
                                   [-1, self.attn_length, 1, self.attn_dim])
                    v = tf.concat(axis=3, values=[z, tf.tile(y, [1, self.attn_length, 1, 1])])
                    s = tf.reduce_sum(
                        input_tensor=l * tf.tanh(tf.nn.conv2d(input=v, filters=k, strides=[1,1,1,1], padding="SAME")), axis=[2, 3])
                elif self.attention_function == 'inner_product':
                    s = tf.reduce_sum(input_tensor=tf.multiply(self.hidden_features[a], y), axis=[2])
                else:
                    raise NotImplementedError

                # Apply attention masks
                # [batch_size x attn_length]
                s = s - (1 - self.encoder_attn_masks) * 1e12
                if a == 0:
                    alignment = tf.nn.softmax(s)    # normalized
                    alignments.append(alignment)
                    # Soft attention read
                    d = tf.reduce_sum(
                        input_tensor=tf.reshape(alignment, [-1, self.attn_length, 1])
                            * self.hidden_features[a], axis=[1])
                    # [batch_size, attn_dim]
                    context = tf.reshape(d, [-1, self.attn_dim])
                else:
                    # Unnormalized
                    alignments.append(s)    # unnormalized
                    # [batch_size, attn_length, attn_dim]
                    context = self.hidden_features[a]
                ds.append(context)

        return ds, alignments

    def __call__(self, input_embedding, state, scope=None):
        cell_output, state = self.cell(input_embedding, state, scope)
        attns, alignments = self.attention(cell_output)

        # with tf.variable_scope("AttnStateProjection"):
        #     attn_state = tf.nn.dropout(
        #                     tf.tanh(tf.nn.rnn_cell.linear(
        #                          [cell_output, attns[0]], self.dim, True)),
        #                          self.attention_output_keep# )

        with tf.compat.v1.variable_scope("AttnOutputProjection"):
            output = graph_utils.linear([cell_output, attns[0]], self.dim, True)

        self.attention_cell_vars = True
        return output, state, alignments, attns
