import logging
from abc import ABC, abstractmethod
from typing import Union

log = logging.getLogger()


class LetterRule(ABC):
    """ Base class for letter rules.

    Rules return a callable function that evaluates itself on a word.
    """
    def __init__(self, letter: str, position: Union[list, set] = None):
        self.letter = letter.lower()

        if position is None:
            position = []
        self.position = set(position)

        self.__post_init__()

    @abstractmethod
    def __post_init__(self):
        pass

    @abstractmethod
    def get_rule(self) -> callable:
        pass

    def eval(self, word) -> bool:
        return self.get_rule()(word)


class IsNotIn(LetterRule):
    """ A rule for a letter that is not present anywhere in a word.

    This is generally a rule used for black tiles (with exceptions)

    This rule does not make assumptions about the position of the letter

    ex: a letter is guessed once in a word and the tile color is black
    """
    def __post_init__(self):
        log.debug(f"Making rule {self.letter} is not in word")

    def get_rule(self):
        def rule(word: str) -> bool:
            return self.letter not in word
        return rule

    def __str__(self):
        return f"{self.letter} is not in word"


class IsIn(LetterRule):
    """ A rule for a letter that is somewhere in a word

    This is one part of the two rules returned for a yellow tile:
        - IsIn + IsNotAt

    This rule does not make assumptions about the position of the letter

    ex: a letter is guessed once in a word and comes back yellow,
        indicating the letter is somewhere in the word.
    """
    def __post_init__(self):
        log.debug(f"Making rule {self.letter} is in word")

    def get_rule(self):
        def rule(word: str) -> bool:
            return self.letter in word
        return rule

    def __str__(self):
        return f"{self.letter} is in word"


class IsNotAt(LetterRule):
    """ A rule for a letter that is not at a specified location in a word

    This is one part of the two rules returned for a yellow tile:
        - IsIn + IsNotAt

    This rule only applies to letters in specified locations.

    ex: a letter is guessed once in a word and comes back yellow,
        indicating the letter is not at that location

    """
    def __post_init__(self):
        log.debug(f"Making rule {self.letter} is not at {self.position} word")
    def get_rule(self):
        def rule(word: str) -> bool:
            return all([word[p] != self.letter for p in self.position])
        return rule

    def __str__(self):
        return f"{self.letter} is not at {self.position}"


class IsPresent(LetterRule):
    """ A rule indicating that a letter is present in a word, but not at a certain location.

    This is generally the rule for yellow tiles, and returns the evaluation of the IsIn and IsNotAt rules

    This rule both applies to letters at specified locations, and to letters in unspecified locations.

    ex: a letter is guessed once in a word and comes back yellow,
        indicating that the letter is not at that location, and is in the word.

    """
    def __post_init__(self):
        log.debug(f"Making rule {self.letter} is present in word")

    def get_rule(self):
        isnotat = IsNotAt(self.letter, self.position).get_rule()
        isin = IsIn(self.letter, self.position).get_rule()
        def rule(word: str):
            return isnotat(word) and isin(word)
        return rule


class IsAt(LetterRule):
    """ A rule indicating that a letter is present in a word at a specified location, and may be present elsewhere.

    This is generally the rule for green tiles.

    This rule applies to certain positions, but makes no assumptions about positions not specified.

    ex: A user places a letter once in one guess, and it returns green,
        indicating that the letter is present at that location.

    """
    def __post_init__(self):
        log.debug(f"Making rule {self.letter} is at {self.position} in word")

    def get_rule(self):
        def rule(word: str) -> bool:
            return all([word[p] == self.letter for p in self.position])
        return rule

    def __str__(self):
        return f"{self.letter} is at {self.position}"


class IsOnlyAt(LetterRule):
    """ A rule indicating that a letter is present in a word, and is only present in the specified locations.

    This is another general rule for green tiles.

    This rule applies to all positions in the word.

    ex: A user places a letter twice in one guess, and one returns green while the other returns black,
        indicating that the letter only appears once at the location of the green tile.

    """
    def __post_init__(self):
        log.debug(f"Making rule {self.letter} is only at {self.position} in word")

    def get_rule(self):
        def rule(word: str) -> bool:
            should_be_letters = [w for i,w in enumerate(word) if i in self.position]
            should_not_be_letters = [w for i,w in enumerate(word) if i not in self.position]
            return all([w == self.letter for w in should_be_letters]) and all([w != self.letter for w in should_not_be_letters])
        return rule

    def __str__(self):
        return f"{self.letter} is only at {self.position}"


class IsOnlyNOf(LetterRule):
    """ A rule indicating that letter only appears N times in a word, with no care for location.

    This a rule added when a letter is placed multiple times in one guess, and one is black while others are yellow.

    ex: A user places the guess "sails", and the first s returns yellow, while the second s returns black.
        On top of the normal "is present" rules defined by the presence of the yellow tile, we also know that there
        is only one s in the word.
    """
    def __post_init__(self):
        log.debug(f"Making rule {self.letter} is only {len(self.position)} of in word")

    def get_rule(self):
        def rule(word: str) -> bool:
            return len([i for i in word if i == self.letter]) == len(self.position)
        return rule


def evaluate_rules_in_list(word_list: list[str], rules: list[LetterRule]) -> list[str]:
    """ Applies each rule to a list of words and filters out words that do not pass the rule's evaluation

    Args:
        word_list: the list of words to test the rules on
        rules: the rules to test on the word list

    Returns:
        a new, filtered word list of only words that pass the rules.

    """
    print("here")
    print(rules)
    for rule in rules:
        rule = rule.get_rule()
        log.debug(f'creating new word list for rule {rule}')
        word_list = [word for word in word_list if rule(word)]
        log.debug("done")

    return word_list

