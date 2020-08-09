############################################################
# FILE : ex7.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex7 2020
# DESCRIPTION: Several recursion problems
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################


def print_to_n(n):
    """ Print all numbers from 1 to n """
    # Base case is n < 1, in which case nothing happens
    # While n >= 1, recursion occurs
    if n >= 1:
        # Print previous number first
        print_to_n(n - 1)
        # Print this number
        print(n)


def digit_sum(n):
    """ Return the sum of the digits of n """
    # Base case - n is between 0 to 9
    if n // 10 == 0:
        return n % 10
    # Recursion step - add the last digit and
    # compute digit sum for the number divided by 10
    else:
        return digit_sum(n // 10) + n % 10


def is_prime(n):
    """ Return whether n is prime """
    # If n <= 1, n is not prime
    if n <= 1:
        return False
    # If n > 1, call a helper method to check if it is prime
    return not has_divisor_smaller_than(n, n // 2)


def has_divisor_smaller_than(n, i):
    """ Check if n is divisible by any number from 1 to i """
    # Base case - i gets all the way down to 1, so n is prime
    if i == 1:
        return False
    # Base case - n is divisible by some i, so it is not prime
    elif n % i == 0:
        return True
    # Recursion step - if n is not divisible by
    # current i, check if it is divisible by i - 1
    else:
        return has_divisor_smaller_than(n, i - 1)


def play_hanoi(hanoi, n, src, dst, temp):
    """ Move the tower of Hanoi from src to dst """
    # Base case - non-positive n, do nothing
    if n <= 0:
        return
    # Base case - move one disk from src to dst
    if n == 1:
        hanoi.move(src, dst)
    else:
        # Recursion, move top n-1 disks from src to temp
        play_hanoi(hanoi, n - 1, src, temp, dst)
        # Move the nth disk to dst
        hanoi.move(src, dst)
        # Recursion, move the n-1 disks from temp to dst
        play_hanoi(hanoi, n - 1, temp, dst, src)


def print_sequences(char_list, n):
    """ Print every sequence of n characters from char_list"""
    # Non-positive n, print empty string
    if n <= 0:
        print()
    # Print every sequence returned from helper function
    else:
        for sequence in get_endings(char_list, n):
            print(sequence)


def get_endings(char_list, n):
    """ Return every sequence of n characters from char_list """
    # Base case - n = 1, return char_list
    if n == 1:
        return char_list
    else:
        # Recursion - get endings for n - 1
        ends = get_endings(char_list, n - 1)
        lst = []
        # Add a character to the front of every
        # item in ends, and put the new item in lst
        for char in char_list:
            for ending in ends:
                lst.append(char + ending)
        # Return list of all possible n-character
        # strings from char_list
        return lst


# What about char_list = [a,b,c] n = 5???
def print_no_repetition_sequences(char_list, n):
    """ Print every sequence of n characters
    with no repetition from char_list"""
    # Non-positive n, print empty string
    if n <= 0:
        print()
    # Print every sequence returned from helper function
    else:
        for sequence in get_no_repetition_endings(char_list, n):
            print(sequence)


def get_no_repetition_endings(char_list, n):
    """ Return every sequence of n characters
    without repetition from char_list """
    # Base case - n = 1, return char_list
    if n == 1:
        return char_list
    else:
        lst = []
        for index, char in enumerate(char_list):
            # Recursion - get endings for n - 1 where
            # char_list does not have the last character used
            ends = get_no_repetition_endings(
                char_list[:index] + char_list[index + 1:], n - 1)
            # Add the current character to every ending in the ends list
            for ending in ends:
                lst.append(char + ending)
        # Return list of all possible n-character
        # strings from char_list with no repeats
        return lst


def parentheses(n):
    """ Get every valid sequence of n pairs of parentheses
     where ( always comes before ) in each pair"""
    # Non-positive n, return empty string
    if n <= 0:
        return ['']
    # Return every sequence from helper function
    else:
        return parentheses_sequences('(', n - 1, 1)


def parentheses_sequences(last_char, num_open, num_close):
    """ Return all parentheses sequences where there
    are num_open ( left and num_close ) left """
    ends = []
    # If less than n parentheses have been opened, get all
    # possibilities where the next char is an open parenthesis
    if num_open > 0:
        ends += parentheses_sequences('(', num_open - 1, num_close + 1)
    # If not all open parentheses have been closed, get all
    # possibilities where the next char is a closed parenthesis
    if num_close > 0:
        ends += parentheses_sequences(')', num_open, num_close - 1)
    # Base case - there have been n pairs of parentheses
    # Return last character
    if len(ends) == 0:
        return [last_char]
    # Otherwise, return all endings from
    # ends, with last_char put in front
    else:
        for ind, end in enumerate(ends):
            ends[ind] = last_char + end
        return ends


def flood_fill(image, start):
    """ Fill start point with * and every . surrounding it """
    # Unpack tuple start
    row, col = start
    # Base case - the current point is *, no more filling
    if image[row][col] == '*':
        return
    # Otherwise, change current point from . to *
    # and fill every adjacent point
    else:
        image[row][col] = '*'
        if row - 1 >= 0:
            flood_fill(image, (row - 1, col))
        if col - 1 >= 0:
            flood_fill(image, (row, col - 1))
        if row + 1 < len(image):
            flood_fill(image, (row + 1, col))
        if col + 1 < len(image[0]):
            flood_fill(image, (row, col + 1))