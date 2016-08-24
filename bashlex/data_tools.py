"""
Domain-specific natural Language and bash command tokenizer.
"""

# builtin
from __future__ import print_function

import re
import sys
sys.path.append("../data")

import bash, normalizer, utils
import gazetteer

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()

# Regular expressions used to tokenize an English sentence.
# _WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<|\'|\"|\`]|[\)|\]|\}|\>|\'|\"|\`]$")
_WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<]|[\)|\]|\}|\>]$")
_WORD_SPLIT_RESPECT_QUOTES = re.compile(b'(?:[^\s,"]|"(?:\\.|[^"])*")+')

def is_stopword(w):
    return w in gazetteer.ENGLISH_STOPWORDS

def basic_tokenizer(sentence, lower_case=True, normalize_digits=True,
                    normalize_long_pattern=True,
                    lemmatization=True):
    """Very basic tokenizer: used for English tokenization."""
    sentence = sentence.replace('`\'', '"') \
            .replace('``', '"') \
            .replace("''", '"') \
            .replace(' \'', ' "') \
            .replace('\' ', '" ') \
            .replace('`', '"') \
            .replace('(', '( ') \
            .replace(')', ' )')
            # .replace('[', '[ ') \
            # .replace('{', '{ ') \
            # .replace(']', ' ]') \
            # .replace('}', ' }') \
            # .replace('<', '< ') \
            # .replace('>', ' >')
    sentence = re.sub('^\'', '"', sentence)
    sentence = re.sub('\'$', '"', sentence)

    sentence = re.sub('(,\s+)|(,$)', ' ', sentence)
    sentence = re.sub('(;\s+)|(;$)', ' ', sentence)
    sentence = re.sub('(:\s+)|(:$)', ' ', sentence)
    sentence = re.sub('(\.\s+)|(\.$)', ' ', sentence)

    sentence = re.sub('\'s', '\\\'s', sentence)
    sentence = re.sub('\'re', '\\\'re', sentence)
    sentence = re.sub('\'ve', '\\\'ve', sentence)
    sentence = re.sub('\'d', '\\\'d', sentence)
    sentence = re.sub('\'t', '\\\'t', sentence)

    words = re.findall(_WORD_SPLIT_RESPECT_QUOTES, sentence)

    normalized_words = []
    for i in xrange(len(words)):
        word = words[i].strip()

        # remove unnecessary upper cases
        if lower_case:
            if len(word) > 1 and word[0].isupper() and word[1:].islower():
                word = word.lower()

        # lemmatization
        if lemmatization:
            word = lmtzr.lemmatize(word)

        # remove English stopwords
        if word in ENGLISH_STOPWORDS:
            continue

        # covert number words into numbers
        if word in word2num:
            word = str(word2num[word])

        # normalize regular expressions
        if not bash.is_english_word(word):
            # msg = word + ' -> '
            if not word.startswith('"'):
                word = '"' + word
            if not word.endswith('"'):
                word = word + '"'
            # msg += word
            # print(msg)

        # normalize long patterns
        if ' ' in word and len(word) > 3:
            try:
                assert(word.startswith('"') and word.endswith('"'))
            except AssertionError, e:
                print("Quotation Error: space inside word " + sentence)
            if normalize_long_pattern:
                word = bash._LONG_PATTERN

        # normalize digits
        word = re.sub(bash._DIGIT_RE, bash._NUM, word) \
            if normalize_digits and not bash.is_option(word) else word

        # convert possessive expression
        if word.endswith("'s"):
            normalized_words.append(word[:-2])
            normalized_words.append("'s")
        else:
            normalized_words.append(word)

    return normalized_words

def bash_tokenizer(cmd, normalize_digits=True, normalize_long_pattern=True,
                   recover_quotation=True):
    tree = normalizer.normalize_ast(cmd, normalize_digits, normalize_long_pattern,
                         recover_quotation)
    return normalizer.to_tokens(tree)

@utils.deprecated
def basic_tokenizer_regex(sentence, normalize_digits=True, lower_case=True):
    """Very basic tokenizer: used for English tokenization."""
    words = []
    for space_separated_fragment in sentence.replace('\n', ' ').strip().split():
        words.extend(re.split(_WORD_SPLIT, space_separated_fragment))
    normalized_words = []
    for i in xrange(len(words)):
        w = words[i].strip()
        word = re.sub(bash._DIGIT_RE, bash._NUM, w) \
            if normalize_digits and not bash.is_option(w) else w
        if lower_case:
            # remove unnecessary upper cases
            if len(word) > 1 and word[0].isupper() and word[1:].islower():
                word = word.lower()
        normalized_words.append(word.encode('utf-8'))
    return normalized_words



