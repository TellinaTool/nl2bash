"""
Split the dataset into train, dev and test randomly according to the given 
ratio.

Usage: python3 split_data.py [data_directory]
"""

import collections
import json
import random
import re
import os, sys

from data_processor.data_utils import DataSet, ExampleGroup, Example
from nlp_tools import canonicalize_text

html_rel2abs = re.compile('"/[^\s<>]*/*http')
hypothes_header = re.compile(
    '\<\!\-\- WB Insert \-\-\>.*\<\!\-\- End WB Insert \-\-\>', re.DOTALL)

RANDOM_SEED = 100


def split_data(data_dir):
    nl_file_path = os.path.join(data_dir, 'all.nl.filtered')
    cm_file_path = os.path.join(data_dir, 'all.cm.filtered')
    with open(nl_file_path) as f:
        nls = [line.strip() for line in f.readlines()]
    with open(cm_file_path) as f:
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
                test[nl_temp].append((nl, cm))
    print('{} pairs moved from test to train'.format(num_moved))

    # select 100 examples as dev
    # dev_nl_list_reorg = []
    # dev_cm_list_reorg = []
    # indices = list(range(len(dev_nl_list_cleaned)))
    # random.seed(RANDOM_SEED)
    # random.shuffle(indices)
    # dev_nl_temps = set()
    # for count, dev_ind in enumerate(indices):
    #     dev_nl_temps.add(get_nl_temp(dev_nl_list_cleaned[dev_ind]))
    #     dev_nl_list_reorg.append(dev_nl_list_cleaned[dev_ind])
    #     dev_cm_list_reorg.append(dev_cm_list_cleaned[dev_ind])
    #     if len(dev_nl_temps) == 100:
    #         break
    # 
    # test_nl_list_reorg = test_nl_list_cleaned
    # test_cm_list_reorg = test_cm_list_cleaned
    # for i in indices[count+1:]:
    #     test_nl_list_reorg.append(dev_nl_list_cleaned[i])
    #     test_cm_list_reorg.append(dev_cm_list_cleaned[i])

    def save_data_split(data_split, out_json):
        dataset = DataSet()
        for nl_temp in data_split:
            example_group = ExampleGroup(nl_temp)
            for nl, cm in data_split[nl_temp]:
                example = Example(nl, cm)
                example_group.add_example(example)
            dataset.add_example(example_group)
        with open(out_json, 'w') as o_f:
            json.dump(dataset.__dict__, o_f, indent=4)

    save_data_split(train, os.path.join(data_dir, "train.filtered.json"))
    save_data_split(dev_cleaned, os.path.join(data_dir, "dev.filtered.json"))
    save_data_split(test_cleaned, os.path.join(data_dir, "test.filtered.json"))


if __name__ == '__main__':
    dataset = sys.argv[1]
    data_dir = os.path.join(os.path.dirname(
        os.path.realpath(os.path.dirname(__file__))), dataset)
    split_data(data_dir)
