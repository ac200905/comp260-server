import random

class Input:

    def __init__(self, player, dungeon):

        self.player = player
        self.dungeon = dungeon

        # Show the player available actions
        self.help_text = "----------------------------------------------------\n" \
                        "List Of Commands: \n" \
                        "Help           : ...fairly obvious \n" \
                        "Go <direction> : Can move north, south, east or west\n" \
                        "Look           : Survey the area\n" \
                        "Map            : See a map of the rooms \n" \
                        "Name <new name>: Change player name\n" \
                         "Say <words>    : Talk to other players in room\n" \
                         "Quit           : Quit game \n" \
                        "----------------------------------------------------"

        self.user_input = ''
        self.split_input = ''
        self.instruction = ''

        # A very basic layout of the dungeon
        self.map = "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
                   "	Stonefruit Farm                                                        \n" \
                   "	        |                                                               \n" \
                   "	        |                                                               \n" \
                   "Cave ------------- Witch's Hut                                                         \n" \
                   "  |  			                                                                       \n" \
                   "  |  			                                                                       \n" \
                   "Fallen Temple ------------- North Street -----------------------------------Quarry     \n" \
                   "    	                 |                                                     \n" \
                   "    	                 |                                                     \n" \
                   "                    Bank ------ Clock Tower ------ Sherrif's Office                        \n" \
                   "     	                 |                                                     \n" \
                   "        	                 |                                                     \n" \
                   "          Helpington's ---- South Street ------ The Davy Lamp                          \n" \
                   "    	                 |                              |                                \n" \
                   "    	                 |                              |                                \n" \
                   "                                    Entry Gate             Large Well                           \n" \
                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

        self.map_void = "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n\n\n\n\n" \
                        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        # string to output to the client
        self.output = ''
        self.output_to_all = ''

        self.current_time = ''

        self.last_room = ''

    def handle_input(self, user_input=""):
        #user_input = input("What will you do next? : ")
        # Convert user input to lower case
        user_input = user_input.lower()
        # Split user input into separate strings for each word
        split_input = user_input.split(' ')
        # Get the first word the user inputs, this is the action the user is taking
        instruction = split_input[0]

        if instruction == "quit" or instruction == "q" or instruction == "exit":
            self.output = "quit_game"

        elif instruction == "help":
            self.output = self.help_text

        elif instruction == "go" or instruction == "move":
            self.move_player(user_input)

        elif instruction == "look" or instruction == "look at" or instruction == "survey":
            self.look_at(user_input)

        elif instruction == "map":
            if self.player.current_room == "The Void":
                self.output = self.map_void
            else:
                self.output = self.map

        elif instruction == "name" and len(split_input) > 1:
            self.change_name(split_input[1])

        elif instruction == "say":
            self.say(self.player.name, split_input[1:])

        elif instruction == "kill":
            self.kill(user_input)

        elif instruction == "clock":
            self.output = "\nThe time is: 11:" + self.current_time +"\n"

        # If the user input isn't recognisable
        else:
            self.output = "No such command - Type 'help' for a list of commands."

    def move_player(self, user_input):
        # If the user inputs a valid direction, change the current room
        if "north" in user_input:
            self.player.current_room = self.dungeon.change_room(self.player.current_room, "north")
        elif "south" in user_input:
            self.player.current_room = self.dungeon.change_room(self.player.current_room, "south")
        elif "east" in user_input:
            self.player.current_room = self.dungeon.change_room(self.player.current_room, "east")
        elif "west" in user_input:
            self.player.current_room = self.dungeon.change_room(self.player.current_room, "west")

        else:
            self.output = "No such command - Type 'help' for a list of commands."

    def look_at(self, user_input):
        # Print the description of room connections
        self.output = self.dungeon.rooms_dict[self.player.current_room].look_description
        #return self.dungeon.rooms_dict[self.player.current_room].look_description

    def check_time(self, user_input):
        # Print the description of room connections
        if "clock" in user_input:
            self.output = "The time is " + self.current_time

        else:
            self.output = "No such command - Type 'help' for a list of commands."

    def kill(self, user_input):
        if "self" in user_input:
            self.output = "That doesn't seem very smart..."

        else:
            self.output = "No such thing to kill - Type 'help' for a list of commands."

    # change player name
    def change_name(self, name):
        self.player.name = name
        self.output = "You changed your name to: " + name

    # send message
    def say(self, name, message):
        makeitastring = ' '.join(map(str, message))
        self.output_to_all = name + ": " + makeitastring
        self.output = ""






