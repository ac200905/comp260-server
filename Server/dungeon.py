import room

class Dungeon:

    def __init__(self, name, player):

        self.name = name
        self.player = player
        self.rooms_dict = {}

        self.dungeon_description =  "--------------------------------------------------------------\n" \
                                    "You travel miles in search of a new place to call home. \n" \
                                    "Eventually you come across a small town. \n" \
                                    "You stand underneath the Southern Entry Gate. \n" \
                                    "---------------------------------------------------------------\n"
        self.dungeon_rooms = room.DungeonRooms()

        self.starting_room = ''

        self.moves_available = 8

        self.moves_taken = 0

    def setup_dungeon(self):
        # Populate the rooms dictionary with
        self.rooms_dict["Entry Gate"] = self.dungeon_rooms.room_1
        self.rooms_dict["Large Well"] = self.dungeon_rooms.room_2
        self.rooms_dict["Helpington's General Store"] = self.dungeon_rooms.room_3
        self.rooms_dict["South Street"] = self.dungeon_rooms.room_4
        self.rooms_dict["The Davy Lamp"] = self.dungeon_rooms.room_5
        self.rooms_dict["Bank"] = self.dungeon_rooms.room_6
        self.rooms_dict["Clock Tower"] = self.dungeon_rooms.room_7
        self.rooms_dict["Sherrif's Office"] = self.dungeon_rooms.room_8
        self.rooms_dict["Fallen Temple"] = self.dungeon_rooms.room_9
        self.rooms_dict["North Street"] = self.dungeon_rooms.room_10
        self.rooms_dict["Quarry"] = self.dungeon_rooms.room_11
        self.rooms_dict["Cave"] = self.dungeon_rooms.room_12
        self.rooms_dict["Witch's Hut"] = self.dungeon_rooms.room_13
        self.rooms_dict["Elder's Manor"] = self.dungeon_rooms.room_14
        self.rooms_dict["Stonefruit Farm"] = self.dungeon_rooms.room_15
        self.rooms_dict["The Void"] = self.dungeon_rooms.room_16

        # The room the player will begin in
        self.starting_room = self.rooms_dict["Entry Gate"].name

    def change_room(self, current_room, direction):
        # Use the dictionary of rooms and dictionary of room connections to
        # establish the new room
        new_room = self.rooms_dict[current_room].connections[direction]


        # If the connection key is not empty
        if new_room != "":

            self.player.input.output = "\nYou make your way " + direction + "\n" \
                                       + self.rooms_dict[new_room].description

            self.player.input.last_room = current_room

            # Timer for dungeon reset
            self.moves_taken = self.moves_taken + 1

            if self.moves_taken >= self.moves_available:

                self.reset_dungeon()
                # Send player to the void
                new_room = self.rooms_dict["The Void"].name

                return self.rooms_dict[new_room].name

            else:

                # Return the new room name
                return self.rooms_dict[new_room].name

        else:
            self.player.input.output = "\nNothing of interest that way... " \
                                       "\nTry another direction."
            return current_room

    def reset_dungeon(self):
        self.moves_taken = -1
        self.player.input.output = "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
                                   "You hear the clock strike twelve...\n" \
                                   "As it does the ground cracks beneath you and hot lava spews into the air.\n" \
                                   "The town, now engulfed in flame, sinks into the ground dragging you down \n" \
                                   "with it... then you awaken in a strange but familiar place...\n" \
                                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"


