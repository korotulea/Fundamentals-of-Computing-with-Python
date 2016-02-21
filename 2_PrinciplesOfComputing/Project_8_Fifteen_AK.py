"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) == 0:
            for tmp_row in range(target_row + 1, self._height, 1):
                for tmp_col in range(self._width):
                    #print "In puz:", self.get_number(tmp_row, tmp_col), "Right num:", tmp_col + self._width * tmp_row
                    if self.get_number(tmp_row, tmp_col) != tmp_col + self._width * tmp_row:
                        #print "Number for solved", tmp_col + self._width * tmp_row
                        #print "Number in place", self.get_number(tmp_row, tmp_col)
                        #assert False, "invalied Lower_row_invariant"
                        return False
            for tmp_col in range(target_col + 1, self._width, 1):
                #print "In puz:", self.get_number(target_row, tmp_col), "Right num:", tmp_col + self._width * target_row
                if self.get_number(target_row, tmp_col) != tmp_col + self._width * target_row:
                    #print "Number for solved", tmp_col + self._width * target_row
                    #print "Number in place", self.get_number(target_row, tmp_col)
                    #assert False, "invalied Lower_row_invariant"
                    return False
            return True
        else:
            #assert False, "invalied Lower_row_invariant"
            return False

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        results = ""
        target = target_col + self._width * target_row
        #if self.get_number(target_row, target_col) == target \
        #          and self.lower_row_invariant(target_row, target_col - 1): #don't know yet
        #    return results     #check!!!
        puz_clone = self.clone()
        #print puz_clone
        target_cur = self.current_position(target_row, target_col)
        #print "Target position", target_cur
        while puz_clone.current_position(0, 0)[0] > target_cur[0]:
            #print "loop 1"
            results += "u"
            puz_clone.update_puzzle("u")
            #print "loop 1", "\n",  puz_clone
        #print "Position after loop 1", puz_clone.current_position(0, 0) 
        #print "Target position after loop 1", puz_clone.current_position(target_row, target_col)
        if puz_clone.current_position(0, 0)[0] < target_row:
            while puz_clone.current_position(0, 0)[1] - 2 > \
                  puz_clone.current_position(target_row, target_col)[1]:
                results += "l"
                puz_clone.update_puzzle("l") 
                #print "loop 2.0.1", "\n", puz_clone    
            while puz_clone.current_position(0, 0)[1] - \
                  puz_clone.current_position(target_row, target_col)[1] > 1:
                #print "loop 2.1"
                results += "lldrru"
                puz_clone.update_puzzle("lldrru") 
                #print "loop 2.1", "\n", puz_clone

        while puz_clone.current_position(target_row, target_col)[0] != \
              puz_clone.current_position(0, 0)[0] - 1 and \
              puz_clone.current_position(target_row, target_col)[1] != \
              puz_clone.current_position(0, 0)[1]:
            #print "loop 2.2"
            if puz_clone.current_position(0, 0)[0] == target_row:
                if puz_clone.current_position(target_row, target_col)[1] + 1 == \
                  puz_clone.current_position(0, 0)[1]:
                    #print "in loop 2.2.1"
                    results += "l"
                    puz_clone.update_puzzle("l") 
                    #print "loop 2.2.1", "\n", puz_clone
                    self.update_puzzle(results)
                    return results
                else:
                    while puz_clone.current_position(0, 0)[1] > puz_clone.current_position(target_row, target_col)[1]:
                        #print "in loop 2.2.2"
                        results += "l"
                        puz_clone.update_puzzle("l")
                        #print "loop 2.2.2", "\n", puz_clone
                    while puz_clone.current_position(0, 0)[1] != target_col - 1 and \
                          puz_clone.current_position(target_row, target_col)[1] != target_col:
                        #print "in loop 2.2.3"
                        results += "urrdl"
                        puz_clone.update_puzzle("urrdl")
                        #print "loop 2.2.3", "\n", puz_clone
                    self.update_puzzle(results)
                    return results
