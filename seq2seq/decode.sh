#!/bin/sh

python translate.py --data_dir ../data/reader/seq2tree.by.command/ --train_dir ../model/seq2seq/lstm-attention-4/ --decode --nl_vocab_size 1500 --cm_vocab_size 1500
