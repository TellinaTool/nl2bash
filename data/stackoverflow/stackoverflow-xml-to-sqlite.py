#!/usr/bin/env python3
"""
StackOverflow data dumps are available from here:
    https://archive.org/details/stackexchange

These dumps come as XML files compressed with 7ZIP. This script converts that
horrible format into an SQLite database. It only keeps "interesting" questions;
see the `is_interesting()` function.

Usage:
    $ python3 script.py 'path/to/Posts.xml' 'out.sqlite3db'

The tool reads from stdin if you give '-' as the first argument. If you have pv
installed you can use this feature to get a nice progress bar:
    $ pv 'path/to/Posts.xml' | python3 script.py - 'out.sqlite3db'

Here is the input data schema, from the readme distributed with the data:

   - **posts**.xml
       - Id
       - PostTypeId
          - 1: Question
          - 2: Answer
       - ParentID (only present if PostTypeId is 2)
       - AcceptedAnswerId (only present if PostTypeId is 1)
       - CreationDate="2009-03-05T22:28:34.823"
       - Score
       - ViewCount (only present if PostTypeId is 1)
       - Body
       - OwnerUserId (optional)
       - LastEditorUserId
       - LastEditorDisplayName="Jeff Atwood"
       - LastEditDate="2009-03-05T22:28:34.823" (optional)
       - LastActivityDate="2009-03-11T12:51:01.480"
       - CommunityOwnedDate="2009-03-11T12:51:01.480" (optional, only present if PostTypeId is 1)
       - ClosedDate="2009-03-11T12:51:01.480" (optional, only present if PostTypeId is 1)
       - Title (only present if PostTypeId is 1)
       - Tags="<tag1><tag2>" (only present if PostTypeId is 1)
       - AnswerCount (only present if PostTypeId is 1)
       - CommentCount
       - FavoriteCount (only present if PostTypeId is 1)

The SQLite schemas are in the source code below. I made the following changes:
 - Questions and answers are in separate tables
 - Tags are in a separate "tags" table containing (Id, Tag) tuples
 - Removed LastEditorDisplayName

"""

import datetime
import re
import sqlite3
import sys
import xml.sax

# Only questions containing one of these tags will be included.
INTERESTING_TAGS = set([
    "bash", "sh", "shell", "zsh", "command-line", "linux", "unix",
    "awk", "sed", "xargs", "tar", "rsync", "scp", "mv", "cp"])
def is_interesting(tag):
    return tag in INTERESTING_TAGS

TAG_REGEX = re.compile("<([^<>]+)>")
def parse_tags(tags):
    """Parses tag strings; e.g. '<tag1><tag2>' --> ['tag1', 'tag2']"""
    return set(TAG_REGEX.findall(tags))

def parse_date(datestring):
    """Parses ISO-8601 formatted dates; e.g. 2009-03-05T22:28:34.823"""
    return datetime.datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%S.%f")

QUESTION_TYPE = 1
ANSWER_TYPE = 2