#            elif puz_clone.current_position(0, 0)[1] < puz_clone.current_position(target_row, target_col)[1]:
#                    while puz_clone.current_position(0, 0)[1] < \
#                          puz_clone.current_position(target_row, target_col)[1]:
#                        results += "r"
#                        puz_clone.update_puzzle("r") 
#                        print "loop 2.2.3.2", "\n", puz_clone #test
            elif puz_clone.current_position(0, 0)[1] > puz_clone.current_position(target_row, target_col)[1]:
                #print "in loop 2.2.4"        
                results += "ldru"
                puz_clone.update_puzzle("ldru") 
                #print "loop 2.2.4", "\n", puz_clone
            else: 
                #print "in loop 2.2.5"
                results += "r"
                puz_clone.update_puzzle("r") 
                #print "loop 2.2.5", "\n", puz_clone #test
        if puz_clone.current_position(target_row, target_col)[1] > target_col and \
              puz_clone.current_position(target_row, target_col)[0] == target_row - 1:
            #print "in loop 2.3"
            while puz_clone.current_position(target_row, target_col)[1] > target_col:
                #print "in loop 2.3.1"
                results += "ldrul"
                puz_clone.update_puzzle("ldrul") 
                #print "loop 2.3.1", "\n", puz_clone #test
        while puz_clone.get_number(target_row, target_col) != target and \
              puz_clone.current_position(target_row, target_col)[0] < target_row:
            #print "loop 3", puz_clone.current_position(0, 0)
            results += "lddru"
            puz_clone.update_puzzle("lddru")
            #print "loop 3", "\n", puz_clone            
        while puz_clone.current_position(target_row, target_col)[1] != target_col:
            #print "loop 4", puz_clone.current_position(0, 0)
            results += "rdlur"
            puz_clone.update_puzzle("rdlur")
            #print "loop 4", "\n", puz_clone
        results += "ld"
        puz_clone.update_puzzle("ld")
        #print "last move", "\n", puz_clone 
        self.update_puzzle(results)
        return results
        
        

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        results = ""
        target = self._width * target_row
        puz_clone = self.clone()
        #print "Start", "\n", puz_clone
        results = "u"
        puz_clone.update_puzzle("u")
        if puz_clone.get_number(target_row, 0) == target:
            while puz_clone.current_position(0, 0)[1] != self._width - 1:
                results += "r"
                puz_clone.update_puzzle("r")
                #print "Loop 1", "\n", puz_clone
            self.update_puzzle(results)
            return results
        if puz_clone.current_position(target_row, 0)[0] == target_row - 1:
            #print "Loop 2", "\n", puz_clone
            while puz_clone.current_position(0, 0)[1] + 1 != \
                  puz_clone.current_position(target_row, 0)[1]:
                results += "r"
                puz_clone.update_puzzle("r")
                #print "Loop 2.1", "\n", puz_clone
            while puz_clone.current_position(0, 0)[1] != 0:
                results += "rulld"
                puz_clone.update_puzzle("rulld")
                #print "Loop 2.2", "\n", puz_clone
        elif puz_clone.current_position(target_row, 0)[0] < target_row - 1:
            #print "In loop 4", "\n", puz_clone  
            while puz_clone.current_position(0, 0)[1] != \
                  puz_clone.current_position(target_row, 0)[1]:
                #print "In loop 4.1", puz_clone.current_position(0, 0)[0]
                results += "r"
                puz_clone.update_puzzle("r") 
                #print "Loop 4.1", "\n", puz_clone
            while puz_clone.current_position(0, 0)[0] - 1 != \
                  puz_clone.current_position(target_row, 0)[0]:
                results += "u"
                puz_clone.update_puzzle("u") 
                #print "Loop 4.1.1", "\n", puz_clone
            while puz_clone.current_position(0, 0)[1] > 0 and \
                  puz_clone.current_position(target_row, 0)[1] != 0: 
                #print "In loop 4.2", puz_clone.current_position(0, 0)[0]
                results += "uld"
                puz_clone.update_puzzle("uld")
                #print "Loop 4.2", "\n", puz_clone
                while puz_clone.current_position(0, 0)[0] >= 0 and \
                      puz_clone.current_position(target_row, 0)[1] != 1: #zzz
                    results += "rulld"
                    puz_clone.update_puzzle("rulld")
                    #print "Loop 4.2.1", "\n", puz_clone
            if puz_clone.current_position(0, 0)[0] < target_row - 1:
                #print "In loop 4.3"
                results += "rdl"
                puz_clone.update_puzzle("rdl")
                #print "Loop 4.3", "\n", puz_clone
            
            if puz_clone.current_position(target_row, 0)[1] == 0 \
                  and puz_clone.current_position(0, 0)[1] == 0:
                #print "In loop 3"
                while puz_clone.current_position(0, 0)[0] - 1 != \
                      puz_clone.current_position(target_row, 0)[0]:
                    results += "u"
                    puz_clone.update_puzzle("u")
                    #print "Loop 3.1", "\n", puz_clone
                while puz_clone.current_position(0, 0)[0] != \
                      puz_clone.current_position(target_row, 0)[0] and \
                      puz_clone.current_position(0, 0)[0] != target_row:
                    #print "In loop 3.2", "\n", puz_clone
                    results += "urdl"
                    puz_clone.update_puzzle("urdl")
                    #print "Loop 3.2", "\n", puz_clone
                    if puz_clone.current_position(0, 0)[0] != target_row - 1:
                        #print "In loop 3.2.1", puz_clone 
                        results += "rdl"
                        puz_clone.update_puzzle("rdl")
        
        results += "ruldrdlurdluurddlur"            
        puz_clone.update_puzzle("ruldrdlurdluurddlur")
        #print "In loop 5.1", "\n", puz_clone
        
        while puz_clone.current_position(0, 0)[1] + 1 < self._width:
            results += "r"
            puz_clone.update_puzzle("r")
            #print "In loop 5.2", "\n", puz_clone
            
        self.update_puzzle(results)
        return results
        

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        #print self.get_number(0, target_col)
        if self.get_number(0, target_col) == 0:
            for tmp_row in range(2, self._height, 1):
                #print "tmp_row", tmp_row
                for tmp_col in range(self._width):
                    if self.get_number(tmp_row, tmp_col) != tmp_col + self._width * tmp_row:
                        #print "loop 1"
                        return False
                    
            if self.get_number(1, target_col) != target_col + self._width:
                return False                    

            for tmp_col in range(target_col + 1, self._width, 1):
                #print tmp_col, self.get_number(1, tmp_col), self.get_number(0, tmp_col)
                if self.get_number(1, tmp_col) != tmp_col + self._width or \
                    self.get_number(0, tmp_col) != tmp_col:
                    #print "loop 2"
                    return False
            return True
        else:
            #print "loop 3"
            return False        

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(1, target_col) == 0:
            for tmp_row in range(2, self._height, 1):
                #print "tmp_row", tmp_row
                for tmp_col in range(self._width):
                    if self.get_number(tmp_row, tmp_col) != tmp_col + self._width * tmp_row:
                        #print "loop 1"
                        return False

            for tmp_col in range(target_col + 1, self._width, 1):
                #print tmp_col, self.get_number(1, tmp_col), self.get_number(0, tmp_col)
                if self.get_number(1, tmp_col) != tmp_col + self._width or \
                      self.get_number(0, tmp_col) != tmp_col:
                    #print "loop 2"
                    return False
            return True
        else:
            return False
        
    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        results = ""
        puz_clone = self.clone()  
        #print "start"
        results += "ld"
        puz_clone.update_puzzle("ld")
        #print puz_clone   
        #print puz_clone.row1_invariant(target_col-1), target_col - 1
        if puz_clone.row1_invariant(target_col-1):
            self.update_puzzle(results)
            return results
        #print "next step"    
        while puz_clone.current_position(0, 0)[1] > \
              puz_clone.current_position(0, target_col)[1]:
            #print "loop 1"
            results += "l"
            puz_clone.update_puzzle("l")
            #print puz_clone
