#!/bin/sh

# script to reproduce seq2seq with attention model on the bash dataset

ARGS=${@:1}

./train.sh --batch_size 16 --encoder_input_keep 0.6 --decoder_input_keep 0.6 --encoder_output_keep 1.0 --decoder_output_keep 0.6 --dataset bash --attention_input_keep 0.6 --attention_output_keep 0.6 --decoding_algorithm beam_search --beam_size 10 --alpha 1.0 --dim 200 --num_epochs 20 --steps_per_epoch 400 --num_layers 1  --beta 0 --learning_rate 0.001 --gpu 0 --create_fresh_params --normalized --use_attention
