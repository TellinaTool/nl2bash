#!/usr/bin/env python

from __future__ import print_function

import collections
import copy
import gzip
import sys
sys.path.append("../../misc")
from grammar import *

class Rule(object):
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def toString(self):
        return "{}=>{}".format(self.parent, self.child)

class Cell(object):

    def __init__(self, t, bp, s, w_uc):
        """
        :member terms: new term string assumed by this cell
        :member backpointer: pointer to parent cell
        :member score: score of the partial command parse up to this cell
        :member left_nl_words: uncovered natural language words up to this cell
        """
        self.term = t
        self.backpointer = bp
        self.rules = [Rule(bp.term, t)]
        self.score = s
        self.isEOF = False
        self.left_nl_words = set(w_uc)

    def addTerm(self, t, b, (s, w_covered)):
        self.phrases.append(t)
        self.size += 1
        self.backpointer = b
        self.score += s
        for w in w_covered:
            self.uncovered_words.remove(w)

    def addTermToLastPhrase(self, t, b, (s, w_covered)):
        self.phrases[-1].append(t)
        self.size += 1
        self.backpointer = b
        self.score += s
        for w in w_covered:
            self.uncovered_words.remove(w)

    def finalizeScoring(self, redundant_word_score):
        self.score -= redundant_word_score * len(self.uncovered_words)

    def toString(self):
        return ' '.join(self.phrases)

class Parser(object):
    """
    :param n:   upperbound on the size of the phrases considered
    :param cl:  upperbound on the length of possible commands
    """
    def __init__(self, n, cl):
        self.enumerator = None
        self.P2TScores = None
        self.T2PScores = None
        self.redundant_word_score = 1e-5
        self.ungrounded_token_score = -1e-5
        self.max_command_length = cl

    def make_grammar(self, grammarFile):
        simple_grammar = load_syntax(grammarFile)
        grammar = make_full_grammar(simple_grammar, max_pipeline_depth=3)
        self.enumerator = Enumerator(grammar)

    def make_phrase_table(self, inputFile):
        self.P2TScores = collections.defaultdict(dict)
        self.T2PScores = collections.defaultdict(dict)
        with gzip.open(inputFile, 'rb') as f:
            for line in f.readlines():
                parts = line.strip().split("|||")
                nl_phrase = parts[0]
                cmd_snippet = parts[1]
                phi_cmd_nl, lex_cmd_nl, phi_nl_cmd, lex_nl_cmd = \
                    [float(s) for s in parts[2].split()]
                # symmetric scoring
                self.P2TScores[nl_phrase][cmd_snippet] = lex_nl_cmd
                self.T2PScores[cmd_snippet][nl_phrase] = lex_nl_cmd

    def score_tool(self, rule, words):
        term = rule.child                 #TODO: consider other methods for rule scoring
        covered_words = set()
        if not term in self.T2PScores:
            return self.ungrounded_token_score
        max = 0.0
        for word in words:
            if word in self.T2PScores[term]:
                if self.T2PScores[term][word] > max:
                    max = self.T2PScores[term][word]
                    covered_words.add(word)
        return max, covered_words

    def parse(self, sent):
        words = sent.split()

        # Entry cell_table[i] stores the parseTree for command tokens [0 ... i]
        cell_table = collections.defaultdict(dict)




if __name__ == "__main__":
    nl_cmd = sys.argv[1]
    parser = Parser(2, 10)
    parser.make_grammar(["../../data/primitive_cmds_grammar.json"])
    parser.make_phrase_table("../../data/phrase-table.gz")
    parser.parse(nl_cmd)