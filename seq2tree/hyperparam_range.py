"""Range of hyperparameters for grid search."""

hyperparam_range = {
    "encoder_input_keep": [0.5, 0.6],
    # "encoder_input_keep": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "encoder_output_keep": [0.7, 0.8, 0.9, 1.0],
    "decoder_input_keep": [0.5, 0.6],
    # "decoder_input_keep": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "decoder_output_keep": [0.7, 0.8, 0.9, 1.0],
    "num_layers": [2, 4, 8],
    "num_samples": [1024, 512]
}
