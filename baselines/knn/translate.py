import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'bashlex'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'eval'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'seq2tree'))

import tensorflow as tf

import data_tools, data_utils, eval_tools
import parse_args
import knn
from eval_archive import DBConnection

FLAGS = tf.app.flags.FLAGS
data_dir = FLAGS.data_dir

def decode_set(model, dataset, rev_nl_vocab, rev_cm_vocab, verbose=True):
    grouped_dataset = data_utils.group_data_by_nl(dataset, use_bucket=True)

    with DBConnection() as db:
        num_eval = 0
        for nl_template in grouped_dataset:
            batch_nl_strs, batch_cm_strs, batch_nls, batch_cmds = \
                grouped_dataset[[nl_template]]

            batch_size = len(batch_nl_strs)

            for batch_id in xrange(batch_size):
                nl_str = batch_nl_strs[batch_id]
                cm_strs = batch_cm_strs[batch_id]
                nl = batch_nls[batch_id]

                if verbose:
                    print("Example {}".format(num_eval))
                    print("Original English: " + nl_str.strip())
                    print("English: " + ' '.join([rev_nl_vocab[i] for i in nl]))
                    for j in xrange(len(cm_strs)):
                        print("GT Command {}: {}".format(j+1, cm_strs[j].strip()))

                nl, pred_cmd, score = model.test(nl, 1)
                tree = data_tools.bash_parse(pred_cmd)
                db.add_prediction("knn", nl, pred_cmd, score)
                if verbose:
                    print("Prediction: {} ({})".format(pred_cmd, score))
                    print("AST: ")
                    data_tools.pretty_print(tree, 0)
                    print()
                break
            num_eval += 1


def decode():
    # Load vocabularies.
    nl_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.nl_vocab_size)
    cm_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm.ast" % FLAGS.cm_vocab_size)
    nl_vocab, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
    cm_vocab, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

    train_set, dev_set, _ = data_utils.load_data(FLAGS, None)
    model = knn.KNNModel()
    model.train(train_set)

    decode_set(model, dev_set, rev_nl_vocab, rev_cm_vocab)


# Chenglong's main function
def manual_eval():
    # test_vec = [26, 12, 10, 11, 15, 17, 28, 171, 18, 339]

    # print "[command] ", decode_vec_to_str(test_vec, nl_dictionary)

    # find k nearest neighbor
    # knn = find_k_nearest_neighbor(test_vec, nl_vec_list, 1)

    # for p in knn:
    #  print "[nn vec] ", p
    # print the decoding result of these filters
    #  print "[nearest neighbor] ", decode_vec_to_str(p[0], nl_dictionary)

    sys.stdout = open('result.txt', 'w')

    # Load vocabularies.
    nl_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.nl_vocab_size)
    cm_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm.ast" % FLAGS.cm_vocab_size)
    nl_vocab, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
    cm_vocab, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
    # the file containing traning nl vectors and cmd vectors
    train_set, dev_set, _ = data_utils.load_data(FLAGS, None)

    model = knn.KNNModel()
    model.train(train_set)

    test_cmd_vec_list = [cmd_vec for _, _, _, cmd_vec in dev_set]
    test_nl_vec_list = [nl_vec for _, _, nl_vec, _ in dev_set]

    for i in range(len(test_nl_vec_list)):
        test_vec = test_nl_vec_list[i]
        cmd_vec = test_cmd_vec_list[i]

        nl, cmd, score = model.test(test_vec, 1)

        print "[text-case ", i, "] ========================================================="
        print "  [original-pair]"
        print "     ", knn.decode_vec_to_str(test_vec, rev_nl_vocab)
        print "     ", knn.decode_vec_to_str(cmd_vec, rev_cm_vocab)
        print "  [new-pair]"
        print "     ", knn.decode_vec_to_str(nl, rev_nl_vocab)
        print "     ", knn.decode_vec_to_str(cmd, rev_cm_vocab)
        print knn.decode_vec_to_str(cmd, rev_cm_vocab)


def main():
    if FLAGS.manual_eval:
        manual_eval()
    elif FLAGS.decode:
        decode()


if __name__ == '__main__':
    parse_args.define_input_flags()
    main()