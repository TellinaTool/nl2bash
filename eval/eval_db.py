"""
Database which stores model predictions and manual judgements.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os, sys
import sqlite3


class DBConnection(object):
    def __init__(self, db_path="eval_archive.db"):
        self.conn = sqlite3.connect(
            os.path.join(os.path.dirname(__file__), db_path),
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

        c.execute("CREATE TABLE IF NOT EXISTS CmdTED ("
                  "cmd1_id INT,"
                  "cmd2_id INT,"
                  "dist FLOAT,"
                  "FOREIGN KEY(cmd1_id) REFERENCES Cmd(id),"
                  "FOREIGN KEY(cmd2_id) REFERENCES Cmd(id)"
                  ")")
        
        c.execute("CREATE TABLE IF NOT EXISTS TempTED ("
                  "temp1_id INT,"
                  "temp2_id INT,"
                  "dist FLOAT,"
                  "FOREIGN KEY(temp1_id) REFERENCES Temp(id),"
                  "FOREIGN KEY(temp2_id) REFERENCES Temp(id)"
                  ")")

        # Manual judgement for pairs
        c.execute("CREATE TABLE IF NOT EXISTS CmdJudge ("
                  "nl_id INT,"
                  "cmd_id INT,"
                  "judgement INT,"
                  "FOREIGN KEY(nl_id) REFERENCES NL(id),"
                  "FOREIGN KEY(cmd_id) REFERENCES Cmd(id)"
                  ")")

        c.execute("CREATE TABLE IF NOT EXISTS TempJudge ("
                  "nl_id INT,"
                  "temp_id INT,"
                  "judgement INT,"
                  "FOREIGN KEY(nl_id) REFERENCES NL(id),"
                  "FOREIGN KEY(temp_id) REFERENCES Cmd(id)"
                  ")")

        self.conn.commit()

    def add_nl(self, nl):
        nl = str(nl, 'utf-8') if not type(nl) is str else nl
        nl_id = self.get_nl_id(nl)
        if nl_id is not None:
            return nl_id
        c = self.cursor
        c.execute("INSERT INTO NL (nl) VALUES (?)", (nl,))
        self.conn.commit()
        return c.lastrowid

    def get_nl_id(self, nl):
        # nl = bytes(nl, 'utf-8')
        c = self.cursor
        for id, _ in c.execute("SELECT * FROM NL WHERE nl = ?", (nl,)):
            return id

    def add_cmd(self, cmd):
        cmd = str(cmd, 'utf-8') if not type(cmd) is str else cmd
        cmd_id = self.get_cm_id(cmd)
        if cmd_id is not None:
            return cmd_id
        c = self.cursor
        c.execute("INSERT INTO Cmd (cmd) VALUES (?)", (cmd,))
        self.conn.commit()
        return c.lastrowid

    def get_cm_id(self, cmd):
        cmd = bytes(cmd, 'utf-8')
        c = self.cursor
        for id, _ in c.execute("SELECT * FROM Cmd WHERE cmd = ?", (cmd,)):
            return id

    def add_temp(self, temp):
        temp = str(temp, 'utf-8') if not type(temp) is str else temp
        temp_id = self.get_temp_id(temp)
        if temp_id is not None:
            return temp_id
        c = self.cursor
        c.execute("INSERT INTO Temp (temp) VALUES (?)", (temp,))
        self.conn.commit()
        return c.lastrowid

    def get_temp_id(self, temp):
        temp = str(temp, 'utf-8') if not type(temp) is str else temp
        c = self.cursor
        for id, _ in c.execute("SELECT * FROM Temp WHERE temp = ?", (temp,)):
            return id

    # --- Tree Edit Distance ---
    def add_str_dist(self, cmd1, cmd2, dist):
        cmd1_id = self.add_cmd(cmd1)
        cmd2_id = self.add_cmd(cmd2)
        c = self.cursor
        c.execute("INSERT INTO CmdTED (cmd1_id, cmd2_id, dist) VALUES (?, ?, ?)",
                  (cmd1_id, cmd2_id, dist))
        self.conn.commit()

    def add_temp_dist(self, temp1, temp2, dist):
        temp1_id = self.add_temp(temp1)
        temp2_id = self.add_temp(temp2)
        c = self.cursor
        c.execute("INSERT INTO TempTED (temp1_id, temp2_id, dist) VALUES (?, ?, ?)",
                  (temp1_id, temp2_id, dist))
        self.conn.commit()

    def get_str_dist(self, cmd1, cmd2):
        cmd1_id = self.get_cm_id(cmd1)
        if cmd1_id is None:
            return None
        cmd2_id = self.get_cm_id(cmd2)
        if cmd2_id is None:
            return None
        c = self.cursor
        for _, _, dist in c.execute(
                "SELECT cmd1_id, cmd2_id, dist FROM CmdTED WHERE cmd1_id = ?, "
                "cmd2_id = ?", (cmd1_id, cmd2_id)):
            return dist

    def get_temp_dist(self, temp1, temp2):
        temp1_id = self.get_temp_id(temp1)
        if temp1_id is None:
            return None
        temp2_id = self.get_temp_id(temp2)
        if temp2_id is None:
            return None
        c = self.cursor
        for _, _, dist in c.execute(
                "SELECT temp1_id, temp2_id, dist FROM TempTED WHERE temp1_id "
                "= ? AND temp2_id = ?", (temp1_id, temp2_id)):
            return dist

    # --- Prediction --- #

    def add_prediction(self, model, nl, pred_cmd, score, update_mode=True):
        nl = bytes(nl, 'utf-8')
        pred_cmd = bytes(pred_cmd, 'utf-8')
        nl_id = self.add_nl(nl)
        cmd_id = self.add_cmd(pred_cmd)
        c = self.cursor
        if update_mode and self.exist_prediction(model, nl):
            c.execute("UPDATE ModelOutput SET cmd_id = ? score = ? WHERE model = ? AND nl_id = ?",
                      (cmd_id, score, model, nl_id))
        else:
            c.execute("INSERT INTO ModelOutput (model, nl_id, cmd_id, score) VALUES (?, ?, ?, ?)",
                      (model, nl_id, cmd_id, score))
        self.conn.commit()

    def remove_model(self, model):
        print("removing record of {} from database".format(model))
        c = self.cursor
        c.execute("DELETE FROM ModelOutput WHERE model = ?", (model,))

    def exist_prediction(self, model, nl):
        nl_id = self.get_nl_id(nl)
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM ModelOutput WHERE model = ? AND nl_id = ?",
                           (model, nl_id)):
            return True
        return False

    def get_prediction(self, model, nl):
        return self.get_top_k_predictions(model, nl, 1)[0]

    def get_top_k_predictions(self, model, nl, k):
        nl = str(nl, 'utf-8') if not isinstance(nl, str) else nl
        c = self.cursor
        predictions = []
        for score, pred_cmd in \
            c.execute("SELECT ModelOutput.score, Cmd.cmd FROM ModelOutput "
                      "JOIN NL ON ModelOutput.nl_id = NL.id "
                      "JOIN Cmd ON ModelOutput.cmd_id = Cmd.id "
                      "WHERE ModelOutput.model = ? AND "
                      "NL.nl = ?", (model, nl)):
            predictions.append((pred_cmd, score))
        sorted_predictions = sorted(predictions, key=lambda x:x[1], reverse=True)
        return sorted_predictions[:k]

    # --- Manual Evaluation --- #
    
    def add_str_judgement(self, triple):
        nl, pred_cmd, judgement = triple
        c = self.cursor
        if not self.exist_str_pair((nl, pred_cmd)):
            nl_id = self.add_nl(nl)
            cmd_id = self.add_cmd(pred_cmd)
            c.execute("INSERT INTO CmdJudge (nl_id, cmd_id, judgement) VALUES (?, ?, ?)",
                      (nl_id, cmd_id, judgement))
        self.conn.commit()

    def get_str_judgement(self, pair):
        nl, pred_cmd = pair
        c = self.cursor
        for _, _, judgement in c.execute("SELECT CmdJudge.nl_id, CmdJudge.cmd_id, "
                                         "CmdJudge.judgement FROM CmdJudge "
                                         "JOIN Cmd ON CmdJudge.cmd_id = Cmd.id "
                                         "JOIN NL ON CmdJudge.nl_id = NL.id "
                                         "WHERE NL.nl = ? AND Cmd.cmd = ?",
                                         (nl, pred_cmd)):
            return judgement

    def exist_str_pair(self, pair):
        nl, pred_cmd = pair
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM CmdJudge "
                           "JOIN Cmd ON CmdJudge.cmd_id = Cmd.id "
                           "JOIN NL ON CmdJudge.nl_id = NL.id "
                           "WHERE NL.nl = ? AND Cmd.cmd = ?", (nl, pred_cmd)):
            return True
        return False

    def add_temp_judgement(self, triple):
        nl, pred_temp, judgement = triple
        c = self.cursor
        if not self.exist_temp_pair((nl, pred_temp)):
            nl_id = self.add_nl(nl)
            temp_id = self.add_temp(pred_temp)
            c.execute("INSERT INTO TempJudge (nl_id, temp_id, judgement) VALUES (?, ?, ?)",
                      (nl_id, temp_id, judgement))
        self.conn.commit()

    def exist_temp_pair(self, pair):
        nl, pred_temp = pair
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM TempJudge "
                           "JOIN Temp ON TempJudge.temp_id = Temp.id "
                           "JOIN NL ON TempJudge.nl_id = NL.id "
                           "WHERE NL.nl = ? AND Temp.temp = ?", (nl, pred_temp)):
            return True
        return False

    def get_temp_judgement(self, pair):
        nl, pred_temp = pair
        c = self.cursor
        for _, _, judgement in c.execute("SELECT TempJudge.nl_id, TempJudge.temp_id, "
                                         "TempJudge.judgement FROM TempJudge "
                                         "JOIN Temp ON TempJudge.temp_id = Temp.id "
                                         "JOIN NL ON TempJudge.nl_id = NL.id "
                                         "WHERE NL.nl = ? AND Temp.temp = ?",
                                         (nl, pred_temp)):
            return judgement

    def get_nl_cm_judge(self, nl):
        nl = str(nl, 'utf-8')
        c = self.cursor
        for nl, pred_cmd, judgement in c.execute("SELECT NL.nl, Cmd.cmd, "
                                                 "CmdJudge.judgement FROM CmdJudge "
                                                 "JOIN NL ON CmdJudge.nl_id = NL.id "
                                                 "WHERE NL.nl = ?", (nl,)):
            print("English description: {}".format(nl))
            print("Prediction: {} ({})".format(pred_cmd, judgement))

    def get_nl_temp_judge(self, nl):
        nl = str(nl, 'utf-8')
        c = self.cursor
        for nl, pred_temp, judgement in c.execute("SELECT NL.nl, Temp.temp, "
                                                  "TempJudge.judgement FROM TempJudge "
                                                  "JOIN NL ON TempJudge.nl_id = NL.id "
                                                  "JOIN Temp ON TempJudge.temp_id = Temp.id"
                                                  "WHERE NL.nl = ?", (nl,)):
            print("English description: {}".format(nl))
            print("Prediction: {} ({})".format(pred_temp, judgement))

    def get_correct_cmds(self, nl):
        nl = str(nl, 'utf-8')
        c = self.cursor
        correct_cmds = []
        for pred_cmd, in c.execute("SELECT Cmd.cmd FROM CmdJudge "
                                  "JOIN NL ON CmdJudge.nl_id = NL.id "
                                  "JOIN Cmd ON CmdJudge.cmd_id = Cmd.id "
                                  "WHERE NL.nl = ? AND CmdJudge.judgement = 1", (nl,)):
            correct_cmds.append(pred_cmd)
        return correct_cmds

    def get_correct_temps(self, nl):
        nl = str(nl, 'utf-8') if not isinstance(nl, str) else nl
        c = self.cursor
        correct_temps = []
        for nl, pred_temp, in c.execute("SELECT NL.nl, Temp.temp FROM TempJudge "
                                    "JOIN NL ON TempJudge.nl_id = NL.id "
                                    "JOIN Temp ON TempJudge.temp_id = Temp.id "
                                    "WHERE NL.nl = ? AND TempJudge.judgement = 1", (nl,)):
            correct_temps.append(pred_temp)
        return correct_temps

    # Correction
    def correct_str_pair(self, pair):
        nl, pred_cmd = pair
        nl_id = self.get_nl_id(nl)
        cmd_id = self.get_cm_id(pred_cmd)
        c = self.cursor
        c.execute("UPDATE CmdJudge SET judgement = ? WHERE nl_id = ? AND cmd_id = ?",
                  (1, nl_id, cmd_id))
        self.conn.commit()

    def correct_temp_pair(self, pair):
        nl, pred_temp = pair
        nl_id = self.get_nl_id(nl)
        temp_id = self.get_temp_id(pred_temp)
        c = self.cursor
        c.execute("UPDATE TempJudge SET judgement = ? WHERE nl_id = ? AND temp_id = ?",
                  (1, nl_id, temp_id))
        self.conn.commit()

    def error_str_pair(self, pair):
        nl, pred_cmd = pair
        nl_id = self.get_nl_id(nl)
        cmd_id = self.get_cm_id(pred_cmd)
        c = self.cursor
        c.execute("UPDATE CmdJudge SET judgement = ? WHERE nl_id = ? AND cmd_id = ?",
                  (0, nl_id, cmd_id))
        self.conn.commit()

    def error_temp_pair(self, pair):
        nl, pred_temp = pair
        nl_id = self.get_nl_id(nl)
        temp_id = self.get_temp_id(pred_temp)
        c = self.cursor
        c.execute("UPDATE TempJudge SET judgement = ? WHERE nl_id = ? AND temp_id = ?",
                  (0, nl_id, temp_id))
        self.conn.commit()

    def positive_examples(self):
        positive_examples = collections.defaultdict(set)
        c = self.cursor
        for nl, temp, _, _, judgement in c.execute("SELECT NL.nl, Temp.temp, "
                                                   "TempJudge.nl_id, TempJudge.temp_id, "
                                                   "TempJudge.judgement FROM TempJudge "
                                                   "JOIN NL ON TempJudge.nl_id = NL.id "
                                                   "JOIN Temp ON TempJudge.temp_id = Temp.id "
                                                   "WHERE TempJudge.judgement = 1"):
            positive_examples[nl].add(temp)

        for nl, cmds in sorted(positive_examples.items(),
                               key=lambda x:len(x[1]), reverse=True)[:20]:
            print("English description: {}".format(nl.strip()))
            cmds = list(cmds)
            for i in xrange(len(cmds)):
                print("Prediction {}: {}".format(i, cmds[i]))

       
    def debug(self):
        c = self.cursor
        for nl, temp, _, _, judgement in c.execute("SELECT NL.nl, Temp.temp, "
                                                   "TempJudge.nl_id, TempJudge.temp_id, "
                                                   "TempJudge.judgement FROM TempJudge "
                                                   "JOIN NL ON TempJudge.nl_id = NL.id "
                                                   "JOIN Temp ON TempJudge.temp_id = Temp.id "
                                                   "WHERE TempJudge.judgement = 1"):
            print("English description: {}".format(nl.strip()))
            print("Prediction: {} ({})".format(temp, judgement))
            print()

    def clear_model_output(self):
        c = self.cursor
        c.execute("DELETE FROM ModelOutput")
        c.execute("VACUUM")
        self.conn.commit()


def import_from_table():
    db_path1 = sys.argv[1]
    db_path2 = sys.argv[2]
    db1 = DBConnection(db_path1)
    db2 = DBConnection(db_path2)
    for nl, cmd in db1.cursor.execute("SELECT NL.nl, Cmd.cmd FROM CmdJudge "
                             "JOIN NL ON CmdJudge.nl_id = NL.id "
                             "JOIN Cmd ON CmdJudge.cmd_id = Cmd.id "
                             "WHERE CmdJudge.judgement = 1"):
        print("cmd judgement: {}".format((nl.strip(), cmd.strip(), 1)))
        db2.add_str_judgement((nl.strip(), cmd.strip(), 1))
    for nl, temp in db1.cursor.execute("SELECT NL.nl, Temp.temp FROM TempJudge "
                              "JOIN NL ON TempJudge.nl_id = NL.id "
                              "JOIN Temp ON TempJudge.temp_id = Temp.id "
                              "WHERE TempJudge.judgement = 1"):
        print("temp judgement: {}".format((nl.strip(), temp.strip(), 1)))
        db2.add_temp_judgement((nl.strip(), temp.strip(), 1))


if __name__ == "__main__":
    db = DBConnection()
    db.create_schema()
    import_from_table()
