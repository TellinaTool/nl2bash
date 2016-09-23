# builtin
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

        c.execute("CREATE TABLE IF NOT EXISTS StrArchives (nl TEXT, str TEXT, judgement INT)")
        c.execute("CREATE TABLE IF NOT EXISTS TempArchives (nl TEXT, temp TEXT, judgement INT)")

        self.conn.commit()

    def add_str_judgement(self, triple):
        c = self.cursor
        if not self.exist_str_pair((triple[0], triple[1])):
            c.execute("INSERT INTO StrArchives (nl, str, judgement) VALUES (?, ?, ?)", triple)
        self.conn.commit()

    def add_temp_judgement(self, triple):
        c = self.cursor
        if not self.exist_temp_pair((triple[0], triple[1])):
            c.execute("INSERT INTO TempArchives (nl, temp, judgement) VALUES (?, ?, ?)", triple)
        self.conn.commit()

    def get_str_judgement(self, pair):
        c = self.cursor
        for _, _, judgement in c.execute("SELECT nl, str, judgement FROM StrArchives WHERE nl = ? AND str = ?", pair):
            return judgement

    def get_temp_judgement(self, pair):
        c = self.cursor
        for _, _, judgement in c.execute("SELECT nl, temp, judgement FROM TempArchives WHERE nl = ? AND temp = ?", pair):
            return judgement

    def exist_str_pair(self, pair):
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM StrArchives WHERE nl = ? AND str = ?", pair):
            return True
        return False

    def exist_temp_pair(self, pair):
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM TempArchives WHERE nl = ? AND temp = ?", pair):
            return True
        return False

    def correct_str_pair(self, pair):
        judgement = self.get_str_judgement(pair)
        c = self.cursor
        c.execute("UPDATE StrArchives SET judgement = ? WHERE nl = ? AND str = ?",
                  (1, pair[0], pair[1]))
        self.conn.commit()

    def correct_temp_pair(self, pair):
        judgement = self.get_temp_judgement(pair)
        c = self.cursor
        c.execute("UPDATE TempArchives SET judgement = ? WHERE nl = ? AND temp = ?",
                  (1, pair[0], pair[1]))
        self.conn.commit()

    def error_str_pair(self, pair):
        judgement = self.get_str_judgement(pair)
        c = self.cursor
        c.execute("UPDATE StrArchives SET judgement = ? WHERE nl = ? AND str = ?",
                  (0, pair[0], pair[1]))
        self.conn.commit()

    def error_temp_pair(self, pair):
        judgement = self.get_temp_judgement(pair)
        c = self.cursor
        c.execute("UPDATE TempArchives SET judgement = ? WHERE nl = ? AND temp = ?",
                  (0, pair[0], pair[1]))
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
