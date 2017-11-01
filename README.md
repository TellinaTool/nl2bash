# Awesome Neural Machine Translation

## Overview

This repository consists of the following components:

1. A Tensorflow implementation of a sequence-to-sequence model which we augmented with argument filling and other enhancements.
2. An improved version of the [bashlex](https://github.com/idank/bashlex) parser which we augmented with in-command structures between utilities, flags and arguments.
3. A set of simple natural language processing tools for processing the input natural language, including the regex-based sentence tokenizer and named entity recognizer.
4. A set of tools used to extract bash utility grammars from man pages.

## Experiment Setup

### Install TensorFlow

The Tensorflow library is required to reproduce our experiments. The experiments can be reproduced on normal CPU machines.

Please follow the instructions on the [official website](https://www.tensorflow.org/versions/r0.9/get_started/os_setup.html) to install the library.

### Environment Variables & Dependencies

Type `make` to set up the experiment environment. This sets the Python path and the tools which the main experiment would depend on.

Afterwards please follow the instructions in the [experiment folder](https://github.com/TellinaTool/learning_module/tree/master/experiments) to reproduce our experiment results.

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
