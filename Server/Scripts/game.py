from Scripts import player
from Scripts import dungeon

from Scripts import client_info
import socket
from time import sleep
import threading
from queue import *



class Game:

    def __init__(self):
        self.running = ''

        self.player = ''

        self.dungeon = ''

        self.exit_text = "Farewell Traveller..."

        self.my_socket = ''

        self.data = []

        self.seqID = 0

        self.current_time = 0

        self.connected = ''

        self.clients = {}

        self.players = []

        self.clients_lock = threading.Lock()

        #self.lost_clients = []

        #self.my_thread = ''

        #self.new_client = ''

        self.message_queue = Queue()

    def setup(self, dungeon_name):
        self.running = True
        self.connected = True

        self.player = player.Player("Player Name")
        self.dungeon = dungeon.Dungeon(dungeon_name, self.player)

        self.dungeon.setup_dungeon()

        self.player.setup(self.dungeon)



    def accept_thread(self, server_socket):

        while self.running:
            new_socket = server_socket.accept()[0]
            print("Added client. Socket info: " + str(new_socket))
            new_client = client_info.ClientInfo(new_socket)


            self.clients_lock.acquire()
            #self.clients[new_client[0]] = 0
            self.players.append(new_client)
            print(self.players)
            self.clients[new_client.client_socket] = 0
            #my_receive_thread = threading.Thread(target=Game.receive_thread, args=(self, new_client[0],))
            #my_receive_thread.start()
            self.clients_lock.release()
            print("Added client.")

            # Send a message to every player

    def send_to_all(self, message):

        for new_player in self.players:
            print("sending to clients")
            new_player.output_queue.put(message)
            new_player.output_queue.pop()

    def loop(self):

        for new_player in self.players:


            if new_player.input_queue.qsize() > 0:
                #print("getting input")

                input = new_player.input_queue.get()
                split_input = input.split(' ')
                # Get the first word the user inputs, this is the action the user is taking
                instruction = split_input[0]
                if instruction == "say":
                    #message_to_all = self.player.input.output_to_all
                    message_to_all = "sending to all"
                    self.send_to_all(message_to_all)
                    #for new_player in self.players:
                        #new_player.output_queue.put(message_to_all)





running = True

if __name__ == '__main__':
    game = Game()


    print("Server Running.")


    game.setup("My dungeon")
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    mySocket.bind(("127.0.0.1", 8222))
    mySocket.listen(5)

    accept_thread = threading.Thread(target=game.accept_thread, args=(mySocket,))
    accept_thread.start()
    #game.accept_thread(mySocket)

    # Main Loop
    while running:

        #game.accept_thread(mySocket)

        game.loop()

"""
    def loop(self):
        #self.running = True
        #self.connected = False

        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        my_socket.bind(("127.0.0.1", 8222))
        my_socket.listen(5)

        my_accept_thread = threading.Thread(target=Game.accept_thread, args=(self, my_socket,))
        my_accept_thread.start()

        while self.running:
            lost_clients = []
            client_and_message = ''
            self.clients_lock.acquire()

            # Update time on clock
            #self.player.input.current_time = str(
                #"{0:0=2d}".format(int(60 / self.dungeon.moves_available * self.dungeon.moves_taken)))
            #if self.dungeon.moves_taken == -1:
                #self.player.input.current_time = "00"

            while self.message_queue.qsize() > 0:
                try:
                    client_and_message = self.message_queue.get()
                    print("Input from client " + str(client_and_message[0]) + ": \n" + client_and_message[1])
                    self.player.input.handle_input(user_input=client_and_message[1])
                    output_string = self.player.input.output
                    client_and_message[0].send(output_string.encode())

                except socket.error:
                    lost_clients.append(client_and_message[0])
                    print("Client Lost")

            for client in lost_clients:
                self.clients.pop(client)

            self.clients_lock.release()
            sleep(0.5)

"""










