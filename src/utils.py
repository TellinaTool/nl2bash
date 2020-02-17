"""
Utility functions.
"""
import os


def get_decode_signature(FLAGS):
    """
    Model signature is used to locate the trained parameters and
    prediction results of a particular model.
    """

    # The model directory is stamped with training hyperparameter information.
    model_subdir = FLAGS.dataset
    if FLAGS.explain:
        model_subdir += '-expl'
    if FLAGS.channel == 'char':
        model_subdir += '--char'
    elif FLAGS.channel == 'partial.token':
        model_subdir += '--partial'
    else:
        if FLAGS.nl_token:
            model_subdir += '-T'
        if FLAGS.sc_char:
            model_subdir += '-C'
        if FLAGS.tg_char:
            model_subdir += '-TC'
            model_subdir += '-{:.1f}'.format(FLAGS.gamma)
    model_subdir += '-{}'.format(FLAGS.min_vocab_frequency)
    model_subdir += '-{}'.format(FLAGS.encoder_topology)
    model_subdir += '-{}'.format(FLAGS.rnn_cell)
    model_subdir += '-{}'.format(FLAGS.training_algorithm)
    if FLAGS.cm_token_use_attention:
        model_subdir += '-attention'
        model_subdir += '-{}'.format(FLAGS.attention_input_keep)
        model_subdir += '-{}'.format(FLAGS.attention_output_keep)
        model_subdir += '-{:.1f}'.format(FLAGS.beta)
    if FLAGS.use_copy:
        model_subdir += '-copy'
        model_subdir += '-{:.1f}'.format(FLAGS.chi)
    model_subdir += '-{}'.format(FLAGS.batch_size)
    if FLAGS.nl_token:
        model_subdir += '-{}'.format(FLAGS.nl_token_dim)
    if FLAGS.sc_char:
        model_subdir += '-{}'.format(FLAGS.sc_char_dim)
    model_subdir += '-{}'.format(FLAGS.num_layers)
    if FLAGS.recurrent_batch_normalization:
        model_subdir += '-rbc'
    model_subdir += '-{}'.format(FLAGS.learning_rate)
    model_subdir += '-{}'.format(FLAGS.adam_epsilon)
    model_subdir += '-{}'.format(FLAGS.sc_input_keep)
    model_subdir += '-{}'.format(FLAGS.sc_output_keep)
    model_subdir += '-{}'.format(FLAGS.tg_input_keep)
    model_subdir += '-{}'.format(FLAGS.tg_output_keep)
    if FLAGS.canonical:
        model_subdir += '.canonical'
    elif FLAGS.normalized:
        model_subdir += '.normalized'

    # The prediction file of a particular model is stamped with decoding
    # hyperparameter information.
    decode_sig = FLAGS.token_decoding_algorithm
    if FLAGS.token_decoding_algorithm == 'beam_search':
        decode_sig += ".{}".format(FLAGS.beam_size)
    if FLAGS.fill_argument_slots:
        decode_sig += '.slot.filler'
    decode_sig += (".test" if FLAGS.test else ".dev")
    return model_subdir, decode_sig


def clean_dir(dir):
    for f_name in os.listdir(dir):
        if f_name.startswith('prediction'):
            continue
        f_path = os.path.join(dir, f_name)
        try:
            if os.path.isfile(f_path):
                os.unlink(f_path)
        except Exception as e:
            print(e)