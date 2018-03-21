# NL2Bash

## Overview

This repository contains the data and source code release of the paper: [NL2Bash: A Corpus and Semantic Parser for
Natural Language Interface to the Linux Operating System](http://victorialin.net/pubs/nl2bash.pdf).

Specifically, it contains the following components:

1. A set of ~10,000 bash one-liners collected from websites such as StackOverflow and their English descriptions written by Bash programmers.
2. Tensorflow implementations of the following translation models:
   - the standard [Seq2Seq](https://arxiv.org/abs/1409.0473) and [CopyNet](https://arxiv.org/abs/1603.06393) models
   - a stage-wise nl⟶Bash model using argument filling heuristics ([Lin et. al. 2017](http://victorialin.net/pubs/tellina_tr_2017.pdf)).
3. A bash command parser which parses a bash command into an abstractive syntax tree, developed on top of  [bashlex](https://github.com/idank/bashlex).
4. A set of domain-specific natural language processing tools, including a regex-based sentence tokenizer and a bash-domain named entity recognizer.

## Experiment Setup

### Install TensorFlow

The Tensorflow library is required to reproduce our experiments. The experiment results can be reproduced on machines with or without GPUs.

Please follow the instructions on the [official website](https://www.tensorflow.org/install/) to install the library.

The following pip installation command has been tested on Mac OS 10.10.5.
```
sudo pip3 install --upgrade \
 https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.3.0-py3-none-any.whl 
```

### Environment Variables & Dependencies
First of all, run `make` in the root directory of the repo.
```
(sudo) make
```
This sets up the Python path and other tools on which the main experiment depends.

Then change to the [experiments](/experiments) folder and follow the instructions there to reproduce our results.
```
cd experiments
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
