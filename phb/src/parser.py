#!/usr/bin/env python

from __future__ import print_function

import collections
import copy
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

    def addTerm(self, t, b, (s, w_covered)):
        self.phrases.append(t)
        self.backpointer = b
        self.score += s
        for w in w_covered:
            self.uncovered_words.remove(w)

    def addTermToLastPhrase(self, t, b, (s, w_covered)):
        self.phrases[-1].append(t)
        self.backpointer = b
        self.score += s
        for w in w_covered:
            self.uncovered_words.remove(w)

    def finalizeScoring(self, redundant_word_score):
        self.score -= redundant_word_score * len(self.uncovered_words)

    def toString(self):
        return ' '.join(self.phrases)

# A cell group contains different chunking of the same partial command
class CellGroup(object):
    def __init__(self, c):
        self.cells = []
        self.max_cell = None
        self.max_score = 0.0
        if c:
            self.cells.append(c)
            self.max_cell = c
            self.max_score = c.score

    def addCell(self, c):
        self.cells.append(c)
        if c.score > self.max_score:
            self.max_cell = c
            self.max_score = c.score

    def finalizeScoring(self, redundant_word_score):
        for c in self.cells:
            c.finalizeScoring(redundant_word_score)
        self.max_score = 0.0
        for c in self.cells:
            if c.score > self.max_score:
                self.max_cell = c
                self.max_score = c.score

    def tailTerm(self):
        if len(self.cells) < 1:
            print("Error: empty cell group doesn't have a tail token", file=sys.stderr)
            sys.exit(1)
        return self.cells[0].phrases[-1][-1]

class Parser(object):
    def __init__(self, n):
        self.max_phrase_length = n
        self.enumerator = None
        self.P2TScores = None
        self.T2PScores = None
        self.redundant_word_score = 1e-5
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

    def openToMerge(self, cell):
        if len(cell.phrases) == 0:
            # empty cell
            return False
        return len(cell.phrases[-1]) < self.max_phrase_length

    def parse(self, sent):
        self.words = sent.split()

        # DFS
        start_cell = Cell("__START_SYMBOL__", None,
                          self.score_tool("__START_SYMBOL__"), self.words)
        start_group = CellGroup(start_cell)
        last_cell = start_cell
        last_group = start_group
        final_group = []
        stack = []
        for term in self.enumerator.legal_tokens():
            cell = copy.deepcopy(last_cell)
            cell.addTerm(term, (last_cell, last_group), self.score_tool(term))
            stack.append(CellGroup(cell))

        while stack:
            last_group = stack.pop()

            # enumerating
            term = last_group.tailTerm()
            if term == "*":
                self.enumerator.push(Enumerator.HOLE)
            else:
                self.enumerator.push(term)

            for term in self.enumerator.legal_tokens():
                cell_group = CellGroup()
                # add all possible chunkings
                for last_cell in last_group:
                    cell = copy.deepcopy(last_cell)
                    cell.addTerm(term, (last_cell, last_group), self.score_tool(term))
                    cell_group.addCell(cell)
                    if self.openToMerge(last_cell):
                        cell = copy.deepcopy(last_cell)
                        cell.addTermToLastPhrase(term, (last_cell, last_group),
                                                 self.score_tool(term))
                        cell_group.addCell(cell)
            # TODO: set backtracking right
            print(cell.term, file=sys.stderr)
            self.enumerator.push(cell.term)

        # Rank and print all parses
        for cell_group in final_group:
            cell_group.finalizeScoring(self.redundant_word_score)
        for cell_group in sorted(final_group, key=lambda x:x.max_score, reverse=True):
            print("{}:\t\t{}".format(cell_group.max_cell.toString(), cell_group.max_score),
                  file=sys.stderr)

if __name__ == "__main__":
    nl_cmd = sys.argv[1]
    parser = Parser(2)
    parser.make_grammar(["../../data/primitive_cmds_grammar.json"])
    parser.make_phrase_table("../../data/phrase-table.gz")
    parser.parse(nl_cmd)