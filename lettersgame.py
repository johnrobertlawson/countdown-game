"""Countdown Letters Game.

The round goes as follows:
1. Nine letters are chosen by the player (passed into init)
    a. These can be randomly chosen if not specified...
2. The player has timer seconds to find the longest word possible. The minimum
    word length is set by "
3. At the end, each player gives their answer
4. If the word is valid (in the nltk dictionary) then the player
    with the longest word gets the points where 1 letter = 1 point.
    A tie sees both players get the points.
5. The "dictionary corner" player also gives their answer. The top three
    words are shown to the players (by percentile/length). Also, each player is
    told how good their answer is at the percentile of all possible words.

In terms of how the script works when initialised:

"""

import os

import numpy as np
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

from letterdeck import LetterDeck

class LettersGame:
    def __init__(self, dictionary=None, letters=None, timer=45,
                    min_word_length=4, auto_pick=False):
        """Letters game class for the Countdown game.

        TODO: if letters is none, generate
        """
        self.min_word_length = min_word_length
        self.dictionary = dictionary
        self.rng = np.random.default_rng()

        if letters is not None:
            self.letters = letters
        elif auto_pick:
            self.letters = self.generate_letter_set()
        else:
            # This means this will be filled by a human via keyboard input
            self.letters = []

        self.timer = timer
        self.deck = LetterDeck(power=0.5)

    def pick_letters(self):
        counts = {}
        chosen_letters = []
        target_count = 9

        print("Welcome to the Countdown Letter Picker!")
        print("You will choose 9 letters by specifying 'vowel' or 'consonant' each time.")
        print("Note: No letter can appear more than twice.\n")

        while len(chosen_letters) < target_count:
            print("Current letters:", " ".join(chosen_letters))
            choice = input("Choose (v)owel or (c)onsonant: ").strip().lower()

            # Validate the input
            if choice not in ("v", "c"):
                print("Invalid input. Please type 'v' for vowel or 'c' for consonant.\n")
                continue

            try:
                if choice == "v":
                    letter = self.deck.pick_vowel(counts)
                else:  # choice == "c"
                    letter = self.deck.pick_consonant(counts)
                chosen_letters.append(letter)
                counts[letter] = counts.get(letter, 0) + 1
                print(f"You picked: {letter}\n")
            except ValueError as e:
                print("Error:", e)
                continue

        print("Final set of letters:", " ".join(chosen_letters))
        # Controversial move here:
        self.letters = chosen_letters
        return chosen_letters

    def generate_letters(self, letters=True):
        """Generate letters for the game.

        Args:
            letters (bool): Generate letter set
        """
        letters_val = self.generate_letter_set() if letters else None
        return letters_val, None

    def generate_letter_set(self, num_letters=9):
        """Generate a set of letters based on vowel and consonant distribution."""
        vowels = np.array(list("AEIOU"))
        consonants = np.array(list("BCDFGHJKLMNPQRSTVWXYZ"))

        num_vowels = self.rng.integers(2, 4)
        num_consonants = num_letters - num_vowels

        vowel_picks = self.rng.choice(vowels, size=num_vowels,
                                      replace=True)
        consonant_picks = self.rng.choice(consonants,
                                size=num_consonants, replace=True)

        letters = np.concatenate([vowel_picks, consonant_picks])
        self.rng.shuffle(letters)
        return letters.tolist()

    def start_round(self):
        """Start a new round by generating new letters."""
        self.letters, _ = self.generate_letters()

    def check_answer(self, word):
        """Check if a word is valid given the current letters and dictionary.

        Args:
            word (str): Word to check
        """
        # First check if word can be made from available letters
        letter_counts = {}
        for letter in self.letters:
            letter_counts[letter] = letter_counts.get(letter, 0) + 1

        word_upper = word.upper()
        for letter in word_upper:
            if letter not in letter_counts or letter_counts[letter] == 0:
                return False, f"'{word}' cannot be made from available letters"
            letter_counts[letter] -= 1

        # Then check if word exists in dictionary
        if word_upper in self.dictionary:
            return True, f"Valid word: {word}"
        return False, f"'{word}' not found in dictionary"

    def validate_word(self, word):
        """Validate if the word exists in the provided dictionary."""
        return word.upper() in self.dictionary

    def get_valid_words(self, sort_by=None):
        try:
            nltk.data.find('corpora/words')
        except LookupError:
            nltk.download('words')

        english_words = set(word.upper() for word in nltk.corpus.words.words())

        # Filter valid words
        possible_words = []
        for word in english_words:
            if len(word) >= self.min_word_length:
                letter_counts = self.letters.copy()
                can_make = True
                for letter in word:
                    if letter not in letter_counts or letter_counts.count(letter) == 0:
                        can_make = False
                        break
                    letter_counts.remove(letter)
                if can_make:
                    possible_words.append(word)

        if sort_by == "length":
            possible_words.sort(key=len, reverse=True)

        return possible_words

    def generate_human_guess(self, skill_level=0.5,
                                    percentile_range=0.2):
        """Generate a single word guess based on skill level.

        Args:
            skill_level (float): 0-1, determines word length percentile target
            min_letters (int): Minimum word length to consider
            percentile_range (float): Range around skill level for randomization

        Returns:
            str: A single word guess
        """
        possible_words = self.get_valid_words(sort_by="length")

        # Calculate range bounds
        min_percentile = max(0.0, skill_level - percentile_range/2)
        max_percentile = min(1.0, skill_level + percentile_range/2)

        # Random percentile within range
        actual_percentile = self.rng.uniform(min_percentile, max_percentile)

        # Select word at that percentile
        index = int(len(possible_words) * actual_percentile)

        # TODO: find optimal word to show as "dictionary corner" best answer.

        return possible_words[index]

    def dictionary_corner(self):
        """Generate the best possible word from the letters.

        TODO: it would be cool to have the word's meaning
        print(word.definition()), apparently.
        """
        # Find possible words from the self.letters
        # Sort by length
        possible_words = self.get_valid_words(sort_by="length")

        # Max length word
        max_len = len(possible_words[0])

        # How many had that length?
        max_len_count = sum(len(word) == max_len for word in possible_words)

        print(f"The longest word possible is {max_len} letters long.")
        print(f"There are {max_len_count} words of that length.")
        print(f"The longest word is: {possible_words[0]}.")
        print(f"This word means: {self.get_word_definition(possible_words[0])}.")

        print("The second and third longest words are:")
        print(f"2. {possible_words[1]}, meaning: {self.get_word_definition(possible_words[1])}")
        print(f"3. {possible_words[2]}, meaning: {self.get_word_definition(possible_words[2])}")

        # return possible_words[0]
        return

    @staticmethod
    def get_word_definition(word):
        syns = wordnet.synsets(word)
        try:
            definition = syns[0].definition()
        except IndexError:
            definition = "...actually, no definition found."
        return definition

    @staticmethod
    def determine_point_dividend(player1, player2):
        """Determine the points to award each player based on word length.

        Args:
            player1 (str, int): Player 1 word or its length
            player2 (str, int): Player 2 word or its length
        """
        players = {1: 0, 2: 0}

        if isinstance(player1, str):
            players[1] = len(player1)
            players[2] = len(player2)
        elif isinstance(player1, int):
            players[1] = player1
            players[2] = player2
        else:
            raise ValueError("Invalid input types.")

        if players[1] > players[2]:
            return players[1], 0
        elif players[1] < players[2]:
            return 0, players[2]
        elif players[1] == players[2]:
            return players[1], players[2]
        else:
            return 0, 0



if __name__ == "__main__":
    LG = LettersGame(auto_pick=True)

    print("Starting new game with AI players...")
    print(f"Letters generated: {' '.join(LG.letters)}")

    print("Start timer")
    # TODO - add timer functionality as function, 45 sec usually

    print(f"First player guess: {(player1_guess := 
                    LG.generate_human_guess(skill_level=0.55))}")
    print("This word means:", LG.get_word_definition(player1_guess))
    print(f"Second player guess: {(player2_guess := 
                    LG.generate_human_guess(skill_level=0.92))}")
    print("This word means:", LG.get_word_definition(player2_guess))

    LG.dictionary_corner()

    scores = LG.determine_point_dividend(player1_guess, player2_guess)
    print(f"Player 1 score: {scores[0]}    Player 2 score: {scores[1]}")


