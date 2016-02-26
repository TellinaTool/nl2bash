#!/bin/sh

INPUTDIR=$1
SOURCE=$2
TARGET=$3
PREFIX=$4
OUTPUTDIR=$5

./plain2snt.out ${INPUTDIR}${SOURCE} ${INPUTDIR}${TARGET}

MKCLSV2DIR="/home/xilin/Toolkits/giza-pp/mkcls-v2"
cd ${MKCLSV2DIR}

./mkcls -p${INPUTDIR}${SOURCE} -V${INPUTDIR}${SOURCE}.vcb.classes
./mkcls -p${INPUTDIR}${TARGET} -V${INPUTDIR}${TARGET}.vcb.classes


GIZAPPDIR="/home/xilin/Toolkits/giza-pp/GIZA++-v2"
cd ${GIZAPPDIR}

# generate concurrence file
./snt2cooc.out ${INPUTDIR}${SOURCE}.vcb ${INPUTDIR}${TARGET}.vcb ${INPUTDIR}${SOURCE}_${TARGET}.snt > ${INPUTDIR}${SOURCE}_${TARGET}.cooc
./GIZA++ -S ${INPUTDIR}${SOURCE}.vcb -T ${INPUTDIR}${TARGET}.vcb -C ${INPUTDIR}${SOURCE}_${TARGET}.snt -o ${SOURCE}_${TARGET} -outputpath ${OUTPUTDIR} -CoocurrenceFile ${INPUTDIR}${SOURCE}_${TARGET}.cooc
./snt2cooc.out ${INPUTDIR}${TARGET}.vcb ${INPUTDIR}${SOURCE}.vcb ${INPUTDIR}${TARGET}_${SOURCE}.snt > ${INPUTDIR}${TARGET}_${SOURCE}.cooc
./GIZA++ -S ${INPUTDIR}${TARGET}.vcb -T ${INPUTDIR}${SOURCE}.vcb -C ${INPUTDIR}${TARGET}_${SOURCE}.snt -o ${TARGET}_${SOURCE} -outputpath ${OUTPUTDIR} -CoocurrenceFile ${INPUTDIR}${TARGET}_${SOURCE}.cooc
