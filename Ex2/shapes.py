############################################################
# FILE : shapes.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex2 2020
# DESCRIPTION: Calculate the area of different shapes
#              based on user input
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################
import math


def shape_area():
    """Choose a shape and calculate its area given its sides/radius"""
    # Get shape chosen
    shape = int(input("Choose shape (1=circle, 2=rectangle, 3=triangle): "))
    circle, rectangle, triangle = 1, 2, 3

    # Calculate area based on shape type
    if shape == circle:
        return circle_area()
    elif shape == rectangle:
        return rectangle_area()
    elif shape == triangle:
        return triangle_area()


def circle_area():
    """Calculate circle area from radius"""
    # Get user input
    r = float(input())
    # Calculate and return area
    return r * r * math.pi


def rectangle_area():
    """Calculate rectangle area from two sides"""
    # Get user input
    side_a = float(input())
    side_b = float(input())
    # Calculate and return area
    return side_a * side_b


def triangle_area():
    """Calculate triangle area from side length"""
    # Get user input
    a = float(input())
    # Calculate and return area
    equilateral_triangle_constant = (3 ** 0.5) / 4
    return a * a * equilateral_triangle_constant
