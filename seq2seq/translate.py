# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Binary for training translation models and decoding from them.

Running this program without --decode will read in the raw training data, perform
tokenization, and then start training a model saving checkpoints to --train_dir.

Running with --decode starts an interactive loop so you can see how
the current checkpoint translates English sentences into French.

See the following papers for more information on neural translation models.
 * http://arxiv.org/abs/1409.3215
 * http://arxiv.org/abs/1409.0473
 * http://arxiv.org/abs/1412.2007
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import random
import sys
sys.path.append("../bashlex")
sys.path.append("../eval")

import time
import cPickle as pickle

import numpy as np

from data_tools import basic_tokenizer, bash_tokenizer

import tensorflow as tf
import seq2seq_model

import data_utils

tf.app.flags.DEFINE_float("learning_rate", 0.001, "Learning rate.")
tf.app.flags.DEFINE_float("learning_rate_decay_factor", 0.99,
                          "Learning rate decays by this much.")
tf.app.flags.DEFINE_float("input_keep_prob", 1.0,
                          "Dropout: proportion of input units to keep.")
tf.app.flags.DEFINE_float("output_keep_prob", 1.0,
                          "Dropout: proportion of output units to keep.")
tf.app.flags.DEFINE_float("max_gradient_norm", 5.0,
                          "Clip gradients to this norm.")
tf.app.flags.DEFINE_integer("batch_size", 128,
                            "Batch size to use during training.")
tf.app.flags.DEFINE_integer("size", 300, "Size of each model layer.")
tf.app.flags.DEFINE_integer("num_layers", 1, "Number of layers in the model.")
tf.app.flags.DEFINE_integer("nl_vocab_size", 1500, "English vocabulary size.")
tf.app.flags.DEFINE_integer("cm_vocab_size", 1500, "Bash vocabulary size.")
tf.app.flags.DEFINE_string("data_dir", "/tmp", "Data directory")
tf.app.flags.DEFINE_string("train_dir", "/tmp", "Directory to save trained models.")
tf.app.flags.DEFINE_string("data_split", "command", "")
tf.app.flags.DEFINE_string("decoder", "greedy", "Type of decoder to use.")
tf.app.flags.DEFINE_integer("beam_size", 3, "Size of beam for beam search.")
tf.app.flags.DEFINE_integer("max_train_data_size", 0,
                            "Limit on the size of training data (0: no limit).")
tf.app.flags.DEFINE_integer("steps_per_checkpoint", 200,
                            "How many training steps to do per checkpoint.")
tf.app.flags.DEFINE_integer("steps_per_milestone", 1000,
                            "How many training steps to do per dev-set evaluation")
tf.app.flags.DEFINE_integer("num_milestones", 5,
                            "How many dev-set evaluation to be performed during training")
tf.app.flags.DEFINE_integer("gpu", 0, "GPU device where the computation is going to be placed.")
tf.app.flags.DEFINE_boolean("log_device_placement", False,
                            "Set to True for logging device placement.")
tf.app.flags.DEFINE_boolean("lstm", False,
                            "Set to True for training with LSTM cells.")
tf.app.flags.DEFINE_boolean("eval", False,
                            "Set to True for quantitive evaluation.")
tf.app.flags.DEFINE_boolean("decode", False,
                            "Set to True for interactive decoding.")
tf.app.flags.DEFINE_boolean("process_data", False,
                            "Set to True for data preprocessing.")
tf.app.flags.DEFINE_boolean("bucket_selection", False,
                            "Run a bucket_selection if this is set to True.")
tf.app.flags.DEFINE_boolean("self_test", False,
                            "Run a self-test if this is set to True.")

FLAGS = tf.app.flags.FLAGS

# We use a number of buckets and pad to the closest one for efficiency.
# See seq2seq_model.Seq2SeqModel for details of how they work.
_buckets = [(5, 10), (10, 20), (20, 30), (30, 40), (40, 50)]

