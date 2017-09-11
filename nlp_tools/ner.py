"""
A named entity recognizer in the file system operation domain.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import re

from . import constants

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
    ner_by_token_id = collections.defaultdict()
    ner_by_char_pos = collections.defaultdict()
    ner_by_category = collections.defaultdict(list)
    entities = (ner_by_char_pos, ner_by_category)

    # -- Size
    _SIZE_RE = re.compile(decorate_boundaries(
        constants.polarity_safe(r'({}|a\s)\s*'.format(constants._DIGIT_RE)) +
        constants._SIZE_UNIT))
    sentence = annotate_ner(_SIZE_RE, constants._SIZE, sentence, entities)

    # -- Timespan
    time_num_re = r'((24\*|60\*)?{}|{}(\*24|\*60))'.format(
        constants._DIGIT_RE, constants._DIGIT_RE)
    _DURATION_RE = re.compile(decorate_boundaries(constants.polarity_safe(
        r'({}|a\s|this\s|next(\s{})?\s|last(\s{})?\s|previous(\s{})?\s)\s*'.format(
        time_num_re, time_num_re, time_num_re, time_num_re) + constants._DURATION_UNIT)))
    sentence = annotate_ner(
        _DURATION_RE, constants._TIMESPAN, sentence, entities)

    # -- DateTime
    # Credit: time expressions adapted from
    # https://github.com/nltk/nltk_contrib/blob/master/nltk_contrib/timex.py
    standard_time = r'\d+:\d+:\d+\.?\d*'
    standard_datetime = r'\d{1,4}[\/-]\d{1,4}[\/-]\d{1,4}([,|\s]' + standard_time + r')?'
    textual_datetime = constants._MONTH_RE \
                       + r'(\s\d{0,2}(st|nd|th)?)?([,|\s]\d{2,4})?([,|\s]' \
                       + standard_time + r')?'
    _DATETIME_RE = re.compile(decorate_boundaries(constants.polarity_safe(
                    '(' + constants._REL_DAY_RE + '|' + standard_time + '|' +
                    standard_datetime + '|' + textual_datetime + ')')))
    sentence = annotate_ner(_DATETIME_RE, constants._DATETIME, sentence, entities)
    
    # -- Permission
    permission_bit = r'(suid|sgid|sticky|sticki)(\sbit)?'
    permission_bit_set = r'(set)?(uid|gid|sticky|sticki)(=\d+)*'
    _PERMISSION_RE = re.compile(decorate_boundaries(constants.polarity_safe(
                    '(' + constants._PATTERN_PERMISSION_RE + '|' +
                    permission_bit + '|' + permission_bit_set + ')')))
    sentence = annotate_ner(
        _PERMISSION_RE, constants._PERMISSION, sentence, entities)

    # -- Number
    _NUMBER_RE = re.compile(decorate_boundaries(
        constants.polarity_safe(constants._DIGIT_RE)))
    sentence = annotate_ner(_NUMBER_RE, constants._NUMBER, sentence, entities)

    # -- Match all quoted patterns first to prevent partial matching within quotations
    # -- Directory
    _DIRECTORY_RE = re.compile(constants.include_quotations(r'[^"\']*\/'))
    sentence = annotate_ner(
        _DIRECTORY_RE, constants._DIRECTORY, sentence, entities)

    # -- File
    _FILE_RE = re.compile(constants.include_quotations(r'([^"\']*\.[^ "\']+)|' +
        r'(([^"\']*\/)+[^"\']*)|' + constants._FILE_EXTENSION_RE))
    sentence = annotate_ner(_FILE_RE, constants._FILE, sentence, entities)
    
    # -- Other patterns
    _REGEX_QUOTED_RE = re.compile(constants.include_space(constants._QUOTED_RE))
    sentence = annotate_ner(_REGEX_QUOTED_RE, constants._REGEX, sentence, entities)
    
    # -- Match all unquoted patterns
    # -- Directory
    _DIRECTORY_RE = re.compile(decorate_boundaries(r'[^ "\']*\/'))
    sentence = annotate_ner(
        _DIRECTORY_RE, constants._DIRECTORY, sentence, entities)
    
    # -- File
    _FILE_RE = re.compile(r'([^ ]*\.[^ ]+|' + r'([^ ]*\/)+[^ ]*)|(' +
        decorate_boundaries(constants._FILE_EXTENSION_RE) + ')')
    sentence = annotate_ner(_FILE_RE, constants._FILE, sentence, entities)
    
    # -- Other patterns
    _REGEX_SPECIAL_RE = re.compile(decorate_boundaries(constants._SPECIAL_SYMBOL_RE))
    sentence = annotate_ner(_REGEX_SPECIAL_RE, constants._REGEX, sentence, entities)

    # prepare list of tokens
    normalized_words = []
    i = 0
    for m in re.finditer(
        re.compile(constants._WORD_SPLIT_RESPECT_QUOTES), sentence):
        w = m.group(0)
        # exclude isolated quotations
        if w in ['"', '\'']:
            continue
        if set(w) == {'-'}:
            if (m.start(0), m.end(0)) in ner_by_char_pos:
                surface, category = ner_by_char_pos[(m.start(0), m.end(0))]
                normalized_words.append(category)
                ner_by_token_id[i] = (surface, category)
        else:
            if not constants.is_english_word(w):
                # catch missed patterns in the final pass
                normalized_words.append(constants._REGEX)
                ner_by_token_id[i] = (w, constants._REGEX)
                ner_by_char_pos[(m.start(0), m.end(0))] = (w, constants._REGEX)
                ner_by_category[constants._REGEX].append(
                    (w, m.start(0), m.end(0)))
            else:
                normalized_words.append(w)
        i += 1

    return normalized_words, (ner_by_token_id, ner_by_char_pos, ner_by_category)

def annotate_ner(pattern, category, sentence, entities):
    ner_by_char_pos, ner_by_category = entities
    for m in re.finditer(pattern, sentence):
        surface = sentence[m.start(0):m.end(0)].strip()
        if category == constants._DATETIME:
            # TODO: rule-based system is not good at differentiating between
            # "May" the month and "may" the modal verb
            if surface == 'may':
                continue
        if category in [constants._FILE, constants._REGEX,
                        constants._DIRECTORY, constants._PATH]:
            if surface in ['i.e', 'i.e.', 'e.g', 'e.g.',
                           's.a', 's.a.', 's.t', 's.t.']:
                continue
        # replace recognized entities with placeholders to ensure that entity
        # position calculation is always correct
        rep_start = m.start(0) + 1 if re.match(r'\s', sentence[m.start(0)]) \
            else m.start(0)
        rep_end = m.end(0) - 1 if re.match(r'\s', sentence[m.end(0)-1]) \
            else m.end(0)
        sentence = sentence[:rep_start] + '-' * (rep_end - rep_start) + \
                   sentence[rep_end:]
        ner_by_char_pos[(rep_start, rep_end)] = (surface, category)
        ner_by_category[category].append((surface, rep_start, rep_end))
    return sentence

def normalize_number_in_token(token):
    return re.sub(re.compile(constants._DIGIT_RE), constants._NUMBER, token)