class XMLHandler(xml.sax.handler.ContentHandler):

    def __init__(self, sqlite_conn, sqlite_cursor):
        self.conn = sqlite_conn
        self.cursor = sqlite_cursor
        self.count = 0
        self.included = 0
        self.skipped = 0
        self.failures = 0
        self.question_ids = set()

    def startElement(self, name, attrs):
        super().startElement(name, attrs)
        if name == "row":
            try:

                Id                   = int(attrs["Id"])
                PostTypeId           = int(attrs["PostTypeId"])
                ParentId             = int(attrs["ParentId"]) if "ParentId" in attrs else None
                AcceptedAnswerId     = int(attrs["AcceptedAnswerId"]) if "AcceptedAnswerId" in attrs else None
                CreationDate         = parse_date(attrs["CreationDate"])
                Score                = int(attrs["Score"])
                ViewCount            = int(attrs["ViewCount"]) if "ViewCount" in attrs else None
                Body                 = attrs["Body"]
                OwnerUserId          = int(attrs["OwnerUserId"]) if "OwnerUserId" in attrs else None
                LastEditorUserId     = int(attrs["LastEditorUserId"]) if "LastEditorUserId" in attrs else None
                LastEditDate         = parse_date(attrs["LastEditDate"]) if "LastEditDate" in attrs else None
                LastActivityDate     = parse_date(attrs["LastActivityDate"])
                CommunityOwnedDate   = parse_date(attrs["CommunityOwnedDate"]) if "CommunityOwnedDate" in attrs else None
                ClosedDate           = parse_date(attrs["ClosedDate"]) if "ClosedDate" in attrs else None
                Title                = attrs["Title"] if "Title" in attrs else None
                Tags                 = parse_tags(attrs["Tags"]) if "Tags" in attrs else []
                AnswerCount          = int(attrs["AnswerCount"]) if "AnswerCount" in attrs else 0
                CommentCount         = int(attrs["CommentCount"])
                FavoriteCount        = int(attrs["FavoriteCount"]) if "FavoriteCount" in attrs else 0

                if PostTypeId == QUESTION_TYPE:
                    # Only include "interesting" questions.
                    if any(is_interesting(Tag) for Tag in Tags):
                        self.included += 1
                        self.question_ids.add(Id)
                        self.cursor.execute("""INSERT OR IGNORE INTO
                            questions (Id, AcceptedAnswerId, CreationDate, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, CommunityOwnedDate, ClosedDate, Title, AnswerCount, CommentCount, FavoriteCount)
                            VALUES    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (Id, AcceptedAnswerId, CreationDate, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, CommunityOwnedDate, ClosedDate, Title, AnswerCount, CommentCount, FavoriteCount))
                        for Tag in Tags:
                            self.cursor.execute("""INSERT OR IGNORE INTO tags (Id, Tag) VALUES (?, ?)""", (Id, Tag))
                    else:
                        self.skipped += 1

                elif PostTypeId == ANSWER_TYPE:
                    # Only include answers to "interesting" questions.
                    # NOTE: this is OK since posts are sorted in the input by
                    # creation time; answers always appear after the relevant
                    # question.
                    if ParentId in self.question_ids:
                        self.included += 1
                        self.cursor.execute("""INSERT OR IGNORE INTO
                            answers   (Id, ParentId, CreationDate, Score, Body, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, CommentCount)
                            VALUES    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (Id, ParentId, CreationDate, Score, Body, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, CommentCount))
                    else:
                        self.skipped += 1

                else:
                    raise Exception("unknown PostTypeId {}".format(PostTypeId))

                self.count += 1
                if self.count % 10000 == 0:
                    self.conn.commit()
                    # print("Processed {} rows ({} skipped, {} included)".format(self.count, self.skipped, self.included))

            except Exception as e:
                self.failures += 1
                print("Failure on {}(attrs={}): {}".format(name, attrs, e))

def run():
    in_xml = sys.argv[1]
    if in_xml == '-':
        in_xml = sys.stdin
    out_sqlite = sys.argv[2]

    print("Opening sqlite db {}...".format(out_sqlite))
    with sqlite3.connect(out_sqlite, detect_types=sqlite3.PARSE_DECLTYPES) as sqlite_db:
        sqlite_cursor = sqlite_db.cursor()

        sqlite_cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
            Id                     INT NOT NULL PRIMARY KEY,
            AcceptedAnswerId       INT,
            CreationDate           TIMESTAMP NOT NULL,
            Score                  INT NOT NULL,
            ViewCount              INT NOT NULL,
            Body                   TEXT NOT NULL,
            OwnerUserId            INT,
            LastEditorUserId       INT,
            LastEditDate           TIMESTAMP,
            LastActivityDate       TIMESTAMP NOT NULL,
            CommunityOwnedDate     TIMESTAMP,
            ClosedDate             TIMESTAMP,
            Title                  TEXT NOT NULL,
            AnswerCount            INT NOT NULL,
            CommentCount           INT NOT NULL,
            FavoriteCount          INT NOT NULL)""")

        sqlite_cursor.execute("""CREATE TABLE IF NOT EXISTS answers (
            Id                     INT NOT NULL PRIMARY KEY,
            ParentId               INT,
            CreationDate           TIMESTAMP NOT NULL,
            Score                  INT NOT NULL,
            Body                   TEXT NOT NULL,
            OwnerUserId            INT,
            LastEditorUserId       INT,
            LastEditDate           TIMESTAMP,
            LastActivityDate       TIMESTAMP NOT NULL,
            CommentCount           INT NOT NULL)""")

        sqlite_cursor.execute("""CREATE TABLE IF NOT EXISTS tags (
            Id                     INT NOT NULL,
            Tag                    VARCHAR(256) NOT NULL)""")

        print("Streaming data from {}...".format(in_xml))
        handler = XMLHandler(sqlite_db, sqlite_cursor)
        xml.sax.parse(in_xml, handler)
        sqlite_db.commit()

        print("{} rows inserted + {} skipped, {} failures".format(handler.included, handler.skipped, handler.failures))

        indexes = [
            ("answer_idx",   "",       "answers", "(ParentId)"),
            ("tags_idx",     "UNIQUE", "tags",    "(Id, Tag)"),
            ("tags_rev_idx", "UNIQUE", "tags",    "(Tag, Id)")]

        i = 0
        for idx_name, unique, table, fields in indexes:
            i += 1
            print("Adding index {}/{} on {} {}".format(i, len(indexes), table, fields))
            sqlite_cursor.execute("""CREATE {} INDEX IF NOT EXISTS {} ON {} {}""".format(unique, idx_name, table, fields))

        sqlite_db.commit()

if __name__ == "__main__":
    run()
