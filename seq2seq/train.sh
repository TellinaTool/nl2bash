#/bin/sh

DATADIR=$1
MODELDIR=$2

python translate.py --data_dir ${DATADIR} --train_dir ${MODELDIR}
