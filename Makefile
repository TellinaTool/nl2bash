# This Makefile wraps commands used to set up the learning environment.

setup:
	# Set up nlp tools
	tar xf src/nlp_tools/spellcheck/most_common.tar.xz --directory src/nlp_tools/spellcheck/
	
	# Install Python packages
	pip3 install -r requirements.txt
