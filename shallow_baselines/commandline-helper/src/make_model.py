#!/usr/bin/env python2.7
from __future__ import print_function
"""
Usage:
    $ python make_model.py <path-to-sqlite-db-file>
"""

# builtin
import collections
import HTMLParser
import os
import re
import sqlite3
import sys

# local
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "baseline1", "src"))
import bash
import common

html = HTMLParser.HTMLParser()

CODE_REGEX = re.compile(r"<pre><code>([^<]+)<\/code><\/pre>")
def extract_code(text):
    for match in CODE_REGEX.findall(text):
        if match.strip():
            yield html.unescape(match.replace("<br>", "\n"))

def all_samples(sqlite_filename):
    with sqlite3.connect(sqlite_filename, detect_types=sqlite3.PARSE_DECLTYPES) as sqlite_db:
        for (question_text, answer_body) in sqlite_db.cursor().execute("""
                SELECT questions.Title, answers.Body
                FROM questions, answers
                WHERE questions.AcceptedAnswerId = answers.Id"""):
            for extracted_code in extract_code(answer_body):
                yield (question_text, extracted_code)

WORD_REGEX = re.compile(r"\w*-?\w+")
# basic stop words list is from http://www.ranks.nl/stopwords/
STOPWORDS = { "a", "about", "above", "after", "again", "against", "all", "am",
    "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been",
    "before", "being", "below", "between", "both", "but", "by", "can't",
    "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further",
    "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd",
    "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
    "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if",
    "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me",
    "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves",
    "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's",
    "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
    "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
    "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
    "what's", "when", "when's", "where", "where's", "which", "while", "who",
    "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't",
    "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
    "yourselves" }
STOPWORDS |= { "bash", "shell", "script" }
STOPWORDS -= { "not", "no" }
def tokenize_question(q):
    seq = []
    for word in WORD_REGEX.findall(q.lower()):
        if word not in STOPWORDS:
            yield word
            seq.append(word)
    for bigram in zip(seq, seq[1:]):
        yield bigram

COMMENT_REGEX = re.compile(r"\#.*")
PROMPT_REGEX = re.compile(r"^\s*\S*\$>?")
# CODE_TERM_REGEX = re.compile(r"(?:\"(?:\\\.|[^\\])*\")|(?:'[^']*')|(\S+)")
# CODE_STOPWORDS = { "|", ";", "[", "]", "[[", "]]", "{", "}", "(", ")", "=", ">", "<", ">>" }
def tokenize_code(code):
    code = PROMPT_REGEX.sub("", code)
    for cmd in bash.parse(str(code)):
        args = cmd[1:]
        cmd = cmd[0]
        yield cmd
        for arg in args:
            yield common.mangle_arg(cmd, arg)

def is_oneliner(code):
    return "\n" not in code.strip()

def run():
    in_sqlite = sys.argv[1]

    total_count = 0
    count = 0
    question_word_counts = collections.defaultdict(int)
    code_term_counts = collections.defaultdict(int)
    pairwise_counts = collections.defaultdict(int)

    print("Gathering stats from {}...".format(in_sqlite), file=sys.stderr)

    for question_title, extracted_code in all_samples(in_sqlite):

        total_count += 1

        if not is_oneliner(extracted_code):
            continue

        words = set(tokenize_question(question_title))
        try:
            terms = set(tokenize_code(extracted_code))
        except ValueError as e:
            # print("unable to parse question {}: {} [err={}]".format(repr(question_title), repr(extracted_code), e), file=sys.stderr)
            terms = ()

        if not terms:
            continue

        for word in words:
            question_word_counts[word] += 1

        for term in terms:
            code_term_counts[term] += 1

        for word in words:
            for term in terms:
                pairwise_counts[(word, term)] += 1

        count += 1

        if count % 1000 == 0:
            print("Processed {} ({} pairs)".format(count, len(pairwise_counts)), file=sys.stderr)

    word_total = sum(question_word_counts.values())
    term_total = sum(code_term_counts.values())

    print("Got {} examples; {} were clean enough to use".format(total_count, count), file=sys.stderr)

    print("Computing relationships...", file=sys.stderr)
    scores = collections.defaultdict(dict)
    for k, count in pairwise_counts.items():
        word, term = k
        if question_word_counts[word] < 5 or code_term_counts[term] < 5:
            continue
        scores[word][term] = (count + 0.0) / question_word_counts[word]

    print("scores = {}".format(repr(dict(scores))))
    print("word_freqs = {}".format(repr({ w : (count + 0.0)/word_total for w,count in question_word_counts.items() })))
    print("code_freqs = {}".format(repr({ t : (count + 0.0)/term_total for t,count in code_term_counts.items() })))

if __name__ == "__main__":
    run()
