############################################################
# FILE : quadratic_equation.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex2 2020
# DESCRIPTION: Return the solution to the quadratic
#              equation from user input of coefficients
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################


def quadratic_equation(a, b, c):
    """Solve the quadratic equation given the three coefficients"""
    discriminant = b*b - 4*a*c

    # Case with no solution
    if discriminant < 0:
        return

    # Case with one solution
    elif discriminant == 0:
        return (-1 * b) / (2 * a)

    # Case with two solutions
    elif discriminant > 0:
        solution_1 = (-1 * b - (discriminant ** 0.5)) / (2 * a)
        solution_2 = (-1 * b + (discriminant ** 0.5)) / (2 * a)
        return solution_1, solution_2

def quadratic_equation_user_input():
    """Solve a quadratic equation with coefficients from user input"""

    # Get user input, split it, and convert from strings to floats
    str_a, str_b, str_c = input("Insert coefficients a, b, and c: ").split()
    a, b, c = float(str_a), float(str_b), float(str_c)

    if a == 0:
        print("The parameter 'a' may not equal 0")

    else:
        # Find solutions to the coefficients
        solution = quadratic_equation(a, b, c)

        # Case with no solutions
        if solution is None:
            print("The equation has no solutions")

        # Case with 1 solution
        elif type(solution) == float:
            print("The equation has 1 solution: " + str(solution))

        # Case with 2 solutions
        else:
            print("The equation has 2 solutions: " + str(solution[0]) + " and " + str(solution[1]))
