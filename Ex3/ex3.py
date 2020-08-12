####################################################################
# FILE : ex3.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex3 2020
# DESCRIPTION: Several functions dealing with lists and sequences
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
####################################################################


def input_list():
    """Create a list from user input and its sum"""
    nums = []
    list_sum = 0

    # Take in an input
    x = input()

    # While the input is not an empty string
    while x:
        # Add the input to the list
        nums.append(float(x))
        # Add to the sum
        list_sum += float(x)
        # Take in a new input
        x = input()

    # Add the sum to the list
    nums.append(list_sum)
    return nums


def inner_product(vec_1, vec_2):
    """Calculate the inner product"""
    # Check if the vectors are the same length
    if len(vec_1) != len(vec_2):
        return None

    product = 0
    # Iterate through the vectors to calculate product
    for i in range(len(vec_1)):
        product += vec_1[i] * vec_2[i]
    return product


def sequence_monotonicity(sequence):
    """Check if a sequence is any of:
    increasing, strictly increasing,
    decreasing, strictly decreasing"""
    increasing = True
    decreasing = True
    strict = True
    # Check every consecutive pair of integers from
    # sequence to see if they're increasing/decreasing/constant
    for i in range(1, len(sequence)):
        # If increased
        if sequence[i] > sequence[i - 1]:
            decreasing = False
        # If decreased
        elif sequence[i] < sequence[i - 1]:
            increasing = False
        # If remained constant
        else:
            strict = False

    monotonicity = [False, False, False, False]

    monotonicity[0] = increasing  # Is increasing
    monotonicity[1] = increasing and strict  # Is strictly increasing
    monotonicity[2] = decreasing  # Is decreasing
    monotonicity[3] = decreasing and strict  # Is strictly decreasing

    return monotonicity


def monotonicity_inverse(def_bool):
    """Give an example for sequences
    according to their monotonicity"""
    # Increasing - [T, *, F, F]
    if def_bool[0] and (not def_bool[2] and not def_bool[3]):
        if def_bool[1]:
            return [0, 1, 2, 3]  # Strictly increasing
        else:
            return [1, 2, 3, 3]  # increasing non-strictly

    # Decreasing - [F, F, T, *]
    elif def_bool[2] and (not def_bool[0] and not def_bool[1]):
        if def_bool[3]:
            return [3, 2, 1, 0]  # Strictly decreasing
        else:
            return [3, 3, 2, 1]  # decreasing non-strictly

    # Decreasing and increasing non-strictly - [T, F, T, F]
    elif def_bool == [True, False, True, False]:
        return [1, 1, 1, 1]

    # Neither increasing nor decreasing - [F, F, F, F]
    elif def_bool == [False, False, False, False]:
        return [1, 2, 3, 2]

    else:
        return None


def primes_for_asafi(n):
    """Calculate the first n primes"""
    if n == 0:
        return []

    primes = [2]
    i = 3
    # While the list has less than n primes
    while len(primes) < n:
        # Check if i is divisible by any primes
        j = 0
        while primes[j]**2 <= i:
            # break if i is not prime
            if i % primes[j] == 0:
                break
            j += 1
        # if the while loop didn't break, i is prime
        else:
            primes.append(i)
        # Check the next odd number
        i += 2

    return primes


def sum_of_vectors(vec_lst):
    """Calculate the sum of all vectors in a list"""
    # Check for empty list
    if len(vec_lst) == 0:
        return None

    # Initialize sum vector
    sum_list = [0] * len(vec_lst[0])

    # loop through vectors in vec_lst
    for i in range(len(vec_lst)):
        # loop through items in each vector
        for j in range(len(vec_lst[i])):
            # add each item to location in sum vector
            sum_list[j] += vec_lst[i][j]

    return sum_list


def num_of_orthogonal(vectors):
    """Find the number of pairs of orthogonal vectors from a list"""
    num_orthogonal = 0

    # loop through each pair of vectors
    for i in range(len(vectors)):
        for j in range(i+1, len(vectors)):
            # Check if the vector pair is orthogonal
            if inner_product(vectors[i], vectors[j]) == 0:
                num_orthogonal += 1

    return num_orthogonal

print(num_of_orthogonal([[],[]]))