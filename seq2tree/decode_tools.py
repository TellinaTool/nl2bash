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
    return tree, cmd, search_history


def decode(output_logits, rev_cm_vocab, FLAGS):
    batch_outputs = []
    if FLAGS.decoding_algorithm == "greedy":
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        scores = reduce(lambda x, y: np.multiply(x, y),
                        [np.max(logit, axis=1) for logit in output_logits])
        predictions = [np.argmax(logit, axis=1) for logit in output_logits]
    else:
        raise ValueError("Unrecognized decoding algorithm: {}."
                         .format(FLAGS.decoding_algorithm))

    batch_size = len(predictions[0])
    for i in xrange(batch_size):
        outputs = [int(pred[i]) for pred in predictions]

        # If there is an EOS symbol in outputs, cut them at that point.
        if data_utils.EOS_ID in outputs:
            outputs = outputs[:outputs.index(data_utils.EOS_ID)]

        if FLAGS.decoder_topology == "rnn":
            if FLAGS.char:
                cmd = "".join([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs])\
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
            search_history = None
        else:
            tree, cmd, search_history = to_readable(outputs, rev_cm_vocab)
        batch_outputs.append((tree, cmd, search_history))
    return batch_outputs, scores


def decode_set(sess, model, dataset, rev_nl_vocab, rev_cm_vocab, FLAGS,
             verbose=True):

    grouped_dataset = data_utils.group_data_by_nl(dataset, use_bucket=True)

    with DBConnection() as db:
        num_eval = 0
        for nl_template in grouped_dataset:
            num_eval += 1

            batch_nl_strs, batch_cm_strs, batch_nls, batch_search_historys = \
                grouped_dataset[nl_template]

            # Which bucket does it belong to?
            bucket_id = min([b for b in xrange(len(model.buckets))
                            if model.buckets[b][0] > batch_nls.shape[1]])

            formatted_example = model.format_example(batch_nls, [data_utils.ROOT_ID],
                                                     bucket_id)

            _, _, output_logits, attn_masks = model.step(sess, formatted_example, bucket_id,
                                             forward_only=True)

            batch_outputs, scores = decode(output_logits, rev_cm_vocab, FLAGS)

            for batch_id in xrange():
                nl_strs = batch_nl_strs[batch_id]
                cm_strs = batch_cm_strs[batch_id]
                nls = batch_nls[batch_id]
                search_historys = batch_search_historys[batch_id]

                nl = nls[batch_id]
                if verbose:
                    print("Example %d (%d)" % (num_eval, len(cm_strs)))
                    print("Original English: " + nl_str.strip())
                    print("English: " + ' '.join([rev_nl_vocab[i] for i in nl]))
                    for j in xrange(len(cm_strs)):
                        print("GT Command {}: {}".format(j+1, cm_strs[j].strip()))
                if FLAGS.decoding_algorithm == "greedy":
                    tree, pred_cmd, search_historys = batch_outputs[batch_id]
                    db.
                    if verbose:
                        print("Prediction: {}".format(pred_cmd))
                        print("AST: ")
                        data_tools.pretty_print(tree, 0)
                        print()
                elif FLAGS.decoding_algorithm == "beam_search":
                    top_k_pred_trees, top_k_pred_cmds, top_k_search_historys = \
                        batch_outputs[batch_id]
                    if verbose:
                        for j in xrange(FLAGS.top_k):
                            print("Prediction {}: {} ".format(j+1, top_k_pred_cmds[j]))
                            print("AST: ")
                            data_tools.pretty_print(top_k_pred_trees[j], 0)
                            print()
                if attn_masks != None:
                    visualize_attn_masks(attn_masks[batch_id, :, :], nls[batch_id], search_historys[batch_id],
                                         rev_nl_vocab, rev_cm_vocab,
                                         os.path.join(FLAGS.train_dir, "{}-{}.jpg".format(num_eval, batch_id)))


def visualize_attn_masks(M, source, target, rev_nl_vocab, rev_cm_vocab, output_path):
    target_length, source_length = M.shape

    plt.clf()
    fig = plt.imshow(M, interpolation='nearest', cmap=plt.cm.Blues)

    nl = [rev_nl_vocab[x] for x in source]
    cm = [rev_cm_vocab[x] for x in target]
    plt.xticks(xrange(source_length),
               [x.replace("$$", "") for x in reversed(nl + [seq2tree.data_utils._PAD] * (source_length - len(nl)))],
               rotation='vertical')
    plt.yticks(xrange(len(cm)),
               [x.replace("$$", "") for x in cm],
               rotation='horizontal')

    plt.colorbar()

    plt.savefig(output_path, bbox_inches='tight')
