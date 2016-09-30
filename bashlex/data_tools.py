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

import normalizer
import gazetteer
import spellcheck.spell_check as spc

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()

# Regular expressions used to tokenize an English sentence.
_WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<]|[\)|\]|\}|\>]$")
_WORD_SPLIT_RESPECT_QUOTES = re.compile(b'(?:[^\s,"]|"(?:\\.|[^"])*")+')

_SPACE = b"<SPACE>"

def is_english_word(word):
    """Check if a token is normal English word."""
    return bool(re.match('[A-Za-z\-\'\(\)]+$', word, re.IGNORECASE))

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
                    remove_stop_words=True):
    """Very basic tokenizer: used for English tokenization."""
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

        # spelling correction
        if word.isalpha() and word.islower() and len(word) > 2:
            old_w = word
            word = spc.correction(word)
            if word != old_w:
                print("spell correction: {} -> {}".format(old_w, word))

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
        if not is_english_word(word):
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
                word = normalizer._LONG_PATTERN

        # normalize digits
        word = re.sub(normalizer._DIGIT_RE, normalizer._NUM, word) \
            if normalize_digits and not word.startswith("-") else word

        # remove empty words
        if not word.strip():
            continue

        # convert possessive expression
        if len(word) > 2 and word.endswith("'s"):
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


def ast2list(node, order='dfs', list=None,
             ignore_flag_order=False, arg_type_only=False):
    """Linearize the AST."""
    if order == 'dfs':
        if arg_type_only and not node.isReservedWord():
            list.append(node.kind.upper() + '_' + node.arg_type)
        else:
            list.append(node.symbol)
        if node.getNumChildren() > 0:
            if node.kind == "headcommand" and ignore_flag_order:
                children = sorted(node.children, key=lambda x:x.value)
            else:
                children = node.children
            for child in children:
                ast2list(child, order, ignore_flag_order,
                         arg_type_only, list)
            list.append(normalizer._H_NO_EXPAND)
        else:
            list.append(normalizer._V_NO_EXPAND)
    return list


def list2ast(list, order='dfs'):
    """Convert the linearized parse tree back to the AST data structure."""
    return normalizer.list_to_ast(list, order)


def ast2tokens(node, loose_constraints=False, ignore_flag_order=False,
               arg_type_only=False):
    return normalizer.to_tokens(node, loose_constraints,
                                ignore_flag_order, arg_type_only)


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


def rewrite(ast, temp):
    arg_slots = normalizer.arg_slots(ast)

    def rewrite_fun(node):
        if node.kind == "argument" and not node.arg_type == "ReservedWord":
            for i in xrange(len(arg_slots)):
                if not arg_slots[i][1] \
                    and arg_slots[i][0].arg_type == node.arg_type:
                    node.value = arg_slots[i][0].value
                    arg_slots[i][1] = True
                    break
        else:
            for child in node.children:
                rewrite_fun(child)

    ast2 = normalizer.normalize_ast(temp)
    rewrite_fun(ast2)

    return ast2


if __name__ == "__main__":
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
            # print(to_command(norm_tree))
            search_history = ast2list(norm_tree, 'dfs', [])
            for state in search_history:
                print(state)
            tree = list2ast(search_history + ['<PAD>'])
            # pretty_print(tree, 0)
            # print(to_template(tree, arg_type_only=False))
            print()
            print("Command Template (flags in alphabetical order):")
            print(ast2template(norm_tree))
            print("Pruned Command Template (flags in alphabetical order):")
            print(ast2template(pruned_tree))
            print()
        except EOFError as ex:
            break


