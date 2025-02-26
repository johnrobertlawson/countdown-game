import os

# from countdowngui import CountdownGUI
from lettersgame import LettersGame
from numbersgame import NumbersGame
from conundrumgame import ConundrumGame
from utils import validate_word, scramble_word

def run_cli_version():
    """Run the CLI version of the Countdown game.

    This is more useful to test it works without testing GUI.
    """
    # This will take us through a whole game. I want this working on
    # the command line first before moving to the GUI.

    # First, one letters game each for the two players
    # The only difference is the player of that round gets to choose
    # "vowels or consonant" one by one as they see the set revealed.
    # The sampling deck is infinite but no letter can appear more than once.

    ######### OPTIONS #############
    timer = 45 # 45 second to reduce stress!


    ########## START ############
    scores = {"player1": 0, "player2": 0}

    # Keyboard entry on CLI to overwrite player names
    question = "Do you want to use default player names? (y/n): "
    default_names = input(question).lower() == "y"
    if not default_names:
        player1 = input("Enter player 1 name: ")
        player2 = input("Enter player 2 name: ")
    else:
        player1 = "Player 1"
        player2 = "Player 2"
    print(f"Welcome to Countdown, {player1} and {player2}!")

    ### GAME 1 - PLAYER 1 CHOOSES
    LG1 = LettersGame()
    # Player 1 chooses the letters
    # Need GUI that shows the list so far so player is informed to choose next
    # Sabotage is possible by choosing all vowels or all consonants

    ### Game 2 - PLAYER 2 CHOOSES
    LG2 = LettersGame()


    ### Game 3 - NUMBERS GAME, PLAYER 1
    NG1 = NumbersGame()
    # Player 1 chooses from 'top' (large numbers in [25, 50, 75, 100]) and
    # "bottom" (1-10) numbers. They can choose 0-4 large numbers. Most players
    # go for 1-2. Sabotage is possible by choosing 4 large numbers.

    ########## Halfway ################
    # Shoer iintermission, maybe "easier" conundrum game for crowd to play

    ### Game 4 - SECOND LETTERS GAME, PLAYER 2
    LG3 = LettersGame()

    ### Game 5 - SECOND LETTERS GAME, PLAYER 1
    LG4 = LettersGame()

    ### Game 6 - NUMBERS GAME, PLAYER 2
    NG2 = NumbersGame()


def main():
    # This will take us through a whole game. I want this working on
    # the command line first before moving to the GUI.

    # First, one letters game each for the two players
    # The only difference is the player gets to choose "vowels or consonant"
    # one by one as they see the set revealed

    ######### OPTIONS #############
    timer = 45 # 45 second to reduce stress!


    ########## KICK OFF ############
    scores = {"player1": 0, "player2": 0}

    # Keyboard entry on CLI to overwrite player names
    question = "Do you want to use default player names? (y/n): "
    default_names = input(question).lower() == "y"
    if not default_names:
        player1 = input("Enter player 1 name: ")
        player2 = input("Enter player 2 name: ")
    else:
        player1 = "Player 1"
        player2 = "Player 2"
    print(f"Welcome to Countdown, {player1} and {player2}!")

    ### GAME 1 - PLAYER 1 CHOOSES
    LG1 = LettersGame()
    # Player 1 chooses the letters
    # Need GUI that shows the list so far so player is informed to choose next
    # Sabotage is possible by choosing all vowels or all consonants

    ### Game 2 - PLAYER 2 CHOOSES
    LG2 = LettersGame()


    ### Game 3 - NUMBERS GAME, PLAYER 1
    NG1 = NumbersGame()
    # Player 1 chooses from 'top' (large numbers in [25, 50, 75, 100]) and
    # "bottom" (1-10) numbers. They can choose 0-4 large numbers. Most players
    # go for 1-2. Sabotage is possible by choosing 4 large numbers.

    ########## Halfway ################
    # Shoer iintermission, maybe "easier" conundrum game for crowd to play

    ### Game 4 - SECOND LETTERS GAME, PLAYER 2
    LG3 = LettersGame()

    ### Game 5 - SECOND LETTERS GAME, PLAYER 1
    LG4 = LettersGame()

    ### Game 6 - NUMBERS GAME, PLAYER 2
    NG2 = NumbersGame()

    # The winner will play conundrum game
    # The conundrum game is a 9-letter word that is scrambled
    # The player has 45 seconds to guess the word
    # If they get it right, they add the points to their total based on
    # seconds left on the clock when they guessed it.
    # If they get it wrong, they get no points but still win!

    CNx = ConundrumGame()

if __name__ == "__main__":
    main()