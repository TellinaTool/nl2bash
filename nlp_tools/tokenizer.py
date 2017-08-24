#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Natural language input tokenizer.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re, sys
if sys.version_info > (3, 0):
    from six.moves import xrange

from . import constants, ner
from .spellcheck import spell_check as spc

# from nltk.stem.wordnet import WordNetLemmatizer
# lmtzr = WordNetLemmatizer()
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english")


def clean_sentence(sentence):
    """
    Fix punctuation errors and extract main content of a sentence.
    """

    # remove content in parentheses
    _PAREN_REMOVE = re.compile('\([^)]*\)')
    sentence = re.sub(_PAREN_REMOVE, '', sentence)

    try:
        sentence = sentence.replace("“", '"')\
            .replace("”", '"')\
            .replace('‘', '\'')\
            .replace('’', '\'')
    except UnicodeDecodeError:
        sentence = sentence.replace("“".decode('utf-8'), '"')\
            .replace("”".decode('utf-8'), '"')\
            .replace('‘'.decode('utf-8'), '\'')\
            .replace('’'.decode('utf-8'), '\'')
    sentence = sentence.replace('`\'', '"')\
        .replace('``', '"')\
        .replace("''", '"')\
        .replace('(', ' ( ')\
        .replace(')', ' ) ')\
        .replace(' `', ' \'') \
        .replace('` ', '\' ') \
        .replace('server`s', 'server\'s')

    sentence = re.sub('(,\s+)|(,$)', ' ', sentence)
    sentence = re.sub('(;\s+)|(;$)', ' ', sentence)
    sentence = re.sub('(:\s+)|(:$)', ' ', sentence)
    sentence = re.sub('(\.\s+)|(\.$)', ' ', sentence)

    # convert abbreviation writings and negations
    sentence = re.sub('\'s', ' \'s', sentence)
    sentence = re.sub('\'re', ' \'re', sentence)
    sentence = re.sub('\'ve', ' \'ve', sentence)
    sentence = re.sub('\'d', ' \'d', sentence)
    sentence = re.sub('\'t', ' \'t', sentence)

    sentence = re.sub("^[T|t]o ", '', sentence)
    sentence = re.sub('\$\{HOME\}', '\$HOME', sentence)
    sentence = re.sub('"?normal\/regular"?', 'regular', sentence)
    sentence = re.sub('"?regular\/normal"?', 'regular', sentence)
    sentence = re.sub('"?normal/regualar"?', 'regular', sentence)
    sentence = re.sub(
        '"?file\/directory"?', 'file or directory', sentence)
    sentence = re.sub(
        '"?files\/directories"?', 'files and directories', sentence)
    sentence = re.sub('"?name\/path"?', 'name or path', sentence)
    sentence = re.sub('"?names\/paths"?', 'name or path', sentence)
    sentence = re.sub(' pattern\' ', ' pattern ', sentence)

    return sentence


def space_tokenizer(sentence):
    """
    Split an already-tokenized sentence into tokens.
    """
    return sentence.split(), None


def basic_tokenizer(sentence, to_lower_case=True, lemmatization=True,
                    remove_stop_words=True, correct_spell=True,
                    separate_quotations=False, verbose=False,):
    """
    Regex-based English tokenizer.
    :param sentence: input sentence.
    :param to_lower_case: if set, remove capitalization at the beginning of the
        input sentence.
    :param lemmatization: if set, lemmatize the tokens.
    :param remove_stop_words: if set, remove stop words.
    :param correct_spell: if set, perform spelling error correction.
    :param separate_quotations: if set, separate quotation marks from a quoted
        token

    :return: list of tokens obtained subjected to the tokenization criteria.
    """
    sentence = clean_sentence(sentence)
    words = [x[0] for x in re.findall(
        constants._WORD_SPLIT_RESPECT_QUOTES, sentence)]
    
    normalized_words = []
    for i in xrange(len(words)):
        word = words[i].strip()

        if word in ['"', '\'']:
            continue
        
        # normalize to lower cases
        if to_lower_case:
            if len(word) > 1 and constants.is_english_word(word) \
                    and not constants.with_quotation(word):
                word = word.lower()
        
        # spelling correction
        if correct_spell:
            if word.isalpha() and word.islower() and len(word) > 2:
                old_w = word
                word = spc.correction(word)
                if word != old_w:
                    if verbose:
                        print("spell correction: {} -> {}".format(old_w, word))
       
        # remove English stopwords
        if remove_stop_words:
            if word.lower() in constants.ENGLISH_STOPWORDS:
                continue
      
        # covert number words into numbers
        if word in constants.word2num:
            word = str(constants.word2num[word])
     
        # lemmatization
        if lemmatization and not constants.starts_with_quotation(word) \
                and not constants.ends_with_quotation(word) \
                and not re.match(constants._SPECIAL_SYMBOL_RE, word):
            word = stemmer.stem(word)
    
        # remove empty words
        if not word.strip():
            continue

        if separate_quotations and constants.with_quotation(word):
            normalized_words.append(word[0])
            normalized_words.append(word[1:-1])
            normalized_words.append(word[-1])
        else:
            normalized_words.append(word)

    return normalized_words, None


def ner_tokenizer(sentence, to_lower_case=True, lemmatization=True,
                  remove_stop_words=True, correct_spell=True):
    words, _ = basic_tokenizer(
        sentence, to_lower_case=to_lower_case, lemmatization=lemmatization,
        remove_stop_words=remove_stop_words, correct_spell=correct_spell)
    return ner.annotate(words)

# --- Utility functions --- #

def test_nl_tokenizer():
    while True:
        nl = input("> ")
        tokens, ners = basic_tokenizer(nl)
        print(tokens, ners)
        tokens, ners = ner_tokenizer(nl)
        print(tokens, ners)        


if __name__ == '__main__':
    test_nl_tokenizer()
