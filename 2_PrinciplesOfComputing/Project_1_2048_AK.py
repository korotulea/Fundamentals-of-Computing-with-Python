"""
Clone of 2048 game.
"""

import poc_2048_gui, random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def shift(line):
    """
    Helper function shif all values in a list to the left and removes zeros
    """
    return [dum_numbers for dum_numbers in line if dum_numbers != 0]

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # shift all the values to the left
    shifted_line = shift(line)
    # check the values in the new list and combine according to the 2048 rules
    for dum_index in range(len(shifted_line) - 1):
        if shifted_line[dum_index] == shifted_line[dum_index + 1]:
            shifted_line[dum_index] *= 2
            shifted_line[dum_index + 1] = 0
    # shift the final line
    final_line = shift(shifted_line)
    return final_line + [0] * (len(line) - len(final_line))

def traverse_grid(start_cell, direction, num_steps):
    """
    Function that iterates through the cells in a grid
    in a linear direction
    
    Both start_cell is a tuple(row, col) denoting the
    starting cell
    
    direction is a tuple that contains difference between
    consecutive cells in the traversal
    """
    line_to_merge = []
    # traverse along direction
    for step in range(num_steps):
        row = start_cell[0] + step * direction[0]
        col = start_cell[1] + step * direction[1]
        line_to_merge.append((row, col))
    return line_to_merge

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # initiate the starting parameters
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = []
        self._init_up = []
        self._init_down = []
        self._init_left = []
        self._init_right = []
        self._directions = {}
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # built an 0-ed grid
        self._grid = [[0*dum_col*dum_row for dum_col in range(self._grid_width)] 
                      for dum_row in range(self._grid_height)]
        # add 2 or 4 into 2 cells
        self.new_tile()
        self.new_tile()
        # create lists of tuples to start the line based on direction
        self._init_up = [(0, init_line) 
                         for init_line in range(self._grid_width)]
        self._init_down = [(self._grid_height - 1, init_line) 
                         for init_line in range(self._grid_width)]
        self._init_right = [(init_line, self._grid_width - 1) 
                         for init_line in range(self._grid_height)]
        self._init_left = [(init_line, 0) 
                         for init_line in range(self._grid_height)]
        self._directions[UP] = self._init_up
        self._directions[DOWN] = self._init_down
        self._directions[RIGHT] = self._init_right
        self._directions[LEFT] = self._init_left

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # reterning grid in readable form
        return str(["Row " + str(dum_index) + ": " + str(self._grid[dum_index]) 
                    for dum_index in range(len(self._grid))])

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # returning the grid height
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # returning the grid width
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # define lenght of line based on direction
        if direction <= 2:
            num_steps = self._grid_height
        else:
            num_steps = self._grid_width
        # save initial state
        initial = str(self)
        # create lines and mergere based on direction
        for dum_line in self._directions[direction]:
            line_ind = traverse_grid(dum_line, OFFSETS[direction], num_steps)
            line_values = [self._grid[l_index[0]][l_index[1]] for l_index in line_ind]
            new_line_values = merge(line_values)
            for nl_index in range(len(line_ind)):
                l_index = line_ind[nl_index]
                self._grid[l_index[0]][l_index[1]] = new_line_values[nl_index]
        # save processed state
        processed = str(self)
        # check if tiles were moved and add new tile/tiles if needed
        if initial != processed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # selecting zero indecies and create a list of lists of zero cells 
        temp = []
        for dum_zrow in range(self._grid_height):
            for dum_zcol in range(self._grid_width): 
                if self._grid[dum_zrow][dum_zcol] == 0:
                    temp.append([dum_zrow, dum_zcol])
        # if there is a second cell avaliable selecting cell gandomly and assing 2 - 90% and 4 - 10% randomly
        if len(temp) > 0:
            number_list = temp.pop(random.choice(range(len(temp))))
            if random.random() < .9:
                self._grid[number_list[0]][number_list[1]] = 2
            else:
                self._grid[number_list[0]][number_list[1]] = 4
               
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # set a new value for the given position
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # return a value at a given position
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
