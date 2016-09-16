"""Range of hyperparameters for grid search."""

hyperparam_range = {
    "encoder_input_keep": [1.0, 0.9, 0.8, 0.7],
    "encoder_output_keep": [1.0, 0.9, 0.8],
    "decoder_input_keep": [1.0, 0.9, 0.8, 0.7],
    "decoder_output_keep": [1.0, 0.9, 0.8],
    "num_layers": [2, 4, 8],
    "num_samples": [1024, 512]
}
