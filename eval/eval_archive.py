"""
Database which stores model predictions and manual judgements.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
import sqlite3

sys.path.append(os.path.dirname(__file__))
from eval_correction import *


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

        c.execute("CREATE TABLE IF NOT EXISTS NL (id INTEGER PRIMARY KEY, nl TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS Cmd (id INTEGER PRIMARY KEY, cmd TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS Temp (id INTEGER PRIMARY KEY, temp TEXT)")

        c.execute("CREATE TABLE IF NOT EXISTS ModelOutput ("
                  "model TEXT,"
                  "nl_id INT,"
                  "cmd_id INT,"
                  "score FLOAT,"
                  "FOREIGN KEY(nl_id) REFERENCES NL(id),"
                  "FOREIGN KEY(cmd_id) REFERENCES Cmd(id)"
                  ")")
        c.execute("CREATE TABLE IF NOT EXISTS Output ("
                  "model TEXT, nl TEXT, pred_cmd TEXT, score FLOAT)")

        c.execute("CREATE TABLE IF NOT EXISTS CmdTED ("
                  "cmd1_id INT,"
                  "cmd2_id INT,"
                  "dist FLOAT,"
                  "FOREIGN KEY(cmd1_id) REFERENCES Cmd(id),"
                  "FOREIGN KEY(cmd2_id) REFERENCES Cmd(id)"
                  ")")
        c.execute("CREATE TABLE IF NOT EXISTS StrTED (cmd1 TEXT, cmd2 TEXT, dist FLOAT)")

        c.execute("CREATE TABLE IF NOT EXISTS TempTED2 (cmd1 TEXT, cmd2 TEXT, dist FLOAT)")
        c.execute("CREATE TABLE IF NOT EXISTS TempTED ("
                  "temp1_id INT,"
                  "temp2_id INT,"
                  "dist FLOAT,"
                  "FOREIGN KEY(temp1_id) REFERENCES Temp(id),"
                  "FOREIGN KEY(temp2_id) REFERENCES Temp(id)"
                  ")")

        c.execute("CREATE TABLE IF NOT EXISTS CmdJudge ("
                  "nl_id INT,"
                  "cmd_id INT,"
                  "judgement INT,"
                  "FOREIGN KEY(nl_id) REFERENCES NL(id),"
                  "FOREIGN KEY(cmd_id) REFERENCES Cmd(id)"
                  ")")
        c.execute("CREATE TABLE IF NOT EXISTS StrArchives (nl TEXT, pred_cmd TEXT, judgement INT)")

        c.execute("CREATE TABLE IF NOT EXISTS TempJudge ("
                  "nl_id INT,"
                  "temp_id INT,"
                  "judgement INT,"
                  "FOREIGN KEY(nl_id) REFERENCES NL(id),"
                  "FOREIGN KEY(temp_id) REFERENCES Cmd(id)"
                  ")")
        c.execute("CREATE TABLE IF NOT EXISTS TempArchives (nl TEXT, pred_temp TEXT, judgement INT)")

        self.conn.commit()

    def migration(self):
        c = self.cursor
        
        old_outputs = []
        for model, nl, pred_cmd, score in c.execute("SELECT * FROM Output"):
            old_outputs.append((model, nl, pred_cmd, score))
        for model, nl, pred_cmd, score in old_outputs:
            print(model, nl, pred_cmd, score)
            nl_id = self.add_nl(nl)
            cmd_id = self.add_cmd(pred_cmd)
            c.execute("INSERT INTO ModelOutput (model, nl_id, cmd_id, score) VALUES (?, ?, ?, ?)",
                      (model, nl_id, cmd_id, score))
            self.conn.commit()

        """for cmd1, cmd2, dist in c.execute("SELECT * FROM StrTED"):
            cmd1_id = self.add_cmd(cmd1)
            cmd2_id = self.add_cmd(cmd2)
            c.execute("INSERT INTO CmdTED (cmd1_id, cmd2_id, dist) VALUES (?, ?, ?)",
                      (cmd1_id, cmd2_id, dist))
            self.conn.commit()

        for temp1, temp2, dist in c.execute("SELECT * FROM TempTED2"):
            temp1_id = self.add_temp(temp1)
            temp2_id = self.add_temp(temp2)
            c.execute("INSERT INTO TempTED (temp1_id, temp2_id, dist) VALUES (?, ?, ?)",
                      (temp1_id, temp2_id, dist))
            self.conn.commit()

        for nl, cmd, judgement in c.execute("SELECT * FROM StrArchives"):
            nl_id = self.add_nl(nl)
            cmd_id = self.add_cmd(cmd)
            c.execute("INSERT INTO CmdJudge (nl_id, cmd_id, judgement) VALUES (?, ?, ?)",
                      (nl_id, cmd_id, judgement))
            self.conn.commit()

        for nl, temp, judgement in c.execute("SELECT nl, pred_temp, judgement FROM TempArchives"):
            nl_id = self.add_nl(nl, c)
            temp_id = self.add_temp(temp, c)
            c.execute("INSERT INTO TempJudge (nl_id, temp_id, judgement) VALUES (?, ?, ?)",
                      (nl_id, temp_id, judgement))
            self.conn.commit()
        """

    def add_nl(self, nl):
        nl = unicode(nl)
        nl_id = self.get_nl_id(nl)
        if nl_id is not None:
            return nl_id
        c = self.cursor
        c.execute("INSERT INTO NL (nl) VALUES (?)", (nl,))
        self.conn.commit()
        return c.lastrowid

    def get_nl_id(self, nl):
        nl = unicode(nl)
        c = self.cursor
        for id, _ in c.execute("SELECT * FROM NL WHERE nl = ?", (nl,)):
            return id

    def add_cmd(self, cmd):
        cmd = unicode(cmd)
        cmd_id = self.get_cmd_id(cmd)
        if cmd_id is not None:
            return cmd_id
        c = self.cursor
        c.execute("INSERT INTO Cmd (cmd) VALUES (?)", (cmd,))
        self.conn.commit()
        return c.lastrowid

    def get_cmd_id(self, cmd):
        cmd = unicode(cmd)
        c = self.cursor
        for id, _ in c.execute("SELECT * FROM Cmd WHERE cmd = ?", (cmd,)):
            return id

    def add_temp(self, temp):
        temp = unicode(temp)
        temp_id = self.get_temp_id(temp)
        if temp_id is not None:
            return temp_id
        c = self.cursor
        c.execute("INSERT INTO Temp (temp) VALUES (?)", (temp,))
        self.conn.commit()
        return c.lastrowid

    def get_temp_id(self, temp):
        temp = unicode(temp)
        c = self.cursor
        for id, _ in c.execute("SELECT * FROM Temp WHERE temp = ?", (temp,)):
            return id

    # --- Tree Edit Distance ---
    def add_str_dist(self, cmd1, cmd2, dist):
        cmd1 = unicode(cmd1)
        cmd2 = unicode(cmd2)
        c = self.cursor
        c.execute("INSERT INTO StrTED (cmd1, cmd2, dist) VALUES (?, ?, ?)", (cmd1, cmd2, dist))
        self.conn.commit()

    def add_temp_dist(self, cmd1, cmd2, dist):
        cmd1 = unicode(cmd1)
        cmd2 = unicode(cmd2)
        c = self.cursor
        c.execute("INSERT INTO TempTED (cmd1, cmd2, dist) VALUES (?, ?, ?)", (cmd1, cmd2, dist))
        self.conn.commit()

    def get_str_dist(self, cmd1, cmd2):
        cmd1 = unicode(cmd1)
        cmd2 = unicode(cmd2)
        c = self.cursor
        for _, _, dist in \
            c.execute("SELECT cmd1, cmd2, dist FROM StrTED WHERE cmd1 = ? AND cmd2 = ?", (cmd1, cmd2)):
            return dist

    def get_temp_dist(self, cmd1, cmd2):
        cmd1 = unicode(cmd1)
        cmd2 = unicode(cmd2)
        c = self.cursor
        for _, _, dist in \
            c.execute("SELECT cmd1, cmd2, dist FROM TempTED WHERE cmd1 = ? AND cmd2 = ?", (cmd1, cmd2)):
            return dist

    # --- Prediction ---
    def add_prediction(self, model, nl, pred_cmd, score, update_mode=True):
        nl = unicode(nl)
        pred_cmd = unicode(pred_cmd)
        c = self.cursor
        if update_mode and self.exist_prediction(model, nl):
            c.execute("UPDATE Output SET pred_cmd = ? score = ? WHERE model = ? AND nl = ?",
                      (pred_cmd, score, model, nl))
        else:
            if self.exist_score(model, nl, pred_cmd):
                if update_mode:
                    c.execute("UPDATE Output SET score = ? WHERE model = ? AND nl = ? AND pred_cmd = ?",
                          (score, model, nl, pred_cmd))
            else:
                c.execute("INSERT INTO Output (model, nl, pred_cmd, score) VALUES (?, ?, ?, ?)",
                      (model, nl, pred_cmd, score))
        self.conn.commit()

    def remove_model(self, model):
        print("removing record of {} from database".format(model))
        c = self.cursor
        c.execute("DELETE FROM Output WHERE model = ?", (model,))

    def exist_score(self, model, nl, pred_cmd):
        nl = unicode(nl)
        pred_cmd = unicode(pred_cmd)
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM Output WHERE model = ? AND nl = ? AND pred_cmd = ?",
                           (model, nl, pred_cmd)):
            return True
        return False

    def exist_prediction(self, model, nl):
        nl = unicode(nl)
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM Output WHERE model = ? AND nl = ?", (model, nl)):
            return True
        return False

    def get_prediction(self, model, nl):
        nl = unicode(nl)
        return self.get_top_k_predictions(model, nl, 1)[0]

    def get_top_k_predictions(self, model, nl, k):
        nl = unicode(nl)
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
        nl = unicode(nl)
        c = self.cursor
        if not self.exist_str_pair((nl, pred_cmd)):
            c.execute("INSERT INTO StrArchives (nl, pred_cmd, judgement) VALUES (?, ?, ?)",
                      (nl, pred_cmd, judgement))
        self.conn.commit()

    def add_temp_judgement(self, triple):
        nl, pred_temp, judgement = triple
        nl = unicode(nl)
        c = self.cursor
        if not self.exist_temp_pair((nl, pred_temp)):
            c.execute("INSERT INTO TempArchives (nl, pred_temp, judgement) VALUES (?, ?, ?)",
                      (nl, pred_temp, judgement))
        self.conn.commit()

    def get_str_judgement(self, pair):
        nl, pred_cmd = pair
        nl = unicode(nl)
        c = self.cursor
        for _, _, judgement in c.execute("SELECT nl, pred_cmd, judgement FROM StrArchives WHERE nl = ? AND pred_cmd = ?",
                                         (nl, pred_cmd)):
            return judgement

    def get_temp_judgement(self, pair):
        nl, pred_temp = pair
        nl = unicode(nl)
        c = self.cursor
        for _, _, judgement in c.execute("SELECT nl, pred_temp, judgement FROM TempArchives WHERE nl = ? AND pred_temp = ?",
                                         (nl, pred_temp)):
            return judgement

    def exist_str_pair(self, pair):
        nl, pred_cmd = pair
        nl = unicode(nl)
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM StrArchives WHERE nl = ? AND pred_cmd = ?", (nl, pred_cmd)):
            return True
        return False

    def exist_temp_pair(self, pair):
        nl, pred_temp = pair
        nl = unicode(nl)
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM TempArchives WHERE nl = ? AND pred_temp = ?", (nl, pred_temp)):
            return True
        return False

    def correct_str_pair(self, pair):
        nl, pred_cmd = pair
        nl = unicode(nl)
        c = self.cursor
        c.execute("UPDATE StrArchives SET judgement = ? WHERE nl = ? AND pred_cmd = ?",
                  (1, nl, pred_cmd))
        self.conn.commit()

    def correct_temp_pair(self, pair):
        nl, pred_temp = pair
        nl = unicode(nl)
        c = self.cursor
        c.execute("UPDATE TempArchives SET judgement = ? WHERE nl = ? AND pred_temp = ?",
                  (1, nl, pred_temp))
        self.conn.commit()

    def error_str_pair(self, pair):
        nl, pred_cmd = pair
        nl = unicode(nl)
        c = self.cursor
        c.execute("UPDATE StrArchives SET judgement = ? WHERE nl = ? AND pred_cmd = ?",
                  (0, nl, pred_cmd))
        self.conn.commit()

    def error_temp_pair(self, pair):
        nl, pred_temp = pair
        nl = unicode(nl)
        c = self.cursor
        c.execute("UPDATE TempArchives SET judgement = ? WHERE nl = ? AND pred_temp = ?",
                  (0, nl, pred_temp))
        self.conn.commit()

    def get_nl_pred_cmd(self, nl):
        nl = unicode(nl)
        c = self.cursor
        for nl, pred_cmd, judgement in c.execute("SELECT nl, pred_cmd, judgement FROM StrArchives WHERE nl = ?", (nl,)):
            print(nl)
            print(pred_cmd) 
            print(judgement)

    def get_nl_pred_temp(self, nl):
        nl = unicode(nl)
        c = self.cursor
        for nl, pred_temp, judgement in c.execute("SELECT nl, pred_temp, judgement FROM TempArchives WHERE nl = ?",
                                                  (nl,)):
            print(nl, pred_temp, judgement)

    def get_correct_temps(self, nl):
        nl = unicode(nl)
        c = self.cursor
        temps = []
        for nl, pred_temp, judgement in c.execute("SELECT nl, pred_temp, judgement FROM "
                                                 "TempArchives WHERE nl = ? AND judgement = 1",
                                                  (nl,)):
            temps.append(pred_temp)
        return temps

    def correction(self):
        for pair in correct_temp_pairs:
            self.correct_temp_pair(pair)
        for pair in correct_str_pairs:
            self.correct_str_pair(pair)
        for pair in error_temp_pairs:
            self.error_temp_pair(pair)
        for pair in error_str_pairs:
            self.error_str_pair(pair)
       
    def debug(self):
        c = self.cursor
        for model, nl, pred_cmd, score in c.execute("SELECT model, nl, pred_cmd, score FROM Output"):
            if "*.tex" in nl:
                print(model)
                print(nl)
                print(pred_cmd)
                print(score)                
 
if __name__ == "__main__":
    db = DBConnection()
    db.create_schema()
    db.migration()
