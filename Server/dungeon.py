
''' #==============================================================================

Dungeon Setup

''' #==============================================================================

class Room:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.players = []
        self.connected_rooms = {}

    def set_room(self, room_name, rooms, description):
        self.name = room_name
        self.connected_rooms = rooms
        self.description = description

class DungeonRooms:

    def __init__(self):
        self.name = ""
        self.rooms = {}
        self.players = []

    # Creates a bespoke Dungeon
    def setup_dungeon(self, DungeonName):

        self.name = DungeonName

        room_1 = Room()
        room_1.set_room("Entry Gate",
                        {"north": "South Street"},
                        "\nYou are at the Entry Gate.\n"
                        "You see a street to the north.\n")

        room_2 = Room()
        room_2.set_room("Large Well",
                        {"north": "The Davy Lamp"},
                        "\nYou are at the Large Well.\n"
                        "You see a Tavern north of you.\n")

        room_3 = Room()
        room_3.set_room("Helpington's General Store",
                        {"east": "South Street"},
                       "\nYou are at Helpington's General Store.\n"
                        "There is a street east of you. \n")

        room_4 = Room()
        room_4.set_room("South Street",
                        {"north": "Clock Tower", "south": "Entry Gate", "east": "The Davy Lamp", "west": "Helpington's General Store"},
                       "\nYou are at the south end of a long street.\n"
                        "You see a Clock Tower to the north of you in the centre of town. \n"
                        "There is a store to the west. \n"
                        "There is a Tavern to the east. \n"
                        "There is the entrance to town in the south. \n")

        room_5 = Room()
        room_5.set_room("The Davy Lamp",
                        {"south": "Large Well",
                        "west": "South Street"},
                       "\nYou are at the Tavern, 'The Davy Lamp'.\n"
                        "There is a Large Well south of you. \n"
                        "You see a street to the west. \n")

        room_6 = Room()
        room_6.set_room("Bank",
                        {"east": "Clock Tower"},
                       "\nYou are at the Bank.\n"
                        "You see a Clock Tower to the east of you. \n"
                        "There is a street south of you. \n")

        room_7 = Room()
        room_7.set_room("Clock Tower",
                        {"north": "North Street", "south": "South Street", "east": "Sherrif's Office", "west": "Bank"},
                       "\nYou are at the Clock Tower.\n"
                        "You see a street to the north. \n"
                        "There is a street to the south. \n"
                        "The Sherrif's Office is east of you. \n"
                        "There is a Bank to the west. \n")

        room_8 = Room()
        room_8.set_room("Sherrif's Office",
                        {"west": "Clock Tower"},
                       "\nYou are at the Sherrif's Office.\n"
                        "You see a Clock Tower west of you. \n")

        room_9 = Room()
        room_9.set_room("Fallen Temple",
                        {"north": "Cave", "east": "North Street"},
                       "\nYou are at the Fallen Temple.\n"
                        "You see a street east of you. \n"
                        "You see a Cave someways north of your position. \n")

        room_10= Room()
        room_10.set_room("North Street",
                         {"north": "Elder's Manor", "south": "Clock Tower", "east": "Quarry", "west": "Fallen Temple"},
                       "\nYou are at the Northern Street.\n"
                        "You see a large Manor north of you. \n"
                        "There is a Clock Tower south of you. \n"
                        "You see a Quarry far off in the east. \n"
                        "You can see a Temple far off in the distance west of you. \n")

        room_11 = Room()
        room_11.set_room("Quarry",
                         {"west": "North Street"},
                        "\nYou are at the Quarry.\n"
                        "You see a street far off to the west of you. \n")

        room_12 = Room()
        room_12.set_room("Cave",
                         {"south": "Fallen Temple", "east": "Witch's Hut"},
                        "\nYou are at the cave.\n"
                        "You see a Temple south of you. \n"
                        "You see a small hut to the east in the forest. \n")

        room_13 = Room()
        room_13.set_room("Witch's Hut",
                         {"north": "Stonefruit Farm","west": "Cave"},
                        "\nYou are deep in the forest outside a small hut.\n"
                        "You see a farm in the clearing north of you \n"
                        "The cave is westward. \n")

        room_14 = Room()
        room_14.set_room("Elder's Manor",
                         {"south": "North Street"},
                        "\nYou are at the Elder's Manor.\n"
                        "You see a street to the south. \n")

        room_15 = Room()
        room_15.set_room("Stonefruit Farm",
                         {"south": "Witch's Hut"},
                        "\nYou are at Stonefruit Farm.\n"
                        "You see a hut in the forest to the south. \n")

        room_16 = Room()
        room_16.set_room("The Void",
                         {"north": "Entry Gate", "south": "Entry Gate", "east": "Entry Gate", "west": "Entry Gate"},
                        "\nYou see white light in every direction and a frail figure in the middle of the room.\n"
                        "'...Find Me...'")


        self.rooms = {"Entry Gate": room_1, "Large Well": room_2, "Helpington's General Store": room_3,
                      "South Street": room_4, "The Davy Lamp": room_5, "Bank": room_6, "Clock Tower": room_7,
                      "Sherrif's Office": room_8, "Fallen Temple": room_9, "North Street": room_10,
                      "Quarry": room_11, "Cave": room_12, "Witch's Hut": room_13, "Elder's Manor": room_14,
                      "Stonefruit Farm": room_15, "The Void": room_16}
