#!/usr/bin/env python

from __future__ import print_function

import collections
import cPickle as pickle
import copy
import gzip
import os
import Queue
import random
from random import shuffle
import sys
sys.path.append("../..")
sys.path.append("../../misc")
import scipy.sparse as ss
import time

from grammar import *
from util import *

class Cell(object):

    def __init__(self, t, p, bp, w_c, ff, weights):
        """
        :member terms:          new term string consumed by this cell
        :member p:              pointer to parent cell in the syntax tree
        :member backpointer:    pointer to last cell sequentially
        :member isEOF:          if cell is terminable
        :member score:          score of the partial command parse
        :member covered_words:  natural language words covered by this cell
        :member feature_vector: features counts of the partial command parse up to this cell
        """
        self.term = t
        self.parent = p
        self.backpointer = bp
        self.length = bp.length + 1 if bp else 0
        self.feature_vector = ff + bp.feature_vector if bp else ff
        self.score = self.featureVector().dot(weights.T)[0, 0]
        self.covered_words = w_c

        # INEFFICIENT
        # self.cnl_words = copy.deepcopy(bp.cnl_words) if bp else set()
        # self.lnl_words = copy.deepcopy(bp.lnl_words) if bp else set(w_uc)
        # for w in w_c:
        #     self.cnl_words.add(w)
        # for w in w_c:
        #     if w in self.lnl_words:
        #         self.lnl_words.remove(w)

        # self.IS_HEAD = False
        self.IS_START = False

    # n-best search
    def __cmp__(self, other):
        return cmp(other.score + random.random() / 1e10, self.score)

    def isHead(self):
        if not self.backpointer:
            return False
        return self.backpointer.isStart()
        # return self.IS_HEAD

    # def setHead(self):
    #     self.IS_HEAD = True

    def isStart(self):
        return self.IS_START

    def setStart(self):
        self.IS_START = True

    def cmd_arg(self):
        return head_arg_template.format(self.parent.term, self.term)

    # natural language words covered by the partial command up to this cell
    def cnl_words(self):
        covered_words = copy.deepcopy(self.covered_words)
        bp = self.backpointer
        while (bp):
            covered_words |= bp.covered_words
            bp = bp.backpointer
        return covered_words

    def featureVector(self):
        return self.feature_vector

    def getCommand(self):
        if self.term == Enumerator.HOLE:
            command = ["*"]
        else:
            command = [self.term]
        bp = self.backpointer
        while (bp):
            if bp.term == Enumerator.HOLE:
                command.insert(0, "*")
            else:
                command.insert(0, bp.term)
            bp = bp.backpointer
        return ' '.join(command[1:])

