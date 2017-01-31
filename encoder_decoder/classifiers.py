"""Basic classifiers implemented using Tensorflow."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import random
import numpy as np

import tensorflow as tf

if os.getcwd() == os.path.dirname(__file__):
    import graph_utils
else:
    from encoder_decoder import graph_utils

class BinaryLogisticRegressionModel(graph_utils.NNModel):

    def __init__ (self, hyperparams, buckets=None, forward_only=False):
        super(BinaryLogisticRegressionModel, self)\
            .__init__(hyperparams, buckets)
        self.learning_rate = tf.Variable(float(hyperparams["learning_rate"]),
                                         trainable=False)
        self.learning_rate_decay_op = self.learning_rate.assign(
            self.learning_rate * hyperparams["learning_rate_decay_factor"])

        self.define_graph()

    def define_graph(self):
        # Feeds for inputs
        X = tf.placeholder(tf.float32, [None, 2*self.dim])
        Y = tf.placeholder(tf.float32, [None, 2])

        # Model weights
        W = tf.Variable(tf.zeros([2*self.dim, 2]))
        b = tf.Variable(tf.zeros([2]))

        # Construct model
        self.output_logits = tf.nn.softmax(tf.matmul(X, W) + b)
        self.cost = tf.reduce_mean(-tf.reduce_sum(Y*tf.log(self.output_logits),
                                                  reduction_indices=1))

        # Optimizer
        opt = tf.train.AdamOptimizer(
            self.learning_rate, beta1=0.9, beta2=0.999, epsilon=1e-08)
        params = tf.trainable_variables()
        gradients = tf.gradients(self.cost, params)
        clipped_gradients, norm = tf.clip_by_global_norm(
            gradients, self.max_gradient_norm)
        self.updates.append(opt.apply_gradients(zip(clipped_gradients, params)))

        # Prediction
        self.prediction = tf.argmax(self.output_logits, 1)

        self.X = X
        self.Y = Y
        self.W = W
        self.b = b
        self.saver = tf.train.Saver(tf.all_variables())

    def get_batch(self, X, Y):
        data = zip(X, Y)
        batch_X, batch_Y = [], []

        for _ in xrange(self.batch_size):
            x, y = random.choice(data)
            batch_X.append(x)
            batch_Y.append(y)

        return tf.concat(0, batch_X), tf.concat(0, batch_Y)

    def train(self, session, X, Y):
        session.run(tf.initialize_all_tables())

        for epoch in xrange(self.num_epochs):
            avg_cost = 0
            for i in xrange(self.steps_per_epoch):
                batch_X, batch_Y = self.get_batch(X, Y)
                _, c = session.run([self.updates, self.cost], feed_dict={
                    self.X: batch_X, self.Y: batch_Y
                })
                avg_cost += c
            avg_cost /= self.steps_per_epoch
            print("Epoch:", '%04d' % (epoch+1),
                  "loss=", "{:.9f}".format(avg_cost))

    def predict(self, session, X):
        # create dummy Y variable
        Y = np.zeros([len(X)])
        output = session.run([self.prediction], feed_dict={
            self.X: X, self.Y: Y
        })
        return output[0]

    def eval(self, session, X, Y):
        with session as sess:
            correct_prediction = tf.equal(self.prediction, tf.argmax(self.Y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            print("Accuracy:", accuracy.eval({self.X: X, self.Y: Y}))
