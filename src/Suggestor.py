
from src import Stats


class Suggestor:
    def __init__(self):
        self.stats = Stats.LetterStats()
        #self.wstats = Stats.WordStats()

    def suggest(self, current_possible_words, unknown_letters):
        letter_stats = self.stats.calc_in_word_stats(current_possible_words)
        print(f"e stats: {letter_stats['e']}")
        guesses = self.find_best_guesses(current_possible_words, letter_stats, unknown_letters)
        return guesses

    def find_best_guesses(self, full_word_list, letter_stats, unknown_letters):
        word_dict = {w: 0 for w in full_word_list}
        for i, word in enumerate(full_word_list):
            rating = self.process_word(word, letter_stats)
            multiplier = 1
            for letter in word:
                if letter in unknown_letters:
                    multiplier += 1

            word_dict[word] = rating * 1.1**multiplier

        sorted_match_num, sorted_words = zip(*sorted(zip(word_dict.values(), word_dict.keys())))
        #return sorted_words, sorted_match_num

        print(sorted_match_num[-1])
        num_to_return = 20
        return sorted_words[-num_to_return:], sorted_match_num[-num_to_return:]

    def process_word(self, word, letter_stats):
        #sorted_letters = self.sort_letters_by_prob(word)
        # repeated words have a reduction in probability 
        multiplier = [1/(1.5**word.count(l)) for l in word]
        return sum([letter_stats[word[i]] * multiplier[i] for i in range(len(word))])

    def process_word_strat1(self, word, letter_stats):
        # Straight addition of word frequency
        # generally bad, words like "whooo" come up a lot just because
        # of vowel frequency.
        return sum([letter_stats[word[i]] for i in range(len(word))])