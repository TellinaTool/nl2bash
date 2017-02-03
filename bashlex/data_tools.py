#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Domain-specific natural Language and bash command tokenizer."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from bashlex import bash, nast, normalizer
from nlp_tools import constants


def is_simple(ast):
    # Check if tree contains only high-frequency commands
    if ast.kind == "headcommand" and not ast.value in bash.head_commands:
        return False
    for child in ast.children:
        if not is_simple(child):
            return False
    return True


def char_tokenizer(sentence, base_tokenizer=None):
    if base_tokenizer:
        # normalization is not needed for character model
        tokens = base_tokenizer(sentence)
    else:
        tokens = [sentence]
    chars = []
    for token in tokens:
        for c in token:
            chars.append(c)
        chars.append(constants._SPACE)
    return chars[:-1]


def bash_tokenizer(cmd, recover_quotation=True, loose_constraints=False,
        ignore_flag_order=False, arg_type_only=False, with_parent=False):
    """Tokenize a bash command."""
    tree = normalizer.normalize_ast(cmd, recover_quotation)
    return normalizer.to_tokens(tree, loose_constraints, ignore_flag_order,
                                arg_type_only, with_parent=with_parent)


def bash_parser(cmd, recover_quotation=True):
    """Parse bash command into AST."""
    return normalizer.normalize_ast(cmd, recover_quotation)


def pretty_print(node, depth=0):
    """Pretty print the AST."""
    try:
        str = "    " * depth + node.kind.upper() + '(' + node.value + ')'
        if node.is_argument():
            str += '<' + node.arg_type + '>'
        print(str)
        for child in node.children:
            pretty_print(child, depth+1)
    except AttributeError:
        print("    " * depth)


def ast2tokens(node, loose_constraints=False, ignore_flag_order=False,
               arg_type_only=False, with_parent=False):
    """Convert a bash ast into a list of tokens."""
    return normalizer.to_tokens(node, loose_constraints, ignore_flag_order,
                                arg_type_only, with_parent=with_parent)


def ast2command(node, loose_constraints=False, ignore_flag_order=False):
    return normalizer.to_command(node, loose_constraints, ignore_flag_order)


def ast2template(node, loose_constraints=False, ignore_flag_order=True,
                 arg_type_only=True):
    # convert a bash AST to a template that contains only reserved words and
    # argument types flags are alphabetically ordered
    tokens = normalizer.to_tokens(node, loose_constraints, ignore_flag_order,
                                  arg_type_only=arg_type_only, index_arg=True)
    return ' '.join(tokens) 


def cmd2template(cmd, recover_quotation=True, arg_type_only=True,
                loose_constraints=False):
    # convert a bash command to a template that contains only reserved words
    # and argument types flags are alphabetically ordered
    tree = normalizer.normalize_ast(cmd, recover_quotation)
    return ast2template(tree, loose_constraints, arg_type_only)


def ast2list(node, order='dfs', list=None, ignore_flag_order=False,
             arg_type_only=False, with_parent=False):
    """Linearize the AST."""
    if order == 'dfs':
        if arg_type_only and node.is_argument() and node.is_open_vocab():
            # print(node.headcommand.value)
            # print(node.parent.value)
            # print(node.value)
            # print(node.arg_type)
            list.append(node.prefix + node.arg_type)
        else:
            if node.is_option() and with_parent and node.headcommand:
                list.append(
                    node.prefix + node.headcommand.value + "@@" + node.value)
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


def paren_parser(line):
    def order_child_fun(node):
        for child in node.children:
            order_child_fun(child)
        if len(node.children) > 1 and node.children[0].value in ["and", "or"]:
            node.children = node.children[:1] + sorted(node.children[1:],
                    key=lambda x:(x.value if x.kind == "t" else (
                        x.children[0].value if x.children else x.value)))

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
            break

    # order nodes
    order_child_fun(root)

    return root


def fill_default_value(node):
    """
    Fill empty slot in the bash ast with default value.
    """
    if node.is_argument():
        if node.arg_type in constants._ENTITIES:
            if node.arg_type == 'Path' and node.parent.is_headcommand() \
                    and node.parent.value == 'find':
                node.value = '.'
            elif node.arg_type == 'Regex':
                node.value = '\'*\''
            else:
                node.arg_type = '[' + node.arg_type.lower() + ']'


def test_bash_parser():
    while True:
        try:
            cmd = raw_input("> ")
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
            print("Command Template:")
            print(ast2template(norm_tree, ignore_flag_order=False))
            print("Command: ")
            print(ast2command(norm_tree, ignore_flag_order=False))
            # print("Pruned Command Template:")
            # print(ast2template(pruned_tree, ignore_flag_order=False))
            print()
        except EOFError as ex:
            break


if __name__ == "__main__":
    test_bash_parser()
