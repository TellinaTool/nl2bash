#!/usr/bin/env python

from __future__ import print_function

import collections
import gzip
import sys
sys.path.append("../../misc")
from grammar import *

class Cell(object):
    def __init__(self, t, b, score, words):
        self.phrases = [t]
        self.backpointer = b
        self.score = score
        self.uncovered_words = set(words)

    def addTerm(self, t, b, s):
        self.phrases.append(t)
        self.backpointer = b
        self.score += s

    def addTermToLastPhrase(self, t, b, s):
        self.phrases[-1].append(t)
        self.backpointer = b
        self.score += s

class Parser(object):
    def __init__(self, n):
        self.max_phrase_length = n
        self.enumerator = None
        self.P2TScores = None
        self.T2PScores = None
        self.redundant_phrase_score = 1e-5
        self.ungrounded_token_score = -1e-5

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

    def score_tool(self, term):
        covered_words = set()
        if not term in self.T2PScores:
            return self.ungrounded_token_score
        max = 0.0
        for word in self.words:
            if word in self.T2PScores[term]:
                if self.T2PScores[term][word] > max:
                    max = self.T2PScores[term][word]
                    covered_words.add(word)
        return max, covered_words

    def isActive(self, cell):
        return len(cell.phrases[-1]) < self.max_phrase_length

    def parse(self, sent):
        words = sent.split()

        # DFS
        start_cell = Cell("__START_SYMBOL__", None,
                          self.score_tool("__START_SYMBOL__"), words)
        last_cell = start_cell
        final_cells = []
        stack = [Cell(term, last_cell, self.score_tool(term), words) \
                 for term in self.enumerator.legal_tokens()]

        while stack:
            term = stack.pop()

            # enumerating
            if term == "*":
                self.enumerator.push(Enumerator.HOLE)
            print(term, file=sys.stderr)
            self.enumerator.push(term)
        self.enumerator.push(Enumerator.EOF)

if __name__ == "__main__":
    nl_cmd = sys.argv[1]
    parser = Parser(2)
    parser.make_grammar(["../../data/primitive_cmds_grammar.json"])
    parser.make_phrase_table("../../data/phrase-table.gz")
    parser.parse(nl_cmd)