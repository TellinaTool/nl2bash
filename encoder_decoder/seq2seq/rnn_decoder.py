"""A set of sequence decoder modules used in the encoder-decoder framework."""

import tensorflow as tf

from encoder_decoder import decoder, data_utils, graph_utils

class RNNDecoder(decoder.Decoder):
    def __init__(self, hyperparameters, scope, vocab_size, dim, use_attention,
                 attention_function, input_keep, output_keep, decoding_algorithm,
                 forward_only, use_token_features=False):
        super(RNNDecoder, self).__init__(hyperparameters, scope, vocab_size,
            dim, use_attention, attention_function, input_keep, output_keep,
            decoding_algorithm, forward_only, use_token_features)
        print("{} dimension = {}".format(scope, dim))
        print("{} decoding_algorithm = {}".format(scope, decoding_algorithm))


    def define_graph(self, encoder_state, decoder_inputs,
                     input_embeddings=None, encoder_attn_masks=None,
                     attention_states=None, num_heads=1,
                     encoder_inputs=None, forward_only=False):
        """
        :return output_symbols: batch of discrete output sequences
        :return output_logits: batch of output sequence scores
        :return outputs: batch output states for all steps
        :return states: batch hidden states for all steps
        :return attn_alignments: batch attention masks
                                 (if attention mechanism is used)
        """

        if input_embeddings is None:
            input_embeddings = self.embeddings()

        if self.use_attention and \
                not attention_states.get_shape()[1:2].is_fully_defined():
            raise ValueError("Shape[1] and [2] of attention_states must be "
                             "known %s" % attention_states.get_shape())

        bs_decoding = forward_only and self.decoding_algorithm == "beam_search"

        if self.force_reading_input:
            print("Warning: reading ground truth decoder inputs at decoding time.")

        with tf.variable_scope(self.scope + "_decoder_rnn") as scope:
            decoder_cell = self.decoder_cell()
            outputs = []
            states = []
            attn_alignments = []

            # applying cell wrappers: ["attention", "beam"]
            if bs_decoding:
                beam_decoder = self.beam_decoder
                state = beam_decoder.wrap_state(
                    encoder_state, self.output_project)
                encoder_inputs = graph_utils.wrap_inputs(
                    beam_decoder, encoder_inputs)
            else:
                state = encoder_state
                past_output_symbols = []
                past_output_logits = tf.cast(decoder_inputs[0] * 0, tf.float32)

            if self.use_attention:
                if bs_decoding:
                    encoder_attn_masks = graph_utils.wrap_inputs(
                        beam_decoder, encoder_attn_masks)
                    attention_states = beam_decoder.wrap_input(attention_states)
                encoder_attn_masks = [tf.expand_dims(encoder_attn_mask, 1)
                    for encoder_attn_mask in encoder_attn_masks]
                encoder_attn_masks = tf.concat(1, encoder_attn_masks)
                decoder_cell = decoder.AttentionCellWrapper(
                    decoder_cell, attention_states, encoder_attn_masks,
                    encoder_inputs, self.attention_function,
                    self.attention_input_keep, self.attention_output_keep,
                    num_heads, self.num_layers, self.use_copy,
                    self.target_vocab_size)

            if self.use_copy and self.copy_fun != 'supervised':
                decoder_cell = decoder.CopyCellWrapper(decoder_cell,
                    self.output_project, self.num_layers, encoder_inputs,
                    self.target_vocab_size, self.generation_mask)

            if bs_decoding:
                decoder_cell = beam_decoder.wrap_cell(
                    decoder_cell, self.output_project)

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
                            if self.use_copy and self.copy_fun != 'supervised':
                                projected_output = graph_utils.normalize(output)
                            else:
                                W, b = self.output_project
                                projected_output = \
                                    tf.nn.log_softmax(tf.matmul(output, W) + b)
                            output_symbol = tf.argmax(projected_output, 1)
                            past_output_symbols.append(tf.expand_dims(output_symbol, 1))
                            past_output_logits = \
                                tf.add(past_output_logits, tf.reduce_max(projected_output, 1))
                            input = tf.cast(output_symbol, dtype=tf.int32)
                        input = tf.select(input >= self.target_vocab_size,
                            tf.ones(tf.shape(input)) * data_utils.UNK_ID, input)

                input_embedding = tf.nn.embedding_lookup(input_embeddings, input)
                if self.use_attention:
                    output, state, alignments = \
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
                attn_alignments = tf.concat(1,
                    [tf.expand_dims(x[0], 1) for x in alignments])
            if self.use_copy and self.copy_fun == 'explicit':
                pointers = tf.concat(1,
                    [tf.expand_dims(x[1], 1) for x in alignments])
            else:
                pointers = None

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
                states = tf.split(1, past_cell_states.get_shape()[1], past_cell_states)[1:]
                if self.use_copy and self.copy_fun != 'supervised':
                    # TODO: make beam search output logits computation in copy mode is right
                    # so far dummy zero vectors are used
                    outputs = [tf.zeros([self.batch_size * self.beam_size, self.target_vocab_size])
                               for s in states]
                else:
                    outputs = [tf.squeeze(s, squeeze_dims=[1])[:, -self.dim:] for s in states]
                return top_k_outputs, top_k_logits, outputs, states, \
                       attn_alignments, pointers
            else:
                # Greedy output
                if self.use_copy and self.copy_fun != 'supervised':
                    projected_output = graph_utils.normalize(output)
                else:
                    W, b = self.output_project
                    projected_output = tf.nn.log_softmax(tf.matmul(output, W) + b)
                output_symbol = tf.argmax(projected_output, 1)
                past_output_symbols.append(tf.expand_dims(output_symbol, 1))
                output_symbols = tf.concat(1, past_output_symbols) \
                    if forward_only else tf.cast(input, tf.float32)
                past_output_logits = tf.add(
                    past_output_logits, tf.reduce_max(projected_output, 1))
                return output_symbols, past_output_logits, outputs, states, \
                       attn_alignments, pointers


    def decoder_cell(self):
        with tf.variable_scope(self.scope + "_decoder_cell") as scope:
            cell = graph_utils.create_multilayer_cell(
                self.rnn_cell, scope, self.dim, self.num_layers,
                self.input_keep, self.output_keep)
        return cell
