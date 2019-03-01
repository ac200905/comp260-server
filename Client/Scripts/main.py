import sys
import socket
import random
from time import sleep
from queue import *
import threading

from PyQt5 import QtCore, QtGui, uic, QtWidgets


message_queue = Queue()
connected = False
my_socket = None
running = True

client_running: bool = True


class ClientInfo:
    def __init__(self):
        self.server_socket = None
        self.server_connected = False
        self.running = True
        self.receive_message = ""




client_info = ClientInfo()
client_info_lock = threading.Lock()

"""-----------------
Threading 
-----------------"""

def send_thread(client_info, MyGUI):
    print("Send Thread running")
    MyGUI.enter_command()
    new_input = ""
    client_info.server_socket.send(new_input.encode())
    print("Sent: " + new_input + " to server")





def receive_thread(client_info, MyGUI):


    print("receive_thread running")

    while client_info.running:
        while client_info.server_connected:
            try:
                #message_queue.put(server_socket.recv(4096).decode("utf-8"))
                data = client_info.server_socket.recv(4096)
                text = ""
                text += data.decode("utf-8")
                client_info_lock.acquire()
                client_info.receive_message += text
                client_info_lock.release()
                print("Text Received: " + text)


                # Display text received to the UI text box
                MyGUI.DisplayText(text)


            except socket.error:

                print("Lost server")

                MyGUI.DisplayText("Lost Server")
                client_info.server_connected = False
                client_info.server_socket = None


"""-----------------
PyQT Window creation
-----------------"""

# Get UI file and load as window.
qtCreatorFile = "window_design.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)



# PyQT application.
class MyGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, game):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


        # button Onclick
        self.InputButton.clicked.connect(lambda: self.enter_command())

        # When enter is pressed in input box.
        self.UserInputBox.returnPressed.connect(lambda: self.enter_command())



    def enter_command(self):
        self.new_input = self.UserInputBox.text().lower()
        print("Client input entered.")
        print(self.new_input)

        # Send to the server!!!
        send_function(self.new_input)

        self.DisplayText(self.new_input)
        self.UserInputBox.setText("")

    def DisplayText(self, text):
        self.textDisplay.append(text)

    def DisplayPlayerName(self, name):

        self.ui.playerName = name

    def DisplayCurrentRoom(self, room):
        self.currentRoom = room

def send_function(new_input):
    if client_info.server_connected:

        client_info.server_socket.send(new_input.encode())








def main_thread(client_info, MyGUI):
    print("Main Thread Running")
    client_info.server_connected = False

    while (client_info.server_connected is False) and (client_info.running is True):
        try:

            if client_info.server_socket is None:
                client_info.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if client_info.server_socket is not None:
                client_info.server_socket.connect(("127.0.0.1", 8222))

                client_info.server_connected = True
                client_info.current_receive_thread = threading.Thread(target=receive_thread, args=(client_info, MyGUI,))
                client_info.current_receive_thread.start()

            print("Server Connected")
            MyGUI.DisplayText("Server Connected.")
            MyGUI.DisplayText("\n                               THE ELEVENTH HOUR\n" \
                                    "--------------------------------------------------------------------------------------------\n" \
                                    "You step through the bubble surrounding the small town, cut off from the rest of the world. \n" \
                                    "As you do, you find yourself standing in a bright white void. \n" \
                                    "An old woman stands in front of you holding a small Chalice. \n" \
                                    "She whispers, 'It's you. Find me.' \n" \
                                    "The woman disappears and you find yourself standing at the entrance into town. \n" \
                                    "--------------------------------------------------------------------------------------------\n")

            while client_info.server_connected is True:
                sleep(1.0)


        except socket.error:
            print("No Server")

            sleep(1)
            client_info_lock.acquire()

            MyGUI.DisplayText("No Server. Attempting connection...")

            client_info_lock.release()


if __name__ == '__main__':
    #main()
    if client_running:
        # Create qtApplication
        GUI = QtWidgets.QApplication(sys.argv)

        # Create and show qtWindow
        window = MyGUI(None)
        window.show()

        # main()
        client_info.current_main_thread = threading.Thread(target=main_thread, args=(client_info, window))
        client_info.current_main_thread.start()

        # Event loop
        sys.exit(GUI.exec_())


def main():
    global connected
    global my_socket
    global running
    """
    print("\n                               THE ELEVENTH HOUR\n" \
          "--------------------------------------------------------------------------------------------\n" \
          "You step through the bubble surrounding the small town, cut off from the rest of the world. \n" \
          "As you do, you find yourself standing in a bright white void. \n" \
          "An old woman stands in front of you holding a small Chalice. \n" \
          "She whispers, 'It's you. Find me.' \n" \
          "The woman disappears and you find yourself standing at the entrance into town. \n" \
          "--------------------------------------------------------------------------------------------\n")



    while running:
        while not connected:

            if my_socket is None:
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                my_receive_thread = threading.Thread(target=receive_thread, args=(my_socket,))
                my_receive_thread.start()

            try:
                my_socket.connect(("127.0.0.1", 8222))
                print("Connection to Server established.\n")
                connected = True
            except socket.error:
                connected = False
                print("Trying to connect...")
                sleep(1)



        while connected:
            try:

                next_option_1 = "What shall you do now? : "
                next_option_2 = "What will you do next? : "
                next_option_3 = "What action do you take next? : "
                next_option_4 = "What's your next move? : "
                list_next_option = [next_option_1, next_option_2, next_option_3, next_option_4]

                input_string = input(random.choice(list_next_option))
                input_string = input_string.lower()
                my_socket.send(input_string.encode())
                sleep(0.5)

                if input_string == "quit" or input_string == "q" or input_string == "exit":

                    running = False
                    raise SystemExit


            except socket.error:
                print("Trying to connect...")
                sleep(1)
                connected = False
                my_socket = None

            while message_queue.qsize() > 0:
                print(message_queue.get())

    print("Exiting Program")
    my_socket.close()
"""