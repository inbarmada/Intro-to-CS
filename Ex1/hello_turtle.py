######################################################################
# FILE : hello_turtle.py
# WRITER : Inbar Leibovich, inbarlei, 21395389
# EXERCISE : intro2cse ex1 2020
# DESCRIPTION : print a picture of three flowers
# ADDITIONAL COMMENTS:
######################################################################
import turtle
def draw_petal():
    '''prints a petal'''
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)

def draw_flower():
    '''prints a flower with four petals and a stem'''
    turtle.left(45)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(135)
    turtle.forward(150)

def draw_flower_and_advance():
    '''prints a flower and moves forward'''
    draw_flower()
    turtle.right(90)
    turtle.up()
    turtle.forward(150)
    turtle.right(90)
    turtle.forward(150)
    turtle.left(90)
    turtle.down()

def draw_flower_bed():
    '''prints three flowers'''
    # Put turtle at beginning location
    turtle.up()
    turtle.forward(200)
    turtle.left(180)
    turtle.down()
    # Draw the three flowers
    draw_flower_and_advance()
    draw_flower_and_advance()
    draw_flower_and_advance()

if __name__ == "__main__":
    draw_flower_bed()
    turtle.done()