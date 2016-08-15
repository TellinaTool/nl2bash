"""Parsing input arguments"""

import tensorflow as tf

def define_input_flags():
    # task and flow
    tf.app.flags.DEFINE_integer("max_train_data_size", 0,
                                "Limit on the size of training data (0: no limit).")
    tf.app.flags.DEFINE_integer("epochs_per_checkpoint", 1,
                                "How many training steps to do per checkpoint.")
    tf.app.flags.DEFINE_integer("epochs_per_milestone", 1,
                                "How many training steps to do per dev-set evaluation")
    tf.app.flags.DEFINE_integer("num_milestones", 10,
                                "How many dev-set evaluation to be performed during training")

    tf.app.flags.DEFINE_boolean("eval", False,
                                "Set to True for quantitive evaluation.")
    tf.app.flags.DEFINE_boolean("decode", False,
                                "Set to True for interactive decoding.")
    tf.app.flags.DEFINE_boolean("bucket_selection", False,
                                "Run a bucket_selection if this is set to True.")
    tf.app.flags.DEFINE_boolean("self_test", False,
                                "Run a self-test if this is set to True.")

    # device
    tf.app.flags.DEFINE_integer("gpu", 0, "GPU device where the computation is going to be placed.")
    tf.app.flags.DEFINE_boolean("log_device_placement", False,
                                "Set to True for logging device placement.")

    # training data property
    tf.app.flags.DEFINE_integer("nl_vocab_size", 4000, "English vocabulary size.")
    tf.app.flags.DEFINE_integer("cm_vocab_size", 4000, "Bash vocabulary size.")
    tf.app.flags.DEFINE_integer("max_nl_length", 40, "maximum length of the English sentence.")
    tf.app.flags.DEFINE_integer("max_cm_length", 100, "maximum length of the command traversal sequence.")
    tf.app.flags.DEFINE_string("data_dir", "/tmp", "Data directory")
    tf.app.flags.DEFINE_string("train_dir", "/tmp", "Training directory.")

    # learning hyperparameters
    tf.app.flags.DEFINE_string("optimizer", "adam")
    tf.app.flags.DEFINE_float("learning_rate", 0.5, "Learning rate.")
    tf.app.flags.DEFINE_float("learning_rate_decay_factor", 0.99,
                              "Learning rate decays by this much.")
    tf.app.flags.DEFINE_float("input_keep_prob", 1.0,
                              "Dropout: proportion of input units to keep.")
    tf.app.flags.DEFINE_float("output_keep_prob", 1.0,
                              "Dropout: proportion of output units to keep.")
    tf.app.flags.DEFINE_float("max_gradient_norm", 5.0,
                              "Clip gradients to this norm.")
    tf.app.flags.DEFINE_integer("batch_size", 64,
                                "Batch size to use during training.")
    tf.app.flags.DEFINE_integer("num_samples", 512,
                                "Number of samples for sampled softmax.")
    tf.app.flags.DEFINE_integer("input_keep_prob", 1.0,
                                "Proportion of input to keep if dropout is used.")
    tf.app.flags.DEFINE_integer("output_keep_prob", 1.0,
                                "Proportion of output to keep if dropout is used.")
    tf.app.flags.DEFINE_integer("size", 200, "Size of each model layer.")
    tf.app.flags.DEFINE_integer("num_layers", 1, "Number of layers in the model.")
    tf.app.flags.DEFINE_boolean("attention", True, "If set, use attention decoder.")

    tf.app.flags.DEFINE_string("decoder_topology", "basic", "structure of the tree RNN")
    tf.app.flags.DEFINE_string("decoding_algorithm", "greedy", "decoding algorithm to use.")
    tf.app.flags.DEFINE_integer("beam_size", 3, "Size of beam for beam search.")
