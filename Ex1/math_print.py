######################################################################
# FILE : math_print.py
# WRITER : Inbar Leibovich, inbarlei, 21395389
# EXERCISE : intro2cse ex1 2020
# DESCRIPTION : print the results for several math functions
# ADDITIONAL COMMENTS:
######################################################################
import math

def golden_ratio():
    '''Prints the goldern ratio'''
    x = 1 + math.sqrt(5)
    print(x/2)

def six_squared():
    '''prints 36'''
    print(math.pow(6,2))

def hypotenuse():
    '''prints the hypotenuse of a right triangle with sides 5 and 12'''
    hypotenuse_squared = math.pow(12, 2) + math.pow(5, 2)
    print(math.sqrt(hypotenuse_squared))

def pi():
    '''prints the value of the number pi'''
    print(math.pi)

def e():
    '''prints the value of the number e'''
    print(math.e)

def squares_area():
    '''prints the areas of squares with sides from 1 to 10'''
    print(math.pow(1,2), math.pow(2,2), math.pow(3,2), math.pow(4,2), math.pow(5,2),
                math.pow(6,2), math.pow(7,2), math.pow(8,2), math.pow(9,2), math.pow(10,2))

if __name__ == "__main__":
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()
