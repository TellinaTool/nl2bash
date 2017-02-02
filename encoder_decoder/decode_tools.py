from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import re

import tensorflow as tf

from encoder_decoder import data_utils, classifiers
from bashlex import data_tools
from nlp_tools import constants, slot_filling, tokenizer
from eval.eval_archive import DBConnection


def translate_fun(sentence, sess, model, sc_vocab, rev_tg_vocab, FLAGS,
                  slot_filling_classifier=None):
    # Get token-ids for the input sentence.
    # entities: ner_by_token_id, ner_by_char_pos, ner_by_category
    if FLAGS.char:
        token_ids, entities = data_utils.sentence_to_token_ids(sentence,
            sc_vocab, data_tools.char_tokenizer, tokenizer.basic_tokenizer)
    else:
        token_ids, entities = data_utils.sentence_to_token_ids(
            sentence, sc_vocab, tokenizer.ner_tokenizer, None)
    # Which bucket does it belong to?
    bucket_id = min([b for b in xrange(len(model.buckets))
                    if model.buckets[b][0] > len(token_ids)])

    # Get a 1-element batch to feed the sentence to the model.
    formatted_example = model.format_example(
        [token_ids], [[data_utils.ROOT_ID]], bucket_id=bucket_id)

    # Decode the ouptut for this 1-element batch.
    # Non-grammatical templates and templates that cannot hold all fillers are
    # filtered out.
    # TODO: align output commands and their scores correctly
    model_step_outputs = model.step(sess, formatted_example, bucket_id,
        forward_only=True, return_rnn_hidden_states=FLAGS.fill_argument_slots)
    output_symbols, output_logits, losses, attn_masks = model_step_outputs[:4]

    nl_fillers, encoder_outputs, decoder_outputs = None, None, None
    if FLAGS.fill_argument_slots:
        assert(slot_filling_classifier is not None)
        nl_fillers = entities[0]
        encoder_outputs = model_step_outputs[4]
        decoder_outputs = model_step_outputs[5]
    batch_outputs = decode(output_symbols, rev_tg_vocab, FLAGS,
                           grammatical_only=True,
                           nl_fillers=nl_fillers,
                           slot_filling_classifier=slot_filling_classifier,
                           encoder_outputs=encoder_outputs,
                           decoder_outputs=decoder_outputs)

    return batch_outputs, output_logits


def demo(sess, model, sc_vocab, rev_tg_vocab, FLAGS):
    """
    Simple command line decoding interface.
    """

    slot_filling_classifier = None
    if FLAGS.fill_argument_slots:
        # create slot filling classifier
        model_param_dir = os.path.join(FLAGS.data_dir, 'train.{}.mappings.X.Y'
                               .format(FLAGS.sc_vocab_size))
        train_X, train_Y = data_utils.load_slot_filling_data(model_param_dir)
        slot_filling_classifier = \
                classifiers.KNearestNeighborModel(1, train_X, train_Y)
        print('Slot filling classifier parameters loaded.')

    # Decode from standard input.
    sys.stdout.write("> ")
    sys.stdout.flush()
    sentence = sys.stdin.readline()

    while sentence:
        batch_outputs, output_logits = translate_fun(
            sentence, sess, model, sc_vocab, rev_tg_vocab, FLAGS,
            slot_filling_classifier=slot_filling_classifier)

        if FLAGS.decoding_algorithm == "greedy":
            tree, pred_cmd, outputs = batch_outputs[0]
            score = output_logits[0]
            print("{} ({})".format(pred_cmd, score))
        elif FLAGS.decoding_algorithm == "beam_search":
            top_k_predictions = batch_outputs[0]
            top_k_scores = output_logits[0]
            for j in xrange(min(FLAGS.beam_size, 10)):
                if len(top_k_predictions) <= j:
                    break
                top_k_pred_tree, top_k_pred_cmd, top_k_outputs = \
                    top_k_predictions[j]
                print("Prediction {}: {} ({}) ".format(
                    j+1, top_k_pred_cmd, top_k_scores[j]))
            print()
        print("> ", end="")
        sys.stdout.flush()
        sentence = sys.stdin.readline()


