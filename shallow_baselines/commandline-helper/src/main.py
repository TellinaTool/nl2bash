#!/usr/bin/env python2.7
from __future__ import print_function

import collections

from model import scores, word_freqs, code_freqs
from make_model import tokenize_question
from commands import TOOLS

EMPTY = {}

def score_tool_name(word, tool_name):
    return (1-word_freqs.get(word, 0)) * scores.get(word, EMPTY).get(tool_name, 0) * (1-code_freqs.get(tool_name, 0))

def score_tool_args(word, tool_args, root_cmd):
    return (1-word_freqs.get(word, 0)) * tool_args.score(root_cmd, word)

def score_tool(word, tool):
    return score_tool_name(word, tool.name) + score_tool_args(word, tool.flags, tool.name)

def run(q):
    words = list(tokenize_question(q))
    scores = { tool:sum(score_tool(word, tool) for word in words) for tool in TOOLS }
    print("Suggestions:")
    for t in sorted(scores.keys(), key=scores.get, reverse=True):
        word_scores = { w : score_tool(w, t) for w in words }
        relevant_words = sorted((w for w in words if word_scores[w] > 0), reverse=True, key=word_scores.get)
        score_func = lambda arg: sum(score_tool_args(w, arg, t.name) for w in words)
        print("        {:40} [score={:1.2f}: {}]".format(
            t.name + t.flags.propose_incantation(t.name, score_func(t.flags), score_func),
            scores[t], ", ".join(str(w) for w in relevant_words[:5])))

if __name__ == "__main__":
    import sys
    run(" ".join(sys.argv[1:]))
