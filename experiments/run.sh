#!/bin/sh

ARGS=${@:1}

python3 -m encoder_decoder.translate --nl_vocab_size 1000 --cm_vocab_size 1000 ${ARGS}
