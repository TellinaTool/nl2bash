#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Domain-specific natural Language and bash command tokenizer."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

if sys.version_info > (3, 0):
    from six.moves import xrange

from bashlint import bash, lint, nast

flag_suffix = '<FLAG_SUFFIX>'


def correct_errors_and_normalize_surface(cm):
    return lint.correct_errors_and_normalize_surface(cm)


def get_utility_statistics(utility):
    return lint.get_utility_statistics(utility)


def get_utilities(ast):
    def get_utilities_fun(node):
        utilities = set([])
        if node.is_utility():
            utilities.add(node.value)
            for child in node.children:
                utilities = utilities.union(get_utilities_fun(child))
        elif not node.is_argument():
            for child in node.children:
                utilities = utilities.union(get_utilities_fun(child))
        return utilities

    if not ast:
        return set([])
    else:
        return get_utilities_fun(ast)


def bash_tokenizer(cmd, recover_quotation=True, loose_constraints=False,
        ignore_flag_order=False, arg_type_only=False, keep_common_args=False, with_flag_head=False,
        with_flag_argtype=False, with_prefix=False, verbose=False):
    """
    Tokenize a bash command.
    """
    if isinstance(cmd, str):
        tree = lint.normalize_ast(cmd, recover_quotation, verbose=verbose)
    else:
        tree = cmd
    return ast2tokens(tree, loose_constraints, ignore_flag_order,
                      arg_type_only, keep_common_args=keep_common_args, with_flag_head=with_flag_head,
                      with_prefix=with_prefix, with_flag_argtype=with_flag_argtype)


def bash_parser(cmd, recover_quotation=True, verbose=False):
    """
    Parse bash command into AST.
    """
    ast = lint.normalize_ast(cmd, recover_quotation, verbose=verbose)
    if ast is None:
        return paren_parser(cmd)
    else:
        return ast


