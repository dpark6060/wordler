# Wordler

The wordler is a wordle guess assistant.

It's pretty dumb, but it does show you all the words you haven't eliminated, 
making this more of a strategy game and less of a "Do you have the most words memorized" game.

People with great memories over there be calling this cheating.  

You think the rocket scientists at NASA never consult a reference table?  Life's not about memorizing things,
It's about developing a strategy to succeed. 

## Use

Just run Game.py with python 3.9 or greater. 

It will prompt you for your first guess.
Enter your guess in wordle, then enter your guess in the terminal.
It will them prompt you for the colors of your guess.

When prompted for the colors, enter the color that each tile got in your guess.

- `b` : Black tile, incorrect letter
- `y` : Yellow tile, letter is present but not in the correct spot
- `g` : Green tile, letter is in the correct spot.


For example, if you guess:
![guess](./data/example_guess.jpg)

You would enter the following into your wordler:

```
enter guess: funky
enter color: bgybb
```


The wordler then provides you with a list of words that adhere to the rules
you've accumulated so far, and a probability rating.

WARNING:
 the probability is pretty unsophisticated right now. First the probability 
that a letter is in a five letter english word is calculated for all letters.
Then, the likelihood of a word is calculated by the sum of all the individual
letter's probability.

Yes, I know that's not how probability works.  Yes, I'm working on it.  
