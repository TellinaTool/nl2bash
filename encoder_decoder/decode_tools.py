from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os
import re

import tensorflow as tf

from encoder_decoder import data_utils
from bashlex import data_tools
from eval.eval_archive import DBConnection


def translate_fun(sentence, sess, model, sc_vocab, rev_tg_vocab, FLAGS):
    # Get token-ids for the input sentence.
    if FLAGS.char:
        token_ids = data_utils.sentence_to_token_ids(
            sentence, sc_vocab, data_tools.char_tokenizer, data_tools.basic_tokenizer)
    else:
        token_ids = data_utils.sentence_to_token_ids(
            sentence, sc_vocab, data_tools.basic_tokenizer, None)

    # Which bucket does it belong to?
    bucket_id = min([b for b in xrange(len(model.buckets))
                    if model.buckets[b][0] > len(token_ids)])

    # Get a 1-element batch to feed the sentence to the model.
    formatted_example = model.format_example([token_ids], [[data_utils.ROOT_ID]],
                                             bucket_id=bucket_id)

    # Get output for the sentence.
    output_symbols, output_logits, losses, attn_masks = \
                model.step(sess, formatted_example, bucket_id, forward_only=True)
    batch_outputs = decode(output_symbols, rev_tg_vocab, FLAGS)

    return batch_outputs[:100], output_logits[:100]


def demo(sess, model, sc_vocab, rev_tg_vocab, FLAGS):
    """
    Simple command line decoding interface.
    """

    # Decode from standard input.
    sys.stdout.write("> ")
    sys.stdout.flush()
    sentence = sys.stdin.readline()

    while sentence:
        batch_outputs, output_logits = translate_fun(
            sentence, sess, model, sc_vocab, rev_tg_vocab, FLAGS)

        if FLAGS.decoding_algorithm == "greedy":
            tree, pred_cmd, outputs = batch_outputs[0]
            score = output_logits[0]
            print("{} ({})".format(pred_cmd, score))
        elif FLAGS.decoding_algorithm == "beam_search":
            top_k_predictions = batch_outputs[0]
            top_k_scores = output_logits[0]
            for j in xrange(min(FLAGS.beam_size, 10)):
                top_k_pred_tree, top_k_pred_cmd, top_k_outputs = \
                    top_k_predictions[j]
                print("Prediction {}: {} ({}) ".format(
                    j+1, top_k_pred_cmd, top_k_scores[j]))
            print()
        print("> ", end="")
        sys.stdout.flush()
        sentence = sys.stdin.readline()


def to_readable(outputs, rev_tg_vocab):
    search_history = [data_utils._ROOT]
    for output in outputs:
        if output < len(rev_tg_vocab):
            search_history.append(rev_tg_vocab[output])
        else:
            search_history.append(data_utils._UNK)
    tree = data_tools.list2ast(search_history)
    cmd = data_tools.ast2command(tree, loose_constraints=True)
    return tree, cmd, search_history


def decode(output_symbols, rev_tg_vocab, FLAGS):
    batch_outputs = []

    for i in xrange(len(output_symbols)):
        top_k_predictions = output_symbols[i]
        assert((FLAGS.decoding_algorithm == "greedy") or 
               len(top_k_predictions) == FLAGS.beam_size)
        if FLAGS.decoding_algorithm == "beam_search":
            beam_outputs = []
        for j in xrange(len(top_k_predictions)):
            prediction = top_k_predictions[j]
            outputs = [int(pred) for pred in prediction]

            # If there is an EOS symbol in outputs, cut them at that point.
            if data_utils.EOS_ID in outputs:
                outputs = outputs[:outputs.index(data_utils.EOS_ID)]

            if FLAGS.decoder_topology == "rnn":
                if FLAGS.char:
                    cmd = "".join([tf.compat.as_str(rev_tg_vocab[output])
                               for output in outputs]).replace(data_utils._UNK, ' ')
                else:
                    tokens = []
                    for output in outputs:
                        if output < len(rev_tg_vocab):
                            pred_token = rev_tg_vocab[output]
                            if "@@" in pred_token:
                                pred_token = pred_token.split("@@")[-1]
                            tokens.append(pred_token)
                        else:
                            tokens.append(data_utils._UNK)
                    cmd = " ".join(tokens)

                if FLAGS.explanation:
                    tree = []
                else:
                    if FLAGS.dataset in ["bash", "bash.cl"]:
                        cmd = re.sub('( ;\s+)|( ;$)', ' \\; ', cmd)
                        # cmd = re.sub('( \)\s+)|( \)$)', ' \\) ', cmd)
                        cmd = re.sub('(^\( )|( \( )', ' \\( ', cmd)
                        tree = data_tools.bash_parser(cmd)
                    else:
                        tree = data_tools.paren_parser(cmd)
            else:
                tree, cmd, outputs = to_readable(outputs, rev_tg_vocab)

            if not tree is None:
                # filter out non-grammatical output
                temp = data_tools.ast2template(tree, loose_constraints=True, 
                                               ignore_flag_order=False)
                if FLAGS.decoding_algorithm == "greedy":
                    batch_outputs.append((tree, temp, outputs))
                else:
                    beam_outputs.append((tree, temp, outputs))
        if FLAGS.decoding_algorithm == "beam_search":
            batch_outputs.append(beam_outputs)

    return batch_outputs


