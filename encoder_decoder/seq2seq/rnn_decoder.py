"""
RNN-based decoders.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from encoder_decoder import decoder, data_utils, graph_utils, rnn


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
        :return output_symbols: (batched) discrete output sequences
        :return output_logits: (batched) output sequence scores
        :return outputs: (batched) output states for all steps
        :return states: (batched) hidden states for all steps
        :return attn_alignments: (batched) attention masks (if attention is used)
        """
        if self.use_attention:
            assert(attention_states.get_shape()[1:2].is_fully_defined())
        bs_decoding = (self.decoding_algorithm == "beam_search")

        if input_embeddings is None:
            input_embeddings = self.embeddings()
        
        with tf.variable_scope(self.scope + "_decoder_rnn") as scope:
            decoder_cell = self.decoder_cell()

            # Initializations
            state = encoder_state
            states = []
            alignments_sequence = []
            pointers = []
            past_output_symbols = []
            past_output_logits = []
            if bs_decoding:
                beam_decoder = self.beam_decoder
                if self.forward_only:
                    state = beam_decoder.wrap_state(encoder_state, self.output_project)
                else:
                    beam_state = beam_decoder.wrap_state(encoder_state, self.output_project)
                    beam_search_losses = tf.zeros_like(decoder_inputs[0], dtype=tf.float32)
                    ground_truth_logprobs = [tf.zeros_like(beam_search_losses)]
                
            # --- Cell Wrappers: 'Attention', 'CopyNet', 'BeamSearch'

            # Attention Cell Wrapper
            if self.use_attention:
                if bs_decoding:
                    if self.forward_only:
                        encoder_attn_masks = graph_utils.wrap_inputs(
                            beam_decoder, encoder_attn_masks)
                        attention_states = beam_decoder.wrap_input(attention_states)
                    else:
                        beam_encoder_attn_masks = \
                            graph_utils.wrap_inputs(beam_decoder, encoder_attn_masks)
                        beam_attention_states = beam_decoder.wrap_input(attention_states)
                decoder_cell = decoder.AttentionCellWrapper(
                    decoder_cell,
                    attention_states,
                    encoder_attn_masks,
                    num_heads,
                    self.attention_function,
                    self.attention_input_keep,
                    self.attention_output_keep,
                    self.dim,
                    self.num_layers,
                    self.use_copy,
                    self.vocab_size
                )
                if bs_decoding and not self.forward_only:
                    beam_decoder_cell = decoder.AttentionCellWrapper(
                        decoder_cell,
                        beam_attention_states,
                        beam_encoder_attn_masks,
                        num_heads,
                        self.attention_function,
                        self.attention_input_keep,
                        self.attention_output_keep,
                        self.dim,
                        self.num_layers,
                        self.use_copy,
                        self.vocab_size
                    )
            # Copy Cell Wrapper
            if self.use_copy and self.copy_fun == 'copynet':
                if bs_decoding:
                    if self.forward_only:
                        encoder_copy_inputs = graph_utils.wrap_inputs(
                            beam_decoder, encoder_copy_inputs)
                    else:
                        beam_encoder_copy_inputs = graph_utils.wrap_inputs(
                            beam_decoder, encoder_copy_inputs)
                decoder_cell = decoder.CopyCellWrapper(
                    decoder_cell,
                    self.output_project,
                    self.num_layers,
                    encoder_copy_inputs,
                    self.vocab_size)
                if bs_decoding and not self.forward_only:
                    beam_decoder_cell = decoder.CopyCellWrapper(
                        beam_decoder_cell,
                        self.output_project,
                        self.num_layers,
                        encoder_copy_inputs,
                        self.vocab_size
                    )
            # Beam Search Cell Wrapper
            if bs_decoding:
                if self.forward_only:
                    decoder_cell = beam_decoder.wrap_cell(
                        decoder_cell, self.output_project)
                else:
                    # Beam search training: run beam search decoder in parallel
                    # to the RNN decoder which computes the log likelihood of
                    # the ground truth sequences
                    beam_decoder_cell = beam_decoder.wrap_cell(
                        beam_decoder_cell, self.output_project)

            # --- RNN Decoder Loop
            def step_output_symbol_and_logit(output):
                epsilon = tf.constant(1e-12)
                if self.copynet:
                    output_logits = tf.log(output + epsilon)
                else:
                    W, b = self.output_project
                    output_logits = tf.log(
                        tf.nn.softmax(tf.matmul(output, W) + b) + epsilon)
                output_symbol = tf.argmax(output_logits, 1)
                past_output_symbols.append(output_symbol)
                past_output_logits.append(output_logits)
                if bs_decoding and not self.forward_only:
                    ground_truth_logprobs.append(
                        tf.reduce_sum(tf.multiply(
                                output_logits,
                                tf.one_hot(target, tf.shape(output_logits)[1])),
                            axis=1))
                return output_symbol, output_logits

            def get_normalized_beam_logprobs(beam_symbols, beam_logprobs):
                """
                Compute the log probability of beam sequences after length
                normalization using the beam symbol sequences and the step-wise
                beam log probability sequences.

                :param beam_symbols: [batch_size*beam_size, seq_len+1]
                :param beam_logprobs: [batch_size*beam_size, seq_len+1]
                :return seq_logprobs: [batch_size*beam_size]
                """
                assert(beam_symbols.get_shape()[0].value == beam_logprobs.get_shape()[0].value)
                assert(beam_symbols.get_shape()[1].value == beam_logprobs.get_shape()[1].value)
                seq_len = tf.minimum(graph_utils.get_indices(beam_symbols[:, 1:],
                                                             data_utils.EOS_ID),
                                     graph_utils.get_indices(beam_symbols[:, 1:],
                                                             data_utils.PAD_ID))
                seq_logprobs = tf.div(tf.reduce_sum(beam_logprobs, axis=1),
                                      tf.pow(tf.cast(seq_len, tf.float32), self.alpha))
                return seq_logprobs

            def update_beam_state_with_restart(beam_state, restart_mask):
                """
                Reinitialize to search with ground-truth for batches where
                the ground truth sequences had fell out of beam.
                """
                (
                    past_beam_symbols,
                    past_beam_logprobs,
                    past_cell_states
                ) = beam_state
                beam_symbols_with_restart = tf.where(restart_mask,
                    beam_decoder.wrap_input(
                        graph_utils.column_array_to_matrix(
                            decoder_inputs[:i+2])),
                    past_beam_symbols)
                beam_logprobs_with_restart = tf.where(restart_mask,
                    beam_decoder.wrap_input(
                        graph_utils.column_array_to_matrix(
                            ground_truth_logprobs)),
                    past_beam_logprobs)
                first_in_beam_mask = tf.equal(
                    tf.range(self.batch_size * self.beam_size) % self.beam_size, 0)
                beam_logprobs_with_restart = tf.where(
                    first_in_beam_mask,
                    beam_logprobs_with_restart,
                    tf.ones_like(beam_logprobs_with_restart) * -1e18
                )
                # TODO: implement LSTM version
                ground_truth_states = tf.concat(
                    [tf.expand_dims(x, 1) for x in states], axis=1)
                cell_states_with_restart = tf.concat(
                    [past_cell_states[:, 0:1, :],
                     tf.where(restart_mask,
                        beam_decoder.wrap_input(ground_truth_states),
                        past_cell_states[:, 1:, :])],
                    axis=1)
      
                return (beam_symbols_with_restart,
                        beam_logprobs_with_restart,
                        cell_states_with_restart)

            for i in range(len(decoder_inputs)-1):
                if not self.forward_only or i == 0:
                    # Always read ground truth input at training time
                    input = decoder_inputs[i]

                if bs_decoding and i == 0:
                    if self.forward_only:
                        input = beam_decoder.wrap_input(input)
                    else:
                        beam_input = beam_decoder.wrap_input(input)

                input_embedding = tf.nn.embedding_lookup(input_embeddings, input)
                if bs_decoding and not self.forward_only:
                    beam_input_embedding = tf.nn.embedding_lookup(
                        input_embeddings, beam_input)
                    target = decoder_inputs[i+1]

                if self.copynet:
                    output, state, alignments, attns, read_copy_source = \
                        decoder_cell(input_embedding, state)
                    alignments_sequence.append(alignments)
                elif self.use_attention:
                    output, state, alignments, attns = \
                        decoder_cell(input_embedding, state)
                    alignments_sequence.append(alignments)
                else:
                    output, state = decoder_cell(input_embedding, state)
                if bs_decoding and not self.forward_only:
                    scope.reuse_variables()
                    if self.copynet:
                        beam_output, beam_state, beam_alignments, beam_attns, \
                            beam_read_copy_source = beam_decoder_cell(
                                beam_input_embedding, beam_state)
                    elif self.use_attention:
                        beam_output, beam_state, beam_alignments, beam_attns = \
                            beam_decoder_cell(beam_input_embedding, beam_state)
                    else:
                        beam_output, beam_state = beam_decoder_cell(
                            beam_input_embedding, beam_state)

                # save output states
                if not bs_decoding or not self.forward_only:
                    # when doing beam search decoding, the output state of each
                    # step cannot simply be gathered step-wise outside the decoder
                    # (speical case: beam_size = 1)
                    states.append(state)
                    alignments_sequence.append(alignments)

                scope.reuse_variables()
                if bs_decoding:
                    if self.forward_only:
                        (
                            past_beam_symbols,  # [batch_size*self.beam_size, i]
                            past_beam_logprobs, # [batch_size*self.beam_size, i]
                            past_cell_states,   # [batch_size*self.beam_size, i, dim]
                        ) = state
                        input = past_beam_symbols[:, -1]
                    else:
                        _, _ = step_output_symbol_and_logit(output)
                        (
                            past_beam_symbols,  # [batch_size*self.beam_size, i]
                            past_beam_logprobs, # [batch_size*self.beam_size, i]
                            past_cell_states,   # [batch_size*self.beam_size, i, dim]
                        ) = beam_state
                        beam_input = past_beam_symbols[:, -1]
                        # Compute beam search losses
                        beam_boundary = tf.reshape(get_normalized_beam_logprobs(
                            past_beam_symbols, past_beam_logprobs),
                            [self.batch_size, self.beam_size])[:, -1]
                        ground_truth_sequence_logprobs = \
                            get_normalized_beam_logprobs(
                                graph_utils.column_array_to_matrix(decoder_inputs[:i+2]),
                                graph_utils.column_array_to_matrix(ground_truth_logprobs))
                        beam_margin = ground_truth_sequence_logprobs - beam_boundary
                        beam_search_losses -= tf.where(beam_margin < self.margin, 
                            beam_margin, tf.ones_like(beam_margin) * self.margin)
                        # Update beam state when the ground truth falls out of the beam
                        restart_mask = beam_decoder.wrap_input(
                            ground_truth_sequence_logprobs < beam_boundary)
                        beam_state = update_beam_state_with_restart(
                            beam_state, restart_mask)
                else:
                    output_symbol, output_logits = \
                        step_output_symbol_and_logit(output)
                    if self.forward_only:
                        input = tf.cast(output_symbol, dtype=tf.int32)
                if self.copynet:
                    input = tf.where(input >= self.target_vocab_size,
                                     tf.ones_like(input)*data_utils.UNK_ID, input)

            # --- Decoder Output
            def process_beam_search_output(state):
                """
                Organize beam search output at the end of search.
                """
                (
                    past_beam_symbols,  # [batch_size*self.beam_size, max_len]
                    past_beam_logprobs, # [batch_size*self.beam_size, max_len]
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
                seq_logprobs = get_normalized_beam_logprobs(past_beam_symbols,
                                                            past_beam_logprobs)
                seq_logprobs = tf.reshape(seq_logprobs,
                                          [self.batch_size, self.beam_size])
                seq_logprobs = tf.split(axis=0, num_or_size_splits=self.batch_size,
                                        value=seq_logprobs)
                top_k_seq_logits = [tf.squeeze(logprob, axis=[0])
                                    for logprob in seq_logprobs]
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
                return top_k_osbs, top_k_seq_logits, states[1:]

            if self.use_attention:
                if not bs_decoding or not self.forward_only:
                    attn_alignments = tf.concat(axis=1, values=[tf.expand_dims(x[0], 1)
                        for x in alignments_sequence])
                else:
                    attn_alignments = alignments[0]
                if bs_decoding:
                    if self.forward_only:
                        attn_alignments = tf.reshape(attn_alignments,
                            [self.batch_size, self.beam_size,
                             attn_alignments.get_shape()[1].value, -1])
                    else:
                        beam_attn_alignments = tf.reshape(attn_alignments,
                            [self.batch_size, self.beam_size,
                             attn_alignments.get_shape()[1].value, -1])
            
            if self.copynet:
                if not bs_decoding or not self.forward_only:
                    pointers = tf.concat(axis=1, values=[tf.expand_dims(x[1], 1)
                        for x in alignments_sequence])
                else:
                    pointers = alignments[1]
                if bs_decoding:
                    if self.forward_only:
                        pointers = tf.reshape(pointers,
                            [self.batch_size, self.beam_size,
                             attn_alignments.get_shape()[1].value, -1])
                    else:
                        beam_pointers = tf.reshape(pointers,
                            [self.batch_size, self.beam_size,
                             attn_alignments.get_shape()[1].value, -1])

            if bs_decoding:
                if self.forward_only:
                    # Beam-search decoding output
                    top_k_osbs, top_k_seq_logits, states = \
                        process_beam_search_output(state)
                    return top_k_osbs, top_k_seq_logits, None, \
                           states, attn_alignments, pointers
                else:
                    # Beam-search training output
                    top_k_osbs, top_k_seq_logits, states = \
                        process_beam_search_output(beam_state)
                    return top_k_osbs, top_k_seq_logits, beam_search_losses, \
                        states, attn_alignments, pointers
            else:
                # Greedy output
                output_symbols = tf.concat(
                    [tf.expand_dims(x, 1) for x in past_output_symbols], axis=1)
                sequence_logits = tf.add_n([tf.reduce_max(x, axis=1) 
                                            for x in past_output_logits])
                return output_symbols, sequence_logits, past_output_logits, \
                       states, attn_alignments, pointers


    def decoder_cell(self):
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
