import player
import dungeon

from client_info import ClientInfo


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


        self.current_time = 0

        self.connected = ''

        self.clients = {}

        self.players_on_server = []

        self.clients_lock = threading.Lock()

        #self.lost_clients = []

        #self.my_thread = ''

        #self.new_client = ''

        self.message_queue = Queue()

        self.client_dict = {}

    def setup(self, dungeon_name):
        self.running = True
        self.connected = True

        self.player = player.Player("Player Name")
        self.dungeon = dungeon.Dungeon(dungeon_name, self.player)

        self.dungeon.setup_dungeon()

        self.player.setup(self.dungeon)



    def accept_thread(self, server_socket):

        while self.running:
            new_socket = server_socket.accept() [0]
            print("Added client. Socket info: " + str(new_socket))
            new_client = ClientInfo(new_socket)

            self.clients_lock.acquire()

            # add client to the list of players
            self.players_on_server.append(new_client)

            # client dictionary not currently working as intended
            self.client_dict[new_socket] = new_client
            self.clients[new_client.client_socket] = 0

            self.clients_lock.release()
            print("Added client.")


    # send message to all players on the server
    def send_to_all(self, message):

        for player in self.players_on_server:
            print("sending to clients")
            player.output_queue.put(message)


    def check_room_for_players(self, this_player):
        players_in_room = []
        for other_client in self.client_dict:
            other_player = self.client_dict.get(other_client)
            if this_player.current_room == other_player.current_room:
                if other_client != this_player:
                    players_in_room[other_client] = 0
        print(players_in_room)
        return players_in_room

    # main loop
    def loop(self):

        # remove player from player list if connection is lost
        for player_in_game in self.players_on_server:
            if player_in_game.client_lost:
                self.players_on_server.remove(player_in_game)

        # loop through players in the list
        for player_in_game in self.players_on_server:
            if player_in_game.input_queue.qsize() > 0:
                print("inq b4get" + str(player_in_game.input_queue.qsize()))
                player_in_game.input_queue.get()
                print("inq aftget" + str(player_in_game.input_queue.qsize()))
                player_in_game.add_to_out_queue(player_in_game.next_output)
                print("outq after add in loop: " +str(player_in_game.output_queue.qsize()))
                print("output: " + player_in_game.next_output + "end")

                # check if the player is chatting
                if player_in_game.client_command == "say":

                    #output chat to other players only if they are in the same room
                    for others in self.players_on_server:

                        if others != player_in_game and others.player.current_room == player_in_game.player.current_room:

                            others.output_queue.put(player_in_game.player.name + " said: " + player_in_game.client_speech)
                        if others == player_in_game:

                            player_in_game.output_queue.put("You said: " + player_in_game.client_speech)

                # check to see if a player has left or entered the room
                if player_in_game.client_command == "go":
                    old_room = player_in_game.player.input.last_room
                    new_room = player_in_game.player.current_room
                    print("old room:" + old_room)
                    print("new room:" + new_room)
                    for others in self.players_on_server:
                        if others != player_in_game and others.player.current_room == player_in_game.player.input.last_room:

                            others.output_queue.put(player_in_game.player.name + " left the room")
                        if others != player_in_game and others.player.current_room == player_in_game.player.current_room:

                            others.output_queue.put(player_in_game.player.name + " has entered the room")

                        if others == player_in_game:
                            player_in_game.output_queue.put("")






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










