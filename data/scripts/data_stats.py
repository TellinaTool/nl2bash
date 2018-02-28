"""
Compute data statistics.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import numpy as np
import os, sys
sys.path.append('../../')  # for bashlint
import re

from bashlint import bash, data_tools
from nlp_tools.tokenizer import basic_tokenizer


def u_hist_to_radar_chart():
    input_file = sys.argv[1]

    u_hist = collections.defaultdict(int)
    with open(input_file) as f:
        for cmd in f:
            ast = data_tools.bash_parser(cmd, verbose=False)
            for u in data_tools.get_utilities(ast):
                if u in bash.BLACK_LIST or u in bash.GREY_LIST:
                    continue
                u_hist[u] += 1

    selected_utilities = []
    for i, (u, freq) in enumerate(
            sorted(u_hist.items(), key=lambda x:x[1], reverse=True)):
        if i >= 50:
            print('{{axis:"{}",value:{:.2f}}},'.format(u, freq))
            selected_utilities.append(u)
    print()


def compute_nl_stats():
    input_file = sys.argv[1]
    unique_sentences = set()
    unique_words = set()
    words_per_sent = []
    sents_per_word = collections.defaultdict(int)
    with open(input_file) as f:
        for line in f:
            nl = line.strip()
            unique_sentences.add(nl)
            words, _ = basic_tokenizer(nl, to_lower_case=False, lemmatization=False)
            unique_words |= set(words)
            words_per_sent.append(len(words))
            for word in words:
                sents_per_word[word] += 1
    print('# unique sentences: {}'.format(len(unique_sentences)))
    print('# unique words: {}'.format(len(unique_words)))
    print('# words per sentence: average {}, median {}'.format(
        np.mean(words_per_sent), np.median(words_per_sent)))
    print('# sentences per word: average {} median {}'.format(
        np.mean(sents_per_word.values()), np.median(sents_per_word.values())))
    for w, f in sorted(sents_per_word.items(), key=lambda x:x[1], reverse=True)[:5]:
        print(w, f)

def compute_cm_stats():
    input_file = sys.argv[1]
    unique_commands = set()
    unique_templates = set()
    unique_tokens = set()
    tokens_per_cmd = []
    cmds_per_token = collections.defaultdict(int)
    with open(input_file) as f:
        for line in f:
            cm = line.strip()
            unique_commands.add(cm)
            temp = data_tools.cmd2template(cm, loose_constraints=True)
            unique_templates.add(temp)
            tokens = data_tools.bash_tokenizer(cm, loose_constraints=True)
            unique_tokens |= set(tokens)
            tokens_per_cmd.append(len(tokens))
            for token in tokens:
                cmds_per_token[token] += 1
    print('# unique commands: {}'.format(len(unique_commands)))
    print('# unique templates: {}'.format(len(unique_templates)))
    print('# unique tokens: {}'.format(len(unique_tokens)))
    print('# tokens per command: average {}, median {}'.format(
        np.mean(tokens_per_cmd), np.median(tokens_per_cmd)))
    print('# commands per token: average {}, median {}'.format(
        np.mean(cmds_per_token.values()), np.median(cmds_per_token.values())))


def compute_regex_stats():
    input_file = sys.argv[1]
    tokens = set()
    with open(input_file) as f:
        for line in f:
            for t in line.strip().split():
                tokens.add(t)
    print('# unique tokens: {}'.format(len(tokens)))                


def compute_jobs_stats():
    input_file = sys.argv[1]
    words = set()
    with open(input_file) as f:
        for line in f:
            match = re.search('\[(.*?)\]', line)
            pattern = match.group(0)
            for word in pattern[1:-1].split(','):
                words.add(word)
    print('# unique words: {}'.format(len(words)))


def compute_nlmaps_stats():
    input_file = sys.argv[1]
    words = set()
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if line[-1] in ['?', '.', '!']:
                sent = line[:-1]
                words.add(line[-1])
            else:
                sent = line
                print(sent)
            for word in sent.split():
                words.add(word)
    print('# unique words: {}'.format(len(words)))
    code_len_hist = {
        7: 28,
        8: 17,
        9: 7,
        10: 3,
        11: 227,
        12: 265,
        13: 182,
        14: 382,
        15: 314,
        16: 244,
        17: 124,
        18: 89,
        19: 58,
        20: 44,
        21: 34,
        22: 49,
        23: 57,
        24: 41,
        25: 54,
        26: 47,
        27: 25,
        28: 18,
        29: 32,
        30: 14,
        31: 2,
        32: 12,
        33: 8,
        36: 5
    }
    total_len = 0
    num = 0
    for key in code_len_hist:
        total_len += key * code_len_hist[key]
        num += code_len_hist[key]
    print('average sentence length: {}'.format(float(total_len) / num))

def compute_bash_stats():
    input_file = sys.argv[1]
    unique_utilities = set()
    unique_flags = set()
    unique_keywords = set()
    cmds_per_utility = collections.defaultdict(int)
    cmds_per_flag = collections.defaultdict(int)
    with open(input_file) as f:
        for line in f:
            cm = line.strip()
            tokens = data_tools.bash_tokenizer(cm, loose_constraints=True, with_prefix=True)
            for token in tokens:
                if token.startswith('UTILITY<KIND_PREFIX>'):
                    unique_utilities.add(token)
                    cmds_per_utility[token] += 1
                elif token.startswith('FLAG<KIND_PREFIX>'):
                    unique_flags.add(token)
                    cmds_per_flag[token] += 1
                elif not token.startswith('ARGUMENT<KIND_PREFIX>'):
                    unique_keywords.add(token)
    print('# unique utilities: {}'.format(len(unique_utilities)))
    print('# unique flags: {}'.format(len(unique_flags)))
    print('# unique keywords: {}'.format(len(unique_keywords)))
    print('# commands per utility: average {}, median {}'.format(
        np.mean(list(cmds_per_utility.values())), np.median(list(cmds_per_utility.values()))))
    print('# commands per flag: average {}, median {}'.format(
        np.mean(list(cmds_per_flag.values())), np.median(list(cmds_per_flag.values()))))

def compute_flag_stats():
    input_file = sys.argv[1]
    train_file = sys.argv[2]

    u_hist = collections.defaultdict(int)
    with open(input_file) as f:
        for cmd in f:
            ast = data_tools.bash_parser(cmd, verbose=False)
            for u in data_tools.get_utilities(ast):
                if u in bash.BLACK_LIST or u in bash.GREY_LIST:
                    continue
                u_hist[u] += 1
    
    sorted_u_by_freq = sorted(u_hist.items(), key=lambda x:x[1], reverse=True)
    most_frequent_10 = [u for u, _ in sorted_u_by_freq[:10]]
    least_frequent_10 = [u for u, _ in sorted_u_by_freq[-10:]]
    
    most_frequent_10_flags = collections.defaultdict(set)
    least_frequent_10_flags = collections.defaultdict(set)
    with open(train_file) as f:
        for cmd in f:
            tokens = data_tools.bash_tokenizer(cmd, loose_constraints=True,
                                               with_flag_head=True)
            for token in tokens:
                if '@@' in token:
                    u, f = token.split('@@')
                    if u in most_frequent_10:
                        most_frequent_10_flags[u].add(f)
                    if u in least_frequent_10:
                        least_frequent_10_flags[u].add(f)

    for u in most_frequent_10:
        if u in most_frequent_10_flags:
            print(u, data_tools.get_utility_statistics(u), len(most_frequent_10_flags[u]))
        else:
            print(u, data_tools.get_utility_statistics(u), 0)
    print()
    for u in least_frequent_10:
        if u in least_frequent_10_flags:
            print(u, data_tools.get_utility_statistics(u), len(least_frequent_10_flags[u]))
        else:
            print(u, data_tools.get_utility_statistics(u), 0)    
    
def compute_mapping_stats():
    nl_file = sys.argv[1]
    cm_file = sys.argv[2]
    nl_to_cm_sizes = collections.defaultdict(int)
    cm_to_nl_sizes = collections.defaultdict(int)
    n_f = open(nl_file)
    c_f = open(cm_file)
    for nl, cm in zip(n_f, c_f):
        nl_to_cm_sizes[nl] += 1
        cm_to_nl_sizes[cm] += 1
    n_f.close()
    c_f.close()
    print('# cms per nl: average {}, median {}, max {}'.format(
        np.mean(nl_to_cm_sizes.values()), np.median(nl_to_cm_sizes.values()), np.max(nl_to_cm_sizes.values())))
    print('# nls per cm: average {}, median {}, max {}'.format(
        np.mean(cm_to_nl_sizes.values()), np.median(cm_to_nl_sizes.values()), np.max(cm_to_nl_sizes.values())))

def count_unique_nls():
    nl_file = sys.argv[1]
    unique_nls = set()
    with open(nl_file) as f:
        for line in f:
            nl = line.strip()
            nl_temp = ' '.join(basic_tokenizer(nl)[0])
            unique_nls.add(nl_temp)
    print('number of unique natural language forms: {}'.format(len(unique_nls)))

        
def main():
    # compute_nl_stats()
    # compute_cm_stats()
    # compute_bash_stats()
    # compute_mapping_stats()
    count_unique_nls()
    # u_hist_to_radar_chart()
    # compute_flag_stats()
    # compute_regex_stats()
    # compute_jobs_stats()
    # compute_nlmaps_stats()

if __name__ == '__main__':
    main()