def read_data(source_path, target_path, max_size=None):
    """Read data from source and target files and put into buckets.

    Args:
      source_path: path to the files with token-ids for the source language.
      target_path: path to the file with token-ids for the target language;
        it must be aligned with the source file: n-th line contains the desired
        output for n-th line from the source_path.
      max_size: maximum number of lines to read, all other will be ignored;
        if 0 or None, data files will be read completely (no limit).

    Returns:
      data_set: a list of length len(_buckets); data_set[n] contains a list of
        (source, target) pairs read from the provided data files that fit
        into the n-th bucket, i.e., such that len(source) < _buckets[n][0] and
        len(target) < _buckets[n][1]; source and target are lists of token-ids.
    """
    data_set = [[] for _ in _buckets]
    with tf.gfile.GFile(source_path, mode="r") as source_file:
        with tf.gfile.GFile(target_path, mode="r") as target_file:
            source, target = source_file.readline(), target_file.readline()
            counter = 0
            while source and target and (not max_size or counter < max_size):
                counter += 1
                if counter % 1000 == 0:
                    print("  reading data line %d" % counter)
                    sys.stdout.flush()
                source_ids = [int(x) for x in source.split()]
                target_ids = [int(x) for x in target.split()]
                target_ids.append(data_utils.EOS_ID)
                for bucket_id, (source_size, target_size) in enumerate(_buckets):
                    if len(source_ids) < source_size and len(target_ids) < target_size:
                        data_set[bucket_id].append([source_ids, target_ids])
                        break
                source, target = source_file.readline(), target_file.readline()
    return data_set


def create_model(session, forward_only):
    """Create translation model and initialize or load parameters in session."""
    beam_decoder = None
    model = seq2seq_model.Seq2SeqModel(
        FLAGS.nl_vocab_size, FLAGS.cm_vocab_size, _buckets,
        FLAGS.size, FLAGS.num_layers, FLAGS.max_gradient_norm, FLAGS.batch_size,
        FLAGS.learning_rate, FLAGS.learning_rate_decay_factor,
        FLAGS.input_keep_prob, FLAGS.output_keep_prob,
        forward_only=forward_only,
        use_lstm=FLAGS.lstm,
        beam_decoder=beam_decoder
        )
    ckpt = tf.train.get_checkpoint_state(FLAGS.train_dir)
    if ckpt and tf.gfile.Exists(ckpt.model_checkpoint_path):
        print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        print("Created model with fresh parameters.")
        session.run(tf.initialize_all_variables())
    return model


