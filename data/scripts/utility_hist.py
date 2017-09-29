from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os, sys
sys.path.append('/home/xilin/Projects/tellina/learning_module/')

import numpy as np

from bashlint import bash, data_tools


def get_u_hist_from_file(input_file):
    u_hist = collections.defaultdict(int)
    with open(input_file) as f:
        for cmd in f:
            ast = data_tools.bash_parser(cmd, verbose=False)
            for u in data_tools.get_utilities(ast):
                if u in bash.BLACK_LIST or u in bash.GREY_LIST:
                    continue
                u_hist[u] += 1
    return u_hist
   

def get_flag_statistics(top_utilities, input_file):
    flag_counts = {}
    for u in top_utilities:
        flag_counts[u] = set()
    with open(input_file) as f:
        for cmd in f:
            ast = data_tools.bash_parser(cmd, verbose=False)
            if ast:
                # DFS 
                stack = []
                stack.extend(ast.children)
                while stack:
                    node = stack.pop()
                    if node.is_option():
                        u = node.utility.value
                        if u in flag_counts:
                            flag_counts[u].add(node.value)
                    stack.extend(node.children)
            else:
                print(cmd)
    for i in range(len(top_utilities)-1, -1, -1):
        u = top_utilities[i]
        print('{{axis:"{}",num_flags:{},num_flags_in_data:{}}},'
              .format(u, data_tools.get_utility_statistics(u), 
                      len(flag_counts[u])))


if __name__ == '__main__':
    input_path = sys.argv[1]
    hist = get_u_hist_from_file(input_path)
    long_tail = 0
    top_utilities = []
    for i, (u, freq) in enumerate(
            sorted(hist.items(), key=lambda x:x[1], reverse=True)):
        if i < 50:
            print('{{axis:"{}",value:{:.2f}}},'.format(u, np.log(freq)))
            top_utilities.append(u)
        else:
            long_tail += freq
    print('{{axis:"{}",value:{:.2f}}}'.format('OTHER', np.log(long_tail)))
    print()

    long_tail = 0
    output = []
    for i, (u, freq) in enumerate(
            sorted(hist.items(), key=lambda x:x[1], reverse=True)):
        if i < 50:
            output.append('{{axis:"{}",value:{}}},'.format(
                u, data_tools.get_utility_statistics(u)))
        else:
            long_tail += data_tools.get_utility_statistics(u)
    output.append('{{axis:"{}",value:{}}}'.format('OTHER', long_tail))
    for i in range(len(output)-1, -1, -1):
        print(output[i])

    get_flag_statistics(top_utilities, input_path)
