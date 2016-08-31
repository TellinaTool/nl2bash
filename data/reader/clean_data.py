#!/usr/bin/env python2.7

import collections
import cPickle as pickle
import functools
import random
import sqlite3
import sys
sys.path.append("..")
sys.path.append("../../bashlex")
import warnings

from data_tools import basic_tokenizer, bash_tokenizer, is_stopword, to_template

# minimum number of edits two natural language descriptions have to differ to not be considered as duplicates
EDITDIST_THRESH = 8

split_by_template = True

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)     #turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)    #reset filter
        return func(*args, **kwargs)

    return new_func

def token_overlap(s1, s2):
    tokens1 = set([w for w in basic_tokenizer(s1) if not is_stopword(w)])
    tokens2 = set([w for w in basic_tokenizer(s2) if not is_stopword(w)])
    return (len(tokens1 & tokens2) + 0.0) / len(tokens1 | tokens2)

def minEditDist(target, source):
    ''' Computes the min edit distance from target to source. '''

    n = len(target)
    m = len(source)

    distance = [[0 for i in range(m+1)] for j in range(n+1)]

    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + insertCost(target[i-1])

    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + deleteCost(source[j-1])

    for i in range(1,n+1):
        for j in range(1,m+1):
           distance[i][j] = min(distance[i-1][j]+1,
                                distance[i][j-1]+1,
                                distance[i-1][j-1]+substCost(source[j-1],target[i-1]))
    return distance[n][m]

def insertCost(x):
    return 1

def deleteCost(x):
    return 1

def substCost(x,y):
    if x == y: return 0
    else: return 1

