# V = Village ( Opens Nested Map )
# M = Mountain Cave Entrance
# X = IMPASSABLE TERRAIN
# W = Water
# 0 = Plains
# 1 = Forest
# C = Cave
# S = Spawn
# P = Path
# B = Bridge
#      1  2  3  4  5  6  7  8  9  10 11 12 13 14 15  
#    |----------------------------------------------|
#  1 | 0  0  0  0  0  W  W  0  0  0  P  0  0  0  0  |
#  2 | 0  0  0  0  0  W  W  0  0  0  P  0  0  0  0  |
#  3 | 0  0  0  0  0  W  P  P  P  P  P  0  0  0  0  |
#  4 | 0  0  V  P  P  B  P  0  0  0  0  0  0  0  0  |
#  5 | 0  0  0  0  0  W  P  0  0  0  X  X  X  0  0  |
#  6 | 0  0  0  0  0  W  P  0  0  X  X  X  X  0  0  |
#  7 | 0  0  0  0  W  P  P  0  0  X  X  M  X  0  0  |
#  8 | W  0  0  W  W  P  0  0  0  0  X  0  X  0  0  |
#  9 | W  W  W  W  0  P  0  0  0  0  0  0  0  0  0  |
# 10 | W  W  W  W  0  P  0  0  0  0  0  0  0  1  1  |
# 11 | W  W  W  0  P  P  P  P  P  0  1  1  1  1  1  |
# 12 | W  W  W  0  P  0  0  0  P  P  P  P  P  P  1  |
# 13 | W  W  0  0  P  0  0  0  0  1  1  C  1  P  1  |
# 14 | 0  0  0  0  P  0  0  0  1  1  1  1  1  V  1  |
# 15 | 0  0  0  0  P  V  0  0  1  1  1  1  1  1  1  |
#    |----------------------------------------------|

from src.asciimap import AsciiMap

class GlobalMap():
    
    def __init__(self, filename : str, trails=[], waters=[], forest=[], instances=[], bridges=[], impassables=[]): 
        """Assigns tiles to a labeled list via their coordinates. 
        Generates the largest type of tiles (plains) by checking if generated tiles are already in use.
        
        Maybe will have a list of available spawn points? Or have one that is fixed? Or random depending on difficulty.
        
        """
        self.file_name = filename
        self.limits = [15, 15]
        self.exits = [0, 0]
        self.old_location = [1, 11]
        self.new_location = [1, 11]
        self.location = [1, 11]

        # Water, Trail, Forest, Bridge, Impassable, Instances (Instances will be determined by their index number/coords).
        self.waters = waters
        self.instances = instances
        self.bridges = bridges
        self.impassables = impassables
        self.trails = trails
        self.forest = forest
        plains = []
        for i in range(0, self.limits[1]):
            for j in range(0, self.limits[0]):
                x = [i + 1, j + 1]
                if x in self.waters:
                    pass
                elif x in self.instances:
                    pass
                elif x in self.impassables:
                    pass
                elif x in self.trails:
                    pass
                elif x in self.forest:
                    pass
                elif x in self.bridges:
                    pass
                else: 
                    plains.append(x)
        self.plains = plains
        self.map_graphics = AsciiMap(self.limits, self.file_name)

    def check_adjacent_tiles(self):
        """Checks if type of tile is adjacent to your current tile. Maybe useful for items like fishing?
        returns 1 if a matching tile is adjacent
        CHECKS ONLY FOR WATER RIGHT NOW."""
        up = self.location
        up[0] -= 1
        down = self.location
        down[0] += 1
        left = self.location
        left[1] -= 1
        right = self.location
        right[1] += 1
        adjacent_tiles = [up, down, left, right]
        for item in adjacent_tiles:
            if item in self.waters:
                return True
        

    def move(self, direction):
        """
        Moves from one 'tile' to an adjacent one on the map. Ensures the tile is available and allows movement
        
        direction arg: 'north', 'south', 'west', or 'east'
        """
        self.old_location = self.location
        if direction == 'north':
            self.new_location = [self.location[0], self.location[1]]
            self.new_location[0] -= 1
        elif direction == 'south':
            self.new_location = [self.location[0], self.location[1]]
            self.new_location[0] += 1
        elif direction == 'west':
            self.new_location = [self.location[0], self.location[1]]
            self.new_location[1] -= 1
        elif direction == 'east':
            self.new_location = [self.location[0], self.location[1]]
            self.new_location[1] += 1
        
        print(f"Old: {self.old_location}\nCurrent: {self.location}\nNew: {self.new_location}")
        check = self.check_valid(self.new_location)
        if check == 1:
            self.location = self.new_location
            print(self)
        elif check == 0:
            print("Unable to move in this direction!")
            self.location = self.old_location
            print(self)
            print(f"Old: {self.old_location}\nCurrent: {self.location}\nNew: {self.new_location}")
        else:
            self.location = self.new_location
            self.enter_instance(self.old_location)
        
    def __repr__(self):
        return str(f"{str(self.map_graphics.print_tiles(self.location))}\n\nCurrent Location: {str(self.location)}")
    
    def check_valid(self, coord):
        #Invalid = 0, Valid = 1, Instance = 2, Exit = 3
        if coord in self.impassables:
            return 0
        elif coord in self.instances:
            return 2
        elif coord in self.exits:
            return 3
        else: 
            if (coord[0] < 1) or (coord[0] > self.limits[0]):
                return 0
            if (coord[1] < 1) or (coord[1] > self.limits[1]):
                return 0
        return 1

    def enter_instance(self, enter=[]):
        """Enters a nested map or instance.
        """
        pass


class MapInstance(GlobalMap):
    """child class for nested maps"""
    def __init__(self):
        pass