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
                        "Quit           : Quit game \n" \
                        "----------------------------------------------------"

        self.user_input = ''
        self.split_input = ''
        self.instruction = ''
        self.next_option_1 = "What shall you do now? : "
        self.next_option_2 = "What will you do next? : "
        self.next_option_3 = "What action do you take next? : "
        self.list_next_option = [self.next_option_1, self.next_option_2, self.next_option_3]

        # A very basic layout of the dungeon
        self.map = "                         Temple                        \n\n\n" \
                   "\n  Tavern              North Street              Bank\n\n\n" \
                   "\nClock Tower           South Street            Large Well\n\n\n" \
                   "\n                       Entry Gate                    \n"


    def handle_input(self):
        user_input = input(random.choice(self.list_next_option))
        # Convert user input to lower case
        user_input = user_input.lower()
        # Split user input into separate strings for each word
        split_input = user_input.split(' ')
        # Get the first word the user inputs, this is the action the user is taking
        instruction = split_input[0]

        if instruction == "quit" or instruction == "q" or instruction == "exit":
            return "quit_game"

        elif instruction == "help":
            print(self.help_text)

        elif instruction == "go" or instruction == "move":
            self.move_player(user_input)

        elif instruction == "look" or instruction == "look at" or instruction == "survey":
            self.look_at()

        elif instruction == "map":
            print(self.map)

        # If the user input isn't recognisable
        else:
            print("No such command - Type 'help' for a list of commands.")

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
            print("No such command - Type 'help' for a list of commands.")

    def look_at(self):
        # Print the description of room connections
        print(self.dungeon.rooms_dict[self.player.current_room].look_description)

    def map(self):
        print(self.map)



