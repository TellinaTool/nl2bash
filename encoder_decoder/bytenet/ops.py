"""
ByteNet: Neural Machine Translation in Linear Time
(cf. https://arxiv.org/abs/1610.10099)

Adapted from
curl -LO 'https://github.com/paarthneekhara/byteNet-tensorflow/blob/master/ByteNet/ops.py'
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf


def time_to_batch(value, dilation, name=None):
	# FOR DILATED CONVOLUTION, code adpated from tensorflow-wavenet
	with tf.name_scope('time_to_batch'):
		shape = value.get_shape()
		shape = [int(s) for s in shape]
		pad_elements = dilation - 1 - (int(shape[1]) + dilation - 1) % dilation
		padded = tf.pad(value, [[0, 0], [0, pad_elements], [0, 0]])
		reshaped = tf.reshape(padded, [-1, dilation, shape[2]])
		transposed = tf.transpose(reshaped, perm=[1, 0, 2])
		return tf.reshape(transposed, [shape[0] * dilation, -1, shape[2]])

def batch_to_time(value, dilation, name=None):
	with tf.name_scope('batch_to_time'):
		shape = value.get_shape()
		shape = [int(s) for s in shape]
		prepared = tf.reshape(value, [dilation, -1, shape[2]])
		transposed = tf.transpose(prepared, perm=[1, 0, 2])
		return tf.reshape(transposed, [(shape[0]/dilation), -1, shape[2]])

def conv1d(input_, output_channels, 
	filter_width = 1, stride = 1, stddev=0.02,
	name = 'conv1d'):
	with tf.variable_scope(name):
		input_shape = input_.get_shape()
		input_channels = input_shape[-1]
		filter_ = tf.get_variable('w', [filter_width, input_channels, output_channels],
			initializer=tf.truncated_normal_initializer(stddev=stddev))
		conv = tf.nn.conv1d(input_, filter_, stride = stride, padding = 'SAME')
		biases = tf.get_variable('biases', [output_channels], initializer=tf.constant_initializer(0.0))
		conv = tf.reshape(tf.nn.bias_add(conv, biases), conv.get_shape())
		return conv

def dilated_conv1d(input_, output_channels, dilation, 
	filter_width = 1, causal = False, name = 'dilated_conv'):
	
	
	if causal:
		# padding for masked convolution
		padding = [[0, 0], [(filter_width - 1) * dilation, 0], [0, 0]]
		padded = tf.pad(input_, padding)
	else:
		
		padding = [[0, 0], [(filter_width - 1) * dilation/2, (filter_width - 1) * dilation/2], [0, 0]]
		padded = tf.pad(input_, padding)
	
	if dilation > 1:
		transformed = time_to_batch(padded, dilation)
		conv = conv1d(transformed, output_channels, filter_width, name = name)
		restored = batch_to_time(conv, dilation)
	else:
		restored = conv1d(padded, output_channels, filter_width, name = name)

	
	result = tf.slice(restored,[0, 0, 0],[-1, int(input_.get_shape()[1]), -1])
	
	return result




