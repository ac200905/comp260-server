from DatabaseInfo import DatabaseInfo


''' #==============================================================================

                                Input Commands

''' #==============================================================================

class Input:

    def __init__(self, users, dungeon):

        self.users = users
        self.current_user = None
        self.current_player = None
        self.input = None
        self.databaseInfo = DatabaseInfo()

        self.dungeon = dungeon

        self.login = {"--!SaltCheck": lambda: self.verify_salt(self.current_user, self.input),
                      "--!Login": lambda: self.login_method(self.current_user, self.input),
                      "--!NewAccount": lambda: self.new_account(self.current_user, self.input)}

        self.player_selection = {"name": lambda: self.new_hero(self.current_user, self.input),
                                 "select": lambda: self.choose_hero(self.current_user, self.input),
                                 "pick": lambda: self.choose_hero(self.current_user, self.input),
                                 "choose": lambda: self.choose_hero(self.current_user, self.input)}

        self.instructions = {"go": lambda: self.move_player(self.current_user, self.input),
                             "move": lambda: self.move_player(self.current_user, self.input),
                             "help": lambda: self.help_instruction(self.current_user),
                             "look": lambda: self.look_at(self.current_user),
                             "survey": lambda: self.look_at(self.current_user),
                             "say": lambda: self.room_speech(self.input),
                             "/s": lambda: self.room_speech(self.input),
                             "stone": lambda: self.use_stone(self.input),
                             "/y": lambda: self.use_stone(self.input)}
                             #"map": lambda: self.use_map(self.current_user)}


    ''' #==============================================================================
    
                                    Main Input Loop
    
    ''' #==============================================================================

    # Check all the Inputs coming in of each player to activate commands accordingly
    def handle_input(self):

        for user in self.users:

            if user.connected:

                self.current_user = user
                self.current_player = user.current_player

                # Check to see if an input has actually been sent
                if user.input_queue.qsize() > 0:

                    # Login State
                    if user.state == user.LoginPanel:

                        # Splits up the delimited input
                        self.input = user.input_queue.get().split("#")

                        # Limits it to the functions in self.login dict
                        if self.input[0] in self.login:
                            self.login[self.input[0]]()

                        else:
                            user.add_to_output_queue("ERROR --INVALID COMMAND--")

                    # Player selection game state
                    elif user.state == user.HeroSelectScreen:

                        # splits up the input and makes it all lower case
                        self.input = user.input_queue.get().lower().split(" ", 1)

                        if self.input[0] in self.player_selection:
                            self.player_selection[self.input[0]]()

                        else:
                            user.add_to_output_queue("ERROR --INVALID COMMAND--")

                    # Actual game state
                    elif user.state == user.InGame:
                            # Splits up the input and makes it all lower case
                            self.input = user.input_queue.get().lower().split(" ", 1)

                            if self.input[0] in self.instructions:
                                try:
                                    self.instructions[self.input[0]]()
                                except Exception as err:
                                    user.add_to_output_queue("ERROR --MISSING AN EXTRA INPUT--")

                            else:
                                user.add_to_output_queue("ERROR --INVALID COMMAND--")

            else:
                self.users.remove(user)
                self.output_to_all(user.username + " has left the game.")
                print(user.username + " has disconnected.")


    ''' #==============================================================================
    
                                    Functions for messaging multiple clients 
    
    ''' #==============================================================================

    # Send a message to every player in the dungeon
    def output_to_all(self, message):
        for user in self.users:
            if user.state == user.InGame:
                user.add_to_output_queue(message)


    # Send a message to every player in the same room
    def output_to_room(self, message, players_in_room):
        for player in players_in_room:
            player.user.add_to_output_queue(message)


    ''' #==============================================================================
    
                                    Login functions
    
    ''' #==============================================================================

    def verify_salt(self, user, input):
        if self.databaseInfo.check_account(input[1]): # Check if username is in database
            # Send the salt back to client is username exists
            user.add_to_output_queue("SALT#" + self.databaseInfo.fetch_salt_in_database(input[1]), True)
        else:
            user.add_to_output_queue("Failed to login!\n"
                               "User Account: " + input[1] + " does not exist.")

    def login_method(self, user, input):
        logged_in = False

        for u in self.users:
            if u.username == input[1]:
                logged_in = True

        # Check username and password
        if self.databaseInfo.check_login_details(input[1], input[2]):
            if not logged_in:

                user.add_to_output_queue("Login successful.")
                user.add_to_output_queue("LOGIN_SUCCESS", True)
                user.username = input[1]

                # This changes the user state to player selection
                self.start_hero_selection(user)

            else:
                user.add_to_output_queue("Failed to login!\n"
                                   "There is already a user logged in with this account.")
        else:
            user.add_to_output_queue("Failed to login!\n"
                               "Incorrect username or password.")

    def new_account(self, player, input):
        player.add_to_output_queue("Creating account...")

        # Create an account using the username, password, and salt
        if self.databaseInfo.create_account(input[1], input[2], input[3]):
            player.add_to_output_queue("Account created.")

        else:
            player.add_to_output_queue("Failed to create an account.\n"
                                 "This user account may already exist.")

    ''' #==============================================================================
    
                                    Hero selection functions
     
    ''' #==============================================================================

    def start_hero_selection(self, user):
        # Sets the user state to player select
        user.state = user.HeroSelectScreen
        user.add_to_output_queue("\nTo create a new hero: name <HeroName>\n"
                           "To choose an existing hero: select <HeroName>\n")

        self.show_heroes(user)

    def show_heroes(self, user):
        user.add_to_output_queue("Current heroes:")
        playerList = self.databaseInfo.list_of_heroes(user.username)

        if len(playerList) < 1:
            user.add_to_output_queue(
                               "\nCreate a new hero with: name <HeroName>")
        else:
            for player in playerList:
                user.add_to_output_queue("- " + str(player[3]) + " in " + str(player[2]))


    def choose_hero(self, user, input):

        player = user.current_player

        chosen_hero = self.databaseInfo.choose_hero(user.username, input[1])

        if chosen_hero:
            user.add_to_output_queue(str(chosen_hero[3]) + " is selected\n")
            player.player_name = str(chosen_hero[3])

            # Adds the hero name to the window UI
            user.add_to_output_queue("UPDATE_HERO_NAME#" + user.current_player.player_name, True)

            user.add_to_output_queue("\nJoining game...")
            user.state = user.InGame
            current_room_in_database = self.databaseInfo.get_current_room(user.current_player.player_name)

            # add user to the dungeon
            user.current_player.current_room = user.current_player.current_dungeon.rooms[current_room_in_database]
            user.current_player.current_room.players.append(user.current_player)
            user.add_to_output_queue("UPDATE_ROOM#" + user.current_player.current_room.name, True)

            # notifies everyone in game that a new player has joined
            self.output_to_all(user.current_player.player_name + " has joined the game!")

        elif chosen_hero is None:
            user.add_to_output_queue("This hero doesn't exist")
        else:
            user.add_to_output_queue("!-ERROR-!")


    def new_hero(self, user, input):

        user.add_to_output_queue("\nCreating new hero...")

        if self.databaseInfo.create_hero(user.username, input[1], "Entry Gate"):
            user.add_to_output_queue("New hero " + input[1] + " has been created!\n"
                                    "To choose an existing hero: select <HeroName>")

        else:
            user.add_to_output_queue("A hero with that name already exists!")

        self.show_heroes(user)


    ''' #==============================================================================
    
                                    General game functions
    
    ''' #==============================================================================

    # Help command displays all the commands the player can write
    def help_instruction(self, player):
        player.add_to_output_queue(
            "\n"
            "----------------------------------------------------\n" 
            "List Of Commands: \n" 
            "Go <direction> : Can move north, south, east or west\n" 
            "Look           : Survey area\n" 
            "Say <speech>   : Speak to other players in the room\n"
            "Stone <speech> : Use the stone of farspeech to talk to everyone in the dungeon\n"
            "Map            : Display map \n" 
            "----------------------------------------------------\n"
        )
    '''
    def use_map(self, player):
        player.add_to_output_queue(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" 
            "	Stonefruit Farm                                                        \n" 
            "	        |                                                               \n" 
            "	        |                                                               \n" 
            "Cave ------------- Witch's Hut                                                         \n" 
            "  |  			                                                                       \n" 
            "  |  			                                                                       \n" 
            "Fallen Temple ------------- North Street -----------------------------------Quarry     \n" 
            "    	                 |                                                     \n" 
            "    	                 |                                                     \n" 
            "                    Bank ------ Clock Tower ------ Sherrif's Office                        \n" 
            "     	                 |                                                     \n" 
            "        	                 |                                                     \n" 
            "          Helpington's ---- South Street ------ The Davy Lamp                          \n" 
            "    	                 |                              |                                \n" 
            "    	                 |                              |                                \n" 
            "                                    Entry Gate             Large Well                           \n" 
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        )
    '''

    # Describes location
    def look_at(self, player):
        player.add_to_output_queue(self.current_player.current_room.description)

    # Send a message to every player in the same room
    def room_speech(self, input):
        for player in self.current_player.current_room.players:
            player.user.add_to_output_queue(self.current_player.player_name + " said: " + input[1])

    # Send a message to every player in the spaceship using the radio
    def use_stone(self, input):
        for player in self.users:
            player.add_to_output_queue(self.current_player.player_name + " used the stone and said: " + input[1])

    # Command that allows the player to move around the different rooms
    def move_player(self, user, input):
        if input[1] in self.current_player.current_room.connected_rooms:
            old_room = self.current_player.current_room
            new_room = self.current_player.current_room.connected_rooms[input[1]]

            # removes the player from the current room
            self.current_player.current_room.players.remove(self.current_player)

            # announce that a player has left the current room
            self.output_to_room(self.current_player.player_name + " has left the room", old_room.players)

            # Move the player to the new Room
            self.current_player.change_room(self.dungeon.rooms[new_room])
            self.databaseInfo.update_player_room(self.current_player.player_name, self.current_player.current_room.name)
            user.add_to_output_queue("You have moved to: " + self.current_player.current_room.name)

            # announce that a player has entered a new room
            self.output_to_room(self.current_player.player_name + " entered the room", self.current_player.current_room.players)

            # adds the player to the new room
            self.current_player.current_room.players.append(self.current_player)

            # update room textbox on client
            user.add_to_output_queue("UPDATE_ROOM#" + user.current_player.current_room.name, True)

        else:
            user.add_to_output_queue("Nothing lies that way...")
