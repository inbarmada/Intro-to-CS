############################################################
# FILE : largest_and_smallest.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex2 2020
# DESCRIPTION: Return a tuple of the largest and smallest
#              numbers out of three and then check the
#              function
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES: In function check_largest_and_smallest, I chose
#        test 4 to check whether the function still works
#        when all parameters are equal. I chose test 5 to
#        check whether the function still works when all
#        parameters are negative (and the two larger one
#        are equal).
############################################################


def largest_and_smallest(a, b, c):
    """Find largest and smallest numbers out of three"""
    # Find biggest number
    big = a if a > b else b
    big = big if big > c else c
    # Find smallest number
    small = a if a < b else b
    small = small if small < c else c
    # Return tuple
    return big, small


def check_largest_and_smallest():
    """Check correctness of largest_and_smallest function"""
    correct = True

    # Test 1
    lg, sm = largest_and_smallest(17, 1, 6)
    if not (lg == 17 and sm == 1):
        correct = False

    # Test 2
    lg, sm = largest_and_smallest(1, 17, 6)
    if not (lg == 17 and sm == 1):
        correct = False

    # Test 3
    lg, sm = largest_and_smallest(1, 1, 2)
    if not (lg == 2 and sm == 1):
        correct = False

    # Test 4
    lg, sm = largest_and_smallest(1, 1, 1)
    if not (lg == 1 and sm == 1):
        correct = False

    # Test 5
    lg, sm = largest_and_smallest(-1, -4, -1)
    if not (lg == -1 and sm == -4):
        correct = False

    # Return whether or not the function works
    return correct
