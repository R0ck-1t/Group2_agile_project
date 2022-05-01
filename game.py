from src.globalmap import GlobalMap
from src.character import Character
import time

class Game():
    def __init__(self):
        self.start_time = time.time()
        self.start_time -= 960
        #name = input("What is your name?")
        self.character = Character('name')
        self.map = GlobalMap()

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