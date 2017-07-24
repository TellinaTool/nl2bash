#!/usr/bin/env python2.7
from __future__ import print_function
"""
Usage:
    $ python clean_stackoverflow.py <path-to-sqlite-db-file>
"""

# builtin
import collections
# import html
import HTMLParser
import re
import sys

# 3rd party
sys.path.append("/home/xilin/Packages")
from semantics.lexical import stanford_lemmatize

# local
import bashlex.bash
from data.utils import ENGLISH_STOPWORDS
from make_model import PROMPT_REGEX
from make_model import all_samples, is_oneliner

html = HTMLParser.HTMLParser()

WORD_REGEX = re.compile(r"\w*-?\w+")
# basic stop words list is from http://www.ranks.nl/stopwords/
STOPWORDS = ENGLISH_STOPWORDS
STOPWORDS |= { ",", ".", "!", "?", ";", ":", "\/", "\\/", "--"}
STOPWORDS |= { "mac", "os", "x", "unix", "linux", "cmd", "bat", "bash", "commandline", "command-line", "shell", "script", "shell-script" }
STOPWORDS -= { "not", "no" }

STOPPHRASE = [ "in bash command", "in linux command line", "in unix command line",
               "in linux command", "in unix command", "in command line",
               "in linux shell", "in unix shell", "in os shell", "in mac os shell",
               "in shell script", "in shell-script", "in bash shell", "in shell",
               "in shell command",
               "in bash", "in unix", "in linux", "with linux","in mac os", 
               "for bash", "for unix", "for linux", "for mac os", 
               "in cmd", "in commandline", "in command-line"
               "commandline", "command line"
             ]

def tokenize_question(q):
    seq = []
    for word in WORD_REGEX.findall(q.lower()):
        if word not in STOPWORDS:
            yield word
            seq.append(word)
    for bigram in zip(seq, seq[1:]):
        yield bigram

def tokenize_code(code):
    code = PROMPT_REGEX.sub("", code)
    for cmd in bashlex.bash.parse(str(code)):
        args = cmd[1:]
        cmd = cmd[0]
        # print("cmd:{}".format(cmd), file=sys.stderr)
        yield cmd
        for arg in args:
            yield arg

def run():
    in_sqlite = sys.argv[1]

    total_count = 0
    count = 0
    question_word_counts = collections.defaultdict(int)
    code_term_counts = collections.defaultdict(int)
    pairwise_counts = collections.defaultdict(int)

    print("Gathering stats from {}...".format(in_sqlite), file=sys.stderr)

    question_command_pairs = []
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

        words = [w for w in stanford_lemmatize(question_title.strip())]
        words = [w for w in words if not w in STOPWORDS]
        try:
            terms = list(tokenize_code(extracted_code.strip()))
            terms = [t.replace("<", " leftanglebrc ") for t in terms]
            terms = [t.replace(">", " rightanglebrc ") for t in terms]
            terms = [t.replace("[", " leftsquarebrc ") for t in terms]
            terms = [t.replace("]", " rightsquarebrc ") for t in terms]
        except ValueError as e:
            # print("unable to parse question {}: {} [err={}]".format(repr(question_title), repr(extracted_code), e), file=sys.stderr)
            terms = []
        
        if len(terms) == 0:
            continue
        if terms[0].startswith("-"):
            continue
        question_command_pairs.append((question_title, extracted_code, ' '.join(words), ' '.join(terms)))        
        # print ("{}".format(len(terms)), file=sys.stderr)
        # print ("{}".format(terms), file=sys.stderr)

        count += 1
        if count % 1000 == 0:
            print("Processed {} ({} pairs)".format(count, total_count), file=sys.stderr)

    origQuestionFile = open("../data/superuser/questions.txt", 'w')
    origCommandFile = open("../data/superuser/commands.txt", 'w')
    questionFile = open("../data/superuser/true.questions", 'w')
    commandFile = open("../data/superuser/true.commands", 'w')
    for question_title, extracted_code, question, command in sorted(question_command_pairs, key=lambda x:x[3]):
        origQuestionFile.write("%s\n" % question_title.encode('utf-8'))
        origCommandFile.write("%s\n" % extracted_code.encode('utf-8'))
        questionFile.write("%s\n" % question.encode('utf-8'))
        commandFile.write("%s\n" % command.encode('utf-8'))
    origQuestionFile.close()
    origCommandFile.close()
    questionFile.close()
    commandFile.close()

if __name__ == "__main__":
    run()
