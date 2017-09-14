"""
Extract bash templates that are semantically equivalent from a parallel corpus.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os, sys

if sys.version_info > (3, 0):
    from six.moves import xrange

from bashlint import data_tools
from nlp_tools import tokenizer


def extract_rewrites(data):
    """Extract all pairs of rewrites from a parallel corpus."""
    nls, cms = data

    # Step 1: group pairs with the same natural language description.
    group_pairs_by_nl = collections.defaultdict(set)
    for nl, cm in zip(nls, cms):
        nl = nl.strip()
        cm = cm.strip()
        if nl.lower() == "na":
            continue
        if not nl:
            continue
        if not cm:
            continue
        nl_tokens, _ = tokenizer.ner_tokenizer(nl)
        nl_temp = ' '.join(nl_tokens)
        cm_temp = data_tools.cmd2template(cm)
        if not cm_temp in group_pairs_by_nl[nl_temp]:
            group_pairs_by_nl[nl_temp].add(cm_temp)

    # Step 2: cluster the commands with the same natural language explanations.
    merged = set()
    nls = group_pairs_by_nl.keys()
    for i in xrange(len(nls)):
        nl = nls[i]
        cm_temp_set = group_pairs_by_nl[nl]
        for j in xrange(i+1, len(nls)):
            nl2 = nls[j]
            cm_temp_set2 = group_pairs_by_nl[nl2]
            if len(cm_temp_set & cm_temp_set2) >= 2:
                for cm_temp in cm_temp_set:
                    if not cm_temp in group_pairs_by_nl[nl2]:
                        group_pairs_by_nl[nl2].add(cm_temp)
                merged.add(i)

    # Step 3: remove redundant clusters after merge.
    rewrites = {}
    for i in xrange(len(nls)):
        if not i in merged:
            rewrites[nls[i]] = group_pairs_by_nl[nls[i]]

    # Step 4: print extracted rewrites and store in database.
    for nl, cm_temps in sorted(rewrites.items(), key=lambda x: len(x[1]),
                               reverse=True):
        if len(cm_temps) >= 2:
            for cm_temp1 in cm_temps:
                for cm_temp2 in cm_temps:
                    if cm_temp1 == cm_temp2:
                        continue
                    print("* {} --> {}".format(cm_temp1, cm_temp2))
            print()