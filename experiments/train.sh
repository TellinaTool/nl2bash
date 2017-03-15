#!/bin/sh

ARGS=${@:1}

python translate.py --nl_vocab_size 1000 --cm_vocab_size 1000 ${ARGS}
