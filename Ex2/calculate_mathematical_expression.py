############################################################
# FILE : calculate_mathematical_expression.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex2 2020
# DESCRIPTION: Calculate a mathematical expression from
#              user input
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################


def calculate_mathematical_expression(a, b, operator):
    """Evaluate expression given two numbers and an operator"""
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        # Don't divide by 0
        if b != 0:
            return a / b


def calculate_from_string(calc):
    """Divide string input into numbers and operator to evaluate"""
    # Get user input
    a, operator, b = calc.split()

    # Convert a and b from strings to numbers
    num_a = float(a)
    num_b = float(b)

    # Return result of expression
    return calculate_mathematical_expression(num_a, num_b, operator)

