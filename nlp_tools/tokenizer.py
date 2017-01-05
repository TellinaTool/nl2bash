"""
A natural language command tokenizer.
"""

import re

from . import constants, ner
from .spellcheck import spell_check as spc

# from nltk.stem.wordnet import WordNetLemmatizer
# lmtzr = WordNetLemmatizer()
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english")

# Regular expressions used to tokenize an English sentence.
_WORD_SPLIT = re.compile("^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<]|[\)|\]|\}|\>]$")
_WORD_SPLIT_RESPECT_QUOTES = re.compile('(?:[^\s,"]|"(?:\\.|[^"])*")+')


def basic_tokenizer(sentence, lower_case=True, normalize_digits=True,
                    normalize_long_pattern=True, lemmatization=True,
                    remove_stop_words=True, correct_spell=True):
    """Very basic tokenizer: used for English tokenization."""

    # remove content in parentheses
    _PAREN_REMOVE = re.compile('\([^)]*\)')
    sentence = re.sub(_PAREN_REMOVE, '', sentence)

    try:
        sentence = sentence.replace("“", '"')
        sentence = sentence.replace("”", '"')
        sentence = sentence.replace('‘', '\'')
        sentence = sentence.replace('’', '\'')
    except UnicodeDecodeError:
        sentence = sentence.replace("“".decode('utf-8'), '"')
        sentence = sentence.replace("”".decode('utf-8'), '"')
        sentence = sentence.replace('‘'.decode('utf-8'), '\'')
        sentence = sentence.replace('’'.decode('utf-8'), '\'')
    sentence = sentence.replace('`\'', '"') \
            .replace('``', '"') \
            .replace("''", '"') \
            .replace(' \'', ' "') \
            .replace('\' ', '" ') \
            .replace('`', '"') \
            .replace('(', ' ( ') \
            .replace(')', ' ) ')
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

    # convert abbreviation writings and negations
    sentence = re.sub('\'s', ' \'s', sentence)
    sentence = re.sub('\'re', ' \'re', sentence)
    sentence = re.sub('\'ve', ' \'ve', sentence)
    sentence = re.sub('\'d', ' \'d', sentence)
    sentence = re.sub('\'t', ' \'t', sentence)

    sentence = re.sub("^[T|t]o ", '', sentence)

    words = re.findall(_WORD_SPLIT_RESPECT_QUOTES, sentence)

    # entity_dict = collections.defaultdict(int)

    normalized_words = []
    for i in xrange(len(words)):
        word = words[i].strip()
        # remove unnecessary upper cases
        if lower_case:
            if i == 0 and word[0].isupper() and len(word) > 1 and word[1:].islower():
                word = word.lower()

        # spelling correction
        if correct_spell:
            if word.isalpha() and word.islower() and len(word) > 2:
                old_w = word
                word = spc.correction(word)
                if word != old_w:
                    print("spell correction: {} -> {}".format(old_w, word))

        # remove English stopwords
        if remove_stop_words:
            if word in constants.ENGLISH_STOPWORDS:
                continue

        # covert number words into numbers
        if word in constants.word2num:
            word = str(constants.word2num[word])

        # quotation recovery
        if not is_english_word(word):
            # msg = word + ' -> '
            if not word.startswith('"'):
                word = '"' + word
            if not word.endswith('"'):
                word = word + '"'

        # normalize long patterns
        if normalize_long_pattern:
            word = ner.normalize_named_entity(word)

        # normalize digits
        word = ner.normalize_number_in_token(word)\
            if normalize_digits and not word.startswith("-") else word

        # lemmatization
        if lemmatization:
            try:
                word = stemmer.stem(word.decode('utf-8'))
            except AttributeError:
                word = stemmer.stem(word)

        # index entities in text
        # if word == normalizer._REGEX \
        #         or word == normalizer._NUM\
        #         or word == normalizer._PARAMETER:
        #     root = word
        #     word += str(entity_dict[root])
        #     entity_dict[root] += 1

        # remove empty words
        if not word.strip():
            continue

        # maintain special tokens
        if word.startswith('_'):
            word = word.upper()

        normalized_words.append(word)

    return normalized_words


# --- Utility functions --- #

def is_english_word(word):
    """Check if a token is normal English word."""
    if any(x.isalpha() for x in word):
        if word[-1].isdigit():
            return False
    if word.isalpha() and any(x.isupper() for x in word):
        return False
    return bool(re.match('[0-9A-Za-z\-\'\(\)]+$', word, re.IGNORECASE))


def is_stopword(w):
    return w in constants.ENGLISH_STOPWORDS


def test_nl_tokenizer():
    while True:
        nl = raw_input("> ")
        tokens = basic_tokenizer(nl)
        print(tokens)


if __name__ == '__main__':
    test_nl_tokenizer()