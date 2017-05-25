#!/bin/sh

CURRENT_DIR=`pwd`

DATADIR=${CURRENT_DIR}/$1
SOURCE=$2
TARGET=$3
MODELDIR=${CURRENT_DIR}/$4

MOSEDIR=${CURRENT_DIR}/mosesdecoder
MOSETOOLS=${MOSEDIR}/tools

nohup nice ${MOSEDIR}/bin/moses \
    -f ${MODELDIR}/mert-work/moses.ini \
    < ${DATADIR}/test.${SOURCE} > ${DATADIR}/test.predict \
    -threads all 2> /tmp/moses.err
