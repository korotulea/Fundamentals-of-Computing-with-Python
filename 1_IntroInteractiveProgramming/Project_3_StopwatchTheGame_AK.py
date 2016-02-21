#"Stopwatch: The Game"
import simplegui

# define global variables
time = 0
overflow = 0
counter_stops = 0
counter_match = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """ Define the proper format of the time """
    global overflow, t1
    t1 = time % 10
    t2 = (t - t1) / 10
    t22 = t2 % 10
    t21 = (t2 % 60) / 10
    t3 = t2 / 60
    if t3 >= 10:
        timer.stop()
        overflow = 1
        return '9:59:9'
    else:
        return str(t3) + ":" + str(t21) + str(t22) + '.' + str(t1)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def button_start():
    """ Define "Start" button for the stopwarch """
    timer.start()

def button_stop():
    """ Define "Stop" button for the stopwarch """
    global counter_stops, counter_match
    timer.stop()
    if t1 == 0:
        counter_match += 1
    else:
        counter_stops += 1
    
def button_reset():
    """ Define "Reset" button for the stopwarch """
    global time, overflow, counter_stops, counter_match
    timer.stop()
    time = 0
    overflow = 0
    counter_stops = 0
    counter_match = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    """ Define timer handler """
    global time
    time += 1   

# define draw handler
def draw_stopwatch(canvas):
    """Draw stopwatch on canvas"""
    counters = str(counter_match) + '/' + str(counter_stops)
    canvas.draw_text(format(time), [100, 150], 42, "White")
    canvas.draw_text(counters, [250, 35], 24, "Lime")
    if overflow == 1:
        canvas.draw_text("Stopwatch overflow! Reset!", [15, 100], 24, "Red")
    
# create frame
frame = simplegui.create_frame("StopWatch: The GAME", 300, 200)

# register event handlers
frame.set_draw_handler(draw_stopwatch)
start_but = frame.add_button("Start", button_start, 50)
stop_but = frame.add_button("Stop", button_stop, 50)
reset_but = frame.add_button("Reset", button_reset, 50)
timer = simplegui.create_timer(100, timer_handler)
                                                               
# start frame
frame.start()
