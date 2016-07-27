import cPickle as pickle
import sys
from parser import *

if __name__ == "__main__":
    with open("../model/model.cpkl") as f:
	parser = pickle.load(f)
    # example = Example("create tar file", "tar -c")
    # print(parser.score_example(example))
    parser.parse(sys.argv[1], 10)
