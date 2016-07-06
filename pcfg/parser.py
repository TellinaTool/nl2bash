#!/usr/bin/env python

from __future__ import print_function

import Queue
import cPickle as pickle
import copy
import gzip
import os
import random
import sys
from random import shuffle
sys.path.append("../..")
import time

from misc.grammar import *
from misc.bleu import BLEU
from misc.util import *

class Cell(object):

    def __init__(self, t, p, bp, w_c, ff, weights):
        """
        :member terms:          new term string consumed by this cell
        :member p:              pointer to parent cell in the syntax tree
        :member backpointer:    pointer to last cell sequentially
        :member isEOF:          if cell is terminable
        :member score:          score of the partial command parse
        :member covered_words:  natural language words covered by this cell
        :member features:       features counts of the partial command parse up to this cell
        :member feature_vector: sparse vector representation of features
        """
        self.term = t
        self.parent = p
        self.backpointer = bp
        self.length = bp.length + 1 if bp else 0
        self.features = ff
        # self.feature_vector = ff + bp.feature_vector if bp else ff
        # self.score = self.feature_vector().dot(weights.T)[0, 0]
        self.score = bp.score + sum([weights[f]*ff[f] for f in ff]) if bp else 0
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

    def is_eof(self):
        return self.term == "<EOF>"

    def is_head(self):
        if not self.backpointer:
            return False
        return self.backpointer.is_start()
        # return self.IS_HEAD

    # def setHead(self):
    #     self.IS_HEAD = True

    def is_start(self):
        return self.IS_START

    def set_start(self):
        self.IS_START = True

    def get_terms(self):
        terms = [self.term]
        bp = self.backpointer
        while (bp and not bp.is_start()):
            terms.insert(0, bp.term)
            bp = bp.backpointer
        return terms

    def get_command(self):
        command = [self.term]
        bp = self.backpointer
        while (bp and not bp.is_start()):
            command.insert(0, bp.term)
            bp = bp.backpointer
        return ' '.join(command)

    # cell features

    def cnl_words(self):
        covered_words = copy.deepcopy(self.covered_words)
        bp = self.backpointer
        while (bp and not bp.is_start()):
            covered_words |= bp.covered_words
            bp = bp.backpointer
        return covered_words

    def cmd_arg(self):
        return head_arg_template.format(self.parent.term, self.term)

    def feature_set(self):
        features = copy.deepcopy(self.features)
        bp = self.backpointer
        while (bp and not bp.is_start()):
            for f in bp.features:
                features[f] = bp.features[f]
            bp = bp.backpointer
        return features

    def feature_vector(self):
        return self.feature_vector

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
        self.step_size = 0.01

        # params
        self.__term_index__ = None
        self.__word_index__ = None
        self.__feature_index__ = None
        self.__feature_freq__ = None
        self.weights = None
        self.__tuple_template__ = tuple_template
        self.__head_arg_template__ = head_arg_template

        # special features
        # self.__unknown_term_feat__ = "__unknown_term_feat__"
        # self.__unknown_word_feat__ = "__unknown_word_feat__"
        # self.__unknown_combination_feat__ = "__unknown_combination_feat__"
        # self.__unknown_term_word_feat__ = "__unknown_term_word_feat__"

    def read_phrase_table(self, inputFile):
        self.T2PScores = collections.defaultdict(dict)
        with gzip.open(inputFile, 'rb') as f:
            for line in f.readlines():
                parts = line.strip().split("|||")
                nl_phrase = parts[0].strip()
                cmd_snippet = parts[1].strip()
                phi_cmd_nl, lex_cmd_nl, phi_nl_cmd, lex_nl_cmd = \
                    [float(s) for s in parts[2].split()]
                self.T2PScores[cmd_snippet][nl_phrase] = lex_nl_cmd

    def read_pmi_table(self, inputFile):
        with open(inputFile) as f:
            self.pmis = pickle.load(f)

    def create_feature_index(self, dataset):
        if not self.__term_index__:
            self.__term_index__ = {}
        if not self.__word_index__:
            self.__word_index__ = {}
        if not self.__feature_index__:
            self.__feature_index__ = {}
        if not self.__feature_freq__:
            self.__feature_freq__ = collections.defaultdict(int)
        if not self.weights:
            self.weights = collections.defaultdict(float)
        for example in dataset:
            terms = example.get_terms()
            words = example.get_words()
            features = example.feature_set0()
            for term in terms:
                self.update_term_index(term)
            for word in words:
                self.update_word_index(word)
            for feature in features:
                self.__feature_freq__[feature] += 1

        # unknown token, word
        # self.update_feature_index(self.__unknown_term_word_feat__)

        for feature in self.__feature_freq__:
            if self.__feature_freq__[feature] < self.__feature_freq_thresh__:
                continue
            self.update_feature_index(feature)
        self.featureDim = len(self.__feature_index__)

        print("{} features in total".format(self.featureDim))

    def update_term_index(self, term):
        if not term in self.__term_index__:
            self.__term_index__[term] = len(self.__term_index__)

    def update_word_index(self, word):
        if not word in self.__word_index__:
            self.__word_index__[word] = len(self.__word_index__)

    def update_feature_index(self, feat):
        if not feat in self.__feature_index__:
            self.__feature_index__[feat] = len(self.__feature_index__)
            self.weights[feat] = 0.0

    def local_score(self, term, words):
        # TODO: consider more complex features
        # features = ss.lil_matrix((1, self.featureDim))
        features = collections.defaultdict(int)
        covered_words = set()

        # if not term in self.__term_index__:
        #     term = "unk_term"

        for word in words:
            feature = self.__tuple_template__.format(term, word)
            if feature in self.__feature_index__:
                pmi = self.pmis[term][word]
                features[feature] = pmi
                covered_words.add(word)
            # if not word in self.__word_index__:
            #     word = "unk_word"


            # growing feature set on the fly
            # feature = self.__tuple_template__.format(term, word)
            # if not feature in self.__feature_index__:
            #     self.update_feature_index(feature)
            # features[feature] = 1
            # if not word == "unk_word":
            #     covered_words.add(word)

        return features, covered_words

    def final_score(self, cell, words):
        # cell.score += self.redundant_word_score * len(set(words) - cell.cnl_words())
        pass

    def score_example(self, example):
        score = 0.0
        for feature in example.feature_set(self.pmis, self.__feature_index__):
            score += self.weights[feature]
        return score

    def train(self, dataset, T, top_K):

        # Indexing features
        self.create_feature_index(dataset)

        # initialization
        for cmd_snippet in self.T2PScores:
            for nl_phrase in self.T2PScores[cmd_snippet]:
                feature = self.__tuple_template__.format(cmd_snippet, nl_phrase)
                if feature in self.__feature_index__:
                    # ind = self.__feature_index__[feature]
                    self.weights[feature] = self.T2PScores[cmd_snippet][nl_phrase]

        # Perceptron

        start_time = time.time()
        for t in xrange(T):
            print("Iteration {}:".format(t))
            num_correct = 0
            bleu_total = 0.0

            # shuffle dataset
            shuffle(dataset)

            start_time_t = time.time()
            for i in xrange(len(dataset)):
                example = dataset[i]
                print("question.{}:\t{}".format(i, example.sent))

                top_K_parses = self.parse(example.sent, top_K, False)

                # Update
                if top_K_parses[0].get_command() != example.cmd:
                    pred_feature = top_K_parses[0].feature_set()
                    # print(pred_feature)
                    gt_feature = example.feature_set(self.pmis, self.__feature_index__)
                    # print(gt_feature)
                    for feat in gt_feature:
                        self.weights[feat] += 2 * self.step_size * gt_feature[feat]
                    for feat in pred_feature:
                        self.weights[feat] -= self.step_size * pred_feature[feat]
                else:
                    num_correct += 1

                bleu = BLEU.compute(top_K_parses[0].get_terms(), [example.get_terms()], weights=[0.25, 0.25, 0.25, 0.25])
                bleu_total += bleu

                print("predict_parse:\t{} ({})".format(top_K_parses[0].get_command(), top_K_parses[0].score))
                print("actual_parse:\t{}".format(example.cmd))
                print("bleu score:\t{}".format(bleu))
                print()

            end_time_t = time.time()
            print("training time = %ds" % (end_time_t - start_time_t))
            print("training accuracy = %f" % ((num_correct + 0.0) / len(dataset)))
            print("training average bleu score = %f" % (bleu_total / len(dataset)))

        end_time = time.time()
        print("total training time = %ds" % (end_time - start_time))

        with open(os.path.join(os.path.dirname(__file__), "..", "model", "model.cpkl"), 'wb') as o_f:
            pickle.dump(self, o_f)

    def parse(self, sent, top_K=50, verbose=True):
        words = sent.split()
        word_set = set(words)

        start_cell = Cell("__START_SYMBOL__", None, None, set(),
                          {}, self.weights)
        start_cell.set_start()
        final_cells = []                # store tail cells of all legal commands

        if verbose:
            print("Enumerating all commands up to length {}".format(
                self.max_command_length), file=sys.stderr)

        # DFS
        start_time = time.time()
        for term in self.legal_tokens():
            local_features, covered_words = self.local_score(self.term_to_str(term), word_set)
            child_cell = Cell(self.term_to_str(term), start_cell, start_cell, covered_words,
                              local_features, self.weights)
            self.dfs(child_cell, word_set, final_cells)
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
            if sorted_cells.empty():
                break
            cell = sorted_cells.get()
            if verbose:
                print("no.{}\t{}:\t\t{}\t{}\t{}\t{}".format(i, cell.get_command(), cell.score,
                        cell.length, cell.cnl_words(), word_set-cell.cnl_words()))
            top_K_parses.append(cell)

        return top_K_parses

    def dfs(self, cell, word_set, final_cells):

        term = cell.term

        # mark head command
        if cell.is_head():
            self.head_cell = cell
        cell.parent = self.head_cell

        # skip <EOF> character
        if cell.is_eof():
            return

        # TODO: handle compound commands
        if term == "|":
            return

        # update enumerator
        if self.allows(self.str_to_term(term)):
            self.push(self.str_to_term(term))
        else:
            print("Error: not allowed {}".format(self.legal_tokens()), file=sys.stderr)
            sys.exit(1)
            return

        # yield legal command
        if cell.length >= self.min_command_length and self.allow_eof():
            final_cells.append(cell)

        # maximum depth reached, backtrack
        if cell.length == self.max_command_length:
            self.pop()
            return

        # look ahead one step
        queue = Queue.PriorityQueue()

        # Enumerator.HOLE priority
        # if self.allow_arbitrary():
        #     term = Enumerator.HOLE
        #     local_features, covered_words = self.local_score(cell, words)
        #     child_cell = Cell(term, None, cell, covered_words, local_features, self.weights)
        #     self.dfs(child_cell, words, final_cells)

        for term in self.legal_tokens():
            local_features, covered_words = self.local_score(self.term_to_str(term), word_set)
            child_cell = Cell(self.term_to_str(term), None, cell, covered_words, local_features, self.weights)
            # if cell.length == self.min_command_length:
            #     print(self.__term_index__)
            #     print(cell.length, cell.get_command(), cell.score, cell.feature_set())
            queue.put(child_cell)
        for i in xrange(self.beam_size):
            if queue.empty():
                break
            child_cell = queue.get()
            self.dfs(child_cell, word_set, final_cells)

        self.pop()
        return

    def term_to_str(self, term):
        if term == Enumerator.HOLE:
            return "*"
        elif term == Enumerator.EOF:
            return "<EOF>"
        else:
            return term

    def str_to_term(self, str):
        if str == "*":
            return Enumerator.HOLE
        elif str == "<EOF>":
            return Enumerator.EOF
        else:
            return str


if __name__ == "__main__":
    nl_cmd = sys.argv[1]

    simple_grammar = load_syntax([os.path.join(os.path.dirname(__file__),
                                               "..", "..", "data", "primitive_cmds_grammar.json")])
    grammar = make_full_grammar(simple_grammar, max_pipeline_depth=3)

    # minimum number of tokens in command = 2
    # maximum number of tokens in command = 3
    # beam size = 10
    parser = Parser(grammar, 2, 5, 7)
    parser.read_phrase_table(os.path.join(os.path.dirname(__file__),
                                           "..", "..", "data", "phrase-table.gz"))
    parser.read_pmi_table(os.path.join(os.path.dirname(__file__),
                                       "..", "model", "pmi.cpkl"))

    questionFile = "../../data/train/true.questions"
    commandFile = "../../data/train/true.commands"

    dataset = read_train_examples(questionFile, commandFile)
    parser.train(dataset, 1, 1)

    parser.parse(nl_cmd)
