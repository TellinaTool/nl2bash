#!/bin/sh

CURRENT_DIR=`pwd`

DATADIR=${CURRENT_DIR}/$1
SOURCE=$2
TARGET=$3
OUTPUTDIR=${CURRENT_DIR}/$4

MOSEDIR=${CURRENT_DIR}/mosesdecoder
MOSETOOLS=${MOSEDIR}/tools

# clean corpora
${MOSEDIR}/scripts/training/clean-corpus-n.perl ${DATADIR}/"temp" ${SOURCE} ${TARGET} ${DATADIR}/"clean" 1 80

# train language model
LMDIR=${DATADIR}"/lm/"
mkdir ${LMDIR}

${MOSEDIR}/bin/lmplz -o 3 <${DATADIR}/${SOURCE} > ${LMDIR}/arpa.${SOURCE}
${MOSEDIR}/bin/build_binary ${LMDIR}/arpa.${SOURCE} ${LMDIR}/blm.${SOURCE}

${MOSEDIR}/bin/lmplz -o 3 --discount_fallback <${DATADIR}/unlabeled.${TARGET} > ${LMDIR}/arpa.${TARGET}
${MOSEDIR}/bin/build_binary ${LMDIR}/arpa.${TARGET} ${LMDIR}/blm.${TARGET}

# train translation model
nohup nice ${MOSEDIR}/scripts/training/train-model.perl -root-dir train \
    -corpus ${DATADIR}/clean -f nl -e cm \
    -alignment grow-diag-final-and -reordering msd-bidirectional-fe \
    -lm 0:3:${DATADIR}/lm/blm.cm:8 -external-bin-dir ${MOSETOOLS} \
    &>${OUTPUTDIR}/training.out
