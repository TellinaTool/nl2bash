# Tellina Learning Module

This repository consists of four main components:

1. A Tensorflow implementation of an RNN encoder-decoder model which we augmented with argument filling and other enhancements.
2. An improved version of the [bashlex](https://github.com/idank/bashlex) parser which we augmented with in-command structures between utilities, flags and arguments.
3. A set of simple natural language processing tools for processing the input natural language, including the regex-based sentence tokenizer and named entity recognizer.
4. A set of tools used to extract bash utility grammars from man pages.

### Install TensorFlow

The Tensorflow library is required to reproduce our experiments. The experiments can be reproduced on normal CPU machines.

Please follow the instructions on the [official website](https://www.tensorflow.org/versions/r0.9/get_started/os_setup.html) to install the library.

### Set up experiment environment

Type `make` to set up the experiment environment. This sets the Python path and the tools which the main experiment would depend on.

Afterwards please follow the instructions in the [experiment folder](https://github.com/TellinaTool/learning_module/tree/master/experiments) to reproduce our experiment results.
