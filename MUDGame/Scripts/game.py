from Scripts import player
from Scripts import dungeon


class Game:

    def __init__(self):
        self.running = ''
        self.player = ''

        self.dungeon = ''

        self.exit_text = "Farewell Traveller..."

    def setup(self, dungeon_name):
        self.running = True

        self.player = player.Player("Player Name")
        self.dungeon = dungeon.Dungeon(dungeon_name, self.player)

        self.dungeon.setup_dungeon()

        self.player.setup(self.dungeon)

    def loop(self):
        # Print the dungeon description at beginning of game
        print(self.dungeon.dungeon_description)

        while self.running:
            # If "quit_game" returned then close application
            if self.player.input.handle_input() == "quit_game":
                print(self.exit_text)
                self.running = False





