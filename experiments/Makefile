# This Makefile wraps commands used to set up the learning environment.
gpu = "--gpu ''"

all: print

data:
	# Filter raw parallel corpus and split to train/dev/test as reported 
	# in the paper
	cd ../data/scripts && \
	python3 filter_data.py bash && \
	python3 split_data.py bash && \
	cd ../../experiments
	
	# Convert raw parallel corpus to features taken by the neural network
	./bash-run.sh --process_data --dataset bash
	
decode:
	# Decode candidate output from pretrained models
	./bash-token.sh --decode $(gpu)
	./bash-token.sh --normalized --fill_argument_slots --decode $(gpu)
	./bash-copy.sh --decode $(gpu)
	./bash-partial-token.sh --decode $(gpu)
	./bash-copy-partial-token.sh --decode $(gpu)
	./bash-char --decode $(gpu)
	./bash-copy-char.sh --decode $(gpu)
	
gen_evaluation_table:
	./bash-token.sh --gen_manual_evaluation_table
	
train:
	./bash-token.sh
	./bash-token.sh --normalized --fill_argument_slots
	./bash-copy.sh
	./bash-partial-token.sh
	./bash-copy-partial-token.sh
	./bash-char
	./bash-copy-char.sh

print: decode gen_evaluation_table
