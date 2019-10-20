"""
Beam decoder with length normalization
Adapted from
curl -LO 'https://gist.github.com/nikitakit/6ab61a73b86c50ad88d409bac3c3d09f'
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.python.util import nest

from encoder_decoder.graph_utils import nest_map


class BeamDecoder(object):
    def __init__(self, num_layers, start_token=-1, stop_token=-1, batch_size=1,
                 beam_size=7, use_attention=False, use_copy=False,
                 copy_fun='copynet', alpha=1.0, locally_normalized=True):
        """
        :param num_classes: int. Number of output classes used
        :param num_layers: int. Number of layers used in the RNN cell.
        :param start_token: int.
        :param stop_token: int.
        :param beam_size: int.
        :param use_attention: if attention is to be used.
        :param use_copy: if copy mechnism is to be used.
        :param alpha: parameter used for length normalization.
        :param locally_normalized: set to true if local normalization is to be
            performed at each search step.
        """
        self.num_layers = num_layers
        self.start_token = start_token
        self.stop_token = stop_token
        self.batch_size = batch_size
        self.beam_size = beam_size
        self.use_attention = use_attention
        self.use_copy = use_copy
        self.copy_fun = copy_fun
        self.alpha = alpha
        self.locally_normalized = locally_normalized
        print("creating beam search decoder: alpha = {}".format(self.alpha))

    @classmethod
    def _tile_along_beam(cls, beam_size, state):
        if nest.is_sequence(state):
            return nest_map(
                lambda val: cls._tile_along_beam(beam_size, val),
                state
            )

        if not isinstance(state, tf.Tensor):
            raise ValueError("State should be a sequence or tensor")

        tensor = state

        tensor_shape = tensor.get_shape().with_rank_at_least(1)

        try:
            new_first_dim = tensor_shape[0] * beam_size
        except:
            new_first_dim = None

        dynamic_tensor_shape = tf.unstack(tf.shape(input=tensor))
        res = tf.expand_dims(tensor, 1)
        res = tf.tile(res, [1, beam_size] + [1] * (tensor_shape.ndims-1))
        res = tf.reshape(res, [-1] + list(dynamic_tensor_shape[1:]))
        res.set_shape([new_first_dim] + list(tensor_shape[1:]))
        return res

    def wrap_cell(self, cell, output_project):
        """
        Wraps a cell for use with the beam decoder
        """
        return BeamDecoderCellWrapper(cell, output_project, self.num_layers,
                                      self.start_token, self.stop_token,
                                      self.batch_size, self.beam_size,
                                      self.use_attention, self.use_copy,
                                      self.copy_fun, self.alpha,
                                      self.locally_normalized)

    def wrap_state(self, state, output_project):
        dummy = BeamDecoderCellWrapper(None, output_project, self.num_layers,
                                       self.start_token, self.stop_token,
                                       self.batch_size, self.beam_size,
                                       self.use_attention, self.use_copy,
                                       self.copy_fun, self.alpha,
                                       self.locally_normalized)
        if nest.is_sequence(state):
            dtype = nest.flatten(state)[0].dtype
        else:
            dtype = state.dtype
        return dummy._create_state(self.batch_size, dtype, cell_state=state)

    def wrap_input(self, input):
        """
        Wraps an input for use with the beam decoder.
        Should be used for the initial input at timestep zero, as well as any
        side-channel inputs that are per-batch (e.g. attention targets)
        """
        return self._tile_along_beam(self.beam_size, input)

    def unwrap_output_dense(self, final_state, include_stop_tokens=True):
        """
        Retreive the beam search output from the final state.
        Returns a [batch_size, max_len]-sized Tensor.
        """
        res = final_state[0]
        if include_stop_tokens:
            res = tf.concat(axis=1, values=[res[:,1:],
                                tf.ones_like(res[:,0:1]) * self.stop_token])
        return res

    def unwrap_output_sparse(self, final_state, include_stop_tokens=True):
        """
        Retreive the beam search output from the final state.
        Returns a sparse tensor with underlying dimensions of
        [batch_size, max_len]
        """
        output_dense = final_state[0]
        mask = tf.not_equal(output_dense, self.stop_token)

        if include_stop_tokens:
            output_dense = tf.concat(axis=1, values=[output_dense[:,1:],
                tf.ones_like(output_dense[:,0:1]) * self.stop_token])
            mask = tf.concat(axis=1, values=[mask[:,1:],
                tf.cast(tf.ones_like(mask[:,0:1], dtype=tf.int8), tf.bool)])

        return sparse_boolean_mask(output_dense, mask)

    def unwrap_output_logprobs(self, final_state):
        """
        Retreive the log-probabilities associated with the selected beams.
        """
        return final_state[1]


class BeamDecoderCellWrapper(tf.compat.v1.nn.rnn_cell.RNNCell):
    def __init__(self, cell, output_project, num_layers,
                 start_token=-1, stop_token=-1, batch_size=1, beam_size=7,
                 use_attention=False, use_copy=False, copy_fun='copynet',
                 alpha=1.0, locally_normalized=True):
        self.cell = cell
        self.output_project = output_project
        self.num_layers = num_layers
        self.start_token = start_token
        self.stop_token = stop_token
        self.batch_size = batch_size
        self.beam_size = beam_size
        self.use_attention = use_attention
        self.use_copy = use_copy
        self.copy_fun = copy_fun
        self.alpha = alpha
        self.locally_normalized = locally_normalized

        self.full_size = self.batch_size * self.beam_size
        self.seq_len = tf.constant(1e-12, shape=[self.full_size], dtype=tf.float32)

    def __call__(self, cell_inputs, state, scope=None):
        (
            past_beam_symbols,      # [batch_size*self.beam_size, :], right-aligned!!!
            past_beam_logprobs,     # [batch_size*self.beam_size]
            past_cell_states        # LSTM: ([batch_size*self.beam_size, :, dim],
                                    #        [batch_size*self.beam_size, :, dim])
                                    # GRU: [batch_size*self.beam_size, :, dim]
        ) = state

        past_cell_state = self.get_last_cell_state(past_cell_states)
        if self.use_copy and self.copy_fun == 'copynet':
            cell_output, cell_state, alignments, attns = \
                self.cell(cell_inputs, past_cell_state, scope)
        elif self.use_attention:
            cell_output, cell_state, alignments, attns = \
                self.cell(cell_inputs, past_cell_state, scope)
        else:
            cell_output, cell_state = \
                self.cell(cell_inputs, past_cell_state, scope)

        # [batch_size*beam_size, num_classes]
        if self.use_copy and self.copy_fun == 'copynet':
            logprobs = tf.math.log(cell_output)
        else:
            W, b = self.output_project
            if self.locally_normalized:
                logprobs = tf.nn.log_softmax(tf.matmul(cell_output, W) + b)
            else:
                logprobs = tf.matmul(cell_output, W) + b
        num_classes = logprobs.get_shape()[1]

        # stop_mask: indicates partial sequences ending with a stop token
        # [batch_size * beam_size]
        # x     0
        # _STOP 1
        # x     0
        # x     0
        input_symbols = past_beam_symbols[:, -1]
        stop_mask = tf.expand_dims(tf.cast(
            tf.equal(input_symbols, self.stop_token), tf.float32), 1)

        # done_mask: indicates stop token in the output vocabulary
        # [1, num_classes]
        # [- - _STOP - - -]
        # [0 0 1 0 0 0]
        done_mask = tf.cast(tf.reshape(tf.equal(tf.range(num_classes),
                                                self.stop_token),
                                       [1, num_classes]),
                            tf.float32)
        # set the next token distribution of partial sequences ending with
        # a stop token to:
        # [- - _STOP - - -]
        # [-inf -inf 0 -inf -inf -inf]
        logprobs = tf.add(logprobs, tf.multiply(
            stop_mask, -1e18 * (tf.ones_like(done_mask) - done_mask)))
        logprobs = tf.multiply(logprobs, (1 - tf.multiply(stop_mask, done_mask)))

        # length normalization
        past_logprobs_unormalized = \
            tf.multiply(past_beam_logprobs, tf.pow(self.seq_len, self.alpha))
        logprobs_unormalized = \
            tf.expand_dims(past_logprobs_unormalized, 1) + logprobs
        seq_len = tf.expand_dims(self.seq_len, 1) + (1 - stop_mask)
        logprobs_batched = tf.compat.v1.div(logprobs_unormalized, tf.pow(seq_len, self.alpha))

        beam_logprobs, indices = tf.nn.top_k(
            tf.reshape(logprobs_batched, [-1, self.beam_size * num_classes]),
            self.beam_size
        )
        beam_logprobs = tf.reshape(beam_logprobs, [-1])

        # For continuing to the next symbols
        parent_refs_offsets = \
                (tf.range(self.full_size) // self.beam_size) * self.beam_size
        symbols = indices % num_classes # [batch_size, self.beam_size]
        parent_refs = tf.reshape(indices // num_classes, [-1]) # [batch_size*self.beam_size]
        parent_refs = parent_refs + parent_refs_offsets

        beam_symbols = tf.concat(axis=1, values=[tf.gather(past_beam_symbols, parent_refs),
                                                 tf.reshape(symbols, [-1, 1])])
        self.seq_len = tf.squeeze(tf.gather(seq_len, parent_refs), axis=[1])

        if self.use_attention:
            ranked_alignments = nest_map(
                lambda element: tf.gather(element, parent_refs), alignments)
            ranked_attns = nest_map(
                lambda element: tf.gather(element, parent_refs), attns)

        # update cell_states
        def concat_and_gather_tuple_states(pc_states, c_state):
            rc_states = (
                tf.concat(axis=1, values=[pc_states[0], tf.expand_dims(c_state[0], 1)]),
                tf.concat(axis=1, values=[pc_states[1], tf.expand_dims(c_state[1], 1)])
            )
            c_states = (
                nest_map(lambda element: tf.gather(element, parent_refs), rc_states[0]),
                nest_map(lambda element: tf.gather(element, parent_refs), rc_states[1])
            )
            return c_states

        if nest.is_sequence(cell_state):
            if self.num_layers > 1:
                ranked_cell_states = [concat_and_gather_tuple_states(pc_states, c_state)
                    for pc_states, c_state in zip(past_cell_states, cell_state)]
            else:
                ranked_cell_states = concat_and_gather_tuple_states(
                    past_cell_states, cell_state)
        else:
            ranked_cell_states = tf.gather(
                tf.concat(axis=1, values=[past_cell_states, tf.expand_dims(cell_state, 1)]),
                parent_refs)

        compound_cell_state = (
            beam_symbols,
            beam_logprobs,
            ranked_cell_states
        )
        ranked_cell_output = tf.gather(cell_output, parent_refs)

        if self.use_copy and self.copy_fun == 'copynet':
            return ranked_cell_output, compound_cell_state, ranked_alignments, \
                   ranked_attns
        elif self.use_attention:
            return ranked_cell_output, compound_cell_state, ranked_alignments, \
                   ranked_attns
        else:
            return ranked_cell_output, compound_cell_state

    def get_last_cell_state(self, past_cell_states):
        def get_last_tuple_state(pc_states):
            c_states, h_states = pc_states
            lc_state = c_states[:, -1, :]
            lh_state = h_states[:, -1, :]
            l_state = (lc_state, lh_state)
            return l_state

        if nest.is_sequence(past_cell_states):
            if self.num_layers > 1:
                last_cell_state = [get_last_tuple_state(l)
                                   for l in past_cell_states]
            else:
                last_cell_state = get_last_tuple_state(past_cell_states)
        else:
            last_cell_state = past_cell_states[:, -1, :]
        return last_cell_state

    def _create_state(self, batch_size, dtype, cell_state=None):
        if cell_state is None:
            cell_state = self.cell.zero_state(batch_size*self.beam_size, dtype=dtype)
        else:
            cell_state = BeamDecoder._tile_along_beam(self.beam_size, cell_state)
        full_size = batch_size * self.beam_size
        first_in_beam_mask = tf.equal(tf.range(full_size) % self.beam_size, 0)

        beam_symbols = tf.fill([full_size, 1],
                               tf.constant(self.start_token, dtype=tf.int32))
        beam_logprobs = tf.compat.v1.where(
            first_in_beam_mask,
            tf.fill([full_size], 0.0),
            tf.fill([full_size], -1e18), # top_k does not play well with -inf
                                         # TODO: dtype-dependent value here
        )

        return (
            beam_symbols,
            beam_logprobs,
            nest_map(lambda element: tf.expand_dims(element, 1), cell_state)
        )

    def zero_state(self, batch_size_times_beam_size, dtype):
        """
        Instead of calling this manually, please use
        BeamDecoder.wrap_state(cell.zero_state(...)) instead
        """
        batch_size = batch_size_times_beam_size / self.beam_size
        return self.cell.zero_state(batch_size, dtype)

    @property
    def output_size(self):
        return 1


def sparse_boolean_mask(tensor, mask):
    """
    Creates a sparse tensor from masked elements of `tensor`
    Inputs:
      tensor: a 2-D tensor, [batch_size, T]
      mask: a 2-D mask, [batch_size, T]
    Output: a 2-D sparse tensor
    """
    mask_lens = tf.reduce_sum(input_tensor=tf.cast(mask, tf.int32), axis=-1, keepdims=True)
    mask_shape = tf.shape(input=mask)
    left_shifted_mask = tf.tile(
        tf.expand_dims(tf.range(mask_shape[1]), 0),
        [mask_shape[0], 1]
    ) < mask_lens
    return tf.SparseTensor(
        indices=tf.compat.v1.where(left_shifted_mask),
        values=tf.boolean_mask(tensor=tensor, mask=mask),
        shape=tf.cast(tf.stack([mask_shape[0], tf.reduce_max(input_tensor=mask_lens)]),
                      tf.int64) # For 2D only
    )
