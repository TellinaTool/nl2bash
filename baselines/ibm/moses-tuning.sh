#!/bin/sh

CURRENT_DIR=`pwd`

DATADIR=${CURRENT_DIR}/$1
SOURCE=$2
TARGET=$3
MODELDIR=${CURRENT_DIR}/$4

MOSESDIR=${CURRENT_DIR}/mosesdecoder
MOSESTOOLS=${MOSEDIR}/tools

nohup nice ${MOSESDIR}/scripts/training/mert-moses.pl  \
    ${DATADIR}/dev.${SOURCE} ${DATADIR}/dev.${TARGET} ${MOSESDIR}/bin/moses \
    ${MODELDIR}/model/moses.ini -mertdir ${MOSESDIR}/bin --rootdir ${MOSESDIR}/scripts \
    --batch-mira --return-best-dev --batch-mira-args '-J 300' \
    --decoder-flags '-threads 8 -v 0' &> mert.out &
