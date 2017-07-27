#!/bin/sh

# Set up path to CUDA library
source ~/.profile

export PYTHONPATH=`pwd`'/..'

ARGS=${@:1}

python3 -m encoder_decoder.translate \
    --nl_known_vocab_size 1030 \
    --cm_known_vocab_size 430 \
    --nl_vocab_size 5000 \
    --cm_vocab_size 5000 \
    --encoder_topology birnn \
    --batch_size 128 \
    --num_epochs 100 \
    --num_samples 256 \
    --variational_recurrent_dropout \
    --token_decoding_algorithm beam_search \
    --beam_size 100 \
    --alpha 1.0 \
    --num_nn_slot_filling 10 \
    ${ARGS}
