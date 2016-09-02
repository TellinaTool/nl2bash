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
import sys
sys.path.append("../bashlex")
sys.path.append("../eval")
sys.path.append("../seq2tree")

import cPickle as pickle
import collections
import time

import numpy as np

import tensorflow as tf

import data_utils, data_tools
import parse_args
import seq2seq_model
import eval_tools


FLAGS = tf.app.flags.FLAGS

# We use a number of buckets and pad to the closest one for efficiency.
# See seq2seq_model.Seq2SeqModel for details of how they work.
if FLAGS.char:
    _buckets = [(10, 20), (20, 30), (40, 50), (60, 80), (80, 100), (100, 120), (120, 120), (140, 120)]
else:
    _buckets = [(5, 10), (10, 20), (20, 30), (30, 40), (40, 40), (50, 40)]


def create_model(session, forward_only):
    """
    :param source_vocab_size: size of the source vocabulary.
    :param target_vocab_size: size of the target vocabulary.
    :param max_source_length: maximum length of the source sequence
        (necessary for static graph construction).
    :param max_target_length: maximum length of the target sequence
        (necessary for static graph construction).
    :param dim: dimension of each layer in the model.
    :param num_layers: number of layers in the model.
    :param max_gradient_norm: gradients are clipped to maximally this norm.
    :param batch_size: the size of the batches used during training or decoding.
    :param learning_rate: learning rate to start with.
    :param learning_rate_decay_factor: decay learning rate by this much when needed.
            not import if the adam optimizer is used.
    :param input_keep_prob: proportion of input to keep if dropout is used.
    :param output_keep_prob: proportion of output to keep if dropout is used.
    :param num_samples: number of samples for sampled softmax.

    :param decoder_topology: topology of the tree rnn decoder.
    :param decoding_algorithm: decoding algorithm used.
    :param
    """
    params = collections.defaultdict()
    params["source_vocab_size"] = FLAGS.nl_vocab_size
    params["target_vocab_size"] = FLAGS.cm_vocab_size
    params["max_source_length"] = FLAGS.max_nl_length
    params["max_target_length"] = FLAGS.max_cm_length
    params["dim"] = FLAGS.dim
    params["rnn_cell"] = FLAGS.rnn_cell
    params["num_layers"] = FLAGS.num_layers
    params["max_gradient_norm"] = FLAGS.max_gradient_norm
    params["batch_size"] = FLAGS.batch_size
    params["num_samples"] = FLAGS.num_samples
    params["input_keep_prob"] = FLAGS.input_keep_prob
    params["output_keep_prob"] = FLAGS.output_keep_prob
    params["optimizer"] = FLAGS.optimizer
    params["learning_rate"] = FLAGS.learning_rate
    params["learning_rate_decay_factor"] = FLAGS.learning_rate_decay_factor
    params["use_attention"] = FLAGS.use_attention
    params["use_copy"] = FLAGS.use_copy

    params["decoder_topology"] = FLAGS.decoder_topology

    params["decoding_algorithm"] = FLAGS.decoding_algorithm

    model = seq2seq_model.Seq2SeqModel(params, _buckets, forward_only)

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
    if FLAGS.char:
        return "".join([tf.compat.as_str(rev_cm_vocab[output]).strip() for output in outputs]) \
                .replace(data_utils._UNK, ' ')
    else:
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
        if FLAGS.char:
            batch_outputs.append("".join([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs]) \
                                .replace(data_utils._UNK, ' '))
        else:
            batch_outputs.append(" ".join([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs]))
    return batch_outputs


def manual_eval():
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
        _, dev_set, _ = load_data()

        eval_tools.manual_eval(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab,
                               FLAGS, num_eval=30)


def eval(verbose=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model = create_model(sess, forward_only=True)

        # Load vocabularies.
        if FLAGS.char:
            nl_vocab_path = os.path.join(FLAGS.data_dir,
                                         "vocab%d.nl.char" % FLAGS.nl_vocab_size)
            cm_vocab_path = os.path.join(FLAGS.data_dir,
                                         "vocab%d.cm.char" % FLAGS.cm_vocab_size)
        else:
            nl_vocab_path = os.path.join(FLAGS.data_dir,
                                         "vocab%d.nl" % FLAGS.nl_vocab_size)
            cm_vocab_path = os.path.join(FLAGS.data_dir,
                                         "vocab%d.cm" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
        _, dev_set, _ = load_data()

        eval_tools.eval_set(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab,
                            FLAGS, verbose)


def interactive_decode():
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        nl_vocab, _ = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

        eval_tools.interactive_decode(sess, model, nl_vocab, rev_cm_vocab,
                                      FLAGS)


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


def load_data(sample_size=-1):
    print("Loading data from %s" % FLAGS.data_dir)

    data_dir = FLAGS.data_dir
    if FLAGS.char:
        nl_train = os.path.join(data_dir, "train") + ".cids%d.nl" % FLAGS.nl_vocab_size
        cm_train = os.path.join(data_dir, "train") + ".cids%d.cm" % FLAGS.cm_vocab_size
        nl_dev = os.path.join(data_dir, "dev") + ".cids%d.nl" % FLAGS.nl_vocab_size
        cm_dev = os.path.join(data_dir, "dev") + ".cids%d.cm" % FLAGS.cm_vocab_size
        nl_test = os.path.join(data_dir, "test") + ".cids%d.nl" % FLAGS.nl_vocab_size
        cm_test = os.path.join(data_dir, "test") + ".cids%d.cm" % FLAGS.cm_vocab_size
    else:
        nl_train = os.path.join(data_dir, "train") + ".ids%d.nl" % FLAGS.nl_vocab_size
        cm_train = os.path.join(data_dir, "train") + ".ids%d.cm" % FLAGS.cm_vocab_size
        nl_dev = os.path.join(data_dir, "dev") + ".ids%d.nl" % FLAGS.nl_vocab_size
        cm_dev = os.path.join(data_dir, "dev") + ".ids%d.cm" % FLAGS.cm_vocab_size
        nl_test = os.path.join(data_dir, "test") + ".ids%d.nl" % FLAGS.nl_vocab_size
        cm_test = os.path.join(data_dir, "test") + ".ids%d.cm" % FLAGS.cm_vocab_size

    train_set = data_utils.read_data(nl_train, cm_train, _buckets, FLAGS.max_train_data_size)
    dev_set = data_utils.read_data(nl_dev, cm_dev, _buckets)
    test_set = data_utils.read_data(nl_test, cm_test, _buckets)

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

    sorted_data = sorted(train_data, key=lambda x:(len(data_tools.basic_tokenizer(x[0])),
                                                   len(data_tools.bash_tokenizer(x[1]))))
    bucket_size = len(sorted_data) / num_buckets
    for i in xrange(num_buckets):
        print(int(bucket_size * (i+1)))
        mark = sorted_data[int(bucket_size * (i+1))-1]
        print(mark)
        print(len(data_tools.basic_tokenizer(mark[0])),
              len(data_tools.bash_tokenizer(mark[1])))


def main(_):
    # set GPU device
    os.environ["CUDA_VISIBLE_DEVICES"] = FLAGS.gpu

    # set GPU device
    with tf.device('/gpu:%d' % FLAGS.gpu):
        if FLAGS.manual_eval:
            manual_eval()
        elif FLAGS.eval:
            eval()
        elif FLAGS.decode:
            interactive_decode()
        elif FLAGS.bucket_selection:
            bucket_selection()
        else:
            train_set, dev_set, _ = load_data()
            train_and_eval(train_set, dev_set)


if __name__ == "__main__":
    parse_args.define_input_flags()

    tf.app.run()
