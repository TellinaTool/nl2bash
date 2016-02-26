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
import shlex
import sqlite3
import sys
sys.path.append("/home/xilin/Packages")
from semantics.lexical import stanford_tokenize, stanford_lemmatize
 
html = HTMLParser.HTMLParser()

CODE_REGEX = re.compile(r"<pre><code>([^<]+)<\/code><\/pre>")
def extract_code(text):
    match = CODE_REGEX.search(text)
    return html.unescape(match.group(1).replace("<br>", "\n")) if match else None

def all_samples(sqlite_filename):
    with sqlite3.connect(sqlite_filename, detect_types=sqlite3.PARSE_DECLTYPES) as sqlite_db:
        for (question_title, answer_body) in sqlite_db.cursor().execute("""
                SELECT questions.Title, answers.Body
                FROM questions, answers
                WHERE questions.AcceptedAnswerId = answers.Id"""):
            extracted_code = extract_code(answer_body)
            if extracted_code:
                yield (question_title, extracted_code)

WORD_REGEX = re.compile(r"\w*-?\w+")
# basic stop words list is from http://www.ranks.nl/stopwords/
# STOPWORDS = { "a", "about", "above", "after", "again", "against", "all", "am", 
#               "an", "and", "any", "are", "aren't", "as", "at", "be", "because", 
#               "been", "before", "being", "below", "between", "both", "but", 
#               "by", "can't", "cannot", "could", "couldn't", "did", "didn't", 
#               "do", "does", "doesn't", "doing", "don't", "down", "during", 
#               "each", "few", "for", "from", "further", "had", "hadn't", "has", 
#               "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", 
#               "he's", "her", "here", "here's", "hers", "herself", "him", "himself", 
#               "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", 
#               "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", 
#               "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", 
#               "of", "off", "on", "once", "only", "or", "other", "ought", "our", 
#               "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", 
#               "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", 
#               "such", "than", "that", "that's", "the", "their", "theirs", "them", 
#               "themselves", "then", "there", "there's", "these", "they", "they'd", 
#               "they'll", "they're", "they've", "this", "those", "through", "to", 
#               "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", 
#               "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", 
#               "when's", "where", "where's", "which", "while", "who", "who's", "whom", 
#               "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", 
#               "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" }
STOPWORDS = {"a", "an", "the", 
             "be", "'s", "been", "being", "was", "were", "here", "there", "do", "how", 
             "i", "i'd", "i'll", "i'm", "i've", "me", "my", "myself",
             "can", "could", "did", "do", "does", "doing", 
             "must", "should", "would",
             "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves".
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
             "command".
             "for",
             "to",
             "but"}
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
    return shlex.split(code, comments=True)

def is_oneliner(code):
    return "\n" not in code.strip()

def run():
    in_sqlite = sys.argv[1]

    count = 0
    question_word_counts = collections.defaultdict(int)
    code_term_counts = collections.defaultdict(int)
    pairwise_counts = collections.defaultdict(int)

    print("Gathering stats from {}...".format(in_sqlite), file=sys.stderr)
    
    questionFile = open("../data/stackoverflow/questions", 'w')
    commandFile = open("../data/stackoverflow/commands", 'w')

    for question_title, extracted_code in all_samples(in_sqlite):

        if not is_oneliner(extracted_code):
            continue
       
        words = [w.lower() for w in stanford_lemmatize(question_title.strip())]
        words = [w for w in words if not w in STOPWORDS]
        # print("{}".format(words), file=sys.stderr)
        try:
            terms = tokenize_code(extracted_code.strip())
        except ValueError as e:
            # print("unable to parse question {}: {} [err={}]".format(repr(question_title), repr(extracted_code), e), file=sys.stderr)
            terms = []

        questionFile.write("%s\n" % ' '.join(words))
        commandFile.write("%s\n" % ' '.join(terms))
    
        count += 1
        if count % 1000 == 0:
            print("Processed {} ({} pairs)".format(count, len(pairwise_counts)), file=sys.stderr)

    questionFile.close()
    commandFile.close()
    
if __name__ == "__main__":
    run()
