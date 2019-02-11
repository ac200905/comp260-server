from Scripts import game



def main():

    new_game = game.Game()
    new_game.setup("My Dungeon")
    new_game.loop()


if __name__ == "__main__":

    main()

