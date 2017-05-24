"""
Meta-experiments which involves training and testing the model with multiple
hyperparamter settings.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import random
import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

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
    Perform hyperparameter tuning of a model using grid-search.

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
    hp_range = hyperparam_range

    print("======== Grid Search ========")
    print("%d hyperparameter(s): " % num_hps)
    for i in xrange(num_hps):
        print("{}: {}".format(
            hyperparameters[i], hp_range[hyperparameters[i]]))
    print()

    param_grid = [v for v in hp_range[hyperparameters[0]]]
    for i in xrange(1, num_hps):
        param_grid = itertools.product(param_grid, hp_range[hyperparameters[i]])

    best_hp_set = [-1] * num_hps
    best_seed = -1
    best_metrics_value = 0

    for row in param_grid:
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


def schedule_experiments(train_fun, decode_fun, eval_fun, train_set, dev_set,
                         hyperparam_sets, FLAGS):
    """
    Run multiple experiments with different sets of hyperparameters.
    """

    print("===== Scheduled Experiments =====")
    for hyperparam_set in hyperparam_sets:
        for hp in hyperparam_set:
            setattr(FLAGS, hp, hyperparam_set[hp])
            if hp == 'universal_keep':
                setattr(FLAGS, 'sc_input_keep', hyperparam_set[hp])
                setattr(FLAGS, 'sc_output_keep', hyperparam_set[hp])
                setattr(FLAGS, 'tg_input_keep', hyperparam_set[hp])
                setattr(FLAGS, 'tg_output_keep', hyperparam_set[hp])
                setattr(FLAGS, 'attention_input_keep', hyperparam_set[hp])
                setattr(FLAGS, 'attention_output_keep', hyperparam_set[hp])

        print("Trying parameter set: ")
        for hp in hyperparam_set:
            print("* {}: {}".format(hp, hyperparam_set[hp]))
            metrics = "top1_temp_ms"

        metrics_value = single_round_model_eval(
            train_fun, decode_fun, eval_fun, train_set, dev_set, metrics)
        print("Parameter set: ")
        for hp in hyperparam_set:
            print("* {}: {}".format(hp, hyperparam_set[hp]))
        print("{} = {}".format(metrics, metrics_value))


def single_round_model_eval(train_fun, decode_fun, eval_fun,
                            train_set, dev_set, metrics):
    """
    Train the model with a certain set of hyperparameters and evaluate on the
    development set.

    :param train_fun: Function to train the model.
    :param decode_fun: Function to decode from the trained model.
    :param eval_fun: Function to evaluate the decoding results.
    :param train_set: Training dataset.
    :param dev_set: Development dataset.
    :param metrics: Name of the evaluation metrics to be tuned.

    :return: The metrics being tuned.
    """
    tf.reset_default_graph()
    train_fun(train_set, dev_set)

    tf.reset_default_graph()
    decode_sig = decode_fun(dev_set, verbose=False)

    M = eval_fun(dev_set, decode_sig, verbose=False)

    return M[metrics]
