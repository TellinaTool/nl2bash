"""Python wrapper for deciding DFA equivalence."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import argparse
import subprocess

def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--gold', help="gold", 
                          type=str, default="None")
    parser.add_argument('--predicted', help="predicted", 
                          type=str, default="None")
    args = parser.parse_args(arguments)
    if args.gold == args.predicted:
        print(1)
        return 0
    gold = unprocess_regex(args.gold)
    predicted = unprocess_regex(args.predicted)
    
    if regex_equiv(gold, predicted):
        print(1)
    else:
        print(0)

def unprocess_regex(regex):
    regex = regex.replace("<VOW>", " ".join('AEIOUaeiou'))
    regex = regex.replace("<NUM>", " ".join('0-9'))
    regex = regex.replace("<LET>", " ".join('A-Za-z'))
    regex = regex.replace("<CAP>", " ".join('A-Z'))
    regex = regex.replace("<LOW>", " ".join('a-z'))

    regex = regex.replace("<M0>", " ".join('dog'))
    regex = regex.replace("<M1>", " ".join('truck'))
    regex = regex.replace("<M2>", " ".join('ring'))
    regex = regex.replace("<M3>", " ".join('lake'))

    regex = regex.replace(" ", "")

    return regex

def regex_equiv(gold, predicted):
    if gold == predicted:
        return True
    try:
        out = subprocess.check_output(['java', '-jar', 
            '{}/regex_dfa_equals.jar'.format(os.path.dirname(__file__)),
            '{}'.format(gold), '{}'.format(predicted)])
        if '\\n1' in str(out):
            return True
        else:
            return False
    except Exception as e:
        return False
    return False

def regex_equiv_from_raw(gold, predicted):
    gold = unprocess_regex(gold)
    predicted = unprocess_regex(predicted)
    return regex_equiv(gold, predicted)

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
