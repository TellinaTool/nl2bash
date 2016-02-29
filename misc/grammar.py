#!/usr/bin/env python

from __future__ import print_function
import os
import glob
import json
import sys

class CommandGenerator(object):
    """Class to generate commands"""
    def pick_token(self, so_far, choices):
        return choices[0]
    def pick_arg(self, so_far):
        return "ARG"

class Grammar(object):
    EMPTY = 0
    CASES = 1
    SEQ   = 2
    EXACT = 3
    PERM  = 4
    HOLE  = 5

    def __init__(self, kind, *args):
        self.kind = kind
        self.args = args

class Enumerator(object):
    EOF = 0
    HOLE = 1

    def __init__(self, grammar, *args):
        if isinstance(grammar, Grammar):
            self.kind = grammar.kind
            self.arbitrary = False
            self.tok = None
            self.sub_enums = []
            if grammar.kind == Grammar.EMPTY:
                pass
            elif grammar.kind == Grammar.CASES:
                self.sub_enums = [Enumerator(g) for g in grammar.args]
            elif grammar.kind == Grammar.SEQ:
                self.sub_enums = [Enumerator(g) for g in grammar.args]
            elif grammar.kind == Grammar.PERM:
                self.sub_enums = [Enumerator(g) for g in grammar.args]
            elif grammar.kind == Grammar.EXACT:
                self.tok = grammar.args[0]
            elif grammar.kind == Grammar.HOLE:
                self.arbitrary = True
            else:
                raise Exception("unknown kind {}".format(grammar.kind))
        else:
            assert grammar in [Grammar.CASES, Grammar.SEQ, Grammar.PERM]
            self.kind = grammar
            self.sub_enums = args

    def __str__(self):
        if self.kind == Grammar.EMPTY:
            return "e"
        elif self.kind == Grammar.CASES:
            return "Cases({})".format(" | ".join(str(e) for e in self.sub_enums))
        elif self.kind == Grammar.SEQ:
            return " ".join(str(e) for e in self.sub_enums)
        elif self.kind == Grammar.PERM:
            return "Perm({})".format(", ".join(str(e) for e in self.sub_enums))
        elif self.kind == Grammar.EXACT:
            return repr(self.tok)
        elif self.kind == Grammar.HOLE:
            return "_"

    # alter state
    def push(self, token):
        assert token in self._legal_tokens(), "grammar {} cannot accept token {}".format(self, token)
        if self.kind == Grammar.EMPTY:
            pass
        elif self.kind == Grammar.CASES:
            self.sub_enums = [e for e in self.sub_enums if e.allows(token)]
            for e in self.sub_enums:
                e.push(token)
        elif self.kind == Grammar.SEQ:
            i = 0
            while True:
                if self.sub_enums[i].allows(token):
                    self.sub_enums[i].push(token)
                    break
                else:
                    assert self.sub_enums[i].allow_eof()
                    i += 1
            self.sub_enums = self.sub_enums[i:]
            if not self.sub_enums:
                self.kind = Grammar.EMPTY # consume this production
        elif self.kind == Grammar.PERM:
            pos = [e for e in self.sub_enums if e.allows(token)]
            neg = [e for e in self.sub_enums if not e.allows(token)]
            for e in pos:
                e.push(token)
            assert len(pos) > 0
            e1 = pos[0] if len(pos) == 1 else Enumerator(Grammar.PERM, *pos)
            e2 = Grammar.EMPTY if len(neg) == 0 else neg[0] if len(neg) == 1 else Enumerator(Grammar.PERM, *neg)
            self.kind = Grammar.SEQ
            self.sub_enums = [e1, e2]
        elif self.kind == Grammar.EXACT:
            self.kind = Grammar.EMPTY # consume this production
        elif self.kind == Grammar.HOLE:
            self.kind = Grammar.EMPTY # consume this production
        else:
            raise Exception("unknown kind {}".format(self.kind))

    # query state
    def allow_eof(self):
        return self.allows(Enumerator.EOF)
    def allow_arbitrary(self):
        return self.allows(Enumerator.HOLE)
    def allows(self, token):
        return token in self._legal_tokens()
    def _legal_tokens(self):
        if self.kind == Grammar.EMPTY:
            yield Enumerator.EOF
        elif self.kind in [Grammar.CASES, Grammar.PERM]:
            for enum in self.sub_enums:
                for tok in enum._legal_tokens():
                    yield tok
        elif self.kind == Grammar.SEQ:
            for enum in self.sub_enums:
                eof = False
                for tok in enum._legal_tokens():
                    if tok == Enumerator.EOF:
                        eof = True
                    else:
                        yield tok
                if not eof:
                    break
            if eof:
                yield Enumerator.EOF
        elif self.kind == Grammar.EXACT:
            yield self.tok
        elif self.kind == Grammar.HOLE:
            yield Enumerator.HOLE
        else:
            raise Exception("unknown kind {}".format(self.kind))
    def legal_tokens(self):
        return set(self._legal_tokens())

