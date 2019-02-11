
class Item:

    def __init__(self, name, item_type, description, attack, defense):

        self.name = name
        self.item_type = item_type
        self.description = description
        self.attack = attack
        self.defense = defense

class DungeonItems:

    def __init__(self):
        self.sword_01 = Item("Shortsword", "Weapon", "A basic shortsword", 3, 1)
        self.sword_02 = Item("Longsword", "Weapon", "A basic longsword", 4, 2)
        self.food_01 = Item("Apple", "Food", "A tasty apple", 0, 0)