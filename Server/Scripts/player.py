from Scripts import input


class Player:

    def __init__(self, name):

        self.name = 'Player'
        self.dungeon = ''
        self.current_room = ''
        self.input = ''

    def setup(self, current_dungeon):
        self.dungeon = current_dungeon
        self.current_room = self.dungeon.starting_room
        self.input = input.Input(self, self.dungeon)




