"""A set of sequence decoder modules used in the encoder-decoder framework."""

import os
import sys

import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import decoder, data_utils, graph_utils

class RNNDecoder(decoder.Decoder):

    def __init__(self, hyperparameters, output_projection=None):
        super(RNNDecoder, self).__init__(hyperparameters, output_projection)

    def define_graph(self, encoder_state, decoder_inputs, embeddings,
                     attention_states=None, num_heads=1,
                     initial_state_attention=False, feed_previous=False):

        if self.use_attention \
                and not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be "
                             "known %s" % attention_states.get_shape())

        with tf.variable_scope("rnn_decoder") as scope:
            decoder_cell, decoder_scope = self.decoder_cell()
            state = encoder_state
            outputs = []
            attn_masks = []

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
                    attns = self.attention(encoder_state, hidden_features,
                                           attn_vecs, num_heads, hidden)

            if self.decoding_algorithm == "beam_search":
                # [self.batch_size * self.beam_size]
                past_beam_logits = tf.constant(0, shape=[self.batch_size *
                                               self.beam_size], dtype=tf.float32)
                # [batch_size*self.beam_size, num_steps]
                past_beam_symbols = tf.constant(data_utils.ROOT_ID,
                                                shape=[self.batch_size *
                                                 self.beam_size, 1])
                parent_refs_offsets = (tf.range(self.batch_size *
                                                self.beam_size) //
                                       self.beam_size) * self.beam_size
            elif self.decoding_algorithm == "greedy":
                past_output_symbols = tf.constant(data_utils.ROOT_ID,
                                                  shape=[self.batch_size, 1])
                past_output_logits = tf.constant(0, shape=[self.batch_size])

            for i, input in enumerate(decoder_inputs):
                if i > 0:
                    scope.reuse_variables()
                    if feed_previous:
                        W, b = self.output_projection
                        num_classes = W.get_shape()[1].value
                        # [self.batch_size * self.beam_size, num_classes]
                        projected_output = tf.log(
                            tf.nn.softmax(tf.matmul(output, W) + b))
                        if self.decoding_algorithm == "beam_search":
                            # [self.batch_size * self.beam_size, num_classes]
                            accumulated_logits = projected_output + tf.expand_dims(
                                past_beam_logits, 1),
                            # [self.batch_size, self.beam_size * num_classes]
                            accumulated_logits = tf.reshape(accumulated_logits,
                                                            [self.batch_size, -1])

                            # [self.batch_size, self.beam_size]
                            beam_logits, beam_indices = \
                                tf.nn.top_k(accumulated_logits, self.beam_size)
                            # [self.batch_size, self.beam_size]
                            symbols = beam_indices % num_classes
                            # [self.batch_size, self.beam_size]
                            parent_refs = beam_indices // num_classes
                            # [self.batch_size * self.beam_size]
                            parent_refs = tf.reshape(parent_refs, [-1]) + \
                                          parent_refs_offsets
                           
                            # Append beam symbols to search histories
                            search_history = tf.gather(past_beam_symbols, parent_refs)
                            beam_symbols = tf.concat(1, [search_history[:, :],
                                                         tf.reshape(symbols, [-1, 1])])
                            # Handle the output and the cell state shuffling
                            # [self.batch_size * self.beam_size]
                            output_symbols = tf.reshape(symbols, [-1])
                            input = tf.cast(output_symbols, dtype=tf.int32)
                            state = decoder.nest_map(
                                lambda X: tf.gather(X, parent_refs), state)

                            past_beam_logits = tf.reshape(beam_logits, [-1])
                            past_beam_symbols = beam_symbols
                        else:
                            output_logits = tf.max(projected_output, 1)
                            past_output_logits += output_logits
                            output_symbol = tf.argmax(projected_output, 1)
                            past_output_symbols = tf.concat(1, [past_output_symbols,
                                tf.expand_dims(output_symbol, 1)])
                            input = tf.cast(output_symbol, dtype=tf.int32)
                else:
                    if self.decoding_algorithm == "beam_search":
                        if not feed_previous:
                            raise NotImplementedError
                        input = tf.expand_dims(input, 1)
                        input = tf.reshape(tf.tile(input, [1, self.beam_size]),
                                           [-1])
                        state = tf.expand_dims(state, 1)
                        state = tf.reshape(tf.tile(state,
                                                   [1, self.beam_size, 1]),
                                           [self.batch_size * self.beam_size,
                                            -1])

                input_embedding = tf.nn.embedding_lookup(embeddings, input)

                if self.use_attention:
                    output, state, attns, attn_mask = \
                        self.attention_cell(decoder_cell, decoder_scope,
                                input_embedding, state, attns,
                                hidden_features, attn_vecs, num_heads, hidden)
                    attn_masks.append(tf.expand_dims(attn_mask, 1))
                else:
                    output, state = self.normal_cell(decoder_cell,
                                        decoder_scope, input_embedding, state)

                # record output state to compute the loss.
                outputs.append(output)

        if self.use_attention:
             attn_masks = tf.concat(1, attn_masks)
        # Beam-search output
        if self.decoding_algorithm == "beam_search":
            # [self.batch_size, self.beam_size, max_len]
            top_k_outputs = tf.reshape(past_beam_symbols, [self.batch_size,
                                                      self.beam_size, -1])
            top_k_outputs = tf.split(0, self.batch_size, top_k_outputs)
            top_k_outputs = [tf.split(0, self.beam_size, 
                                      tf.squeeze(top_k_output, squeeze_dims=[0])) 
                             for top_k_output in top_k_outputs]
            # [self.batch_size, self.beam_size]
            top_k_logits = tf.reshape(past_beam_logits, [self.batch_size, 
                                                         self.beam_size])
            top_k_logits = tf.split(0, self.batch_size, top_k_logits)
            if self.use_attention:
                return top_k_outputs, top_k_logits, outputs, state, attn_masks
            else:
                return top_k_outputs, top_k_logits, outputs, state
        else:
            output_symbols = tf.split(0, self.batch_size, past_output_symbols)
            if self.use_attention:
                return output_symbols, past_output_logits, outputs, \
                       state, attn_masks
            else:
                return output_symbols, past_output_logits, outputs, state


    def decoder_cell(self):
        with tf.variable_scope("decoder_cell") as scope:
            cell = graph_utils.create_multilayer_cell(
                self.rnn_cell, scope, self.dim, self.num_layers,
                self.decoder_input_keep, self.decoder_output_keep)
            self.encoder_cell_vars = True
        return cell, scope
