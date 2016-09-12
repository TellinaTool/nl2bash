#!/bin/sh

SPLIT=$1

python translate.py --data_dir ../data/reader/seq2tree.by.${SPLIT}/ --train_dir ../model/seq2tree.by.${SPLIT}/ --use_attention --nl_vocab_size 1500 --cm_vocab_size 1500 --gpu 2 --eval > eval.by.${SPLIT}
