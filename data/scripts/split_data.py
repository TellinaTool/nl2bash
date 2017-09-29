"""
Split the dataset into train, dev and test randomly according to the given ratio.

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
hypothes_header = re.compile('\<\!\-\- WB Insert \-\-\>.*\<\!\-\- End WB Insert \-\-\>', re.DOTALL)

# minimum number of edits two natural language descriptions have to differ to not be considered as duplicates
EDITDIST_THRESH = 8


def split_data(data_dir):
    def write_data(data_path, data):
        with open(data_path, 'w') as o_f:
            for line in data:
                o_f.write(line + '\n')
            print('{} saved'.format(data_path))

    nl_file_path = os.path.join(data_dir, 'all.nl')
    cm_file_path = os.path.join(data_dir, 'all.cm')

    with open(nl_file_path) as f:
        nls = [line.strip() for line in f.readlines()]
    with open(cm_file_path) as f:
        cms = [line.strip() for line in f.readlines()]

    assert(len(nls) == len(cms))

    pairs = collections.defaultdict(list)

    for nl, cm in zip(nls, cms):
        nl_temp = ' '.join(basic_tokenizer(nl)[0])
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

    random.seed(100)

    for nl_temp in pairs:
        ind = random.randrange(num_folds)
        if ind < num_folds - 2:
            num_train += 1
            for nl, cm in pairs[nl_temp]:
                train_nl_list.append(nl)
                train_cm_list.append(cm)
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

    train_path = os.path.join(data_dir, "train")
    dev_path = os.path.join(data_dir, "dev")
    test_path = os.path.join(data_dir, "test")
    write_data(train_path + ".nl", train_nl_list)
    write_data(train_path + ".cm", train_cm_list)
    write_data(dev_path + ".nl", dev_nl_list)
    write_data(dev_path + ".cm", dev_cm_list)
    write_data(test_path + ".nl", test_nl_list)
    write_data(test_path + ".cm", test_cm_list)


if __name__ == '__main__':
    data_dir = sys.argv[1]
    split_data(data_dir)
