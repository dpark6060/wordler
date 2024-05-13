from dataclasses import dataclass
from functools import cache
from typing import Union

import src.Rules as Rules

import logging
log = logging.getLogger()

@dataclass
class Code:
    correct: str = "g"
    present: str = "y"
    incorrect: str = "b"

    @classmethod
    def keys(cls):
        return [cls.correct, cls.present, cls.incorrect]

code = Code()

class WordGuess:
    """ a single guess, prompts the user to enter the letters and the tile colors of the guess

    """

    def __init__(self):
        self.letters = input("enter guess: ")
        self.lvals = input("enter color: ")
        if any([v not in Code.keys() for v in self.lvals]):
            print("Invalid colors:")
            print(
                f"{code.incorrect}: black\n{code.present}: yellow\n{code.correct}: green")

    # def get_letter_type(self, guess_type: str) -> tuple[list[str], list[int]]:
    #     """ Returns the letters who's
    #
    #     Args:
    #         guess_type:
    #
    #     Returns:
    #
    #     """
    #     if guess_type not in code:
    #         print(f"Type {guess_type} not in code {code.keys}")
    #         return [], []
    #     indexes = find_letter(self.lvals, guess_type)
    #     letters = [self.guess[i] for i in indexes]
    #     return letters, indexes

    def zip_vals(self):
        """ returns the zipped collection of letters and their tile value

        """
        return zip(self.letters, self.lvals)

    def get_letter_val(self, letter, code: Union[Code, None]=None) -> [list[int], list[str]]:
        """ given a letter, and optionally a tile value code, return the positions and tile values of that letter

        ex: if the guess is "guess", with the tiles "black", "black", "black", "green", "yellow",
        calling `get_letter_val('s')`, will return: [3,4] , ['g', 'y']

        but passing in a code to filter for will only return the positions of that letter with that code:
        calling `get_letter_val('s',Code.correct)`, will return: [3, 4] , ['g']

        Args:
            letter: the letter to find the positions and tile values of
            code: the tile value code to filter for when returning the positions of the letter.

        Returns:
            (positions, values): the positions and tile values of the guess.

        """
        if code:
            result = [(i, lval) for i, (ltr, lval) in enumerate(self.zip_vals()) if ltr == letter and lval == code]
        else:
            result = [(i, lval) for i, (ltr, lval) in enumerate(self.zip_vals()) if ltr == letter]

        if not result:
            return [], []
        return zip(*result)


class GuessRules:
    """ Given a guess and the tile values of that guess, constructs rules for the remaining words
    """
    def __init__(self):

        self.rules: list = []
        self.guess: Union[WordGuess, None] = None

    def update_guess(self, guess: WordGuess):
        self.guess = guess

    def process_guess(self):
        self.rules = []
        for letter in set(self.guess.letters):
            self.update_correct_rules(letter)
            self.update_present_rules(letter)
            self.update_incorrect_rules(letter)
        print(self.rules)

    def guess_to_rules(self, guess: WordGuess):
        self.update_guess(guess)
        self.process_guess()
        return self.rules

    def get_positions(self, letter, code):
        """ Get the positions of a letter that got a given code.
        """
        positions, _ = self.guess.get_letter_val(letter, code)
        return positions

    def _n_codes(self, letter, code):
        """ returns the number of codes a certain letter got.

        For example, asking for letter "g" and code "correct" returns the number of
        g's that were correct in this guess

        Args:
            letter: the letter to search for
            code: the code to search for

        Returns:
            the number of times that letter got that code.

        """
        positions = self.get_positions(letter, code)
        return len(positions)

    def update_correct_rules(self, letter):
        """ Rules to apply for letters with green tiles.
        """
        log.debug(f"setting correct rules for letter {letter}")

        # Rule 1: is there a green?
        correct_positions = self.get_positions(letter, Code.correct)
        # Skip if nothing present
        if len(correct_positions) == 0:
            log.debug(f"No correct positions for {letter}")
            return

        # If we have a green and a black, the letter is ONLY in one place.

        if self._n_codes(letter, Code.incorrect) > 0:
            log.debug(f"Found an incorrect code for correct letter {letter}")
            # We only apply this rule
            self.rules.append(Rules.IsOnlyAt(letter, correct_positions))

        else:
            # Otherwise we have a green and NO black, all we can do is say it is at this spot
            self.rules.append(Rules.IsAt(letter, correct_positions))

    def update_present_rules(self, letter):
        """ Rules to apply for letters with yellow tiles
        """
        log.debug(f"setting present rules for letter {letter}")

        # Now we tackle yellow:
        present_positions = self.get_positions(letter, Code.present)
        if len(present_positions) == 0:
            return

        # If we have X yellow tiles of this letter, AND a black, we know there is ONLY X of this letter present
        if self._n_codes(letter, Code.incorrect) > 0:
            self.rules.append(Rules.IsOnlyNOf(letter, present_positions))

        # I think that's  the only special rule.  Otherwise we get our normal IsPresent rule,
        # which always gets added regardless of special cases above
        self.rules.append(Rules.IsPresent(letter, present_positions))

    def update_incorrect_rules(self, letter):
        """ Rules to apply for letters with black tiles
        """
        log.debug(f"setting incorrect rules for letter {letter}")
        incorrect_positions = self.get_positions(letter, Code.incorrect)
        if len(incorrect_positions) == 0:
            return

        # If there are NO green or NO yellow tiles of the same letter in this guess, we can say for sure
        # that not only is the letter not at that spot, but it is also not present in the world at all.
        present_positions = self.get_positions(letter, Code.present)
        correct_positions = self.get_positions(letter, Code.correct)
        if len(present_positions) == 0 and len(correct_positions) == 0:
            self.rules.append(Rules.IsNotIn(letter))
        else:
            # otherwise all we can say is that the letter is not at this location.
            self.rules.append(Rules.IsNotAt(letter, incorrect_positions))



def find_letter(string, char):
    return [i for i, ltr in enumerate(string) if ltr == char]
