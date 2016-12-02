#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from bs4 import BeautifulSoup
import HTMLParser
import socket
import ssl
import urllib2
import httplib2

import sqlite3

import os, sys
import re

from bashlex import data_tools


resources = ["stackoverflow", "superuser", "bashoneliners", "commandlinefu"]

prefixes = {
    "stackoverflow": "http://stackoverflow.com/questions/",
    "superuser": "http://superuser.com/questions/",
    "bashoneliners": "http://www.bashoneliners.com/oneliners/oneliner/",
    "commandlinefu": "http://www.commandlinefu.com/commands/view/"
}

stackoverflow_db = sqlite3.connect(os.path.join("..", "stackoverflow", "stackoverflow.sqlite"),
                                   detect_types=sqlite3.PARSE_DECLTYPES)
superuser_db = sqlite3.connect(os.path.join("..", "stackoverflow", "superuser.sqlite"),
                               detect_types=sqlite3.PARSE_DECLTYPES)


html = HTMLParser.HTMLParser()
CODE_REGEX = re.compile(r"<pre><code>([^<]+)<\/code><\/pre>")
def extract_code(text):
    for match in CODE_REGEX.findall(text):
        if match.strip():
            yield html.unescape(match.replace("<br>", "\n"))


def extract_bashoneliner(url):
    try:
        html = urllib2.urlopen(url, timeout=2)
    except urllib2.URLError, e:
        print("Website (%s) could not be reached due to %s" % (e.url, e.reason))
        # return "", randomstr(180)
        return None, None
    except socket.timeout, e:
        print("Error: extract_text_from_url() socket.timeout")
        # return "", randomstr(180)
        return None, None
    except ssl.SSLError, e:
        print("Error: extract_text_from_url() ssl.SSLError")
        # return "", randomstr(180)
        return None, None

    html = html.read()
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    for span in body.find_all('span', {'class', 'oneliner-line'}):
        oneliner = span.get_text()
    return oneliner


def extract_commandlinefu(url):
    fp = httplib2.Http('.cache')
    response, html = fp.request(url, "GET")

    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    print(url)
    for div in body.find_all('div', {'class', 'command'}):
        oneliner = div.get_text()
        print(oneliner)
    return oneliner

def extract_resource(resource):
    result_tbody = ""

    with open(resource + ".html") as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        tbody = soup.tbody
        for a in tbody.find_all('a', href=True):
            url = a['href']
            prefix = prefixes[resource]
            post_id = url[len(prefix):].split('/')[0]
            post_title = a.get_text()
            oneliner = ''
            # retreive target command from database
            if resource in ["stackoverflow", "superuser"]:
                if resource == "stackoverflow":
                    c = stackoverflow_db.cursor()
                else:
                    c = superuser_db.cursor()
                for (question_id, answer_body) in c.execute("""
                        SELECT questions.Id, answers.Body
                        FROM questions, answers
                        WHERE questions.AcceptedAnswerId = answers.Id 
                        AND questions.Id = ?""", (post_id,)):
                    for extracted_code in extract_code(answer_body):
                        oneliner = extracted_code
                        break

            # retrieve target command from the web
            if resource in ["bashoneliners"]:
                oneliner = extract_bashoneliner(url)

            if resource in ["commandlinefu"]:
                oneliner = ''

            ast = data_tools.bash_parser(oneliner)
            if ast is not None:
                if data_tools.is_simple(ast):
                    result_tbody += "<tr>"
                    result_tbody += "<td>{}</td>".format(resource)
                    result_tbody += "<td>{}</td>".format(post_title.encode('utf-8'))
                    result_tbody += "<td>{}</td>".format(url.encode('utf-8'))
                    result_tbody += "<td>{}</td>".format(oneliner)
                    result_tbody += "</tr>"

    return result_tbody

def extract(outFile):
    table = "<table>"
    for resource in resources:
        print("Resource: {}".format(resource))
        tbody = extract_resource(resource)
        table += tbody
    table += "</table>"

    with open(outFile, 'w') as o_f:
        o_f.write(table)


if __name__ == "__main__":
    outFile = sys.argv[1]
    extract(outFile)
