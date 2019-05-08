import sqlite3


''' #==============================================================================

                                Database Interactions

''' #==============================================================================

class DatabaseInfo:

    def __init__(self):

        self.database = sqlite3.connect('ServerDatabase.sql')
        self.cursor = self.database.cursor()

    ''' #==============================================================================

                                    Database Setup

    '''  # ==============================================================================

    # Create the tables in the database
    def setup_database(self):

        self.setup_room_table()
        self.setup_user_table()
        self.setup_hero_table()

        print("Creating Database.")

    # Create table to store all rooms
    def setup_room_table(self):

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS rooms(
                            room_name TEXT PRIMARY KEY)
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
    def setup_hero_table(self):

        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS heroes(
                        id INTEGER PRIMARY KEY, 
                        owner TEXT, 
                        hero_name TEXT,
                        current_room TEXT)
                        ''')

        self.database.commit()

    ''' #==============================================================================
                                Login and Account functions
    ''' #==============================================================================

    # Checks password is that of the user
    def check_login_details(self, username_login, password_login):

        try:

            self.cursor.execute("SELECT password FROM users WHERE username == '" + username_login + "'")
            password_in_database = self.cursor.fetchone()[0]

            if password_login == password_in_database:

                return True

            else:

                return False

        except:

            print('!LOGIN ERROR! - PASSWORD NOT IN DATABASE')
            return False

    # Adds new account details to database
    def create_account(self, username, password, salt):

        try:

            self.cursor.execute("select * from  Users where username == '" + username + "'")
            rows = self.cursor.fetchall()


            if len(rows) == 0:

                self.cursor.execute('insert into Users(username, password, salt) VALUES(?,?,?)',
                                    (username, password, salt))

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

            print('LOGIN ERROR! - USERNAME ERROR')
            return False

    # Get this users password salt to send across
    def fetch_salt_in_database(self, username_login):

        try:

            self.cursor.execute("SELECT salt FROM users WHERE username == '" + username_login + "'")
            salt_in_database = self.cursor.fetchone()[0]

            return salt_in_database

        except:

            print('LOGIN ERROR! - SALT FETCH ERROR')
            return False




    ''' #==============================================================================
    
                                    Player Information 
    
    ''' #==============================================================================

    # Adds a new hero to the database
    def create_hero(self, username, hero_name, starting_room):

        try:

            self.cursor.execute("SELECT * FROM heroes WHERE hero_name == '" + hero_name + "'")
            rows = self.cursor.fetchall()

            if len(rows) == 0:

                self.cursor.execute('insert into heroes(hero_name, owner, current_room) VALUES(?,?,?)',
                                    (hero_name, username, starting_room))
                self.database.commit()

                return True

            else:

                return False

        except:

            print('HERO CREATION ERROR!')
            return False

    # Gets a list of all the heroes that user has created
    def list_of_heroes(self, username):

        try:

            self.cursor.execute("SELECT * FROM heroes WHERE owner == '" + username + "'")
            heroes_owned = self.cursor.fetchall()
            return heroes_owned


        except:

            print('HERO FETCH ERROR!')
            return False

    # Selects a hero fromm the database
    def choose_hero(self, username, hero_name):

        try:

            self.cursor.execute("SELECT * FROM heroes WHERE hero_name == '" + hero_name + "'" + " AND owner == '"
                                + username + "'")
            hero = self.cursor.fetchone()

            if hero is not None:

                return hero

            else:

                return None
        except:

            print('HERO SELECTION ERROR!')
            return False

    # Gets the rom the hero is currently in
    def get_current_room(self, hero_name):

        try:

            self.cursor.execute("SELECT current_room FROM heroes WHERE hero_name == '" + hero_name + "'")
            hero_room = self.cursor.fetchone()

            if hero_room is not None:

                return hero_room[0]

            else:

                return None

        except:

            print('ROOM GET ERROR!')
            return False

    # Change the heroes current room in the database
    def update_hero_room(self, hero_name, new_room):

        try:

            self.cursor.execute("SELECT * FROM heroes WHERE hero_name == '" + hero_name + "'")
            hero = self.cursor.fetchone()

            if hero:

                self.cursor.execute("UPDATE heroes SET current_room = '" + new_room + "'" + " WHERE hero_name == '" + hero_name + "'")
                self.database.commit()

            else:

                return None

        except:

            print('ROOM UPDATE ERROR!')
            return False






