"""
Beam decoder with length normalization
Adapted from source
curl -LO 'https://gist.github.com/nikitakit/6ab61a73b86c50ad88d409bac3c3d09f'
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import tensorflow as tf
from tensorflow.python.util import nest

def nest_map(func, nested):
    if not nest.is_sequence(nested):
        return func(nested)
    flat = nest.flatten(nested)
    return nest.pack_sequence_as(nested, list(map(func, flat)))

class BeamDecoder(object):
    def __init__(self, num_classes, start_token=-1, stop_token=-1,
                 batch_size=1, beam_size=7, use_attention=False,
                 use_copy=False, alpha=1.0, locally_normalized=True):
        """
        :param num_classes: int. Number of output classes used
        :param start_token: int.
        :param stop_token: int.
        :param beam_size: int.
        :param use_attention: if attention is to be used.
        :param use_copy: if copy mechnism is to be used.
        :param alpha: parameter used for length normalization.
        :param locally_normalized: set to true if local normalization is to be
            performed at each search step.
        """
        self.num_classes = num_classes
        self.start_token = start_token
        self.stop_token = stop_token
        self.batch_size = batch_size
        self.beam_size = beam_size
        self.use_attention = use_attention
        self.use_copy = use_copy
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

        dynamic_tensor_shape = tf.unpack(tf.shape(tensor))
        res = tf.expand_dims(tensor, 1)
        res = tf.tile(res, [1, beam_size] + [1] * (tensor_shape.ndims-1))
        res = tf.reshape(res, [-1] + list(dynamic_tensor_shape[1:]))
        res.set_shape([new_first_dim] + list(tensor_shape[1:]))
        return res

    def wrap_cell(self, cell, token_output_projection):
        """
        Wraps a cell for use with the beam decoder
        """
        return BeamDecoderCellWrapper(cell, token_output_projection,
                                      self.num_classes, self.start_token,
                                      self.stop_token, self.batch_size,
                                      self.beam_size, self.use_attention,
                                      self.use_copy,
                                      self.alpha, self.locally_normalized)

    def wrap_state(self, state, token_output_projection):
        dummy = BeamDecoderCellWrapper(None, token_output_projection,
                                       self.num_classes, self.start_token,
                                       self.stop_token, self.batch_size,
                                       self.beam_size, self.use_attention,
                                       self.use_copy,
                                       self.alpha, self.locally_normalized)
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
            res = tf.concat(1, [res[:,1:],
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
            output_dense = tf.concat(1, [output_dense[:,1:],
                tf.ones_like(output_dense[:,0:1]) * self.stop_token])
            mask = tf.concat(1, [mask[:,1:],
                tf.cast(tf.ones_like(mask[:,0:1], dtype=tf.int8), tf.bool)])

        return sparse_boolean_mask(output_dense, mask)

    def unwrap_output_logprobs(self, final_state):
        """
        Retreive the log-probabilities associated with the selected beams.
        """
        return final_state[1]

class BeamDecoderCellWrapper(tf.nn.rnn_cell.RNNCell):
    def __init__(self, cell, token_output_projection, num_classes, start_token=-1,
                 stop_token=-1, batch_size=1, beam_size=7, use_attention=False,
                 use_copy=False, alpha=1.0, locally_normalized=True):
        self.cell = cell
        self.token_output_projection = token_output_projection
        self.num_classes = num_classes
        self.start_token = start_token
        self.stop_token = stop_token
        self.batch_size = batch_size
        self.beam_size = beam_size
        self.use_attention = use_attention
        self.use_copy = use_copy
        self.alpha = alpha
        self.locally_normalized = locally_normalized

        self.parent_refs_offsets = None

        # Note: masking out entries to -inf plays poorly with top_k, so just
        # subtract out a large number.
        # TODO: consider using slice+fill+concat instead of adding a mask
        # TODO: consider making the large negative constant dtype-dependent
        self._nondone_mask = tf.reshape(
            tf.cast(tf.equal(tf.range(self.num_classes), self.stop_token),
                    tf.float32) * -1e18,
            [1, 1, self.num_classes]
        )
        self._nondone_mask = tf.reshape(tf.tile(self._nondone_mask,
                                                [1, self.beam_size, 1]),
            [-1, self.beam_size*self.num_classes])

        full_size = self.batch_size * self.beam_size
        self.seq_len = tf.constant(1e-10, shape=[full_size], dtype=tf.float32)
        # [self.batch_size*self.beam_size, self.num_classes]
        # [- - _STOP - - - ]
        # [-100 -100 0 -100 -100 -100]
        # [-100 -100 0 -100 -100 -100]
        # [-100 -100 0 -100 -100 -100]
        # [-100 -100 0 -100 -100 -100]
        self._done_mask = tf.reshape(
            tf.cast(tf.not_equal(tf.range(self.num_classes), self.stop_token),
                    tf.float32) * -1e18,
            [1, self.num_classes]
        )
        self._done_mask = tf.tile(self._done_mask, [full_size, 1])


    def __call__(self, inputs, state, alignments=None, pointers=None,
                 scope=None):
        (
            past_cand_symbols,      # [batch_size, :]
            past_cand_logprobs,     # [batch_size]
            past_beam_symbols,      # [batch_size*self.beam_size, :], right-aligned!!!
            past_beam_logprobs,     # [batch_size*self.beam_size]
            past_cell_states,       # [batch_size*self.beam_size, :, dim]
        ) = state
        batch_size = past_cand_symbols.get_shape()[0].value
        full_size = batch_size * self.beam_size
        if self.parent_refs_offsets is None:
            self.parent_refs_offsets = \
                (tf.range(full_size) // self.beam_size) * self.beam_size

        input_symbols = past_beam_symbols[:, -1]
        # [batch_size * beam_size]
        # - 0
        # _STOP 1
        # - 0
        # - 0
        stop_mask = tf.cast(tf.equal(input_symbols, self.stop_token),
                            tf.float32)

        cell_inputs = inputs

        past_cell_state = self.get_past_cell_state(past_cell_states)
        if self.use_copy:
            cell_output, raw_cell_state, alignments, pointers = \
                self.cell(cell_inputs, past_cell_state, alignments,
                          pointers, scope)
        elif self.use_attention:
            cell_output, raw_cell_state, alignments = \
                self.cell(cell_inputs, past_cell_state, alignments, scope)
        else:
            cell_output, raw_cell_state = \
                self.cell(cell_inputs, past_cell_state, scope)
        W, b = self.token_output_projection

        # [batch_size*beam_size, num_classes]
        if self.locally_normalized:
            logprobs = tf.nn.log_softmax(tf.matmul(cell_output, W) + b)
        else:
            logprobs = tf.matmul(cell_output, W) + b
        # set the probabilities of all other symbols following the stop symbol
        # to a very small number
        stop_mask_2d = tf.expand_dims(stop_mask, 1)
        # [- - _STOP - - - ]
        # [0 0 0 0 0 0]
        # [-100 -100 0 -100 -100 -100]
        # [0 0 0 0 0 0]
        # [0 0 0 0 0 0]
        done_only_mask = tf.mul(stop_mask_2d, self._done_mask)
        # [- - _STOP - - - ]
        # [1 1 1 1 1 1]
        # [1 1 0 1 1 1]
        # [1 1 1 1 1 1]
        # [1 1 1 1 1 1]
        zero_done_mask = tf.ones([full_size, self.num_classes]) - \
                         tf.mul(stop_mask_2d,
                                tf.cast(tf.equal(self._done_mask, 0), tf.float32))
        logprobs = tf.add(logprobs, done_only_mask)
        logprobs = tf.mul(logprobs, zero_done_mask)

        # length normalization
        past_beam_acc_logprobs = tf.mul(past_beam_logprobs,
                                        tf.pow(self.seq_len, self.alpha))
        logprobs_batched = tf.expand_dims(past_beam_acc_logprobs, 1) + logprobs
        seq_len = tf.expand_dims(self.seq_len, 1) + \
                  tf.mul(tf.ones([full_size, 1]) - stop_mask_2d, 
                         tf.cast(tf.not_equal(self._done_mask, 0), tf.float32))
        logprobs_batched = tf.div(logprobs_batched, tf.pow(seq_len, self.alpha))
        logprobs_batched = tf.reshape(logprobs_batched,
                                      [-1, self.beam_size * self.num_classes])

        beam_logprobs, indices = tf.nn.top_k(
            #TODO: make sure it's reasonable to remove nondone mask
            tf.reshape(logprobs_batched,
                       [-1, self.beam_size * self.num_classes]),
            self.beam_size
        )
        beam_logprobs = tf.reshape(beam_logprobs, [-1])

        # For continuing to the next symbols
        symbols = indices % self.num_classes # [batch_size, self.beam_size]
        parent_refs = tf.reshape(indices // self.num_classes, [-1]) # [batch_size*self.beam_size]

        parent_refs = parent_refs + self.parent_refs_offsets

        symbols_history = tf.gather(past_beam_symbols, parent_refs)
        if alignments is not None:
            num_alignments = len(alignments)
            alignments = nest.flatten(alignments)
            alignments = tf.split(1, num_alignments * 2,
                                  tf.gather(tf.concat(1, alignments), 
                                            parent_refs))
            new_alignments = []
            for i in xrange(num_alignments):
                new_alignments.append([alignments[2*i], alignments[2*i+1]])
            alignments = new_alignments

        beam_symbols = tf.concat(1, [symbols_history,
                                     tf.reshape(symbols, [-1, 1])])
        self.seq_len = tf.gather(self.seq_len, parent_refs) + \
                       tf.cast(tf.not_equal(tf.reshape(symbols, [-1]),
                                            self.stop_token),
                               tf.float32)
        # if nest.is_sequence(raw_cell_state):
        #     raw_cell_states = (
        #         tf.concat(1, [past_cell_states[0], tf.expand_dims(raw_cell_state[0], 1)]),
        #         tf.concat(1, [past_cell_states[1], tf.expand_dims(raw_cell_state[1], 1)])
        #     )
        #     cell_states = (
        #         nest_map(lambda element: tf.gather(element, parent_refs), raw_cell_states[0]),
        #         nest_map(lambda element: tf.gather(element, parent_refs), raw_cell_states[1])
        #     )
        # TODO: this statement might choke if the cell state is a tuple
        cell_states = nest_map(
            lambda element: tf.gather(element, parent_refs),
            tf.concat(1, [past_cell_states, tf.expand_dims(raw_cell_state, 1)])
        )

        # Handling for getting a done token
        logprobs_done = tf.reshape(logprobs_batched,
            [-1, self.beam_size, self.num_classes])[:,:,self.stop_token]
        done_parent_refs = tf.to_int32(tf.argmax(logprobs_done, 1))
        done_parent_refs_offsets = tf.range(batch_size) * self.beam_size
        done_symbols = tf.gather(past_beam_symbols[:, -1:],
                                 done_parent_refs + done_parent_refs_offsets)

        logprobs_done_max = tf.reduce_max(logprobs_done, 1)
        cand_symbols = tf.select(logprobs_done_max > past_cand_logprobs,
                                done_symbols, past_cand_symbols)
        cand_logprobs = tf.maximum(logprobs_done_max, past_cand_logprobs)

        cell_state = (
                    cand_symbols,
                    cand_logprobs,
                    beam_symbols,
                    beam_logprobs,
                    cell_states,
                )
        if self.use_copy:
            return cell_output, cell_state, alignments, pointers
        elif self.use_attention:
            return cell_output, cell_state, alignments
        else:
            return cell_output, cell_state

    @property
    def output_size(self):
        return 1

    def get_past_cell_state(self, past_cell_states):
        if nest.is_sequence(past_cell_states):
            # LSTM
            cell_states, hidden_states = past_cell_states
            past_cell_state = cell_states[:, -1, :]
            past_hidden_state = hidden_states[:, -1, :]
            past_cell_state = (past_cell_state, past_hidden_state)
        else:
            past_cell_state = past_cell_states[:, -1, :]
        return past_cell_state

    def _create_state(self, batch_size, dtype, cell_state=None):
        cand_symbols = tf.fill([batch_size, 1],
                               tf.constant(self.start_token, dtype=tf.int32))
        cand_logprobs = tf.ones((batch_size,), dtype=tf.float32) * -float('inf')

        if cell_state is None:
            cell_state = self.cell.zero_state(batch_size*self.beam_size, dtype=dtype)
        else:
            cell_state = BeamDecoder._tile_along_beam(self.beam_size, cell_state)
        full_size = batch_size * self.beam_size
        first_in_beam_mask = tf.equal(tf.range(full_size) % self.beam_size, 0)

        beam_symbols = tf.fill([full_size, 1],
                               tf.constant(self.start_token, dtype=tf.int32))
        beam_logprobs = tf.select(
            first_in_beam_mask,
            tf.fill([full_size], 0.0),
            tf.fill([full_size], -1e18), # top_k does not play well with -inf
                                         # TODO: dtype-dependent value here
        )

        return (
            cand_symbols,
            cand_logprobs,
            beam_symbols,
            beam_logprobs,
            tf.expand_dims(cell_state, 1)
        )

    def zero_state(self, batch_size_times_beam_size, dtype):
        """
        Instead of calling this manually, please use
        BeamDecoder.wrap_state(cell.zero_state(...)) instead
        """
        batch_size = batch_size_times_beam_size / self.beam_size
        return self.cell.zero_state(batch_size, dtype)

def sparse_boolean_mask(tensor, mask):
    """
    Creates a sparse tensor from masked elements of `tensor`
    Inputs:
      tensor: a 2-D tensor, [batch_size, T]
      mask: a 2-D mask, [batch_size, T]
    Output: a 2-D sparse tensor
    """
    mask_lens = tf.reduce_sum(tf.cast(mask, tf.int32), -1, keep_dims=True)
    mask_shape = tf.shape(mask)
    left_shifted_mask = tf.tile(
        tf.expand_dims(tf.range(mask_shape[1]), 0),
        [mask_shape[0], 1]
    ) < mask_lens
    return tf.SparseTensor(
        indices=tf.where(left_shifted_mask),
        values=tf.boolean_mask(tensor, mask),
        shape=tf.cast(tf.pack([mask_shape[0], tf.reduce_max(mask_lens)]),
                      tf.int64) # For 2D only
    )
