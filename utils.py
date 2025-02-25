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
    random.shuffle(word_list)
    return ''.join(word_list)


    # if __name__ == "__main__":
    #     deck = generate_9_letters(normalized)
    #     print("Selected 9 letters:", deck)