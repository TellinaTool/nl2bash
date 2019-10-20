"""
RNN-based decoders.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

from encoder_decoder import decoder, data_utils, graph_utils


class RNNDecoder(decoder.Decoder):
    def __init__(self, hyperparameters, scope, dim, embedding_dim, use_attention,
                 attention_function, input_keep, output_keep, decoding_algorithm):
        """
        :member hyperparameters:
        :member scope:
        :member dim:
        :member embedding_dim:
        :member use_attention:
        :member attention_function:
        :member input_keep:
        :member output_keep:
        :member decoding_algorithm:
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
        :param encoder_state: Encoder state => initial decoder state.
        :param decoder_inputs: Decoder training inputs ("<START>, ... <EOS>").
        :param input_embeddings: Decoder vocabulary embedding.
        :param encoder_attn_masks: Binary masks whose entries corresponding to non-padding tokens are 1.
        :param attention_states: Encoder hidden states.
        :param num_heads: Number of attention heads.
        :param encoder_copy_inputs: Array of encoder copy inputs where the copied words are represented using target
            vocab indices and place holding indices are used elsewhere.
        :return output_symbols: (batched) discrete output sequences
        :return output_logits: (batched) output sequence scores
        :return outputs: (batched) output states for all steps
        :return states: (batched) hidden states for all steps
        :return attn_alignments: (batched) attention masks (if attention is used)
        """
        if self.use_attention:
            assert(attention_states.get_shape()[1:2].is_fully_defined())
        if encoder_copy_inputs:
            assert(attention_states.get_shape()[1] == len(encoder_copy_inputs))
        bs_decoding = self.forward_only and \
                      self.decoding_algorithm == "beam_search"

        if input_embeddings is None:
            input_embeddings = self.embeddings()

        if self.force_reading_input:
            print("Warning: reading ground truth decoder inputs at decoding time.")

        with tf.compat.v1.variable_scope(self.scope + "_decoder_rnn") as scope:
            decoder_cell = self.decoder_cell()
            states = []
            alignments_list = []
            pointers = None

            # Cell Wrappers -- 'Attention', 'CopyNet', 'BeamSearch'
            if bs_decoding:
                beam_decoder = self.beam_decoder
                state = beam_decoder.wrap_state(encoder_state, self.output_project)
            else:
                state = encoder_state
                past_output_symbols = []
                past_output_logits = []

            if self.use_attention:
                if bs_decoding:
                    encoder_attn_masks = graph_utils.wrap_inputs(
                        beam_decoder, encoder_attn_masks)
                    attention_states = beam_decoder.wrap_input(attention_states)
                encoder_attn_masks = [tf.expand_dims(encoder_attn_mask, 1)
                    for encoder_attn_mask in encoder_attn_masks]
                encoder_attn_masks = tf.concat(axis=1, values=encoder_attn_masks)
                decoder_cell = decoder.AttentionCellWrapper(
                    decoder_cell,
                    attention_states,
                    encoder_attn_masks,
                    self.attention_function,
                    self.attention_input_keep,
                    self.attention_output_keep,
                    num_heads,
                    self.dim,
                    self.num_layers,
                    self.use_copy,
                    self.vocab_size
                )

            if self.use_copy and self.copy_fun == 'copynet':
                decoder_cell = decoder.CopyCellWrapper(
                    decoder_cell,
                    self.output_project,
                    self.num_layers,
                    encoder_copy_inputs,
                    self.vocab_size)

            if bs_decoding:
                decoder_cell = beam_decoder.wrap_cell(
                    decoder_cell, self.output_project)

            def step_output_symbol_and_logit(output):
                epsilon = tf.constant(1e-12)
                if self.copynet:
                    output_logits = tf.math.log(output + epsilon)
                else:
                    W, b = self.output_project
                    output_logits = tf.math.log(
                        tf.nn.softmax(tf.matmul(output, W) + b) + epsilon)
                output_symbol = tf.argmax(input=output_logits, axis=1)
                past_output_symbols.append(output_symbol)
                past_output_logits.append(output_logits)
                return output_symbol, output_logits

            for i, input in enumerate(decoder_inputs):
                if bs_decoding:
                    input = beam_decoder.wrap_input(input)

                if i > 0:
                    scope.reuse_variables()
                    if self.forward_only:
                        if self.decoding_algorithm == "beam_search":
                            (
                                past_beam_symbols,  # [batch_size*self.beam_size, max_len], right-aligned!!!
                                past_beam_logprobs, # [batch_size*self.beam_size]
                                past_cell_states,   # [batch_size*self.beam_size, max_len, dim]
                            ) = state
                            input = past_beam_symbols[:, -1]
                        elif self.decoding_algorithm == "greedy":
                            output_symbol, _ = step_output_symbol_and_logit(output)
                            if not self.force_reading_input:
                                input = tf.cast(output_symbol, dtype=tf.int32)
                    else:
                        step_output_symbol_and_logit(output)
                    if self.copynet:
                        decoder_input = input
                        input = tf.compat.v1.where(input >= self.target_vocab_size,
                                         tf.ones_like(input)*data_utils.UNK_ID, input)

                input_embedding = tf.nn.embedding_lookup(params=input_embeddings, ids=input)

                # Appending selective read information for CopyNet
                if self.copynet:
                    attn_length = attention_states.get_shape()[1]
                    attn_dim = attention_states.get_shape()[2]
                    if i == 0:
                        # Append dummy zero vector to the <START> token
                        selective_reads = tf.zeros([self.batch_size, attn_dim])
                        if bs_decoding:
                            selective_reads = beam_decoder.wrap_input(selective_reads)
                    else:
                        encoder_copy_inputs_2d = tf.concat(
                            [tf.expand_dims(x, 1) for x in encoder_copy_inputs], axis=1)
                        if self.forward_only:
                            copy_input = tf.compat.v1.where(decoder_input >= self.target_vocab_size,
                                                  tf.reduce_sum(
                                                    input_tensor=tf.one_hot(input-self.target_vocab_size, 
                                                               depth=attn_length, dtype=tf.int32)
                                                    * encoder_copy_inputs_2d,
                                                    axis=1),
                                                  decoder_input)
                        else:
                            copy_input = decoder_input
                        tiled_copy_input = tf.tile(input=tf.reshape(copy_input, [-1, 1]),
                                                   multiples=np.array([1, attn_length]))
                        # [batch_size(*self.beam_size), max_source_length]
                        selective_mask = tf.cast(tf.equal(tiled_copy_input, encoder_copy_inputs_2d),
                                                 dtype=tf.float32)
                        # [batch_size(*self.beam_size), max_source_length]
                        weighted_selective_mask = tf.nn.softmax(selective_mask * alignments[1])
                        # [batch_size(*self.beam_size), max_source_length, attn_dim]
                        weighted_selective_mask_3d = tf.tile(input=tf.expand_dims(weighted_selective_mask, 2), 
                                                             multiples=np.array([1, 1, attn_dim]))
                        # [batch_size(*self.beam_size), attn_dim]
                        selective_reads = tf.reduce_sum(input_tensor=weighted_selective_mask_3d * attention_states, axis=1)
                    input_embedding = tf.concat([input_embedding, selective_reads], axis=1)

                if self.copynet:
                    output, state, alignments, attns = \
                        decoder_cell(input_embedding, state)
                    alignments_list.append(alignments)
                elif self.use_attention:
                    output, state, alignments, attns = \
                        decoder_cell(input_embedding, state)
                    alignments_list.append(alignments)
                else:
                    output, state = decoder_cell(input_embedding, state)
               
                # save output states
                if not bs_decoding:
                    # when doing beam search decoding, the output state of each
                    # step cannot simply be gathered step-wise outside the decoder
                    # (speical case: beam_size = 1)
                    states.append(state)

            if self.use_attention:
                # Tensor list --> tenosr
                attn_alignments = tf.concat(axis=1,
                    values=[tf.expand_dims(x[0], 1) for x in alignments_list])
            if self.copynet:
                pointers = tf.concat(axis=1,
                    values=[tf.expand_dims(x[1], 1) for x in alignments_list])

            if bs_decoding:
                # Beam-search output
                (
                    past_beam_symbols,  # [batch_size*self.beam_size, max_len], right-aligned!!!
                    past_beam_logprobs, # [batch_size*self.beam_size]
                    past_cell_states,
                ) = state
                # [self.batch_size, self.beam_size, max_len]
                top_k_osbs = tf.reshape(past_beam_symbols[:, 1:],
                                        [self.batch_size, self.beam_size, -1])
                top_k_osbs = tf.split(axis=0, num_or_size_splits=self.batch_size,
                                      value=top_k_osbs)
                top_k_osbs = [tf.split(axis=0, num_or_size_splits=self.beam_size,
                                       value=tf.squeeze(top_k_output, axis=[0]))
                              for top_k_output in top_k_osbs]
                top_k_osbs = [[tf.squeeze(output, axis=[0]) for output in top_k_output]
                              for top_k_output in top_k_osbs]
                # [self.batch_size, self.beam_size]
                top_k_seq_logits = tf.reshape(past_beam_logprobs,
                                              [self.batch_size, self.beam_size])
                top_k_seq_logits = tf.split(axis=0, num_or_size_splits=self.batch_size,
                                            value=top_k_seq_logits)
                top_k_seq_logits = [tf.squeeze(top_k_logit, axis=[0])
                                    for top_k_logit in top_k_seq_logits]
                if self.use_attention:
                    attn_alignments = tf.reshape(attn_alignments,
                            [self.batch_size, self.beam_size, len(decoder_inputs),
                             attention_states.get_shape()[1]])
                # LSTM: ([batch_size*self.beam_size, :, dim],
                #        [batch_size*self.beam_size, :, dim])
                # GRU: [batch_size*self.beam_size, :, dim]
                if self.rnn_cell == 'lstm':
                    if self.num_layers == 1:
                        c_states, h_states = past_cell_states
                        states = list(zip(
                            [tf.squeeze(x, axis=[1])
                                for x in tf.split(c_states, c_states.get_shape()[1],
                                                  axis=1)],
                            [tf.squeeze(x, axis=[1])
                                for x in tf.split(h_states, h_states.get_shape()[1],
                                                  axis=1)]))
                    else:
                        layered_states = [list(zip(
                                [tf.squeeze(x, axis=[1]) 
                                    for x in tf.split(c_states, c_states.get_shape()[1],
                                                      axis=1)[1:]],
                                [tf.squeeze(x, axis=[1])
                                    for x in tf.split(h_states, h_states.get_shape()[1],
                                                      axis=1)[1:]]))
                            for c_states, h_states in past_cell_states]
                        states = list(zip(layered_states))
                elif self.rnn_cell in ['gru', 'ran']:
                    states = [tf.squeeze(x, axis=[1]) for x in \
                        tf.split(num_or_size_splits=past_cell_states.get_shape()[1],
                                 axis=1, value=past_cell_states)][1:]
                else:
                    raise AttributeError(
                        "Unrecognized rnn cell type: {}".format(self.rnn_cell))
                return top_k_osbs, top_k_seq_logits, states, \
                       states, attn_alignments, pointers
            else:
                # Greedy output
                step_output_symbol_and_logit(output)
                output_symbols = tf.concat(
                    [tf.expand_dims(x, 1) for x in past_output_symbols], axis=1)
                sequence_logits = tf.add_n([tf.reduce_max(input_tensor=x, axis=1) 
                                            for x in past_output_logits])
                return output_symbols, sequence_logits, past_output_logits, \
                       states, attn_alignments, pointers


    def decoder_cell(self):
        if self.copynet:
            input_size = self.dim * 2
        else:
            input_size = self.dim
        with tf.compat.v1.variable_scope(self.scope + "_decoder_cell") as scope:
            cell = graph_utils.create_multilayer_cell(
                self.rnn_cell, scope, self.dim, self.num_layers,
                self.input_keep, self.output_keep,
                variational_recurrent=self.variational_recurrent_dropout,
                input_dim=input_size)
        return cell
