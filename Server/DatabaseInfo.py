import sqlite3


''' #==============================================================================

                                Database Interactions

''' #==============================================================================

class DatabaseInfo:

    def __init__(self):

        self.database = sqlite3.connect('ServerDatabase.sql')
        self.cursor = self.database.cursor()

    ''' #==============================================================================
                                Login and Account functions
    ''' #==============================================================================

    def create_account(self, username, password, salt):

        try:
            self.cursor.execute("select * from  Users where username == '" + username + "'")
            rows = self.cursor.fetchall()


            if len(rows) == 0:

                self.cursor.execute('insert into Users(username, password, salt) VALUES(?,?,?)', (username, password, salt))

                # Add to SQL database
                self.database.commit()

                return True
            else:
                return False
        except:
            print('Failed to add to DB')
            return False

    # Checks if the account is in the database already
    def check_account(self, username_login):

        try:
            self.cursor.execute("SELECT username FROM users WHERE username == '" + username_login + "'")
            username_in_database = self.cursor.fetchone()[0]

            if username_login == username_in_database:
                return True

            else:
                return False

        except:
            print('--!LOGIN ERROR!--')
            return False

    def fetch_salt_in_database(self, username_login):

        try:
            self.cursor.execute("SELECT salt FROM users WHERE username == '" + username_login + "'")
            salt_in_database = self.cursor.fetchone()[0]
            return salt_in_database

        except:
            print('--!LOGIN ERROR!--')
            return False

    def check_login_details(self, username_login, password_login):

        try:
            self.cursor.execute("SELECT password FROM users WHERE username == '" + username_login + "'")
            password_in_database = self.cursor.fetchone()[0]

            if password_login == password_in_database:
                return True

            else:
                return False

        except:
            print('--!LOGIN ERROR!--')
            return False


    ''' #==============================================================================
    
                                    Player Information 
    
    ''' #==============================================================================

    def list_of_heroes(self, username):

        try:
            self.cursor.execute("SELECT * FROM players WHERE owner == '" + username + "'")
            players_owned = self.cursor.fetchall()
            return players_owned


        except:
            print('--!HERO FETCH ERROR!--')
            return False


    def create_hero(self, username, player_name, starting_room):

        try:
            self.cursor.execute("SELECT * FROM players WHERE player_name == '" + player_name + "'")
            rows = self.cursor.fetchall()

            if len(rows) == 0:
                self.cursor.execute('insert into players(player_name, owner, current_room) VALUES(?,?,?)',
                                    (player_name, username, starting_room))
                self.database.commit()
                return True
            else:
                return False
        except:
            print('--!HERO CREATION ERROR!--')
            return False


    def choose_hero(self, username, player_name):

        try:
            self.cursor.execute("SELECT * FROM players WHERE player_name == '" + player_name + "'" + " AND owner == '"
                                + username + "'")
            player = self.cursor.fetchone()

            if player is not None:
                return player
            else:
                return None
        except:
            print('--!HERO CREATION ERROR!--')
            return False


    def get_current_room(self, player_name):

        try:
            self.cursor.execute("SELECT current_room FROM players WHERE player_name == '" + player_name + "'")
            player_room = self.cursor.fetchone()

            if player_room is not None:
                return player_room[0]
            else:
                return None
        except:
            print('--!HERO CREATION ERROR!--')
            return False


    def update_player_room(self, player_name, new_room):

        try:
            self.cursor.execute("SELECT * FROM players WHERE player_name == '" + player_name + "'")
            player = self.cursor.fetchone()

            if player:
                self.cursor.execute("UPDATE players SET current_room = '" + new_room + "'" + " WHERE player_name == '" + player_name + "'")
                self.database.commit()
            else:
                return None
        except:
            print('--!HERO CREATION ERROR!--')
            return False


    ''' #==============================================================================
    
                                    Database Setup
    
    ''' #==============================================================================

    def setup_database(self):

        self.setup_room_table()
        self.setup_user_table()
        self.setup_player_table()
        #self.setup_dungeon_table()

        print("Creating Database.")


    # Create table to store all rooms
    def setup_room_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS rooms(
                            room_name TEXT PRIMARY KEY,
                            room_description TEXT
                            )
                            ''')

        # Add the table
        self.database.commit()


    # Create table to store all users
    def setup_user_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users(
                        username TEXT PRIMARY KEY, 
                        password TEXT, 
                        salt TEXT)
                        ''')

        self.database.commit()


    # Create table to store all players
    def setup_player_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS players(
                        id INTEGER PRIMARY KEY, 
                        owner TEXT, 
                        current_room TEXT, 
                        player_name TEXT)
                        ''')

        self.database.commit()



