"""
Split the dataset into train, dev and test randomly according to the given 
ratio.

Usage: python3 split_data.py [data_directory]
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json
import random
import re
import os, sys

from src.data_processor.data_loader import save_data_split
from src.nlp_tools import canonicalize_text

html_rel2abs = re.compile('"/[^\s<>]*/*http')
hypothes_header = re.compile(
    '\<\!\-\- WB Insert \-\-\>.*\<\!\-\- End WB Insert \-\-\>', re.DOTALL)

RANDOM_SEED = 100


def split_data(data_dir):
    nl_file_path = os.path.join(data_dir, 'all.nl.filtered')
    cm_file_path = os.path.join(data_dir, 'all.cm.filtered')
    with open(nl_file_path, encoding='utf-8') as f:
        nls = [line.strip() for line in f.readlines()]
    with open(cm_file_path, encoding='utf-8') as f:
        cms = [line.strip() for line in f.readlines()]
    assert(len(nls) == len(cms))

    pairs = collections.defaultdict(list)
    for nl, cm in zip(nls, cms):
        nl_temp = canonicalize_text(nl)
        pairs[nl_temp].append((nl, cm))

    train, dev, test = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
    num_folds = 12
    num_train, num_dev, num_test = 0, 0, 0

    # randomly split data according to ratio
    random.seed(RANDOM_SEED)
    random_tokens = [random.randint(0, num_folds-1) for i in range(len(pairs.keys()))]
    with open(os.path.join(data_dir, 'random_tokens.txt'), 'w') as o_f:
        for r_token in random_tokens:
            o_f.write('{}\n'.format(r_token))

    train_commands = set()
    for i, nl_temp in enumerate(sorted(pairs.keys())):
        ind = random_tokens[i]
        if ind < num_folds - 2:
            train[nl_temp] = pairs[nl_temp]
            num_train += 1
            for _, cm in pairs[nl_temp]:
                train_commands.add(cm)
        elif ind == num_folds - 2:
            dev[nl_temp] = pairs[nl_temp]
            num_dev += 1
        elif ind == num_folds - 1:
            test[nl_temp] = pairs[nl_temp]
            num_test += 1
    print('First round split:')
    print('train - {} pairs, dev - {} pairs, test - {} pairs'.format(
        len(train), len(dev), len(test)))

    # move dev/test examples whose command has appeared in the train set to 
    # train
    dev_cleaned = collections.defaultdict(list)
    num_moved = 0
    for nl_temp in dev:
        for nl, cm in dev[nl_temp]:
            if cm in train_commands:
                train[nl_temp].append((nl, cm))
                num_moved += 1
            else:
                dev_cleaned[nl_temp].append((nl, cm))
    print('{} pairs moved from dev to train'.format(num_moved))

    test_cleaned = collections.defaultdict(list)
    num_moved = 0
    for nl_temp in test:
        for nl, cm in test[nl_temp]:
            if cm in train_commands:
                train[nl_temp].append((nl, cm))
                num_moved += 1
            else:
                test_cleaned[nl_temp].append((nl, cm))
    print('{} pairs moved from test to train'.format(num_moved))
    print('Second round split:')
    print('train - {} pairs, dev - {} pairs, test - {} pairs'.format(
        len(train), len(dev_cleaned), len(test_cleaned)))

    save_data_split(train, os.path.join(data_dir, "train.filtered.json"))
    save_data_split(dev_cleaned, os.path.join(data_dir, "dev.filtered.json"))
    save_data_split(test_cleaned, os.path.join(data_dir, "test.filtered.json"))


if __name__ == '__main__':
    dataset = sys.argv[1]
    data_dir = os.path.join(os.path.dirname(
        os.path.realpath(os.path.dirname(__file__))), dataset)
    split_data(data_dir)
