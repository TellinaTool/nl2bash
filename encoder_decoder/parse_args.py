"""Parsing input arguments"""

import os
import tensorflow as tf

def define_input_flags():
    # task and flow
    tf.app.flags.DEFINE_integer("max_train_data_size", 0,
                                "Limit on the size of training data (0: no limit).")
    tf.app.flags.DEFINE_integer("steps_per_epoch", 200,
                                "How many training steps to do per checkpoint.")
    tf.app.flags.DEFINE_integer("num_epochs", 20,
                                "Number of training epochs")
    tf.app.flags.DEFINE_integer("epochs_per_checkpoint", 1,
                                "How many training steps to do per checkpoint.")

    tf.app.flags.DEFINE_boolean("explanation", False,
                                "Set to True to translate code to natural language.")

    tf.app.flags.DEFINE_boolean("cross_valid", False,
                                "Set to True for cross validation.")
    tf.app.flags.DEFINE_integer("num_folds", 5,
                                "Number of folds in cross validation.")

    tf.app.flags.DEFINE_boolean("grid_search", False,
                                "Set to True for grid search.")
    tf.app.flags.DEFINE_string("tuning", "initialization,output_keep_prob,num_samples",
                               "List of hyperparamters to tune.")
    tf.app.flags.DEFINE_boolean("initialization", False,
                                "Set to try multiple random intialization and select the best one.")

    tf.app.flags.DEFINE_boolean("compare_models", False,
                                "Set to True to compare model performance.")
    tf.app.flags.DEFINE_boolean("data_stats", False,
                                "Set to True to print dataset statistics.")
    tf.app.flags.DEFINE_boolean("manual_eval", False,
                                "Set to True for manual evaluation.")
    tf.app.flags.DEFINE_boolean("eval", False,
                                "Set to True for quantitive evaluation.")
    tf.app.flags.DEFINE_boolean("process_data", False,
                                "Set to True for data preprocessing.")
    tf.app.flags.DEFINE_boolean("induce_slot_filling_mapping", False,
                                "Set to True for slot-filling mapping induction.")
    tf.app.flags.DEFINE_boolean("gen_slot_filling_training_data", False,
                                "Set to True to generate feature vectors for slot-filling training.")
    tf.app.flags.DEFINE_boolean("train_slot_filling", False,
                                "Set to True to train slot-filling classifier.")
    tf.app.flags.DEFINE_boolean("decode", False,
                                "Set to True for decoding.")
    tf.app.flags.DEFINE_boolean("test", False,
                                "Set to True to decode and evaluate on the test set.")
    tf.app.flags.DEFINE_boolean("demo", False,
                                "Set to True for interactive demo.")
    tf.app.flags.DEFINE_boolean("bucket_selection", False,
                                "Run a bucket_selection if this is set to True.")
    tf.app.flags.DEFINE_boolean("self_test", False,
                                "Run a self-test if this is set to True.")
    tf.app.flags.DEFINE_boolean("sample_train", False,
                                "Train on a subset of data if this is set to True.")
    tf.app.flags.DEFINE_integer("sample_size", 200,
                                "Training data sample size")

    # device
    tf.app.flags.DEFINE_string("gpu", '0', "GPU device where the computation is going to be placed.")
    tf.app.flags.DEFINE_boolean("log_device_placement", False,
                                "Set to True for logging device placement.")


    # training data property
    tf.app.flags.DEFINE_string("dataset", "bash", "select dataset to use.")
    tf.app.flags.DEFINE_integer("sc_vocab_size", 1000, "source vocabulary size.")
    tf.app.flags.DEFINE_integer("tg_vocab_size", 1000, "target vocabulary size.")
    tf.app.flags.DEFINE_integer("max_sc_length", 100, "maximum length of the source token sequence.")
    tf.app.flags.DEFINE_integer("max_tg_length", 100, "maximum length of the target token sequence.")
    tf.app.flags.DEFINE_string("data_dir", os.path.join(os.path.dirname(__file__), "data"),
                               "Raw data directory")
    tf.app.flags.DEFINE_string("data_split", "command", "Data split criteria")
    tf.app.flags.DEFINE_string("model_dir", "model", "Directory to save trained models.")
    tf.app.flags.DEFINE_boolean("create_fresh_params", False, "Set to force remove previously trained models.")

    # learning hyperparameters
    tf.app.flags.DEFINE_boolean("char", False, "Set to True for training character models.")
    tf.app.flags.DEFINE_boolean("canonical", False, "Set to True for learning with normalized command with "
                                                    "canonical option order.")
    tf.app.flags.DEFINE_boolean("normalized", False, "Set to True for learning with normalized command.")
    tf.app.flags.DEFINE_string("rnn_cell", "gru", "Type of RNN cell to use.")
    tf.app.flags.DEFINE_string("optimizer", "adam", "Type of numeric optimization algorithm to use.")
    tf.app.flags.DEFINE_float("learning_rate", 0.001, "Learning rate.")
    tf.app.flags.DEFINE_float("learning_rate_decay_factor", 0.99,
                              "Learning rate decays by this much.")
    tf.app.flags.DEFINE_float("max_gradient_norm", 5.0,
                              "Clip gradients to this norm.")
    tf.app.flags.DEFINE_integer("batch_size", 128,
                                "Batch size to use during training.")
    tf.app.flags.DEFINE_integer("num_samples", 512,
                                "Number of samples for sampled softmax.")
    tf.app.flags.DEFINE_float("encoder_input_keep", 1.0,
                                "Proportion of input to keep if dropout is used.")
    tf.app.flags.DEFINE_float("encoder_output_keep", 1.0,
                                "Proportion of output to keep if dropout is used.")
    tf.app.flags.DEFINE_float("decoder_input_keep", 1.0,
                                "Proportion of input to keep if dropout is used.")
    tf.app.flags.DEFINE_float("decoder_output_keep", 1.0,
                                "Proportion of output to keep if dropout is used.")
    tf.app.flags.DEFINE_integer("seed", -1, "Random seed for graph initialization.")
    tf.app.flags.DEFINE_integer("dim", 300, "Dimension of each model layer.")
    tf.app.flags.DEFINE_integer("num_layers", 1, "Number of layers in the model.")

    tf.app.flags.DEFINE_string("training_algorithm", "standard", "training algorithm to use.")
    tf.app.flags.DEFINE_string("pretrained_model_subdir", "", "signature of pretrained model.")

    tf.app.flags.DEFINE_boolean("use_copy", False, "If set, use copying mechanism.")

    tf.app.flags.DEFINE_string("encoder_topology", "rnn", "structure of the encoder.")
    tf.app.flags.DEFINE_string("decoder_topology", "rnn", "structure of the decoder.")

    tf.app.flags.DEFINE_boolean("use_attention", False, "If set, use attention decoder.")
    tf.app.flags.DEFINE_float("beta", 0.5, "Attention regularization.")
    tf.app.flags.DEFINE_float("attention_input_keep", 1.0,
                              "Proportion of attention input state to keep if dropout is used.")
    tf.app.flags.DEFINE_float("attention_output_keep", 1.0,
                              "Proportion of attention hidden state to keep if dropout is used.")

    tf.app.flags.DEFINE_string("decoding_algorithm", "greedy", "decoding algorithm to use.")
    tf.app.flags.DEFINE_integer("beam_size", -1, "Size of beam for beam search.")
    tf.app.flags.DEFINE_integer("beam_order", -1, "Order for beam search.")
    tf.app.flags.DEFINE_float("alpha", 0.5, "Beam search length normalization parameter.")
    tf.app.flags.DEFINE_integer("top_k", 5, "Top-k highest-scoring structures to output.")

    tf.app.flags.DEFINE_integer("num_gts", 1, "maximum number of ground truths per example.")
    tf.app.flags.DEFINE_float("margin", 1.0, "margin for margin-based loss function")
