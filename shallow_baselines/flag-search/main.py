from __future__ import print_function
import os
import json
import glob

# 3rd party
import nltk
from nltk.stem.porter import PorterStemmer
nltk.download('punkt')

cmd_docs = { }
flag_docs = { }
descs = { }

# Stemming, tokenization
stem = PorterStemmer().stem
def tokenize(s):
    toks = [stem(tok) for tok in nltk.word_tokenize(s)]
    return toks + list(zip(toks, toks[1:]))

def datafiles():
    yield os.path.join(os.path.dirname(__file__), "..", "data", "jsonman-for-search.txt")

print("Reading data...")
for f in datafiles():
    with open(f, "r") as handle:
        data = json.loads(handle.read())
        for j in data:
            cmd = j["name"]
            desc = j["description"]
            flags = { (cmd, flag["name"]): flag["description"] for flag in j["optionDesc"] }
            cmd_docs[cmd] = tokenize(desc)
            for k, desc in flags.items():
                descs[k] = desc
                toks = tokenize(desc)
                cmd_docs[cmd] += toks
                flag_docs[k] = toks

print("Indexing...")
import tfidf
engine = tfidf.tfidf()
flag_engines = {}
for cmd, toks in cmd_docs.items():
    engine.addDocument(cmd, toks)
    flag_engines[cmd] = tfidf.tfidf()
    for (cmdd, flag), flag_toks in flag_docs.items():
        if cmdd == cmd:
            flag_engines[cmd].addDocument(flag, flag_toks)

print("Running...")
while True:
    try:
        inp = raw_input("> ")
    except EOFError:
        break
    toks = tokenize(inp)
    if toks:
        scores = engine.similarities(toks)
        top_cmds = sorted(scores, key=lambda s: s[1], reverse=True)
        for cmd, score in top_cmds[:3]:
            print("{} [score={:0.2}]".format(cmd, score))
            engine2 = flag_engines[cmd]
            top_flags = sorted(engine2.similarities(toks), key=lambda s: s[1], reverse=True)
            for flag, score in top_flags[:5]:
                print("  [score={score:0.2}] {desc}".format(flag=flag, desc=descs[(cmd, flag)].strip(), score=score))
            print()
