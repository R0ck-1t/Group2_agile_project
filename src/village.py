from src.building import Building
from src.globalmap import GlobalMap
from src.character import Character
#      1 2 3 4 5 6
#    X X X X X X X X    *Rockstone Village*
# 1  X X ^ X E X X X    E = Exit
# 2  X X 0 X 0 M X X    X = Impassable
# 3  X E 0 0 0 0 E X    T = Tavern/Inn
# 4  X X 0 X 0 X X X    M = Market  
# 5  X T 0 X E X X X    ^ = Village Leader
#    X X X X X X X X    0 = Roads

rockstone_exits = [[1, 4], [3, 6], [5, 4], [3, 1]]
rockstone_roads = [[2, 2], [2, 4], [3, 2], [3, 3], [3, 4], [3, 5], [4, 2], [4, 4], [5, 2]]
rockstone_instances = [[1, 2], [5, 1], [2, 5]]
rockstone_limits = [5, 6]

#rockstone_village = Village('Rockstone Village')


class Village(GlobalMap):
    
    def __init__(self, name: str, buildings, map, exits: list, roads: list, instances: list, limits=[0, 0]):
        """Constructor for the village. More to do"""
        self.name = name
        self.buildings = buildings
        self.map = map
        self.exits = exits
        self.roads = roads
        self.instances = instances
        impassable = []
        self.inside = True
        for i in range(1, limits[0] + 1):
            for j in range(1, limits[1] + 1):
                coords = [i, j]
                if (coords not in self.exits) and (coords not in self.roads) and (coords not in self.instances):
                    impassable.append(coords)
        self.impassable = impassable
        print(self.exits)
        print(self.roads)
        print(self.instances)
        print(self.impassable)

    def move(self, direction): #Moves inside village. Village will need its own commands
        """
        Moves from one 'tile' to an adjacent one on the map. Ensures the tile is available and allows movement
        
        direction arg: 'north', 'south', 'west', or 'east'
        """
        if direction == 'north':
            self.new_location = self.location
            self.new_location[0] -= 1
        elif direction == 'south':
            self.new_location = self.location
            self.new_location[0] += 1
        elif direction == 'west':
            self.new_location = self.location
            self.new_location[1] -= 1
        elif direction == 'east':
            self.new_location = self.location
            self.new_location[1] += 1
        
        check = self.check_valid(self.new_location)
        if check == 1:
            self.location = self.new_location
            print(f"Moved to {self.new_location}")
        elif check == 0:
            print("Unable to move in this direction!")
        elif check == 2:
            pass


    def exit(self, direction=''):
        """Exits village and goes back to main map. Will need to determine adj tile to spit the player onto."""
        pass

    def get_buildings(self):
        """Gets a list of building names in the town with their building type"""
        return_string = "Buildings in this town:\n" + str(self.buildings[0])
        if len(self.buildings) > 1:
            for i in range(1, len(self.buildings)):
                return_string += f", {self.buildings[i]}" 
        return print(return_string)

    def __repr__(self) -> str:
        """Dunder method, prints the village name when you try to print the object"""
        return "Village: " + str(self.name)

    
    def enter_village(self, vill_coords):
        pass


    def enter_building(self, building: Building, character: Character):
        pass

