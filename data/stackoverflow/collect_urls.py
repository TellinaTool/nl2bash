"""
Compute the set of URLs which contains command lines that contains a specific
utility.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import html
import pickle
import re
import sqlite3
import sys
sys.path.append('../../')

from bashlint import bash, data_tools

CODE_REGEX = re.compile(r"<pre><code>([^<]+)<\/code><\/pre>")

def extract_code(text):
    for match in CODE_REGEX.findall(text):
        if match.strip():
            yield html.unescape(match.replace("<br>", "\n"))

def extract_oneliner_from_code(code_block):
    for cmd in code_block.splitlines():
        if cmd.startswith('$ '):
            cmd = cmd[2:]
        if cmd.startswith('# '):
            cmd = cmd[2:]
        comment = re.search(r'\s+#\s+', cmd)
        if comment:
            old_cmd = cmd
            cmd = cmd[:comment.start()]
            print('Remove comment: {} -> {}'.format(old_cmd, cmd))
        cmd = cmd.strip()

        # discard code block opening line
        if not cmd.endswith('{') and not cmd.endswith('[') and not cmd.endswith('('):
            yield cmd
            
def run():
    sqlite_filename = sys.argv[1]
    url_prefix = 'https://stackoverflow.com/questions/'

    urls = {}
    commands = {}

    with sqlite3.connect(sqlite_filename, detect_types=sqlite3.PARSE_DECLTYPES) as db:
        count = 0
        for post_id, answer_body in db.cursor().execute("""
                SELECT questions.Id, answers.Body FROM questions, answers
                WHERE questions.Id = answers.ParentId
                ORDER BY questions.Score DESC"""):
            print(post_id)
            for code_block in extract_code(answer_body):
                for cmd in extract_oneliner_from_code(code_block):
                    print('command string: {}'.format(cmd))
                    ast = data_tools.bash_parser(cmd)
                    if not ast:
                        continue
                    utilities = data_tools.get_utilities(ast)
                    for utility in utilities:
                        if utility in bash.top_100_utilities:
                            print('extracted: {}, {}'.format(utility, cmd))
                            temp = data_tools.ast2template(ast, loose_constraints=True)
                            if not utility in commands:
                                commands[utility] = {}
                                commands[utility][temp] = cmd
                                urls[utility] = {'{}{}'.format(url_prefix, post_id)}
                            else:
                                if len(commands[utility]) >= 40:
                                    continue
                                if not temp in commands[utility]:
                                    commands[utility][temp] = cmd
                                    urls[utility].add('{}{}'.format(url_prefix, post_id))
            count += 1
            if count % 1000 == 0:
                completed = False
                for utility in bash.top_100_utilities:
                    if not utility in commands or len(commands[utility]) < 40:
                        completed = False
                    else:
                        print('{} collection done.'.format(utility))

                if completed:
                    break

    with open('stackoverflow.urls', 'wb') as o_f:
        pickle.dump(urls, o_f)
    with open('stackoverflow.commands', 'wb') as o_f:
        pickle.dump(commands, o_f)

    for utility in commands:
        print('{} ({})'.format(utility, len(commands[utility])))
        for cmd in commands[utility]:
            print(cmd)

if __name__ == "__main__":
    run()
