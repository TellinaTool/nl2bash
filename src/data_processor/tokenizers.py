"""
Tokenizers.
"""
from src.bashlint import bash, nast
import src.bashlint as bashlint
import src.data_processor.data_utils as data_utils
from src.nlp_tools import constants, tokenizer


def parallel_data_to_tokens(dataset):
    nl_tokens_list, cm_tokens_list = [], []
    for exp in dataset.example_list:
        exp.nl_tokens = nl_to_tokens(exp.nl, tokenizer.basic_tokenizer)
        exp.nl_tokens_orig = nl_to_tokens(
            exp.nl, tokenizer.basic_tokenizer, to_lower_case=False, lemmatization=False)
        exp.cm_tokens = cm_to_tokens(exp.cm, bashlint.bash_tokenizer)
        nl_tokens_list.append(exp.nl_tokens)
        cm_tokens_list.append(exp.cm_tokens)
    return nl_tokens_list, cm_tokens_list


def parallel_data_to_chars(dataset):
    nl_chars_list, cm_chars_list = [], []
    for exp in dataset.example_list:
        exp.nl_chars = nl_to_chars(exp.nl)
        exp.cm_chars = cm_to_chars(exp.cm)
        nl_chars_list.append(exp.nl_chars)
        cm_chars_list.append(exp.cm_chars)
    return nl_chars_list, cm_chars_list


def parallel_data_to_partial_tokens(dataset):
    nl_partial_tokens_list, cm_partial_tokens_list = [], []
    for exp in dataset.example_list:
        exp.nl_partial_tokens = nl_to_partial_tokens(exp.nl, tokenizer.basic_tokenizer)
        exp.nl_partial_tokens_orig = nl_to_partial_tokens(
            exp.nl, tokenizer.basic_tokenizer, to_lower_case=False, lemmatization=False)
        exp.cm_partial_tokens = cm_to_partial_tokens(exp.cm, bashlint.bash_tokenizer)
        nl_partial_tokens_list.append(exp.nl_partial_tokens)
        cm_partial_tokens_list.append(exp.cm_partial_tokens)
    return nl_partial_tokens_list, cm_partial_tokens_list


def parallel_data_to_normalized_tokens(dataset):
    nl_normalized_tokens_list, cm_normalized_tokens_list = [], []
    for exp in dataset.example_list:
        exp.nl_normalized_tokens = nl_to_tokens(exp.nl, tokenizer.ner_tokenizer)
        exp.cm_normalized_tokens = cm_to_tokens(exp.cm, bashlint.bash_tokenizer, arg_type_only=True)
        nl_normalized_tokens_list.append(exp.nl_normalized_tokens)
        cm_normalized_tokens_list.append(exp.cm_normalized_tokens)
    return nl_normalized_tokens_list, cm_normalized_tokens_list


def nl_to_chars(nl, use_preprocessing=False):
    nl_example = []
    if use_preprocessing:
        nl_tokens = nl_to_tokens(nl, tokenizer.basic_tokenizer, lemmatization=False)
        for c in ' '.join(nl_tokens):
            if c == ' ':
                nl_example.append(constants._SPACE)
            else:
                nl_example.append(c)
    else:
        nl_example = string_to_chars(nl)
    return nl_example


def cm_to_chars(cm, use_preprocessing=False):
    cm_example = []
    if use_preprocessing:
        cm_tokens = cm_to_tokens(
            cm, bashlint.bash_tokenizer, with_prefix=True,
            with_flag_argtype=True)
        for i, t in enumerate(cm_tokens):
            if not nast.KIND_PREFIX in t:
                cm_example.append(t)
            else:
                kind, token = t.split(nast.KIND_PREFIX, 1)
                if kind.lower() == 'utility':
                    cm_example.append(token)
                elif kind.lower() == 'flag':
                    cm_example.append(token)
                else:
                    for c in token:
                        cm_example.append(c)
            if i < len(cm_tokens) - 1:
                cm_example.append(constants._SPACE)
    else:
        cm = bashlint.clean_and_normalize(cm)
        cm_example = string_to_chars(cm)
    return cm_example


def string_to_chars(s):
    assert (isinstance(s, str))
    chars = []
    for c in s:
        if c == ' ':
            chars.append(constants._SPACE)
        else:
            chars.append(c)
    return chars


def nl_to_partial_tokens(s, tokenizer, to_lower_case=True, lemmatization=True):
    return string_to_partial_tokens(
        nl_to_tokens(s, tokenizer, to_lower_case=to_lower_case,
                     lemmatization=lemmatization), use_arg_start_end=False)


def cm_to_partial_tokens(s, tokenizer):
    s = bashlint.clean_and_normalize(s)
    return string_to_partial_tokens(cm_to_tokens(s, tokenizer))


def string_to_partial_tokens(s, use_arg_start_end=True):
    """
    Split a sequence of tokens into a sequence of partial tokens.

    A partial token sequence may consist of
        1. continuous span of alphabetical letters
        2. continuous span of digits
        3. a non-alpha-numerical character
        4. _ARG_START which indicates the beginning of an argument token
        5. _ARG_END which indicates the end of an argument token
    """
    partial_tokens = []

    for token in s:
        if not token:
            continue
        if token.isalpha() or token.isnumeric() \
                or bashlint.flag_suffix in token \
                or token in bash.binary_logic_operators \
                or token in bash.left_associate_unary_logic_operators \
                or token in bash.right_associate_unary_logic_operators:
            partial_tokens.append(token)
        else:
            arg_partial_tokens = []
            pt = ''
            reading_alpha = False
            reading_numeric = False
            for c in token:
                if reading_alpha:
                    if c.isalpha():
                        pt += c
                    else:
                        arg_partial_tokens.append(pt)
                        reading_alpha = False
                        pt = c
                        if c.isnumeric():
                            reading_numeric = True
                elif reading_numeric:
                    if c.isnumeric():
                        pt += c
                    else:
                        arg_partial_tokens.append(pt)
                        reading_numeric = False
                        pt = c
                        if c.isalpha():
                            reading_alpha = True
                else:
                    if pt:
                        arg_partial_tokens.append(pt)
                    pt = c
                    if c.isalpha():
                        reading_alpha = True
                    elif c.isnumeric():
                        reading_numeric = True
            if pt:
                arg_partial_tokens.append(pt)
            if len(arg_partial_tokens) > 1:
                if use_arg_start_end:
                    partial_tokens.append(data_utils._ARG_START)
                partial_tokens.extend(arg_partial_tokens)
                if use_arg_start_end:
                    partial_tokens.append(data_utils._ARG_END)
            else:
                partial_tokens.extend(arg_partial_tokens)

    return partial_tokens


def nl_to_tokens(s, tokenizer, to_lower_case=True, lemmatization=True):
    """
    Split a natural language string into a sequence of tokens.
    """
    tokens, _ = tokenizer(
        s, to_lower_case=to_lower_case, lemmatization=lemmatization)
    return tokens


def cm_to_tokens(s, tokenizer, loose_constraints=True, arg_type_only=False,
                 with_prefix=False, with_flag_argtype=True):
    """
    Split a command string into a sequence of tokens.
    """
    tokens = tokenizer(s, loose_constraints=loose_constraints,
                       arg_type_only=arg_type_only,
                       with_prefix=with_prefix,
                       with_flag_argtype=with_flag_argtype)
    return tokens


if __name__ == '__main__':
    print(nl_to_partial_tokens('Execute md5sum command on files found by the find command',
                               tokenizer=tokenizer.basic_tokenizer))
    print(cm_to_partial_tokens("find . -perm -600 -print",
                               tokenizer=bashlint.bash_tokenizer))