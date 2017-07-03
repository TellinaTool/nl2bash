#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Consume tokens in a bash command and tract the next possible states.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json
import os

__FLAG_S__ = 0
__COMMAND_S__ = 1
__EXEC_COMMAND_S__ = 2
__ARG_S__ = 3


class BashGrammarState(object):
    def __init__(self, type):
        self.type = type

    def is_flag(self):
        return self.type == __FLAG_S__

    def is_command(self):
        return

class BashGrammar(object):
    def consume(self, token, state_type):

