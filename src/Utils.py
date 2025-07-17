
import copy
from functools import cache
from pathlib import Path
import numpy as np

data_dir = Path("data")

def display_choices(words, probs):
    print(f'getting max of probs')
    max_prob = max(probs)
    normalized = [p/max_prob * 10 for p in probs]
    n_stars = np.round(normalized).astype(int)
    n_stars, words = zip(*sorted(zip(n_stars, words)))

    for word, stars in zip(words, n_stars):
        print(f"{word} {'*'*stars}")

@cache
def get_words():
    # Load the file.
    with open(data_dir / "five-letter-words.txt", 'r') as f:
        ## This includes \n at the end of each line:
        # words = f.readlines()

        # This drops the \n at the end of each line:
        words = f.read().splitlines()

    return words

@cache
def get_wordles():
    with open( data_dir / 'updated_words.txt', 'r') as f:
        ## This includes \n at the end of each line:
        # words = f.readlines()

        # This drops the \n at the end of each line:
        words = f.read().lower().split()

    return words


def add_wordle(new_word):
    wordles = get_wordles()
    if new_word in wordles:
        print("Oopsie, this is already here")
        return

    with open(data_dir / 'updated_words.txt', 'a') as f:
        f.write("\n" + new_word)


def get_word_list(remove_previous_wordles=False, remove_plural=False, remove_past_tense=False, remove_un=False):

    wordles = copy.deepcopy(get_wordles())
    words = copy.deepcopy(get_words())
    # Wordle words are only ever true five letter words.
    # They are never plurals of four letter words,
    # Nor any modified version of shorter words, e.g.
    # time -> timed would never be used as it's the past tense of a four letter word.
    # These rules are based on observation and may not strictly apply to every game.

    if remove_plural:
        plural_wordles = [w for w in wordles if w.endswith('s')]
        plural_words = [w for w in words if w.endswith('s')]
        accepted_s_words = [w for w in plural_words if w in plural_wordles or w.endswith('ss')]

        non_plurals = [w for w in words if w not in plural_words or w in accepted_s_words]
        words = non_plurals

    if remove_past_tense:
        ed_wordles = [w for w in wordles if w.endswith('ed')]
        ed_words = [w for w in words if w.endswith('ed')]
        accepted_ed_words = [w for w in ed_words if w in ed_wordles or w.endswith('eed')]
        non_eds = [w for w in words if w not in ed_words or w in accepted_ed_words]
        words = non_eds

    if remove_previous_wordles:
        words = [w for w in words if w not in wordles]
    
    if remove_un:
        words = [w for w in words if not w.startswith("un")]

    

    return words

# words = get_words()
# wordles = get_wordles()