def decode(output_symbols, rev_tg_vocab, FLAGS, grammatical_only=True,
           nl_fillers=None, slot_filling_classifier=None, encoder_outputs=None,
           decoder_outputs=None):
    """
    Transform the neural network output into readable strings and apply the
    relevant filters.
    """
    if nl_fillers is None:
        assert(slot_filling_classifier is None)
        assert(encoder_outputs is None)
        assert(decoder_outputs is None)

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

    batch_outputs = []

    for i in xrange(len(output_symbols)):
        top_k_predictions = output_symbols[i]
        assert((FLAGS.decoding_algorithm == "greedy") or 
               len(top_k_predictions) == FLAGS.beam_size)
        if FLAGS.decoding_algorithm == "beam_search":
            beam_outputs = []
        for j in xrange(len(top_k_predictions)):

            # Step 1: transform the neural network output into readable strings
            prediction = top_k_predictions[j]
            outputs = [int(pred) for pred in prediction]

            # If there is an EOS symbol in outputs, cut them at that point.
            if data_utils.EOS_ID in outputs:
                outputs = outputs[:outputs.index(data_utils.EOS_ID)]

            if nl_fillers is not None:
                cm_slots = {}

            tree, output_tokens = None, []
            if FLAGS.decoder_topology == "rnn":
                if FLAGS.char:
                    tg = "".join([tf.compat.as_str(rev_tg_vocab[output])
                        for output in outputs]).replace(data_utils._UNK, ' ')
                else:
                    for ii in xrange(len(outputs)):
                        output = outputs[ii]
                        if output < len(rev_tg_vocab):
                            pred_token = rev_tg_vocab[output]
                            if "@@" in pred_token:
                                pred_token = pred_token.split("@@")[-1]
                            output_tokens.append(pred_token)
                            if nl_fillers is not None and \
                                    pred_token in constants._ENTITIES:
                                if ii > 0 and slot_filling.is_min_flag(
                                        rev_tg_vocab[outputs[ii-1]]):
                                    pred_token_type = 'Timespan'
                                else:
                                    pred_token_type = pred_token
                                cm_slots[ii] = (pred_token, pred_token_type)
                        else:
                            output_tokens.append(data_utils._UNK)
                    tg = " ".join(output_tokens)
            else:
                tree, tg, outputs = to_readable(outputs, rev_tg_vocab)

            # check if the predicted command templates have enough slots to
            # hold the fillers (to rule out templates that are trivially
            # unqualified)
            if nl_fillers is None or len(cm_slots) >= len(nl_fillers):

                # Step 2: check if the predicted command template is grammatical
                if FLAGS.dataset.startswith("bash"):
                    tg = re.sub('( ;\s+)|( ;$)', ' \\; ', tg)
                    tg = re.sub('( +\s+)|( +$)', ' \\+ ', tg)
                    tree = data_tools.bash_parser(tg)
                else:
                    tree = data_tools.paren_parser(tg)

                # filter out non-grammatical output
                if tree is not None or not grammatical_only:
                    output_example = False
                    if FLAGS.explanation:
                        temp = tg
                        output_example = True
                    else:
                        temp = data_tools.ast2template(tree,
                            loose_constraints=True, ignore_flag_order=False)
                        if nl_fillers is None:
                            output_example = True
                        else:
                            # Step 3: match the fillers to the argument slots
                            tree2, temp = slot_filling.stable_slot_filling(
                                output_tokens, nl_fillers, cm_slots,
                                encoder_outputs[i],
                                decoder_outputs[i*FLAGS.beam_size+j],
                                slot_filling_classifier
                            )
                            if temp is not None:
                                output_example = True
                                tree = tree2
                    if output_example:
                        if FLAGS.decoding_algorithm == "greedy":
                            batch_outputs.append((tree, temp, outputs))
                        else:
                            beam_outputs.append((tree, temp, outputs))

        if FLAGS.decoding_algorithm == "beam_search":
            if beam_outputs:
                batch_outputs.append(beam_outputs)

    return batch_outputs


def decode_set(sess, model, dataset, rev_sc_vocab, rev_tg_vocab,
               FLAGS, verbose=True):
    grouped_dataset = data_utils.group_data_by_nl(dataset, use_bucket=True,
        use_temp=FLAGS.dataset.startswith("bash") and not FLAGS.explanation)
    bucketed_sc_strs, bucketed_tg_strs, bucketed_scs, bucketed_tgs = \
        data_utils.bucket_grouped_data(grouped_dataset, model.buckets)

    with DBConnection() as db:
        db.create_schema()
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
                    sc = batch_scs[batch_id]
                    sc_temp = ' '.join([rev_sc_vocab[i] for i in sc])
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
                        visualize_attn_masks(M, sc, outputs, rev_sc_vocab, rev_tg_vocab,
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
