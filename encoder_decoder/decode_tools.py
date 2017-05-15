from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
if sys.version_info > (3, 0):
    from six.moves import xrange
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

from encoder_decoder import classifiers, data_utils
from bashlex import data_tools
from nlp_tools import constants, slot_filling, tokenizer
from eval.eval_archive import DBConnection


APOLOGY_MSG = \
        "I'm very sorry, I can't translate this command at the moment."


def demo(sess, model, FLAGS):
    """
    Simple command line decoding interface.
    """
    slot_filling_classifier = None
    if FLAGS.fill_argument_slots:
        # create slot filling classifier
        mapping_param_dir = os.path.join(
            FLAGS.model_dir, 'train.mappings.X.Y.npz')
        train_X, train_Y = \
            data_utils.load_slot_filling_data(mapping_param_dir)
        slot_filling_classifier = classifiers.KNearestNeighborModel(
            FLAGS.num_nn_slot_filling, train_X, train_Y)
        print('Slot filling classifier parameters loaded.')

    # Decode from standard input.
    sys.stdout.write("> ")
    sys.stdout.flush()
    sentence = sys.stdin.readline()

    vocabs = data_utils.load_vocab(FLAGS)

    while sentence:
        batch_outputs, output_logits = translate_fun(sentence, sess, model,
            vocabs, FLAGS, slot_filling_classifier=slot_filling_classifier)

        if FLAGS.token_decoding_algorithm == "greedy":
            tree, pred_cmd, outputs = batch_outputs[0]
            score = output_logits[0]
            print("{} ({})".format(pred_cmd, score))
        elif FLAGS.token_decoding_algorithm == "beam_search":
            if batch_outputs:
                top_k_predictions = batch_outputs[0]
                top_k_scores = output_logits[0]
                for j in xrange(min(FLAGS.beam_size, 10, len(batch_outputs[0]))):
                    if len(top_k_predictions) <= j:
                        break
                    top_k_pred_tree, top_k_pred_cmd, top_k_outputs = \
                        top_k_predictions[j]
                    print("Prediction {}: {} ({}) ".format(
                        j+1, top_k_pred_cmd, top_k_scores[j]))
                print()
            else:
                print("I'm very sorry, I can't translate this command at the moment.")
        print("> ", end="")
        sys.stdout.flush()
        sentence = sys.stdin.readline()


