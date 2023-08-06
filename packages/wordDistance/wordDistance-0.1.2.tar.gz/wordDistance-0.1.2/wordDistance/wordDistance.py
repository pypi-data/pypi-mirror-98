import multiprocessing
from multiprocessing import Pool
import multiprocessing, logging
from itertools import combinations
import json


class wordDistance:
    def __init__(self, arr):
        self.input = arr
        self.result_list = []

    def __repr__(self):
        return json.dumps(self.result_list)

    # by default we can only have two permutations
    def create_logger(self):
        logger = multiprocessing.get_logger()
        logger.setLevel(logging.DEBUG) # logging.DEBUG
        formatter = logging.Formatter(\
            '[%(asctime)s| %(levelname)s| %(processName)s] %(message)s')
        handler = logging.FileHandler('word_editor.log')
        handler.setFormatter(formatter)

        # this bit will make sure you won't have
        # duplicated messages in the output
        if not len(logger.handlers):
            logger.addHandler(handler)
        return logger


    def log_result(self, result):
        self.result_list.append(result)
        if len(self.result_list) % 100 == 0:
            print("We are running %s calculations"%(len(self.result_list) % 100))


    # algorithm for word distance
    def parallel_run(self, word1, word2):
        if not word1: return len(word2)
        if not word2: return len(word1)
        len_word1 = len(word1)
        len_word2 = len(word2)
        # use the dynamic programming to calculate the word distance
        dp = [[0 for i in range(len_word1 + 1)] for j in range(len_word2 + 1)]

        for i in range(len_word1 + 1):
            dp[0][i] = i
        for j in range(len_word2 + 1):
            dp[j][0] = j
        for i in range(1, len_word2 + 1):
            for j in range(1, len_word1 + 1):
                if word1[j - 1] == word2[i - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j]) + 1

        return dp[-1][-1]


    def calculate_distance(self):

        logger = self.create_logger()
        logger.info('Starting pooling')
        pool = Pool(multiprocessing.cpu_count() - 2)
        word_pair = []
        total_number = 0
        input = combinations(self.input, 2)
        for data in input:

            word_pair.append(data)
            total_number += 1
            pool.apply_async(self.parallel_run, args=(*data, ), callback=self.log_result)

        pool.close()
        pool.join()
        hashmap = {}
        for key, val in zip(word_pair, self.result_list):
            hashmap[key] = val

        print(hashmap)
        return hashmap


if __name__ == '__main__':
    print('main line')
    arr = ['abscca', 'bbsscc', 'dsddccd', 'cc', 'cc', 'd', 'ccss', 'ssddc ']
    obj = wordDistance(arr)
    obj.calculate_distance()
    print(obj)

