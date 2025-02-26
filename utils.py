import random

def validate_word(word, dictionary):
    """
    Validate if the word exists in the provided dictionary.
    """
    return word.upper() in dictionary

def scramble_word(word):
    """
    Return a scrambled version of the input word.
    """
    word_list = list(word)
    while list(word) == word_list:
        random.shuffle(word_list)
    return ''.join(word_list)
