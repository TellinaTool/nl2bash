#!/bin/bash

# reproduce experiments using seq2seq with attention model on the bash dataset

ARGS=${@:1}

./bash-run.sh \
    --dataset bash \
    --channel char \
    --batch_size 32 \
    --sc_token_dim 200 \
    --learning_rate 0.0001 \
    --steps_per_epoch 4000 \
    --tg_token_use_attention \
    --tg_token_attn_fun non-linear \
    --universal_keep 0.6 \
    --sc_input_keep 1.0 \
    --tg_input_keep 1.0 \
    --sc_output_keep 1.0 \
    --tg_output_keep 1.0 \
    --attention_input_keep 1.0 \
    --attention_output_keep 1.0 \
    --beta 0 \
    --create_fresh_params \
    ${ARGS}
