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

    def __init__(self, t, bp, s, w_c, w_uc):
        """
        :member terms:          new term string assumed by this cell
        :member backpointer:    pointer to parent cell
        :member isEOF:          if cell is terminable
        :member score:          score of the partial command parse up to this cell
        :member left_nl_words:  uncovered natural language words up to this cell
        :member features:       features of the partial command parse up to this cell
        """
        self.term = t
        self.backpointer = bp
        self.length = bp.length + 1 if bp else 0
        self.score = bp.score + s if bp else 0
        self.left_nl_words = set(w_uc)
        # print("{}".format(w_c), file=sys.stderr)
        for w in w_c:
            if w in self.left_nl_words:
                self.left_nl_words.remove(w)

        self.features = []

    def finalizeScoring(self, redundant_word_score):
        self.score += redundant_word_score * len(self.left_nl_words)

    def genCommand(self):
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
        # print("{}".format(command), file=sys.stderr)
        return ' '.join(command[1:])

class Parser(Enumerator):

    def __init__(self, grammar, min_cl=2, max_cl=10):
        """
        :param grammar:
        :param min_cl: minimum number of tokens in command
        :param max_cl: maximum number of tokens in command
        """
        Enumerator.__init__(self, grammar)
        self.P2TScores = None
        self.T2PScores = None
        self.redundant_word_score = 1e-5
        self.ungrounded_token_score = -1e-5
        self.min_command_length = min_cl
        self.max_command_length = max_cl

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

    def score_tool(self, term, words):
        #TODO: consider other methods for rule scoring
        covered_words = set()
        if not term in self.T2PScores:
            return self.ungrounded_token_score, words
        max = 0.0
        for word in words:
            if word in self.T2PScores[term]:
                if self.T2PScores[term][word] > max:
                    max = self.T2PScores[term][word]
                    print("{} {}".format(term, word), file=sys.stderr)
                    covered_words.add(word)
        # print("{}".format(covered_words), file=sys.stderr)
        return max, covered_words

    def parse(self, sent):
        words = sent.split()

        start_cell = Cell("__START_SYMBOL__", None,
                          0.0, set(), words)
        final_cells = []                # tail cells of all legal commands

        print("Enumerating all commands up to length {}".format(self.max_command_length), file=sys.stderr)

        # DFS
        self.dfs(start_cell, words, final_cells)

        # Rank and print all parses
        for cell in final_cells:
            cell.finalizeScoring(self.redundant_word_score)
        for cell in sorted(final_cells, key=lambda x:x.score, reverse=True)[:20]:
            print("{}:\t\t{}\t{}".format(cell.genCommand(), cell.score, cell.length),
                  file=sys.stderr)

    def dfs(self, cell, words, final_cells):

        term = cell.term
        # print("{} {}".format(term, cell.length), file=sys.stderr)
        # skip <EOF> character
        if term == Enumerator.EOF:
            return

        #TODO: handle compound commands
        if term == "|":
            return

        # yield legal command
        if cell.length > self.min_command_length and self.allow_eof():
            final_cells.append(cell)

        # maximum depth reached, backtrack
        if cell.length == self.max_command_length:
            return

        # update enumerator
        if term != "__START_SYMBOL__":
            if self.allows(term):
                # print("{}".format(self.legal_tokens()), file=sys.stderr)
                self.push(term)
            else:
                # print("Not allowed {}".format(self.legal_tokens()), file=sys.stderr)
                # print("Error: shouldn't happen!", file=sys.stderr)
                sys.exit(1)
                return

        # look ahead one step
        for term in self.legal_tokens():
            score, covered_words = self.score_tool(term, words)
            child_cell = Cell(term, cell, score, covered_words, cell.left_nl_words)
            self.dfs(child_cell, words, final_cells)

        if term != "__START_SYMBOL__":
            self.pop()
        return


if __name__ == "__main__":
    nl_cmd = sys.argv[1]

    simple_grammar = load_syntax([os.path.join(os.path.dirname(__file__), "..", "..", "data", "primitive_cmds_grammar.json")])
    grammar = make_full_grammar(simple_grammar, max_pipeline_depth=3)

    parser = Parser(grammar, 2, 3)
    parser.make_phrase_table("../../data/phrase-table.gz")
    parser.parse(nl_cmd)