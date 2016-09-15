"""Range of hyperparameters for grid search."""

hyperparam_range = {
    "decoder_input_keep": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
    "decoder_output_keep_": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
    "num_layers": [2, 4, 8],
    "num_samples": [1024, 512]
}
