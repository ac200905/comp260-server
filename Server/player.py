

''' #==============================================================================

                                Player Class

''' #==============================================================================

class player:

    def __init__(self, user, dungeon):

        # Player game vars
        self.user = user
        self.player_name = "Taako"
        self.current_dungeon = dungeon
        self.current_room = self.current_dungeon.rooms["Entry Gate"]
        self.health = 100
        self.inventory = {}

    ''' #==============================================================================
    
                                    Player Movement
    
    ''' #==============================================================================

    # Moves the player to a new room
    def change_room(self, new_room):
        self.current_room = new_room