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
    ner_by_pos = collections.defaultdict()
    ner_by_category = collections.defaultdict(list)
    entities = (ner_by_pos, ner_by_category)

    # -- Size
    _SIZE_RE = re.compile(decorate_boundaries(
        constants.polarity_safe(r'({}|a)\s*'.format(constants._DIGIT_RE)) +
        constants._SIZE_UNIT))
    sentence = annotate_ner(_SIZE_RE, constants._SIZE, sentence, entities)

    # -- Timespan
    _DURATION_RE = re.compile(decorate_boundaries(constants.polarity_safe(
        r'({}|a|this|next(\s{})?|last(\s{})?|previous(\s{})?)\s*'.format(
            constants._DIGIT_RE, constants._DIGIT_RE, constants._DIGIT_RE,
            constants._DIGIT_RE) + constants._DURATION_UNIT)))
    sentence = annotate_ner(
        _DURATION_RE, constants._TIMESPAN, sentence, entities)

    # -- DateTime
    # Credit: time expressions adapted from
    # https://github.com/nltk/nltk_contrib/blob/master/nltk_contrib/timex.py
    standard_time = r'\d+:\d+:\d+\.?\d*'
    standard_datetime = r'\d{1,4}[\/-]\d{1,4}[\/-]\d{1,4}' \
                        r'([,|\s]' + standard_time + r')?'
    textual_datetime = constants._MONTH_RE + r'(\s\d{0,2})?([,|\s]\d{2,4})?' \
                        r'([,|\s]' + standard_time + r')?'
    _DATETIME_RE = re.compile(decorate_boundaries(constants.polarity_safe(
                    '(' + constants._REL_DAY_RE + '|' + standard_time + '|' +
                    standard_datetime + '|' + textual_datetime + ')')))
    sentence = annotate_ner(
        _DATETIME_RE, constants._DATETIME, sentence, entities)

    # -- Permission
    permission_bit = r'(suid|sgid|sticky|sticki)(\sbit)?'
    permission_bit_set = r'(set)?(uid|gid|sticky|sticki)(=\d+)*'
    _PERMISSION_RE = re.compile(decorate_boundaries(constants.polarity_safe(
                    '(' + constants._NUMERICAL_PERMISSION_RE + '|' +
                    constants._PATTERN_PERMISSION_RE + '|' +
                    permission_bit + '|' + permission_bit_set + ')')))
    sentence = annotate_ner(
        _PERMISSION_RE, constants._PERMISSION, sentence, entities)

    # -- Number
    _NUMBER_RE = re.compile(decorate_boundaries(
        constants.polarity_safe(constants._DIGIT_RE)))
    sentence = annotate_ner(_NUMBER_RE, constants._NUMBER, sentence, entities)

    # -- Path
    # _PATH_RE = re.compile(decorate_boundaries(r'([^ ]*\/)+[^ ]*'))
    # sentence = annotate_ner(_PATH_RE, constants._PATH, sentence, entities)

    # -- Directory
    _DIRECTORY_RE = re.compile(decorate_boundaries(r'[^ ]*\/'))
    sentence = annotate_ner(
        _DIRECTORY_RE, constants._DIRECTORY, sentence, entities)

    # -- File
    _FILE_RE = re.compile(decorate_boundaries(r'([^ ]*\.[^ ]*|' +
                    r'([^ ]*\/)+[^ ]*|' + constants._FILE_EXTENSION_RE +
                    r's?' + ')'))
    sentence = annotate_ner(_FILE_RE, constants._FILE, sentence, entities)

    # -- Other patterns
    _REGEX_RE = re.compile(decorate_boundaries(constants._SPECIAL_SYMBOL_RE))
    sentence = annotate_ner(_REGEX_RE, constants._REGEX, sentence, entities)

    ner_by_pos, ner_by_category = entities
    normalized_words = []
    word_matches = re.finditer(
        re.compile(constants._WORD_SPLIT_RESPECT_QUOTES), sentence)
    for m in word_matches:
        w = m.group(0)
        if set(w) == {'_'}:
            normalized_words.append(ner_by_pos[(m.start(0), m.end(0))][0])
        else:
            if not is_english_word(w):
                # catch missed irregular patterns in the final pass
                normalized_words.append(constants._REGEX)
                ner_by_pos[(m.start(0), m.end(0))] = (w, constants._REGEX)
                ner_by_category[constants._REGEX].append((w, m.start(0), m.end(0)))
            else:
                normalized_words.append(w)


    return normalized_words, entities

def annotate_ner(pattern, category, sentence, entities):
    ner_by_pos, ner_by_category = entities
    for m in re.finditer(pattern, sentence):
        surface = sentence[m.start(0):m.end(0)].strip()
        ner_by_pos[(m.start(0), m.end(0))] = (surface, category)
        ner_by_category[category].append((surface, m.start(0), m.end(0)))
        # replace recognized entities with placeholders to ensure that entity
        # position calculation is always correct
        sentence = sentence[:m.start(0)] + '_' * (m.end(0) - m.start(0)) + \
                   sentence[m.end(0):]
    return sentence

def normalize_number_in_token(token):
    return re.sub(re.compile(constants._DIGIT_RE), constants._NUMBER, token)

def is_english_word(word):
    """Check if a token is a normal English word."""
    if any(x.isalpha() for x in word):
        if word[-1].isdigit():
            return False
    if word.isalpha() and any(x.isupper() for x in word):
        return False
    return bool(re.match('[0-9A-Za-z\-\'\(\)]+$', word, re.IGNORECASE))
