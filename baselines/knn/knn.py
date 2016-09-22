import os
import heapq
import math
import sys

data_dir = "."

default_encoding_val = 999999999

# utility function to load vector list from file
def load_file_to_vec_list(path):
  f = open(path, 'r')
  lst = []
  for line in f:
    vec = line.split()
    lst.append(map(lambda x : int(x), vec))
  return lst

def load_dictionary(path, reverse = False):
  f = open(path, 'r')
  dictionary = {}
  cnt = 0
  for line in f:
    if not reverse:
      dictionary[cnt] = line.strip()
    else:
      dictionary[line.strip()] = cnt
    cnt += 1
  return dictionary

# the file containing traning nl vectors and cmd vectors
cmd_vec_list = load_file_to_vec_list(os.path.join(data_dir, "train.ids1500.cm"))
nl_vec_list = load_file_to_vec_list(os.path.join(data_dir, "train.ids1500.nl"))


nl_vec_to_cmd_vec = {}

for i in range(len(cmd_vec_list)):
  nl_vec_to_cmd_vec[str(nl_vec_list[i])] = cmd_vec_list[i]


# dictionary to decode vectors to raw cmd or nl string
cmd_dictionary = load_dictionary(os.path.join(data_dir, "vocab1500.cm"))
nl_dictionary = load_dictionary(os.path.join(data_dir, "vocab1500.nl"))

# dictionary to encode nl/cmd string to bitvector
cmd_reverse_dictionary = load_dictionary(os.path.join(data_dir, "vocab1500.cm"), reverse=True)
nl_reverse_dictionary = load_dictionary(os.path.join(data_dir, "vocab1500.nl"), reverse=True)

# calculate term weight based on tf-idf

idf = {}
term_occur_count = {}

for vec in nl_vec_list:
  for k in set(vec):
    if k in term_occur_count:
      term_occur_count[k] += 1
    else:
      term_occur_count[k] = 1

# given a token, return idf
def get_idf(k):
  count = 0
  if k in term_occur_count:
    count = term_occur_count[k]
  return math.log(float(len(nl_vec_list)) / (1 + count) )

def get_tf(term, term_vec):
  r = 0
  for k in term_vec:
    if k == term:
      r = r + 1
  return r

token_weight_func = {}

# take a vector and a dictionary to decode a vector to a string
def decode_vec_to_str(vec, dictionary):
  return reduce(lambda x, y: x + " " + y, map(lambda x : dictionary[x], vec), "")

# encode a string to a vector based on the dictionary
def encode_str_to_vec(s, dictionary):
  return filter(lambda x :  x != default_encoding_val, 
                  map(lambda x : dictionary[x] if (x in dictionary) else default_encoding_val, 
                        s.split()))

# sort and find top k most rated bitvectors
def find_k_nearest_neighbor(vec, vec_list, k):
  scored_vec_list = map(lambda v : (v, compute_nl_vec_distance(vec, v)), vec_list)
  return heapq.nlargest(k, scored_vec_list, key=lambda x:x[1])

# compute the distance between two natural language vectors
def compute_nl_vec_distance(nlvec1, nlvec2):
  overlapped_tok = list(set(nlvec1) & set(nlvec2))

  nlvec1_weighted_len = 0.
  for k in set(nlvec1):
    v = get_tf(k, nlvec1) * get_idf(k)
    nlvec1_weighted_len += v * v
  nlvec1_weighted_len = math.sqrt(nlvec1_weighted_len)

  nlvec2_weighted_len = 0.
  for k in set(nlvec2):
    v = get_tf(k, nlvec2) * get_idf(k)
    nlvec2_weighted_len += v * v
  nlvec2_weighted_len = math.sqrt(nlvec2_weighted_len)

  s = 0

  for k in overlapped_tok:
    v1 = get_tf(k, nlvec1) * get_idf(k)
    v2 = get_tf(k, nlvec2) * get_idf(k)
    s += v1 * v2

  return s / (nlvec2_weighted_len * nlvec1_weighted_len)


  #return float(len(overlapped_tok)) / float(((len(nlvec1) + len(nlvec2)) / 2))

def main():
  #test_vec = [26, 12, 10, 11, 15, 17, 28, 171, 18, 339]

  #print "[command] ", decode_vec_to_str(test_vec, nl_dictionary)

  # find k nearest neighbor
  #knn = find_k_nearest_neighbor(test_vec, nl_vec_list, 1)

  #for p in knn:
  #  print "[nn vec] ", p
    # print the decoding result of these filters
  #  print "[nearest neighbor] ", decode_vec_to_str(p[0], nl_dictionary)

  sys.stdout = open('result.txt', 'w')

  # the file containing traning nl vectors and cmd vectors
  test_cmd_vec_list = load_file_to_vec_list(os.path.join(data_dir, "dev.ids1500.cm"))
  test_nl_vec_list = load_file_to_vec_list(os.path.join(data_dir, "dev.ids1500.nl"))


  for i in range(len(test_nl_vec_list)):
    test_vec = test_nl_vec_list[i]
    cmd_vec = test_cmd_vec_list[i]

    print test_vec

    nl = find_k_nearest_neighbor(test_vec, nl_vec_list, 1)[0][0]
    cmd = nl_vec_to_cmd_vec[str(nl)]

    print "[text-case]"
    print "  [original-pair]"
    print "     ", decode_vec_to_str(test_vec, nl_dictionary)
    print "     ", decode_vec_to_str(cmd_vec, cmd_dictionary)
    print "  [new-pair]"
    print "     ", decode_vec_to_str(nl, nl_dictionary)
    print "     ", decode_vec_to_str(cmd, cmd_dictionary)



if __name__ == '__main__':
  main()












