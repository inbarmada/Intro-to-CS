############################################################
# FILE : game.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex9 2020
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES:
############################################################
import sys
import helper
from car import Car
from board import Board


class Game:
    """
    Add class description here
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        self.board = board

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        print(self.board.possible_moves())

        user_input = input('Type your move | car_name,movekey : ')
        # Make sure it's a valid input
        while ',' not in user_input and user_input != '!':
            print('Invalid input')
            user_input = input()

        # Check if user wants to end game
        if user_input == '!':
            return False

        # If not, get car and move from user
        c, d = user_input.split(',')

        self.board.move_car(c, d)
        return True



    def get_cars(self, json_file):
        car_dict = helper.load_json(json_file)
        for c in car_dict.keys():
            val = car_dict[c]
            if val[0] > 0:
                c = Car(c, val[0], tuple(val[1]), val[2])
                self.board.add_car(c)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print(self.board)

        target = self.board.target_location()
        while self.__single_turn() and self.board.cell_content(target) is None:
            print(self.board)

        if self.board.cell_content(target) is not None:
            print(self.board)
            print('YOU WONNNNNN!!!!!!')


if __name__== "__main__":
    json_file = sys.argv[1]
    b = Board()
    game = Game(b)
    game.get_cars(json_file)
    game.play()


