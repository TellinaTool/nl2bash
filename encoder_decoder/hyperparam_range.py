"""Range of hyperparameters for grid search."""

hyperparam_range = {
    "attention_input_keep": [0.5, 0.6, 0.7, 0.8],
    "attention_output_keep": [0.5, 0.6, 0.7, 0.8],
    "encoder_input_keep": [0.6, 0.7, 0.8],
    "encoder_output_keep": [0.6, 0.7, 0.8],
    "decoder_input_keep": [0.6, 0.7, 0.8],
    "decoder_output_keep": [0.5, 0.6, 0.7, 0.8],
    "num_layers": [2, 4, 8],
    "num_samples": [1024, 512],
    "beta": [0.1]
}
