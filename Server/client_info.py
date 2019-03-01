from queue import *
import player
import dungeon

import threading
import socket

class ClientInfo:
    # Init function
    def __init__(self, client_socket):
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.client_socket = client_socket
        self.player = ''
        self.player = player.Player("Player Name")
        self.clientID = ""
        self.player_name = self.player.name
        self.player_position = self.player.current_room
        self.current_room = self.player.current_room
        #self.player_position = "banana"
        self.dungeon = dungeon.Dungeon("My dungeon", self.player)

        self.dungeon.setup_dungeon()

        self.player.setup(self.dungeon)

        self.client_lost = False

        self.client_command = ""
        self.client_input = ""
        self.client_speech = ""
        self.next_output = ""

        client_receive_thread = threading.Thread(target=ClientInfo.receive_thread, args=(self,))
        client_receive_thread.start()

        client_send_thread = threading.Thread(target=ClientInfo.send_thread, args=(self,))
        client_send_thread.start()

        self.last_room = ""



    def receive_thread(self):
        print("client receive_thread running")
        can_receive = True
        while can_receive:
            try:
                data = self.client_socket.recv(4096)
                text = data.decode("utf-8")
                self.client_input = text
                self.client_input = self.client_input.lower()
                self.client_input = self.client_input.split(" ", 1)
                self.client_command = self.client_input[0]
                if len(self.client_input) > 1:
                    self.client_speech = self.client_input[1]
                print("Input qsize b4: " + str(self.input_queue.qsize()) + "\n")
                self.input_queue.put(text)
                print("Input qsize after: " + str(self.input_queue.qsize()) + "\n")
                print(text)



                self.player.input.handle_input(user_input=text)
                self.next_output = self.player.input.output

                #self.output_queue.put(self.player.input.output)
                print(self.player_name + " at " + self.player.current_room)

                #print(self.player.input.output)


                #print(self.input_queue.get())

            except socket.error:
                self.client_lost = True
                can_receive = False
                print("receive_thread: ERROR - Lost client")

    def send_thread(self):
        print("send_thread running")
        can_send = True
        while can_send:
            try:
                if self.output_queue.qsize() > 0:
                    # Get the output message to be sent
                    print("Output qsize b4: " + str(self.output_queue.qsize()) + "\n")
                    output_string = self.output_queue.get()
                    print("Output qsize after: " + str(self.output_queue.qsize()) + "\n")

                    print(self.player.name + " is sending :" + output_string + "sent \n")


                    #output_string = self.player.input.output
                    #self.output_queue.put(output_string)

                    # Send message to the player
                    self.client_socket.send(output_string.encode("utf-8"))

                    #print(self.playerName + " is Sending: " + outputMessage)

            except socket.error:
                self.client_lost = True
                can_send = False
                print("sending_thread: ERROR - Lost client")



    def add_to_out_queue(self, message):
        self.output_queue.put(message)