def translate_fun(input, sess, model, vocabs, FLAGS,
                  slot_filling_classifier=None):
    # Get token-ids for the input sentence.
    # entities: ner_by_token_id, ner_by_char_pos, ner_by_category
    if type(input) is list:
        sentence = input[0].sc_txt
        tg_ids = input[0].tg_ids
        tg_full_ids = input[0].tg_full_ids
        pointer_targets = input[0].pointer_targets
    else:
        sentence = input
        tg_ids = [data_utils.ROOT_ID]
        tg_full_ids = [data_utils.ROOT_ID]
        pointer_targets = np.zeros([1, FLAGS.max_tg_length, FLAGS.max_sc_length])

    sc_vocab = vocabs.sc_vocab
    tg_vocab = vocabs.tg_vocab

    if FLAGS.char:
        sc_ids, entities = data_utils.sentence_to_token_ids(sentence,
            sc_vocab, data_tools.char_tokenizer, tokenizer.basic_tokenizer)
        sc_full_ids, _ = data_utils.sentence_to_token_ids(sentence,
            sc_vocab, data_tools.char_tokenizer, tokenizer.basic_tokenizer,
            use_unk=False)
        sc_copy_full_ids = []
    else:
        if FLAGS.explain:
            sentence = data_tools.bash_tokenizer(
                sentence, arg_type_only=FLAGS.normalized)
            sc_tokenizer = None
            sc_full_tokenizer = None
        else:
            if FLAGS.dataset.startswith("bash"):
                sc_tokenizer = tokenizer.basic_tokenizer \
                    if not FLAGS.normalized else tokenizer.ner_tokenizer
                sc_full_tokenizer = tokenizer.basic_tokenizer
            else:
                sc_tokenizer = tokenizer.space_tokenizer
                sc_full_tokenizer = tokenizer.space_tokenizer
        sc_ids, entities = data_utils.sentence_to_token_ids(
            sentence, sc_vocab, sc_tokenizer, None)
        sc_full_ids, _ = data_utils.sentence_to_token_ids(
            sentence, sc_vocab,sc_full_tokenizer, None, use_unk=False)
        sc_copy_full_ids, _ = data_utils.sentence_to_token_ids(sentence,
            tg_vocab, sc_full_tokenizer, None, use_unk=False,
            use_dummy_indices=True, parallel_vocab_size=FLAGS.tg_vocab_size)

    # Note that we only perform source word filtering when translating from
    # natural language to bash
    if not (FLAGS.dataset.startswith('bash') and not FLAGS.explain):
        sc_ids = sc_full_ids
    
    # Which bucket does it belong to?
    bucket_id = min([b for b in xrange(len(model.buckets))
                    if model.buckets[b][0] > len(sc_ids)])

    # Get a 1-element batch to feed the sentence to the model.
    formatted_example = model.format_example(
        [[sc_ids], [sc_full_ids], [sc_copy_full_ids]], [[tg_ids], [tg_full_ids]],
        pointer_targets=[pointer_targets], bucket_id=bucket_id)
    print(sc_copy_full_ids)

    # Decode the output for this 1-element batch.
    # Non-grammatical templates and templates that cannot hold all fillers are
    # filtered out.
    # TODO: align output commands and their scores correctly
    model_outputs = model.step(sess, formatted_example, bucket_id,
        forward_only=True, return_rnn_hidden_states=FLAGS.fill_argument_slots)
    output_logits = model_outputs.output_logits

    nl_fillers = None
    if FLAGS.fill_argument_slots:
        assert(slot_filling_classifier is not None)
        nl_fillers = entities[0]
    decoded_outputs = decode(formatted_example.encoder_full_inputs, model_outputs, 
                             FLAGS, vocabs, nl_fillers, slot_filling_classifier)

    return decoded_outputs, output_logits


