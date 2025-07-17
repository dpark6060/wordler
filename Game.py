import copy

from src import Utils, Stats, Rules, WordGuess, Suggestor

import logging

logging.basicConfig(level="INFO")
log = logging.getLogger()
WOI = "pious"
debug_WOI = True

class Game:
    def __init__(self, practice: bool = False, remove_previous_wordles: bool = False, remove_plural: bool = False, remove_past_tense: bool = False, remove_un: bool = False):
        """ The main game object

        Args:
            practice: if True, won't ask you to add the correct word to the correct wordle list
            remove_previous_wordles: if True, do not consider previous wordle words for solutions
            remove_plural: if True, remove all wornds ending in "s", excluding "ss" words
            remove_past_tense: if True, remove all words ending in "ed"
        """

        self.remove_previous_wordles = remove_previous_wordles
        self.remove_plural = remove_plural
        self.remove_past_tense = remove_past_tense
        self.remove_un = remove_un
        self.practice = practice

        self.rule_maker = WordGuess.GuessRules()
        self.word_list = self.init_wordlist()
        self.full_word_list = copy.deepcopy(self.word_list)
        self.stat_calc = Stats.LetterStats.init_and_calc(self.word_list)
        self.word_stat_calc = Stats.WordStats(self.stat_calc.letter_prob, self.stat_calc.bigram_prob)
        self.suggestor = Suggestor.Suggestor()
        self.unknown_letters = [a for a in "abcdefghijklmnopqrstuvwxyz"]

        self._play = True

    def _check_woi(self) -> None:
        """ For debugging, check on the presence of a word in the list.
        """
        if not debug_WOI:
            return
        print(f"{WOI} in list: {WOI in self.word_list}")

    def init_wordlist(self) -> list[str]:
        """ Initialize the word list
        """
        my_word_list = copy.deepcopy(Utils.get_word_list(remove_previous_wordles=self.remove_previous_wordles, remove_plural=self.remove_plural, remove_past_tense=self.remove_past_tense, remove_un=self.remove_un))
        return my_word_list

    def get_guess(self) -> WordGuess.WordGuess:
        """ capture a new guess from the user

        Returns:
            the guess object

        """
        return WordGuess.WordGuess()

    def process_guess(self, guess: WordGuess) -> None:
        """ process the guess.

        Converts the guess into a list of rules and then applies those rules to the current word list

        Args:
            guess: the guess to filter the word list with

        """
        log.debug('making rules')
        rules = self.rule_maker.guess_to_rules(guess)
        self.update_letters(guess)
        log.debug('done')
        self._check_woi()
        self.word_list = Rules.evaluate_rules_in_list(self.word_list, rules)
        self._check_woi()

    def update_letters(self, guess: WordGuess):
        for letter in guess.letters:
            if letter in self.unknown_letters:
                self.unknown_letters.remove(letter)

    def is_game_won(self):
        """ Checks to see if we've won the game.

        The game is won if there's only one word left in the list.

        Returns:
            True if won, False otherwise

        """
        if len(self.word_list) == 1:
            return True
        return False

    def get_winning_word(self) -> str:
        """ Returns the winning word
        """
        if len(self.word_list) != 1:
            raise Exception("Game is not won!")
        return self.word_list[0]

    def add_word_to_wordle(self) -> None:
        """ Adds the winning word to the list of wordle solutions.

        Has to check if there's only one solution left because we want the word
        even if the user lost, in which case we need to ask for them to enter it.
        """
        if self.practice:
            return

        add = input("Add word to wordle list? (Y/n)")
        if add != "Y":
            return

        if len(self.word_list) == 1:
            word = self.word_list[0]
        else:
            word = input("what was the word?")
        Utils.add_wordle(word)

    def ask_play_again(self) -> None:
        """ Asks the user if they want to play again and resets if yes
        """
        start_over = input("Play Again? (Y/n)")
        if start_over == "n":
            self._play = False
        else:
            self.word_list = self.init_wordlist()

    def win_state(self) -> None:
        """ Actions to perform if the user wins
        """
        log.info("Congrats!")
        word = self.get_winning_word()
        log.info(f"Word is {word}")
        self.end_state()

    def lose_state(self) -> None:
        """ Actions to perform if the user loses
        """
        log.info("womp womp")
        self.end_state()

    def end_state(self) -> None:
        """ Actions that are carried out at the end of game, regardless of state

        """
        self.add_word_to_wordle()
        self.ask_play_again()

    def display_word_suggestions(self) -> None:
        """ Display remaining possible words with an estimated likelihood.

        Currently, likelihood is just the amount of common letters in each word.

        """
        log.debug("Calculating stats")
        guess_words, guess_vals = self.suggestor.suggest(self.word_list, self.unknown_letters)
        log.debug('done')
        Utils.display_choices(guess_words, guess_vals)

    def play(self) -> None:
        """ Executes the game

        """
        while self._play:

            for i in range(6):
                log.info(f"{len(self.word_list)} possibilities")
                guess = self.get_guess()
                self.process_guess(guess)
                if self.is_game_won():
                    self.win_state()
                    break
                self.display_word_suggestions()

            if len(self.word_list) > 1:
                self.lose_state()




if __name__ == "__main__":
    game = Game(remove_previous_wordles=True,remove_plural=True, remove_un=True)
    game.play()
