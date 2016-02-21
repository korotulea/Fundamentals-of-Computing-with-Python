# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck, deck_exposed, counter_click, tmp
    counter_click = 0
    deck_exposed = []
    m = 0
    deck = range(8) * 2
    random.shuffle(deck) 
    for i in range(len(deck)):
        deck_exposed.append(False)
    tmp = []
    label.set_text("Turns = " + str(counter_click))
    
# define event handlers
def mouseclick(pos):
    global card_clicked, counter_click, tmp 
    card_clicked = pos[0] // 50

    if not deck_exposed[card_clicked] and len(tmp) < 2:
        deck_exposed[card_clicked] = True
        counter_click += 1
        tmp.append(card_clicked)
        label.set_text("Turns = " + str(counter_click//2 + counter_click%2))
        
        if len(tmp) == 2 and deck[tmp[0]] == deck[tmp[1]]:
            deck_exposed[tmp[0]] = True
            deck_exposed[tmp[1]] = True
            tmp = []
            label.set_text("Turns = " + str(counter_click//2 + counter_click%2))
            if sum(deck_exposed) == 16:
                label.set_text("Turns = " + str(counter_click//2 + counter_click%2) + " GAME OVER")
            
    elif not deck_exposed[card_clicked] and len(tmp) == 2:
        deck_exposed[tmp[0]] = False
        deck_exposed[tmp[1]] = False
        tmp = []
        deck_exposed[card_clicked] = True
        counter_click += 1
        tmp.append(card_clicked)
        label.set_text("Turns = " + str(counter_click//2 + counter_click%2))

    elif sum(deck_exposed) == 16:
        label.set_text("Turns = " + str(counter_click//2 + counter_click%2) + " GAME OVER")  
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(deck)):
        if deck_exposed[i]:
            canvas.draw_text(str(deck[i]), [10+i*50, 70], 60, 'White')
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 2, 'Red')
        else:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 2, 'Red', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric