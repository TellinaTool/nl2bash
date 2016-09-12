# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Sequence-to-sequence model with an attention mechanism."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
import numpy as np

import tensorflow as tf
import decoder

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "seq2tree"))
from encoder_decoder import EncoderDecoderModel
import encoder, graph_utils


class Seq2SeqModel(EncoderDecoderModel):
    """Sequence-to-sequence model with attention and for multiple buckets.

    This class implements a multi-layer recurrent neural network as encoder,
    and an attention-based decoder. This is the same as the model described in
    this paper: http://arxiv.org/abs/1412.7449 - please look there for details,
    or into the seq2seq library for complete model implementation.
    This class also allows to use GRU cells in addition to LSTM cells, and
    sampled softmax to handle large output vocabulary size. A single-layer
    version of this model, but with bi-directional encoder, was presented in
      http://arxiv.org/abs/1409.0473
    and sampled softmax is described in Section 3 of the following paper.
      http://arxiv.org/abs/1412.2007
    """

    def __init__(self, hyperparameters, buckets=None, forward_only=False):
        super(Seq2SeqModel, self).__init__(hyperparameters, buckets, forward_only)

        self.global_step = tf.Variable(0, trainable=False)

        self.define_graph(forward_only)


    def define_encoder(self):
        """Construct sequence encoders."""
        if self.encoder_topology == "rnn":
            self.encoder = encoder.RNNEncoder(self.dim, self.rnn_cell, self.num_layers)
        elif self.encoder_topology == "birnn":
            self.encoder = encoder.BiRNNEncoder(self.dim, self.rnn_cell, self.num_layers)
        else:
            raise ValueError("Unrecognized encoder type.")


    def define_decoder(self):
        """Construct sequence decoders."""
        if self.decoder_topology == "rnn":
            self.decoder = decoder.RNNDecoder(self.dim, self.batch_size, self.rnn_cell, self.num_layers,
                                              self.input_keep_prob, self.output_keep_prob,
                                              self.use_attention, self.use_copy,
                                              self.output_projection())
        else:
            raise ValueError("Unrecognized decoder type.")

