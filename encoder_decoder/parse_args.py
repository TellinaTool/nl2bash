'''Parsing input arguments'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tensorflow as tf

def define_input_flags():
    # translation experiments
    tf.compat.v1.flags.DEFINE_integer('max_train_data_size', 0,
                                'Limit on the size of training data (0: no limit).')
    tf.compat.v1.flags.DEFINE_integer('steps_per_epoch', 200,
                                'How many training steps to do per checkpoint.')
    tf.compat.v1.flags.DEFINE_integer('num_epochs', 20,
                                'Number of training epochs')
    tf.compat.v1.flags.DEFINE_integer('epochs_per_checkpoint', 1,
                                'How many training steps to do per checkpoint.')

    tf.compat.v1.flags.DEFINE_boolean('explain', False,
                                'Set to True to translate code to natural language.')

    tf.compat.v1.flags.DEFINE_boolean('cross_valid', False,
                                'Set to True for cross validation.')
    tf.compat.v1.flags.DEFINE_integer('num_folds', 5,
                                'Number of folds in cross validation.')

    tf.compat.v1.flags.DEFINE_boolean('grid_search', False,
                                'Set to True for grid search.')
    tf.compat.v1.flags.DEFINE_boolean('schedule_experiments', False,
                                'Set to True for running multiple experiments with different pre-specified '
                                'hyperparameters.')
    tf.compat.v1.flags.DEFINE_string('tuning', 'initialization,output_keep_prob,num_samples',
                               'List of hyperparamters to tune.')
    tf.compat.v1.flags.DEFINE_boolean('initialization', False,
                                'Set to try multiple random intialization and select the best one.')

    tf.compat.v1.flags.DEFINE_boolean('process_data', False,
                                'Set to True for data preprocessing.')
    tf.compat.v1.flags.DEFINE_boolean('decode', False,
                                'Set to True for decoding.')
    tf.compat.v1.flags.DEFINE_boolean('test', False,
                                'Set to True to decode and evaluate on the test set.')
    tf.compat.v1.flags.DEFINE_boolean('eval', False,
                                'Set to True to perform automatic evaluation.')
    tf.compat.v1.flags.DEFINE_boolean('manual_eval', False,
                                'Set to True to perform manual evaluation in the commandline interface.')
    tf.compat.v1.flags.DEFINE_boolean('demo', False,
                                'Set to True for interactive demo.')

    tf.compat.v1.flags.DEFINE_boolean('gen_error_analysis_sheet', False,
                                'Set to True to generate error analysis spreadsheet.')
    tf.compat.v1.flags.DEFINE_boolean('gen_manual_evaluation_sheet', False,
                                'Set to True to tabulate the output of specified baseline models in .csv files '
                                'for manual annotation.')
    tf.compat.v1.flags.DEFINE_boolean('gen_manual_evaluation_sheet_single_model', False,
                                'Set to True to tabulate the output of a specific model in .csv file '
                                'for manual annotation.')
    tf.compat.v1.flags.DEFINE_boolean('gen_manual_evaluation_table', False,
                                'Set to True to tabulate manual evaluation results of specified baseline systems '
                                'in standard output.'
                                'Opens the commandline interface when the model output contains unseen command.')
    tf.compat.v1.flags.DEFINE_boolean('gen_auto_evaluation_table', False,
                                'Set to True to tabulate the automatic evaluation results '
                                'for specified baseline systems in standard output.')

    # device
    tf.compat.v1.flags.DEFINE_string('gpu', '0', 'GPU device where the computation is going to be placed.')
    tf.compat.v1.flags.DEFINE_boolean('log_device_placement', False, 'Set to True for logging device placement.')

    # data hyperparameters
    tf.compat.v1.flags.DEFINE_string('dataset', 'bash', 'select dataset to use.')
    tf.compat.v1.flags.DEFINE_string('channel', '', 'translation feature channel.')
    tf.compat.v1.flags.DEFINE_string('data_dir', os.path.join(os.path.dirname(__file__), 'data'), 'Data directory')
    tf.compat.v1.flags.DEFINE_string('model_dir', os.path.join(os.path.dirname(__file__), 'model'), 'Model directory')
    tf.compat.v1.flags.DEFINE_string('prediction_file', None, 'path to where the decoding output is stored')
    tf.compat.v1.flags.DEFINE_integer('sample_size', 200, 'Training data sample size')
    tf.compat.v1.flags.DEFINE_boolean('normalized', False, 'Set to True for learning with normalized command.')
    tf.compat.v1.flags.DEFINE_boolean('canonical', False,
                                'Set to True for learning with normalized command with canonicalized option order.')
    tf.compat.v1.flags.DEFINE_integer('max_sc_length', 100, 'Maximum source sequence length.')
    tf.compat.v1.flags.DEFINE_integer('max_tg_length', 100, 'Maximum target sequence length.')
    tf.compat.v1.flags.DEFINE_integer('sc_vocab_size', 1000, 'Source vocabulary size.')
    tf.compat.v1.flags.DEFINE_integer('tg_vocab_size', 1000, 'Target vocabulary size.')
    tf.compat.v1.flags.DEFINE_integer('max_sc_token_size', 100, 'Maximum source token size.')
    tf.compat.v1.flags.DEFINE_integer('max_tg_token_size', 100, 'Maximum target token size.')
    tf.compat.v1.flags.DEFINE_integer('min_vocab_frequency', 1,
                                'Minimum frequency of token in the dataset that are not considered UNK.')
    tf.compat.v1.flags.DEFINE_integer('num_buckets', 3, 'Number of buckets to use.')

    # training hyperparameters
    tf.compat.v1.flags.DEFINE_string('model_root_dir', 'model', 'Directory to save trained models.')
    tf.compat.v1.flags.DEFINE_boolean('create_fresh_params', False,
                                'Set to force remove previously trained models.')
    tf.compat.v1.flags.DEFINE_string('rnn_cell', 'gru', 'Type of RNN cell to use.')
    tf.compat.v1.flags.DEFINE_string('optimizer', 'adam',
                               'Type of numeric optimization algorithm to use.')
    tf.compat.v1.flags.DEFINE_float('learning_rate', 0.001, 'Learning rate.')
    tf.compat.v1.flags.DEFINE_float('learning_rate_decay_factor', 0.99,
                              'Learning rate decays by this much.')
    tf.compat.v1.flags.DEFINE_float('adam_epsilon', 1e-08, 'Epsilon parameter in the Adam Optimizer.')
    tf.compat.v1.flags.DEFINE_float('max_gradient_norm', 5.0,
                              'Clip gradients to this norm.')
    tf.compat.v1.flags.DEFINE_integer('batch_size', 128,
                                'Batch size to use during training.')
    tf.compat.v1.flags.DEFINE_integer('num_layers', 1,
                                'Number of layers in the encoder-decoder.')
    tf.compat.v1.flags.DEFINE_integer('num_samples', -1,
                                'Number of samples for sampled softmax.')
    tf.compat.v1.flags.DEFINE_integer('seed', -1, 'Random seed for graph initialization.')

    tf.compat.v1.flags.DEFINE_boolean('variational_recurrent_dropout', False, 'Set to use variational ' +
                                'recurrent dropout on the RNN cells.')
    tf.compat.v1.flags.DEFINE_float('universal_keep', -1, 'Use the rate for all ' +
                              'dropout layers if set to a number between 0 and 1.')
    tf.compat.v1.flags.DEFINE_float('sc_input_keep', .5, 'Proportion of source input to keep if dropout is used.')
    tf.compat.v1.flags.DEFINE_float('sc_output_keep', .5, 'Proportion of source output to keep if dropout is used.')
    tf.compat.v1.flags.DEFINE_float('tg_input_keep', .5, 'Proportion of target input to keep if dropout is used.')
    tf.compat.v1.flags.DEFINE_float('tg_output_keep', .5, 'Proportion of target output to keep if dropout is used.')

    tf.compat.v1.flags.DEFINE_boolean('recurrent_batch_normalization', False,
                                'Set to use recurrent batch normalization.')
    tf.compat.v1.flags.DEFINE_float('gamma_c', .1, 'Scale of cell state normalization.')
    tf.compat.v1.flags.DEFINE_float('beta_c', .1, 'Offset of cell state normalization.')
    tf.compat.v1.flags.DEFINE_float('gamma_h', .1, 'Scale of hidden state normalization.')
    tf.compat.v1.flags.DEFINE_float('beta_h', .1, 'Offset of hidden state normalization.')
    tf.compat.v1.flags.DEFINE_float('gamma_x', .1, 'Scale of input state normalization.')
    tf.compat.v1.flags.DEFINE_float('beta_x', .1, 'Offset of input state normalization.')

    tf.compat.v1.flags.DEFINE_string('training_algorithm', 'standard', 'training algorithm to use.')
    tf.compat.v1.flags.DEFINE_string('pretrained_model_subdir', '', 'signature of pretrained model.')

    tf.compat.v1.flags.DEFINE_string('encoder_topology', 'rnn', 'structure of the encoder.')
    tf.compat.v1.flags.DEFINE_string('decoder_topology', 'rnn', 'structure of the decoder.')

    tf.compat.v1.flags.DEFINE_boolean('tg_token_use_attention', False, 'If set, use attention for token decoder.')
    tf.compat.v1.flags.DEFINE_boolean('tg_char_use_attention', False, 'If set, use attention for char decoder.')
    tf.compat.v1.flags.DEFINE_string('tg_token_attn_fun', 'inner_product',
                                'Function used for token-level attention module.')
    tf.compat.v1.flags.DEFINE_string('tg_char_attn_fun', 'inner_product',
                               'Function used for char-level attention module.')
    tf.compat.v1.flags.DEFINE_float('beta', 0, 'Attention regularization weight.')
    tf.compat.v1.flags.DEFINE_float('attention_input_keep', .5,
                              'Proportion of attention input state to keep if dropout is used.')
    tf.compat.v1.flags.DEFINE_float('attention_output_keep', .5,
                              'Proportion of attention hidden state to keep if dropout is used.')

    tf.compat.v1.flags.DEFINE_float('margin', 1.0, 'margin for margin-based loss function')

    # decoding hyperparameters
    tf.compat.v1.flags.DEFINE_string('token_decoding_algorithm', 'beam_search',
                               'decoding algorithm used for token generation.')
    tf.compat.v1.flags.DEFINE_string('char_decoding_algorithm', 'greedy',
                               'decoding algorithm used for character generation.')
    tf.compat.v1.flags.DEFINE_integer('beam_size', -1, 'Size of beam for beam search.')
    tf.compat.v1.flags.DEFINE_integer('beam_order', -1, 'Order for beam search.')
    tf.compat.v1.flags.DEFINE_float('alpha', 0.5, 'Beam search length normalization parameter.')
    tf.compat.v1.flags.DEFINE_integer('top_k', 5, 'Top-k highest-scoring structures to output.')
    tf.compat.v1.flags.DEFINE_boolean('grammatical_only', True, 'If set, output only grammatical predictions.')

    tf.compat.v1.flags.DEFINE_boolean('fill_argument_slots', False, 'If set, fill the argument slots in '
                                'the output command with filler constants extracted from the natural language input.')

    # slot-filling experiments
    tf.compat.v1.flags.DEFINE_integer('num_nn_slot_filling', 1, 'Number of nearest neighbors to use in '
                                'the nearest neighbor slot-filling classifier.')
    tf.compat.v1.flags.DEFINE_boolean('gen_slot_filling_training_data', False,
                                'Set to True to generate feature vectors for slot-filling training.')
    tf.compat.v1.flags.DEFINE_boolean('eval_slot_filling', False,
                                'Set to True for evaluation of the slot-filling classifier.')
    tf.compat.v1.flags.DEFINE_boolean('eval_local_slot_filling', False,
                                'Set to True for raw evaluation of the slot-filling classifier.')


    # channel network hyperparameters
    tf.compat.v1.flags.DEFINE_boolean('sc_token', True,
                                'Set to True to turn on the token channel in the encoder. On by default.')
    tf.compat.v1.flags.DEFINE_integer('sc_token_embedding_size', 1000, 'source word embedding size.')
    tf.compat.v1.flags.DEFINE_integer('sc_token_dim', 300, 'Basic token embedding dimensions.')
    tf.compat.v1.flags.DEFINE_boolean('sc_char', False,
                                'Set to True to turn on the character channel in the encoder. Off by default.')
    tf.compat.v1.flags.DEFINE_integer('sc_char_dim', 300, 'Dimension of each character embeddings.')
    tf.compat.v1.flags.DEFINE_string('sc_char_composition', 'rnn', 'Specify the character to token composition function.')
    tf.compat.v1.flags.DEFINE_string('sc_char_rnn_cell', 'gru', 'Type of RNN cell to use for the character model.')
    tf.compat.v1.flags.DEFINE_integer('sc_char_rnn_num_layers', 1,
                                'Number of layers in the RNN cell used for the character model.')

    tf.compat.v1.flags.DEFINE_boolean('tg_token', True,
                                'Set to True to turn on the token channel in the decoder. On by default.')
    tf.compat.v1.flags.DEFINE_integer('tg_token_embedding_size', 1000, 'target word embedding size.')
    tf.compat.v1.flags.DEFINE_boolean('tg_char', False,
                                'Set to True to turn on character RNN extention module in the decoder.')
    tf.compat.v1.flags.DEFINE_string('tg_char_composition', 'rnn',
                               'Specify the model configuration used for character generation in the target.')
    tf.compat.v1.flags.DEFINE_string('tg_char_rnn_cell', 'gru', 'Type of RNN cell to use for the character model.')
    tf.compat.v1.flags.DEFINE_integer('tg_char_rnn_num_layers', 1,
                                'Number of layers in the RNN cell used for the character model.')
    tf.compat.v1.flags.DEFINE_float('tg_char_rnn_input_keep', .5,
                                'Proportion of character target input to keep if dropout is used.')
    tf.compat.v1.flags.DEFINE_float('tg_char_rnn_output_keep', .5,
                                'Proportion of character target output to keep if dropout is used.')
    tf.compat.v1.flags.DEFINE_float('gamma', 5, 'Define the weight of the character channel loss.')

    # hyperparameters for copying UNKs
    tf.compat.v1.flags.DEFINE_boolean('use_copy', False, 'If set, use copying mechanism.')
    tf.compat.v1.flags.DEFINE_string('copy_fun', 'implicit',
                                'Specifying the type of copying functions to use.')
    tf.compat.v1.flags.DEFINE_float('chi', 1, 'Copy loss weight.')

    # debugging options
    tf.compat.v1.flags.DEFINE_boolean('force_reading_input', False, 'If set, read ground truth decoder inputs for decoding.')

    # Generate tables and plots charts for paper.
    tf.compat.v1.flags.DEFINE_boolean('tabulate_example_predictions', False,
                                'Set to True to print example predictions with Latex formattings')