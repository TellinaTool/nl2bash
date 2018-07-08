# NL2Bash

## Overview

This repository contains the data and source code release of the paper: [NL2Bash: A Corpus and Semantic Parser for
Natural Language Interface to the Linux Operating System](http://victorialin.net/pubs/nl2bash.pdf).

Specifically, it contains the following components:

1. A set of ~10,000 bash one-liners collected from websites such as StackOverflow and their English descriptions written by Bash programmers.
2. Tensorflow implementations of the following translation models:
   - the standard [Seq2Seq](https://arxiv.org/abs/1409.0473) and [CopyNet](https://arxiv.org/abs/1603.06393) models
   - a stage-wise NL⟶Bash model using argument filling heuristics ([Lin et. al. 2017](http://victorialin.net/pubs/tellina_tr_2017.pdf)).
3. A Bash command parser which parses a Bash command into an abstractive syntax tree, developed on top of  [bashlex](https://github.com/idank/bashlex).
4. A set of domain-specific natural language processing tools, including a regex-based sentence tokenizer and a domain specific named entity recognizer.

## Experiment Setup

### Install TensorFlow

To reproduce our experiments, please install TensorFlow (>= 1.0). The experiments can be reproduced on machines with or without GPUs.

We suggest following the [official instructions](https://www.tensorflow.org/install/) to install the library. The following pip installation command is copied from the official website and has been tested on Mac OS 10.10.5.
```
sudo pip3 install --upgrade \
 https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.3.0-py3-none-any.whl 
```

### Environment Variables & Dependencies

Once TensorFlow is installed, run `make` in the root directory of the repo. This sets up the Python path and main experiment dependencies.
```
(sudo) make
```

### Change Directory

Then enter the [experiments](/experiments) directory.
```
cd experiments
```
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
make gen_evaluation_table
```

By default, the decoding and evaluation steps will print sanity checking messages. You may set `verbose` to `False` in the following source files to suppress those messages.
```
encoder_decoder/decode_tools.py
eval/eval_tools.py
```


## Citation

If you use the data or source code in your work, please cite
```
@inproceedings{LinWZE2018:NL2Bash, 
  author = {Xi Victoria Lin and Chenglong Wang and Luke Zettlemoyer and Michael D. Ernst}, 
  title = {NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System}, 
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources
               and Evaluation {LREC} 2018, Miyazaki (Japan), 7-12 May, 2018.},
  year = {2018} 
}
```

Related paper: [Program Synthesis from Natural Language Using Recurrent Neural Networks](http://victorialin.net/pubs/tellina_tr_2017.pdf). 
