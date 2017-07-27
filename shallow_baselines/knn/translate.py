from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
import re

import tensorflow as tf

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "eval"))
    from bashlint import data_tools
    from encoder_decoder import data_utils, parse_args
    from nlp_tools import tokenizer, constants, slot_filling
    from eval import eval_tools
    from eval.eval_archive import DBConnection
    import knn_model
else:
    from bashlint import data_tools
    from encoder_decoder import data_utils, parse_args
    from eval import eval_tools
    from eval.eval_archive import DBConnection
    from shallow_baselines.knn import knn_model

FLAGS = tf.app.flags.FLAGS
parse_args.define_input_flags()

data_dir = FLAGS.data_dir

model_name = "knn"

def decode_set(model, dataset, rev_sc_vocab, rev_tg_vocab, verbose=True):
    grouped_dataset = data_utils.group_data_by_nl(dataset, use_bucket=False,
                                                  use_temp=False)

    with DBConnection() as db:
        db.remove_model(model_name)
        
        num_eval = 0
        for sc_temp in grouped_dataset:
            batch_sc_strs, batch_tg_strs, batch_scs, batch_cmds = \
                grouped_dataset[sc_temp]
            _, entities = tokenizer.ner_tokenizer(sc_temp)
            nl_fillers = entities[-1]
            if nl_fillers is not None:
                cm_slots = {}

            sc_str = batch_sc_strs[0]
            nl = batch_scs[0]
            if verbose:
                print("Example {}".format(num_eval+1))
                print("Original English: " + sc_str.strip())
                print("English: " + sc_temp)
                for j in xrange(len(batch_tg_strs)):
                    print("GT Command {}: {}".format(j+1, batch_tg_strs[j].strip()))
            # retrieve top-ranked command template
            top_k_results = model.test(nl, 100)
            count = 0
            for i in xrange(len(top_k_results)):
                nn, output_tokens, score = top_k_results[i]
                nn_str = ' '.join([rev_sc_vocab[j] for j in nn])
                tokens = []
                for j in xrange(1, len(output_tokens)-1):
                    pred_token = rev_tg_vocab[output_tokens[j]]
                    if "@@" in pred_token:
                        pred_token = pred_token.split("@@")[-1]
                    if nl_fillers is not None and \
                            pred_token in constants._ENTITIES:
                        if j > 0 and slot_filling.is_min_flag(
                                rev_tg_vocab[output_tokens[j-1]]):
                            pred_token_type = 'Timespan'
                        else:
                            pred_token_type = pred_token
                        cm_slots[j] = (pred_token, pred_token_type)
                    tokens.append(pred_token)
                pred_cmd = ' '.join(tokens)
                # check if the predicted command templates have enough slots to
                # hold the fillers (to rule out templates that are trivially
                # unqualified)
                if FLAGS.dataset.startswith("bash"):
                    pred_cmd = re.sub('( ;\s+)|( ;$)', ' \\; ', pred_cmd)
                    tree = data_tools.bash_parser(pred_cmd)
                else:
                    tree = data_tools.paren_parser(pred_cmd)
                if nl_fillers is None or len(cm_slots) >= len(nl_fillers):
                    # Step 2: check if the predicted command template is grammatical
                    # filter out non-grammatical output
                    if tree is not None:
                        matched = slot_filling.heuristic_slot_filling(tree, nl_fillers)
                if tree is not None:
                    slot_filling.fill_default_value(tree)
                    pred_cmd = data_tools.ast2command(tree)
                if verbose:
                    print("NN: {}".format(nn_str))
                    print("Prediction {}: {} ({})".format(i, pred_cmd, score))
                db.add_prediction(model_name, sc_str, pred_cmd, float(score),
                                      update_mode=False)
                count += 1
                if count == 10:
                    break
            print("")        
            num_eval += 1


def decode():
    # Load vocabularies.
    sc_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.sc_vocab_size)
    tg_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm.norm" % FLAGS.tg_vocab_size)
    sc_vocab, rev_sc_vocab = data_utils.initialize_vocabulary(sc_vocab_path)
    tg_vocab, rev_tg_vocab = data_utils.initialize_vocabulary(tg_vocab_path)

    train_set, dev_set, test_set = load_data()
    model = knn_model.KNNModel()
    model.train(train_set)

    decode_set(model, test_set, rev_sc_vocab, rev_tg_vocab)