class DBConnection(object):
    def __init__(self):
        self.conn = sqlite3.connect("data.db", detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def create_schema(self):
        c = self.cursor

        c.execute("CREATE TABLE IF NOT EXISTS Urls    (search_phrase TEXT, url TEXT)")
        c.execute("CREATE INDEX IF NOT EXISTS Urls_url ON Urls (url)")
        c.execute("CREATE INDEX IF NOT EXISTS Urls_sp  ON Urls (search_phrase)")

        c.execute("CREATE TABLE IF NOT EXISTS SearchContent (url TEXT, fingerprint TEXT, min_distance INT, " +
                                                            "max_score FLOAT, avg_score FLOAT, num_cmds INT, " +
                                                            "num_visits INT, html TEXT)")
        c.execute("CREATE INDEX IF NOT EXISTS SearchContent_url ON SearchContent (url)")
        # c.execute("ALTER TABLE SearchContent ADD num_cmds INT")
        # c.execute("ALTER TABLE SearchContent ADD num_visits INT")
        # c.execute("ALTER TABLE SearchContent ADD avg_score FLOAT")
        # c.execute("ALTER TABLE SearchContent ADD max_score FLOAT")
        # c.execute("CREATE INDEX IF NOT EXISTS SearchContent_num_cmds ON SearchContent (num_cmds)")
        # c.execute("CREATE INDEX IF NOT EXISTS SearchContent_avg_score ON SearchContent (avg_score)")
        c.execute("CREATE INDEX IF NOT EXISTS SearchContent_idx ON SearchContent (avg_score, num_cmds, num_visits)")

        c.execute("CREATE TABLE IF NOT EXISTS Commands (url TEXT, cmd TEXT)")
        c.execute("CREATE INDEX IF NOT EXISTS Commands_url ON Commands (url)")

        c.execute("CREATE TABLE IF NOT EXISTS Skipped (url TEXT, user_id INT, time_stamp INT)")
        c.execute("CREATE INDEX IF NOT EXISTS Skipped_idx ON Skipped (user_id, url)")
        # c.execute("ALTER TABLE Skipped ADD time_stamp INT")

        c.execute("CREATE TABLE IF NOT EXISTS NoPairs (url TEXT, user_id INT, time_stamp INT)")
        c.execute("CREATE INDEX IF NOT EXISTS NoPairs_idx ON NoPairs (user_id, url)")
        # c.execute("ALTER TABLE NoPairs ADD time_stamp INT")

        c.execute("CREATE TABLE IF NOT EXISTS Pairs   (url TEXT, user_id INT, nl TEXT, cmd TEXT, time_stamp INT, judgement FLOAT)")
        c.execute("CREATE INDEX IF NOT EXISTS Pairs_idx ON Pairs (user_id, url)")
        # c.execute("ALTER TABLE Pairs ADD time_stamp INT")
        # c.execute("ALTER TABLE Pairs ADD judgement FLOAT")

        c.execute("CREATE TABLE IF NOT EXISTS Users   (user_id INT, first_name TEXT, last_name TEXT, alias TEXT, time_stamp INT)")
        c.execute("CREATE INDEX IF NOT EXISTS Users_userid ON Users (user_id)")
        # c.execute("ALTER TABLE Users Add alias TEXT")
        # c.execute("ALTER TABLE Users Add time_stamp INT")
        # c.execute("ALTER TABLE Users Add recall FLOAT")

        c.execute("CREATE TABLE IF NOT EXISTS TokenCounts (token TEXT, count INT)")
        c.execute("CREATE INDEX IF NOT EXISTS TokenCounts_token ON TokenCounts (token)")

        self.conn.commit()

    def pairs(self):
        c = self.conn.cursor()
        for user, url, nl, cmd, time_stamp in c.execute("SELECT user_id, url, nl, cmd, time_stamp FROM Pairs"):
            yield (user, url, nl, cmd, time_stamp)
        c.close()

    def unique_pairs(self, head_cmd):
        cmds_dict = {}
        for user, url, nl, cmd, time_stamp in self.pairs():
            if not cmd:
                continue
            if not nl:
                continue
            if not self.head_present(cmd, head_cmd):
                continue
            if not url in cmds_dict:
                cmds_dict[url] = {}
            if not nl in cmds_dict[url]:
                cmds_dict[url][nl] = set()
            cmds_dict[url][nl].add(cmd)
        return cmds_dict

    @deprecated
    def unique_pairs_by_signature(self):
        unique_pairs = self.unique_pairs()
        cmds_dict = collections.defaultdict(list)
        num_errors = 0
        for cmd in unique_pairs:
            if not cmd:
                continue
            signature = to_template(cmd, arg_type_only=split_by_template)
            if not signature:
                num_errors += 1
                continue
            for nl in unique_pairs[cmd]:
                cmds_dict[signature].append((cmd, nl))
        print("Unable to parse %d commands" % num_errors)
        return cmds_dict

    @deprecated
    def unique_pairs_by_description(self, head_cmd):
        unique_pairs = self.unique_pairs(head_cmd)
        desp_dict = collections.defaultdict(list)
        num_errors = 0
        for cmd in unique_pairs:
            if not cmd:
                continue
            tokens = bash_tokenizer(cmd)
            if not tokens:
                num_errors += 1
                continue
            # print(cmd.encode('utf-8'))
            # print(' '.join(tokens))
            # print
            for nl in unique_pairs[cmd]:
                """inserted = False
                for nl2 in desp_dict:
                    if token_overlap(nl, nl2) > 0.6:
                        desp_dict[nl2].append((cmd, nl))
                        inserted = True
                        break
                if not inserted:
                    desp_dict[nl].append((cmd, nl))
                """
                desp_dict[nl].append(cmd)
        return desp_dict

    def dump_data(self, data_dir, num_folds=10):
        # First-pass: group pairs by URLs
        pairs = self.unique_pairs("find")

        # Second-pass: group url clusters by nls
        urls = pairs.keys()
        print("%d urls in the database" % len(urls))

        merged_urls_by_nl = []
        for i in xrange(len(urls)):
            url = urls[i]
            for j in xrange(i+1, len(urls)):
                url2 = urls[j]
                merge = False
                for nl in pairs[url]:
                    for nl2 in pairs[url2]:
                        if nl == nl2:
                            merge = True
                            break
                    if merge:
                        break
                if merge:
                    break
            if merge:
                for nl in pairs[url]:
                    if nl in pairs[url2]:
                        pairs[url2][nl] = pairs[url][nl] | pairs[url2][nl]
                    else:
                        pairs[url2][nl] = pairs[url][nl]
                merged_urls_by_nl.append(i)
        print("%d urls merged by nl" % len(merged_urls_by_nl))

        # Third-pass: group url clusters by commands
        merged_urls_by_cmd = []
        for i in xrange(len(urls)):
            if i in merged_urls_by_nl:
                continue
            url = urls[i]
            for j in xrange(i+1, len(urls)):
                if j in merged_urls_by_nl:
                    continue
                url2 = urls[j]
                merge = False
                for _, cmds in pairs[url].items():
                    for cmd in cmds:
                        template = to_template(cmd, arg_type_only=split_by_template)
                        for _, cmd2s in pairs[url2].items():
                            for cmd2 in cmd2s:
                                template2 = to_template(cmd2, arg_type_only=split_by_template)
                                if template == template2:
                                    merge = True
                                    break
                            if merge:
                                break
                        if merge:
                            break
                    if merge:
                        break
                if merge:
                    break
            if merge:
                for nl in pairs[url]:
                    if nl in pairs[url2]:
                        pairs[url2][nl] = pairs[url][nl] | pairs[url2][nl]
                    else:
                        pairs[url2][nl] = pairs[url][nl]
                merged_urls_by_cmd.append(i)
        print("%d urls merged by cmd" % len(merged_urls_by_cmd))

        remained_urls = []
        for i in xrange(len(urls)):
            if i in merged_urls_by_cmd:
                continue
            if i in merged_urls_by_nl:
                continue
            remained_urls.append(urls[i])
        sorted_urls = sorted(urls, key=lambda x:len(pairs[url]), reverse=True)

        data = collections.defaultdict(list)

        num_pairs = 0
        num_train = 0
        num_train_pairs = 0
        num_dev = 0
        num_dev_pairs = 0
        num_test = 0
        num_test_pairs = 0
        num_urls = 0

        top_k = 10

        for i in xrange(len(sorted_urls)):
            url_size = reduce(lambda x, y: x+y, [len(pairs[url][nl]) for nl in pairs[url]])
            print("url %d (%d)" % (i, url_size))
            url = sorted_urls[i]
            if i < top_k:
                ind = random.randrange(num_folds - 2)
                num_train += 1
                num_train_pairs += url_size
            else:
                ind = random.randrange(num_folds)
                if ind < num_folds - 2:
                    num_train += 1
                    num_train_pairs += url_size
                elif ind == num_folds - 2:
                    num_dev += 1
                    num_dev_pairs += url_size
                elif ind == num_folds - 1:
                    num_test += 1
                    num_test_pairs += url_size
            num_urls += 1

            bin = data[ind]
            for nl in pairs[url]:
                for cmd in pairs[url][nl]:
                    num_pairs += 1
                    cmd = cmd.strip().replace('\n', ' ').replace('\r', ' ')
                    nl = nl.strip().replace('\n', ' ').replace('\r', ' ')
                    if not type(nl) is unicode:
                        nl = nl.decode()
                    if not type(cmd) is unicode:
                        cmd = cmd.decode()
                    bin.append((nl, cmd))

        print("Total number of pairs: %d" % num_pairs)
        print("Total number of url clusters: %d" % num_urls)
        print("Total number of train clusters: %d (%d pairs)" % (num_train, num_train_pairs))
        print("Total number of dev clusters: %d (%d pairs)" % (num_dev, num_dev_pairs))
        print("Total number of test clusters: %d (%d pairs)" % (num_test, num_test_pairs))
        print("%.2f pairs per url cluster" % ((num_pairs + 0.0) / num_urls))

        if split_by_template:
            split_by = "template"
        else:
            split_by = "command"
        with open(data_dir + "/data.by.%s.dat" % split_by, 'w') as o_f:
            pickle.dump(data, o_f)

    def head_present(self, cmd, head):
        if (head + ' ') in cmd:
            return True
        elif (' ' + head) in cmd:
            return True
        else:
            return False

if __name__ == "__main__":
    split_by = sys.argv[1]
    if split_by == "template":
        split_by_template = True
    else:
        split_by_template = False
    with DBConnection() as db:
        db.create_schema()
        db.dump_data(".")
