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
# 15 | 0  0  0  0  P  B  0  0  1  1  1  1  1  1  1  |
#    |----------------------------------------------|

from src.asciimap import AsciiMap

class GlobalMap():
    
    def __init__(self): 
        """Assigns tiles to a labeled list via their coordinates. 
        Generates the largest type of tiles (plains) by checking if generated tiles are already in use.
        
        Maybe will have a list of available spawn points? Or have one that is fixed? Or random depending on difficulty.
        
        """
        self.file_name = "./src/asciimap.txt"
        self.limits = [15, 15]
        self.exits = [0, 0]
        self.old_location = [1, 11]
        self.new_location = [1, 11]
        self.location = [1, 11]
        self.enemies = [[2, 11]]
        self.enemy_fight = False
        self.water = [[1, 6], [1, 7], [2, 6], [3, 6], [5, 6], [5, 5], [6, 5], [7, 5], [7, 4], [7, 1], [8, 1], [8, 2], [8, 3], [8, 4], [9, 1], [9, 2], [9, 3], [9, 4], [10, 1], [10, 2], [10, 3], [11, 1], [11, 2], [11, 3], [12, 1], [12, 2]]
        self.instances = [[3, 3], [14, 6], [13, 15], [7, 12], [12, 12]]
        self.bridge = [[4, 6]]
        self.impassable = [[1, 6], [1, 7], [2, 6], [3, 6], [5, 6], [5, 5], [6, 5], [7, 5], [7, 4], [7, 1], [8, 1], [8, 2], [8, 3], [8, 4], [9, 1], [9, 2], [9, 3], [9, 4], [10, 1], [10, 2], [10, 3], [11, 1], [11, 2], [11, 3], [12, 1], [12, 2], [4, 11], [4, 12], [4, 13], [5, 10], [5, 11], [5, 12], [5, 13], [5, 14], [6, 10], [6, 11], [6, 12], [6, 13], [6, 14], [7, 11], [7, 13]]
        self.trail = [[1, 11], [2, 11], [2, 10], [2, 9], [2, 9], [2, 7], [3, 7], [3, 5], [3, 4], [4, 7], [5, 7], [6, 7], [6, 6], [7, 6], [8, 6], [9, 6], [10, 5], [10, 6], [10, 7], [10, 8], [10, 9], [11, 9], [11, 10,], [11, 11], [11, 12], [11, 13], [11, 14], [11, 15], [12, 15], [11, 5], [12, 5], [13, 5], [14, 5]]
        self.forest = [[9, 15], [10, 11], [10, 12], [10, 13], [10, 14], [10, 15], [12, 10], [12, 11], [12, 13], [12, 14], [13, 10], [13, 11], [13, 12], [13, 13], [13, 14], [14, 9], [14, 10], [14, 11], [14, 12], [14, 13], [14, 14], [14, 15], [15, 9], [15, 10], [15, 11], [15, 12], [15, 13], [15, 14], [15, 15]]
        plains = []
        for i in range(1, 16):
            for j in range(1, 16):
                x = [i, j]
                if x in self.water:
                    pass
                elif x in self.instances:
                    pass
                elif x in self.impassable:
                    pass
                elif x in self.trail:
                    pass
                elif x in self.forest:
                    pass
                elif x in self.bridge:
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
            if item in self.water:
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
        if coord in self.impassable:
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
        if coord in self.enemies:
            self.enemy_fight = True
        return 1

    def enter_instance(self, enter=[]):
        """Enters a nested map or instance.
        """
        pass


class MapInstance(GlobalMap):
    """child class for nested maps"""
    def __init__(self):
        pass