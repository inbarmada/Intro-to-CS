############################################################
# FILE : board.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex9 2020
# DESCRIPTION: A class representing a board object for
#              the game rush hour
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES:
############################################################


class Board:
    """
    The Board class holds a matrix that represents
    the board game, with cars sitting in different
    positions on it. It holds a list of all the
    cars. It also handles all interaction between
    the Game and individual Car objects.
    """
    EXIT_LOCATION = (3, 7)
    DUPLICATE_CAR_NAME_MSG = 'Car name already in use.'
    DUPLICATE_CAR_MSG = 'Car already exists.'
    ILLEGAL_LENGTH_MSG = 'Illegal length - non-positive number.'
    COORDINATE_OUTSIDE_MSG = 'Illegal coordinate - outside board'
    COORDINATE_TAKEN_MSG = 'Illegal coordinate - another car ' \
                           'is already in this position'
    CAR_DOES_NOT_EXIST_MSG = 'Car does not exist'
    INVALID_MOVE_MSG = 'Invalid move'
    MOVE_OUTSIDE_MSG = 'Illegal move - outside board'
    MOVE_TAKEN_MSG = 'Illegal move - another car is already in this position'
    
    def __init__(self):
        """
        A constructor for the board object
        """
        # Build board matrix
        self.board = []
        for i in range(7):
            self.board.append(['_'] * 7)

        # Add exit location to the board
        self.board[3].append('_')

        # Create an empty list for storing cars
        self.car_list = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        board_string = ''
        for row in self.board:
            for cell in row:
                board_string += cell
            board_string += '\n'
        return board_string

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        cells = []
        # Iterate over board and add all coordinates to list
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                cells.append((i, j))
        return cells

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        move_list = []

        # Iterate through the cars in the car list
        for car_name in self.car_list.keys():
            car = self.car_list[car_name]
            possible_moves = car.possible_moves()

            # Iterate over each car's possible moves
            for move_key in possible_moves:
                # Get the coordinate that must be empty for the move to work
                new_loc = car.movement_requirements(move_key)[0]
                # Check if the coordinate is on the board and is empty
                if new_loc in self.cell_list() and \
                        self.cell_content(new_loc) is None:
                    # Add the move to the list
                    move_tup = car_name, move_key, possible_moves[move_key]
                    move_list.append(move_tup)

        # Return list of moves
        return move_list

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
        filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return self.EXIT_LOCATION

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row, col = coordinate
        val = self.board[row][col]
        # If coordinate contains a car, return the car name
        if val != '_':
            return val
        # Otherwise return None
        else:
            return None

    def check_car_validity(self, car):
        """
        Checks that car is not a duplicate, has
        a legal length
        :param car: car object of car to add
        :return: True if car is valid. False otherwise
        """
        # Car name already in use
        if car.get_name() in self.car_list:
            print(self.DUPLICATE_CAR_NAME_MSG)
            return False

        # Car is not a duplicate (in case car name was somehow changed)
        elif car in self.car_list.items():
            print(self.DUPLICATE_CAR_MSG)
            return False

        # Car length illegal
        elif car.length <= 0:
            print(self.ILLEGAL_LENGTH_MSG)
            return False

        # All valid
        return True

    def check_car_coordinates(self, car):
        """
        Checks that coordinates are on the board and currently empty.
        :param car: car object of car to add
        :return: True if coordinates are legal. False otherwise
        """
        # Check all car coordinates are valid
        for coord in car.car_coordinates():
            # Coordinate is outside the board
            if coord not in self.cell_list():
                print(self.COORDINATE_OUTSIDE_MSG)
                return False
            # Another car is already in this coordinate
            elif self.cell_content(coord):
                print(self.COORDINATE_TAKEN_MSG)
                return False
        # All valid
        return True

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Check car validity
        if not self.check_car_validity(car) or \
                not self.check_car_coordinates(car):
            return False

        # Add car to car list
        self.car_list[car.get_name()] = car

        # Add car coordinates to board
        for coord in car.car_coordinates():
            row, col = coord
            self.board[row][col] = car.get_name()

        return True

    def check_move_car(self, name, movekey):
        """
        Check validity of car and move
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True if move is valid. False otherwise
        """
        # Check that chosen car is in car_list
        if name not in self.car_list:
            print(self.CAR_DOES_NOT_EXIST_MSG)
            return False

        # Get the car
        car = self.car_list[name]

        # Check that move is valid
        if movekey not in car.possible_moves():
            print(self.INVALID_MOVE_MSG)
            return False

        # Get the coordinate that must be empty
        new_loc = car.movement_requirements(movekey)[0]

        # Check that the coordinate is on the board
        if new_loc not in self.cell_list():
            print(self.MOVE_OUTSIDE_MSG)
            return False

        # Check that the coordinate is empty
        elif self.cell_content(new_loc):
            print(self.MOVE_TAKEN_MSG)
            return False

        return car, new_loc

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # Check move validity
        check_result = self.check_move_car(name, movekey)
        if not check_result:
            return False

        # Move is valid - proceed to do it
        else:
            car, new_loc = check_result

            print('Moving the car')

            # Remove car from its previous location
            for coord in car.car_coordinates():
                self.board[coord[0]][coord[1]] = '_'

            # Move the car
            car.move(movekey)

            # Put the car in its new coordinates
            for coord in car.car_coordinates():
                self.board[coord[0]][coord[1]] = car.get_name()

            return True
