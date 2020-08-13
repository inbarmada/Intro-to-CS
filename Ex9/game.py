############################################################
# FILE : game.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex9 2020
# DESCRIPTION: A class representing the game rush hour
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
    The Game class runs the game rush hour.
    It stores the board and handles user input and prints.
    """
    WIN_MESSAGE = 'Great job! You won!!!'

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board
        self.reprint_board = True

    def __single_turn(self):
        """
        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.
        """
        # Get move from user
        user_input = input('Type your move | car_name,movekey : ')

        # Make sure input is valid
        while ',' not in user_input and user_input != '!':
            print('Invalid input. Try again')
            user_input = input()

        # Check if user wants to end game
        if user_input == '!':
            return False

        # If not, get car and move from user
        c, d = user_input.split(',')

        # Move the cars as user requested.
        # If the move was successful, reprint the board to
        # show change. Otherwise simply ask for a new input
        self.reprint_board = self.board.move_car(c, d)
        return True

    def print_game_info(self):
        """
        Print board and possible moves
        """
        # Print board
        print(self.board)

        # Print moves
        print('Moves allowed: ')
        for move in self.board.possible_moves():
            print(move)

        print()

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # Print board and moves
        self.print_game_info()

        # Get target location
        target = self.board.target_location()

        # Continue playing so long as the player didn't win or end the game
        while self.__single_turn() and self.board.cell_content(target) is None:
            # If move was successful, print the change
            if self.reprint_board:
                # Print board and moves
                self.print_game_info()

        # If the player won, print the board and print a win message
        if self.board.cell_content(target) is not None:
            print(self.board)
            print(self.WIN_MESSAGE)


if __name__ == "__main__":
    # Get json file from sys argv
    json_file = sys.argv[1]

    # Create a board
    b = Board()
    # Get legal locations on board
    board_locations = b.cell_list()

    # Add cars from json file to board
    car_dict = helper.load_json(json_file)
    # For each car in the json file
    for car_name in car_dict.keys():
        # Get values of the car
        val = car_dict[car_name]

        # Check if car values are valid
        if val[0] > 0:
            location = tuple(val[1])
            if location in board_locations:
                # Create car and add to board
                car = Car(car_name, val[0], location, val[2])
                b.add_car(car)

    # Create game
    game = Game(b)
    # Begin playing
    game.play()
