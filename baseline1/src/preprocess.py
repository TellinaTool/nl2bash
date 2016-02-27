#!/usr/bin/env python2.7
from __future__ import print_function
"""
Usage:
    $ python preprocess.py <path-to-sqlite-db-file>
"""

# builtin
import collections
# import html
import HTMLParser
import re
import sys
import shlex
import string
import sqlite3

# 3rd party
sys.path.append("/home/xilin/Packages")
from semantics.lexical import stanford_tokenize, stanford_lemmatize

sys.path.append("../../baseline0/src")
# local
import bash
import common
from make_model import CODE_REGEX, COMMENT_REGEX, PROMPT_REGEX
from make_model import extract_code, all_samples, tokenize_code, is_oneliner

html = HTMLParser.HTMLParser()

WORD_REGEX = re.compile(r"\w*-?\w+")
# basic stop words list is from http://www.ranks.nl/stopwords/
STOPWORDS = {"a", "an", "the",
             "be", "'s", "been", "being", "was", "were", "here", "there", "do", "how",
             "i", "i'd", "i'll", "i'm", "i've", "me", "my", "myself",
             "can", "could", "did", "do", "does", "doing",
             "must", "should", "would",
             "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",
             "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his",
             "she", "she'd", "she'll", "she's",
             "it", "it's", "its", "itself",
             "we", "we'd", "we'll", "we're", "we've",
             "their", "theirs", "them", "themselves", "then", "there", "there's", "they", "they'd", "they'll", "they're", "they've",
             "let", "let's",
             "this", "that", "these", "those",
             "what", "what's",
             "which",
             "how", "how's",
             "command",
             "but"}
STOPWORDS |= { ",", ".", "!", "?", ";", ":", "\/", "\\/"}
STOPWORDS |= { "mac", "os", "x", "unix", "linux", "cmd", "bat", "bash", "command", "commandline", "command-line", "shell", "script" }
STOPWORDS -= { "not", "no" }

STOPPHRASE = { "in bash", "in unix", "in linux", "in mac os", 
               "for bash", "for unix", "for linux", "for mac os", 
               "in cmd", "command line", "in command line"
             }

def tokenize_question(q):
    seq = []
    for word in WORD_REGEX.findall(q.lower()):
        if word not in STOPWORDS:
            yield word
            seq.append(word)
    for bigram in zip(seq, seq[1:]):
        yield bigram

def run():
    in_sqlite = sys.argv[1]

    total_count = 0
    count = 0
    question_word_counts = collections.defaultdict(int)
    code_term_counts = collections.defaultdict(int)
    pairwise_counts = collections.defaultdict(int)

    print("Gathering stats from {}...".format(in_sqlite), file=sys.stderr)

    questionFile = open("../data/true.questions", 'w')
    commandFile = open("../data/true.commands", 'w')

    for question_title, extracted_code in all_samples(in_sqlite):

        total_count += 1
        
        if not is_oneliner(extracted_code):
            continue

        question_title = question_title.lower()
        question_title = question_title.replace("\\/", " ")
        question_title = question_title.replace("\/", " ")     
        for phrase in STOPPHRASE:
            question_title = question_title.replace(phrase, "")   
    
        # required by moses
        question_title = question_title.replace("<", " leftanglebrc ")
        question_title = question_title.replace(">", " rightanglebrc ")
        question_title = question_title.replace("[", " leftsquarebrc ")
        question_title = question_title.replace("]", " rightsquarebrc ")
        # extracted_code = extracted_code.replace("<", " leftanglebrc ")
        # extracted_code = extracted_code.replace(">", " rightanglebrc ")
        # extracted_code = extracted_code.replace("[", " leftsquarebrc ")
        # extracted_code = extracted_code.replace("]", " rightsquarebrc ")

        words = [w for w in stanford_lemmatize(question_title.strip())]
        words = [w for w in words if not w in STOPWORDS]
        # print("{}".format(words), file=sys.stderr)
        try:
            terms = tokenize_code(extracted_code.strip())
        except ValueError as e:
            # print("unable to parse question {}: {} [err={}]".format(repr(question_title), repr(extracted_code), e), file=sys.stderr)
            terms = []

        if not set(terms):
            continue

        questionFile.write("%s\n" % ' '.join(words))
        commandFile.write("%s\n" % ' '.join(list(terms)))

        count += 1
        if count % 1000 == 0:
            print("Processed {} ({} pairs)".format(count, total_count), file=sys.stderr)

    questionFile.close()
    commandFile.close()

if __name__ == "__main__":
    run()
