#!/usr/bin/env python

from __future__ import print_function
import collections
import os
import json
import sys

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

class EnumeratorState(object):
    @staticmethod
    def from_grammar(grammar):
        if grammar.kind == Grammar.EMPTY:
            return EnumeratorState(Grammar.EMPTY)
        elif grammar.kind in [Grammar.CASES, Grammar.SEQ, Grammar.PERM]:
            return EnumeratorState(grammar.kind, [EnumeratorState.from_grammar(g)
                                                  for g in grammar.args])
        elif grammar.kind == Grammar.EXACT:
            return EnumeratorState(Grammar.EXACT, tok=grammar.args[0])
        elif grammar.kind == Grammar.HOLE:
            return EnumeratorState(Grammar.HOLE)
        else:
            raise Exception("unknown kind {}".format(grammar.kind))

    def __init__(self, kind, sub_states=None, tok=None):
        self.kind = kind
        self.sub_states = sub_states or []
        self.tok = tok

    def __str__(self):
        if self.kind == Grammar.EMPTY:
            return "e"
        elif self.kind == Grammar.CASES:
            return "Cases({})".format(" | ".join(str(e) for e in self.sub_states))
        elif self.kind == Grammar.SEQ:
            return " ".join(str(e) for e in self.sub_states)
        elif self.kind == Grammar.PERM:
            return "Perm({})".format(", ".join(str(e) for e in self.sub_states))
        elif self.kind == Grammar.EXACT:
            return repr(self.tok)
        elif self.kind == Grammar.HOLE:
            return "_"

    # token -> EnumeratorState
    def push(self, token):
        assert token in self._legal_tokens(), "grammar {} cannot accept token {}".format(self, token)
        if self.kind == Grammar.EMPTY:
            return self
        elif self.kind == Grammar.CASES:
            return EnumeratorState(Grammar.CASES, [e.push(token) for e in self.sub_states if e.allows(token)])
        elif self.kind == Grammar.SEQ:
            i = 0
            new_state = None
            while True:
                if self.sub_states[i].allows(token):
                    new_state = self.sub_states[i].push(token)
                    break
                else:
                    assert self.sub_states[i].allow_eof()
                    i += 1
            if new_state:
                return EnumeratorState(Grammar.SEQ, [new_state] + self.sub_states[i+1:])
            else:
                return EnumeratorState(Grammar.EMPTY, [])
        elif self.kind == Grammar.PERM:
            pos = [e.push(token) for e in self.sub_states if e.allows(token)]
            neg = [e for e in self.sub_states if not e.allows(token)]
            assert len(pos) > 0
            e1 = pos[0] if len(pos) == 1 else EnumeratorState(Grammar.PERM, pos)
            e2 = EnumeratorState(Grammar.EMPTY) if len(neg) == 0 else neg[0] if len(neg) == 1 else EnumeratorState(Grammar.PERM, neg)
            return EnumeratorState(Grammar.SEQ, [e1, e2])
        elif self.kind == Grammar.EXACT:
            return EnumeratorState(Grammar.EMPTY) # consume this production
        elif self.kind == Grammar.HOLE:
            return EnumeratorState(Grammar.EMPTY) # consume this production
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
            for enum in self.sub_states:
                for tok in enum._legal_tokens():
                    yield tok
        elif self.kind == Grammar.SEQ:
            for enum in self.sub_states:
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

class Enumerator(object):
    EOF = 0
    HOLE = 1

    def __init__(self, arg):
        if isinstance(arg, Grammar):
            self.state_stack = [EnumeratorState.from_grammar(arg)]
        elif isinstance(arg, list):
            self.state_stack = list(arg)
        else:
            raise Exception("cannot make enumerator of {}".format(arg))

    def __str__(self):
        return str(self.state_stack[-1])

    # alter state
    def push(self, token):
        self.state_stack.append(self.state_stack[-1].push(token))
    def pop(self):
        assert len(self.state_stack) > 1, "cannot pop() this enumerator"
        del self.state_stack[-1]
    def reset(self):
        self.state_stack = [self.state_stack[0]]

    # make a fresh copy of this enumerator
    def copy(self):
        return Enumerator(self.state_stack)

    # query state
    def allow_eof(self):
        return self.state_stack[-1].allow_eof()
    def allow_arbitrary(self):
        return self.state_stack[-1].allow_arbitrary()
    def allows(self, token):
        return self.state_stack[-1].allows(token)
    def legal_tokens(self):
        return self.state_stack[-1].legal_tokens()

def make_grammar_from_options(x, seen=None):
    if seen is None:
        seen = set()
    if x["type"] == "compound_options":
        return Grammar(Grammar.SEQ, *[make_grammar_from_options(o, seen=seen) for o in x["commands"]])
    elif x["type"] == "optional_option":
        flag_name = None
        if x["cmd"]["type"] == "flag_option":
            flag_name = x["cmd"]["flag_name"]
        elif x["cmd"]["type"] == "compound_options" and x["cmd"]["commands"][0]["type"] == "flag_option":
            flag_name = x["cmd"]["commands"][0]["flag_name"]
        if flag_name is not None and flag_name in seen:
            print("skipping duplicate flag -{}".format(flag_name), file=sys.stderr)
            return Grammar(Grammar.EMPTY)
        return Grammar(Grammar.CASES, Grammar(Grammar.EMPTY), make_grammar_from_options(x["cmd"], seen=seen))
    elif x["type"] == "exclusive_options":
        return Grammar(Grammar.CASES, *[make_grammar_from_options(o, seen=set(seen)) for o in x["commands"]])
    elif x["type"] == "flag_option":
        seen.add(x["flag_name"])
        g = Grammar(Grammar.EXACT, "-" + x["flag_name"])
    elif x["type"] == "long_flag_option":
        g = Grammar(Grammar.EXACT, "--" + x["flag_name"])
    elif x["type"] == "argument_option":
        return Grammar(Grammar.HOLE) # TODO: record type, description, etc...
    else:
        raise Exception("unknown type: {}".format(x["type"]))

    # has arg?
    if "arg_exists" in x and x["arg_exists"]:
        g = Grammar(Grammar.SEQ, g, make_grammar_from_options(x["argument"], seen=seen))
    return g

def make_grammar_from_json_syntax(syntax):
    g = Grammar(Grammar.EXACT, syntax["name"])
    g = Grammar(Grammar.SEQ, g, make_grammar_from_options(syntax["option"]))
    return g

def load_syntax(json_files):
    simple_cmds = []
    counts = collections.defaultdict(int)
    for jsonfile in json_files:
        print("loading from {}".format(jsonfile))
        with open(jsonfile, "r") as f:
            syntax = json.loads(f.read())
        for cmd in syntax:
            simple_cmds.append(make_grammar_from_json_syntax(cmd))
            counts[cmd["name"]] += 1
            print(" --> loaded {} ({})".format(cmd["name"], counts[cmd["name"]]))
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
    simple_grammar = load_syntax([os.path.join(os.path.dirname(__file__), "primitive_cmds_grammar.json")])
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
            if inp == "$":
                print(e)
                continue
            if inp == "*":
                inp = Enumerator.HOLE
            e.push(inp)
        except EOFError as ex:
            break
    e.push(Enumerator.EOF)
