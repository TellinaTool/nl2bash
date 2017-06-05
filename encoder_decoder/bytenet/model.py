"""
ByteNet: Neural Machine Translation in Linear Time
(cf. https://arxiv.org/abs/1610.10099)

Adapted from
curl -LO 'https://github.com/paarthneekhara/byteNet-tensorflow/blob/master/ByteNet/model.py'
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import ops

from encoder_decoder import graph_utils


class ByteNet(graph_utils.NNModel):
	def __init__(self, options):
		'''
		options
		n_source_quant : quantization channels of source text
		n_target_quant : quantization channels of target text
		residual_channels : number of channels in internal blocks
		batch_size : Batch Size
		sample_size : Text Sample Length
		encoder_filter_width : Encoder Filter Width
		decoder_filter_width : Decoder Filter Width
		encoder_dilations : Dilation Factor for decoder layers (list)
		decoder_dilations : Dilation Factor for decoder layers (list)
		'''
		self.options = options
		
		self.w_source_embedding = tf.get_variable('w_source_embedding', 
			[options['n_source_quant'], 2*options['residual_channels']],
			initializer=tf.truncated_normal_initializer(stddev=0.02))

		# TO BE CONCATENATED WITH THE ENCODER EMBEDDING
		self.w_target_embedding = tf.get_variable('w_target_embedding', 
			[options['n_target_quant'], options['residual_channels']],
			initializer=tf.truncated_normal_initializer(stddev=0.02))


		if 'source_mask_chars' in options:
			# FOR EMBEDDING ONLY THE INPUT SENTENCE BEFORE THE PADDING
			# THE OUTPUT NETWORK WHOULD BE CONDITIONED ONLY UPTO INPUT LENGTH
			# ALSO LOSS NEEDS TO BE CALCULATED UPTO TARGET SENTENCE
			input_sentence_mask = np.ones( 
				(options['n_source_quant'], 2 * options['residual_channels']), dtype = 'float32')


			input_sentence_mask[options['source_mask_chars'], :] = np.zeros(
				(1,2 * options['residual_channels'] ), dtype = 'float32')

			output_sentence_mask = np.ones( 
				(options['n_target_quant'], 1), dtype = 'float32')
			
			output_sentence_mask[options['target_mask_chars'], :] = np.zeros(
				(1,1), dtype = 'float32')

			self.input_mask = tf.constant(input_sentence_mask)
			self.output_mask = tf.constant(output_sentence_mask)

	def build_translation_model(self, sample_size):
		self.options['sample_size'] = sample_size
		options = self.options
		
		source_sentence = tf.placeholder('int32', [options['batch_size'], options['sample_size']], name = 'source_sentence')
		

		target_sentence = tf.placeholder('int32', [options['batch_size'], options['sample_size']+1], name = 'target_sentence')
		
		self.source_masked = tf.nn.embedding_lookup(self.input_mask, source_sentence, name = "source_masked")
		self.source_masked_d = tf.slice(self.source_masked, [0,0,0], 
			[options['batch_size'], options['sample_size'], options['residual_channels']], name = 'source_masked_d')


		source_embedding = tf.nn.embedding_lookup(self.w_source_embedding, source_sentence)
		# MASK EMBEDDING BEYOND SOURCE LENGTH
		source_embedding = tf.mul(source_embedding, self.source_masked, name = "source_embedding")
		

		# Input to the decoder
		target_sentence1 = tf.slice(target_sentence, 
			[0,0], 
			[options['batch_size'], options['sample_size']], 
			name = 'target_sentence1')
		target1_embedding = tf.nn.embedding_lookup(self.w_target_embedding, target_sentence1, name = "target1_embedding")

		# Output of the decoder
		target_sentence2 = tf.slice(target_sentence, 
			[0,1], 
			[options['batch_size'], options['sample_size']], 
			name = 'target_sentence2')

		# FOR MASKING LOSS BEYOND THE TARGET LENGTH
		self.target_masked = tf.nn.embedding_lookup(self.output_mask, target_sentence2, name = "target_masked")
		

		encoder_output = self.encoder(source_embedding)
		decoder_output = self.decoder(target1_embedding, encoder_output)

		loss = self.loss(decoder_output, target_sentence2)

		tf.scalar_summary('LOSS', loss)

		flat_logits = tf.reshape( decoder_output, [-1, options['n_target_quant']])
		prediction = tf.argmax(flat_logits, 1)
		
		variables = tf.trainable_variables()

		merged_summary = tf.merge_all_summaries()
		
		# first_column_decoder = t
		tensors = {
			'source_sentence' : source_sentence,
			'target_sentence' : target_sentence,
			'loss' : loss,
			'prediction' : prediction,
			'variables' : variables,
			'merged_summary' : merged_summary,
			'source_embedding' : source_embedding,
			'encoder_output' : encoder_output,
			'target_masked' : self.target_masked,
			'source_masked' : self.source_masked,
			'source_gradient' : tf.gradients(loss, [source_embedding]),
			'target_gradient' : tf.gradients(loss, [target1_embedding]),
			'probs' : tf.nn.softmax(flat_logits)
		}

		return tensors


	def build_prediction_model(self):
		options = self.options
		sentence = tf.placeholder('int32', [options['batch_size'], options['sample_size']], name = 'sentence')
		
		source_sentence = tf.slice(sentence, 
			[0,0], 
			[options['batch_size'], options['sample_size'] - 1], 
			name = 'source_sentence')
		
		target_sentence = tf.slice(sentence, 
			[0,1], 
			[options['batch_size'], options['sample_size'] - 1], 
			name = 'target_sentence')
		
		source_embedding = tf.nn.embedding_lookup(self.w_source_embedding, source_sentence, name = "source_embedding")
		decoder_output = self.decoder(source_embedding)
		loss = self.loss(decoder_output, target_sentence)
		
		tf.scalar_summary('LOSS', loss)

		flat_logits = tf.reshape( decoder_output, [-1, options['n_target_quant']])
		prediction = tf.argmax(flat_logits, 1)
		
		variables = tf.trainable_variables()
		
		tensors = {
			'sentence' : sentence,
			'loss' : loss,
			'prediction' : prediction,
			'variables' : variables
		}


		return tensors

	def build_translator(self, sample_size, reuse = False):
		if reuse:
			tf.get_variable_scope().reuse_variables()

		self.options['sample_size'] = sample_size
		options = self.options
		source_sentence = tf.placeholder('int32', [1, sample_size], name = 'source_sentence')
		target_sentence = tf.placeholder('int32', [1, sample_size], name = 'target_sentence')

		self.source_masked = tf.nn.embedding_lookup(self.input_mask, source_sentence, name = "source_masked")
		self.source_masked_d = tf.slice(self.source_masked, [0,0,0], 
			[options['batch_size'], options['sample_size'], options['residual_channels']],
			name = 'source_masked_d')

		source_embedding = tf.nn.embedding_lookup(self.w_source_embedding, source_sentence)
		source_embedding = tf.mul(source_embedding, self.source_masked, name = "source_embedding")

		target1_embedding = tf.nn.embedding_lookup(self.w_target_embedding, target_sentence, name = "target1_embedding")

		encoder_output = self.encoder(source_embedding)
		decoder_output = self.decoder(target1_embedding, encoder_output)

		flat_logits = tf.reshape( decoder_output, [-1, options['n_target_quant']])
		prediction = tf.argmax(flat_logits, 1)
		probs = tf.nn.softmax(flat_logits)
		
		tensors = {
			'source_sentence' : source_sentence,
			'target_sentence' : target_sentence,
			'prediction' : prediction,
			'encoder_output': encoder_output,
			'probs' : probs
		}

		return tensors

	def build_generator(self, sample_size, reuse = False):
		if reuse:
			tf.get_variable_scope().reuse_variables()
		options = self.options
		source_sentence = tf.placeholder('int32', [1, sample_size], name = 'sentence')
		source_embedding = tf.nn.embedding_lookup(self.w_source_embedding, source_sentence, name = "source_embedding")
		decoder_output = self.decoder(source_embedding)
		flat_logits = tf.reshape( decoder_output, [-1, options['n_target_quant']])


		prediction = tf.argmax(flat_logits, 1)
		probs = tf.nn.softmax(flat_logits)
		tensors = {
			'source_sentence' : source_sentence,
			'prediction' : prediction,
			'probs' : probs
		}

		return tensors

	def loss(self, decoder_output, target_sentence):
		options = self.options
		target_one_hot = tf.one_hot(target_sentence, 
			depth = options['n_target_quant'],
			dtype = tf.float32)
		

		flat_logits = tf.reshape( decoder_output, [-1, options['n_target_quant']])
		flat_targets = tf.reshape( target_one_hot, [-1, options['n_target_quant']])
		loss = tf.nn.softmax_cross_entropy_with_logits(flat_logits, flat_targets, name='decoder_cross_entropy_loss')

		if 'target_mask_chars' in options:
			# MASK LOSS BEYOND EOL IN TARGET
			target_masked = tf.reshape( self.target_masked, [-1])
			loss = tf.mul( loss, target_masked, name = 'masked_loss')
			loss = tf.div( tf.reduce_sum(loss),tf.reduce_sum(target_masked), name = "Reduced_mean_loss")
		else:
			loss = tf.reduce_mean(loss, name = "Reduced_mean_loss")

		return loss


	def decode_layer(self, input_, dilation, layer_no):
		options = self.options
		relu1 = tf.nn.relu(input_, name = 'dec_relu1_layer{}'.format(layer_no))
		conv1 = ops.conv1d(relu1, options['residual_channels'], name = 'dec_conv1d_1_layer{}'.format(layer_no))
		

		relu2 = tf.nn.relu(conv1, name = 'enc_relu2_layer{}'.format(layer_no))
		dilated_conv = ops.dilated_conv1d(relu2, options['residual_channels'], 
			dilation, options['decoder_filter_width'],
			causal = True, 
			name = "dec_dilated_conv_laye{}".format(layer_no)
			)
		
		relu3 = tf.nn.relu(dilated_conv, name = 'dec_relu3_layer{}'.format(layer_no))
		conv2 = ops.conv1d(relu3, 2 * options['residual_channels'], name = 'dec_conv1d_2_layer{}'.format(layer_no))
		
		return input_ + conv2

	def decoder(self, input_, encoder_embedding = None):
		options = self.options
		curr_input = input_
		if encoder_embedding != None:
			# CONDITION WITH ENCODER EMBEDDING FOR THE TRANSLATION MODEL
			curr_input = tf.concat(2, [input_, encoder_embedding])
			print("Decoder Input", curr_input)
			

		for layer_no, dilation in enumerate(options['decoder_dilations']):
			layer_output = self.decode_layer(curr_input, dilation, layer_no)
			curr_input = layer_output


		processed_output = ops.conv1d(tf.nn.relu(layer_output), 
			options['n_target_quant'], 
			name = 'decoder_post_processing')

		return processed_output


	def encode_layer(self, input_, dilation, layer_no, last_layer = False):
		options = self.options
		relu1 = tf.nn.relu(input_, name = 'enc_relu1_layer{}'.format(layer_no))
		conv1 = ops.conv1d(relu1, options['residual_channels'], name = 'enc_conv1d_1_layer{}'.format(layer_no))
		conv1 = tf.mul(conv1, self.source_masked_d)
		relu2 = tf.nn.relu(conv1, name = 'enc_relu2_layer{}'.format(layer_no))
		dilated_conv = ops.dilated_conv1d(relu2, options['residual_channels'], 
			dilation, options['encoder_filter_width'],
			causal = False, 
			name = "enc_dilated_conv_layer{}".format(layer_no)
			)
		dilated_conv = tf.mul(dilated_conv, self.source_masked_d)
		relu3 = tf.nn.relu(dilated_conv, name = 'enc_relu3_layer{}'.format(layer_no))
		conv2 = ops.conv1d(relu3, 2 * options['residual_channels'], name = 'enc_conv1d_2_layer{}'.format(layer_no))
		return input_ + conv2
		
	def encoder(self, input_):
		options = self.options
		curr_input = input_
		for layer_no, dilation in enumerate(self.options['encoder_dilations']):
			layer_output = self.encode_layer(curr_input, dilation, layer_no)

			# ENCODE ONLY TILL THE INPUT LENGTH, conditioning should be 0 beyond that
			layer_output = tf.mul(layer_output, self.source_masked, name = 'layer_{}_output'.format(layer_no))

			curr_input = layer_output
		
		# TO BE CONCATENATED WITH TARGET EMBEDDING
		processed_output = tf.nn.relu( ops.conv1d(tf.nn.relu(layer_output), 
			options['residual_channels'], 
			name = 'encoder_post_processing') )

		processed_output = tf.mul(processed_output, self.source_masked_d, name = 'encoder_processed')

		return processed_output
