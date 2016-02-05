#!/usr/bin/env python3

import collections

from model import scores, word_freqs, code_freqs
from make_model import tokenize_question

Tool = collections.namedtuple("Tool", ["name", "flags"])

TAR_ARGS = [dash + main_cmd + v + f
    for dash in ["-", ""]
    for main_cmd in "xct"
    for v in ["v", ""]
    for f in ["f", ""]]

EMPTY = {}
TOOLS = [
    Tool("find"  , flags=("-name", "-iname", "-mtime", "-size", "-and", "-or", "-not", "-exec", "-print0", "-print", "-delete")),
    Tool("ls"    , flags=("-l", "-la")),
    Tool("sed"   , flags=("-e")),
    Tool("awk"   , flags=()),
    Tool("grep"  , flags=("-v", "-r", "-l")),
    Tool("xargs" , flags=("-0", "-n1")),
    Tool("rsync" , flags=()),
    Tool("scp"   , flags=("-n",)),
    Tool("tar"   , flags=tuple(TAR_ARGS + ["-T", "--include", "--exclude"])),
    Tool("sort"  , flags=("-n", "-u")),
    Tool("head"  , flags=("-n",)),
    Tool("tail"  , flags=("-n",)),
    Tool("rm"    , flags=("-r", "-f", "-rf")),
    Tool("rmdir" , flags=()),
    Tool("mv"    , flags=()),
    Tool("cp"    , flags=("-R",)),
    Tool("chmod" , flags=("-R",)),
    Tool("git"   , flags=("branch", "commit", "clone", "rebase", "merge", "checkout", "reset", "subtree"))]

def score_tool(word, tool):
    score = (1-word_freqs.get(word, 0)) * (
        scores.get(word, EMPTY).get(tool.name, 0)*(1-code_freqs.get(tool.name, 0)) +
        sum(scores.get(word, EMPTY).get(flag, 0)*(1-code_freqs.get(flag, 0)) for flag in tool.flags))
    if isinstance(word, tuple):
        score *= len(word) # N-grams get a *N weight
    return score

def run(q):
    words = list(tokenize_question(q))
    scores = { tool:sum(score_tool(word, tool) for word in words) for tool in TOOLS }
    print("Suggested tools:")
    for t in sorted(scores.keys(), key=scores.get, reverse=True):
        word_scores = { w : score_tool(w, t) for w in words }
        relevant_words = sorted((w for w in words if word_scores[w] > 0), reverse=True, key=word_scores.get)
        print("    {:10} [score={:1.2f}: {}]".format(t.name, scores[t], ", ".join(str(w) for w in relevant_words[:5])))

if __name__ == "__main__":
    import sys
    run(" ".join(sys.argv[1:]))
