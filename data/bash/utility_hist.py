from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os, sys
sys.path.append('/home/xilin/Projects/tellina/learning_module/')

from bashlint import data_tools


def get_u_hist_from_file(input_file):
    u_hist = collections.defaultdict(int)
    with open(input_file) as f:
        for cmd in f:
            ast = data_tools.bash_parser(cmd, verbose=False)
            for u in data_tools.get_utilities(ast):
                u_hist[u] += 1
    return u_hist
    

if __name__ == '__main__':
    train_path = os.path.join(os.path.dirname(__file__), 'train.cm.filtered')
    dev_path = os.path.join(os.path.dirname(__file__), 'dev.cm.filtered')
    train_hist = get_u_hist_from_file(train_path)
    dev_hist = get_u_hist_from_file(dev_path)
    for i, (u, freq) in enumerate(
            sorted(train_hist.items(), key=lambda x:x[1], reverse=True)):
        print('{},{},{},{},{}'.format(i+1, u, 
            data_tools.get_utility_statistics(u),freq, dev_hist[u]))
