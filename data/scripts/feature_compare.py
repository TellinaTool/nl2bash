"""
Print features from different channels side-by-side.
"""

import os, sys
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))

from bashlint import data_tools
from encoder_decoder import data_utils


def gen_compare_file(split, lang):
     with open('{}.{}.compare'.format(split, lang), 'w') as o_f:
        with open('{}.{}.{}'.format(split, lang, channel1)) as f:
            train_nls_channel1 = [line.strip() for line in f.readlines()]
        with open('{}.{}.{}'.format(split, lang, channel2)) as f:
            train_nls_channel2 = [line.strip() for line in f.readlines()]
        assert(len(train_nls_channel1) == len(train_nls_channel2))
        for nl1, nl2 in zip(train_nls_channel1, train_nls_channel2):
            o_f.write('\t'.join(
                [t.split(data_tools.flag_suffix)[0] 
                    for t in nl1.split(data_utils.TOKEN_SEPARATOR)]) + '\n')
            o_f.write('\t'.join(
                [t.split(data_tools.flag_suffix)[0] 
                    for t in nl2.split(data_utils.TOKEN_SEPARATOR)]) + '\n')
            o_f.write('\n')

if __name__ == '__main__':
    channel1 = sys.argv[1]
    channel2 = sys.argv[2]
    gen_compare_file('train', 'nl')
    gen_compare_file('train', 'cm')
    gen_compare_file('dev', 'nl')
    gen_compare_file('dev', 'cm')
