# This Makefile wraps commands used to set up the learning environment.

setup:
	# Set PYTHONPATH 
	export PYTHONPATH=`pwd`
	# Set up data files used in the learning module
	tar xf data/bash/vocab.tar.xz --directory data/bash/
	# tar xf data/bash.final/vocab.tar.xz --directory data/bash.final/
	# Set up nlp tools
	tar xf nlp_tools/spellcheck/most_common.tar.xz --directory nlp_tools/spellcheck/
