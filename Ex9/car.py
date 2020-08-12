############################################################
# FILE : car.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex9 2020
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES:
############################################################


class Car:
    """
    Add class description here
    """
    VERTICAL, HORIZONTAL = 0, 1
    DESCRIPTION_UP = 'Move the car one cell up'
    DESCRIPTION_DOWN = 'Move the car one cell down'
    DESCRIPTION_LEFT = 'Move the car one cell left'
    DESCRIPTION_RIGHT = 'Move the car one cell right'

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        # implement your code and erase the "pass"
        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coordinates = []
        change = (1, 0) if self.orientation == self.VERTICAL else (0, 1)
        loc = self.location
        for i in range(self.length):
            coordinates.append(loc)
            loc = loc[0] + change[0], loc[1] + change[1]
        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        move_dict = {}
        if self.orientation == self.VERTICAL:
            move_dict['u'] = self.DESCRIPTION_UP
            move_dict['d'] = self.DESCRIPTION_DOWN
        else:
            move_dict['l'] = self.DESCRIPTION_LEFT
            move_dict['r'] = self.DESCRIPTION_RIGHT
        return move_dict

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for
        this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        loc = []
        row, col = self.location
        if movekey == 'u':
            loc = row - 1, col
        elif movekey == 'l':
            loc = row, col - 1
        else:
            car_coord = self.car_coordinates()
            row, col = car_coord[len(car_coord) - 1]
            if movekey == 'd':
                loc = row + 1, col
            elif movekey == 'r':
                loc = row, col + 1
        return [loc]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in self.possible_moves():
            return False
        cell = self.movement_requirements(movekey)[0]
        row, col = self.location
        if movekey == 'd':
            self.location = (row + 1, col)
            return True
        elif movekey in 'u':
            self.location = (row - 1, col)
            return True
        elif movekey in 'l':
            self.location = (row, col - 1)
            return True
        elif movekey in 'r':
            self.location = (row, col + 1)
            return True
        else:
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name