def decode_set(sess, model, dataset, rev_sc_vocab, rev_tg_vocab, FLAGS, verbose=True):
    if FLAGS.explanation:
        group_data_by_sc = data_utils.group_data_by_cm
    else:
        group_data_by_sc = data_utils.group_data_by_nl
    grouped_dataset = group_data_by_sc(dataset, use_bucket=True,
                                       use_temp = FLAGS.dataset.startswith("bash"))
    bucketed_sc_strs, bucketed_tg_strs, bucketed_scs, bucketed_tgs = \
        data_utils.bucket_grouped_data(grouped_dataset, model.buckets)

    with DBConnection() as db:
        db.remove_model(model.model_sig)

        for bucket_id in xrange(len(model.buckets)):
            bucket_sc_strs = bucketed_sc_strs[bucket_id]
            bucket_tg_strs = bucketed_tg_strs[bucket_id]
            bucket_scs = bucketed_scs[bucket_id]
            bucket_tgs = bucketed_tgs[bucket_id]
            bucket_size = len(bucket_sc_strs)

            num_batches = int(bucket_size / FLAGS.batch_size)
            if bucket_size % FLAGS.batch_size != 0:
                num_batches += 1

            for b in xrange(num_batches):
                batch_sc_strs = bucket_sc_strs[b*FLAGS.batch_size:(b+1)*FLAGS.batch_size]
                batch_tg_strs = bucket_tg_strs[b*FLAGS.batch_size:(b+1)*FLAGS.batch_size]
                batch_scs = bucket_scs[b*FLAGS.batch_size:(b+1)*FLAGS.batch_size]
                batch_tgs = bucket_tgs[b*FLAGS.batch_size:(b+1)*FLAGS.batch_size]

                # make a full batch
                if len(batch_sc_strs) < FLAGS.batch_size:
                    batch_size = len(batch_sc_strs)
                    pad_size = FLAGS.batch_size - len(batch_sc_strs)
                    batch_sc_strs = batch_sc_strs + [batch_sc_strs[-1]] * pad_size
                    assert(len(batch_tg_strs) == batch_size)
                    batch_tg_strs = batch_tg_strs + [batch_tg_strs[-1]] * pad_size
                    assert(len(batch_scs) == batch_size)
                    batch_scs = batch_scs + [batch_scs[-1]] * pad_size
                    assert(len(batch_tgs) == batch_size)
                    batch_tgs = batch_tgs + [batch_tgs[-1]] * pad_size
                else:
                    batch_size = FLAGS.batch_size
                formatted_example = model.format_example(batch_scs, batch_tgs, bucket_id=bucket_id)
                output_symbols, output_logits, losses, attn_masks = \
                        model.step(sess, formatted_example, bucket_id, forward_only=True)
                batch_outputs = decode(output_symbols, rev_tg_vocab, FLAGS)

                for batch_id in xrange(batch_size):
                    example_id = b * FLAGS.batch_size + batch_id
                    sc_str = batch_sc_strs[batch_id]
                    tg_strs = batch_tg_strs[batch_id]
                    nl = batch_scs[batch_id]
                    sc_temp = ' '.join([rev_sc_vocab[i] for i in nl])

                    if verbose:
                        print("Example {}:{}".format(bucket_id, example_id))
                        print("(Orig) Source: " + sc_str.strip())
                        print("Source: " + sc_temp)
                        for j in xrange(len(tg_strs)):
                            print("GT Target {}: {}".format(j+1, tg_strs[j].strip()))
                    if FLAGS.decoding_algorithm == "greedy":
                        tree, pred_cmd, outputs = batch_outputs[batch_id]
                        score = output_logits[batch_id]
                        db.add_prediction(model.model_sig, sc_str, pred_cmd, float(score))
                        if verbose:
                            print("Prediction: {} ({})".format(pred_cmd, score))
                    elif FLAGS.decoding_algorithm == "beam_search":
                        top_k_predictions = batch_outputs[batch_id]
                        top_k_scores = output_logits[batch_id]
                        for j in xrange(min(FLAGS.beam_size, len(top_k_predictions), 10)):
                            top_k_pred_tree, top_k_pred_cmd, top_k_outputs = top_k_predictions[j]
                            if verbose:
                                print("Prediction {}: {} ({}) ".format(
                                    j+1, top_k_pred_cmd, top_k_scores[j]))
                            db.add_prediction(model.model_sig, sc_str, top_k_pred_cmd,
                                              float(top_k_scores[j]), update_mode=False)
                        if verbose:
                            print()
                        outputs = top_k_predictions[0][2]
                    else:
                        raise ValueError("Unrecognized decoding algorithm: {}."
                             .format(FLAGS.decoding_algorithm))

                    if attn_masks is not None:
                        if FLAGS.decoding_algorithm == "greedy":
                            M = attn_masks[batch_id, :, :]
                        elif FLAGS.decoding_algorithm == "beam_search":
                            M = attn_masks[batch_id, 0, :, :]
                        visualize_attn_masks(M, nl, outputs, rev_sc_vocab, rev_tg_vocab,
                            os.path.join(FLAGS.model_dir, "{}-{}.jpg".format(bucket_id, example_id)))


def visualize_attn_masks(M, source, target, rev_sc_vocab, rev_tg_vocab, output_path):
    target_length, source_length = M.shape

    nl = [rev_sc_vocab[x] for x in source]
    cm = []
    for i, x in enumerate(target):
        cm.append(rev_tg_vocab[x])
        if rev_tg_vocab[x] == data_utils._EOS:
            break

    plt.clf()
    if len(target) == 0:
        i = 0
    fig = plt.imshow(M[:i+1, :], interpolation='nearest', cmap=plt.cm.Blues)

    pad_size = source_length - len(nl)
    plt.xticks(xrange(source_length),
               [x.replace("$$", "") for x in reversed(nl + [data_utils._PAD] * pad_size)],
               rotation='vertical')
    plt.yticks(xrange(len(cm)),
               [x.replace("$$", "") for x in cm],
               rotation='horizontal')

    plt.colorbar()

    plt.savefig(output_path, bbox_inches='tight')
