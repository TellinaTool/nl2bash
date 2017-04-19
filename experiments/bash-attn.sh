#!/bin/sh

# script to reproduce seq2seq with attention model on the bash dataset

ARGS=${@:1}

./run.sh --batch_size 32 --sc_input_keep 0.5 --sc_input_keep 0.5 --sc_output_keep 0.5 --sc_output_keep 0.5 --dataset bash --attention_input_keep 1.0 --attention_output_keep 1.0 --decoding_algorithm beam_search --beam_size 100 --alpha 1.0 --encoder_topology birnn --sc_token_dim 150 --num_epochs 40 --steps_per_epoch 4000 --learning_rate 0.0001 --create_fresh_params --normalized --tg_token_use_attention --tg_token_attn_fun non-linear --sc_token --num_nn_slot_filling 30 ${ARGS}
