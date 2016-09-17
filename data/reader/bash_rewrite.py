"""Extract bash templates that are paraphrases to each other."""
import collections
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "bashlex"))

import data_tools

if __name__ == "__main__":
    nl_path = sys.argv[1]
    cm_path = sys.argv[2]

    with open(nl_path) as f:
        nls = f.readlines()
    with open(cm_path) as f:
        cms = f.readlines()

    group_pairs_by_nl = {}
    for nl, cm in zip(nls, cms):
        nl_temp = ' '.join(data_tools.basic_tokenizer(nl))
        if not nl_temp in group_pairs_by_nl:
            group_pairs_by_nl[nl_temp] = {}
        cm_temp = data_tools.cmd2template(cm)
        if not cm_temp in group_pairs_by_nl[nl_temp]:
            group_pairs_by_nl[nl_temp][cm_temp] = \
                collections.defaultdict(int)
        group_pairs_by_nl[nl_temp][cm_temp][cm] += 1

    merged = set()
    nls = group_pairs_by_nl.keys()
    for i in xrange(len(nls)):
        nl = nls[i]
        cm_set = set(group_pairs_by_nl[nl].keys())
        for j in xrange(i+1, len(nls)):
            nl2 = nls[j]
            cm_set2 = set(group_pairs_by_nl[nl2].keys())
            if cm_set & cm_set2:
                for cm_temp in cm_set:
                    if not cm_temp in group_pairs_by_nl[nl2]:
                        group_pairs_by_nl[nl2][cm_temp] = \
                            group_pairs_by_nl[nl][cm_temp]
                    else:
                        for cm in group_pairs_by_nl[nl][cm_temp]:
                            group_pairs_by_nl[nl2][cm_temp][cm] += \
                                group_pairs_by_nl[nl][cm_temp][cm]
                merged.add(i)

    bash_paraphrases = {}
    for i in xrange(len(nls)):
        if i in merged:
            continue
        bash_paraphrases[nls[i]] = group_pairs_by_nl[nls[i]]

    for nl, cm_temps in sorted(bash_paraphrases.items(), lambda x: len(x[1]), reverse=True):
        print nl.encode('utf-8'), len(cm_temps)




