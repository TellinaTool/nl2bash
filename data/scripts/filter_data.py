"""
Filter data pairs and retain only grammatical and frequently used commands.

Usage: python3 filter_data.py data_dir
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os, sys
sys.path.append('../../')  # for bashlint

from bashlint import bash, data_tools

data_splits = ['train', 'dev', 'test']

NUM_UTILITIES = 100

def compute_top_utilities(path, k):
    print('computing top most frequent utilities...') 
    utilities = collections.defaultdict(int)
    with open(path, encoding='utf-8') as f:
        while (True):
            command = f.readline().strip()
            if not command:
                break
            ast = data_tools.bash_parser(command, verbose=False)
            for u in data_tools.get_utilities(ast):
                utilities[u] += 1
    top_utilities = []

    freq_threshold = -1   
    for u, freq in sorted(utilities.items(), key=lambda x:x[1], reverse=True):
        if freq_threshold > 0 and freq < freq_threshold:
            break 
        if u in bash.BLACK_LIST or u in bash.GREY_LIST:
            continue
        top_utilities.append(u)
        print('{}: {} ({})'.format(len(top_utilities), u, freq))
        if len(top_utilities) == k:
            freq_threshold = freq
    top_utilities = set(top_utilities)
    return top_utilities


def filter_by_most_frequent_utilities(data_dir, num_utilities):
    def select(ast, utility_set):
        for ut in data_tools.get_utilities(ast):
            if not ut in utility_set:
                print('Utility currently not handled: {} - {}'.format(
                    ut, data_tools.ast2command(ast, loose_constraints=True).encode('utf-8')))
                return False
        return True

    cm_path = os.path.join(data_dir, 'all.cm')
    top_utilities = compute_top_utilities(cm_path, num_utilities)
    for split in ['all']:
        nl_file_path = os.path.join(data_dir, split + '.nl')
        cm_file_path = os.path.join(data_dir, split + '.cm')
        with open(nl_file_path, encoding='utf-8') as f:
            nls = [nl.strip() for nl in f.readlines()]
        with open(cm_file_path, encoding='utf-8') as f:
            cms = [cm.strip() for cm in f.readlines()]
        nl_outfile_path = os.path.join(data_dir, split + '.nl.filtered')
        cm_outfile_path = os.path.join(data_dir, split + '.cm.filtered')
        with open(nl_outfile_path, 'w', encoding='utf-8') as nl_outfile:
            with open(cm_outfile_path, 'w', encoding='utf-8') as cm_outfile:
                for nl, cm in zip(nls, cms):
                    if len(nl.split()) > 50:
                        print('lenthy description skipped: {}'.format(nl))
                        continue
                    ast = data_tools.bash_parser(cm)
                    if ast and select(ast, top_utilities):
                        nl_outfile.write('{}\n'.format(nl))
                        cm_outfile.write('{}\n'.format(cm))
                            

def gen_non_specific_description_check_csv(data_dir):
    with open(os.path.join(data_dir, 'all.nl')) as f:
        nl_list = [nl.strip() for nl in f.readlines()]
    with open(os.path.join(data_dir, 'all.cm')) as f:
        cm_list = [cm.strip() for cm in f.readlines()]
    assert(len(nl_list) == len(cm_list))

    with open('annotation_check_sheet.non.specific.csv', 'w') as o_f:
        o_f.write('Utility,Command,Description\n')
        for nl, cm in zip(nl_list, cm_list):
            if ' specific ' in nl or ' a file ' in nl or ' a folder ' in nl \
                    or ' a directory ' in nl or ' some ' in nl \
                    or ' a pattern ' in nl or ' a string ' in nl:
                ast = data_tools.bash_parser(cm)
                if ast:
                    o_f.write(',"{}","{}"\n'.format(cm.replace('"', '""'), 
                        nl.replace('"', '""')))
                    o_f.write(',,<Type a new description here>\n')


if __name__ == '__main__':
    dataset = sys.argv[1]
    data_dir = os.path.join(os.path.dirname(os.path.dirname(
        os.path.realpath(__file__))), dataset)
    filter_by_most_frequent_utilities(data_dir, NUM_UTILITIES)