def ast2tokens(node, loose_constraints=False, ignore_flag_order=False,
               arg_type_only=False, keep_common_args=False,
               with_arg_type=False, with_flag_head=False,
               with_flag_argtype=False, with_prefix=False,
               indexing_args=False):
    """
    Convert a bash ast into a list of tokens.

    :param loose_constraints: If set, do not check semantic coherence between
        flags and arguments.
    :param ignore_flag_order: If set, output flags in alphabetical order.
    :param arg_type_only: If set, output argument semantic types instead of the
        actual value.
    :param: keep_common_args: If set, keep common arguments such as "/", "."
        and do not replace them with semantic types. Effective only when
        arg_type_only is set.
    :param with_arg_type: If set, append argument type to argument token.
    :param with_flag_head: If set, add utility prefix to flag token.
    :param with_flag_argtype: If set, append argument type suffix to flag token.
    :param with_prefix: If set, add node kind prefix to token.
    :param indexing_args: If set, append order index to argument token.
    """
    if not node:
        return []

    lc = loose_constraints

    def to_tokens_fun(node):
        tokens = []
        if node.is_root():
            assert(loose_constraints or node.get_num_of_children() == 1)
            if lc:
                for child in node.children:
                    tokens += to_tokens_fun(child)
            else:
                tokens = to_tokens_fun(node.children[0])
        elif node.kind == "pipeline":
            assert(loose_constraints or node.get_num_of_children() > 1)
            if lc and node.get_num_of_children() < 1:
                tokens.append("|")
            elif lc and node.get_num_of_children() == 1:
                # treat "singleton-pipe" as atomic command
                tokens += to_tokens_fun(node.children[0])
            else:
                for child in node.children[:-1]:
                    tokens += to_tokens_fun(child)
                    tokens.append("|")
                tokens += to_tokens_fun(node.children[-1])
        elif node.kind == "commandsubstitution":
            assert(loose_constraints or node.get_num_of_children() == 1)
            if lc and node.get_num_of_children() < 1:
                tokens += ["$(", ")"]
            else:
                tokens.append("$(")
                tokens += to_tokens_fun(node.children[0])
                tokens.append(")")
        elif node.kind == "processsubstitution":
            assert(loose_constraints or node.get_num_of_children() == 1)
            if lc and node.get_num_of_children() < 1:
                tokens.append(node.value + "(")
                tokens.append(")")
            else:
                tokens.append(node.value + "(")
                tokens += to_tokens_fun(node.children[0])
                tokens.append(")")
        elif node.is_utility():
            token = node.value
            if with_prefix:
                token = node.prefix + token
            tokens.append(token)
            children = sorted(node.children, key=lambda x:x.value) \
                if ignore_flag_order else node.children
            for child in children:
                tokens += to_tokens_fun(child)
        elif node.is_option():
            assert(loose_constraints or node.parent)
            if '::' in node.value and (node.value.startswith('-exec') or 
                                       node.value.startswith('-ok')):
                value, op = node.value.split('::')
                token = value
            else:
                token = node.value
            if with_flag_head:
                if node.parent:
                    token = node.utility.value + "@@" + token
                else:
                    token = token
            if with_prefix:
                token = node.prefix + token
            if with_flag_argtype:
                suffix = ''
                if node.children:
                    for child in node.children:
                        if child.is_argument():
                            suffix += child.arg_type
                        elif child.is_utility():
                            suffix += 'UTILITY'
                token = token + flag_suffix + suffix
            tokens.append(token)
            for child in node.children:
                tokens += to_tokens_fun(child)
            if '::' in node.value and (node.value.startswith('-exec') or
                                       node.value.startswith('-ok')):
                if op == ';':
                    op = "\\;"
                tokens.append(op)
        elif node.kind == 'operator':
            tokens.append(node.value)
        elif node.kind == "binarylogicop":
            assert(loose_constraints or node.get_num_of_children() == 0)
            if lc and node.get_num_of_children() > 0:
                for child in node.children[:-1]:
                    tokens += to_tokens_fun(child)
                    tokens.append(node.value)
                tokens += to_tokens_fun(node.children[-1])
            else:
                tokens.append(node.value)
        elif node.kind == "unarylogicop":
            assert(loose_constraints or node.get_num_of_children() == 0)
            if lc and node.get_num_of_children() > 0:
                if node.associate == nast.UnaryLogicOpNode.RIGHT:
                    tokens.append(node.value)
                    tokens += to_tokens_fun(node.children[0])
                else:
                    tokens += to_tokens_fun(node.children[0])
                    tokens.append(node.value)
            else:
                tokens.append(node.value)
        elif node.kind == "bracket":
            assert(loose_constraints or node.get_num_of_children() >= 1)
            if lc and node.get_num_of_children() < 2:
                for child in node.children:
                    tokens += to_tokens_fun(child)
            else:
                tokens.append("\\(")
                for i in xrange(len(node.children)-1):
                    tokens += to_tokens_fun(node.children[i])
                tokens += to_tokens_fun(node.children[-1])
                tokens.append("\\)")
        elif node.kind == "nt":
            assert(loose_constraints or node.get_num_of_children() > 0)
            tokens.append("(")
            for child in node.children:
                tokens += to_tokens_fun(child)
            tokens.append(")")
        elif node.is_argument() or node.kind in ["t"]:
            assert(loose_constraints or node.get_num_of_children() == 0)
            if arg_type_only and node.is_open_vocab():
                if (keep_common_args and node.parent.is_utility() and
                    node.parent.value == 'find' and node.value in bash.find_common_args):
                    # keep frequently-occurred arguments in the vocabulary
                    # TODO: define the criteria for "common args"
                    token = node.value
                else:
                    if node.arg_type in bash.quantity_argument_types:
                        if node.value.startswith('+'):
                            token = '+{}'.format(node.arg_type)
                        elif node.value.startswith('-'):
                            token = '-{}'.format(node.arg_type)
                        else:
                            token = node.arg_type
                    else:
                        token = node.arg_type
            else:
                token = node.value
            if with_prefix:
                token = node.prefix + token
            if with_arg_type:
                token = token + "_" + node.arg_type
            if indexing_args and node.to_index():
                token = token + "-{:02d}".format(node.index)

            tokens.append(token)
            if lc:
                for child in node.children:
                    tokens += to_tokens_fun(child)
        return tokens

    return to_tokens_fun(node)


def ast2command(node, loose_constraints=False, ignore_flag_order=False):
    return lint.serialize_ast(node, loose_constraints=loose_constraints,
                              ignore_flag_order=ignore_flag_order)


def ast2template(node, loose_constraints=False, ignore_flag_order=False,
                 arg_type_only=True, indexing_args=False,
                 keep_common_args=False):
    """
    Convert a bash AST to a template that contains only reserved words and
    argument types flags are alphabetically ordered.
    """
    tokens = ast2tokens(node, loose_constraints, ignore_flag_order,
                        arg_type_only=arg_type_only, 
                        indexing_args=indexing_args,
                        keep_common_args=keep_common_args)
    return ' '.join(tokens)

