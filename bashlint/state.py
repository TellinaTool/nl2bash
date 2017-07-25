from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from bashlint import flags, butils

parserstate = lambda: butils.typedset(flags.parser)
