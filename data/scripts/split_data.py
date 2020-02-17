"""
Split the dataset into train, dev and test randomly according to the given 
ratio.

Usage: python3 split_data.py [data_directory]
"""

import collections
import random
import re
import os, sys
sys.path.append("..")
sys.path.append("../../")
sys.path.append("../../bashlint")

from nlp_tools.tokenizer import basic_tokenizer, ner_tokenizer

html_rel2abs = re.compile('"/[^\s<>]*/*http')
hypothes_header = re.compile(
    '\<\!\-\- WB Insert \-\-\>.*\<\!\-\- End WB Insert \-\-\>', re.DOTALL)

RANDOM_SEED = 100

nl_suffix, cm_suffix = 'nl.filtered', 'cm.filtered'

def get_nl_temp(nl):
    return ' '.join(basic_tokenizer(nl)[0])


def split_data(data_dir):
    def write_data(data_path, data):
        with open(data_path, 'w', encoding='utf-8') as o_f:
            for line in data:
                o_f.write(line + '\n')
            print('{} saved'.format(data_path))

    nl_file_path = os.path.join(data_dir, 'all.{}'.format(nl_suffix))
    cm_file_path = os.path.join(data_dir, 'all.{}'.format(cm_suffix))

    with open(nl_file_path, encoding='utf-8') as f:
        nls = [line.strip() for line in f.readlines()]
    with open(cm_file_path, encoding='utf-8') as f:
        cms = [line.strip() for line in f.readlines()]

    assert(len(nls) == len(cms))

    pairs = collections.defaultdict(list)

    for nl, cm in zip(nls, cms):
        nl_temp = get_nl_temp(nl)
        pairs[nl_temp].append((nl, cm))

    train_nl_list = []
    train_cm_list = []
    dev_nl_list = []
    dev_cm_list = []
    test_nl_list = []
    test_cm_list = []

    num_folds = 12
    num_train = 0
    num_dev = 0
    num_test = 0

    # randomly split data according to ratio
    random.seed(RANDOM_SEED)
    train_commands = set()
    count = 0
    random_tokens = [random.randint(0, num_folds-1) for i in range(len(pairs.keys()))] 
    with open(os.path.join(data_dir, 'random_tokens.txt'), 'w') as o_f:
        for r_token in random_tokens:
            o_f.write('{}\n'.format(r_token))

    for i, nl_temp in enumerate(sorted(pairs.keys())):
        ind = random_tokens[i]
        if ind < num_folds - 2:
            num_train += 1
            for nl, cm in pairs[nl_temp]:
                train_nl_list.append(nl)
                train_cm_list.append(cm)
                train_commands.add(cm)
        elif ind == num_folds - 2:
            num_dev += 1
            for nl, cm in pairs[nl_temp]:
                dev_nl_list.append(nl)
                dev_cm_list.append(cm)
        elif ind == num_folds - 1:
            num_test += 1
            for nl, cm in pairs[nl_temp]:
                test_nl_list.append(nl)
                test_cm_list.append(cm)
        count += 1
    print(len(train_nl_list), len(dev_nl_list), len(test_nl_list))

    # move dev/test examples whose command has appeared in the train set to 
    # train
    dev_nl_list_cleaned = []
    dev_cm_list_cleaned = []
    num_moved = 0
    for nl, cm in zip(dev_nl_list, dev_cm_list):
        if cm in train_commands:
            train_nl_list.append(nl)
            train_cm_list.append(cm)
            num_moved += 1
        else:
            dev_nl_list_cleaned.append(nl)
            dev_cm_list_cleaned.append(cm)
    print('{} pairs moved from dev to train'.format(num_moved))

    test_nl_list_cleaned = []
    test_cm_list_cleaned = []
    num_moved = 0
    for nl, cm in zip(test_nl_list, test_cm_list):
        if cm in train_commands:
            train_nl_list.append(nl)
            train_cm_list.append(cm)
            num_moved += 1
        else:
            test_nl_list_cleaned.append(nl)
            test_cm_list_cleaned.append(cm)
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
    
    train_path = os.path.join(data_dir, "train")
    dev_path = os.path.join(data_dir, "dev")
    test_path = os.path.join(data_dir, "test")
    write_data(train_path + '.' + nl_suffix, train_nl_list)
    write_data(train_path + '.' + cm_suffix, train_cm_list)
    write_data(dev_path + '.' + nl_suffix, dev_nl_list_cleaned)
    write_data(dev_path + '.' + cm_suffix, dev_cm_list_cleaned)
    write_data(test_path + '.' + nl_suffix, test_nl_list_cleaned)
    write_data(test_path + '.' + cm_suffix, test_cm_list_cleaned)


if __name__ == '__main__':
    dataset = sys.argv[1]
    data_dir = os.path.join(os.path.dirname(
        os.path.realpath(os.path.dirname(__file__))), dataset)
    split_data(data_dir)
