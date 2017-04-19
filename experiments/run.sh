#!/bin/sh

ARGS=${@:1}

python3 -m encoder_decoder.translate --sc_vocab_size 3074 --tg_vocab_size 3112 ${ARGS}
