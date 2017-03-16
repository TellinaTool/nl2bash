# This Makefile wraps commands used to set up the learning environment.

MODEL_ROOT=`pwd`

setup:
	# Set PYTHONPATH 
	export PYTHONPATH=$(MODEL_ROOT)
	# Set up data files used in the learning module
	tar xf $(MODEL_ROOT)/data/bash/vocab.tar.xz --directory $(MODLE_ROOT)/data/bash/
	tar xf $(MODEL_ROOT)/data/bash.final/vocab.tar.xz --directory $(MODEL_ROOT)/data/bash.final/
	# Set up nlp tools
	tar xf $(MODEL_ROOT)/nlp_tools/spellcheck/most_common.tar.xz --directory $(MODEL_ROOT)/nlp_tools/spellcheck/
