############################################################
# FILE : car.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex9 2020
# DESCRIPTION: A class representing a car object
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES:
############################################################


class Car:
    """
    The Car class holds properties about each car object,
    allowing the game to know its location and possible moves.
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
        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coordinates = []
        # Are coordinates horizontal or vertical
        change = (1, 0) if self.orientation == self.VERTICAL else (0, 1)

        loc = self.location
        # Iterate through length of car and add car positions
        for i in range(self.length):
            coordinates.append(loc)
            loc = loc[0] + change[0], loc[1] + change[1]

        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        # Create a dictionary
        move_dict = {}

        # Vertical car can move up and down
        if self.orientation == self.VERTICAL:
            move_dict['u'] = self.DESCRIPTION_UP
            move_dict['d'] = self.DESCRIPTION_DOWN

        # Horizontal car can move left and right
        else:
            move_dict['l'] = self.DESCRIPTION_LEFT
            move_dict['r'] = self.DESCRIPTION_RIGHT

        # Return dictionary
        return move_dict

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for
        this move to be legal.
        """
        # Create list of cell locations
        loc = []
        change = self.movekey_change(movekey)

        # If change will start at upper left corner
        if movekey in 'ul':
            # Get top left corner
            row, col = self.location
            # Add the change
            row, col = row + change[0], col + change[1]
            loc.append((row, col))

        # If change will be in lower right corner
        elif movekey in 'dr':
            # Get bottom right corner
            car_coord = self.car_coordinates()
            row, col = car_coord[len(car_coord) - 1]
            # Add the change
            row, col = row + change[0], col + change[1]
            loc.append((row, col))

        return loc

    @staticmethod
    def movekey_change(movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: Tuple representing the coordinate change in that direction
        """
        num = 1
        if movekey in 'ul':
            num = -1
        if movekey in 'ud':
            return num, 0
        else:
            return 0, num

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # Movekey not allowed
        if movekey not in self.possible_moves():
            return False

        # Get car's location
        row, col = self.location
        # Get change in location
        change = self.movekey_change(movekey)
        # Update location
        self.location = row + change[0], col + change[1]

        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name
