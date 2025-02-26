"""Class for the conundrum game"""

# import random

import numpy as np
import nltk
# from nltk.corpus import words

from utils import scramble_word
from lettersgame import LettersGame

class ConundrumGame:
    def __init__(self, word_list=None, original_word=None, timer=45,
                    n_letters=9):
        """Conundrum game class for the Countdown game.

        Rules: an n-level word is scrambled and the player has to guess
            the original word in time allocated.

        Args:
            word_list (list): List of words to use in the game.
            original_word (str): Original word to guess.
            timer (int): Time limit in seconds.
            n_letters (int): Number of letters in the word.

        """
        self.rng = np.random.default_rng()
        self.n_letters = n_letters
        # This needs to be long list of 9-letter words
        self.word_list = word_list if (word_list is not None
                        ) else self.generate_wordlist()
        self.original_word = self.generate_word() if (
                    original_word is None) else original_word
        self.scrambled_word = scramble_word(self.original_word)
        self.timer = timer  # seconds

    def check_answer(self, answer):
        if answer.upper() == self.original_word:
            return True, "Correct!"
        else:
            return False, "Incorrect, try again."

    def generate_word(self):
        """Generate a word of n_letters length."""
        return self.rng.choice(self.word_list).upper()

    def generate_wordlist(self):
        """Generate a list of n-letter words using NLTK."""
        nltk.download('words')  # Only needed once
        word_list = nltk.corpus.words.words()
        return [word.upper() for word in word_list if len(word) == self.n_letters]

# A quick test
if __name__ == "__main__":
    game = ConundrumGame()
    print(f"Scrambled: {game.scrambled_word}")
    print(f"Original: {game.original_word}")
    print(game.check_answer(game.original_word)[1])
    print("This word means:", LettersGame.get_word_definition(game.original_word))
