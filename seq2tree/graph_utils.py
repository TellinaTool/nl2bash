"""Utility functions related to graph construction."""

import functools
import warnings

import tensorflow as tf

def create_multilayer_cell(type, scope, dim, num_layers, input_keep_prob=1, output_keep_prob=1):
    """
    Create the multi-layer RNN cell.
    :param type: Type of RNN cell.
    :param scope: Variable scope.
    :param dim: Dimension of hidden layers.
    :param num_layers: Number of layers of cells.
    :param input_keep_prob: Proportion of input to keep in dropout.
    :param output_keep_prob: Proportion of output to keep in dropout.
    :return: RNN cell as specified.
    """
    with tf.variable_scope(scope):
        if type == "lstm":
            cell = tf.nn.rnn_cell.BasicLSTMCell(dim, state_is_tuple=True)
        elif type == "gru":
            cell = tf.nn.rnn_cell.GRUCell(dim)
        else:
            raise ValueError("Unrecognized RNN cell type.")

        if num_layers > 1:
            cell = tf.nn.rnn_cell.MultiRNNCell([cell] * num_layers,
                                               state_is_tuple = (type == "lstm"))

        assert(input_keep_prob >= 0 and output_keep_prob >= 0)
        if input_keep_prob < 1 or output_keep_prob < 1:
            cell = tf.nn.rnn_cell.DropoutWrapper(cell, input_keep_prob=input_keep_prob,
                                                 output_keep_prob=output_keep_prob)
    return cell


def map_fn(fn, elems, batch_size):
    """Pesudo multi-ariti scan."""
    results = []
    elem_lists = [tf.split(0, batch_size, elem) for elem in elems]
    for i in xrange(batch_size):
        args = [tf.squeeze(elem_lists[0][i], squeeze_dims=[0])] + \
               [elem_list[i] for elem_list in elem_lists[1:]]
        results.append(fn(args))
    _results = tf.concat(0, results)
    return _results


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)     #turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)    #reset filter
        return func(*args, **kwargs)

    return new_func
