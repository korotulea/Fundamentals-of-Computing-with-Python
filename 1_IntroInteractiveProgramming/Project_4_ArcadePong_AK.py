# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left

def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_vel[0] = random.randrange(120, 240) / 60
    if not direction:
        ball_vel[0] = - ball_vel[0]
    ball_vel[1] = - random.randrange(60, 180) / 60
    #print 'ball_vel = ', ball_vel
    #print 'ball_pos = ', ball_pos

# define RESET button
def but_reset():
    new_game()
    
# define event handlers
def new_game():
    global ball_pos, ball_vel, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, direction  # these are numbers
    global score1, score2  # these are ints
    direction = random.choice([RIGHT, LEFT])
    print direction
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [0, 0]
    spawn_ball(direction)
    paddle1_pos = [HEIGHT/2 - PAD_HEIGHT/2, HEIGHT/2 + PAD_HEIGHT/2] 
    paddle2_pos = [HEIGHT/2 - PAD_HEIGHT/2, HEIGHT/2 + PAD_HEIGHT/2] 
    paddle1_vel = 0 
    paddle2_vel = 0
    score1 = 0
    score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, direction, paddle1_vel, paddle2_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    #print ball_pos[0]
    if ball_pos[0] <= PAD_WIDTH - 1 + BALL_RADIUS or ball_pos[0] >= WIDTH + 1 - PAD_WIDTH - BALL_RADIUS:
        ball_pos = [WIDTH/2, HEIGHT/2]
        if direction:
            score1 += 1
        else:
            score2 += 1
        direction = not direction
        spawn_ball(direction)
        
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]            
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[0] < 0:
        paddle1_vel = 0
        paddle1_pos[0] += 1
        paddle1_pos[1] += 1
    elif paddle1_pos[1] > HEIGHT:
        paddle1_vel = 0
        paddle1_pos[0] -= 1
        paddle1_pos[1] -= 1        
    paddle1_pos[0] += paddle1_vel
    paddle1_pos[1] += paddle1_vel

    if paddle2_pos[0] < 0:
        paddle2_vel = 0
        paddle2_pos[0] += 1
        paddle2_pos[1] += 1
    elif paddle2_pos[1] > HEIGHT:
        paddle2_vel = 0
        paddle2_pos[0] -= 1
        paddle2_pos[1] -= 1        
    paddle2_pos[0] += paddle2_vel
    paddle2_pos[1] += paddle2_vel        

    
    # draw paddles
    canvas.draw_line([PAD_WIDTH / 2, paddle1_pos[0]], [PAD_WIDTH / 2, paddle1_pos[1]], PAD_WIDTH, 'White')
    canvas.draw_line([WIDTH - PAD_WIDTH / 2, paddle2_pos[0]], [WIDTH - PAD_WIDTH / 2, paddle2_pos[1]], PAD_WIDTH, 'White')    
    
#    print '0 = ', ball_pos[0]
#    print '1 = ', ball_pos[1]
#    print '0p = ', paddle1_pos[0]
#    print '1p = ', paddle1_pos[1]
    
    # determine whether paddle and ball collide    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH + 4 and ball_pos[1] >= paddle1_pos[0] and ball_pos[1] <= paddle1_pos[1]:
        ball_vel[0] = - ball_vel[0] * 1.1
        ball_vel[1] *= 1.1
        direction = not direction

    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH - 4 and ball_pos[1] >= paddle2_pos[0] and ball_pos[1] <= paddle2_pos[1]:
        ball_vel[0] = - ball_vel[0] * 1.1
        ball_vel[1] *= 1.1
        direction = not direction    
    
#    print ball_vel
        
    # draw scores
    canvas.draw_text(str(score1), (150, 100), 60, 'White')
    canvas.draw_text(str(score2), (450, 100), 60, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -4
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 4 
    else: 
        paddle1_vel = 0   

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -4
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 4 
    else: 
        paddle2_vel = 0   
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    else: 
        paddle1_vel = 0

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    else: 
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button_reset = frame.add_button('RESET', but_reset, 50)


# start frame
new_game()
frame.start()
