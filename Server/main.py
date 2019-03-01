import game
import socket
import threading

"""=============================================================================

###############   Run game.py to initialize Server.   ##################

running = True
setup_dungeon = True

def main():

    new_game = game.Game()


    new_game.setup("My Dungeon")

    while running:

        new_game.loop()




if __name__ == "__main__":

    new_game2 = game.Game()
    new_game2.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    new_game2.my_socket.bind(("127.0.0.1", 8222))
    new_game2.my_socket.listen(5)

    new_game2.accept_thread = threading.Thread(target=new_game2.accept_thread, args=(new_game2.my_socket,))
    new_game2.accept_thread.start()
    print("doing it!!!!!!!!!!!!!")

    main()           """

