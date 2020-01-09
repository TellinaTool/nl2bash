#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.

from __future__ import absolute_import
from __future__ import print_function

import os
from random import seed

from zss.compare import (
    simple_distance,
    distance,
    strdist,
    Node,
)


seed(os.urandom(15))


def test_empty_tree_distance():
    assert simple_distance(Node(''), Node('')) == 0
    assert simple_distance(Node('a'), Node('')) == 1
    assert simple_distance(Node(''), Node('b')) == 1


def test_paper_tree():
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
    dist = simple_distance(A,B)
    assert dist == 2


def test_simplelabelchange():
    A = (
        Node("f")
            .addkid(Node("a")
                .addkid(Node("h"))
                .addkid(Node("c")
                    .addkid(Node("l"))))
            .addkid(Node("e"))
        )
    B = (
        Node("f")
            .addkid(Node("a")
                .addkid(Node("d"))
                .addkid(Node("r")
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )
    dist = simple_distance(A,B)
    print(dist)
    assert dist == 3
    #print 'distance', d


def test_incorrect_behavior_regression():
    A = (
     Node("a")
       .addkid(Node("b")
         .addkid(Node("x"))
         .addkid(Node("y"))
       )
     )
    B = (
     Node("a")
       .addkid(Node("x"))
       .addkid(Node("b")
         .addkid(Node("y"))
       )
     )
    dist = simple_distance(A, B)
    print(dist)
    assert dist == 2

def test_dict():
    A = {
        'name': 'tree', 
        'children': [
            {
                'name': 'child 1'
            },
            {
                'name': 'child 2'  
            }
            ]}
    B = {
        'name': 'tree', 
        'children': [
            {
                'name': 'child 1'
            },
            {
                'name': 'child Z'  
            }
            ]}
    dist = simple_distance(
        A,
        B,
        get_children=lambda x: x['children'] if 'children' in x else [],
        get_label=lambda x: x['name'],
        label_dist=lambda x,y: 1 if x!=y else 0
    )
    assert dist == 1

def test_wrong_index_regression():
    A = Node('r')
    B = (
        Node("a")
          .addkid(Node("b")
            .addkid(Node("c"))
            .addkid(Node("d"))
          )
          .addkid(Node("e")
            .addkid(Node("f"))
            .addkid(Node("g"))
          )
     )
    def insert(n):
        return ord(n.label[0])
    def remove(n):
        return ord(n.label[0])
    def update(a,b):
        return 10000*strdist(a.label, b.label)
    dist = distance(A, B,
        get_children=(lambda n: n.children),
        insert_cost=insert,
        remove_cost=remove,
        update_cost=update,
    )
    assert dist == 814

