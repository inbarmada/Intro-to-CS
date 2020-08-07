############################################################
# FILE : wordsearch.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex5 2020
# DESCRIPTION: Word search solver
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################

import sys
import os.path
from collections import Counter


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


def find_words_in_matrix(word_list, matrix, directions):
    """ Search through matrix to return all words
    from word_list in the directions given"""
    words_found = Counter()

    # Find words in each direction given
    for d in set(directions):
        words_found += direction_words(word_list, matrix, d)

    # Change results from Counter to list of tuples
    results = []
    for word in sorted(words_found.keys()):
        tup = (word, words_found[word])
        results.append(tup)

    return results


def direction_words(word_list, matrix, d):
    """ Search through matrix and return all
    words from word_list in a given direction"""
    words_found = Counter()

    # Iterate through cells of matrix and add word(s)
    # that start at each cell to the word_found counter
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            words_found.update(check_cell(word_list, matrix, d, row, col, 0))

    return words_found


def check_cell(word_list, matrix, d, row, col, num):
    """ Return all words in direction d that
    start at given cell through recursive calls"""
    # Words from previous calls that end at this cell
    found = []
    # Words from previous calls that continue beyond this cell
    next_cell = []

    while len(word_list) > 0 and row is not None and col is not None:
        # Check if current letter of words match the current cell
        letter_match_cell(word_list, matrix[row][col], num, found, next_cell)
        # Update to check for next cell
        row = new_row(row, d, len(matrix))
        col = new_col(col, d, len(matrix[0]))
        word_list, next_cell = next_cell, []
        num += 1

    # Return found words
    return found


def letter_match_cell(word_list, cell_letter, num, found, next_cell):
    """ Check if character num of words in list matches
    the character of cell and if so add to list """
    # Iterate through words that matched the previous cell
    for word in word_list:
        # If the next letter matches this cell
        if word[num] == cell_letter:
            # If word ends at this cell add it to found
            if len(word) == num + 1:
                found.append(word)
            # If word continues beyond this cell add it to next_cell
            else:
                next_cell.append(word)


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
