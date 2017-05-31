#!/usr/bin/env python

import cPickle as pickle
import sys
sys.path.append("../../")
from misc.util import *
import numpy as np

def pmi(dataset):
    count_t = collections.defaultdict(int)
    count_w = collections.defaultdict(int)
    count_t_w = collections.defaultdict(dict)

    for example in dataset:
        for term in example.get_terms():
            count_t[term] += 1
        for word in example.get_words():
            count_w[word] += 1
        for term in example.get_terms():
            for word in example.get_words():
                if not word in count_t_w[term]:
                    count_t_w[term][word] = 1
                else:
                    count_t_w[term][word] += 1

    total_num_term = sum(count_t.values())
    total_num_word = sum(count_w.values())
    total_num_pair = sum([sum(count_t_w[t].values()) for t in count_t_w])

    pmis = collections.defaultdict(dict)

    for term in count_t_w:
        for word in count_t_w[term]:
            p_t = (count_t[term] + 0.0) / total_num_term
            p_w = (count_w[word] + 0.0) / total_num_word
            p_t_w = (count_t_w[term][word] + 0.0) / total_num_pair
            pmi = np.log(p_t_w / p_t / p_w)
            if pmi < 1e-5:
                pmi = 1e-5
            if pmi > 3.0:
                pmi = 3.0
            pmis[term][word] = pmi
            print(term, word, pmis[term][word])

    with open("../model/pmi.cpkl", 'wb') as o_f:
        pickle.dump(pmis, o_f)

if __name__ == "__main__":
    questionFile = "../../data/train/true.questions"
    commandFile = "../../data/train/true.commands"

    dataset = read_train_examples(questionFile, commandFile)

    pmi(dataset)