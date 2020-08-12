############################################################
# FILE : board.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex9 2020
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES:
############################################################


class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """
    EXIT_LOCATION = (3, 7)

    def __init__(self):
        self.board = []
        for i in range(7):
            self.board.append(['_'] * 7)
        self.board[3].append('_')
        self.car_list = {}
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
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
        for car_name in self.car_list.keys():
            car = self.car_list[car_name]
            possible_moves = car.possible_moves()
            for move_key in possible_moves:
                new_loc = car.movement_requirements(move_key)[0]
                if new_loc in self.cell_list() and self.cell_content(new_loc) is None:
                    move_tup = car_name, move_key, possible_moves[move_key]
                    move_list.append(move_tup)
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
        if val != '_':
            return val
        else:
            return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        if car.get_name() in self.car_list:
            print('Car name already in use')
            return False

        elif car in self.car_list.items():
            print('Car already exists')
            return False

        elif car.length <= 0:
            print('Illegal length - <= 0')
            return False

        self.car_list[car.get_name()] = car

        for coord in car.car_coordinates():
            row, col = coord
            if coord in self.cell_list() and not self.cell_content(coord):
                self.board[row][col] = car.get_name()
            else:
                print('Illegal coordinate - outside board')
                return False
        return True
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # Check that car is valid
        if name not in self.car_list:
            print('Car does not exist')
            return

        car = self.car_list[name]

        # Check that move is valid
        if movekey not in car.possible_moves():
            print('Invalid move')
            return

        new_loc = car.movement_requirements(movekey)[0]

        if new_loc not in self.cell_list():
            print(new_loc, self.cell_list())
            print('Illegal move - outside the board')
            return False

        else:
            if self.cell_content(new_loc) is None:
                print('Moving the car')
                # Nullify previous location of the car
                for coord in car.car_coordinates():
                    self.board[coord[0]][coord[1]] = '_'
                # Find the car's new location
                car.move(movekey)
                # Put the car in its new coordinates
                for coord in car.car_coordinates():
                    self.board[coord[0]][coord[1]] = car.get_name()

                # Check if won
                if new_loc == self.target_location():
                    print('You WON!!')

                return True
            else:
                return False
