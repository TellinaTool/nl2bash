from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from src.bashlint import flags
from src.bashlint import butils

parserstate = lambda: butils.typedset(flags.parser)
