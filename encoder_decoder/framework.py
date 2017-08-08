"""Encoder-decoder model with attention mechanism."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import numpy as np

import tensorflow as tf

from encoder_decoder import data_utils, graph_utils
from encoder_decoder.seq2seq import rnn_decoder


DEBUG = False

class EncoderDecoderModel(graph_utils.NNModel):

    def __init__(self, hyperparams, buckets=None):
        """Create the model.

        Hyperparameters:
          source_vocab_size: size of the source vocabulary.
          target_vocab_size: size of the target vocabulary.
          buckets: a list of pairs (I, O), where I specifies maximum input length
            that will be processed in that bucket, and O specifies maximum output
            length. Training instances that have inputs longer than I or outputs
            longer than O will be pushed to the next bucket and padded accordingly.
            We assume that the list is sorted, e.g., [(2, 4), (8, 16)].
          size: number of units in each layer of the model.
          num_layers: number of layers in the model.
          max_gradient_norm: gradients will be clipped to maximally this norm.
          batch_size: the size of the batches used during training;
            the model construction is independent of batch_size, so it can be
            changed after initialization if this is convenient, e.g., for decoding.
          learning_rate: learning rate to start with.
          learning_rate_decay_factor: decay learning rate by this much when needed.
          use_lstm: if true, we use LSTM cells instead of GRU cells.
          num_samples: number of samples for sampled softmax.
          use_attention: if set, use attention model.
        """
        super(EncoderDecoderModel, self).__init__(hyperparams, buckets)
        self.learning_rate = tf.Variable(
            float(hyperparams["learning_rate"]), trainable=False)
        self.learning_rate_decay_op = self.learning_rate.assign(
            self.learning_rate * hyperparams["learning_rate_decay_factor"])

        self.global_epoch = tf.Variable(0, trainable=False)

        # Encoder.
        self.define_encoder(self.sc_input_keep, self.sc_output_keep)

        # Decoder.
        decoder_embedding_dim = self.encoder.output_dim
        decoder_dim = decoder_embedding_dim
        self.define_decoder(decoder_dim, decoder_embedding_dim,
                            self.tg_token_use_attention,
                            self.tg_token_attn_fun,
                            self.tg_input_keep,
                            self.tg_output_keep)

        # Character Decoder.
        if self.tg_char:
            self.define_char_decoder(self.decoder.dim, False,
                self.tg_char_rnn_input_keep, self.tg_char_rnn_output_keep)

        self.define_graph()

    # --- Graph Operations --- #

    def define_graph(self):
        self.debug_vars = []

        # Feeds for inputs.
        self.encoder_inputs = []        # encoder inputs.
        self.encoder_full_inputs = []   # encoder inputs without unknown tokens.
        self.encoder_attn_masks = []    # mask out PAD symbols in the encoder
        self.decoder_inputs = []        # decoder inputs (always start with "_GO").
        self.decoder_full_inputs = []   # decoder inputs without unknown tokens.
        self.target_weights = []        # weights at each position of the target sequence.
        self.pointer_targets = None

        for i in xrange(self.max_source_length):
            self.encoder_inputs.append(
                tf.placeholder(
                    tf.int32, shape=[None], name="encoder{0}".format(i)))
            self.encoder_full_inputs.append(
                tf.placeholder(
                    tf.int32, shape=[None], name="encoder_full{0}".format(i)))
            self.encoder_attn_masks.append(
                tf.placeholder(
                    tf.float32, shape=[None], name="attn_alignment{0}".format(i)))
        self.encoder_channel_inputs = \
            [self.encoder_inputs, self.encoder_full_inputs]
        if self.sc_char:
            self.char_encoder_inputs = []
            for i in xrange(self.max_source_length):
                self.char_encoder_inputs.append(
                    tf.placeholder(tf.int32, shape=[None, self.max_target_token_size],
                                   name="char_encoder{0}".format(i)))
            self.encoder_channel_inputs.append(self.char_encoder_inputs)

        for i in xrange(self.max_target_length + 1):
            self.decoder_inputs.append(
                tf.placeholder(
                    tf.int32, shape=[None], name="decoder{0}".format(i)))
            self.decoder_full_inputs.append(
                tf.placeholder(
                    tf.int32, shape=[None], name="decoder_full{0}".format(i)))
            self.target_weights.append(
                tf.placeholder(
                    tf.float32, shape=[None], name="weight{0}".format(i)))

        # Our targets are decoder inputs shifted by one.
        if self.use_copynet:
            self.targets = [self.decoder_full_inputs[i + 1]
                            for i in xrange(self.max_target_length)]
        else:
            self.targets = [self.decoder_inputs[i + 1]
                            for i in xrange(self.max_target_length)]

        if self.tg_char:
            # inputs for character generation
            self.char_decoder_inputs = []   # decoder inputs (always start with "_CGO")
                                            # [batch_size*max_target_token_size, dim]
            self.char_target_weights = []   # weights at each position of the target sequence
            for i in xrange(self.max_target_length):
                self.char_decoder_inputs.append(
                    tf.placeholder(tf.int32,
                                   shape=[None, self.max_target_token_size + 2],
                                   name="char_decoder{0}".format(i)))
                self.char_target_weights.append(
                    tf.placeholder(tf.float32,
                                   shape=[None, self.max_target_token_size + 1],
                                   name="char_target_weight{0}".format(i)))
            self.char_targets = [self.char_decoder_inputs[i][:, 1:]
                                 for i in xrange(self.max_target_length)]

        if self.use_copy and self.copy_fun == 'supervised':
            for i in xrange(self.max_target_length):
                self.pointer_targets = tf.placeholder(
                    tf.int32, shape=[None, None, None], name="pointer_targets")

        # Compute training outputs and losses in the forward direction.
        if self.buckets:
            self.output_symbols = []
            self.output_logits = []
            self.losses = []
            self.attn_alignments = []
            self.pointers = []
            if self.tg_char:
                self.char_output_symbols = []
                self.char_output_logits = []
            with tf.variable_scope(tf.get_variable_scope()) as scope:
                for bucket_id, bucket in enumerate(self.buckets):
                    print("creating bucket {} ({}, {})...".format(
                            bucket_id, bucket[0], bucket[1]))
                    if bucket_id > 0:
                        scope.reuse_variables()
                    encode_decode_outputs = \
                        self.encode_decode(
                            [channel_input[:bucket[0]] for channel_input in
                             self.encoder_channel_inputs],
                            self.encoder_attn_masks[:bucket[0]],
                            self.decoder_inputs,
                            self.targets[:bucket[1]],
                            self.target_weights[:bucket[1]],
                        )
                    bucket_output_symbols, bucket_output_logits, bucket_losses, \
                        batch_attn_alignments = encode_decode_outputs[:4]
                    self.output_symbols.append(bucket_output_symbols)
                    self.output_logits.append(bucket_output_logits)
                    self.losses.append(bucket_losses)
                    self.attn_alignments.append(batch_attn_alignments)
                    if self.forward_only and self.tg_char:
                         bucket_char_output_symbols, bucket_char_output_logits = \
                             encode_decode_outputs[4:6]
                         self.char_output_symbols.append(
                             tf.reshape(bucket_char_output_symbols,
                                        [self.max_target_length,
                                         self.batch_size, self.beam_size,
                                         self.max_target_token_size + 1]))
                         self.char_output_logits.append(
                             tf.reshape(bucket_char_output_logits,
                                        [self.max_target_length,
                                        self.batch_size, self.beam_size]))
                    if self.use_copy:
                        self.pointers.append(encode_decode_outputs[-1])
        else:
            encode_decode_outputs = self.encode_decode(
                                        self.encoder_channel_inputs,
                                        self.encoder_attn_masks,
                                        self.decoder_inputs,
                                        self.targets,
                                        self.target_weights
                                    )
            self.output_symbols, self.output_logits, self.losses, \
                self.attn_alignments = encode_decode_outputs[:4]
            if self.tg_char:
                char_output_symbols, char_output_logits = \
                    encode_decode_outputs[4:6]
                self.char_output_symbols = tf.reshape(char_output_symbols,
                                   [self.batch_size, self.beam_size,
                                    self.max_target_length,
                                    self.max_target_token_size])
                self.char_output_logits = tf.reshape(char_output_logits,
                                   [self.batch_size, self.beam_size,
                                    self.max_target_length])
            if self.forward_only and self.use_copy:
                self.pointers = encode_decode_outputs[-1]


        # Gradients and SGD updates in the backward direction.
        if not self.forward_only:
            params = tf.trainable_variables()
            if self.optimizer == "sgd":
                opt = tf.train.GradientDescentOptimizer(self.learning_rate)
            elif self.optimizer == "adam":
                opt = tf.train.AdamOptimizer(
                    self.learning_rate, beta1=0.9, beta2=0.999,
                    epsilon=self.adam_epsilon, )
            else:
                raise ValueError("Unrecognized optimizer type.")

            if self.buckets:
                self.gradient_norms = []
                self.updates = []
                for bucket_id, _ in enumerate(self.buckets):
                    gradients = tf.gradients(self.losses[bucket_id], params)
                    clipped_gradients, norm = tf.clip_by_global_norm(
                        gradients, self.max_gradient_norm)
                    self.gradient_norms.append(norm)
                    self.updates.append(opt.apply_gradients(
                        zip(clipped_gradients, params)))
            else:
                gradients = tf.gradients(self.losses, params)
                clipped_gradients, norm = tf.clip_by_global_norm(
                    gradients, self.max_gradient_norm)
                self.gradient_norms = norm
                self.updates = opt.apply_gradients(zip(clipped_gradients, params))

        self.saver = tf.train.Saver(tf.global_variables())


    def encode_decode(self, encoder_channel_inputs, encoder_attn_masks,
                      decoder_inputs, targets, target_weights):

        encoder_outputs, encoder_states = \
            self.encoder.define_graph(encoder_channel_inputs)
        if self.tg_token_use_attention:
            top_states = [tf.reshape(m, [-1, 1, self.encoder.output_dim])
                          for m in encoder_outputs]
            attention_states = tf.concat(axis=1, values=top_states)
        else:
            attention_states = None

        num_heads = 2 if (self.tg_token_use_attention and 
                          self.use_copynet) else 1

        # --- Run encode-decode steps --- #
        output_symbols, output_logits, outputs, states, attn_alignments, \
            pointers = self.decoder.define_graph(
                        encoder_states[-1], decoder_inputs,
                        encoder_attn_masks=encoder_attn_masks,
                        attention_states=attention_states,
                        num_heads=num_heads,
                        encoder_copy_inputs=self.encoder_full_inputs)

        bs_decoding = self.forward_only and \
                      self.token_decoding_algorithm == 'beam_search'

        # --- Compute Losses --- #

        # A. Sequence Loss
        if self.forward_only or self.training_algorithm == "standard":
            if bs_decoding:
                targets = graph_utils.wrap_inputs(
                    self.decoder.beam_decoder, targets)
            if self.use_copynet:
                step_loss_fun = graph_utils.sparse_cross_entropy
            else:
                step_loss_fun = graph_utils.softmax_loss(
                    self.decoder.output_project,
                    self.num_samples,
                    self.target_vocab_size)
            encoder_decoder_token_loss = self.sequence_loss(
                outputs, targets, target_weights, step_loss_fun)
        else:
            raise AttributeError("Unrecognized training algorithm.")

        # B. Attention Regularization
        attention_reg = self.attention_regularization(attn_alignments) \
            if self.tg_token_use_attention else 0

        # C. Supervised Copying Loss (if any)
        if self.use_copy and self.copy_fun == 'supervised':
            if bs_decoding:
                pointer_targets = self.decoder.beam_decoder.wrap_input(
                    self.pointer_targets)
            else:
                pointer_targets = self.pointer_targets
            copy_loss = self.copy_loss(pointers, pointer_targets)
        else:
            copy_loss = 0

        # D. Character Sequence Loss
        if self.tg_char:
            # re-arrange character inputs
            char_decoder_inputs = [
                tf.squeeze(x, 1) for x in tf.split(axis=1, num_or_size_splits=self.max_target_token_size + 2,
                                                   value=tf.concat(axis=0, values=self.char_decoder_inputs))]
            char_targets = [
                tf.squeeze(x, 1) for x in tf.split(axis=1, num_or_size_splits=self.max_target_token_size + 1,
                                                   value=tf.concat(axis=0, values=self.char_targets))]
            char_target_weights = [
                tf.squeeze(x, 1) for x in tf.split(axis=1, num_or_size_splits=self.max_target_token_size + 1,
                                                   value=tf.concat(axis=0, values=self.char_target_weights))]
            if bs_decoding:
                char_decoder_inputs = graph_utils.wrap_inputs(
                    self.decoder.beam_decoder, char_decoder_inputs)
                char_targets = graph_utils.wrap_inputs(
                    self.decoder.beam_decoder, char_targets)
                char_target_weights = graph_utils.wrap_inputs(
                    self.decoder.beam_decoder, char_target_weights)
            # get initial state from decoder output
            char_decoder_init_state = \
                tf.concat(axis=0, values=[tf.reshape(d_o, [-1, self.decoder.dim]) for d_o in outputs])
            char_output_symbols, char_output_logits, char_outputs, _, _ = \
                self.char_decoder.define_graph(
                    char_decoder_init_state, char_decoder_inputs)
            encoder_decoder_char_loss = self.sequence_loss(
                char_outputs, char_targets, char_target_weights,
                graph_utils.softmax_loss(
                    self.char_decoder.output_project,
                    self.tg_char_vocab_size / 2,
                    self.tg_char_vocab_size))
        else:
            encoder_decoder_char_loss = 0
       
        losses = encoder_decoder_token_loss + \
                 self.gamma * encoder_decoder_char_loss + \
                 self.chi * copy_loss + \
                 self.beta * attention_reg

        # store encoder/decoder output states
        self.encoder_hidden_states = tf.concat(axis=1,
            values=[tf.reshape(e_o, [-1, 1, self.encoder.output_dim])
                    for e_o in encoder_outputs])
        
        top_states = []
        if self.rnn_cell == 'gru':
            for state in states:
                top_states.append(state[:, -self.decoder.dim:])
        elif self.rnn_cell == 'lstm':
            for state in states:
                if self.num_layers > 1:
                    top_states.append(state[-1][1])
                else:
                    top_states.append(state[1])
        self.decoder_hidden_states = tf.concat(axis=1,
            values=[tf.reshape(d_o, [-1, 1, self.decoder.dim])
                    for d_o in top_states])

        O = [output_symbols, output_logits, losses, attn_alignments]
        if self.tg_char:
            O.append(char_output_symbols)
            O.append(char_output_logits)
        if self.use_copy:
            O.append(pointers)
        return O


    # Loss functions.
    def sequence_loss(self, logits, targets, target_weights, loss_function):
        targets = targets[:len(logits)]
        weights = target_weights[:len(logits)]

        with tf.variable_scope("sequence_loss"):
            log_perp_list = []
            for logit, target, weight in zip(logits, targets, weights):
                crossent = loss_function(logit, target)
                log_perp_list.append(crossent * weight)
            log_perps = tf.add_n(log_perp_list)
            total_size = tf.add_n(weights)
            total_size += 1e-12     # Just to avoid division by 0 for all-0 weights.
            log_perps /= total_size

        avg_log_perps = tf.reduce_mean(log_perps)

        return avg_log_perps


    def copy_loss(self, pointers, pointer_targets):
        raw_loss = tf.reshape(
                tf.nn.softmax_cross_entropy_with_logits(
                     logits=tf.reshape(pointers, [-1, self.max_source_length]), 
                     labels=tf.reshape(pointer_targets, [-1, self.max_source_length])),
                [-1, self.max_target_length])
        copy_positions = tf.cast(tf.reduce_sum(pointer_targets, 2), tf.floatf2)
        return tf.reduce_mean(
                tf.reduce_sum(tf.multiply(raw_loss, copy_positions), 1) /
                (tf.reduce_sum(copy_positions, 1) + 1e-12))


    def attention_regularization(self, attn_alignments):
        """Entropy regularization term.

        :param attn_alignments: [batch_size, decoder_size, encoder_size]
        """
        # P_unnorm = tf.reduce_sum(attn_alignments, 1)
        # Z = tf.reduce_sum(P_unnorm, 1, keep_dims=True)
        # P = P_unnorm / Z
        # return tf.reduce_mean(tf.reduce_sum(P * tf.log(P), 1))

        P = tf.reduce_sum(attn_alignments, 1)
        P_exp = tf.exp(P)
        Z = tf.reduce_sum(P_exp, 1, keep_dims=True)
        return tf.reduce_mean(tf.reduce_sum(P_exp / Z * (P - tf.log(Z)), 1))


    def define_encoder(self, input_keep, output_keep):
        """Placeholder function."""
        self.encoder = None


    def define_decoder(self, dim, embedding_dim, use_attention,
                       attention_function, input_keep, output_keep):
        """Placeholder function."""
        self.decoder = None


    def define_char_decoder(self, dim, use_attention, input_keep, output_keep):
        """
        Define the decoder which does character-level generation of a token.
        """
        if self.tg_char_composition == 'rnn':
            self.char_decoder = rnn_decoder.RNNDecoder(self.hyperparams,
                "char_decoder", self.tg_char_vocab_size, dim, use_attention,
                input_keep, output_keep, self.char_decoding_algorithm)
        else:
            raise ValueError("Unrecognized target character composition: {}."
                             .format(self.tg_char_composition))

    # --- Graph Operations --- #

    def format_batch(self, encoder_inputs, decoder_inputs, pointer_targets=None,
                     bucket_id=-1):
        """
        Convert the feature vectors into the dimensions required by the neural
        network.
        """
        def load_channel(inputs, output_length, reversed_output=True):
            """
            :param inputs: batch of feature vectors
            :param output_length: length of the output sequence
            :param reversed_output: if set, reverse the padded inputs
            :return: batched input sequence
            """
            padded_inputs = []
            batch_inputs = []
            for batch_idx in xrange(batch_size):
                input = inputs[batch_idx]
                paddings = [data_utils.PAD_ID] * (output_length - len(input))
                if reversed_output:
                    padded_inputs.append(list(reversed(input + paddings)))
                else:
                    padded_inputs.append(input + paddings)
            for length_idx in xrange(output_length):
                batch_inputs.append(
                    np.array([padded_inputs[batch_idx][length_idx]
                        for batch_idx in xrange(batch_size)], dtype=np.int32))
            return batch_inputs

        if bucket_id >= 0:
            encoder_size, decoder_size = self.buckets[bucket_id]
        else:
            encoder_size, decoder_size = \
                self.max_source_length, self.max_target_length

        batch_size = len(encoder_inputs)

        # create batch-major vectors
        batch_encoder_inputs = load_channel(
            encoder_inputs, encoder_size, reversed_output=True)
        batch_decoder_inputs = load_channel(
            decoder_inputs, decoder_size, reversed_output=False)

        batch_encoder_input_masks = []
        batch_decoder_input_masks = []
        for length_idx in xrange(encoder_size):
            batch_encoder_input_mask = np.ones(batch_size, dtype=np.float32)
            for batch_idx in xrange(batch_size):
                source = batch_encoder_inputs[length_idx][batch_idx]
                if source == data_utils.PAD_ID:
                    batch_encoder_input_mask[batch_idx] = 0.0
            batch_encoder_input_masks.append(batch_encoder_input_mask)

        for length_idx in xrange(decoder_size):
            # Create target_weights to be 0 for targets that are padding.
            batch_decoder_input_mask = np.ones(batch_size, dtype=np.float32)
            for batch_idx in xrange(batch_size):
                # We set weight to 0 if the corresponding target is a PAD symbol.
                # The corresponding target is decoder_input shifted by 1 forward.
                if length_idx < decoder_size - 1:
                    target = batch_decoder_inputs[length_idx+1][batch_idx]
                if length_idx == decoder_size - 1 or target == data_utils.PAD_ID:
                    batch_decoder_input_mask[batch_idx] = 0.0
            batch_decoder_input_masks.append(batch_decoder_input_mask)

        E = Example()
        E.encoder_inputs = batch_encoder_inputs
        E.encoder_attn_masks = batch_encoder_input_masks
        E.decoder_inputs = batch_decoder_inputs
        E.target_weights = batch_decoder_input_masks

        if self.use_copy and self.copy_fun == 'supervised':
            E.pointer_targets = np.concatenate(pointer_targets, 0)\
                [:, :decoder_size, -encoder_size:]

        return E


    def get_batch(self, data, bucket_id=-1, use_all=False):
        """
        Randomly sample a batch of examples from the specified bucket and
        convert the feature vectors into the dimensions required by the neural
        network.
        """
        encoder_inputs, decoder_inputs, pointer_targets = [], [], []

        if bucket_id == -1:
            sample_pool = data
        else:
            sample_pool = data[bucket_id]

        # Randomly sample a batch of encoder and decoder inputs from data
        data_ids = list(xrange(len(sample_pool)))
        if not use_all:
            data_ids = np.random.choice(data_ids, self.batch_size)
        for i in data_ids:
            data_point = sample_pool[i]
            encoder_inputs.append(data_point.sc_ids)
            decoder_inputs.append(data_point.tg_ids)
            if self.use_copy and self.copy_fun == 'supervised':
                pointer_targets.append(data_point.pointer_targets)

        return self.format_batch(encoder_inputs, decoder_inputs,
            pointer_targets=pointer_targets, bucket_id=bucket_id)


    def feed_input(self, E):
        """
        Assign the data vectors to the corresponding neural network variables.
        """
        encoder_size, decoder_size = len(E.encoder_inputs), len(E.decoder_inputs)
        input_feed = {}
        for l in xrange(encoder_size):
            input_feed[self.encoder_inputs[l].name] = E.encoder_inputs[l]
            input_feed[self.encoder_attn_masks[l].name] = E.encoder_attn_masks[l]
        for l in xrange(decoder_size):
            input_feed[self.decoder_inputs[l].name] = E.decoder_inputs[l]
            input_feed[self.target_weights[l].name] = E.target_weights[l]
        # Since our targets are decoder inputs shifted by one, we need one more.
        last_target = self.decoder_inputs[decoder_size].name
        input_feed[last_target] = np.zeros(E.decoder_inputs[0].shape, dtype=np.int32)

        if self.use_copy and self.copy_fun == 'supervised':
            input_feed[self.pointer_targets.name] = E.pointer_targets

        return input_feed


    def step(self, session, formatted_example, bucket_id=-1, forward_only=False):
        """Run a step of the model feeding the given inputs.
        :param session: tensorflow session to use.
        :param encoder_inputs: list of numpy int vectors to feed as encoder inputs.
        :param attn_alignments: list of numpy int vectors to feed as the mask
            over inputs about which tokens to attend to.
        :param decoder_inputs: list of numpy int vectors to feed as decoder inputs.
        :param target_weights: list of numpy float vectors to feed as target weights.
        :param bucket_id: which bucket of the model to use.
        :param forward_only: whether to do the backward step or only forward.
        :param return_rnn_hidden_states: if set to True, return the hidden states
            of the two RNNs.
        :return (gradient_norm, average_perplexity, outputs)
        """

        # Input feed: encoder inputs, decoder inputs, target_weights, as provided.
        input_feed = self.feed_input(formatted_example)

        # Output feed: depends on whether we do a backward step or not.
        if not forward_only:
            if bucket_id == -1:
                output_feed = {
                    'updates': self.updates,                    # Update Op that does SGD.
                    'gradient_norms': self.gradient_norms,      # Gradient norm.
                    'losses': self.losses}                      # Loss for this batch.
            else:
                output_feed = {
                    'updates': self.updates[bucket_id],         # Update Op that does SGD.
                    'gradient_norms': self.gradient_norms[bucket_id],  # Gradient norm.
                    'losses': self.losses[bucket_id]}           # Loss for this batch.
        else:
            if bucket_id == -1:
                output_feed = {
                    'output_symbols': self.output_symbols,      # Loss for this batch.
                    'output_logits': self.output_logits,        # Batch output sequence
                    'losses': self.losses}                      # Batch output scores
            else:
                output_feed = {
                    'output_symbols': self.output_symbols[bucket_id], # Loss for this batch.
                    'output_logits': self.output_logits[bucket_id],   # Batch output sequence
                    'losses': self.losses[bucket_id]}           # Batch output logits

        if self.tg_token_use_attention:
            if bucket_id == -1:
                output_feed['attn_alignments'] = self.attn_alignments
            else:
                output_feed['attn_alignments'] = self.attn_alignments[bucket_id]

        output_feed['encoder_hidden_states'] = self.encoder_hidden_states
        output_feed['decoder_hidden_states'] = self.decoder_hidden_states

        if self.use_copy:
            if bucket_id == -1:
                output_feed['pointers'] = self.pointers
            else:
                output_feed['pointers'] = self.pointers[bucket_id]

        extra_update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        if extra_update_ops and not forward_only:
            outputs, extra_updates = session.run(
                [output_feed, extra_update_ops], input_feed)
        else:
            outputs = session.run(output_feed, input_feed)

        O = Output()
        if not forward_only:
            # Gradient norm, loss, no outputs
            O.gradient_norms = outputs['gradient_norms']
            O.losses = outputs['losses']
        else:
            # No gradient loss, output_symbols, output_logits
            O.output_symbols = outputs['output_symbols']
            O.output_logits = outputs['output_logits']
            O.losses = outputs['losses']
        # [attention_masks]
        if self.tg_token_use_attention:
            O.attn_alignments = outputs['attn_alignments']

        O.encoder_hidden_states = outputs['encoder_hidden_states']
        O.decoder_hidden_states = outputs['decoder_hidden_states']

        if self.use_copy:
            O.pointers = outputs['pointers']

        return O


class Example(object):
    """
    Input data to the neural network (batched when mini-batch training is used).
    """
    def __init__(self):
        self.encoder_inputs = None
        self.encoder_attn_masks = None
        self.decoder_inputs = None
        self.target_weights = None
        self.pointer_targets = None


class Output(object):
    """
    Data output from the neural network (batched when mini-batch training is used).
    """
    def __init__(self):
        self.updates = None
        self.gradient_norms = None
        self.losses = None
        self.output_symbols = None
        self.output_logits = None
        self.attn_alignments = None
        self.encoder_hidden_states = None
        self.decoder_hidden_states = None
