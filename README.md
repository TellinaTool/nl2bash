# Awesome Neural Machine Translation

## Overview

This repository consists of the following components:

1. Tensorflow implementations of the sequence-to-sequence neural machine translation model and its variations.
2. A bash command parser which parses a bash command into an abstractive syntax tree, developed on top of  [bashlex](https://github.com/idank/bashlex).
3. A set of domain-specific natural language processing tools, including a regex-based sentence tokenizer and a bash-domain named entity recognizer.

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
First of all, run `make` in the root directory of the repo. Run `sudo make` if you encounter permission error in this step.
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
@techreport{LinWPVZE2017:TR, 
  author = {Xi Victoria Lin and Chenglong Wang and Deric Pang and Kevin Vu and Luke Zettlemoyer and Michael D. Ernst}, 
  title = {Program synthesis from natural language using recurrent neural networks}, 
  institution = {University of Washington Department of Computer Science and Engineering}, 
  number = {UW-CSE-17-03-01}, 
  address = {Seattle, WA, USA}, 
  month = mar, 
  year = {2017} 
}
```
