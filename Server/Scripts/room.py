from Scripts import item

class Room:

    def __init__(self, name, description, look_description, north="", south="", east="", west="", room_items={}):
        self.name = name
        self.description = description
        self.look_description = look_description

        # Create a dictionary with up to four connections
        self.connections = dict()
        # Each direction key can be assigned a room name key that
        # can be accessed in order to change rooms later
        self.connections["north"] = north
        self.connections["south"] = south
        self.connections["east"] = east
        self.connections["west"] = west

        self.room_items = room_items


class DungeonRooms:

    def __init__(self):

        self.dungeonItems = item.DungeonItems()

        # Create a basic dungeon using the Room Class
        self.room_1 = Room("Entry Gate", "You stand at the entrance to town...\n",
                           "\nYou are at the Entry Gate.\n"
                           "You see a street to the north.\n",
                           north="South Street",
                           south="",
                           east="",
                           west="",
                           room_items={"Apple": self.dungeonItems.food_01})

        self.room_2 = Room("Large Well", "You gaze into the deepest, darkest well you have ever seen...\n",
                           "\nYou are at the Large Well.\n"
                           "You see a Tavern north of you.\n",
                           north="The Davy Lamp",
                           south="",
                           east="",
                           west="",
                           room_items={"Longsword": self.dungeonItems.sword_01})

        self.room_3 = Room("Helpington's General Store", "You enter the general store...\n",
                           "\nYou are at Helpington's General Store.\n"
                           "There is a street east of you. \n",
                           north="",
                           south="",
                           east="South Street",
                           west="")

        self.room_4 = Room("South Street", "You stand at the south end of a busy street...\n",
                           "\nYou are at the south end of a long street.\n"
                           "You see a Clock Tower to the north of you in the centre of town. \n"
                           "There is a store to the west. \n"
                           "There is a Tavern to the east. \n"
                           "There is the entrance to town in the south. \n",
                           north="Clock Tower",
                           south="Entry Gate",
                           east="The Davy Lamp",
                           west="Helpington's General Store")

        self.room_5 = Room("The Davy Lamp", "You enter a dingy tavern full of drunkards...\n",
                           "\nYou are at the Tavern, 'The Davy Lamp'.\n"
                           "There is a Large Well south of you. \n"
                           "You see a street to the west. \n",
                           north="",
                           south="Large Well",
                           east="",
                           west="South Street")

        self.room_6 = Room("Bank", "You enter a small Bank...\n",
                           "\nYou are at the Bank.\n"
                           "You see a Clock Tower to the east of you. \n"
                           "There is a street south of you. \n",
                           north="",
                           south="",
                           east="Clock Tower",
                           west="")

        self.room_7 = Room("Clock Tower", "You stare up at the giant Clock...\n",
                           "\nYou are at the Clock Tower.\n"
                           "You see a street to the north. \n"
                           "There is a street to the south. \n"
                           "The Sherrif's Office is east of you. \n"
                           "There is a Bank to the west. \n",
                           north="North Street",
                           south="South Street",
                           east="Sherrif's Office",
                           west="Bank")

        self.room_8 = Room("Sherrif's Office", "Tou enter the Sherrif's Office...\n",
                           "\nYou are at the Sherrif's Office.\n"
                           "You see a Clock Tower west of you. \n",
                           north="",
                           south="",
                           east="",
                           west="Clock Tower")

        self.room_9 = Room("Fallen Temple", "Tou enter a large Temple that's seen better days...\n",
                           "\nYou are at the Fallen Temple.\n"
                           "You see a street east of you. \n"
                           "You see a Cave someways north of your position. \n",
                           north="Cave",
                           south="",
                           east="North Street",
                           west="")

        self.room_10 = Room("North Street", "You enter the north end of the street. \n",
                           "\nYou are at the Northern Street.\n"
                           "You see a large Manor north of you. \n"
                           "There is a Clock Tower south of you. \n"
                           "You see a Quarry far off in the east. \n"
                           "You can see a Temple far off in the distance west of you. \n",
                           north="Elder's Manor",
                           south="Clock Tower",
                           east="Quarry",
                           west="Fallen Temple")

        self.room_11 = Room("Quarry", "Tou enter a deep Quarry...\n",
                           "\nYou are at the Quarry.\n"
                           "You see a street far off to the west of you. \n",
                           north="",
                           south="",
                           east="",
                           west="North Street")

        self.room_12 = Room("Cave", "Tou see the entrance to a dark cave\n",
                           "\nYou are at the cave.\n"
                           "You see a Temple south of you. \n"
                           "You see a small hut to the east in the forest. \n",
                           north="",
                           south="Fallen Temple",
                           east="Witch's Hut",
                           west="")

        self.room_13 = Room("Witch's Hut", "Tou stand at the Witch's Hut...\n",
                           "\nYou are deep in the forest outside a small hut.\n"
                           "You see a farm in the clearing north of you \n"
                           "The cave is westward. \n",
                           north="Stonefruit Farm",
                           south="",
                           east="",
                           west="Cave")

        self.room_14 = Room("Elder's Manor", "Tou stand infront of a large Manor...\n",
                           "\nYou are at the Elder's Manor.\n"
                           "You see a street to the south. \n",
                           north="",
                           south="North Street",
                           east="",
                           west="")

        self.room_15 = Room("Stonefruit Farm", "Tou enter the clearing to find a small farm...\n",
                           "\nYou are at Stonefruit Farm.\n"
                           "You see a hut in the forest to the south. \n",
                           north="",
                           south="Witch's Hut",
                           east="",
                           west="")

        self.room_16 = Room("The Void", "Tou open your eyes to a room make of light and nothing else...\n",
                            "\nYou see white light in every direction and a frail figure in the middle of the room.\n"
                            "'...Find Me...'",
                            north="Entry Gate",
                            south="Entry Gate",
                            east="Entry Gate",
                            west="Entry Gate")



