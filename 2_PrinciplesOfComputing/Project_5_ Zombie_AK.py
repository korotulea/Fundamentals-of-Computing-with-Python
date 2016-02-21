"""
Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_width * self._grid_height \
                           for dummy_col in range(self._grid_width)] \
                             for dummy_row in range(self._grid_height)]        
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            tmp_list = self._zombie_list
        elif entity_type == HUMAN:
            tmp_list = self._human_list
        else:
            tmp_list = []
        for dummy_coord in tmp_list:
            boundary.enqueue(dummy_coord)
            visited.set_full(dummy_coord[0], dummy_coord[1])
            distance_field[dummy_coord[0]][dummy_coord[1]] = 0
        
        while len(boundary) > 0:
            cell = boundary.dequeue()
            neighbors = self.four_neighbors(cell[0], cell[1])
            #neighbors = self.eight_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]) and \
                self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1
                    
#        print "Boundary", boundary
#        
#        print "Visited"    
#        print visited        
#        
        print "Distance_field"
        for grid_row in range(self._grid_height):
            print distance_field[grid_row]
#        
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for index_human in range(self.num_humans()):
            c_human = self._human_list[index_human]
#            print "Human ", c_human
            neighbors_full = self.eight_neighbors(c_human[0], c_human[1])
            neighbors = [cell for cell in neighbors_full if \
                         zombie_distance_field[cell[0]][cell[1]] != self._grid_width * self._grid_height]
#            print "Neighbors_full ", neighbors_full 
#            print "Neighbors ", neighbors
            distances = [zombie_distance_field[cell[0]][cell[1]] for cell in neighbors]
            max_dist =  max(distances)
#            print "Distances ", distances, " Max ", max_dist
            moves = [neighbors[ind] for ind in range(len(distances)) if distances[ind] == max_dist]
            move = random.choice(moves)
#            print "Moves ", moves, " Move ", move
            if max_dist != 0:
                self._human_list[index_human] = move
            
            
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for index_zomb in range(self.num_zombies()):
            c_zomb = self._zombie_list[index_zomb]
            print "Zomb ", c_zomb
            if human_distance_field[c_zomb[0]][c_zomb[1]] != 0 and self.num_zombies() != 0:
                neighbors_full = self.four_neighbors(c_zomb[0], c_zomb[1])
                neighbors = [cell for cell in neighbors_full if \
                             human_distance_field[cell[0]][cell[1]] != self._grid_width * self._grid_height]
                print "Neighbors_full ", neighbors_full 
                print "Neighbors ", neighbors
                distances = [human_distance_field[cell[0]][cell[1]] for cell in neighbors]
                if len(distances) > 0:
                    min_dist =  min(distances)
                    print "Distances ", distances, " Min ", min_dist
                    moves = [neighbors[ind] for ind in range(len(distances)) if distances[ind] == min_dist]
                    move = random.choice(moves)
                    print "Moves ", moves, " Move ", move
                    self._zombie_list[index_zomb] = move



# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Apocalypse(30, 40))

#poc_zombie_gui.run_gui(Apocalypse(3, 3, [(0, 0), (0, 1), (0, 2), (1, 0)], [(2, 1)], [(1, 1)]))
#dist0 = [[9, 9, 9], [9, 1, 2], [1, 0, 1]]
#game0.move_humans(dist0)
#print game0
# expected location to be one of [(1, 2)] but received (0, 1)

#poc_zombie_gui.run_gui(Apocalypse(3, 3, [(0, 1), (1, 2), (2, 1)], [(0, 2)], [(1, 1)]))
# while testing obj.zombies: (ValueError) min() arg is an empty sequence at line 178, in move_zombies

#poc_zombie_gui.run_gui(Apocalypse(3, 3, [(0, 0), (0, 1), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)], [(0, 2)], [(1, 1)]))
# dist = [[9, 9, 0], [9, 9, 9], [9, 9, 9]]
# obj.move_humans(dist) then obj.humans() expected location to be one of [(1, 1)] but received (0, 2)




        

