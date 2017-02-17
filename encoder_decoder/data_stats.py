from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .data_utils import *

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

def data_stats(FLAGS):
    train_set, dev_set, test_set = load_data(FLAGS)
    train_by_nl = group_data_by_nl(train_set, use_temp=FLAGS.dataset.startswith("bash"))
    print(len(train_by_nl))
    print("train cmd/nl ratio = {}".format(ratio(train_by_nl, 1)))
    print("train %nl(cmd+) = {}".format(pp(train_by_nl)))
    print("train entropy = {}".format(entropy(train_set)))
    dev_by_nl = group_data_by_nl(dev_set, use_temp=FLAGS.dataset.startswith("bash"))
    print("dev cmd/nl ratio = {}".format(ratio(dev_by_nl, 1)))
    print("dev %nl(cmd+) = {}".format(pp(dev_by_nl)))
    print("dev nl overlap = {}".format(overlap(train_by_nl, dev_by_nl)))
    print("dev entropy = {}".format(entropy(dev_set)))
    test_by_nl = group_data_by_nl(test_set, use_temp=FLAGS.dataset.startswith("bash"))
    print("test cmd/nl ratio = {}".format(ratio(test_by_nl, 1)))
    print("test %nl(cmd+) = {}".format(pp(test_by_nl)))
    print("test nl overlap = {}".format(overlap(train_by_nl, test_by_nl)))
    print("test entropy = {}".format(entropy(test_set)))
    print("total entropy = {}".format(entropy(train_set + dev_set + test_set)))
    train_by_cm = group_data_by_cm(train_set, use_temp=FLAGS.dataset.startswith("bash"))
    print(len(train_by_cm))
    print("train nl/cmd ratio = {}".format(ratio(train_by_cm, 0)))
    print("train %cmd(nl+) = {}".format(pp(train_by_cm)))
    dev_by_cm = group_data_by_cm(dev_set, use_temp=FLAGS.dataset.startswith("bash"))
    print("dev nl/cmd ratio = {}".format(ratio(dev_by_cm, 0)))
    print("dev %cmd(nl+) = {}".format(pp(dev_by_cm)))
    print("dev cm overlap = {}".format(overlap(train_by_cm, dev_by_cm)))
    test_by_cm = group_data_by_cm(test_set, use_temp=FLAGS.dataset.startswith("bash"))
    print("test nl/cmd ratio = {}".format(ratio(test_by_cm, 0)))
    print("test %cmd(nl+) = {}".format(pp(test_by_cm)))
    print("test cm overlap = {}".format(overlap(train_by_cm, test_by_cm)))