class Parser(Enumerator):

    def __init__(self, grammar, min_cl=2, max_cl=10, beam_size=10):
        """
        :param grammar:
        :param min_cl: minimum number of tokens in command
        :param max_cl: maximum number of tokens in command
        :param beam_size: beam size of greedy search
        """
        Enumerator.__init__(self, grammar)
        self.min_command_length = min_cl
        self.max_command_length = max_cl
        self.beam_size = beam_size

        # hyperparameters
        self.__feature_freq_thresh__ = 3
        self.step_size = 0.1

        # params
        self.__feature_index__ = None
        self.__feature_freq__ = None
        self.__tuple_template__ = tuple_template
        self.__head_arg_template__ = head_arg_template

        self.redundant_word_score = 0.0
        self.ungrounded_token_score = -1e-5

    def make_phrase_table(self, inputFile):
        self.T2PScores = collections.defaultdict(dict)
        with gzip.open(inputFile, 'rb') as f:
            for line in f.readlines():
                parts = line.strip().split("|||")
                nl_phrase = parts[0].strip()
                cmd_snippet = parts[1].strip()
                phi_cmd_nl, lex_cmd_nl, phi_nl_cmd, lex_nl_cmd = \
                    [float(s) for s in parts[2].split()]
                self.T2PScores[cmd_snippet][nl_phrase] = lex_nl_cmd
                feature = self.__tuple_template__.format(cmd_snippet, nl_phrase)

    def create_feature_index(self, dataset):
        if not self.__feature_index__:
            self.__feature_index__ = {}
        if not self.__feature_freq__:
            self.__feature_freq__ = collections.defaultdict(int)
        for example in dataset:
            features = example.featureSet()
            for feature in features:
                self.__feature_freq__[feature] += 1

        for feature in self.__feature_freq__:
            if self.__feature_freq__[feature] < self.__feature_freq_thresh__:
                continue
            self.update_feature_index(feature)
        self.featureDim = len(self.__feature_index__)

        print("{} features in total".format(self.featureDim))

    def update_feature_index(self, feat):
        if not feat in self.__feature_index__:
            self.__feature_index__[feat] = len(self.__feature_index__)

    def local_score(self, cell, words):
        # TODO: consider more complex features
        features = ss.lil_matrix((1, self.featureDim))
        covered_words = set()

        for word in words:
            if cell.isStart():
                feature = self.__tuple_template__.format(cell.term, word)
            else:
                feature = self.__tuple_template__.format(cell.cmd_arg(), word)

            if feature in self.__feature_index__:
                ind = self.__feature_index__[feature]
                features[0, ind] += 1
                covered_words.add(word)
        return features.tocsr(), covered_words

    def final_score(self, cell, words):
        cell.score += self.redundant_word_score * len(set(words) - cell.cnl_words())

    def train(self, dataset, T, top_K):

        # Indexing features
        self.create_feature_index(dataset)

        # initialization
        self.weights = ss.lil_matrix((1, self.featureDim))
        for cmd_snippet in self.T2PScores:
            for nl_phrase in self.T2PScores[cmd_snippet]:
                feature = self.__tuple_template__.format(cmd_snippet, nl_phrase)
                if feature in self.__feature_index__:
                    ind = self.__feature_index__[feature]
                    self.weights[0, ind] = self.T2PScores[cmd_snippet][nl_phrase]
        self.weights = self.weights.tocsr()

        # Perceptron
        num_correct = 0

        start_time = time.time()
        for t in xrange(T):
            print("Iteration {}:".format(t))

            # shuffle dataset
            # shuffle(dataset)

            start_time_t = time.time()
            for i in xrange(len(dataset)):
                example = dataset[i]
                print("question.{}:\t{}".format(i, example.sent))

                top_K_parses = self.parse(example.sent, top_K, False)

                # Update
                if top_K_parses[0].getCommand() != example.cmd:
                    self.weights = self.weights + self.step_size * (example.featureVector(self.__feature_index__)
                                   - top_K_parses[0].featureVector())
                else:
                    num_correct += 1

                print("predict_parse:\t{} ({})".format(top_K_parses[0].getCommand(), top_K_parses[0].score))
                print("actual_parse:\t{}".format(example.cmd))
                print()

            end_time_t = time.time()
            print("training time = %ds" % (end_time_t - start_time_t))
            print("training accuracy = %f" % ((num_correct + 0.0) / len(dataset)))
        end_time = time.time()
        print("total training time = %ds" % (end_time - start_time))

        with open(os.path.join(os.path.dirname(__file__), "..", "model", "model.cpkl"), 'wb') as o_f:
            pickle.dump([self.weights,
                         self.__feature_index__,
                         self.__tuple_template__,
                         self.__head_arg_template__,
                         self.redundant_word_score,
                         self.ungrounded_token_score
                        ], o_f)

    def parse(self, sent, top_K=50, verbose=True):
        words = sent.split()
        word_set = set(words)

        start_cell = Cell("__START_SYMBOL__", None, None, set(),
                          ss.lil_matrix((1, self.featureDim)), self.weights)
        start_cell.setStart()
        final_cells = []                # store tail cells of all legal commands

        if verbose:
            print("Enumerating all commands up to length {}".format(
                self.max_command_length), file=sys.stderr)

        # DFS
        start_time = time.time()
        for term in self.legal_tokens():
            local_features, covered_words = self.local_score(start_cell, words)
            child_cell = Cell(term, start_cell, start_cell, covered_words,
                              local_features, self.weights)
            # if child_cell.score != cell.score:
            #     print("cell score = {}".format(cell.score))
            #     print("child cell score = {}".format(child_cell.score))
            self.dfs(child_cell, words, final_cells)
        end_time = time.time()
        if verbose:
            print("total # of parses: %d" % len(final_cells), file=sys.stderr)
            print("execution time: %ds" % (end_time-start_time), file=sys.stderr)

        # Rank and print all parses
        for cell in final_cells:
            self.final_score(cell, words)

        sorted_cells = Queue.PriorityQueue()
        for cell in final_cells:
            sorted_cells.put(cell)

        top_K_parses = []
        for i in xrange(top_K):
            cell = sorted_cells.get()
            if verbose:
                print("{}:\t\t{}\t{}\t{}\t{}\t{}".format(cell.getCommand(), cell.score,
                        cell.length, cell.cnl_words(), word_set-cell.cnl_words(), cell.featureSet()),
                        file=sys.stderr)
            top_K_parses.append(cell)

        return top_K_parses

    def dfs(self, cell, words, final_cells):

        term = cell.term

        # mark head command
        if cell.isHead():
            self.head_cell = cell
        cell.parent = self.head_cell

        # skip <EOF> character
        if term == Enumerator.EOF:
            return

        # TODO: handle compound commands
        if term == "|":
            return

        # maximum depth reached, backtrack
        if cell.length == self.max_command_length:
            return

        # update enumerator
        if self.allows(term):
            # print("{}".format(self.legal_tokens()), file=sys.stderr)
            self.push(term)
        else:
            print("Error: not allowed {}".format(self.legal_tokens()), file=sys.stderr)
            sys.exit(1)
            return

        # yield legal command
        if cell.length >= self.min_command_length and self.allow_eof():
            final_cells.append(cell)

        # look ahead one step
        queue = Queue.PriorityQueue()

        # Enumerator.HOLE priority
        # if self.allow_arbitrary():
        #     term = Enumerator.HOLE
        #     local_features, covered_words = self.local_score(cell, words)
        #     child_cell = Cell(term, None, cell, covered_words, local_features, self.weights)
        #     self.dfs(child_cell, words, final_cells)

        for term in self.legal_tokens():
            local_features, covered_words = self.local_score(cell, words)
            child_cell = Cell(term, None, cell, covered_words, local_features, self.weights)
            queue.put(child_cell)
        for i in xrange(self.beam_size):
            if queue.empty():
                break
            self.dfs(queue.get(), words, final_cells)

        self.pop()
        return


if __name__ == "__main__":
    nl_cmd = sys.argv[1]

    simple_grammar = load_syntax([os.path.join(os.path.dirname(__file__),
                                               "..", "..", "data", "primitive_cmds_grammar.json")])
    grammar = make_full_grammar(simple_grammar, max_pipeline_depth=3)

    # minimum number of tokens in command = 2
    # maximum number of tokens in command = 3
    # beam size = 10
    parser = Parser(grammar, 2, 5, 7)
    parser.make_phrase_table(os.path.join(os.path.dirname(__file__),
                                           "..", "..", "data", "phrase-table.gz"))

    questionFile = "../../baseline1/data/true.questions"
    commandFile = "../../baseline1/data/true.commands"

    dataset = readTrainExamples(questionFile, commandFile)
    parser.train(dataset, 10, 1)

    parser.parse(nl_cmd)
