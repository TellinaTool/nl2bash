from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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


def decode(output_symbols, rev_cm_vocab, FLAGS):
    batch_outputs = []
    batch_size = len(output_symbols)
    
    predictions = reduce(lambda x,y: x + y, output_symbols)

    for i in xrange(len(predictions)):
        outputs = [int(pred) for pred in predictions[i]]

        # If there is an EOS symbol in outputs, cut them at that point.
        if data_utils.EOS_ID in outputs:
            outputs = outputs[:outputs.index(data_utils.EOS_ID)]

        if FLAGS.decoder_topology == "rnn":
            if FLAGS.char:
                cmd = "".join([tf.compat.as_str(rev_cm_vocab[output])
                               for output in outputs]).replace(data_utils._UNK, ' ')
            else:
                tokens = []
                for output in outputs:
                    if output < len(rev_cm_vocab):
                        pred_token = rev_cm_vocab[output]
                        if "@@" in pred_token:
                            pred_token = pred_token.split("@@")[-1]
                        tokens.append(pred_token)
                    else:
                        tokens.append(data_utils._UNK)
                cmd = " ".join(tokens)

            if FLAGS.dataset == "bash":
                cmd = re.sub('( ;\s+)|( ;$)', ' \\; ', cmd)
                cmd = re.sub('( \)\s+)|( \)$)', ' \\) ', cmd)
                cmd = re.sub('(^\( )|( \( )', ' \\( ', cmd)
                tree = data_tools.bash_parser(cmd)
            else:
                tree = data_utils.parse_brackets(cmd)
            search_history = outputs
        else:
            tree, cmd, search_history = to_readable(outputs, rev_cm_vocab)
        batch_outputs.append((tree, cmd, search_history))
    
    if FLAGS.decoding_algorithm == "beam_search":
        batch_beam_outputs = []
        for i in xrange(batch_size):
            beam_outputs = []
            for j in xrange(FLAGS.beam_size):
                beam_outputs.append(batch_outputs[i * FLAGS.beam_size + j])
            batch_beam_outputs.append(beam_outputs)
        return batch_beam_outputs
    else:
        return batch_outputs


def decode_set(sess, model, dataset, rev_nl_vocab, rev_cm_vocab, FLAGS,
             verbose=True):

    grouped_dataset = data_utils.group_data_by_nl(dataset, use_bucket=True)
    bucketed_nl_strs, bucketed_cm_strs, bucketed_nls, bucketed_cmds = \
        data_utils.bucket_grouped_data(grouped_dataset, model.buckets)

    with DBConnection() as db:
        db.remove_model(model.model_sig)

        for bucket_id in xrange(len(model.buckets)):
            batch_nl_strs = bucketed_nl_strs[bucket_id]
            batch_cm_strs = bucketed_cm_strs[bucket_id]
            batch_nls = bucketed_nls[bucket_id]
            batch_cmds = bucketed_cmds[bucket_id]

            batch_size = len(batch_nl_strs)

            for batch_id in xrange(batch_size):
                formatted_example = model.format_example(
                    batch_nls[batch_id:batch_id+1],
                    batch_cmds[batch_id:batch_id+1],
                    bucket_id=bucket_id)
                output_symbols, output_logits, losses, attn_masks = \
                    model.step(sess, formatted_example, bucket_id, forward_only=True)
                    
                batch_outputs = decode(output_symbols, rev_cm_vocab, FLAGS)

                nl_str = batch_nl_strs[batch_id]
                cm_strs = batch_cm_strs[batch_id]
                nl = batch_nls[batch_id]
                nl_temp = ' '.join([rev_nl_vocab[i] for i in nl])

                if verbose:
                    print("Example {}:{}".format(bucket_id, batch_id))
                    print("Original English: " + nl_str.strip())
                    print("English: " + nl_temp)
                    for j in xrange(len(cm_strs)):
                        print("GT Command {}: {}".format(j+1, cm_strs[j].strip()))
                if FLAGS.decoding_algorithm == "greedy":
                    tree, pred_cmd, outputs = batch_outputs[0]
                    score = output_logits
                    db.add_prediction(model.model_sig, nl_str, pred_cmd, float(score))
                    if verbose:
                        print("Prediction: {} ({})".format(pred_cmd, score))
                        # print("AST: ")
                        # data_tools.pretty_print(tree, 0)
                        # print()
                elif FLAGS.decoding_algorithm == "beam_search":
                    top_k_predictions = batch_outputs[0]
                    top_k_scores = output_logits[0]
                    for j in xrange(FLAGS.beam_size):
                        top_k_pred_tree, top_k_pred_cmd, top_k_outputs = \
                            top_k_predictions[j]
                        if verbose:
                            print("Prediction {}: {} ({}) ".format(j+1,
                                top_k_pred_cmd, top_k_scores[j]))
                        db.add_prediction(model.model_sig, nl_str, top_k_pred_cmd,
                                          float(top_k_scores[j]), update_mode=False)
                        # print("AST: ")
                        # data_tools.pretty_print(top_k_pred_tree, 0)
                    if verbose:
                        print()
                    outputs = top_k_predictions[0][2]
                else:
                    raise ValueError("Unrecognized decoding algorithm: {}."
                         .format(FLAGS.decoding_algorithm))

                if attn_masks is not None:
                    if FLAGS.decoding_algorithm == "greedy":
                        M = attn_masks[0, :, :]
                    elif FLAGS.decoding_algorithm == "beam_search":
                        M = attn_masks[0, 0, :, :]
                    print(M)
                    visualize_attn_masks(M, nl, outputs, rev_nl_vocab, rev_cm_vocab,
                                         os.path.join(FLAGS.model_dir,
                                                      "{}-{}.jpg".format(bucket_id, batch_id)))


def demo(sess, model, nl_vocab, rev_cm_vocab, FLAGS):
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
        formatted_example = model.format_example([token_ids], [[data_utils.ROOT_ID]],
                                                 bucket_id=bucket_id)

        # Get output for the sentence.
        output_symbols, output_logits, losses, attn_masks = \
                    model.step(sess, formatted_example, bucket_id, forward_only=True)
        batch_outputs = decode(output_symbols, rev_cm_vocab, FLAGS)

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

    nl = [rev_nl_vocab[x] for x in source]
    cm = []
    for i, x in enumerate(target):
        cm.append(rev_cm_vocab[x])
        if rev_cm_vocab[x] == data_utils._EOS:
            break


    plt.clf()
    if len(target) == 0:
        i = 0
    fig = plt.imshow(M[:i+1, :], interpolation='nearest', cmap=plt.cm.Blues)

    plt.xticks(xrange(source_length),
               [x.replace("$$", "") for x in reversed(nl + [data_utils._PAD] * (source_length - len(nl)))],
               rotation='vertical')
    plt.yticks(xrange(len(cm)),
               [x.replace("$$", "") for x in cm],
               rotation='horizontal')

    plt.colorbar()

    plt.savefig(output_path, bbox_inches='tight')
