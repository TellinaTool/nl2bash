from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os, sys
sys.path.append('/home/xilin/Projects/tellina/learning_module/')

from bashlint import data_tools

data_splits = ['train', 'dev', 'test']

NUM_UTILITIES = 64

BLACK_LIST = {
    'cpp',
    'g++',
    'java',
    'perl',
    'python',
    'ruby',
    'nano',
    'emacs',
    'vim',
    'sed',
    'awk',
    'less',
    'more'
}
GREY_LIST = {
    'alias',
    'unalias',
    'set',
    'unset',
    'screen',
    'apt-get',
    'brew',
    'yum',
    'export',
    'shift',
    'exit',
    'logout'}

def compute_top_utilities(path, k):
    utilities = collections.defaultdict(int)
    with open(path) as f:
        while (True):
            command = f.readline().strip()
            if not command:
                break
            ast = data_tools.bash_parser(command, verbose=False)
            for u in data_tools.get_utilities(ast):
                utilities[u] += 1
    top_utilities = []
    for u, freq in sorted(utilities.items(), key=lambda x:x[1], reverse=True):
        if u in BLACK_LIST or u in GREY_LIST:
            continue
        top_utilities.append(u)
        if len(top_utilities) == k:
            break
    top_utilities = set(top_utilities)
    return top_utilities


if __name__ == '__main__':
    data_dir = sys.argv[1]
    cm_path = os.path.join(data_dir, 'cm.txt')
    top_utilities = compute_top_utilities(cm_path, NUM_UTILITIES)

    for split in data_splits:
        nl_file_path = os.path.join(data_dir, split + '.nl')
        cm_file_path = os.path.join(data_dir, split + '.cm')
        with open(nl_file_path) as f:
            nls = [nl.strip() for nl in f.readlines()]
        with open(cm_file_path) as f:
            cms = [cm.strip() for cm in f.readlines()]
        nl_outfile_path = os.path.join(data_dir, split + '.nl.filtered')
        cm_outfile_path = os.path.join(data_dir, split + '.cm.filtered')
        with open(nl_outfile_path, 'w') as nl_outfile:
            with open(cm_outfile_path, 'w') as cm_outfile:
                for nl, cm in zip(nls, cms):
                    ast = data_tools.bash_parser(cm)
                    if ast and data_tools.select(ast, top_utilities):
                        nl_outfile.write('{}\n'.format(nl))
                        cm_outfile.write('{}\n'.format(cm)) 