#        while puz_clone.current_position(0,0)[1] != target_col and \
#              puz_clone.current_position(0, target_col)[1] != target_col - 1 and \
#              puz_clone.current_position(0, target_col)[0] == 0:
#            print "loop 2"
#            results += "drrul"
#            puz_clone.update_puzzle("drrul")
#            print puz_clone
        if puz_clone.current_position(0,0)[0] != puz_clone.current_position(0, target_col)[0] and \
              puz_clone.current_position(0,0)[1] < target_col - 1:
            #print "loop 3.1"
            results += "urdl"
            puz_clone.update_puzzle("urdl")
            #print puz_clone 
        elif puz_clone.current_position(0,0)[0] != puz_clone.current_position(0, target_col)[0] and \
              puz_clone.current_position(0,0)[1] == target_col - 1:
            #print "loop 3.2"
            results += "uld"
            puz_clone.update_puzzle("uld")
            #print puz_clone
#        print "move r"
#        results += 'r'
#        puz_clone.update_puzzle("r")
#        print puz_clone
        while puz_clone.current_position(0,0)[1] != target_col - 2:
            #print "loop 4"
            results += "urrdl"
            puz_clone.update_puzzle("urrdl")
            #print puz_clone
        #print "last move"
        results += "urdlurrdluldrruld"
        puz_clone.update_puzzle("urdlurrdluldrruld")
        #print puz_clone

        self.update_puzzle(results)
        return results
            
            
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code  
        results = ""
        puz_clone = self.clone() 
        while puz_clone.current_position(0, 0)[0] > 0 and \
              puz_clone.current_position(1, target_col)[0] == 0:
            #print "loop 1"
            results += "u"
            puz_clone.update_puzzle("u")
            #print puz_clone
            if puz_clone.row0_invariant(target_col):
                #print "done in loop 1"
                self.update_puzzle(results)
                return results 
        while puz_clone.current_position(0,0)[1] - 1 > puz_clone.current_position(1, target_col)[1]:
            #print "loop 2"
            results += "l"
            puz_clone.update_puzzle("l")
            #print puz_clone            
        while puz_clone.current_position(0,0)[1] != target_col and \
              puz_clone.current_position(1, target_col)[1] != target_col - 1 and \
              puz_clone.current_position(1, target_col)[0] == 0:
            #print "loop 3"
            results += "ldrru"
            puz_clone.update_puzzle("ldrru")
            #print puz_clone 
        if puz_clone.current_position(0,0)[1] == target_col and \
              puz_clone.current_position(1, target_col)[1] == target_col - 1 and \
              puz_clone.current_position(1, target_col)[0] == 0:
            #print "loop 4"
            results += "ldru"
            puz_clone.update_puzzle("ldru")
            #print puz_clone        
            self.update_puzzle(results)
            return results
        while puz_clone.current_position(0,0)[1] != target_col and \
              puz_clone.current_position(1, target_col)[1] != target_col - 1:
            #print "loop 5"
            results += "lurrd"
            puz_clone.update_puzzle("lurrd")
            #print puz_clone
        #print "last move 5"
        results += "lur"
        puz_clone.update_puzzle("lur")
        #print puz_clone
            
        self.update_puzzle(results)
        return results        
        

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        results = ""
        if self.current_position(0, 1) == (1, 0):
            assert self.current_position(1, 1) != (0, 1), "can't solve"                
            #print "sol 1"
            results = "uldrul"
            self.update_puzzle(results)
        elif self.current_position(0, 1) == (0, 0):
            assert self.current_position(1, 1) != (1, 0), "can't solve" 
            #print "sol 2"
            results = "ul"
            self.update_puzzle(results)        
        elif self.current_position(0, 1) == (0, 1):
            assert self.current_position(1, 1) != (0, 0), "can't solve"
            #print "sol 3"
            results = "lu"
            self.update_puzzle(results)
            
        return results        
                

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        results = ""
        puz_clone = self.clone() 
        cur = self.current_position(0, 0)
        #print "start"
        if puz_clone.lower_row_invariant(cur[0], cur[1]) and \
              self.current_position(0, 0) == (0, 0):
            #print "in loop 0.0"
            puz_clone.update_puzzle("")
            return results 
        #print cur
        if puz_clone.row1_invariant(cur[1]) and cur == (1, 1):
        # and puz_clone.lower_row_invariant(cur[0], cur[1]) \
              
            #print "in loop 0.0.1"
            results += puz_clone.solve_2x2()
            #print puz_clone
            self.update_puzzle(results)
            return results
        cur1 = puz_clone.current_position(0, 0)
        if cur1 != (self._height - 1, self._width -1):
            while puz_clone.current_position(0, 0)[0] < self._height - 1:
                if puz_clone.lower_row_invariant(cur1[0], cur1[1]):
                    break
                #print puz_clone.lower_row_invariant(cur1[0], cur1[1]), puz_clone.current_position(0, 0)[0], self._height - 1 
                #print "loop 0.1"
                results += "d"
                puz_clone.update_puzzle("d")
                #print puz_clone
                cur1 = puz_clone.current_position(0, 0)
            while not puz_clone.lower_row_invariant(cur1[0], cur1[1]): #or \
                  #puz_clone.current_position(0, 0)[1] != self._width - 1:   
                #print puz_clone.lower_row_invariant(cur1[0], cur1[1]), puz_clone.current_position(0, 0)[1]
                
                #print "loop 0.2"
                results += "r"
                puz_clone.update_puzzle("r")
                #print puz_clone
                cur1 = puz_clone.current_position(0, 0)
        #print "end loop 0.2"
        while cur1[0] > 1 and cur1[1] > 0 and \
              puz_clone.lower_row_invariant(cur1[0], cur1[1]):
            #print "loop 1"
            
            for tmp_row in range(cur1[0], 1, -1):
                #print "tmp_row", tmp_row, range(cur1[0], 1, -1)
                for tmp_col in range(cur1[1], 0, -1):
                    #print "Interior loop, tmp_col", tmp_col 
                    results += puz_clone.solve_interior_tile(tmp_row, tmp_col)
                    #print puz_clone
                #print "col 0"
                results += puz_clone.solve_col0_tile(tmp_row)
                #print puz_clone
                #print "cur1", puz_clone.current_position(0, 0)
                cur1 = puz_clone.current_position(0, 0)      
        
        for tmp_col in range(self._width - 1, 1, -1): 
            #print "row1"
            results += puz_clone.solve_row1_tile(tmp_col)
            #print puz_clone
            #print "row0"
            results += puz_clone.solve_row0_tile(tmp_col)
            #print puz_clone
            
        results += puz_clone.solve_2x2()    
        #print puz_clone
        
        #print "done"
        self.update_puzzle(results)
        return results 

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[3, 2, 6], [4, 0, 5], [1, 7, 8]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3))
#poc_fifteen_gui.FifteenGUI(Puzzle(2, 2, [[0, 3], [1, 2]]))

