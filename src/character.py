# Authors: Peter Vanderhook and Victor Polemeni
# Date: March 11th, 2022
from src.item import Gear
class Character():
    
    def __init__(self, name):
        """Creates a character.
        Stats are stored in a dictionary.
        xp to next level increases on levelup, xp is not reset
        
        list for status effects, not sure how I will implement this yet. Maybe via 'time' module."""
        self.name = name
        self.level = 1
        self.coins = 0
        self.skills = { "attack": 4, 'strength': 3, "defense": 3, "wisdom": 3, "agility": 3, "luck": 3, "health": 10}
        self.exp = 0
        self.exp_to_level = 69
        self.inventory = []
        sack = Gear("Old Leather Pouch", capacity=4, value=2, weight=1, slot='back')
        dagger = Gear("Rusty Dagger", weight=1, stats={'attack': 1, 'strength': 0, 'defense': 0, 'wisdom': 0, 'agility': 0, 'luck': 0, 'health': 0}, slot='weapon')
        self.equipment = {'pouch': sack, 'helmet': None, 'armor': None, 'amulet': None, 'ring': None, 'gloves': None, 'back': None, 'boots': None, 'weapon': dagger, 'offhand': None}
        self.capacity = 4
       
        

    def unequip(self):
        print("Running")
        #add stat removal   
        self.show_equipment(True)
        slot = input("\nWhat 'slot' would you like to unequip?\n>").lower()
        if slot == 'pouch':
            print("Unable to manipulate this slot.")
            return 0
        else:
            if slot in self.equipment:
                if self.equipment[slot] != None:
                    if len(self.inventory) >= (self.capacity - self.equipment[slot].capacity):
                        print("Unable to unequip, no space in your inventory!")
                        return 0
                    else:
                        self.inventory.append(self.equipment[slot])
                        for stat_boost in self.equipment[slot].stats:
                            if self.equipment[slot].stats[stat_boost] > 0:
                                self.skills[stat_boost] -= self.equipment[slot].stats[stat_boost]
                        print("Unequipped your " + str(self.equipment[slot]) + ".")
                        self.equipment[slot] = None
                        return
                else:
                    print("Slot is already empty!")
                    return 0
            else:
                print("Please enter a valid slot.")
                return 0
    
    def show_inventory(self):
        silver = self.coins % 100
        gold = self.coins // 100
        print(f"You have {gold} gold and {silver} silver coins.")
        return_string = ""
        for item in self.inventory:
            return_string += f"'{str(item.name)}'\n"
        if return_string == "":
            print("Your inventory is empty!")
        else:
            print("Items in inventory:")
            print(return_string)

    def manage_inventory(self):
        print(f"You have {len(self.inventory)} items and have space for {str(self.capacity)} in total")
        manage = True
        while manage:
            try:
                choice = input("What would you like to do?\n'equip', 'unequip', 'view', 'discard', 'use'\n>").lower()
            except:
                print("Please enter a valid choice.")
                continue
            if choice == 'view':
                self.show_inventory()
            elif choice == 'unequip':
                self.unequip()
            elif choice == 'equip':
                self.show_inventory()
                print()
            elif choice == 'use':
                print("Incomplete method")
            elif choice == 'discard':
                print("Incomplete method")
            else:
                print("Please pick a valid choice")
                

    def equip(self):
        self.show_inventory()
        item_name = input("What item would you like to equip?\n>").lower()
        for check_item in self.inventory:
            if str(check_item.name).lower() == item_name:
                item = check_item
                break
        try:
            if self.equipment[str(item.slot)] != None:
                print("Equipment slot is already occupied!")
                return 0
            self.equipment[str(item.slot)] = item
            try:
                pop_num = self.inventory.index(item)
            except ValueError:
                print("Something went wrong, unable to find item in inventory.")
                return 0
                
            self.inventory.pop(pop_num)
            self.capacity += item.capacity

            for stat_boost in item.stats:
                if item.stats[stat_boost] > 0:
                    self.skills[stat_boost] += item.stats[stat_boost]

            #add actual stat boosts
            print("Equipped " + str(item.name))

        except KeyError:
            print("Unable to equip this item.")
            return 0
        

    def level_up(self):
        """Levels up. Run this function after xp gain if xp > exp to level.

        Grants 2 skill points and runs loop forcing the user to assign all points
        """
        self.exp_to_level = round(self.exp_to_level * 1.44)
        skillpoints = 2
        while skillpoints > 0:
            try:
                print(f"Skills:\nAttack - {self.skills['attack']}\nDefense - {self.skills['defense']}\nWisdom - {self.skills['wisdom']}\nAgility - {self.skills['agility']}\nHealth - {self.skills['health']} (+2 per skill point)\nLuck - {self.skills['luck']}")
                choice = input(f"What would you like to improve? You have {skillpoints} skill points.\nChoices: 'attack' 'defense' 'wisdom' 'agility' 'health' 'luck'").lower()
                if choice == "health":
                    self.skills['health'] += 2
                    skillpoints -= 1
                else:
                    self.skills[choice] += 1
                    skillpoints -= 1
                    continue
            except (AttributeError, KeyError):
                print("Please enter a valid choice")
                print('\n' * 100)
    
    
    def show_equipment(self, hide=False):
        for item in self.equipment:
            if str(item) == 'pouch':
                continue
            if self.equipment[str(item)] != None:
                print('\n' + str(self.equipment[str(item)]) + " equipped in the '"+ str(item) + "' slot.")
                for stat in self.equipment[str(item)].stats:
                    if self.equipment[str(item)].stats[str(stat)] > 0:
                        print(f"Grants +{self.equipment[str(item)].stats[str(stat)]} to {stat}.")
            else:
                if hide == False:
                    print('\n' + "Nothing equipped in the " + str(item) + " slot.")

    def discard(self):
        self.show_inventory()
        item_name = input("What item would you like to discard?\n>").lower()
        item = None
        for check_item in self.inventory:
            if str(check_item.name).lower() == item_name:
                item = check_item
                break
        if item == None:
            print("Unable to find item in inventory.")
            return 0
        else:
            while True:
                confirm = input(f"Are you sure you wish to discard {str(item.name)}?\n'yes', 'no'\n>").lower()
                if confirm == 'no':
                    self.discard()
                    return 
                elif confirm == 'yes':
                    print("Discarding...")
                    pop_num = self.inventory.index(item)
                    self.inventory.pop(pop_num)
                    break
    
    def __repr__(self):
        #make this look good later
        status_effects = ""
        return f"========== {self.name} ==========\nLevel: {self.level}   Progress: {self.exp}/{self.exp_to_level}\nStatus: {status_effects}\nHealth: {self.skills['health']}\nAttack: {self.skills['attack']}    Defense: {self.skills['defense']}\nStrength: {self.skills['strength']}    Wisdom: {self.skills['wisdom']}\nAgility: {self.skills['agility']}    Luck: {self.skills['luck']}\n========== {self.name} =========="
    

        

