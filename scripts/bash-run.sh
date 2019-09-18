#!/bin/bash

ARGS=${@:1}

python3 -m encoder_decoder.translate \
    --rnn_cell gru \
    --encoder_topology birnn \
    --num_epochs 100 \
    --num_samples 256 \
    --variational_recurrent_dropout \
    --token_decoding_algorithm beam_search \
    --beam_size 100 \
    --alpha 1.0 \
    --num_nn_slot_filling 10 \
    ${ARGS}