# Pass test_1 = Puzzle(3, 3, [[3, 2, 1], [4, 0, 5], [6, 7, 8]])
#print test_1.lower_row_invariant(1, 1)

# Pass test_2 = Puzzle(3, 3, [[3, 2, 1], [5, 7, 4], [6, 0, 8]])
#print test_2.lower_row_invariant(2, 1)

# test solve_interior_tile
#test_3 = Puzzle(3, 3, [[7, 3, 1], [5, 2, 4], [6, 0, 8]])
#print test_3.solve_interior_tile(2, 1)

#test_4 = Puzzle(3, 3, [[8, 3, 1], [5, 2, 4], [6, 7, 0]])
#print test_4.solve_interior_tile(2, 2)
#print test_4

#test_5 = Puzzle(3, 3, [[7, 3, 1], [5, 2, 4], [6, 8, 0]])
#print test_5.solve_interior_tile(2, 2)
#print test_5

#test_6 = Puzzle(3, 3, [[7, 3, 1], [5, 2, 4], [8, 6, 0]])
#print test_6.solve_interior_tile(2, 2)
#print test_6

#test solve_col0_tile 
#test_7 = Puzzle(3, 3, [[5, 3, 1], [6, 2, 4], [0, 7, 8]])
#print test_7
#print test_7.solve_col0_tile(2)
#print test_7, "\n", "Test 7 pass", "\n"
#
#test_8 = Puzzle(3, 3, [[5, 3, 1], [2, 4, 6], [0, 7, 8]])
#print test_8
#print test_8.solve_col0_tile(2)
#print test_8, "\n", "Test 8 pass", "\n"
#
#test_9 = Puzzle(3, 3, [[6, 3, 1], [2, 4, 5], [0, 7, 8]])
#print test_9
#print test_9.solve_col0_tile(2)
#print test_9, "\n", "Test 9 pass", "\n"

