#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Authors: Tim Henderson and Steve Johnson
#Email: tim.tadh@gmail.com, steve@steveasleep.com
#For licensing see the LICENSE file in the top level directory.

from __future__ import absolute_import

from zss import (
    compare,
    Node,
)


def simple_trees():
    A = (
        Node("f")
            .addkid(Node("d")
                .addkid(Node("a"))
                .addkid(Node("c")
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )
    B = (
        Node("f")
            .addkid(Node("c")
                .addkid(Node("d")
                    .addkid(Node("a"))
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )
    return A, B

def test_nodes():
    A, B = [compare.AnnotatedTree(t, t.get_children) for t in simple_trees()]
    for i, nid in enumerate(reversed(A.ids)):
        assert nid == i
    for i, nid in enumerate(reversed(B.ids)):
        assert nid == i

def test_left_most_descendent():
    A, B = [compare.AnnotatedTree(t, t.get_children) for t in simple_trees()]
    assert A.lmds[0] == 0
    assert A.lmds[1] == 1
    assert A.lmds[2] == 1
    assert A.lmds[3] == 0
    assert A.lmds[4] == 4
    assert A.lmds[5] == 0

    assert B.lmds[0] == 0
    assert B.lmds[1] == 1
    assert B.lmds[2] == 0
    assert B.lmds[3] == 0
    assert B.lmds[4] == 4
    assert B.lmds[5] == 0

def test_keyroots():
    A, B = [compare.AnnotatedTree(t, t.get_children) for t in simple_trees()]
    assert A.keyroots == [2, 4, 5]
    assert B.keyroots == [1, 4, 5]
