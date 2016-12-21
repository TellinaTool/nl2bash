#!/bin/sh

# script to reproduce seq2seq with attention model on the bash dataset

ARGS=${@:1}

./train.sh --batch_size 16 --encoder_input_keep 0.5 --decoder_input_keep 0.5 --encoder_output_keep 0.5 --decoder_output_keep 0.5 --dataset bash --attention_input_keep 0.5 --attention_output_keep 0.5 --decoding_algorithm beam_search --beam_size 100 --alpha 0.9 --encoder_topology birnn --dim 400 --num_epochs 40 --steps_per_epoch 4000 --num_layers 1  --beta 0 --create_fresh_params --normalized --use_attention ${ARGS}
