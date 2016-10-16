import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'bashlex'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'encoder_decoder'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'eval'))

import tensorflow as tf

import data_tools, data_utils, eval_tools
import parse_args
import knn
from eval_archive import DBConnection

FLAGS = tf.app.flags.FLAGS
parse_args.define_input_flags()

data_dir = FLAGS.data_dir

model_name = "knn"

def decode_set(model, dataset, rev_nl_vocab, rev_cm_vocab, verbose=True):
    grouped_dataset = data_utils.group_data_by_nl(dataset)

    with DBConnection() as db:
        db.remove_model(model_name)
        num_eval = 0
        for nl_temp in grouped_dataset:
            batch_nl_strs, batch_cm_strs, batch_nls, batch_cmds = \
                grouped_dataset[nl_temp]

            nl_str = batch_nl_strs[0]
            nl = batch_nls[0]
            if verbose:
                print("Example {}".format(num_eval+1))
                print("Original English: " + nl_str.strip())
                print("English: " + nl_temp)
                for j in xrange(len(batch_cm_strs)):
                    print("GT Command {}: {}".format(j+1, batch_cm_strs[j].strip()))
            top_k_results = model.test(nl, 10)
            for i in xrange(len(top_k_results)):
                nn, cmd, score = top_k_results[i]
                nn_str = ' '.join([rev_nl_vocab[i] for i in nn])
                pred_cmd = ' '.join([rev_cm_vocab[i] for i in cmd])
                tree = data_tools.bash_parser(pred_cmd)
                if verbose:
                    print("NN: {}".format(nn_str))
                    print("Prediction {}: {} ({})".format(i, pred_cmd, score))
                    print("AST: ")
                    data_tools.pretty_print(tree, 0)
                    print
                db.add_prediction(model_name, nl_str, pred_cmd, float(score),
                                  update_mode=False)
            
            num_eval += 1


def decode():
    # Load vocabularies.
    nl_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.nl_vocab_size)
    cm_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm" % FLAGS.cm_vocab_size)
    nl_vocab, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
    cm_vocab, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

    train_set, dev_set, _ = load_data()
    model = knn.KNNModel()
    model.train(train_set)

    decode_set(model, dev_set, rev_nl_vocab, rev_cm_vocab)


def eval():
    # Load vocabularies.
    nl_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.nl_vocab_size)
    cm_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm.ast" % FLAGS.cm_vocab_size)
    nl_vocab, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
    cm_vocab, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

    train_set, dev_set, _ = load_data()
    model = knn.KNNModel()
    model.train(train_set)
    eval_tools.eval_set(model_name, dev_set, rev_nl_vocab, FLAGS)


def manual_eval():
    # Load vocabularies.
    nl_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.nl_vocab_size)
    cm_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm.ast" % FLAGS.cm_vocab_size)
    nl_vocab, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
    cm_vocab, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

    train_set, dev_set, _ = load_data()
    model = knn.KNNModel()
    model.train(train_set)
    eval_tools.manual_eval(model_name, dev_set, rev_nl_vocab,
                           FLAGS, FLAGS.model_dir, num_eval=500)

# Chenglong's main function
def original():
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
                                 "vocab%d.cm" % FLAGS.cm_vocab_size)
    nl_vocab, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
    cm_vocab, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
    # the file containing traning nl vectors and cmd vectors
    train_set, dev_set, _ = load_data()

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


def load_data():
    print("Loading data from %s" % FLAGS.data_dir)
    nl_extention = ".ids%d.nl" % FLAGS.nl_vocab_size
    cm_extension = ".ids%d.cm" % FLAGS.cm_vocab_size

    nl_txt_train = os.path.join(data_dir, "train") + ".nl"
    cm_txt_train = os.path.join(data_dir, "train") + ".cm"
    nl_txt_dev = os.path.join(data_dir, "dev") + ".nl"
    cm_txt_dev = os.path.join(data_dir, "dev") + ".cm"
    nl_txt_test = os.path.join(data_dir, "test") + ".nl"
    cm_txt_test = os.path.join(data_dir, "test") + ".cm"

    nl_train = os.path.join(data_dir, "train") + nl_extention
    cm_train = os.path.join(data_dir, "train") + cm_extension
    nl_dev = os.path.join(data_dir, "dev") + nl_extention
    cm_dev = os.path.join(data_dir, "dev") + cm_extension
    nl_test = os.path.join(data_dir, "test") + nl_extention
    cm_test = os.path.join(data_dir, "test") + cm_extension

    train_set = data_utils.read_data(nl_txt_train, cm_txt_train, nl_train, cm_train, None,
                                     FLAGS.max_train_data_size)
    dev_set = data_utils.read_data(nl_txt_dev, cm_txt_dev, nl_dev, cm_dev, None)
    test_set = data_utils.read_data(nl_txt_test, cm_txt_test, nl_test, cm_test, None)

    return train_set, dev_set, test_set


def main():
    if FLAGS.manual_eval:
        manual_eval()
    elif FLAGS.eval:
        eval()
    elif FLAGS.decode:
        decode()
    elif FLAGS.self_test:
        original()


if __name__ == '__main__':
    main()
