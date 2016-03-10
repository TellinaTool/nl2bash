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

    def Words(self):
        if self.words == None:
            self.words = set(self.sent.split())
        return self.words

    def Terms(self):
        if self.terms == None:
            self.terms = self.cmd.split()
            self.head_cmd = self.terms[0]
        return self.terms

    def featureSet(self):
        if self.features == None:
            features = collections.defaultdict(int)
            for term in self.Terms():
                for word in self.Words():
                    # feature = tuple_template.format(
                    #    head_arg_template.format(head_cmd, term), word)
                    feature = tuple_template.format(term, word)
                    features[feature] += 1
            self.features = features
        return self.features

    def featureVector(self, feature_index):
        if self.feature_vector == None:
            feature_vector = ss.lil_matrix((1, len(feature_index)))
            for feature in self.featureSet():
                if feature in feature_index:
                    ind = feature_index[feature]
                    feature_vector[0, ind] = 1
            self.feature_vector = feature_vector.tocsr()
        return self.feature_vector

def readTrainExamples(questionFile, commandFile):
    with open(questionFile) as f:
        questions = f.readlines()
    with open(commandFile) as f:
        commands = f.readlines()

    assert(len(questions) == len(commands))

    dataset = []
    for i in xrange(len(questions)):
        if not commands[i].strip().split()[0] in ["find", "mv", "sort", "grep", "cp", "ls", "tar"]:
            continue
        if len(questions[i].split()) < 3:
            continue
        if len(commands[i]) > 50:
            continue
        example = Example(questions[i].strip(), commands[i].strip())
        dataset.append(example)

    print("{} training examples".format(len(dataset)), file=sys.stderr)

    return dataset