def decode(encoder_inputs, model_outputs, FLAGS, vocabs, nl_fillers=None,
           slot_filling_classifier=None):
    """
    Transform the neural network output into readable strings and apply the
    relevant filters.
    """

    rev_sc_vocab = vocabs.rev_sc_vocab
    rev_tg_vocab = vocabs.rev_tg_vocab
    rev_tg_char_vocab = vocabs.rev_tg_char_vocab

    encoder_outputs = model_outputs.encoder_hidden_states
    decoder_outputs = model_outputs.decoder_hidden_states
    if nl_fillers is not None:
        assert(slot_filling_classifier is not None)
        assert(encoder_outputs is not None)
        assert(decoder_outputs is not None)

    # def to_readable(outputs, rev_tg_vocab):
    #     search_history = [data_utils._ROOT]
    #     for output in outputs:
    #         if output < len(rev_tg_vocab):
    #             search_history.append(rev_tg_vocab[output])
    #         else:
    #             search_history.append(data_utils._UNK)
    #     tree = data_tools.list2ast(search_history)
    #     cmd = data_tools.ast2command(tree, loose_constraints=True)
    #     return tree, cmd, search_history

    def as_str(output):
        if output < FLAGS.target_vocab_size:
            token = rev_tg_vocab[output]
        else:
            token = rev_sc_vocab[
                encoder_inputs[batch_id][output - FLAGS.target_vocab_size]]
        return token

    output_symbols = model_outputs.output_symbols
    batch_outputs = []
    num_output_examples = 0

    # prepare copied indices
    if FLAGS.use_copy and FLAGS.copy_fun == 'supervised':
        pointers = model_outputs.pointers
        sentence_length = pointers.shape[1]
        if FLAGS.token_decoding_algorithm == 'greedy':
            batch_copy_indices = np.reshape(np.argmax(pointers, 2),
                [FLAGS.batch_size, 1, sentence_length])
        else:
            batch_copy_indices = np.reshape(np.argmax(pointers, 2),
                [FLAGS.batch_size, FLAGS.beam_size, sentence_length])

    for batch_id in xrange(len(output_symbols)):
        top_k_predictions = output_symbols[batch_id]
        assert((FLAGS.token_decoding_algorithm == "greedy") or 
               len(top_k_predictions) == FLAGS.beam_size)
        if FLAGS.token_decoding_algorithm == "beam_search":
            beam_outputs = []
        else:
            top_k_predictions = [top_k_predictions]
        for beam_id in xrange(len(top_k_predictions)):
            # Step 1: transform the neural network output into readable strings
            prediction = top_k_predictions[beam_id]
            outputs = [int(pred) for pred in prediction]
            
            # If there is an EOS symbol in outputs, cut them at that point.
            if data_utils.EOS_ID in outputs:
                outputs = outputs[:outputs.index(data_utils.EOS_ID)]

            if nl_fillers is not None:
                cm_slots = {}

            tree, output_tokens = None, []
            if FLAGS.char:
                tg = "".join([as_str(output) for output in outputs])\
                    .replace(data_utils._UNK, ' ')
            else:
                for ii in xrange(len(outputs)):
                    output = outputs[ii]
                    if output < len(rev_tg_vocab):
                        pred_token = rev_tg_vocab[output]
                        if "@@" in pred_token:
                            pred_token = pred_token.split("@@")[-1]
                        if pred_token.startswith('__LF__'):
                            pred_token = pred_token[len('__LF__'):]
                        # process argument slots
                        if pred_token in constants._ENTITIES:
                            if nl_fillers is not None:
                                if ii > 0 and slot_filling.is_min_flag(
                                        rev_tg_vocab[outputs[ii-1]]):
                                    pred_token_type = 'Timespan'
                                else:
                                    pred_token_type = pred_token
                                cm_slots[ii] = (pred_token, pred_token_type)
                    else:
                        if FLAGS.use_copy:
                            pred_token = rev_sc_vocab[
                                encoder_inputs[len(encoder_inputs) - 1
                                    - (output - FLAGS.tg_vocab_size)][batch_id]]
                            if pred_token.startswith('__LF__'):
                                pred_token = pred_token[len('__LF__'):]
                        else:
                            pred_token = data_utils._UNK
                    output_tokens.append(pred_token)
                if FLAGS.partial_token:
                    # process partial-token outputs
                    merged_output_tokens = []
                    buffer = ''
                    load_buffer = False
                    for token in output_tokens:
                        if load_buffer:
                            if token == data_utils._ARG_END:
                                merged_output_tokens.append(buffer)
                                load_buffer = False
                                buffer = ''
                            else:
                                buffer += token
                        else:
                            if token == data_utils._ARG_START:
                                load_buffer = True
                            else:
                                merged_output_tokens.append(token)
                    output_tokens = merged_output_tokens
                tg = " ".join(output_tokens)
                      
            # check if the predicted command templates have enough slots to
            # hold the fillers (to rule out templates that are trivially
            # unqualified)
            if nl_fillers is None or len(cm_slots) >= len(nl_fillers):
                # Step 2: check if the predicted command template is grammatical
                if not FLAGS.explain:
                    if FLAGS.dataset.startswith("bash"):
                        tg = re.sub('( ;\s+)|( ;$)', ' \\; ', tg)
                        tree = data_tools.bash_parser(tg)
                    else:
                        tree = data_tools.paren_parser(tg)

                # filter out non-grammatical output
                if tree is not None or not FLAGS.grammatical_only:
                    output_example = False
                    if FLAGS.explain or not FLAGS.dataset.startswith("bash"):
                        temp = tg
                        output_example = True
                    else:
                        temp = data_tools.ast2template(tree,
                            loose_constraints=True, ignore_flag_order=False)
                        if nl_fillers is None:
                            output_example = True
                        else:
                            # Step 3: match the fillers to the argument slots
                            tree2, temp, _ = slot_filling.stable_slot_filling(
                                output_tokens, nl_fillers, cm_slots,
                                encoder_outputs[batch_id],
                                decoder_outputs[batch_id*FLAGS.beam_size+beam_id],
                                slot_filling_classifier, verbose=False)
                            if temp is not None:
                                output_example = True
                                tree = tree2
                    if output_example:
                        if FLAGS.token_decoding_algorithm == "greedy":
                            batch_outputs.append((tree, temp, outputs))
                        else:
                            beam_outputs.append((tree, temp, outputs))
                        num_output_examples += 1

            # TODO: the threshold is used to increase decoding speed
            if num_output_examples == 20:
                break

        if FLAGS.token_decoding_algorithm == "beam_search":
            if beam_outputs:
                batch_outputs.append(beam_outputs)

    if FLAGS.tg_char:
        char_output_symbols = model_outputs.char_output_symbols
        sentence_length = char_output_symbols.shape[0]
        batch_char_outputs = []
        batch_char_predictions = \
            [np.transpose(np.reshape(x, [sentence_length, FLAGS.beam_size,
                                         FLAGS.max_tg_token_size + 1]),
                          (1, 0, 2))
             for x in np.split(char_output_symbols, FLAGS.batch_size, 1)]
        for batch_id in xrange(len(batch_char_predictions)):
            beam_char_outputs = []
            top_k_char_predictions = batch_char_predictions[batch_id]
            for k in xrange(len(top_k_char_predictions)):
                top_k_char_prediction = top_k_char_predictions[k]
                sent = []
                for i in xrange(sentence_length):
                    word = ''
                    for j in xrange(FLAGS.max_tg_token_size):
                        char_prediction = top_k_char_prediction[i, j]
                        if char_prediction == data_utils.CEOS_ID or \
                            char_prediction == data_utils.CPAD_ID:
                            break
                        elif char_prediction in rev_tg_char_vocab:
                            word += rev_tg_char_vocab[char_prediction]
                        else:
                            word += data_utils._CUNK
                    sent.append(word)
                if data_utils._CATOM in sent:
                    sent = sent[:sent[:].index(data_utils._CATOM)]
                beam_char_outputs.append(' '.join(sent))
            batch_char_outputs.append(beam_char_outputs)
        return batch_outputs, batch_char_outputs
    else:
        return batch_outputs


