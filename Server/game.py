import socket
import threading
import dungeon
from DatabaseInfo import DatabaseInfo
from clientInfo import ClientInfo
from input import Input


running = True

testing_server = True # Change when setting up server online

heroes = []
clients = []
clients_lock = threading.Lock()

# SQL database
database_information = DatabaseInfo()

# Current dungeon
my_dungeon = dungeon.DungeonRooms
my_dungeon.setup_dungeon(dungeon.DungeonRooms, "Refuge")

# Main input
input = Input(clients, my_dungeon)



''' #==============================================================================

                                Socket Accept Thread

''' #==============================================================================

def accept_thread(server_socket):

    print("accept_thread running")

    while running:

        new_socket = server_socket.accept()[0]

        new_client = ClientInfo(new_socket, my_dungeon)

        clients_lock.acquire()

        clients.append(new_client)

        heroes.append(new_client.current_hero)

        new_client.add_to_output_queue("You are connected to the server!\n"
                              "Please use the Login Panel to either login or create a new account.")

        clients_lock.release()

        print("Added new client!")


''' #==============================================================================

                                     Main

''' #==============================================================================

if __name__ == '__main__':

    database_information.setup_database()

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if testing_server:

        my_socket.bind(("127.0.0.1", 8222))

    else:

        my_socket.bind(("46.101.56.200", 9234))

    my_socket.listen(5)

    acceptThread = threading.Thread(target=accept_thread, args=(my_socket,))
    acceptThread.start()

    # Main Loop
    while running:

        input.handle_input()
