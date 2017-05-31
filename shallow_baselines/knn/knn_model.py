import heapq
import math

default_encoding_val = 999999999

class KNNModel(object):
    def __init__(self):
        self.idf = {}
        self.term_occur_count = {}

    def train(self, train_set):
        self.data_size = len(train_set)

        # the file containing training nl vectors and cmd vectors
        cmd_vec_list = [cmd_vec for _, _, _, cmd_vec in train_set]
        sc_vec_list = [sc_vec for _, _, sc_vec, _ in train_set]

        sc_vec_to_tg_vec = {}
        for i in range(self.data_size):
            sc_vec_to_tg_vec[str(sc_vec_list[i])] = cmd_vec_list[i]

        # calculate term weight based on tf-idf
        for vec in sc_vec_list:
            for k in set(vec):
                if k in self.term_occur_count:
                    self.term_occur_count[k] += 1
                else:
                    self.term_occur_count[k] = 1

        self.sc_vec_list = sc_vec_list
        self.sc_vec_to_tg_vec = sc_vec_to_tg_vec

    def test(self, test_vec, k):
        top_knns = self.find_k_nearest_neighbor(test_vec, self.sc_vec_list, k)
        top_k_results = []
        for nl, score in top_knns:
            cmd = self.sc_vec_to_tg_vec[str(nl)]
            top_k_results.append((nl, cmd, score))
        return top_k_results

    # given a token, return idf
    def get_idf(self, k):
        count = 0
        if k in self.term_occur_count:
            count = self.term_occur_count[k]
        # remove low-frequency words
        # if count < 4:
        #     return 0
        return math.log(float(self.data_size) / (1 + count))

    def get_tf(self, term, term_vec):
        r = 0
        for k in term_vec:
            if k == term:
                r += 1
        return r

    # compute the distance between two natural language vectors
    def compute_sc_vec_distance(self, nlvec1, nlvec2):
        overlapped_tok = list(set(nlvec1) & set(nlvec2))

        nlvec1_weighted_len = 0.
        for k in set(nlvec1):
            v = self.get_tf(k, nlvec1) * self.get_idf(k)
            nlvec1_weighted_len += v * v
        nlvec1_weighted_len = math.sqrt(nlvec1_weighted_len)

        nlvec2_weighted_len = 0.
        for k in set(nlvec2):
            v = self.get_tf(k, nlvec2) * self.get_idf(k)
            nlvec2_weighted_len += v * v
        nlvec2_weighted_len = math.sqrt(nlvec2_weighted_len)

        s = 0

        for k in overlapped_tok:
            v1 = self.get_tf(k, nlvec1) * self.get_idf(k)
            v2 = self.get_tf(k, nlvec2) * self.get_idf(k)
            s += v1 * v2

        return s / (nlvec2_weighted_len * nlvec1_weighted_len)

    # sort and find top k most rated bitvectors
    def find_k_nearest_neighbor(self, vec, vec_list, k):
        scored_vec_list = map(lambda v: (v, self.compute_sc_vec_distance(vec, v)),
                              vec_list)
        return heapq.nlargest(k, scored_vec_list, key=lambda x: x[1])


# take a vector and a dictionary to decode a vector to a string
def decode_vec_to_str(vec, dictionary):
    return reduce(lambda x, y: x + " " + y, map(lambda x: dictionary[x], vec), "")


# encode a string to a vector based on the dictionary
def encode_str_to_vec(s, dictionary):
    return filter(lambda x: x != default_encoding_val,
                  map(lambda x: dictionary[x] if (x in dictionary) else default_encoding_val,
                      s.split()))
