"""A set of sequence decoder modules used in the encoder-decoder framework."""

import os, sys

import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import seq2tree.decoder
import seq2tree.graph_utils

class RNNDecoder(seq2tree.decoder.Decoder):

    def __init__(self, dim, batch_size, rnn_cell, num_layers,
                 input_keep_prob, output_keep_prob,
                 use_attention, use_copy, output_projection=None):
        super(RNNDecoder, self).__init__(dim, batch_size, rnn_cell, num_layers,
                                         input_keep_prob, output_keep_prob,
                                         use_attention, use_copy, output_projection)

    def define_graph(self, encoder_state, decoder_inputs, embeddings,
                     attention_states=None, num_heads=1,
                     initial_state_attention=False, feed_previous=False):

        if self.use_attention and not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be known %s"
                             % attention_states.get_shape())

        with tf.variable_scope("rnn_decoder") as scope:
            decoder_cell, decoder_scope = self.decoder_cell()
            state = encoder_state
            outputs = []

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

            for i, input in enumerate(decoder_inputs):
                if i > 0:
                    scope.reuse_variables()
                    if feed_previous:
                        W, b = self.output_projection
                        projected_output = tf.matmul(output, W) + b
                        output_symbol = tf.argmax(projected_output, 1)
                        input = tf.cast(output_symbol, dtype=tf.int32)

                input.set_shape([self.batch_size])
                input_embedding = tf.nn.embedding_lookup(embeddings, input)

                if self.use_attention:
                    output, state, attns, attn_mask = \
                        self.attention_cell(decoder_cell, decoder_scope,
                                            input_embedding, state, attns,
                                            hidden_features, attn_vecs, num_heads, hidden)
                else:
                    output, state = self.normal_cell(
                                        decoder_cell, decoder_scope, input_embedding, state)

                # record output state to compute the loss.
                outputs.append(output)

        return outputs, state

    def decoder_cell(self):
        """RNN cell for the encoder."""
        with tf.variable_scope("decoder_cell") as scope:
            cell = seq2tree.graph_utils.create_multilayer_cell(
                self.rnn_cell, scope, self.dim, self.num_layers)
            self.encoder_cell_vars = True
        return cell, scope
