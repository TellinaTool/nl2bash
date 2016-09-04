"""Range of hyperparameters for grid search."""

hyperparam_range = {
    "input_keep_prob": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
    "output_keep_prob": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
    "num_samples": [1024, 512]
}