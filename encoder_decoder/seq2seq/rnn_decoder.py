"""A set of sequence decoder modules used in the encoder-decoder framework."""

import os
import sys

import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import decoder, data_utils, graph_utils

class RNNDecoder(decoder.Decoder):
    def __init__(self, hyperparameters, output_projection=None):
        super(RNNDecoder, self).__init__(hyperparameters, output_projection)


    def define_bso_graph(self, encoder_state, decoder_inputs, target_weights, embeddings,
                         encoder_attn_masks=None, attention_states=None, num_heads=1,
                         beam_decoder=None, forward_only=False, reuse_variables=False):
        """
        :return output_symbols: batch of discrete output sequences
        :return output_logits: batch of output sequence scores
        :return outputs: batch output states
        :return state: batch final hidden states
        :return attn_masks: batch attention masks (if attention mechanism is used)
        :return bso_losses: beam search optimization loss (if beam search optimization is used)
        """

        if self.use_attention and not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be "
                             "known %s" % attention_states.get_shape())

        with tf.variable_scope("decoder_rnn") as scope:
            decoder_cell, decoder_scope = self.decoder_cell(scope)

            beam_outputs = []
            outputs = []
            beam_attn_masks = []
            attn_masks = []
            bso_losses = []

            state = encoder_state
            beam_state = beam_decoder.wrap_state(state, self.output_projection)
            past_output_symbols = tf.expand_dims(tf.cast(decoder_inputs[0], tf.int64), 1)
            past_output_logits = tf.cast(decoder_inputs[0] * 0, tf.float32)

            if self.use_attention:
                ## Beam Search
                beam_encoder_attn_masks = [beam_decoder.wrap_input(encoder_attn_mask)
                                  for encoder_attn_mask in encoder_attn_masks]
                beam_encoder_attn_masks = [tf.expand_dims(beam_encoder_attn_mask)
                                  for beam_encoder_attn_mask in beam_encoder_attn_masks]
                beam_encoder_attn_masks = tf.concat(1, beam_encoder_attn_masks)
                beam_attention_states = beam_decoder.wrap_input(attention_states)
                beam_decoder_cell = decoder.AttentionCellWrapper(
                    decoder_cell,
                    beam_attention_states,
                    beam_encoder_attn_masks,
                    self.attention_input_keep,
                    self.attention_ouptut_keep,
                    num_heads,
                    reuse_variables
                )

                ## Reference Search
                encoder_attn_masks = [tf.expand_dims(encoder_attn_mask, 1)
                                      for encoder_attn_mask in encoder_attn_masks]
                encoder_attn_masks = tf.concat(1, encoder_attn_masks)
                decoder_cell = decoder.AttentionCellWrapper(
                    decoder_cell,
                    attention_states,
                    encoder_attn_masks,
                    self.attention_input_keep,
                    self.attention_output_keep,
                    num_heads,
                    reuse_variables
                )

            beam_decoder_cell = \
                beam_decoder.wrap_cell(beam_decoder_cell, self.output_projection)

            partial_target_symbols = None
            partial_target_weights = None

            for i, input in enumerate(decoder_inputs):
                beam_input = beam_decoder.wrap_input(input)

                if partial_target_symbols is None:
                    partial_target_symbols = tf.expand_dims(
                        beam_decoder.wrap_input(decoder_inputs[i+1]), 1
                    )
                    partial_target_weights = tf.expand_dims(
                        beam_decoder.wrap_input(target_weights[i]), 1
                    )
                else:
                    if i == len(decoder_inputs) - 1:
                        # last target is a dummy token
                        partial_target_symbols = tf.concat(partial_target_symbols,
                            tf.expand_dims(tf.zeros(beam_input.get_shape()), 1)
                        )
                    else:
                        partial_target_symbols = tf.concat(partial_target_symbols,
                            tf.expand_dims(beam_decoder.wrap_input(decoder_inputs[i+1]), 1)
                        )
                    partial_target_weights = tf.concat(partial_target_weights,
                        tf.expand_dims(beam_decoder.wrap_input(target_weights[i]), 1), 1
                    )

                if i > 0:
                    scope.reuse_variables()
                    decoder_scope.reuse_variables()
                    ## Beam Search
                    (
                        past_cand_symbols,  # [batch_size, max_len]
                        past_cand_logprobs, # [batch_size]
                        past_beam_symbols,  # [batch_size*self.beam_size, max_len], right-aligned!!!
                        past_beam_logprobs, # [batch_size*self.beam_size]
                        past_cell_state,
                    ) = beam_state
                    beam_input = past_beam_symbols[:, -1]

                    ## Reference Search
                    W, b = self.output_projection
                    projected_output = tf.nn.log_softmax(tf.matmul(output, W) + b)
                    output_symbol = tf.argmax(projected_output, 1)
                    past_output_symbols = tf.concat(1, [past_output_symbols,
                                                        tf.expand_dims(output_symbol, 1)])
                    past_output_logits = tf.add(past_output_logits,
                                                tf.reduce_max(projected_output, 1))
                    input = tf.cast(output_symbol, dtype=tf.int32)

                input_embedding = tf.nn.embedding_lookup(embeddings, input)
                beam_input_embedding = tf.nn.embedding_lookup(embeddings, beam_input)

                if self.use_attention:
                    beam_output, beam_state, beam_attn_masks = \
                        beam_decoder_cell(beam_input_embedding, beam_state, beam_attn_masks,
                                          scope=decoder_scope)
                    output, state, attn_masks = \
                        decoder_cell(input_embedding, state, attn_masks, scope=decoder_scope)
                else:
                    beam_output, beam_state = \
                        beam_decoder_cell(beam_input_embedding, beam_state, scope=decoder_scope)
                    output, state = decoder_cell(input_embedding, state, scope=decoder_scope)

                # compute search-based training loss
                if not forward_only:
                    (
                        past_cand_symbols,  # [batch_size, max_len]
                        past_cand_logprobs, # [batch_size]
                        past_beam_symbols,  # [batch_size*self.beam_size, max_len], right-aligned!!!
                        past_beam_logprobs, # [batch_size*self.beam_size]
                        past_cell_state,
                    ) = beam_state
                    # [batch_size*beam_size, (i+1)]
                    partial_beam_symbols = past_beam_symbols[-(i+1):]

                    # check if ground truth has fell off the beam
                    in_beam = tf.equal(tf.reduce_add(tf.mul(tf.cast(tf.equal(
                                                                        partial_beam_symbols,
                                                                        partial_target_symbols),
                                                                    tf.int32),
                                                            partial_target_weights),
                                                    1),
                                       tf.reduce_add(partial_target_weights, 1)
                    )
                    in_beam = tf.reduce_add(tf.reshape(in_beam, [-1, self.beam_size]), 1)

                    # check if ground truth search is completed
                    search_complete = tf.equal(partial_target_weights[:, -1], 0)
                    

    def define_graph(self, encoder_state, decoder_inputs, embeddings,
                     encoder_attn_masks=None, attention_states=None, num_heads=1,
                     beam_decoder=None, forward_only=False, reuse_variables=False):
        """
        :return output_symbols: batch of discrete output sequences
        :return output_logits: batch of output sequence scores
        :return outputs: batch output states
        :return state: batch final hidden states
        :return attn_masks: batch attention masks (if attention mechanism is used)
        """
        if self.use_attention and not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be "
                             "known %s" % attention_states.get_shape())

        with tf.variable_scope("decoder_rnn") as scope:
            decoder_cell, decoder_scope = self.decoder_cell(scope)
            state = encoder_state
            outputs = []
            attn_masks = []

            # applying cell wrappers: ["attention", "beam"]
            if self.decoding_algorithm == "beam_search":
                state = beam_decoder.wrap_state(state, self.output_projection)
            elif self.decoding_algorithm == "greedy":
                past_output_symbols = tf.expand_dims(tf.cast(decoder_inputs[0], tf.int64), 1)
                past_output_logits = tf.cast(decoder_inputs[0] * 0, tf.float32)

            if self.use_attention:
                if self.decoding_algorithm == "beam_search":
                    encoder_attn_masks = [beam_decoder.wrap_input(encoder_attn_mask)
                                      for encoder_attn_mask in encoder_attn_masks]
                    attention_states = beam_decoder.wrap_input(attention_states)
                encoder_attn_masks = [tf.expand_dims(encoder_attn_mask, 1)
                    for encoder_attn_mask in encoder_attn_masks]
                encoder_attn_masks = tf.concat(1, encoder_attn_masks)
                decoder_cell = decoder.AttentionCellWrapper(
                                                decoder_cell,
                                                attention_states,
                                                encoder_attn_masks,
                                                self.attention_input_keep,
                                                self.attention_output_keep,
                                                num_heads,
                                                reuse_variables)

            if self.decoding_algorithm == "beam_search":
                decoder_cell = beam_decoder.wrap_cell(decoder_cell, self.output_projection)

            for i, input in enumerate(decoder_inputs):
                if self.decoding_algorithm == "beam_search":
                    input = beam_decoder.wrap_input(input)

                if i > 0:
                    scope.reuse_variables()
                    decoder_scope.reuse_variables()

                    if forward_only:
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
                            projected_output = tf.nn.log_softmax(tf.matmul(output, W) + b)
                            output_symbol = tf.argmax(projected_output, 1)
                            past_output_symbols = tf.concat(1, [past_output_symbols,
                                                                tf.expand_dims(output_symbol, 1)])
                            past_output_logits = tf.add(past_output_logits,
                                                        tf.reduce_max(projected_output, 1))
                            input = tf.cast(output_symbol, dtype=tf.int32)

                input_embedding = tf.nn.embedding_lookup(embeddings, input)

                if self.use_attention:
                    output, state, attn_masks = \
                        decoder_cell(input_embedding, state, attn_masks, scope=decoder_scope)
                else:
                    output, state = decoder_cell(input_embedding, state, scope=decoder_scope)

                # record output state to compute the loss.
                outputs.append(output)

            if self.use_attention:
                # Tensor list --> tenosr
                attn_masks = tf.concat(1, attn_masks)

            if forward_only and self.decoding_algorithm == "beam_search":
                # Beam-search output
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
                    attn_masks = tf.reshape(attn_masks, [self.batch_size, self.beam_size,
                                            len(decoder_inputs), attention_states.get_shape()[1].value])
                return top_k_outputs, top_k_logits, outputs, state, attn_masks
            else:
                # Greedy output
                W, b = self.output_projection
                projected_output = tf.nn.log_softmax(tf.matmul(output, W) + b)
                output_symbol = tf.argmax(projected_output, 1)
                past_output_symbols = tf.concat(1, [past_output_symbols,
                                                    tf.expand_dims(output_symbol, 1)])
                output_symbols = past_output_symbols[:, 1:]
                past_output_logits = tf.add(past_output_logits,
                                            tf.reduce_max(projected_output, 1))
                return output_symbols, past_output_logits, outputs, state, attn_masks


    def decoder_cell(self, scope):
        with tf.variable_scope(scope or "decoder_cell") as scope:
            cell = graph_utils.create_multilayer_cell(
                self.rnn_cell, scope, self.dim, self.num_layers,
                self.decoder_input_keep, self.decoder_output_keep)
            self.encoder_cell_vars = True
        return cell, scope
