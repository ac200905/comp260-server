from DatabaseInfo import DatabaseInfo


''' #==============================================================================

                                Input Commands

''' #==============================================================================

class Input:

    def __init__(self, users, dungeon):

        self.users = users
        self.current_user = None
        self.current_hero = None
        self.input = None
        self.databaseInfo = DatabaseInfo()

        self.dungeon = dungeon

        self.login_command = None
        self.hero_select_command = None
        self.instruction = None
        self.direction = None



    ''' #==============================================================================
    
                                    Main Input Loop
    
    ''' #==============================================================================

    # Handle all the Inputs from each player
    def handle_input(self):

        for user in self.users:

            if user.connected:

                self.current_user = user
                self.current_hero = user.current_hero

                # Check to see if an input has actually been sent
                if user.input_queue.qsize() > 0:

                    # Login State instructions
                    if user.state == user.LoginPanel:

                        # Splits up the delimited input
                        self.input = user.input_queue.get()
                        self.input = self.input.split('#')
                        self.login_command = self.input[0]
                        print(self.login_command)

                        if self.login_command == "VerifySalt":
                            self.verify_salt(self.current_user, self.input)
                        elif self.login_command == "CheckLogin":
                            self.login_method(self.current_user, self.input)
                        elif self.login_command == "CreateAccount":
                            self.new_account(self.current_user, self.input)

                        else:
                            user.add_to_output_queue("ERROR - login error")

                    # Player selection game state instructions
                    elif user.state == user.HeroSelectScreen:
                        # splits up the input and makes it all lower case
                        self.input = user.input_queue.get()
                        self.input = self.input.lower()
                        self.input = self.input.split(" ", 1)
                        self.hero_select_command = self.input[0]


                        if self.hero_select_command == "name":

                            self.new_hero(self.current_user, self.input)

                        elif self.hero_select_command == "pick" or \
                            self.hero_select_command == "select" or \
                            self.hero_select_command == "choose" :

                            self.choose_hero(self.current_user, self.input)

                        else:
                            user.add_to_output_queue("ERROR - hero select error")

                    # Actual game state
                    elif user.state == user.InGame:
                            # Splits up the input and makes it all lower case
                            self.input = user.input_queue.get()
                            self.input = self.input.lower()
                            self.input = self.input.split(" ", 1)
                            self.instruction = self.input[0]

                            if self.instruction == "move" or self.instruction == "go":

                                self.move_hero(self.current_user, self.input)

                            elif self.instruction == "look" or self.instruction == "survey":

                                self.look_at(self.current_user)

                            elif self.instruction == "map":

                                self.use_map(self.current_user)

                            elif self.instruction == "help":

                                self.help_instruction(self.current_user)

                            elif self.instruction == "say" or self.instruction == "/s":

                                self.room_speech(self.input)

                            elif self.instruction == "stone" or self.instruction == "/y":

                                self.use_stone(self.input)

                            else:

                                user.add_to_output_queue("ERROR - instruction error")


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
    def output_to_room(self, message, heroes_in_room):

        for hero in heroes_in_room:

            hero.user.add_to_output_queue(message)


    ''' #==============================================================================
    
                                    Login functions
    
    ''' #==============================================================================

    # Verify the users salt
    def verify_salt(self, user, input):

        if self.databaseInfo.check_account(input[1]): # Check if username is in database
            # Send the salt back to client is username exists
            user.add_to_output_queue("SALT#" + self.databaseInfo.fetch_salt_in_database(input[1]), True)

        else:

            user.add_to_output_queue("Failed to login!\n"
                               "User Account: " + input[1] + " does not exist.")

    # Login user
    def login_method(self, user, input):

        logged_in = False

        for u in self.users:

            if u.username == input[1]:

                logged_in = True

        # Check username and password
        if self.databaseInfo.check_login_details(input[1], input[2]):

            if not logged_in:

                user.add_to_output_queue("Login successful.")

                # Send command to hide the login panel
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

    # Create a new account
    def new_account(self, hero, input):

        hero.add_to_output_queue("Creating account...")

        # Create an account using the username, password, and salt
        if self.databaseInfo.create_account(input[1], input[2], input[3]):

            hero.add_to_output_queue("Account created.")

        else:

            hero.add_to_output_queue("Failed to create an account.\n"
                                 "This user account may already exist.")

    ''' #==============================================================================
    
                                    Hero selection functions
     
    ''' #==============================================================================

    # Start hero selection
    def start_hero_selection(self, user):
        # Sets the user state to player select
        user.state = user.HeroSelectScreen
        user.add_to_output_queue("\nTo create a new hero: name <HeroName>\n"
                           "To choose an existing hero: select <HeroName>\n")

        self.show_heroes(user)

    # Get the heroes the user currently has in the database
    def show_heroes(self, user):

        user.add_to_output_queue("Current heroes:")
        hero_list = self.databaseInfo.list_of_heroes(user.username)

        if len(hero_list) < 1:

            user.add_to_output_queue("\nCreate a new hero with: name <HeroName>")

        else:

            for hero in hero_list:
                # get the hero name and hero location
                user.add_to_output_queue("- " + str(hero[2]) + " in " + str(hero[3]))


    def choose_hero(self, user, input):

        hero = user.current_hero

        chosen_hero = self.databaseInfo.choose_hero(user.username, input[1])

        if chosen_hero:

            user.add_to_output_queue(str(chosen_hero[2]) + " is selected\n")

            hero.hero_name = str(chosen_hero[2])

            # Adds the hero name to the window UI
            user.add_to_output_queue("UPDATE_HERO_NAME#" + user.current_hero.hero_name, True)

            user.add_to_output_queue("\nJoining game...")

            current_room_in_database = self.databaseInfo.get_current_room(user.current_hero.hero_name)

            # add user to the dungeon
            user.current_hero.current_room = user.current_hero.current_dungeon.rooms_dict[current_room_in_database]
            user.current_hero.current_room.heroes.append(user.current_hero)

            # Updates current room name in the QT window
            user.add_to_output_queue("UPDATE_ROOM#" + user.current_hero.current_room.name, True)

            # notifies everyone in game that a new player has joined
            self.output_to_all(user.current_hero.hero_name + " has joined the game!")

            # Go to next input state
            user.state = user.InGame

        elif chosen_hero is None:

            user.add_to_output_queue("This hero doesn't exist")

        else:

            user.add_to_output_queue("ERROR! - Hero selection error")


    def new_hero(self, user, input):

        user.add_to_output_queue("\nCreating new hero...")

        hero_name = input[1]

        if self.databaseInfo.create_hero(user.username, hero_name, "Entry Gate"):

            user.add_to_output_queue("New hero " + hero_name + " has been created!\n"
                                    "To choose an existing hero: select <HeroName>")

        else:

            user.add_to_output_queue("A hero with that name already exists!")

        self.show_heroes(user)


    ''' #==============================================================================
    
                                    General game functions
    
    ''' #==============================================================================

    # Help command displays all the commands the player can write
    def help_instruction(self, hero):

        hero.add_to_output_queue(
            "\n"
            "------------------------------------------\n" 
            "List Of Commands: \n" 
            "Go <direction> : Can move north, south, east or west\n" 
            "Look           : Survey area\n" 
            "Say <speech>   : Speak to other heroes in the room\n"
            "Stone <speech> : Use the stone of farspeech to talk to everyone in the dungeon\n"
            "Map            : Display map \n" 
            "------------------------------------------\n"
        )

    # Open/Close the map
    def use_map(self, hero):

        hero.add_to_output_queue("OPEN_MAP", True)


    # Describes location
    def look_at(self, hero):

        hero.add_to_output_queue(self.current_hero.current_room.description)

    # Send a message to every player in the same room
    def room_speech(self, input):

        for hero in self.current_hero.current_room.heroes:

            hero.user.add_to_output_queue(self.current_hero.hero_name + " said: " + input[1])

    # Send a message to every player in dungeon
    def use_stone(self, input):

        for hero in self.users:

            hero.add_to_output_queue(self.current_hero.hero_name + " used the stone and said: " + input[1])

    # Command that allows the player to move around the different rooms
    def move_hero(self, user, input):

        self.direction = input[1]

        if self.direction in self.current_hero.current_room.connected_rooms:

            old_room = self.current_hero.current_room
            new_room = self.current_hero.current_room.connected_rooms[self.direction]

            # removes the player from the current room
            self.current_hero.current_room.heroes.remove(self.current_hero)

            # announce that a player has left the current room
            self.output_to_room(self.current_hero.hero_name + " has left the room", old_room.heroes)

            # Move the player to the new Room
            self.current_hero.change_room(self.dungeon.rooms_dict[new_room])
            self.databaseInfo.update_hero_room(self.current_hero.hero_name, self.current_hero.current_room.name)
            user.add_to_output_queue("You have moved to: " + self.current_hero.current_room.name)

            # announce that a player has entered a new room
            self.output_to_room(self.current_hero.hero_name + " entered the room", self.current_hero.current_room.heroes)

            # adds the player to the new room
            self.current_hero.current_room.heroes.append(self.current_hero)

            # update room textbox on client
            user.add_to_output_queue("UPDATE_ROOM#" + user.current_hero.current_room.name, True)

        else:

            user.add_to_output_queue("Nothing lies that way...")
