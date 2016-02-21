# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import math
import random

# initialize global variables used in your code here
range_max_init = 100
guesses_left = 7

# helper function to start and restart the game
def new_game():
    # initialize new game
    global comp_number
    print
    print 'New game. Range is from 0 to', range_max_init
    print 'Number of remaning guesses', guesses_left
    comp_number = random.randrange(0, range_max_init)
    
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global range_max_init, guesses_left
    range_max_init = 100
    guesses_left = 7
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global range_max_init, guesses_left
    range_max_init = 1000
    guesses_left = 10
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global guesses_left
    guesses_left -= 1
    guess = int(guess)
    print
    print 'Guess was', guess
    print 'Number of remaning quesses is', guesses_left

    # check if this was the las guess
    if guesses_left == 0:
        print 'You run out of guesses'
        if range_max_init == 100:
            guesses_left = 7
        else:
            guesses_left = 10
        new_game()
    # compare guess to computer number    
    elif comp_number == guess:
        print 'Correct!'
        if range_max_init == 100:
            guesses_left = 7
        else:
            guesses_left = 10
        new_game()
    elif comp_number < guess:
        print 'Lower!'
    else:
        print 'Higher!'
    
# create frame
frame = simplegui.create_frame('Guess the Number', 200, 200)

# register event handlers for control elements and start frame
frame.add_button('Range is [0, 100)', range100, 150)
frame.add_button('Range is [0, 1000)', range1000, 150)
frame.add_input('Enter a guess', input_guess, 150)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
