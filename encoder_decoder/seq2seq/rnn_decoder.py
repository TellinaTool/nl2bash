"""
RNN-based decoders.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from encoder_decoder import decoder, data_utils, graph_utils, rnn

class RNNDecoder(decoder.Decoder):
    def __init__(self, hyperparameters, scope, dim, embedding_dim,
                 use_attention, attention_function, input_keep, output_keep,
                 decoding_algorithm):
        """
        :member hyperparameters:
        :member scope:
        :member vocab_size:
        :member dim:
        :member embedding_dim:
        :member use_attention:
        :member attention_function:
        :member input_keep:
        :member output_keep:
        :member decoding_algorithm:
        :member forward_only:
        :member use_token_features:
        """
        super(RNNDecoder, self).__init__(hyperparameters, scope, dim,
            embedding_dim, use_attention, attention_function, input_keep,
            output_keep, decoding_algorithm)
        print("{} dimension = {}".format(scope, dim))
        print("{} decoding_algorithm = {}".format(scope, decoding_algorithm))


    def define_graph(self, encoder_state, decoder_inputs,
                     input_embeddings=None, encoder_attn_masks=None,
                     attention_states=None, num_heads=1,
                     encoder_copy_inputs=None):
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
            raise ValueError("Shape [1] and [2] of attention_states must be "
                             "known %s" % attention_states.get_shape())

        bs_decoding = self.forward_only and self.decoding_algorithm == "beam_search"

        if self.force_reading_input:
            print("Warning: reading ground truth decoder inputs at decoding time.")

        with tf.variable_scope(self.scope + "_decoder_rnn") as scope:
            decoder_cell = self.decoder_cell()
            outputs = []
            states = []
            alignments_list = []

            # applying cell wrappers: ["attention", "beam"]
            if bs_decoding:
                beam_decoder = self.beam_decoder
                state = beam_decoder.wrap_state(
                    encoder_state, self.output_project)
                encoder_copy_inputs = graph_utils.wrap_inputs(
                    beam_decoder, encoder_copy_inputs)
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
                encoder_attn_masks = tf.concat(axis=1, values=encoder_attn_masks)
                decoder_cell = decoder.AttentionCellWrapper(
                    decoder_cell, attention_states, encoder_attn_masks,
                    encoder_copy_inputs, self.attention_function,
                    self.attention_input_keep, self.attention_output_keep,
                    num_heads, self.dim, self.num_layers, self.use_copy,
                    self.vocab_size)

            if self.use_copy and self.copy_fun != 'supervised':
                decoder_cell = decoder.CopyCellWrapper(decoder_cell,
                    self.output_project, self.num_layers, encoder_copy_inputs,
                    self.vocab_size, self.generation_mask)

            if bs_decoding:
                decoder_cell = beam_decoder.wrap_cell(
                    decoder_cell, self.output_project)

            for i, input in enumerate(decoder_inputs):
                if bs_decoding:
                    input = beam_decoder.wrap_input(input)

                if i > 0:
                    scope.reuse_variables()
                    if self.forward_only and not self.force_reading_input:
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
                                epsilon = tf.constant(1e-12)
                                projected_output = tf.log(output + epsilon)
                            else:
                                W, b = self.output_project
                                projected_output = \
                                    tf.nn.log_softmax(tf.matmul(output, W) + b)
                            output_symbol = tf.argmax(projected_output, 1)
                            past_output_symbols.append(tf.expand_dims(output_symbol, 1))
                            past_output_logits = \
                                tf.add(past_output_logits, tf.reduce_max(projected_output, 1))
                            input = tf.cast(output_symbol, dtype=tf.int32)
                        input = tf.where(input >= self.target_vocab_size,
                            tf.ones(tf.shape(input), dtype=tf.int32) * data_utils.UNK_ID, input)

                input_embedding = tf.nn.embedding_lookup(input_embeddings, input)

                if self.use_copynet:
                    if i == 0:
                        attn_dim = attention_states.get_shape()[2]
                        selective_reads = tf.zeros([self.batch_size, attn_dim])
                        if bs_decoding:
                            selective_reads = beam_decoder.wrap_input(selective_reads)
                    else:
                        selective_reads = attns[-1] * read_copy_source
                    input_embedding = tf.concat(axis=1, values=[input_embedding, selective_reads])
                    output, state, alignments, attns, read_copy_source = \
                        decoder_cell(input_embedding, state)
                    alignments_list.append(alignments)
                elif self.use_attention:
                    output, state, alignments, attns = \
                        decoder_cell(input_embedding, state)
                    alignments_list.append(alignments)
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
                attn_alignments = tf.concat(axis=1,
                    values=[tf.expand_dims(x[0], 1) for x in alignments_list])
            if self.use_copynet:
                pointers = tf.concat(axis=1,
                    values=[tf.expand_dims(x[1], 1) for x in alignments_list])
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
                top_k_outputs = tf.reshape(past_beam_symbols[:, 1:],
                                           [self.batch_size, self.beam_size, -1])
                top_k_outputs = tf.split(axis=0, num_or_size_splits=self.batch_size, value=top_k_outputs)
                top_k_outputs = [tf.split(axis=0, num_or_size_splits=self.beam_size,
                                          value=tf.squeeze(top_k_output, axis=[0]))
                                 for top_k_output in top_k_outputs]
                top_k_outputs = [[tf.squeeze(output, axis=[0]) for output in top_k_output]
                                 for top_k_output in top_k_outputs]
                # [self.batch_size, self.beam_size]
                top_k_logits = tf.reshape(past_beam_logprobs,
                                          [self.batch_size, self.beam_size])
                top_k_logits = tf.split(axis=0, num_or_size_splits=self.batch_size, value=top_k_logits)
                top_k_logits = [tf.squeeze(top_k_logit, axis=[0])
                                for top_k_logit in top_k_logits]
                if self.use_attention:
                    attn_alignments = tf.reshape(attn_alignments,
                            [self.batch_size, self.beam_size, len(decoder_inputs),
                             attention_states.get_shape()[1].value])
                # LSTM: ([batch_size*self.beam_size, :, dim],
                #        [batch_size*self.beam_size, :, dim])
                # GRU: [batch_size*self.beam_size, :, dim]
                if self.rnn_cell == 'lstm':
                    if self.num_layers == 1:
                        c_states, h_states = past_cell_states
                        states = list(zip(
                            [tf.squeeze(x, axis=[1])
                             for x in tf.split(axis=1, num_or_size_splits=c_states.get_shape()[1], value=c_states)],
                            [tf.squeeze(x, axis=[1])
                             for x in tf.split(axis=1, num_or_size_splits=h_states.get_shape()[1], value=h_states)]))
                    else:
                        layered_states = [list(zip(
                                [tf.squeeze(x, axis=[1]) 
                                    for x in tf.split(axis=1, num_or_size_splits=c_states.get_shape()[1], value=c_states)],
                                [tf.squeeze(x, axis=[1])
                                    for x in tf.split(axis=1, num_or_size_splits=h_states.get_shape()[1], value=h_states)]))
                            for c_states, h_states in past_cell_states]
                        states = list(zip(layered_states))
                elif self.rnn_cell in ['gru', 'ran']:
                    states = [tf.squeeze(x, axis=[1]) for x in \
                        tf.split(axis=1, num_or_size_splits=past_cell_states.get_shape()[1], value=past_cell_states)][1:]
                else:
                    raise AttributeError(
                        "Unrecognized rnn cell type: {}".format(self.rnn_cell))

                if self.use_copy and self.copy_fun != 'supervised':
                    # TODO: correct beam search output logits computation in copy modes
                    # so far dummy zero vectors are used
                    outputs = [tf.zeros([self.batch_size * self.beam_size, self.vocab_size])
                               for s in states]
                else:
                    if self.rnn_cell in ['gru', 'ran']:
                        outputs = [s[:, -self.dim:] for s in states]
                    else:
                        if self.num_layers == 1:
                            outputs = [s[1] for s in states]
                        else:
                            outputs = [s[-1][1] for s in states]

                return top_k_outputs, top_k_logits, outputs, states, attn_alignments, pointers
            else:
                # Greedy output
                if self.use_copynet:
                    epsilon = tf.constant(1e-12)
                    projected_output = tf.log(output + epsilon)
                else:
                    W, b = self.output_project
                    projected_output = tf.nn.log_softmax(tf.matmul(output, W) + b)
                output_symbol = tf.argmax(projected_output, 1)
                past_output_symbols.append(tf.expand_dims(output_symbol, 1))
                output_symbols = tf.concat(axis=1, values=past_output_symbols) \
                    if self.forward_only else tf.cast(input, tf.float32)
                past_output_logits = tf.add(
                    past_output_logits, tf.reduce_max(projected_output, 1))
                return output_symbols, past_output_logits, outputs, states, \
                    attn_alignments, pointers


    def decoder_cell(self):
        if self.use_copy and self.copy_fun != 'supervised':
            input_size = 2 * self.dim
        else:
            input_size = self.dim
        with tf.variable_scope(self.scope + "_decoder_cell") as scope:
            cell = rnn.create_multilayer_cell(
                self.rnn_cell, scope, self.dim, self.num_layers,
                self.input_keep, self.output_keep,
                variational_recurrent=self.variational_recurrent_dropout,
                batch_normalization=self.recurrent_batch_normalization,
                forward_only=self.forward_only,
                input_dim=input_size)
        return cell