def eval():
    # Load vocabularies.
    sc_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.sc_vocab_size)
    tg_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm.ast" % FLAGS.tg_vocab_size)
    sc_vocab, rev_sc_vocab = data_utils.initialize_vocabulary(sc_vocab_path)
    tg_vocab, rev_tg_vocab = data_utils.initialize_vocabulary(tg_vocab_path)

    train_set, dev_set, test_set = load_data()
    model = knn_model.KNNModel()
    model.train(train_set)
    print_eval_form(test_set)
    # eval_tools.eval_set(model_name, test_set, FLAGS)


def print_eval_form(dataset):
    eval_tools.print_evaluation_form(model_name, dataset, FLAGS,
                                     "predictions.csv")
    print("prediction results saved to {}".format('predictions.csv'))


def manual_eval():
    # Load vocabularies.
    sc_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.sc_vocab_size)
    tg_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm.ast" % FLAGS.tg_vocab_size)
    sc_vocab, rev_sc_vocab = data_utils.initialize_vocabulary(sc_vocab_path)
    tg_vocab, rev_tg_vocab = data_utils.initialize_vocabulary(tg_vocab_path)

    train_set, dev_set, test_set = load_data()
    model = knn_model.KNNModel()
    model.train(train_set)
    eval_tools.manual_eval(model_name, test_set, rev_sc_vocab,
                           FLAGS, FLAGS.model_dir, num_eval=500)

# Chenglong's main function
def original():
    # test_vec = [26, 12, 10, 11, 15, 17, 28, 171, 18, 339]

    # print "[command] ", decode_vec_to_str(test_vec, sc_dictionary)

    # find k nearest neighbor
    # knn = find_k_nearest_neighbor(test_vec, sc_vec_list, 1)

    # for p in knn:
    #  print "[nn vec] ", p
    # print the decoding result of these filters
    #  print "[nearest neighbor] ", decode_vec_to_str(p[0], sc_dictionary)

    sys.stdout = open('result.txt', 'w')

    # Load vocabularies.
    sc_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.sc_vocab_size)
    tg_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm" % FLAGS.tg_vocab_size)
    sc_vocab, rev_sc_vocab = data_utils.initialize_vocabulary(sc_vocab_path)
    tg_vocab, rev_tg_vocab = data_utils.initialize_vocabulary(tg_vocab_path)
    # the file containing traning nl vectors and cmd vectors
    train_set, dev_set, _ = load_data()

    model = knn.KNNModel()
    model.train(train_set)

    test_tg_vec_list = [cmd_vec for _, _, _, cmd_vec in dev_set]
    test_sc_vec_list = [sc_vec for _, _, sc_vec, _ in dev_set]

    for i in range(len(test_sc_vec_list)):
        test_vec = test_sc_vec_list[i]
        cmd_vec = test_tg_vec_list[i]

        nl, cmd, score = model.test(test_vec, 1)

        print("[text-case ", i, "] =========================================================")
        print("  [original-pair]")
        print("     ", knn.decode_vec_to_str(test_vec, rev_sc_vocab))
        print("     ", knn.decode_vec_to_str(cmd_vec, rev_tg_vocab))
        print("  [new-pair]")
        print("     ", knn.decode_vec_to_str(nl, rev_sc_vocab))
        print("     ", knn.decode_vec_to_str(cmd, rev_tg_vocab))
        print(knn.decode_vec_to_str(cmd, rev_tg_vocab))


def load_data():
    return data_utils.load_data(FLAGS, buckets=None)

def main():
    # set up data and model directories
    FLAGS.data_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", FLAGS.dataset)
    print("Reading data from {}".format(FLAGS.data_dir))

    if FLAGS.manual_eval:
        manual_eval()
    elif FLAGS.eval:
        eval()
    elif FLAGS.decode:
        decode()


if __name__ == '__main__':
    main()
