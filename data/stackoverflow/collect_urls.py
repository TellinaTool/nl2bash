"""
Compute the set of URLs which contains command lines that contains a specific
utility.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import html
import re
import sqlite3
import sys

from bashlex import bash, data_tools

CODE_REGEX = re.compile(r"<pre><code>([^<]+)<\/code><\/pre>")

def extract_code(text):
    for match in CODE_REGEX.findall(text):
        if match.strip():
            yield html.unescape(match.replace("<br>", "\n"))


def run():
    sqlite_filename = sys.argv[1]
    url_prefix = 'https://stackoverflow.com/questions/'

    urls = {}
    commands = {}

    with sqlite3.connect(sqlite_filename, detect_types=sqlite3.PARSE_DECLTYPES) as db:
        count = 0
        for (post_id, answer_body) in db.cursor().execute("""
                SELECT questions.Id, answers.Body FROM questions, answers
                ORDER BY questions.FavoriteCount DESC
                WHERE questions.Id = answers.ParentId"""):
            for cmd in extract_code(answer_body):
                commands.append(cmd)
                ast = data_tools.bash_parser(cmd)
                utilities = data_tools.get_utilities(ast)
                for utility in utilities:
                    if utility in bash.top_100_utilities:
                        if not utility in commands:
                            commands[utility] = {cmd}
                            urls[utility] = {url_prefix + post_id}
                        else:
                            if not cmd in commands[utility]:
                                if len(commands[utility]) > 40:
                                    continue
                                commands[utility].add(cmd)
                                urls[utility].add(url_prefix + post_id)
            count += 1
            if count % 1000 == 0:
                completed = False
                for utility in bash.top_100_utilities:
                    if not utility in commands or len(commands[utility]) < 40:
                        completed = False

            if completed:
                break

    for utility in urls:
        print(utility)
        print(urls[utility])