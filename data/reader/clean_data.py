#!/usr/bin/env python2.7

import collections
import cPickle as pickle
import sqlite3
import sys
sys.path.append("..")
sys.path.append("../../bashlex")
import random

from utils import is_stopword
from bash import basic_tokenizer, bash_tokenizer

# minimum number of edits two natural language descriptions have to differ to not be considered as duplicates
EDITDIST_THRESH = 8

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

    def unique_pairs(self):
        cmds_dict = collections.defaultdict(list)
        for user, url, nl, cmd, time_stamp in self.pairs():
            duplicated = False
            for nl2 in cmds_dict[cmd]:
                if minEditDist(nl.lower(), nl2.lower()) < EDITDIST_THRESH:
                    duplicated = True
                    break
            if not duplicated:
                cmds_dict[cmd].append(nl)
        return cmds_dict

    def unique_pairs_by_signature(self):
        unique_pairs = self.unique_pairs()
        cmds_dict = collections.defaultdict(list)
        num_errors = 0
        for cmd in unique_pairs:
            if not cmd:
                continue
            signature = self.reserved_words_signature(cmd)
            if not signature:
                num_errors += 1
                continue
            for nl in unique_pairs[cmd]:
                cmds_dict[signature].append((cmd, nl))
        print("Unable to parse %d commands" % num_errors)
        return cmds_dict

    def unique_pairs_by_description(self, head_cmd):
        unique_pairs = self.unique_pairs()
        desp_dict = collections.defaultdict(list)
        num_errors = 0
        for cmd in unique_pairs:
            if not cmd:
                continue
            if not self.head_present(cmd, "find"):
                continue
            tokens = bash_tokenizer(cmd)
            if not tokens:
                num_errors += 1
                continue
            print(cmd.encode('utf-8'))
            print(' '.join(tokens).encode('utf-8'))
            print
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
                desp_dict[nl].append((cmd, nl))
        return desp_dict

    def dump_data(self, data_dir, num_folds=10):
        num_cmd = 0
        num_pairs = 0

        desp_dict = self.unique_pairs_by_description("find")

        data = collections.defaultdict(list)
        for query in desp_dict:
            # if not ("find " in signature or " find" in signature):
            #     continue
            # print(signature)
            print("Query: %s" % query.encode('utf-8'))
            num_cmd += 1
            ind = random.randrange(num_folds)
            bin = data[ind]
            for cmd, nl in desp_dict[query]:
                if nl == "NA":
                    continue
                print("desp: %s" % nl.encode('utf-8'))
                num_pairs += 1
                cmd = cmd.strip().replace('\n', ' ').replace('\r', ' ')
                nl = nl.strip().replace('\n', ' ').replace('\r', ' ')
                if nl.endswith("."):
                    nl = nl[:-1]
                if not type(nl) is unicode:
                    nl = nl.decode()
                if not type(cmd) is unicode:
                    cmd = cmd.decode()
                bin.append((nl, cmd))

        print("Total number of pairs: %d" % num_pairs)
        print("Total number of commands: %d" % num_cmd)
        print("%.2f descriptions per command" % ((num_pairs + 0.0) / num_cmd))
        with open(data_dir + "/data.dat", 'w') as o_f:
            pickle.dump(data, o_f)

    def head_present(self, cmd, head):
        if (head + ' ') in cmd:
            return True
        elif (' ' + head) in cmd:
            return True
        else:
            return False

if __name__ == "__main__":
    with DBConnection() as db:
        db.create_schema()
        db.dump_data(".")
