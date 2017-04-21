"""Sequence-to-tree model with an attention mechanism."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from encoder_decoder import encoder
from encoder_decoder.framework import EncoderDecoderModel
from . import tree_decoder

class Seq2TreeModel(EncoderDecoderModel):
    """Sequence-to-tree models.
    """
    def __init__(self, hyperparams, buckets=None, forward_only=False):
        """
        Create the model.
        :param hyperparams: learning hyperparameters
        :param buckets: if not None, train bucket model.
        :param forward_only: if set, we do not construct the backward pass.
        """
        super(Seq2TreeModel, self).__init__(hyperparams, buckets, forward_only)


    def define_encoder(self):
        """Construct sequence encoders."""
        if self.encoder_topology == "rnn":
            self.encoder = encoder.RNNEncoder(self.hyperparams)
        elif self.encoder_topology == "birnn":
            self.encoder = encoder.BiRNNEncoder(self.hyperparams)
        else:
            raise ValueError("Unrecognized encoder type.")


    def define_decoder(self, dim):
        """Construct tree decoders."""
        if self.decoder_topology == "basic_tree":
            self.decoder = tree_decoder.BasicTreeDecoder(
                self.hyperparams, dim, self.output_project())
        else:
            raise ValueError("Unrecognized decoder topology: {}."
                             .format(self.decoder_topology))
