"""Basic classifiers implemented using Tensorflow."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import random
import numpy as np

import tensorflow as tf

from encoder_decoder import graph_utils


class KNearestNeighborModel():
    #TODO: change the numpy kNN model implementation to Tensorflow
    def __init__(self, k, train_X, train_Y):
        """
        :member k: number of neighboring examples to use
        :member train_X: [size, dim] training feature matrix
        :member train_Y: [size, label_dim] training label matrix
        """
        self.k = k
        self.train_X = train_X
        self.train_Y = train_Y

    def predict(self, X):
        """
        :param X: [size, dim]
        """
        # [size, size]
        sim_scores = np.matmul(X, self.train_X.T)
        # [size, self.k]
        nn = np.argpartition(sim_scores, -self.k, axis=1)[:, -self.k:]
        # [size, self.k]
        nn_weights = np.partition(sim_scores, -self.k, axis=1)[:, -self.k:]

        nn_prediction = np.sum(
            np.expand_dims(nn_weights, 2) * self.train_Y[nn], axis=1) 
        return nn_prediction

    def eval(self, X, Y, verbose=True):
        nn_prediction = self.predict(X)
        # compute accuracy
        threshold = 0.5
        num_total = 0.0
        num_correct = 0.0
        for i in xrange(len(nn_prediction)):
            if Y[i][0] == 1 and nn_prediction[i][0] >= threshold:
                num_correct += 1
            if Y[i][0] == 0 and nn_prediction[i][0] < threshold:
                num_correct += 1
            if verbose:
                print(nn_prediction[i][0], Y[i][0])
            num_total += 1
        print("Accuracy: ", num_correct / num_total)


class BinaryLogisticRegressionModel(graph_utils.NNModel):
    # TODO: create separate graphs for the forward and backward passes of the
    # logistic regression model
    def __init__ (self, hyperparams, buckets=None):
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
        Wh = tf.Variable(tf.zeros([2*self.dim, 2*self.dim]))
        W = tf.Variable(tf.zeros([2*self.dim, 2]))    
        b = tf.Variable(tf.zeros([2]))

        # Construct model
        h = tf.nn.sigmoid(tf.matmul(X, Wh))
        self.output_logits = tf.nn.softmax(tf.matmul(h, W) + b)
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
            logits=self.output_logits, labels=Y))

        # Optimizer
        opt = tf.train.AdamOptimizer(
            self.learning_rate, beta1=0.9, beta2=0.999, epsilon=1e-08)
        params = tf.trainable_variables()
        gradients = tf.gradients(self.cost, params)
        clipped_gradients, norm = tf.clip_by_global_norm(
            gradients, self.max_gradient_norm)
        self.updates = opt.apply_gradients(zip(clipped_gradients, params))

        # Prediction
        self.prediction = tf.argmax(self.output_logits, 1)

        self.X = X
        self.Y = Y
        self.W = W
        self.b = b
        self.saver = tf.train.Saver(tf.global_variables())

    def get_batch(self, X, Y):
        data = zip(X, Y)
        batch_X, batch_Y = [], []

        for _ in xrange(self.batch_size):
            x, y = random.choice(data)
            batch_X.append(x)
            batch_Y.append(np.expand_dims(y, axis=0))

        return np.concatenate(batch_X, axis=0), \
               np.concatenate(batch_Y, axis=0)

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
        batch_X = np.concatenate(X, axis=0)
        dummy_Y = np.zeros([[len(X), 2]])
        output = session.run([self.prediction], feed_dict={
            self.X: batch_X, self.Y: dummy_Y
        })
        return output[0]

    def eval(self, session, X, Y):
        batch_X = np.concatenate(X, axis=0)
        batch_Y = np.concatenate([np.expand_dims(y, axis=0) for y in Y], axis=0)
        print(batch_X.shape)
        correct_prediction = tf.equal(self.prediction, tf.argmax(self.Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        acc = session.run([accuracy], feed_dict={
            self.X: batch_X, self.Y: batch_Y
        })
        print("Accuracy: {}".format(acc))
