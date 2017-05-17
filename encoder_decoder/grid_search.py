"""
Perform hyper-parameter tuning of a model using grid-search.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import random

import tensorflow as tf

from tensorflow.python.util import nest


hyperparam_range = {
    "attention_input_keep": [0.4, 0.6, 0.8, 1.0],
    "attention_output_keep": [0.4, 0.6, 0.8, 1.0],
    "universal_keep": [0.5, 0.6, 0.7, 0.8, 0.9],
    "sc_input_keep": [0.6, 0.7, 0.8],
    "sc_output_keep": [0.6, 0.7, 0.8],
    "tg_input_keep": [0.6, 0.7, 0.8],
    "tg_output_keep": [0.5, 0.6, 0.7, 0.8],
    "num_layers": [2, 4, 8],
    "num_samples": [1024, 512],
    "beta": [0.8,0.9,1.0,1.1,1.2]
}


def grid_search(train_fun, decode_fun, eval_fun, train_set, dev_set, FLAGS):
    """
    :param train_fun: Function to train the model.
    :param decode_fun: Function to decode from the trained model.
    :param eval_fun: Function to evaluate the decoding results.
    :param train_set: Training dataset.
    :param dev_set: Development dataset.
    :param FLAGS: General model hyperparameters.
    """
    FLAGS.create_fresh_params = True

    hyperparameters = FLAGS.tuning.split(',')
    num_hps = len(hyperparameters)
    hp_range = grid_search.hyperparam_range

    print("======== Grid Search ========")
    print("%d hyperparameters: " % num_hps)
    for i in xrange(num_hps):
        print("{}: {}".format(
            hyperparameters[i], hp_range[hyperparameters[i]]))
    print()

    grid = [v for v in hp_range[hyperparameters[0]]]
    for i in xrange(1, num_hps):
        grid = itertools.product(grid, hp_range[hyperparameters[i]])

    best_hp_set = [-1] * num_hps
    best_seed = -1
    best_metrics_value = 0

    model_root_dir = FLAGS.model_dir

    for row in grid:
        row = nest.flatten(row)
        for i in xrange(num_hps):
            setattr(FLAGS, hyperparameters[i], row[i])
            if hyperparameters[i] == 'universal_keep':
                setattr(FLAGS, 'sc_input_keep', row[i])
                setattr(FLAGS, 'sc_output_keep', row[i])
                setattr(FLAGS, 'tg_input_keep', row[i])
                setattr(FLAGS, 'tg_output_keep', row[i])
                setattr(FLAGS, 'attention_input_keep', row[i])
                setattr(FLAGS, 'attention_output_keep', row[i])
        FLAGS.model_dir = model_root_dir

        print("Trying parameter set: ")
        for i in xrange(num_hps):
            print("* {}: {}".format(hyperparameters[i], row[i]))

        num_trials = 5 if FLAGS.initialization else 1

        for t in xrange(num_trials):
            seed = random.getrandbits(32)
            tf.set_random_seed(seed)
            metrics = "top1_temp_ms"
            metrics_value = single_round_model_eval(
                train_fun, decode_fun, eval_fun, train_set, dev_set, metrics)
            print("Parameter set: ")
            for i in xrange(num_hps):
                print("* {}: {}".format(hyperparameters[i], row[i]))
            print("random seed: {}".format(seed))
            print("{} = {}".format(metrics, metrics_value))
            print("Best parameter set so far: ")
            for i in xrange(num_hps):
                print("* {}: {}".format(hyperparameters[i], best_hp_set[i]))
            print("Best random seed so far: {}".format(best_seed))
            print("Best {} so far = {}".format(metrics, best_metrics_value))
            if metrics_value > best_metrics_value:
                best_hp_set = row
                best_seed = seed
                best_metrics_value = metrics_value
                print("☺ New best parameter setting found")

    print()
    print("*****************************")
    print("Best parameter set: ")
    for i in xrange(num_hps):
        print("* {}: {}".format(hyperparameters[i], best_hp_set[i]))
    print("Best seed = {}".format(best_seed))
    print("Best {} = {}".format(metrics, best_metrics_value))
    print("*****************************")


def schedule_experiments():
    pass


def single_round_model_eval(train_fun, decode_fun, eval_fun,
                            train_set, dev_set, metrics):
    """
    :param train_fun: Function to train the model.
    :param decode_fun: Function to decode from the trained model.
    :param eval_fun: Function to evaluate the decoding results.
    :param train_set: Training dataset.
    :param dev_set: Development dataset.
    :param metrics: Name of the evaluation metrics to be tuned.

    :return: The metrics being tuned.
    """
    train_fun(train_set, dev_set, construct_model_dir=True)

    tf.reset_default_graph()
    model_sig = decode_fun(dev_set, construct_model_dir=False, verbose=False)
    M = eval_fun(dev_set, model_sig, verbose=False)

    tf.reset_default_graph()
    return M[metrics]