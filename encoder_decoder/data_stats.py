from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from encoder_decoder.data_utils import *

def ratio(ll, x):
    print(sum([len(l[x]) for l in ll.values()]))
    return float(sum([len(set(l[x])) for l in ll.values()])) / len(ll)

def pp(ll):
    num_pp = 0
    for l in ll.values():
        if len(set(l[1])) > 1:
            num_pp += 1
    return float(num_pp) / len(ll)

def overlap(dict1, dict2):
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())
    return float(len(keys1 & keys2)) / len(keys2)

def entropy(data):
    keys = [x[0] for x in data]
    counts = collections.Counter(keys)
    ent = 0
    for w, c in counts.items():
        p = float(c) / len(keys)
        ent += -p * np.log(p)
    return ent
