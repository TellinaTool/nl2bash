from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import numpy as np
import re
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bashlex"))
import sqlite3

import data_utils, data_tools

class DBConnection(object):
    def __init__(self):
        self.conn = sqlite3.connect(
            os.path.join(os.path.dirname(__file__), "model_output.db"),
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

        self.conn.commit()

    def add_prediction(self, model, nl, pred_cmd, score):
        c = self.cursor
        if self.exist_prediction(model, nl):
            c.execute("UPDATE Output SET pred_cmd = ?, score = ? WHERE model = ? AND nl = ?",
                      (pred_cmd, score, model, nl))
        else:
            c.execute("INSERT INTO Output (model, nl, pred_cmd, score) VALUES (?, ?, ?, ?)",
                      (model, nl, pred_cmd, score))
        self.conn.commit()

    def exist_prediction(self, model, nl):
        c = self.cursor
        for _ in c.execute("SELECT 1 FROM Output WHERE model = ? AND nl = ?", (model, nl)):
            return True
        return False

    def get_prediction(self, model, nl):
        c = self.cursor
        for _, _, pred_cmd, score in \
                c.execute("SELECT model, nl, pred_cmd, score FROM Output WHERE model = ? AND nl = ?",
                          (model, nl)):
            return pred_cmd, score

def to_readable(outputs, rev_cm_vocab):
    search_history = [data_utils._ROOT]
    for output in outputs:
        if output < len(rev_cm_vocab):
            search_history.append(rev_cm_vocab[output])
        else:
            search_history.append(data_utils._UNK)
    tree = data_tools.list2ast(search_history)
    cmd = data_tools.ast2command(tree, loose_constraints=True)
    return tree, cmd, outputs


def decode(output_logits, rev_cm_vocab, FLAGS):
    if FLAGS.decoding_algorithm == "greedy":
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
    elif FLAGS.decoding_algorithm == "beam_search":
        outputs = [np.argmax(logit, axis=1) for logit in output_logits]
    else:
        raise ValueError("Unrecognized decoding algorithm name.")

    # If there is an EOS symbol in outputs, cut them at that point.
    if data_utils.EOS_ID in outputs:
        outputs = outputs[:outputs.index(data_utils.EOS_ID)]

    # Print out command corresponding to outputs.
    if FLAGS.decoder_topology == "rnn":
        if FLAGS.char:
            cmd = "".join([tf.compat.as_str(rev_cm_vocab[output]).strip() for output in outputs]) \
                .replace(data_utils._UNK, ' ')
        else:
            tokens = []
            for output in outputs:
                if output < len(rev_cm_vocab):
                    tokens.append(rev_cm_vocab[output])
                else:
                    tokens.append(data_utils._UNK)
            cmd = " ".join(tokens)
        cmd = re.sub('( ;\s+)|( ;$)', ' \\; ', cmd)
        cmd = re.sub('( \)\s+)|( \)$)', ' \\) ', cmd)
        cmd = re.sub('(^\( )|( \( )', '\\(', cmd)
        tree = data_tools.bash_parser(cmd)
        return tree, cmd, outputs
    else:
        return to_readable(outputs, rev_cm_vocab)


def batch_decode(output_logits, rev_cm_vocab, FLAGS):
    batch_size = len(output_logits[0])
    batch_outputs = []
    if FLAGS.decoding_algorithm == "greedy":
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        predictions = [np.argmax(logit, axis=1) for logit in output_logits]
    elif FLAGS.decoding_algorithm == "beam_search":
        predictions = [np.argmax(logit, axis=1) for logit in output_logits]
    else:
        raise ValueError("Unrecognized decoding algorithm name.")

    for i in xrange(batch_size):
        outputs = [int(pred[i]) for pred in predictions]
        # If there is an EOS symbol in outputs, cut them at that point.
        if data_utils.EOS_ID in outputs:
            outputs = outputs[:outputs.index(data_utils.EOS_ID)]
            # Print out command corresponding to outputs.
        if FLAGS.decoder_topology == "seq":
            if FLAGS.char:
                cmd = "".join([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs]) \
                                    .replace(data_utils._UNK, ' ')
            else:
                cmd = " ".join([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs])
            cmd = cmd.replace(' ; ', ' \\; ')
            tree = data_tools.bash_parser(cmd)
            search_history = None
        else:
            tree, cmd, search_history = to_readable(outputs, rev_cm_vocab)
        batch_outputs.append((tree, cmd, search_history))
    return batch_outputs