#test_10 = Puzzle(3, 3, [[3, 1, 6], [2, 4, 5], [0, 7, 8]])
#print test_10
#print test_10.solve_col0_tile(2)
#print test_10

#test_11 = Puzzle(4, 4, [[3, 1, 2, 12], [6, 7, 5, 8], [9, 10, 11, 4], [0, 13, 14, 15]])
#print test_11
#print test_11.solve_col0_tile(3)
#print test_11

#test_12 = Puzzle(4, 4, [[3, 12, 2, 1], [6, 7, 5, 8], [9, 10, 11, 4], [0, 13, 14, 15]])
#print test_12
#print test_12.solve_col0_tile(3)
#print test_12

#test_13 = Puzzle(4, 4, [[12, 3, 2, 1], [6, 7, 5, 8], [9, 10, 11, 4], [0, 13, 14, 15]])
#print test_13
#print test_13.solve_col0_tile(3)
#print test_13

#test row1_invariant
#test_14 = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print test_14
#print test_14.row1_invariant(1)

#test row0_invariant
#test_15 = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#print test_15
#print test_15.row0_invariant(0)

#test slove_row1
#test_16 = Puzzle(3, 3, [[5, 2, 3], [4, 1, 0], [6, 7, 8]])
#print test_16
#print test_16.solve_row1_tile(2)

