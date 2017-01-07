"""
A named entity recognizer in the file system operation domain.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import re

from . import constants

def add_space(s):
    return ' ' + s + ' '

def decorate_boundaries(r):
    """
    Match named entity boundary characters s.a. quotations and whitespaces.
    """
    return constants.include_space(constants.quotation_safe(r))

def annotate(tokens):
    """
    Identify named entities in a (tokenized) sentence and replace them with the
    corresponding categories.

    The NER so far recognizes the following named entity categories:
    - Pattern-based:
        - File
        - Directory
        - Path
        - Permission
        - Username
        - Groupname
        - DateTime
        - Other Patterns
    - Quantity-based:
        - Number
        - Size
        - Timespan

    :return: 1. a list of tokens where the named entities are replaced with
        category names
             2. a dictionary that stores a list of named entities matched for
        each category
    """

    sentence = ' '.join(tokens)
    entities = collections.defaultdict(list)

    # Credit: time expressions adapted from
    # https://github.com/nltk/nltk_contrib/blob/master/nltk_contrib/timex.py
    rel_day = r'(today|yesterday|tomorrow|the day before yesterday|' \
              r'the day after tomorrow)'
    standard_time = r'\d+:\d+:\d+\.?\d*'
    standard_datetime = r'\d{1,4}[\/-]\d{1,4}[\/-]\d{1,4}' \
                        r'([,|\s]' + standard_time + r')?'
    textual_datetime = constants._MONTH_RE + r'(\s\d{0,2})?([,|\s]\d{2,4})?' \
                        r'([,|\s]' + standard_time + r')?'

    permission_bit = r'(suid|sgid|sticky|sticki)(\sbit)?'
    permission_bit_set = r'(set)*(uid|gid|sticky|sticki)(=\d+)*'

    # -- Size
    _SIZE_RE = re.compile(decorate_boundaries(r'(\d+|a)\s*' + constants._SIZE_UNIT))
    sentence = annotate_ner(_SIZE_RE, constants._SIZE, sentence, entities)

    # -- Timespan
    _DURATION_RE = re.compile(decorate_boundaries(
        r'(\d+|a|this|next(\s\d+)?|last(\s\d+)?|previous(\s\d+)?)\s*'
        + constants._DURATION_UNIT))
    sentence = annotate_ner(_DURATION_RE, constants._TIMESPAN, sentence, entities)

    # -- DateTime
    _DATETIME_RE = re.compile(decorate_boundaries('(' + rel_day + '|' +
                    standard_time + '|' + standard_datetime + '|' +
                    textual_datetime + ')'))
    sentence = annotate_ner(_DATETIME_RE, constants._DATETIME, sentence, entities)

    # -- Permission
    _PERMISSION_RE = re.compile(decorate_boundaries('(' +
                constants._NUMERICAL_PERMISSION_RE + '|' + 
                constants._PATTERN_PERMISSION_RE + '|' +
                permission_bit + '|' + permission_bit_set + ')'))
    sentence = annotate_ner(_PERMISSION_RE, constants._PERMISSION, sentence, entities)

    # -- Number
    _NUMBER_RE = re.compile(decorate_boundaries(constants._DIGIT_RE))
    sentence = annotate_ner(_NUMBER_RE, constants._NUMBER, sentence, entities)

    # -- Path
    _PATH_RE = re.compile(decorate_boundaries(r'([^ ]*\/)+[^ ]*'))
    sentence = annotate_ner(_PATH_RE, constants._PATH, sentence, entities)

    # -- File/Directory
    _FILE_RE = re.compile(decorate_boundaries(r'([^ ]*\.[^ ]*|' +
                          constants._FILE_EXTENSION_RE + ')'))
    sentence = annotate_ner(_FILE_RE, constants._FILE, sentence, entities)

    # -- Other patterns
    _REGEX_RE = re.compile(decorate_boundaries(constants._SPECIAL_SYMBOL_RE))
    sentence = annotate_ner(_REGEX_RE, constants._REGEX, sentence, entities)

    normalized_words = []
    words = re.findall(constants._WORD_SPLIT_RESPECT_QUOTES, sentence)
    for w in words:
        if not w.startswith('_') and not is_english_word(w):
            normalized_words.append(constants._REGEX)
        else:
            normalized_words.append(w)

    return normalized_words, entities


def annotate_ner(pattern, category, sentence, entities):
    for m in re.finditer(pattern, sentence):
        entities[category].append(sentence[m.start(0):m.end(0)].strip())
    sentence = re.sub(pattern, add_space(category), sentence).strip()
    return sentence

def normalize_number_in_token(token):
    return re.sub(re.compile(_DIGIT_RE), _NUMBER, token)

def is_english_word(word):
    """Check if a token is normal English word."""
    if any(x.isalpha() for x in word):
        if word[-1].isdigit():
            return False
    if word.isalpha() and any(x.isupper() for x in word):
        return False
    return bool(re.match('[0-9A-Za-z\-\'\(\)]+$', word, re.IGNORECASE))
