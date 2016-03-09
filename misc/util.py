#!/usr/bin/env python
from __future__ import print_function

import scipy.sparse as ss
import sys

tuple_template = "{}->{}"

class Example(object):

    def __init__(self, sent, cmd):
        self.sent = sent
        self.cmd = cmd
        self.features = None
        self.feature_vector = None

    def featureSet(self):
        if not self.features:
            self.features = set()
            words = self.sent.split()
            terms = self.cmd.split()
            for term in terms:
                for word in words:
                    feature = tuple_template.format(term, word)
                    self.features.add(feature)
        return self.features

    def featureVector(self, feature_index):
        if not self.feature_vector:
            self.feature_vector = ss.csr_matrix((1, len(feature_index)))
            for feature in self.featureSet():
                if feature in feature_index:
                    ind = feature_index[feature]
                    self.feature_vector[0, ind] = 1
        return self.feature_vector

def readTrainExamples(questionFile, commandFile):
    with open(questionFile) as f:
        questions = f.readlines()
    with open(commandFile) as f:
        commands = f.readlines()

    assert(len(questions) == len(commands))

    dataset = []
    for i in xrange(len(questions)):
        example = Example(questions[i].strip(), commands[i].strip())
        dataset.append(example)

    print("{} training examples".format(len(dataset)), file=sys.stderr)

    return dataset