def cmd2template(cmd, recover_quotation=True, arg_type_only=True,
                loose_constraints=False, verbose=False):
    """
    Convert a bash command to a template that contains only reserved words
    and argument types flags are alphabetically ordered.
    """
    tree = lint.normalize_ast(cmd, recover_quotation, verbose=verbose)
    return ast2template(tree, loose_constraints=loose_constraints, 
                        arg_type_only=arg_type_only)


def pretty_print(node, depth=0):
    """
    Pretty print the AST.
    """
    try:
        str = "    " * depth + node.kind.upper() + '(' + node.value + ')'
        if node.is_argument():
            str += '<' + node.arg_type + '>'
        print(str)
        for child in node.children:
            pretty_print(child, depth+1)
    except AttributeError:
        print("    " * depth)


def ast2list(node, order='dfs', _list=None, ignore_flag_order=False,
             arg_type_only=False, keep_common_args=False,
             with_flag_head=False, with_prefix=False):
    """
    Linearize the AST.
    """
    if order == 'dfs':
        if node.is_argument() and node.is_open_vocab() and arg_type_only:
            token = node.arg_type
        elif node.is_option() and with_flag_head:
            token = node.utility.value + '@@' + node.value if node.utility \
                else node.value
        else:
            token = node.value
        if with_prefix:
            token = node.prefix + token
        _list.append(token)
        if node.get_num_of_children() > 0:
            if node.is_utility() and ignore_flag_order:
                children = sorted(node.children, key=lambda x:x.value)
            else:
                children = node.children
            for child in children:
                ast2list(child, order, _list, ignore_flag_order, arg_type_only,
                         keep_common_args, with_flag_head, with_prefix)
            _list.append(nast._H_NO_EXPAND)
        else:
            _list.append(nast._V_NO_EXPAND)
    return _list


# --- Other syntax parsers --- #

def paren_parser(line):
    """A simple parser for parenthesized sequence."""
    def order_child_fun(node):
        for child in node.children:
            order_child_fun(child)
        if len(node.children) > 1 and node.children[0].value in ["and", "or"]:
            node.children = node.children[:1] + sorted(node.children[1:],
                    key=lambda x:(x.value if x.kind == "t" else (
                        x.children[0].value if x.children else x.value)))

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
            if stack:
                node = nast.Node(kind="t", value=word)
                stack[-1].add_child(node)
                node.parent = stack[-1]
        i += 1
        if len(stack) == 0:
            break

    # order nodes
    order_child_fun(root)

    return root

# --- Test functions --- #

def batch_parse(input_file):
    """
    Parse the input_file each line of which is a bash command.
    """
    with open(input_file) as f:
        i = 0
        for cmd in f:
            print("{}. {}".format(i, cmd))
            ast = bash_parser(cmd)
            pretty_print(ast)
            i += 1

def test_bash_parser():
    while True:
        try:
            cmd = input("> ")
            norm_tree = bash_parser(cmd)
            # pruned_tree = normalizer.prune_ast(norm_tree)
            print()
            print("AST:")
            pretty_print(norm_tree, 0)
            # print("Pruned AST:")
            # pretty_print(pruned_tree, 0)
            # search_history = ast2list(norm_tree, 'dfs', list=[])
            # for state in search_history:
            #     print(state)
            print(get_utilities(norm_tree))
            print("Command Template:")
            print(ast2template(norm_tree, ignore_flag_order=False))
            print("Command: ")
            print(ast2command(norm_tree, ignore_flag_order=False))
            # print("Pruned Command Template:")
            # print(ast2template(pruned_tree, ignore_flag_order=False))
            print()
        except EOFError as ex:
            break


def test_bash_tokenizer():

    def test(cmd):
        tokens = bash_tokenizer(cmd)
        print('cmd: {}'.format(cmd))
        print('tokens: {}'.format(tokens))

    cmd1 = 'find . -name "*.andnav" | rename -vn "s/\.andnav$/.tile/"'
    test(cmd1)
    cmd2 = 'find /volume1/uploads -name "*.mkv" -exec mv \{\} \{\}.avi \;'
    test(cmd2)
    cmd3 = 'touch -d "$(date -r filename) - 2 hours" filename'
    test(cmd3)


if __name__ == "__main__":
    # input_file = sys.argv[1]
    # batch_parse(input_file)
    # test_bash_parser()
    test_bash_tokenizer()