def make_grammar_from_options(x):
    if "type" in x:
        if x["type"] == "argument":
            return Grammar(Grammar.HOLE)
        elif x["type"] == "compound":
            return Grammar(Grammar.PERM, *[make_grammar_from_options(o) for o in x["cmds"]])
        elif x["type"] == "optional":
            return Grammar(Grammar.CASES, Grammar(Grammar.EMPTY), make_grammar_from_options(x["cmd"]))
        elif x["type"] == "eclusive": # sic
            return Grammar(Grammar.CASES, *[make_grammar_from_options(o) for o in x["cmds"]])
        else:
            raise Exception("unknown type: {}".format(x["type"]))
    else:
        return Grammar(Grammar.EXACT, "-" + x["flagName"])

def make_grammar_from_json_syntax(syntax):
    g = Grammar(Grammar.CASES, *[Grammar(Grammar.EXACT, alias) for alias in syntax["aliases"]])
    g = Grammar(Grammar.SEQ, g, *[make_grammar_from_options(x) for x in syntax["optionLists"]])
    return g

def load_syntax(root_dir):
    simple_cmds = []
    for jsonfile in glob.glob(os.path.join(root_dir, "*.json")):
        with open(jsonfile, "r") as f:
            syntax = json.loads(f.read())
        simple_cmds.append(make_grammar_from_json_syntax(syntax))
        print("loaded {}".format(syntax["name"]))
    return Grammar(Grammar.CASES, *simple_cmds)

def make_full_grammar(simple_grammar, max_pipeline_depth):
    pipe = Grammar(Grammar.EXACT, "|")
    def make_pipeline(g, n):
        return Grammar(Grammar.SEQ, g, *([Grammar(Grammar.SEQ, pipe, g)] * n))

    grammar = simple_grammar
    for n in range(max_pipeline_depth + 1):
        grammar = Grammar(Grammar.CASES, grammar, make_pipeline(simple_grammar, n))
    return grammar

if __name__ == "__main__":
    simple_grammar = load_syntax(os.path.join(os.path.dirname(__file__), "..", "data", "jsonman"))
    grammar = make_full_grammar(simple_grammar, max_pipeline_depth=3)

    e = Enumerator(grammar)
    while True:
        choices = list(e.legal_tokens())
        if Enumerator.HOLE in choices:
            choices.remove(Enumerator.HOLE)
            choices.append("*")
        if Enumerator.EOF in choices:
            choices.remove(Enumerator.EOF)
            choices.append("<EOF>")
        print("choices: {}".format(", ".join(choices)))
        try:
            inp = raw_input("> ")
            if inp == "*":
                inp = Enumerator.HOLE
            e.push(inp)
        except EOFError as ex:
            break
    e.push(Enumerator.EOF)
