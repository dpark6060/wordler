
import functools


class LetterStats:
    """ Calculates frequency statistics for every letter given a list of words.
    Generally given the full list of five letter words initially and stats are calculated off that.

    """
    def __init__(self, words):

        self.words = words
        self.letter_prob = None
        self.bigram_prob = None
        self.calc_stats()
        self.num_words = len(self.words)



    def calc_stats(self, words = []):
        if words:
            self.words = words

        # Store frequencies of letters and bigrams (combos of two letters)
        letters = {}
        bigrams = {}

        # Loop through each letter of each word
        for word in self.words:
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

        numwords = len(self.words)
        letters = {k: v / numwords for k, v in letters.items()}
        bigrams = {k: v / numwords for k, v in bigrams.items()}

        sorted_letters = letters
        sorted_bigrams = bigrams

        self.letter_prob = sorted_letters
        self.bigram_prob = sorted_bigrams


    def get_letter_prob(self, letter: str):
        return self.letter_prob[letter]


    @functools.cache
    def get_word_stats(self, word: str):
        return sum([self.get_letter_prob(w) for w in word])
