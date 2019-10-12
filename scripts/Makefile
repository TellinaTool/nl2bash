# This Makefile wraps commands used to reproduce the baseline system results.

## Toggle the two lines below if you are reproducing the experiments using CPU
# gpu = "--gpu ''"
gpu = "--gpu 0"

all: print

data:
	# Filter raw parallel corpus and split to train/dev/test 
	cd ../data/scripts && \
	python3 filter_data.py bash && \
	python3 split_data.py bash && \
	cd ../../scripts
	
	# Convert raw parallel corpus to features taken by the neural network
	./bash-run.sh --process_data --dataset bash
	
decode:
	# Decode candidate outputs of the baseline systems given the pretrained models (on the dev set)
	## Add '--test' to the end of each command to perform decoding on the test set  
	./bash-token.sh --decode $(gpu)
	./bash-token.sh --normalized --fill_argument_slots --decode $(gpu)
	./bash-copy.sh --decode $(gpu)
	./bash-partial-token.sh --decode $(gpu)
	./bash-copy-partial-token.sh --decode $(gpu)
	./bash-char.sh --decode $(gpu)
	./bash-copy-char.sh --decode $(gpu)	
	
gen_manual_evaluation_table:
	# Generate dev set manual evaluation result table
	## Add '--test' to the end of the command to generate the test set (manual) evaluation result table
	./bash-token.sh --gen_manual_evaluation_table
	
gen_auto_evaluation_table:
	# Generate dev set automatic evaluation result table
	## Add '--test' to the end of the command to generate the test set (automatic) evaluation result table
	./bash-token.sh --gen_auto_evaluation_table
	
train:
	
	./bash-token.sh
	./bash-token.sh --normalized --fill_argument_slots
	./bash-copy.sh
	./bash-partial-token.sh
	./bash-copy-partial-token.sh
	./bash-char.sh
	./bash-copy-char.sh

results: train decode gen_evaluation_table
