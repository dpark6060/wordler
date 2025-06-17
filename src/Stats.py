
import functools
from itertools import chain, combinations
import logging
import re

log = logging.getLogger()


class LetterStats:
    """ Calculates frequency statistics for every letter given a list of words.
    Generally given the full list of five letter words initially and stats are calculated off that.

    """

    @classmethod
    def init_and_calc(cls, words):
        instance = cls()
        instance.calc_stats(words)
        return instance

    def __init__(self):

        self.letter_prob = None
        self.bigram_prob = None
        self.letter_occurance = None
        self.num_words = 0


    def calc_stats(self, words = []):

        # Store frequencies of letters and bigrams (combos of two letters)
        letters = {}
        bigrams = {}

        # Loop through each letter of each word
        for word in words:
            for c in word:
                if c in letters.keys():
                    letters[c] += 1
                else:
                    letters[c] = 1

            for i in range(len(word) - 1):
                bigram = str(word[i] + word[i + 1])
                if bigram in bigrams.keys():
                    bigrams[bigram] += 1
                else:
                    bigrams[bigram] = 1

        numwords = len(words)
        letters = {k: v / numwords for k, v in letters.items()}
        bigrams = {k: v / numwords for k, v in bigrams.items()}

        sorted_letters = letters
        sorted_bigrams = bigrams

        self.letter_prob = sorted_letters
        self.bigram_prob = sorted_bigrams

    def calc_in_word_stats(self, words):

        # Store frequencies of letters and bigrams (combos of two letters)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        letters = {l:0 for l in alphabet}
        for letter in alphabet:
            for word in words:
                if letter in word:
                    letters[letter] += 1


        numwords = len(words)
        letters = {k: v / numwords for k, v in letters.items()}
        for k, v in letters.items():
            if v == 1.0:
                letters[k] = 0
        return letters

    def get_letter_prob(self, letter: str):
        return self.letter_prob[letter]


    @functools.cache
    def get_word_stats(self, word: str):
        return sum([self.get_letter_prob(w) for w in word])


class WordStats:
    def __init__(self, letter_prob, bigram_prob):
        self.letter_prob = letter_prob
        self.bigram_prob = bigram_prob

    def debug_print(self, sorted_match_num, sorted_words):
        for word, num in zip(sorted_words, sorted_match_num):
            print(f"Word {word} Total Matches:  {num}")

    def find_best_guess(self, full_word_list, current_possible_words):
        word_dict = {w: 0 for w in full_word_list}
        for i,word in enumerate(full_word_list):
            print(f"processing {i}")
            shared_letter_rating = self.process_word(word, current_possible_words)
            word_dict[word] = shared_letter_rating

        sorted_match_num, sorted_words = zip(*sorted(zip(word_dict.values(), word_dict.keys())))
        self.debug_print(sorted_match_num, sorted_words)
        return sorted_words[-10:], sorted_match_num[-10:]

    def process_word(self, word, word_list):
        #sorted_letters = self.sort_letters_by_prob(word)
        words_with_common_letters = self.find_words_with_common_letters(word, word_list)
        shared_letter_rating = self.calc_stats(words_with_common_letters)
        return shared_letter_rating

    def find_words_with_common_letters(self, sorted_letters, word_list):
        words_with_letter_subset = {k: 0 for k in list(range(1, 6))}
        for subset in self.all_subsets(sorted_letters):
            n_letters = len(subset)
            if n_letters == 0:
                continue

            joined_subset = "".join(subset)
            counted_subset = {char: joined_subset.count(char) for char in joined_subset}
            matching_words = self.find_words_with_matching_letters(counted_subset, word_list)
            words_with_letter_subset[n_letters] += len(matching_words)

        return words_with_letter_subset

    def find_words_with_matching_letters(self, counted_letters, word_list):
        matching_words = [w for w in word_list if all([w.count(letter) == count for letter, count in counted_letters.items()])]
        return matching_words

    # This gets a bit beyond my understanding of python, but I timed it compared to another method, and it's faster.
    @staticmethod
    def all_subsets(ss):
        # Skip single letters, that's kinda useless.
        return chain(*map(lambda x: combinations(ss, x), range(4, len(ss) + 1)))

    def calc_stats(self, words_with_common_letters):
        total_matches = 0
        for k, v in words_with_common_letters.items():
            total_matches += v
            #print(f"Words Sharing {k} letters:  {v}")
        return total_matches