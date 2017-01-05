"""
A named entity recognizer in the file system operation domain.
"""

import re

from .constants import _REGEX, _PARAMETER, _NUM


_DIGIT_RE = re.compile(r"\d+")


def normalize_named_entity(value, verbose=False):
    if value.isalpha() and value.isupper():
        return _REGEX
    value = value.replace("$HOME", "${HOME}")
    value = value.replace("~", "${HOME}")
    remove_current_dir = re.compile("\./")
    remove_dir_suffix = re.compile("/$")
    if not value == "/":
        value = re.sub(remove_dir_suffix, "", value)
    value = re.sub(remove_current_dir, "", value)
    if not (value.startswith("-")
            or value == "\"/\""
            or value == "/"
            or value == "\"normal/regular\""
            or value == "\"regular/normal\""
            or value == "\"files/directories\""
            or value == "\".\""
            or value == "."
            or value == "${HOME}"):
        if "$" in value:
            return _PARAMETER
        if (value[0] in ['\'', '"']
            and value[-1] in ['\'', '"']) \
                or ' ' in value \
                or '\\' in value \
                or '~' in value \
                or '*' in value \
                or '@' in value \
                or "%" in value \
                or '#' in value \
                or '?' in value:
            return _REGEX
        if '/' in value:
            if not (('u-' in value and len(value) <= 12) or
                    ('g-' in value and len(value) <= 12) or
                    ('o-' in value and len(value) <= 12) or
                    value[1:].isdigit() or
                    '+' in value or
                    '=' in value):
                return _REGEX
    for i, c in enumerate(value):
        if c == ".":
            if i == 0 or i == len(value)-1 \
                or not value[i-1].isdigit() \
                or not value[i+1].isdigit():
                return _REGEX
    return value


def normalize_number_in_token(token):
    return re.sub(_DIGIT_RE, _NUM, token)