def train(train_set, dev_set, num_iter):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        print("Creating %d layers of %d units." % (FLAGS.num_layers, FLAGS.size))
        model = create_model(sess, False)

        train_bucket_sizes = [len(train_set[b]) for b in xrange(len(_buckets))]
        train_total_size = float(sum(train_bucket_sizes))

        # A bucket scale is a list of increasing numbers from 0 to 1 that we'll use
        # to select a bucket. Length of [scale[i], scale[i+1]] is proportional to
        # the size if i-th training bucket, as used later.
        train_buckets_scale = [sum(train_bucket_sizes[:i + 1]) / train_total_size
                               for i in xrange(len(train_bucket_sizes))]

        # This is the training loop.
        step_time, loss = 0.0, 0.0
        current_step = 0
        previous_losses = []
        previous_dev_losses = []

        # Load Vocabularies for evaluation on dev set at each checkpoint
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        # nl_vocab, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

        for t in xrange(num_iter):
            # Choose a bucket according to data distribution. We pick a random number
            # in [0, 1] and use the corresponding interval in train_buckets_scale.
            random_number_01 = np.random.random_sample()
            bucket_id = min([i for i in xrange(len(train_buckets_scale))
                             if train_buckets_scale[i] > random_number_01])

            # Get a batch and make a step.
            start_time = time.time()
            encoder_inputs, decoder_inputs, target_weights = model.get_batch(
                train_set, bucket_id)
            _, step_loss, _ = model.step(sess, encoder_inputs, decoder_inputs,
                                         target_weights, bucket_id, False)
            step_time += (time.time() - start_time) / FLAGS.steps_per_checkpoint
            loss += step_loss / FLAGS.steps_per_checkpoint
            current_step += 1

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if current_step % FLAGS.steps_per_checkpoint == 0:

                # Print statistics for the previous epoch.
                perplexity = math.exp(loss) if loss < 300 else float('inf')
                print("global step %d learning rate %.4f step-time %.2f perplexity "
                      "%.2f" % (model.global_step.eval(), model.learning_rate.eval(),
                                step_time, perplexity))

                # Decrease learning rate if no improvement of loss was seen over last 3 times.
                if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                    sess.run(model.learning_rate_decay_op)
                previous_losses.append(loss)

                # Save checkpoint and zero timer and loss.
                checkpoint_path = os.path.join(FLAGS.train_dir, "translate.ckpt")
                model.saver.save(sess, checkpoint_path, global_step=model.global_step)
                
                step_time, loss, dev_loss = 0.0, 0.0, 0.0
                
                # Run evals on development set and print their perplexity.
                for bucket_id in xrange(len(_buckets)):
                    if len(dev_set[bucket_id]) == 0:
                        print("  eval: empty bucket %d" % (bucket_id))
                        continue
                    encoder_inputs, decoder_inputs, target_weights = model.get_batch(
                        dev_set, bucket_id)
                    _, eval_loss, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
                                                             target_weights, bucket_id, True)
                    dev_loss += eval_loss
                    eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
                    print("  eval: bucket %d perplexity %.2f" % (bucket_id, eval_ppx))

                dev_perplexity = math.exp(dev_loss/len(_buckets)) if dev_loss < 300 else float('inf')
                print("global step %d learning rate %.4f step-time %.2f dev_perplexity "
                      "%.2f" % (model.global_step.eval(), model.learning_rate.eval(),
                                step_time, dev_perplexity))

                # Early stop if no improvement of dev loss was seen over last 3 times.
                if len(previous_dev_losses) > 2 and dev_loss > max(previous_dev_losses[-3:]):
                    return False
                previous_dev_losses.append(dev_loss)

                sys.stdout.flush()
    return True


def decode(output_logits, rev_cm_vocab, beam_decoder):
    if FLAGS.decoder == "greedy":
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
    elif FLAGS.decoder == "beam_search":
        outputs = [np.argmax(logit, axis=1) for logit in output_logits]

    # If there is an EOS symbol in outputs, cut them at that point.
    if data_utils.EOS_ID in outputs:
        outputs = outputs[:outputs.index(data_utils.EOS_ID)]
    # Print out command corresponding to outputs.
    return " ".join([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs])


def batch_decode(output_logits, rev_cm_vocab, beam_decoder):
    batch_size = len(output_logits[0])
    batch_outputs = []
    if FLAGS.decoder == "greedy":
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        predictions = [np.argmax(logit, axis=1) for logit in output_logits]
    elif FLAGS.decoder == "beam_search":
        predictions = [np.argmax(logit, axis=1) for logit in output_logits]
    for i in xrange(batch_size):
        outputs = [int(pred[i]) for pred in predictions]
        # If there is an EOS symbol in outputs, cut them at that point.
        if data_utils.EOS_ID in outputs:
            outputs = outputs[:outputs.index(data_utils.EOS_ID)]
            # Print out command corresponding to outputs.
            batch_outputs.append(" ".join([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs]))
    return batch_outputs