def decode_set(sess, model, dataset, FLAGS, verbose=True):
    grouped_dataset = data_utils.group_data(dataset, use_bucket=True)
    vocabs = data_utils.load_vocab(FLAGS)
    rev_sc_vocab = vocabs.rev_sc_vocab

    slot_filling_classifier = None
    if FLAGS.fill_argument_slots:
        # create slot filling classifier
        mapping_param_dir = os.path.join(
            FLAGS.model_dir, 'train.mappings.X.Y.npz')
        train_X, train_Y = data_utils.load_slot_filling_data(mapping_param_dir)
        slot_filling_classifier = classifiers.KNearestNeighborModel(
            FLAGS.num_nn_slot_filling, train_X, train_Y)
        print('Slot filling classifier parameters loaded.')

    with DBConnection() as db:
        db.create_schema()
        db.remove_model(model.model_sig)

        sorted_sc_temps = sorted(grouped_dataset.keys(), key=lambda x:len(x))
        example_id = 0
        for sc_temp in sorted_sc_temps:
            example_id += 1
            data_group = grouped_dataset[sc_temp]

            sc_normalized_temp = ' '.join(
                [rev_sc_vocab[i] for i in data_group[0].sc_ids])
            if verbose:
                print("Example {}:".format(example_id))
                print("(Orig) Source: " + sc_temp.strip())
                print("Source: " + sc_normalized_temp)
                for j in xrange(len(data_group)):
                    print("GT Target {}: {}".format(
                        j+1, data_group[j].tg_txt.strip()))

            batch_outputs, output_logits = translate_fun(data_group, sess, model,
                vocabs, FLAGS, slot_filling_classifier=slot_filling_classifier)
            if FLAGS.tg_char:
                batch_outputs, batch_char_outputs = batch_outputs

            if FLAGS.token_decoding_algorithm == "greedy":
                if batch_outputs:
                    tree, pred_cmd, outputs = batch_outputs[0]
                    if FLAGS.dataset.startswith('bash') and not FLAGS.explain:
                        pred_cmd = data_tools.ast2command(
                            tree, loose_constraints=True)
                    score = output_logits[0]
                    print("{} ({})".format(pred_cmd, score))
                    db.add_prediction(
                        model.model_sig, sc_temp, pred_cmd, float(score))
                else:
                    print(APOLOGY_MSG)
            elif FLAGS.token_decoding_algorithm == "beam_search":
                if batch_outputs:
                    top_k_predictions = batch_outputs[0]
                    if FLAGS.tg_char:
                        top_k_char_predictions = batch_char_outputs[0]
                    top_k_scores = output_logits[0]
                    for j in xrange(min(FLAGS.beam_size, 10,
                                        len(batch_outputs[0]))):
                        if len(top_k_predictions) <= j:
                            break
                        top_k_pred_tree, top_k_pred_cmd, top_k_outputs = \
                            top_k_predictions[j]
                        if verbose:
                            if FLAGS.dataset.startswith('bash') and not FLAGS.explain:
                                pred_cmd = data_tools.ast2command(
                                    top_k_pred_tree, loose_constraints=True)
                            else:
                                pred_cmd = top_k_pred_cmd
                            print("Prediction {}: {} ({})".format(j+1,
                                pred_cmd, top_k_scores[j]))
                            if FLAGS.tg_char:
                                print("Character-based prediction {}: {}".format(
                                    j+1, top_k_char_predictions[j]))
                        db.add_prediction(model.model_sig, sc_temp,
                            pred_cmd, float(top_k_scores[j]),
                            update_mode=False)
                    print()
                else:
                    print(APOLOGY_MSG)

            # if attn_alignments is not None:
            #     if FLAGS.token_decoding_algorithm == "greedy":
            #         M = attn_alignments[batch_id, :, :]
            #     elif FLAGS.token_decoding_algorithm == "beam_search":
            #         M = attn_alignments[batch_id, 0, :, :]
            #     visualize_attn_alignments(M, sc, outputs, rev_sc_vocab, rev_tg_vocab,
            #         os.path.join(FLAGS.model_dir, "{}-{}.jpg".format(bucket_id, example_id)))


