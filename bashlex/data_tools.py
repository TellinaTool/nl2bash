"""
Domain-specific natural Language and bash command tokenizer.
"""

# builtin
from __future__ import print_function

import re
import sys
sys.path.append("../data")

import bash, normalizer
import gazetteer

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()

# Regular expressions used to tokenize an English sentence.
# _WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<|\'|\"|\`]|[\)|\]|\}|\>|\'|\"|\`]$")
_WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<]|[\)|\]|\}|\>]$")
_WORD_SPLIT_RESPECT_QUOTES = re.compile(b'(?:[^\s,"]|"(?:\\.|[^"])*")+')

def is_stopword(w):
    return w in gazetteer.ENGLISH_STOPWORDS

def char_tokenizer(sentence, base_tokenizer=None, normalize_digits=False):
    if base_tokenizer:
        tokens = base_tokenizer(sentence, normalize_digits=False,
                                normalize_long_pattern=False)
    else:
        tokens = [sentence]
    chars = []
    for token in tokens:
        for c in token:
            chars.append(c)
        chars.append(' ')
    return chars[:-1]

def basic_tokenizer(sentence, lower_case=True, normalize_digits=True, normalize_long_pattern=True,
                    lemmatization=True, remove_stop_words=True):
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
        if remove_stop_words:
            if word in gazetteer.ENGLISH_STOPWORDS:
                continue

        # covert number words into numbers
        if word in gazetteer.word2num:
            word = str(gazetteer.word2num[word])

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
            if normalize_digits and not word.startswith("-") else word

        # convert possessive expression
        if word.endswith("'s"):
            normalized_words.append(word[:-2])
            normalized_words.append("'s")
        else:
            normalized_words.append(word)

    return normalized_words

def bash_parser(cmd, normalize_digits=True, normalize_long_pattern=True,
                recover_quotation=True):
    return normalizer.normalize_ast(cmd, normalize_digits, normalize_long_pattern,
                                    recover_quotation)

def bash_tokenizer(cmd, normalize_digits=True, normalize_long_pattern=True,
                   recover_quotation=True):
    tree = normalizer.normalize_ast(cmd, normalize_digits, normalize_long_pattern,
                         recover_quotation)
    return normalizer.to_tokens(tree)

def to_template(cmd, normalize_digits=True, normalize_long_pattern=True,
                   recover_quotation=True, arg_type_only=True):
    tree = normalizer.normalize_ast(cmd, normalize_digits, normalize_long_pattern,
                         recover_quotation)
    return normalizer.to_template(tree, arg_type_only=arg_type_only)

if __name__ == "__main__":
    cmd = sys.argv[1]
    print(bash_tokenizer(cmd))
    print(to_template(cmd))


