"""A set of sequence decoder modules used in the encoder-decoder framework."""

import os
import sys

import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import decoder, beam_search, data_utils, graph_utils

class RNNDecoder(decoder.Decoder):
    def __init__(self, hyperparameters, output_projection=None):
        super(RNNDecoder, self).__init__(hyperparameters, output_projection)


    def define_graph(self, encoder_state, decoder_inputs, embeddings,
                     encoder_attn_masks=None, attention_states=None, num_heads=1,
                     initial_state_attention=False, feed_previous=False,
                     reuse_variables=False):

        if self.use_attention \
                and not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be "
                             "known %s" % attention_states.get_shape())

        with tf.variable_scope("rnn_decoder") as scope:
            decoder_cell, decoder_scope = self.decoder_cell()
            state = encoder_state
            outputs = []
            attn_masks = []

            # applying cell wrappers: ["attention", "beam"]
            if self.decoding_algorithm == "beam_search":
                if not feed_previous:
                    # TODO: support beam search training
                    raise NotImplementedError
                beam_decoder = beam_search.BeamDecoder(self.target_vocab_size,
                                                       data_utils.ROOT_ID,
                                                       data_utils.EOS_ID,
                                                       self.batch_size,
                                                       self.beam_size,
                                                       len(decoder_inputs),
                                                       self.use_attention)
                state = beam_decoder.wrap_state(state, self.output_projection)
                if self.use_attention:
                    attention_states = beam_decoder.wrap_input(attention_states)
                    encoder_attn_masks = [beam_decoder.wrap_input(encoder_attn_mask)
                                      for encoder_attn_mask in encoder_attn_masks]
                    decoder_cell = decoder.AttentionCellWrapper(decoder_cell,
                                                            attention_states,
                                                            encoder_attn_masks,
                                                            self.attention_input_keep,
                                                            self.attention_output_keep,
                                                            num_heads,
                                                            reuse_variables)
                decoder_cell = beam_decoder.wrap_cell(decoder_cell, self.output_projection)
            elif self.decoding_algorithm == "greedy":
                if self.use_attention:
                    decoder_cell = decoder.AttentionCellWrapper(decoder_cell,
                                                            attention_states,
                                                            encoder_attn_masks,
                                                            self.attention_input_keep,
                                                            self.attention_output_keep,
                                                            num_heads,
                                                            reuse_variables)
                past_output_symbols = tf.constant(data_utils.ROOT_ID,
                                                  shape=[self.batch_size, 1],
                                                  dtype=tf.int64)
                past_output_logits = tf.constant(0, shape=[self.batch_size],
                                                 dtype=tf.float32)

            # initial attention state
            if self.use_attention:
                batch_size = tf.shape(attention_states)[0]
                attn_dim = tf.shape(attention_states)[2]
                batch_attn_size = tf.pack([batch_size, attn_dim])
                attns = tf.concat(1, [tf.zeros(batch_attn_size, dtype=tf.float32)
                                      for _ in xrange(num_heads)])
                if initial_state_attention:
                    attns, _ = decoder_cell.attention(encoder_state)

            for i, input in enumerate(decoder_inputs):
                if self.decoding_algorithm == "beam_search":
                    input = beam_decoder.wrap_input(input)
                    if self.use_attention:
                        attns = beam_decoder.wrap_input(attns)
               
                if i > 0:
                    scope.reuse_variables()
                    decoder_scope.reuse_variables()
                    if feed_previous:
                        if self.decoding_algorithm == "beam_search":
                            (
                                past_cand_symbols,  # [batch_size, max_len]
                                past_cand_logprobs, # [batch_size]
                                past_beam_symbols,  # [batch_size*self.beam_size, max_len], right-aligned!!!
                                past_beam_logprobs, # [batch_size*self.beam_size]
                                past_cell_state,
                            ) = state
                            input = past_beam_symbols[:, -1]
                        elif self.decoding_algorithm == "greedy":
                            W, b = self.output_projection
                            # [self.batch_size * self.beam_size, num_classes]
                            projected_output = tf.nn.log_softmax(tf.matmul(output, W) + b)
                            output_symbol = tf.argmax(projected_output, 1)
                            past_output_symbols = tf.concat(1, [past_output_symbols,
                                                                tf.expand_dims(output_symbol, 1)])
                            past_output_logits = tf.add(past_output_logits,
                                                        tf.reduce_max(projected_output, 1))
                            input = tf.cast(output_symbol, dtype=tf.int32)
                input_embedding = tf.nn.embedding_lookup(embeddings, input)

                if self.use_attention:
                    output, state, attns, attn_mask = \
                        decoder_cell(input_embedding, state, attns, scope=decoder_scope)
                    attn_length = tf.shape(attention_states)[1]
                    if self.decoding_algorithm == "beam_search":
                        attn_mask = tf.reshape(attn_mask, [-1, self.beam_size, attn_length])
                    attn_masks.append(tf.expand_dims(attn_mask, 1))
                else:
                    output, state = decoder_cell(input_embedding, state, scope=decoder_scope)
                # record output state to compute the loss.
                outputs.append(output)

        if self.use_attention:
             attn_masks = tf.concat(1, attn_masks)

        # Beam-search output
        if self.decoding_algorithm == "beam_search":
            (
                past_cand_symbols,  # [batch_size, max_len]
                past_cand_logprobs, # [batch_size]
                past_beam_symbols,  # [batch_size*self.beam_size, max_len], right-aligned!!!
                past_beam_logprobs, # [batch_size*self.beam_size]
                past_cell_state,
            ) = state
            # [self.batch_size, self.beam_size, max_len]
            top_k_outputs = tf.reshape(past_beam_symbols, [self.batch_size, self.beam_size, -1])
            top_k_outputs = tf.split(0, self.batch_size, top_k_outputs)
            top_k_outputs = [tf.split(0, self.beam_size, tf.squeeze(top_k_output, squeeze_dims=[0]))
                             for top_k_output in top_k_outputs]
            top_k_outputs = [[tf.squeeze(output, squeeze_dims=[0]) for output in top_k_output]
                             for top_k_output in top_k_outputs]
            # [self.batch_size, self.beam_size]
            top_k_logits = tf.reshape(past_beam_logprobs, [self.batch_size, self.beam_size])
            top_k_logits = tf.split(0, self.batch_size, top_k_logits)
            top_k_logits = [tf.squeeze(top_k_logit, squeeze_dims=[0])
                            for top_k_logit in top_k_logits]
            if self.use_attention:
                return top_k_outputs, top_k_logits, outputs, state, attn_masks
            else:
                return top_k_outputs, top_k_logits, outputs, state
        else:
            W, b = self.output_projection
            projected_output = tf.nn.log_softmax(tf.matmul(output, W) + b)
            output_symbol = tf.argmax(projected_output, 1)
            past_output_symbols = tf.concat(1, [past_output_symbols,
                                                tf.expand_dims(output_symbol, 1)])
            past_output_symbols = past_output_symbols[:, 1:]
            output_symbols = tf.split(0, self.batch_size, past_output_symbols)
            past_output_logits = tf.add(past_output_logits,
                                        tf.reduce_max(projected_output, 1))
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
