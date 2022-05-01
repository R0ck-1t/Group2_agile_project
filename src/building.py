
class Building():

    def __init__(self, name, building_type="inn", store_inventory=[], npcs_here=[]):
        """Building has npcs inside + store inventory if available."""
        self.name = name
        self.type = building_type

    def __repr__(self):
        """Prints the name of the building and it's type. Will be used in the village function to print list of buildings."""
        return "Name: " + str(self.name) + " | Type: " + str(self.type)
    

    def shop_instance(self):
        """Shop loop when you are trying to purchase from a building."""
        pass
    
    def enter_building(self, char):
        print('\n' * 1000)
        check_prefixes = ['check', 'view', 'see', 'open', 'show']
        time_postfixes = ['time', 'date', 'day', 'hour']
        inventory_postfixes = ['bag', 'inventory', 'backpack', 'sack', 'pack']
        character_postfixes = ['character', 'health', 'stats', 'xp', 'exp', 'level', 'lvl', 'experience', 'progress', 'char', str(self.character.name).lower()]
        gear_postfixes = ['gear', 'equipped', 'equipment', 'items', 'garb', 'armor', 'weapon']
        if input == 'help':
            print("Available Prefixes: ")
            print(check_prefixes)
            print("Available Postfixes")
            print(character_postfixes, inventory_postfixes, time_postfixes)
            print("To leave: 'exit'")
            return 1
        
        
        command_list = input.split()
        if len(command_list) != 2:
            return 0
        prefix = command_list[0]
        postfix = command_list[1]

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
            