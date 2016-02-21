"""
Cookie Clicker strategy Simulator
"""

import simpleplot, math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total = 0.0
        self._current = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + str(self._time) + " Current cookies: " + str(self._current) + " CPS: " + str(self._cps) \
               + " Total cookies: " + str(self._total) + " History (lenght: " + str(len(self._history)) \
               + "): " + str(self._history)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        time = 0.0
        if cookies > self._current:
            time = math.ceil((cookies - self._current) / self._cps)
        
        return time
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._time += time
            self._current += time * self._cps
            self._total += time * self._cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current >= cost:
            self._cps += additional_cps
            self._current -= cost
            self._history.append((self._time, item_name, cost, self._total))
        
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    new_build = build_info.clone()
    clicker = ClickerState()
    time = 0.0
    while time <= duration:
        #print clicker
        item = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), \
                 duration - time, new_build)
        #print "Item:", item
        if item == None:
            break
        # Determine how much time must elapse until it is possible 
        # to purchase the item. If you would have to wait past the duration 
        # of the simulation to purchase the item, you should end the simulation
        cost = new_build.get_cost(item)
        time_wait = clicker.time_until(cost)
        #print "Cost: ", cost, "CPS: ", new_build.get_cps(item), "Wait time: ", time_wait
        if time_wait + time > duration:
            break
        # Wait until that time
        time += time_wait
        #print "Time =", time
        clicker.wait(time_wait)
        # Buy the item and Update the build information
        clicker.buy_item(item, cost, new_build.get_cps(item))
        new_build.update_item(item)
        
    clicker.wait(duration - time)  
    
    
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    Time: 10000000000.0
    Current Cookies: 6965195661.5
    CPS: 16.1
    Total Cookies: 153308849166.0
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    item_return = None
    items = {}
    for item in build_info.build_items():
        if build_info.get_cost(item) <= cookies + time_left * cps:
            items[item] = build_info.get_cost(item)
    if len(items) > 0:
        min_value = min(items.values())
        for buy_item in items:
            if items[buy_item] == min_value:
                item_return = buy_item            
    return item_return

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    item_return = None
    items = {}
    for item in build_info.build_items():
        if build_info.get_cost(item) <= cookies + time_left * cps:
            items[item] = build_info.get_cost(item)
    if len(items) > 0:
        max_value = max(items.values())
        for buy_item in items:
            if items[buy_item] == max_value:
                item_return = buy_item            
    return item_return

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    item_return = None
    items = {}
    for item in build_info.build_items():
        if build_info.get_cost(item) <= cookies + time_left * cps:
            items[item] = build_info.get_cost(item) * time_left * build_info.get_cps(item)
    if len(items) > 0:
        max_value = max(items.values())
        for buy_item in items:
            if items[buy_item] == max_value:
                item_return = buy_item            
    return item_return
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #print "Start"
    #test = ClickerState()
    #print test
    #test.wait(10)
    #print test
    #test.wait(10000000000)
    #print test
    
    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #print strategy_cheap(0.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
    #print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 15.0, strategy_cursor_broken)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

