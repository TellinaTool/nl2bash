#!/bin/sh

MOSEDIR="/home/xilin/Toolkits/mosesdecoder"

echo $1 | ${MOSEDIR}/bin/moses -f train/model/moses.ini 
