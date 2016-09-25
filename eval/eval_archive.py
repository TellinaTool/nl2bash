"""
Database which stores model predictions and manual judgements.
"""
from __future__ import print_function

import os
import sqlite3

class DBConnection(object):
    def __init__(self):
        self.conn = sqlite3.connect(
            os.path.join(os.path.dirname(__file__), "eval_archive.db"),
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

        c.execute("CREATE TABLE IF NOT EXISTS Output (model TEXT, nl TEXT, pred_cmd TEXT, score FLOAT)")

        c.execute("CREATE TABLE IF NOT EXISTS StrArchives (nl TEXT, pred_cmd TEXT, judgement INT)")
        c.execute("CREATE TABLE IF NOT EXISTS TempArchives (nl TEXT, pred_temp TEXT, judgement INT)")

        self.conn.commit()

    # --- Prediction ---
    def add_prediction(self, model, nl, pred_cmd, score):
        nl = nl.encode('utf-8')
        c = self.cursor
        if self.exist_prediction(model, nl):
            c.execute("UPDATE Output SET pred_cmd = ?, score = ? WHERE model = ? AND nl = ?",
                      (pred_cmd, score, model, nl))
        else:
            c.execute("INSERT INTO Output (model, nl, pred_cmd, score) VALUES (?, ?, ?, ?)",
                      (model, nl, pred_cmd, score))
        self.conn.commit()

    def exist_prediction(self, model, nl):
        nl = nl.encode('utf-8')
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM Output WHERE model = ? AND nl = ?", (model, nl)):
            return True
        return False

    def get_prediction(self, model, nl):
        nl = nl.encode('utf-8')
        return self.get_top_k_predictions(model, nl, 1)[0]

    def get_top_k_predictions(self, model, nl, k):
        nl = nl.encode('utf-8')
        c = self.cursor
        predictions = []
        for _, _, pred_cmd, score in \
            c.execute("SELECT model, nl, pred_cmd, score FROM Output WHERE model = ? AND nl = ?",
                      (model, nl)):
            predictions.append((pred_cmd, score))
        sorted_predictions = sorted(predictions, key=lambda x:x[1], reverse=True)
        return sorted_predictions[:k]

    # --- Manual Evaluation ---
    def add_str_judgement(self, triple):
        nl, pred_cmd, judgement = triple
        nl = nl.encode('utf-8')
        c = self.cursor
        if not self.exist_str_pair((nl, pred_cmd)):
            c.execute("INSERT INTO StrArchives (nl, pred_cmd, judgement) VALUES (?, ?, ?)", (nl, pred_cmd, judgement))
        self.conn.commit()

    def add_temp_judgement(self, triple):
        nl, pred_temp, judgement = triple
        nl = nl.encode('utf-8')
        c = self.cursor
        if not self.exist_temp_pair((nl, pred_temp)):
            c.execute("INSERT INTO TempArchives (nl, pred_temp, judgement) VALUES (?, ?, ?)", (nl, pred_temp, judgement))
        self.conn.commit()

    def get_str_judgement(self, pair):
        nl, pred_cmd = pair
        nl = nl.encode('utf-8')
        c = self.cursor
        for _, _, judgement in c.execute("SELECT nl, pred_cmd, judgement FROM StrArchives WHERE nl = ? AND pred_cmd = ?",
                                         (nl, pred_cmd)):
            return judgement

    def get_temp_judgement(self, pair):
        nl, pred_temp = pair
        nl = nl.encode('utf-8')
        c = self.cursor
        for _, _, judgement in c.execute("SELECT nl, pred_temp, judgement FROM TempArchives WHERE nl = ? AND pred_temp = ?",
                                         (nl, pred_temp)):
            return judgement

    def exist_str_pair(self, pair):
        nl, pred_cmd = pair
        nl = nl.encode('utf-8')
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM StrArchives WHERE nl = ? AND pred_cmd = ?", (nl, pred_cmd)):
            return True
        return False

    def exist_temp_pair(self, pair):
        nl, pred_temp = pair
        nl = nl.encode('utf-8')
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM TempArchives WHERE nl = ? AND pred_temp = ?", (nl, pred_temp)):
            return True
        return False

    def correct_str_pair(self, pair):
        nl, pred_cmd = pair
        nl = nl.encode('utf-8')
        c = self.cursor
        c.execute("UPDATE StrArchives SET judgement = ? WHERE nl = ? AND pred_cmd = ?",
                  (1, nl, pred_cmd))
        self.conn.commit()

    def correct_temp_pair(self, pair):
        nl, pred_temp = pair
        nl = nl.encode('utf-8')
        c = self.cursor
        c.execute("UPDATE TempArchives SET judgement = ? WHERE nl = ? AND pred_temp = ?",
                  (1, nl, pred_temp))
        self.conn.commit()

    def error_str_pair(self, pair):
        nl, pred_cmd = pair
        nl = nl.encode('utf-8')
        c = self.cursor
        c.execute("UPDATE StrArchives SET judgement = ? WHERE nl = ? AND pred_cmd = ?",
                  (0, nl, pred_cmd))
        self.conn.commit()

    def error_temp_pair(self, pair):
        nl, pred_temp = pair
        nl = nl.encode('utf-8')
        c = self.cursor
        c.execute("UPDATE TempArchives SET judgement = ? WHERE nl = ? AND pred_temp = ?",
                  (0, nl, pred_temp))
        self.conn.commit()

if __name__ == "__main__":
    db = DBConnection()
    db.create_schema()
    db.correct_temp_pair((
        "Find all .c and .h files in the current directory tree and search them for \"expr\"\n",
        "find -name Pattern File | xargs grep -r Pattern"
    ))
    db.error_temp_pair((
        "find  file which case-insensitive name is too in currect directory\n",
        "find -name Pattern File"
    ))
    db.error_temp_pair((
        "Search directory foo for files containing \"foo/bar\" in their full names\n",
        "find foo -type f -iname foo | grep foo" 
    ))
    db.correct_temp_pair((
        "Search the current directory tree for files containing \"sh\" in their names\n",
        "find -name Pattern File"
    ))
    db.error_temp_pair((
        "display all sqlite files in the current directory along with their timestamp\n",
        "find -name Pattern File"
    ))
    db.error_str_pair((
        "find  file which case-insensitive name is too in currect directory\n",
        "find . -iname \"filename\""
    ))
    db.error_str_pair((
        "find in the file system for a specific file\n",
        "find / -name 'top???'"
    ))
    db.error_str_pair((
        "search for files with the name \"temp\" in the /usr folder\n",
        "find /usr -name '*.sh'"    
    ))
    db.error_str_pair((
        "Find all the files called FindCommandExamples.txt of owner root\n",
        "find / -user root -name tecmint.txt"
    ))
    db.error_str_pair((
        "Find all .c and .h files in the current directory tree and search them for \"expr\"\n",
        "find . -name \"*.c\" | xargs grep -E 'expr'"
    ))
    db.error_str_pair((
        "List all empty files in the current directory tree\n",
        "find . -empty"
    ))
