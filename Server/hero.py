

''' #==============================================================================

                                Hero Class

''' #==============================================================================

class Hero:

    def __init__(self, user, dungeon):

        # Player game vars
        self.user = user

        self.hero_name = "Taako"

        self.current_dungeon = dungeon

        # Starting room
        self.current_room = self.current_dungeon.rooms_dict["Entry Gate"]


    ''' #==============================================================================
    
                                    Player Movement
    
    ''' #==============================================================================

    # Moves the player to a new room
    def change_room(self, new_room):

        self.current_room = new_room