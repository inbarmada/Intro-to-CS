############################################################
# FILE : wordsearch.py
# WRITER : Inbar Leibovich , inbarlei
# EXERCISE : intro2cse Ex5 2020
# DESCRIPTION: Word search solver
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################

import sys
import os.path
from collections import Counter
from time import time

def check_input_args(args):
    """ Check validity of input arguments"""
    msg = None
    if len(args) != 4:
        msg = "Wrong number of arguments"
    elif not os.path.isfile(args[0]):
        msg = "Word list file does not exist"
    elif not os.path.isfile(args[1]):
        msg = "Matrix file does not exist"
    elif not check_dir(args[3]):
        msg = "Incorrect directions"
    return msg


def check_dir(dirs):
    """ Check if directions are valid"""
    # Add directions to set
    directions = set(dirs)

    # Check if directions are valid
    valid_dirs = ['u', 'd', 'l', 'r', 'w', 'x', 'y', 'z']
    for d in directions:
        if d not in valid_dirs:
            return False

    return True


def read_wordlist_file(filename):
    """ Read word_list from file and return as a list """
    word_list = []

    # Read file
    with open(filename, 'r') as file:
        for line in file.read().splitlines():
            word_list.append(line)

    return word_list


def read_matrix_file(filename):
    """ Read matrix from file and return as 2D list"""
    matrix = []

    # Read file
    with open(filename, 'r') as file:
        # Read line
        for line in file.read().splitlines():
            row = line.split(',')
            matrix.append(row)

    return matrix


def get_first_letter_dict(word_list):
    """ Convert word_list into dictionary sorted
    with first letter of each word as the key """
    word_dict = {}

    # Put words in dictionary
    for word in word_list:
        if word[0] in word_dict:
            word_dict.get(word[0]).append(word)
        else:
            word_dict[word[0]] = [word]

    # Sort each list in dictionary
    for item in word_dict.keys():
        word_dict[item].sort()

    return word_dict


def find_words_in_matrix(word_list, matrix, directions):
    """ Search through matrix to return all words
    from word_list in the directions given"""
    words_found = Counter()
    word_dict = get_first_letter_dict(word_list)
    directions = set(directions)
    # Iterate through matrix to find words starting in each cell
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            cell_letter = matrix[row][col]
            if cell_letter in word_dict:
                words_found.update(check_cell(word_dict[cell_letter],
                                              matrix, directions, row, col))

    # Change results from Counter to list of tuples
    results = []
    for word in words_found.keys():
        tup = (word, words_found[word])
        results.append(tup)
    return results


def check_cell(word_list, matrix, directions, start_row, start_col):
    """ Return all words in given directions that
    start at given cell through recursive calls"""
    # List of words in wordsearch that start at this cell
    found = []

    # Check for one-letter words
    next_cell = []
    letter_match_cell(word_list, matrix[start_row][start_col], 0, found,
                      next_cell)
    word_list = next_cell
    found = found * len(directions)

    # Check for each direction
    for d in directions:
        # Reset variables for each direction
        num = 1
        w_list, next_cell = word_list[:], []
        row = new_row(start_row, d, len(matrix))
        col = new_col(start_col, d, len(matrix[0]))

        # Look for words in direction d
        while len(word_list) > 0 and row is not None and col is not None:
            # Check if current letter of words match the current cell
            letter_match_cell(w_list, matrix[row][col], num, found, next_cell)
            # Update to check for next cell
            row = new_row(row, d, len(matrix))
            col = new_col(col, d, len(matrix[0]))
            w_list, next_cell = next_cell, []
            num += 1

    # Return found words
    return found


def letter_match_cell(word_list, cell_letter, num, found, next_cell):
    """ Check if character num of words in list matches
    the character of cell and if so add to list """
    # Do a binary search to find a word with num-th letter equal to cell
    index = get_letter_index(word_list, cell_letter, num)  # O(log n)
    # If letter is not in word_list
    if index is None:
        return

    # Find all matching words before index
    check_letter_words(word_list, num, cell_letter, found, next_cell,
                       index - 1, -1, 0, len(word_list) - 1)

    # Switch the order of words in next_cell to be alphabetical
    next_cell.reverse()

    # Find all matching words after index
    check_letter_words(word_list, num, cell_letter, found, next_cell,
                       index, 1, 0, len(word_list) - 1)


def check_letter_words(word_list, num, letter, found, next_cell,
                       index, increment, low_bound, up_bound):
    """ Find all words that contain letter as their num-th
    character and add them to lists next_cell if they continue
    beyond current cell, and found if they do not """
    while low_bound <= index <= up_bound:
        word = word_list[index]

        if word[num] == letter:
            # If word ends at this cell add it to found
            if len(word) == num + 1:
                found.append(word)
            # If word continues beyond this cell add it to next_cell
            else:
                next_cell.append(word)

        # List has moved past words starting with the letter
        else:
            break

        index += increment


def get_letter_index(word_list, letter, num):
    """ Binary search through word_list to find a word
    that has given letter for its num-th character """
    lo = 0
    hi = len(word_list) - 1
    while hi >= lo:
        mid = (hi + lo)//2
        if word_list[mid][num] > letter:
            hi = mid - 1
        elif word_list[mid][num] < letter:
            lo = mid + 1
        else:
            return mid


def new_row(row, d, length):
    """ Return the next row in the given
    direction, knowing current row """
    if d in ['u', 'w', 'x']:
        row -= 1
    elif d in ['d', 'y', 'z']:
        row += 1
    # If next row is outside the matrix, return None
    if row < 0 or row >= length:
        row = None
    return row


def new_col(col, d, length):
    """ Return the next col in the given
        direction, knowing current col """
    if d in ['l', 'x', 'z']:
        col -= 1
    elif d in ['r', 'w', 'y']:
        col += 1
    # If next col is outside the matrix, return None
    if col < 0 or col >= length:
        col = None
    return col


def write_output_file(results, output_filename):
    """ Write results to output file """
    cur_time = time()
    with open(output_filename, 'w') as file:
        for tup in results:
            file.write(tup[0] + "," + str(tup[1]) + "\n")


def search_words(args):
    """ Execute all functions to find all words of a given
    direction in the matrix, and print results to file """
    # Make sure arguments are valid
    if check_input_args(args) is None:
        # Get word_list and matrix from their files
        word_list = read_wordlist_file(args[0])
        matrix = read_matrix_file(args[1])
        # Find words of given direction in matrix
        results = find_words_in_matrix(word_list, matrix, args[3])
        # Print results to a file
        write_output_file(results, args[2])


if __name__ == "__main__":
    search_words(sys.argv[1:])
