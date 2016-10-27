#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Domain-specific natural Language and bash command tokenizer.
"""

# builtin
from __future__ import print_function

import re
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "data"))

import nast, normalizer
import gazetteer
import spellcheck.spell_check as spc

# from nltk.stem.wordnet import WordNetLemmatizer
# lmtzr = WordNetLemmatizer()
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english")

# Regular expressions used to tokenize an English sentence.
_WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<]|[\)|\]|\}|\>]$")
_WORD_SPLIT_RESPECT_QUOTES = re.compile(b'(?:[^\s,"]|"(?:\\.|[^"])*")+')

_SPACE = b"<SPACE>"

def is_english_word(word):
    """Check if a token is normal English word."""
    if any(x.isalpha() for x in word):
        if word[-1].isdigit():
            return False
    if word.isalpha() and any(x.isupper() for x in word):
        return False
    return bool(re.match('[0-9A-Za-z\-\'\(\)]+$', word, re.IGNORECASE))

def is_stopword(w):
    return w in gazetteer.ENGLISH_STOPWORDS

def char_tokenizer(sentence, base_tokenizer=None, normalize_digits=False,
                   normalize_long_pattern=False):
    if base_tokenizer:
        # normalization is not needed for character model
        tokens = base_tokenizer(sentence, normalize_digits=False,
                                normalize_long_pattern=False)
    else:
        tokens = [sentence]
    chars = []
    for token in tokens:
        for c in token:
            chars.append(c)
        chars.append(_SPACE)
    return chars[:-1]

def basic_tokenizer(sentence, lower_case=True, normalize_digits=True,
                    normalize_long_pattern=True, lemmatization=True,
                    remove_stop_words=True, correct_spell=True):
    """Very basic tokenizer: used for English tokenization."""

    # remove content in parentheses
    sentence = re.sub(r'\([^)]*\)', '', sentence)

    try:
        sentence = sentence.replace("“", '"')
        sentence = sentence.replace("”", '"')
        sentence = sentence.replace('‘', '\'')
        sentence = sentence.replace('’', '\'')
    except UnicodeDecodeError, e:
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
            if word in gazetteer.ENGLISH_STOPWORDS:
                continue

        # covert number words into numbers
        if word in gazetteer.word2num:
            word = str(gazetteer.word2num[word])

        # quotation recovery
        if not is_english_word(word):
            # msg = word + ' -> '
            if not word.startswith('"'):
                word = '"' + word
            if not word.endswith('"'):
                word = word + '"'

        # normalize long patterns
        if normalize_long_pattern:
            word = normalizer.normalize_pattern(word)

        # normalize digits
        word = re.sub(normalizer._DIGIT_RE, normalizer._NUM, word) \
            if normalize_digits and not word.startswith("-") else word

        # lemmatization
        if lemmatization:
            word = stemmer.stem(word)

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


def bash_tokenizer(cmd, normalize_digits=True, normalize_long_pattern=True,
                   recover_quotation=True):
    tree = normalizer.normalize_ast(cmd, normalize_digits, normalize_long_pattern,
                         recover_quotation)
    return normalizer.to_tokens(tree)


def bash_parser(cmd, normalize_digits=True, normalize_long_pattern=True,
                recover_quotation=True):
    """Parse bash command into AST."""
    return normalizer.normalize_ast(cmd, normalize_digits, normalize_long_pattern,
                                    recover_quotation)


def pretty_print(node, depth=0):
    """Pretty print the AST."""
    try:
        print("    " * depth + node.kind.upper() + '(' + node.value + ')')
        for child in node.children:
            pretty_print(child, depth+1)
    except AttributeError, e:
        print("    " * depth)


def ast2list(node, order='dfs', list=None, ignore_flag_order=False, arg_type_only=False,
             with_parent=False):
    """Linearize the AST."""
    if order == 'dfs':
        if arg_type_only and node.is_argument() and node.is_open_vocab():
            list.append(node.prefix + node.arg_type)
        else:
            if node.is_option() and with_parent and node.headcommand:
                list.append(node.prefix + node.headcommand.value + "@@" + node.value)
            else:
                list.append(node.symbol)
        if node.get_num_of_children() > 0:
            if node.kind == "headcommand" and ignore_flag_order:
                children = sorted(node.children, key=lambda x:x.value)
            else:
                children = node.children
            for child in children:
                ast2list(child, order, list, ignore_flag_order, arg_type_only,
                         with_parent)
            list.append(normalizer._H_NO_EXPAND)
        else:
            list.append(normalizer._V_NO_EXPAND)
    return list


def list2ast(list, order='dfs'):
    """Convert the linearized parse tree back to the AST data structure."""
    return normalizer.list_to_ast(list, order)


def ast2tokens(node, loose_constraints=False, ignore_flag_order=False,
               arg_type_only=False, with_parent=False):
    return normalizer.to_tokens(node, loose_constraints, ignore_flag_order, arg_type_only,
                                with_parent=with_parent)


def ast2command(node, loose_constraints=False, ignore_flag_order=False):
    return ' '.join(normalizer.to_tokens(node, loose_constraints, ignore_flag_order))


def ast2template(node, loose_constraints=False, arg_type_only=True):
    # convert a bash AST to a template that contains only reserved words and argument types
    # flags are alphabetically ordered
    tokens = normalizer.to_tokens(node, loose_constraints, ignore_flag_order=True,
                                  arg_type_only=arg_type_only)
    return ' '.join(tokens) 


def cmd2template(cmd, normalize_digits=True, normalize_long_pattern=True,
                recover_quotation=True, arg_type_only=True,
                loose_constraints=False):
    # convert a bash command to a template that contains only reserved words and argument types
    # flags are alphabetically ordered
    tree = normalizer.normalize_ast(cmd, normalize_digits, normalize_long_pattern,
                         recover_quotation)
    return ast2template(tree, loose_constraints, arg_type_only)


def paren_parser(line):
    def order_child_fun(node):
        if len(node.children) > 1 and node.children[0].value in ["and", "or"]:
            for child in node.children:
                order_child_fun(child)
            node.children = node.children[:1] + sorted(node.children[1:],
                    key=lambda x:x.value if x.kind == "t" else x.children[0].value)

    """A very simple algorithm for parsing data with parentheses."""
    if not line.startswith("("):
        line = "( " + line
    if not line.endswith(")"):
        line = line + " )"
    words = line.strip().split()

    root = nast.Node(kind="root", value="root")
    stack = []

    i = 0
    while i < len(words):
        word = words[i]
        if word == "(":
            if stack:
                # creates non-terminal
                node = nast.Node(kind="nt", value="<n>")
                stack[-1].add_child(node)
                node.parent = stack[-1]
                stack.append(node)
            else:
                stack.append(root)
        elif word == ")":
            if stack:
                stack.pop()
        else:
            node = nast.Node(kind="t", value=word)
            stack[-1].add_child(node)
            node.parent = stack[-1]
        i += 1
        if len(stack) == 0:
            break;

    # order nodes
    order_child_fun(root)

    return root


def test_nl_tokenizer():
    while True:
        nl = raw_input("> ")
        tokens = basic_tokenizer(nl)
        print(tokens)


def test_bash_parser():
    while True:
        try:
            cmd = raw_input("> ")
            norm_tree = bash_parser(cmd)
            pruned_tree = normalizer.prune_ast(norm_tree)
            print()
            print("AST:")
            pretty_print(norm_tree, 0)
            print("Pruned AST:")
            pretty_print(pruned_tree, 0)
            search_history = ast2list(norm_tree, 'dfs', list=[])
            for state in search_history:
                print(state)
            tree = list2ast(search_history + ['<PAD>'])
            print()
            print("Command Template (flags in alphabetical order):")
            print(ast2template(norm_tree))
            print("Pruned Command Template (flags in alphabetical order):")
            print(ast2template(pruned_tree))
            print()
        except EOFError as ex:
            break


def data_preparation(nl_file, cm_file, outfile):
    with open(nl_file) as f:
        nl_list = f.readlines()
    with open(cm_file) as f:
        cm_list = f.readlines()
    with open(outfile, 'w') as o_f:
        for i in xrange(len(nl_list)):
            nl = nl_list[i].decode('utf-8')
            cm = cm_list[i].decode('utf-8')
            o_f.write(' '.join(basic_tokenizer(nl, normalize_digits=False, normalize_long_pattern=False)).encode('utf-8') + '\n')
            o_f.write(cm.encode('utf-8') + '\n')
            o_f.write('\n')


if __name__ == "__main__":
    # test_nl_tokenizer()
    # test_bash_parser()
    data_preparation(sys.argv[1], sys.argv[2], sys.argv[3])
