#!/bin/sh

# reproduce experiments using CopyNet on the bash dataset

ARGS=${@:1}

./bash-run.sh \
    --dataset bash \
    --sc_token_dim 150 \
    --learning_rate 0.0001 \
    --steps_per_epoch 4000 \
    --tg_token_use_attention \
    --tg_token_attn_fun non-linear \
    --universal_keep 0.6 \
    --sc_input_keep 0.5 \
    --tg_input_keep 0.5 \
    --sc_output_keep 0.5 \
    --tg_output_keep 0.5 \
    --attention_input_keep 1.0 \
    --attention_output_keep 1.0 \
    --beta 0 \
    --use_copy \
    --copy_fun copynet \
    --create_fresh_params \
    ${ARGS}
