#!/bin/sh

DATADIR=$1
MODELDIR=$2
ARGS=${@:3}

python translate.py --eval --data_dir ${DATADIR} --train_dir ${MODELDIR} ${ARGS}
