## Experiments

### Data filtering, split and pre-processing

Run the following command. This will clean the raw NL2Bash corpus and apply filtering, create the train/dev/test splits and preprocess the data into the formats taken by the Tensorflow models. 

```
make data
```
To change the data-processing workflow, go to [data](/data) and modify the utility scripts.

### Train the models
```
make train
```

### Generate evaluation table using pre-trained models

Decode the pre-trained models and print the evaluation summary table.
```
make decode
```

Skip the decoding step and print the evaluation summary table from the predictions saved on disk.
```
make gen_manual_evaluation_table
```

By default, the decoding and evaluation steps will print sanity checking messages. You may set `verbose` to `False` in the following source files to suppress those messages.
```
encoder_decoder/decode_tools.py
eval/eval_tools.py
```