#test_17 = Puzzle(4, 5, [[7, 6, 5, 3, 4], [2, 1, 0, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print test_17
#print test_17.solve_row1_tile(2)

#test_18 = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print test_18
#test_18.solve_row0_tile(2)

#(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]]), obj.solve_row0_tile(2)

#test_19 = Puzzle(4, 5, [[2, 5, 0, 3, 4], [6, 1, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print test_19
#print test_19.solve_row0_tile(2)

#solve_2x2()
#test_20 = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print test_20
#print test_20.solve_2x2()
#print test_20

#test_21 = Puzzle(3, 3, [[1, 4, 2], [3, 0, 5], [6, 7, 8]])
#print test_21
#print test_21.solve_2x2()
#print test_21

#test_22 = Puzzle(3, 3, [[3, 1, 2], [4, 0, 5], [6, 7, 8]])
#print test_22
#print test_22.solve_2x2()
#print test_22



#test_23 = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print test_23
#print test_23.solve_puzzle()
#print test_23
#
#test_24 = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print test_24
#print test_24.solve_puzzle()
#print test_24
#
#test_25 = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#print test_25
#print test_25.solve_puzzle()
#print test_25
#
#
#test_26 = Puzzle(5, 4, [[5, 4, 2, 3], [1, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]])
#print test_26
#print test_26.solve_puzzle()
#print test_26