def print_test_results(test_file, output_file, sess, model, FLAGS):
    vocabs = data_utils.load_vocab(FLAGS)

    slot_filling_classifier = None
    if FLAGS.fill_argument_slots:
        # create slot filling classifier
        mapping_param_dir = os.path.join(
            FLAGS.model_dir, 'train.mappings.X.Y.npz')
        train_X, train_Y = \
            data_utils.load_slot_filling_data(mapping_param_dir)
        slot_filling_classifier = classifiers.KNearestNeighborModel(
            FLAGS.num_nn_slot_filling, train_X, train_Y)
        print('Slot filling classifier parameters loaded.')

    o_f = open(output_file, 'w')
    with open(test_file) as f:
        for line in f:
            sentence = line.strip()
            batch_outputs, output_logits = translate_fun(sentence, sess, model,
                vocabs, FLAGS, slot_filling_classifier=slot_filling_classifier)
            if FLAGS.token_decoding_algorithm == "greedy":
                tree, pred_cmd, outputs = batch_outputs[0]
                o_f.write(pred_cmd + '\n')
            elif FLAGS.token_decoding_algorithm == "beam_search":
                if batch_outputs:
                    top_k_predictions = batch_outputs[0]
                    for j in xrange(min(FLAGS.beam_size, 1, len(batch_outputs[0]))):
                        if len(top_k_predictions) <= j:
                            break
                        top_k_pred_tree, top_k_pred_cmd, top_k_outputs = \
                            top_k_predictions[j]
                        o_f.write(top_k_pred_cmd + '\n')
                else:
                    print('\m')
    o_f.close()


def visualize_attn_alignments(M, source, target, rev_sc_vocab,
                              rev_tg_vocab, output_path):
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
    plt.imshow(M[:i+1, :], interpolation='nearest', cmap=plt.cm.Blues)

    pad_size = source_length - len(nl)
    plt.xticks(xrange(source_length),
               [x.replace("$$", "") for x in reversed(
                   nl + [data_utils._PAD] * pad_size)],
               rotation='vertical')
    plt.yticks(xrange(len(cm)), [x.replace("$$", "") for x in cm],
               rotation='horizontal')

    plt.colorbar()

    plt.savefig(output_path, bbox_inches='tight')
