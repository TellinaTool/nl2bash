#!/bin/sh

# Set up path to CUDA library
source ~/.profile

export PYTHONPATH=`pwd`'/..'

ARGS=${@:1}

python3 -m encoder_decoder.translate \
    --encoder_topology birnn \
    --num_epochs 100 \
    --num_samples 256 \
    --variational_recurrent_dropout \
    --token_decoding_algorithm beam_search \
    --beam_size 100 \
    --alpha 1.0 \
    --margin 1.0 \
    --num_nn_slot_filling 10 \
    ${ARGS}