def eval_set(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab, verbose=True):

    num_eval = 0
    for bucket_id in xrange(len(_buckets)):
        if len(dev_set[bucket_id]) == 0:
            continue
        model.batch_size = len(dev_set[bucket_id])

        encoder_inputs, decoder_inputs, target_weights = model.get_bucket(
                    dev_set, bucket_id)
        _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
                                         target_weights, bucket_id, True)

        rev_encoder_inputs = []
        for i in xrange(len(encoder_inputs)-1, -1, -1):
            rev_encoder_inputs.append(encoder_inputs[i])
        sentences = data_utils.token_ids_to_sentences(rev_encoder_inputs, rev_nl_vocab)
        ground_truths = data_utils.token_ids_to_sentences(decoder_inputs, rev_cm_vocab, True)
        assert(len(sentences) == len(ground_truths))
        predictions = batch_decode(output_logits, rev_cm_vocab, model.beam_decoder)
        assert(len(ground_truths) == len(predictions))
        for i in xrange(len(ground_truths)):
            sent = sentences[i]
            gt = ground_truths[i]
            pred = predictions[i]
            print("Example %d" % (num_eval + 1))
            print("English: " + sent)
            print("Ground truth: " + gt)
            print("Prediction: " + pred)
            print()
            num_eval += 1


def eval_model(sess, dev_set, rev_nl_vocab, rev_cm_vocab, verbose=True):
    # Create model and load parameters.
    model = create_model(sess, True)
    eval_set(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab, verbose)


def eval(verbose=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model = create_model(sess, forward_only=True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
        _, dev_set, _ = load_data()

        eval_set(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab, verbose)


def train_and_eval(train_set, dev_set):
    num_iter = FLAGS.steps_per_milestone
    for i in xrange(FLAGS.num_milestones):
        is_learning = train(train_set, dev_set, num_iter)
        tf.reset_default_graph()
        eval(False)
        tf.reset_default_graph()

        if not is_learning:
            print("Training stopped early for no improvement observed on dev set.")
            break

def _decode():
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model = create_model(sess, True)
        model.batch_size = 1  # We decode one sentence at a time.

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        nl_vocab, _ = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

        # Decode from standard input.
        sys.stdout.write("> ")
        sys.stdout.flush()
        sentence = sys.stdin.readline()
        while sentence:
            # Get token-ids for the input sentence.
            token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), nl_vocab,
                                                         basic_tokenizer)
            # Which bucket does it belong to?
            bucket_id = min([b for b in xrange(len(_buckets))
                             if _buckets[b][0] > len(token_ids)])
            # Get a 1-element batch to feed the sentence to the model.
            encoder_inputs, decoder_inputs, target_weights = model.get_batch(
                {bucket_id: [(token_ids, [])]}, bucket_id)
            # Get output logits for the sentence.
            _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
                                             target_weights, bucket_id, True)
            print(decode(output_logits, rev_cm_vocab, model.beam_decoder))
            print("> ", end="")
            sys.stdout.flush()
            sentence = sys.stdin.readline()


def process_data():
    print("Preparing data in %s" % FLAGS.data_dir)

    with open(FLAGS.data_dir + "data.dat") as f:
        data = pickle.load(f)

    numFolds = len(data)
    print("%d folds" % numFolds)

    train_cm_list = []
    train_nl_list = []
    dev_cm_list = []
    dev_nl_list = []
    test_cm_list = []
    test_nl_list = []
    for i in xrange(numFolds):
        if i < numFolds - 2:
            for nl, cmd in data[i]:
                train_cm_list.append(cmd)
                train_nl_list.append(nl)
        elif i == numFolds - 2:
            for nl, cmd in data[i]:
                dev_cm_list.append(cmd)
                dev_nl_list.append(nl)
        elif i == numFolds - 1:
            for nl, cmd in data[i]:
                test_cm_list.append(cmd)
                test_nl_list.append(nl)

    train_dev_test = {}
    train_dev_test["train"] = [train_cm_list, train_nl_list]
    train_dev_test["dev"] = [dev_cm_list, dev_nl_list]
    train_dev_test["test"] = [test_cm_list, test_nl_list]

    nl_train, cm_train, nl_dev, cm_dev, nl_test, cm_test, _, _ = data_utils.prepare_data(
        train_dev_test, FLAGS.data_dir, FLAGS.nl_vocab_size, FLAGS.cm_vocab_size)

    train_set = read_data(nl_train, cm_train, FLAGS.max_train_data_size)
    dev_set = read_data(nl_dev, cm_dev)
    test_set = read_data(nl_test, nl_test)

    with open(FLAGS.data_dir + "data.processed.dat", 'wb') as o_f:
        pickle.dump((train_set, dev_set, test_set), o_f)
    return train_set, dev_set, test_set


