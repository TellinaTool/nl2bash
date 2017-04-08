"""A set of sequence decoder modules used in the encoder-decoder framework."""

import tensorflow as tf

from encoder_decoder import decoder, graph_utils

class RNNDecoder(decoder.Decoder):
    def __init__(self, hyperparameters, dim, scope):
        super(RNNDecoder, self).__init__(hyperparameters, dim, scope)
        print("{} dimension = {}".format(scope, dim))


    def define_graph(self, encoder_state, decoder_inputs,
                     encoder_attn_masks=None, attention_states=None,
                     num_heads=1, forward_only=False):
        """
        :return output_symbols: batch of discrete output sequences
        :return output_logits: batch of output sequence scores
        :return outputs: batch output states
        :return state: batch final hidden states
        :return attn_alignments: batch attention masks
                                 (if attention mechanism is used)
        """
        if self.use_attention and \
                not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be "
                             "known %s" % attention_states.get_shape())

        bs_decoding = forward_only and self.decoding_algorithm == "beam_search"

        with tf.variable_scope("decoder_rnn") as scope:
            decoder_cell = self.decoder_cell()
            outputs = []
            states = []
            attn_alignments = []

            # applying cell wrappers: ["attention", "beam"]
            if bs_decoding:
                beam_decoder = self.beam_decoder
                state = beam_decoder.wrap_state(encoder_state,
                                                self.output_projection())
            else:
                past_output_symbols = \
                    tf.expand_dims(tf.cast(decoder_inputs[0], tf.int64), 1)
                past_output_logits = tf.cast(decoder_inputs[0] * 0, tf.float32)

            if self.use_attention:
                if bs_decoding:
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
                                                self.rnn_cell,
                                                self.num_layers)

            if bs_decoding:
                decoder_cell = beam_decoder.wrap_cell(decoder_cell,
                                                      self.output_projection())

            for i, input in enumerate(decoder_inputs):
                if bs_decoding:
                    input = beam_decoder.wrap_input(input)

                if i > 0:
                    scope.reuse_variables()

                    if forward_only and not self.force_reading_input:
                        if self.decoding_algorithm == "beam_search":
                            (
                                past_cand_symbols,  # [batch_size, max_len]
                                past_cand_logprobs, # [batch_size]
                                past_beam_symbols,  # [batch_size*self.beam_size, max_len], right-aligned!!!
                                past_beam_logprobs, # [batch_size*self.beam_size]
                                past_cell_states,   # [batch_size*self.beam_size, max_len, dim]
                            ) = state
                            input = past_beam_symbols[:, -1]
                        elif self.decoding_algorithm == "greedy":
                            W, b = self.output_projection()
                            projected_output = tf.nn.log_softmax(tf.matmul(output, W) + b)
                            output_symbol = tf.argmax(projected_output, 1)
                            past_output_symbols = tf.concat(1, [past_output_symbols,
                                                                tf.expand_dims(output_symbol, 1)])
                            past_output_logits = tf.add(past_output_logits,
                                                        tf.reduce_max(projected_output, 1))
                            input = tf.cast(output_symbol, dtype=tf.int32)

                input_embedding = tf.nn.embedding_lookup(
                    self.token_embeddings(), input)

                if self.use_attention:
                    output, state, attn_alignments = \
                        decoder_cell(input_embedding, state, attn_alignments)
                else:
                    output, state = decoder_cell(input_embedding, state)

                # record output state to compute the loss.
                if bs_decoding:
                    # when doing beam search decoding, the output state of each
                    # step cannot simply be gathered step-wise outside the decoder
                    # (speical case: beam_size = 1)
                    pass
                else:
                    outputs.append(output)
                    states.append(state)

            if self.use_attention:
                # Tensor list --> tenosr
                attn_alignments = tf.concat(1, attn_alignments)

            if bs_decoding:
                # Beam-search output
                (
                    past_cand_symbols,  # [batch_size, max_len]
                    past_cand_logprobs, # [batch_size]
                    past_beam_symbols,  # [batch_size*self.beam_size, max_len], right-aligned!!!
                    past_beam_logprobs, # [batch_size*self.beam_size]
                    past_cell_states,
                ) = state
                # [self.batch_size, self.beam_size, max_len]
                top_k_outputs = tf.reshape(past_beam_symbols[:, 1:], [self.batch_size, self.beam_size, -1])
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
                    attn_alignments = tf.reshape(attn_alignments, [self.batch_size, self.beam_size,
                            len(decoder_inputs), attention_states.get_shape()[1].value])
                outputs = [tf.squeeze(s, squeeze_dims=[1])[:, -self.dim:]
                           for s in tf.split(1, past_cell_states.get_shape()[1],
                                             past_cell_states)[1:]]
                return top_k_outputs, top_k_logits, outputs, states, attn_alignments
            else:
                # Greedy output
                W, b = self.output_projection()
                projected_output = tf.nn.log_softmax(tf.matmul(output, W) + b)
                output_symbol = tf.argmax(projected_output, 1)
                past_output_symbols = tf.concat(1, [past_output_symbols,
                                                    tf.expand_dims(output_symbol, 1)])
                output_symbols = past_output_symbols[:, 1:]
                past_output_logits = tf.add(past_output_logits,
                                            tf.reduce_max(projected_output, 1))
                return output_symbols, past_output_logits, outputs, states, attn_alignments


    def decoder_cell(self):
        with tf.variable_scope("decoder_cell") as scope:
            cell = graph_utils.create_multilayer_cell(
                self.rnn_cell, scope, self.dim, self.num_layers,
                self.decoder_input_keep, self.decoder_output_keep)
            self.encoder_cell_vars = True
        return cell
