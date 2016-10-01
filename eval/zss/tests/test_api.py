#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.

from __future__ import absolute_import

from zss import (
    distance,
    simple_distance,
    Node,
)


try:
    from editdist import distance as strdist
except ImportError:
    def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1

def weird_dist(A, B):
    return 10 * strdist(A, B)

class WeirdNode(object):

    def __init__(self, label):
        self.my_label = label
        self.my_children = list()

    @staticmethod
    def get_children(node):
        return node.my_children

    @staticmethod
    def get_label(node):
        return node.my_label

    def addkid(self, node, before=False):
        if before:  self.my_children.insert(0, node)
        else:   self.my_children.append(node)
        return self


def test_paper_tree():
    Node = WeirdNode
    A = (
      Node("f")
        .addkid(Node("d")
          .addkid(Node("a"))
          .addkid(Node("c")
            .addkid(Node("b"))
          )
        )
        .addkid(Node("e"))
    )
    B = (
      Node("f")
        .addkid(Node("c")
          .addkid(Node("d")
            .addkid(Node("a"))
            .addkid(Node("b"))
          )
        )
        .addkid(Node("e"))
    )
    #print A
    #print
    #print B
    dist = simple_distance(A, B, WeirdNode.get_children, WeirdNode.get_label,
        weird_dist)
    assert dist == 20


def test_rich_api():
    insert_cost = lambda node: 1
    remove_cost = lambda node: 1
    small_update_cost = lambda a, b: 1
    large_update_cost = lambda a, b: 3
    no_insert_cost = lambda node: 0

    A = Node('a')
    B = Node('b')
    # prefer update
    assert distance(
        A, B, Node.get_children, insert_cost, remove_cost,
        small_update_cost) == 1
    # prefer insert/remove
    assert distance(
        A, B, Node.get_children, insert_cost, remove_cost,
        large_update_cost) == 2

    C = Node('a', [Node('x')])
    assert (
        distance(
            A, C, Node.get_children, insert_cost, remove_cost,
            small_update_cost) >
        distance(
            A, C, Node.get_children, no_insert_cost, remove_cost,
            small_update_cost)
    )