def load_data(sample_size=-1):
    print("Loading data from %s" % FLAGS.data_dir)

    data_dir = FLAGS.data_dir
    nl_train = os.path.join(data_dir, "train") + ".ids%d.nl" % FLAGS.nl_vocab_size
    cm_train = os.path.join(data_dir, "train") + ".ids%d.cm" % FLAGS.cm_vocab_size
    nl_dev = os.path.join(data_dir, "dev") + ".ids%d.nl" % FLAGS.nl_vocab_size
    cm_dev = os.path.join(data_dir, "dev") + ".ids%d.cm" % FLAGS.cm_vocab_size
    nl_test = os.path.join(data_dir, "test") + ".ids%d.nl" % FLAGS.nl_vocab_size
    cm_test = os.path.join(data_dir, "test") + ".ids%d.cm" % FLAGS.cm_vocab_size

    train_set = read_data(nl_train, cm_train, FLAGS.max_train_data_size)
    dev_set = read_data(nl_dev, cm_dev)
    test_set = read_data(nl_test, cm_test)

    return train_set, dev_set, test_set


def bucket_selection(num_buckets=10):
    with open(FLAGS.data_dir + "data.dat") as f:
        data = pickle.load(f)

    numFolds = len(data)
    print("%d folds" % numFolds)

    train_data = []
    for i in xrange(numFolds):
        if i < numFolds - 2:
            for nl, cmd in data[i]:
                train_data.append((nl, cmd))

    sorted_data = sorted(train_data, key=lambda x:(len(basic_tokenizer(x[0])), 
                                                   len(bash_tokenizer(x[1]))))
    bucket_size = len(sorted_data) / num_buckets
    for i in xrange(num_buckets):
        print(int(bucket_size * (i+1)))
        mark = sorted_data[int(bucket_size * (i+1))-1]
        print(mark)
        print(len(basic_tokenizer(mark[0])), len(bash_tokenizer(mark[1])))


def self_test():
    """Test the translation model."""
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        print("Self-test for neural translation model.")
        # Create model with vocabularies of 10, 2 small buckets, 2 layers of 32.
        model = seq2seq_model.Seq2SeqModel(10, 10, [(3, 3), (6, 6)], 32, 2,
                                           5.0, 32, 0.3, 0.99, num_samples=8)
        sess.run(tf.initialize_all_variables())

        # Fake data set for both the (3, 3) and (6, 6) bucket.
        data_set = ([([1, 1], [2, 2]), ([3, 3], [4]), ([5], [6])],
                    [([1, 1, 1, 1, 1], [2, 2, 2, 2, 2]), ([3, 3, 3], [5, 6])])
        for _ in xrange(5):  # Train the fake model for 5 steps.
            bucket_id = random.choice([0, 1])
            encoder_inputs, decoder_inputs, target_weights = model.get_batch(
                data_set, bucket_id)
            model.step(sess, encoder_inputs, decoder_inputs, target_weights,
                       bucket_id, False)


def main(_):
    # set GPU device
    with tf.device('/gpu:%d' % FLAGS.gpu):
        if FLAGS.self_test:
            self_test()
        elif FLAGS.eval:
            eval()
        elif FLAGS.decode:
            _decode()
        elif FLAGS.bucket_selection:
            bucket_selection()
        elif FLAGS.process_data:
            process_data()
        else:
            train_set, dev_set, _ = load_data()
            train_and_eval(train_set, dev_set)


if __name__ == "__main__":
    tf.app.run()
