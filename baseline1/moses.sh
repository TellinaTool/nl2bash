#!/bin/sh

DATADIR=$1
SOURCE=$2
TARGET=$3
PREFIX=$4

MOSEDIR="/home/xilin/Toolkits/mosesdecoder"

# clean corpora
${MOSEDIR}/scripts/training/clean-corpus-n.perl ${DATADIR}/"true" ${SOURCE} ${TARGET} ${DATADIR}/"clean" 1 80

# language model
LMDIR=${DATADIR}"/lm/"

${MOSEDIR}/bin/lmplz -o 3 <${DATADIR}/true.${SOURCE} > ${LMDIR}/arpa.${SOURCE}
${MOSEDIR}/bin/build_binary ${LMDIR}/arpa.${SOURCE} ${LMDIR}/blm.${SOURCE}

${MOSEDIR}/bin/lmplz -o 3 <${DATADIR}/true.${TARGET} > ${LMDIR}/arpa.${TARGET}
${MOSEDIR}/bin/build_binary ${LMDIR}/arpa.${TARGET} ${LMDIR}/blm.${TARGET}