#!/usr/bin/env python
from __future__ import print_function

import collections
import scipy.sparse as ss
import sys

head_arg_template = "{}:::{}"
tuple_template = "{}->{}"

class Example(object):

    def __init__(self, sent, cmd):
        self.sent = sent
        self.cmd = cmd
        self.words = None
        self.terms = None
        self.features = None
        self.feature_vector = None

    def get_words(self):
        if self.words == None:
            self.words = set(self.sent.split())
        return self.words

    def get_terms(self):
        if self.terms == None:
            self.terms = self.cmd.split()
            self.head_cmd = self.terms[0]
        return self.terms

    def feature_set0(self):
        features = collections.defaultdict(int)
        for term in self.get_terms():
            for word in self.get_words():
                # feature = tuple_template.format(
                #    head_arg_template.format(head_cmd, term), word)
                feature = tuple_template.format(term, word)
                features[feature] = 1
        return features

    def feature_set(self, pmis, feature_index):
        if self.features == None:
            features = collections.defaultdict(int)
            for term in self.get_terms():
                for word in self.get_words():
                    # feature = tuple_template.format(
                    #    head_arg_template.format(head_cmd, term), word)
                    feature = tuple_template.format(term, word)
                    if not feature in feature_index:
                        continue
                    pmi = pmis[term][word]
                    features[feature] = pmi
            self.features = features
        return self.features

    def feature_vector(self, feature_index):
        if self.feature_vector == None:
            feature_vector = ss.lil_matrix((1, len(feature_index)))
            for feature in self.feature_set():
                if feature in feature_index:
                    ind = feature_index[feature]
                    feature_vector[0, ind] = 1
            self.feature_vector = feature_vector.tocsr()
        return self.feature_vector

def read_train_examples(questionFile, commandFile):
    with open(questionFile) as f:
        questions = f.readlines()
    with open(commandFile) as f:
        commands = f.readlines()

    assert(len(questions) == len(commands))

    dataset = []
    for i in xrange(len(questions)):
        if "perl" in questions[i]:
            continue
        if questions[i].startswith("ca n't"):
            continue
        if len(questions[i].split()) < 4:
            continue
        if len(commands[i].split()) < 4:
            continue
        if len(commands[i]) > 50:
            continue
        if not commands[i].strip().split()[0] in ["find", "mv", "sort", "grep", "cp", "ls", "tar"]:
            continue
        example = Example(questions[i].strip(), commands[i].strip())
        dataset.append(example)

    print("{} training examples".format(len(dataset)), file=sys.stderr)

    return dataset
