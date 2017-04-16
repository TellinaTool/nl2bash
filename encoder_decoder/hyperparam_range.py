"""Range of hyperparameters for grid search."""

hyperparam_range = {
    "attention_input_keep": [0.4, 0.6, 0.8, 1.0],
    "attention_output_keep": [0.4, 0.6, 0.8, 1.0],
    "sc_input_keep": [0.6, 0.7, 0.8],
    "sc_output_keep": [0.6, 0.7, 0.8],
    "tg_input_keep": [0.6, 0.7, 0.8],
    "tg_output_keep": [0.5, 0.6, 0.7, 0.8],
    "num_layers": [2, 4, 8],
    "num_samples": [1024, 512],
    "beta": [0.8,0.9,1.0,1.1,1.2]
}
