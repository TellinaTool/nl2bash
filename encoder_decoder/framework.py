"""Encoder-decoder model with attention mechanism."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import random
import numpy as np

import tensorflow as tf

from encoder_decoder import data_utils, graph_utils


class EncoderDecoderModel(graph_utils.NNModel):

    def __init__(self, hyperparams, buckets=None, forward_only=False):
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
          forward_only: if set, we do not construct the backward pass in the model.
          use_attention: if set, use attention model.
        """
        super(EncoderDecoderModel, self).__init__(hyperparams, buckets)
        self.learning_rate = tf.Variable(float(hyperparams["learning_rate"]),
                                         trainable=False)
        self.learning_rate_decay_op = self.learning_rate.assign(
            self.learning_rate * hyperparams["learning_rate_decay_factor"])

        # variable sharing
        self.output_projection_vars = False

        self.global_epoch = tf.Variable(0, trainable=False)

        # Encoder.
        self.define_encoder()

        # Decoder.
        self.define_decoder(self.encoder.output_dim)

        self.define_graph(forward_only)


    def define_graph(self, forward_only):
        # Feeds for inputs.
        self.encoder_inputs = []        # encoder inputs.
        self.encoder_attn_masks = []    # mask out PAD symbols in the encoder
        self.decoder_inputs = []        # decoder inputs (always start with "root").
        self.target_weights = []        # weights at each position of the target sequence.
        self.debug_vars = []

        print('beam_size: {}'.format(self.beam_size))
        print('batch_size: {}'.format(self.batch_size))
        for i in xrange(self.max_source_length):
            self.encoder_inputs.append(
                tf.placeholder(tf.int32, shape=[None],
                               name="encoder{0}".format(i)))
            self.encoder_attn_masks.append(
                tf.placeholder(tf.float32, shape=[None],
                               name="attn_alignment{0}".format(i)))
        for i in xrange(self.max_target_length + 1):
            self.decoder_inputs.append(
                tf.placeholder(tf.int32, shape=[None],
                               name="decoder{0}".format(i)))
            self.target_weights.append(
                tf.placeholder(tf.float32, shape=[None],
                               name="weight{0}".format(i)))
        # Our targets are decoder inputs shifted by one.
        self.targets = [self.decoder_inputs[i + 1]
                        for i in xrange(self.max_target_length)]

        if self.use_copy:
            self.original_encoder_inputs = []   # original encoder inputs.
                                                # used for accurate detection of copy action.
            self.original_decoder_inputs = []   # original decoder inputs.
                                                # used for accurate detection of copy action.
            self.copy_masks = []                # copy masks.
                                                # mark position in the inputs that are copyable.
            for i in xrange(self.max_source_length):
                self.original_encoder_inputs.append(
                    tf.placeholder(tf.int32, shape=[None],
                                   name="original_encoder{0}".format(i)))
                self.copy_masks.append(
                    tf.placeholder(tf.int32, shape=[None],
                                   name="copy_mask{0}".format(i)))
            for i in xrange(self.max_target_length):
                self.original_decoder_inputs.append(
                    tf.placeholder(tf.int32, shape=[None],
                                   name="original_decoder{0}".format(i)))

        # Compute training outputs and losses in the forward direction.
        if self.buckets:
            self.output_symbols = []
            self.output_logits = []
            self.losses = []
            self.attn_alignments = []
            for bucket_id, bucket in enumerate(self.buckets):
                print("creating bucket {} ({}, {})...".format(
                        bucket_id, bucket[0], bucket[1]))
                if bucket_id > 0:
                    tf.get_variable_scope().reuse_variables()
                encode_decode_outputs = \
                    self.encode_decode(
                        self.encoder_inputs[:bucket[0]],
                        self.encoder_attn_masks[:bucket[0]],
                        self.decoder_inputs[:bucket[1]],
                        self.targets[:bucket[1]],
                        self.target_weights[:bucket[1]],
                        forward_only=forward_only
                    )
                bucket_output_symbols, bucket_output_logits, bucket_losses, \
                    batch_encoder_input_mask = encode_decode_outputs
                self.output_symbols.append(bucket_output_symbols)
                self.output_logits.append(bucket_output_logits)
                self.losses.append(bucket_losses)
                self.attn_alignments.append(batch_encoder_input_mask)
        else:
            encode_decode_outputs = self.encode_decode(
                                        self.encoder_inputs,
                                        self.encoder_attn_masks,
                                        self.decoder_inputs,
                                        self.targets,
                                        self.target_weights,
                                        forward_only=forward_only
                                    )
            self.output_symbols, self.output_logits, self.losses, \
                self.attn_alignment = encode_decode_outputs

        # Gradients and SGD updates in the backward direction.
        if not forward_only:
            params = tf.trainable_variables()
            if self.optimizer == "sgd":
                opt = tf.train.GradientDescentOptimizer(self.learning_rate)
            elif self.optimizer == "adam":
                opt = tf.train.AdamOptimizer(self.learning_rate, beta1=0.9,
                                             beta2=0.999, epsilon=1e-08)
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


    def encode_decode(self, encoder_inputs, encoder_attn_masks,
                      decoder_inputs, targets, target_weights, forward_only):

        encoder_outputs, encoder_state = \
            self.encoder.define_graph(encoder_inputs)
        if self.use_attention:
            top_states = [tf.reshape(e, [-1, 1, self.encoder.output_dim])
                          for e in encoder_outputs]
            attention_states = tf.concat(1, top_states)
        else:
            attention_states = None
        
        # Losses.
        if self.training_algorithm == "bso":
            output_symbols, output_logits, outputs, state, attn_alignment, \
                bso_losses = self.decoder.define_bso_graph(
                    encoder_state, decoder_inputs, encoder_attn_masks,
                    attention_states, num_heads=1, forward_only=forward_only)
        else:
            output_symbols, output_logits, outputs, state, \
                attn_alignment = self.decoder.define_graph(
                    encoder_state, decoder_inputs, encoder_attn_masks,
                    attention_states, num_heads=1, forward_only=forward_only)

        if forward_only:
            # if self.decoding_algorithm == 'beam_search':
            #     outputs = [tf.gather(output, tf.range(0,
            #         self.batch_size*self.beam_size, self.beam_size))
            #         for output in outputs]
            encoder_decoder_loss = graph_utils.sequence_loss(
                                       outputs, targets, target_weights,
                                       graph_utils.softmax_loss(
                                           self.output_projection(),
                                           self.num_samples,
                                           self.target_vocab_size
                                   ))
        else:
            if self.training_algorithm == "standard":
                encoder_decoder_loss = graph_utils.sequence_loss(
                                           outputs, targets, target_weights,
                                           graph_utils.softmax_loss(
                                               self.output_projection(),
                                               self.num_samples,
                                               self.target_vocab_size
                                       ))
            elif self.training_algorithm == "bso":
                encoder_decoder_loss = tf.reduce_mean(
                    [tf.mul(x, y) for x, y in zip(bso_losses, target_weights)]
                )
            else:
                raise AttributeError("Unrecognized training algorithm.")

        attention_loss = self.beta * graph_utils.attention_reg(attn_alignment) \
            if self.use_attention else 0

        losses = encoder_decoder_loss + attention_loss

        # store encoder/decoder output states
        self.encoder_outputs = tf.concat(1, [tf.reshape(e_o, [-1, 1, self.encoder.output_dim])
                                             for e_o in encoder_outputs])
        self.decoder_outputs = tf.concat(1, [tf.reshape(d_o, [-1, 1, self.decoder.dim])
                                             for d_o in outputs])

        return output_symbols, output_logits, losses, attn_alignment


    def define_encoder(self):
        """Placeholder function."""
        self.encoder = None


    def define_decoder(self, dim):
        """Placeholder function."""
        self.decoder = None


    def output_projection(self):
        with tf.variable_scope("output_projection",
                               reuse=self.output_projection_vars):
            w = tf.get_variable("proj_w", [self.encoder.output_dim,
                                           self.target_vocab_size])
            b = tf.get_variable("proj_b", [self.target_vocab_size])
            self.output_projection_vars = True
        return (w, b)


    def format_example(self, encoder_channel_inputs, decoder_inputs,
                       copy_data=None, bucket_id=-1):
        """
        Prepare the data to be fed into the neural model.

        :param encoder_channel_inputs: dictionary of (batch of) sequence
            indices for different encoder channels [[...], [...], ...]
        :param decoder_inputs: batch of output sequence indices
            [[...], [...], ...]
        :param copy_data: set to true if using a copying network
        :param bucket_id: bucket id of the current batch

        Returns:
            batch_encoder_channel_inputs: list of input indices
            (batched, padded and reversed) for different encoder channels
            batch_encoder_input_masks: encoder input masks
            (mask out padding symbols, batched)
            batch_decoder_inputs: decoder input indices
            (batched, padded)
            batch_decoder_input_masks: decoder input masks
            (mask out padding symbols, batched)
        """
        def load_encoder_channel(inputs, input_size):
            # Encoder inputs are padded and then reversed
            padded_inputs = []
            batch_inputs = []
            for batch_idx in xrange(batch_size):
                input = inputs[batch_idx]
                paddings = [data_utils.PAD_ID] * (input_size - len(input))
                padded_inputs.append(list(reversed(input + paddings)))
            for length_idx in xrange(input_size):
                batch_inputs.append(
                    np.array([padded_inputs[batch_idx][length_idx]
                          for batch_idx in xrange(batch_size)], dtype=np.int32))
            return batch_inputs

        if bucket_id >= 0:
            encoder_size, decoder_size = self.buckets[bucket_id]
        else:
            encoder_size, decoder_size = \
                self.max_source_length, self.max_target_length

        batch_size = len(encoder_channel_inputs)

        padded_decoder_inputs = []
        for batch_idx in xrange(batch_size):
            decoder_input = decoder_inputs[batch_idx]
            decoder_pad = [data_utils.PAD_ID] * \
                          (decoder_size - len(decoder_input))
            padded_decoder_inputs.append(decoder_input + decoder_pad)

        # create batch-major vectors
        batch_encoder_channel_inputs = load_encoder_channel(
            encoder_channel_inputs, encoder_size)
        batch_encoder_input_masks = []
        batch_decoder_inputs = []
        batch_decoder_input_masks = []

        # Batch encoder inputs are just re-indexed encoder_inputs.
        for length_idx in xrange(encoder_size):
            batch_encoder_input_mask = np.ones(batch_size, dtype=np.float32)
            for batch_idx in xrange(batch_size):
                source = batch_encoder_channel_inputs[0][length_idx][batch_idx]
                if source == data_utils.PAD_ID:
                    batch_encoder_input_mask[batch_idx] = 0.0
            batch_encoder_input_masks.append(batch_encoder_input_mask)
            if self.use_copy:
                raise NotImplementedError

        # Batch decoder inputs are re-indexed decoder_inputs.
        for length_idx in xrange(decoder_size):
            batch_decoder_inputs.append(
                np.array([padded_decoder_inputs[batch_idx][length_idx]
                          for batch_idx in xrange(batch_size)], dtype=np.int32))
            if self.use_copy:
                raise NotImplementedError

            # Create target_weights to be 0 for targets that are padding.
            batch_decoder_input_mask = np.ones(batch_size, dtype=np.float32)
            for batch_idx in xrange(batch_size):
                # We set weight to 0 if the corresponding target is a PAD symbol.
                # The corresponding target is decoder_input shifted by 1 forward.
                if length_idx < decoder_size - 1:
                    target = padded_decoder_inputs[batch_idx][length_idx + 1]
                if length_idx == decoder_size - 1 or target == data_utils.PAD_ID:
                    batch_decoder_input_mask[batch_idx] = 0.0
            batch_decoder_input_masks.append(batch_decoder_input_mask)
        
        if self.use_copy:
            raise NotImplementedError
        else:
            return batch_encoder_channel_inputs, batch_encoder_input_masks,\
                   batch_decoder_inputs, batch_decoder_input_masks


    def get_batch(self, data, bucket_id, copy_data=None):
        """Get a random batch of data from the specified bucket, prepare for step.

        To feed data in step(..) it must be a list of batch-major vectors, while
        data here contains single length-major cases. So the main logic of this
        function is to re-index data cases to be in the proper format for feeding.

        Args:
          data: a tuple of size len(self.buckets) in which each element contains
            lists of pairs of input and output data that we use to create a batch.
          bucket_id: integer, which bucket to get the batch for.
          add_extra_go: if set to True, add an extra "GO" symbol to decoder inputs.
        Returns:
          The triple (encoder_inputs, decoder_inputs, target_weights) for
          the constructed batch that has the proper format to call step(...) later.
        """
        encoder_inputs, decoder_inputs = [], []

        # Get a random batch of encoder and decoder inputs from data,
        # pad them if needed, reverse encoder inputs and add GO to decoder.
        for _ in xrange(self.batch_size):
            random_example = random.choice(data[bucket_id])
            encoder_input = random_example[2]
            decoder_input = random_example[3]
            encoder_inputs.append(encoder_input)
            decoder_inputs.append(decoder_input)

        return self.format_example(encoder_inputs, decoder_inputs,
                                   copy_data=copy_data, bucket_id=bucket_id)


    def get_bucket(self, data, bucket_id, copy_data=None):
        """Get all data points from the specified bucket, prepare for step.
        """
        encoder_inputs, decoder_inputs = [], []

        for i in xrange(len(data[bucket_id])):
            encoder_input = data[bucket_id][i][2]
            decoder_input = data[bucket_id][i][3]
            encoder_inputs.append(encoder_input)
            decoder_inputs.append(decoder_input)

        return self.format_example(encoder_inputs, decoder_inputs,
                                   copy_data=copy_data, bucket_id=bucket_id)


    def step(self, session, formatted_example, bucket_id=-1, forward_only=False,
             return_rnn_hidden_states=False):
        """Run a step of the model feeding the given inputs.
        :param session: tensorflow session to use.
        :param encoder_inputs: list of numpy int vectors to feed as encoder inputs.
        :param attn_alignments: list of numpy int vectors to feed as the mask over inputs
            about which tokens to attend to.
        :param decoder_inputs: list of numpy int vectors to feed as decoder inputs.
        :param target_weights: list of numpy float vectors to feed as target weights.
        :param bucket_id: which bucket of the model to use.
        :param forward_only: whether to do the backward step or only forward.
        :param return_rnn_hidden_states: if set to True, return the hidden states of the
            two RNNs.
        :return (gradient_norm, average_perplexity, outputs)
        """

        # Input feed: encoder inputs, decoder inputs, target_weights, as provided.
        input_feed = self.get_input_feed(formatted_example, bucket_id)

        # Output feed: depends on whether we do a backward step or not.
        if not forward_only:
            if bucket_id == -1:
                output_feed = [self.updates,                    # Update Op that does SGD.
                               self.gradient_norms,             # Gradient norm.
                               self.losses]                     # Loss for this batch.
            else:
                output_feed = [self.updates[bucket_id],         # Update Op that does SGD.
                               self.gradient_norms[bucket_id],  # Gradient norm.
                               self.losses[bucket_id]]          # Loss for this batch.
        else:
            if bucket_id == -1:
                output_feed = [self.output_symbols]             # Loss for this batch.
                output_feed.append(self.output_logits)          # Batch output sequence
                output_feed.append(self.losses)                 # Batch output scores
            else:
                output_feed = [self.output_symbols[bucket_id]]      # Loss for this batch.
                output_feed.append(self.output_logits[bucket_id])   # Batch output sequence
                output_feed.append(self.losses[bucket_id])          # Batch output logits

        if self.use_attention:
            if bucket_id == -1:
                output_feed.append(self.attn_alignments)
            else:
                output_feed.append(self.attn_alignments[bucket_id])

        if return_rnn_hidden_states:
            output_feed.append(self.encoder_outputs)
            output_feed.append(self.decoder_outputs)

        outputs = session.run(output_feed, input_feed)

        outputs_to_return = []
        if not forward_only:
            # Gradient norm, loss, no outputs
            outputs_to_return.append(outputs[1])
            outputs_to_return.append(outputs[2])
            outputs_to_return.append(None)
        else:
            # No gradient loss, output_symbols, output_logits
            outputs_to_return.append(outputs[0])
            outputs_to_return.append(outputs[1])
            outputs_to_return.append(outputs[2])
        # [attention_masks]
        if self.use_attention:
            outputs_to_return.append(outputs[3])
        else:
            outputs_to_return.append(None)
        if return_rnn_hidden_states:
            outputs_to_return.append(outputs[4])
            outputs_to_return.append(outputs[5])

        return outputs_to_return


    def get_input_feed(self, formatted_example, bucket_id):
        # Unwarp data tensors
        if self.use_copy:
            encoder_inputs, attn_alignments, decoder_inputs, target_weights, \
            original_encoder_inputs, original_decoder_inputs, copy_masks = formatted_example
        else:
            encoder_inputs, attn_alignments, decoder_inputs, target_weights = formatted_example

        # Check if the sizes match.
        if bucket_id == -1:
            encoder_size, decoder_size = len(encoder_inputs), len(decoder_inputs)
            assert(encoder_size == self.max_source_length)
            assert(decoder_size == self.max_target_length)
        else:
            encoder_size, decoder_size = self.buckets[bucket_id]
            if len(encoder_inputs) != encoder_size:
                raise ValueError("Encoder length must be equal to the one in bucket,"
                                 " %d != %d." % (len(encoder_inputs), encoder_size))
            if len(decoder_inputs) != decoder_size:
                raise ValueError("Decoder length must be equal to the one in bucket,"
                                 " %d != %d." % (len(decoder_inputs), decoder_size))
            if len(target_weights) != decoder_size:
                raise ValueError("Weights length must be equal to the one in bucket,"
                                 " %d != %d." % (len(target_weights), decoder_size))

        input_feed = {}
        for l in xrange(encoder_size):
            input_feed[self.encoder_inputs[l].name] = encoder_inputs[l]
            input_feed[self.encoder_attn_masks[l].name] = attn_alignments[l]
        for l in xrange(decoder_size):
            input_feed[self.decoder_inputs[l].name] = decoder_inputs[l]
            input_feed[self.target_weights[l].name] = target_weights[l]
        if self.use_copy:
            for l in xrange(encoder_size):
                input_feed[self.original_encoder_inputs[l].name] = \
                    original_encoder_inputs[l]
                input_feed[self.copy_masks[l].name] = copy_masks[l]
            for l in xrange(decoder_size):
                input_feed[self.original_decoder_inputs[l].name] = \
                    original_decoder_inputs[l]

        # Since our targets are decoder inputs shifted by one, we need one more.
        last_target = self.decoder_inputs[decoder_size].name
        input_feed[last_target] = np.zeros(decoder_inputs[0].shape, dtype=np.int32)

        return input_feed