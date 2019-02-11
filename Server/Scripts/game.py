from Scripts import player
from Scripts import dungeon
import socket
import time


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

    def setup(self, dungeon_name):
        self.running = True
        self.connected = False

        self.player = player.Player("Player Name")
        self.dungeon = dungeon.Dungeon(dungeon_name, self.player)

        self.dungeon.setup_dungeon()

        self.player.setup(self.dungeon)

    def loop(self):
        #self.running = True
        #self.connected = False

        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.my_socket.bind(("127.0.0.1", 8222))
        self.my_socket.listen(5)

        while self.running:

            # Update time on clock
            self.player.input.current_time = str(
                "{0:0=2d}".format(int(60 / self.dungeon.moves_available * self.dungeon.moves_taken)))
            if self.dungeon.moves_taken == -1:
                self.player.input.current_time = "00"

            if not self.connected:
                print("Waiting for client...")
                self.client = self.my_socket.accept()

            try:
                self.data = self.client[0].recv(4096)
                self.connected = True
                print("Connection to Client established.\n")

                self.player.input.handle_input(user_input=self.data.decode("utf-8"))

                output_string = self.player.input.output

                self.client[0].send(output_string.encode())

            except socket.error:
                self.connected = False

            while self.connected:

                try:
                    self.data = self.client[0].recv(4096)

                    self.player.input.handle_input(user_input=self.data.decode("utf-8"))

                    output_string = self.player.input.output

                    self.client[0].send(output_string.encode())

                    #time.sleep(0.5)

                except socket.error:
                    self.connected = False
                    self.client = None
                    print("Client connection lost.")












