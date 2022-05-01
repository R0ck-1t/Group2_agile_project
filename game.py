from src.globalmap import GlobalMap
from src.character import Character
import time

class Game():
    def __init__(self):
        self.start_time = time.time()
        self.start_time -= 960
        #name = input("What is your name?")
        self.character = Character('name')
        impassables = [[5, 11], [5, 12], [5, 13], [6, 10], [6, 11], [6, 12], [6, 13], [7, 10], [7, 11], [7, 13], [8, 11], [8, 13]]
        file = "./src/asciimap.txt"
        trails = [ [1, 11], [2, 11], [3, 7], [3, 8], [3, 9], [3, 10], [3, 11], [4, 4], [4, 5], [4, 7], [5, 7], [6, 7], [7, 6], [7, 7], [8, 6], [9, 6], [10, 6], [11, 5], [11, 6], [11, 7], [11, 8], [11, 9], [12, 5], [12, 9], [12, 10], [12, 11], [12, 12], [12, 13], [12, 14], [13, 5], [13, 14], [14, 5], [15, 5] ]
        forest = [ [10, 14], [10, 15], [11, 11], [11, 12], [11, 13], [11, 14], [11, 15], [12, 15], [13, 10], [13, 11], [13, 13], [13, 15], [14, 9], [14, 10], [14, 11], [14, 12], [14, 13], [14, 15], [15, 9], [15, 10], [15, 11], [15, 12], [15, 13], [15, 14], [15, 15] ]
        instances = [ [4, 3], [7, 12], [13, 12], [14, 14], [15, 6] ]
        bridges= [ [4, 6] ]
        waters = [ [1, 6], [1, 7], [2, 6], [2, 7], [3, 6], [5, 6], [6, 6], [7, 6], [8, 1], [8, 4], [8, 5], [9, 1], [9, 2], [9, 3], [9, 4], [10, 1], [10, 2], [10, 3], [10, 4], [11, 1], [11, 2], [11, 3], [12, 1], [12, 2], [12, 3], [13, 1], [13, 2] ]
        self.map = GlobalMap(filename=file, bridges=bridges, waters=waters, trails=trails, instances=instances, forest=forest, impassables=impassables)

    def get_name_and_difficulty(self):
        pass
    

    def get_time(self):
        time_elapsed = time.time() - self.start_time
        hours = int(time_elapsed) // 120
        days = hours // 24
        hours = hours % 24
        minutes = (time_elapsed % 120) / 2

        return f"0{int(days)}:0{int(hours)}:{int(minutes)}"
    
    def get_command(self, input: str):
        print('\n' * 1000)
        check_prefixes = ['check', 'view', 'see', 'open', 'show']
        move_prefixes = ['go', 'head', 'move', 'travel']
        time_postfixes = ['time', 'date', 'day', 'hour']
        inventory_postfixes = ['bag', 'inventory', 'backpack', 'sack', 'pack']
        character_postfixes = ['character', 'health', 'stats', 'xp', 'exp', 'level', 'lvl', 'experience', 'progress', 'char', str(self.character.name).lower()]
        gear_postfixes = ['gear', 'equipped', 'equipment', 'items', 'garb', 'armor', 'weapon']
        north = ['up', 'north']
        south = ['down', 'south']
        west = ['left', 'west']
        east = ['right', 'east']
        if input == 'help':
            print("Available Prefixes: ")
            print(check_prefixes, move_prefixes)
            print("Available Postfixes")
            print(character_postfixes, inventory_postfixes, time_postfixes)
            return 1
        command_list = input.split()
        prefix = command_list[0]
        postfix = command_list[1]

        if len(command_list) != 2:
            return 0
        if prefix in check_prefixes:
            if postfix in time_postfixes:
                print(self.get_time())
                return 1
            elif postfix in inventory_postfixes:
                print("No method as of yet")
                return 1
            elif postfix in character_postfixes:
                print(self.character)
                return 1
            elif postfix in gear_postfixes:
                print(self.character.show_equipment())
                return 1
            else:
                return 3
        elif prefix in move_prefixes:
            if postfix in north:
                self.map.move('north')
                self.map.map_graphics.print_tiles(self.map.location)
                return 1
            elif postfix in south:
                self.map.move('south')
                self.map.map_graphics.print_tiles(self.map.location)
                return 1
            elif postfix in west:
                self.map.move('west')
                self.map.map_graphics.print_tiles(self.map.location)
                return 1
            elif postfix in east:
                self.map.move('east')
                self.map.map_graphics.print_tiles(self.map.location)
                return 1
            else:
                return 3





def main():
    

    game = Game()
    while True:
        try:
            command = input("\n\nWhat would you like to do?\n>").lower()
            s = game.get_command(command)
        # COMMANDS: 
        # Moving: Prefixes(move, go, head) Postfixes(north, south, west, east, up, down, left, right)
        # Doing: Prefixes(check, view) Postfixes(inventory, time, health, status, character)
        except (IndexError, ValueError):
            print(f"{command} what, where, who... How??")
        if s == 3:
            print("Error, Invalid Command.")




if __name__ == '__main__':
    main()
    pass