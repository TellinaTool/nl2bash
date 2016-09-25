from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import re
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bashlex"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "eval"))

import tensorflow as tf

import data_utils, data_tools
from eval_archive import DBConnection

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
    bucketed_group = data_utils.bucket_grouped_data(grouped_dataset, model.buckets)

    with DBConnection() as db:
        for bucket_id in xrange(len(model.buckets)):
            print(len(bucketed_group[bucket_id]))
            batch_nl_strs, batch_cm_strs, batch_nls, batch_cmds = \
                bucketed_group[bucket_id]

            batch_size = len(batch_nl_strs)

            formatted_example = model.format_example(
                batch_nls, batch_cmds, bucket_id=bucket_id)

            _, _, output_logits, attn_masks = model.step(
                sess, formatted_example, bucket_id, forward_only=True)

            batch_outputs, scores = decode(output_logits, rev_cm_vocab, FLAGS)

            for batch_id in xrange(batch_size):
                nl_str = batch_nl_strs[batch_id]
                cm_strs = batch_cm_strs[batch_id]
                nl = batch_nls[batch_id]

                if verbose:
                    print("Example {}:{}".format(bucket_id, batch_id))
                    print("Original English: " + nl_str.strip())
                    print("English: " + ' '.join([rev_nl_vocab[i] for i in nl]))
                    for j in xrange(len(cm_strs)):
                        print("GT Command {}: {}".format(j+1, cm_strs[j].strip()))
                if FLAGS.decoding_algorithm == "greedy":
                    tree, pred_cmd, outputs = batch_outputs[batch_id]
                    score = scores[batch_id]
                    db.add_prediction(model.model_dir, nl, pred_cmd, score)
                    if verbose:
                        print("Prediction: {} ({})".format(pred_cmd, score))
                        print("AST: ")
                        data_tools.pretty_print(tree, 0)
                        print()
                elif FLAGS.decoding_algorithm == "beam_search":
                    top_k_pred_trees, top_k_pred_cmds, top_k_outputs = \
                        batch_outputs[batch_id]
                    top_k_scores = scores[batch_id]
                    if verbose:
                        for j in xrange(FLAGS.top_k):
                            print("Prediction {}: {} ({}) ".format(j+1,
                                top_k_pred_cmds[j], top_k_scores[j]))
                            print("AST: ")
                            data_tools.pretty_print(top_k_pred_trees[j], 0)
                    print()
                    outputs = top_k_outputs[0]
                else:
                    raise ValueError("Unrecognized decoding algorithm: {}."
                         .format(FLAGS.decoding_algorithm))
                if attn_masks != None:
                    visualize_attn_masks(attn_masks[batch_id, :, :], nl, outputs[batch_id],
                                         rev_nl_vocab, rev_cm_vocab,
                                         os.path.join(FLAGS.train_dir, "{}-{}.jpg".format(bucket_id, batch_id)))


def interactive_decode(sess, model, nl_vocab, rev_cm_vocab, FLAGS):
    """
    Simple command line decoding interface.
    """

    # Decode from standard input.
    sys.stdout.write("> ")
    sys.stdout.flush()
    sentence = sys.stdin.readline()

    while sentence:
        # Get token-ids for the input sentence.
        if FLAGS.char:
            token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), nl_vocab,
                                                         data_tools.char_tokenizer, data_tools.basic_tokenizer)
        else:
            token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), nl_vocab,
                                                         data_tools.basic_tokenizer, None)

        # Which bucket does it belong to?
        bucket_id = min([b for b in xrange(len(model.buckets))
                        if model.buckets[b][0] > len(token_ids)])

        # Get a 1-element batch to feed the sentence to the model.
        formatted_example = model.format_example([token_ids], [[data_utils.ROOT_ID]], bucket_id)

        # Get output logits for the sentence.
        _, _, output_logits, _ = model.step(sess, formatted_example, bucket_id,
                                            forward_only=True)
        batch_outputs, scores = decode(output_logits, rev_cm_vocab, FLAGS)

        if FLAGS.decoding_algorithm == "greedy":
            tree, pred_cmd, outputs = batch_outputs[0]
            print()
            print(pred_cmd)
            print()
            data_tools.pretty_print(tree, 0)
            print()
        elif FLAGS.decoding_algorithm == "beam_search":
            top_k_search_histories, decode_scores = model.beam_decode(FLAGS.beam_size, FLAGS.top_k)
            print()
            for i in xrange(FLAGS.top_k):
                outputs = top_k_search_histories[i]
                tree, cmd, _ = to_readable(outputs, rev_cm_vocab)
                print("prediction %d (%.2f): " % (i, decode_scores[i]) + cmd)
                print()
                data_tools.pretty_print(tree, 0)
                print()

        print("> ", end="")
        sys.stdout.flush()
        sentence = sys.stdin.readline()


def visualize_attn_masks(M, source, target, rev_nl_vocab, rev_cm_vocab, output_path):
    target_length, source_length = M.shape

    plt.clf()
    fig = plt.imshow(M, interpolation='nearest', cmap=plt.cm.Blues)

    nl = [rev_nl_vocab[x] for x in source]
    cm = [rev_cm_vocab[x] for x in target]
    plt.xticks(xrange(source_length),
               [x.replace("$$", "") for x in reversed(nl + [data_utils._PAD] * (source_length - len(nl)))],
               rotation='vertical')
    plt.yticks(xrange(len(cm)),
               [x.replace("$$", "") for x in cm],
               rotation='horizontal')

    plt.colorbar()

    plt.savefig(output_path, bbox_inches='tight')
