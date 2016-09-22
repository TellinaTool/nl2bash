# builtin
from __future__ import print_function

import sqlite3

class DBConnection(object):
    def __init__(self):
        self.conn = sqlite3.connect("eval_archive.db",
                                    detect_types=sqlite3.PARSE_DECLTYPES,
                                    check_same_thread=False)
        self.cursor = self.conn.cursor()

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def create_schema(self):
        c = self.cursor

        c.execute("CREATE TABLE IF NOT EXISTS Archives (nl TEXT, temp TEXT, judgement INT)")

        self.conn.commit()

    def add_judgement(self, triple):
        c = self.cursor
        if not self.exist_pair((triple[0], triple[1])):
            c.execute("INSERT INTO Archives (nl, temp, judgement) VALUES (?, ?, ?)", triple)
        self.conn.commit()

    def get_judgement(self, pair):
        c = self.cursor
        for _, _, judgement in c.execute("SELECT nl, temp, judgement FROM Archives WHERE nl = ? AND temp = ?", pair):
            return judgement

    def exist_pair(self, pair):
        c = self.cursor
        for _, _, judgement in c.execute("SELECT 1 FROM Archives WHERE nl = ? AND temp = ?", pair):
            return True
        return False