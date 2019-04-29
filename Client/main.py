import sys
import socket
import threading
import time
import bcrypt
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

running: bool = True


""" #==============================================================================

                                Client Information

""" #==============================================================================

class ClientInfo:
    def __init__(self):

        self.server_socket = None
        self.connected = False
        self.running = True

        self.current_main_thread = None
        self.current_receive_thread = None

        self.encryption_key = b"ATERRIBLEKEYYYYY"


clientInfo = ClientInfo()
clientInfoLock = threading.Lock()


""" #==============================================================================

                                Window Creation

""" #==============================================================================

# Get UI file and load as window.
qtCreatorFile = "window_design.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# PyQT application.
class QtWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Send startup message
        self.textDisplay.append("Window initialised.")

        # Hide the login panel
        self.hide_login_panel()



        # buttons Onclick
        self.InputButton.clicked.connect(lambda: self.text_input())

        self.LoginButton.clicked.connect(lambda: self.attempt_login())
        self.NewAccountButton.clicked.connect(lambda: self.attempt_account_creation())

        # When enter is pressed in input box.
        self.UserInputBox.returnPressed.connect(lambda: self.text_input())


    def text_input(self):

        self.new_nput = self.UserInputBox.text()
        print("User input submitted")

        self.text_to_display(self.new_nput)
        self.UserInputBox.setText("")

        # Send to the server!!!say
        send_data(self.new_nput)


    def text_to_display(self, text):

        self.textDisplay.append(text)
        self.textDisplay.moveCursor(QtGui.QTextCursor.End)

    ''' #==============================================================================
    
                                    Logging In
    
    ''' #==============================================================================




    def attempt_login(self):

        if len(self.UsernameInput.text()) > 4 and \
            len(self.PasswordInput.text()) > 4:

            username = self.UsernameInput.text()
            password = self.PasswordInput.text()

            # Send Username and password across for checking
            send_data("--!SaltCheck#" + username + "#" + password)

        else:
            self.text_to_display("!ERROR! - Credentials must be longer than 4 characters")


    def send_salted_password(self, recSalt):

        username = self.UsernameInput.text()
        password = self.PasswordInput.text().encode('utf-8')

        salt = recSalt.encode('utf-8')

        password = bcrypt.hashpw(password, salt)
        password = password.decode()

        # Send Username and password across for checking
        send_data("--!Login#" + username + "#" + password)


    def attempt_account_creation(self):

        if len(self.UsernameInput.text()) > 4 and \
            len(self.PasswordInput.text()) > 4:

            username = self.UsernameInput.text()
            password = self.PasswordInput.text()
            salt = bcrypt.gensalt(12)

            password = password.encode('utf-8')
            password = bcrypt.hashpw(password, salt)
            password = password.decode()
            salt = salt.decode()

            send_data("--!NewAccount#" + username + "#" + password + "#" + salt)

            self.UsernameInput.clear()
            self.PasswordInput.clear()


        else:
            self.text_to_display("!ERROR! - Credentials must be longer than 4 characters")


    def display_login_panel(self):

        self.loginPanel.show()

    def hide_login_panel(self):

        self.loginPanel.hide()


''' #==============================================================================

                                Cryptography

''' #==============================================================================

def encrypt_info(data):

    print("Encrypting DATA")

    dataa = data.encode()
    key = clientInfo.encryption_key

    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(dataa, AES.block_size))

    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')

    result = json.dumps({'iv':iv, 'ciphertext':ct})

    return result


def decrypt_info(data, key):

    b64 = json.loads(data)
    iv = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_CBC, iv)

    result = unpad(cipher.decrypt(ct), AES.block_size)

    return result.decode('utf-8')


def send_data(new_input):

    if clientInfo.connected:
        new_input = encrypt_info(new_input)
        clientInfo.server_socket.send(new_input.encode())
    else:
        window.text_to_display("ERROR - Client is not connected to a server")


''' #==============================================================================

                                Receive Thread

''' #==============================================================================

def receive_thread(clientInfo):

    print("receive_thread running")

    while clientInfo.connected is True:

        try:

            data_recv = clientInfo.server_socket.recv(4)

            payload_size = int.from_bytes(data_recv, byteorder='big')

            payload_data = clientInfo.server_socket.recv(payload_size)

            payload_data = decrypt_info(payload_data, clientInfo.encryption_key)

            data = json.loads(payload_data)

            print("Time received:" + data['Time'] + "\nMessage:[" + data['Message'] + "]")

            # Decrypts the data and checks the result
            parse_incoming_data(data['Message'])

        except socket.error:

            print("Server lost")
            window.text_to_display("Server lost")
            clientInfo.connected = False
            clientInfo.server_socket = None


''' #==============================================================================

   Function to determine what to do with the data received fromm the server 

''' #==============================================================================

def parse_incoming_data(data):

    split_list = data.split(":", 1)

    if split_list[0] == "DISPLAY":

        # Display received message on screen
        window.text_to_display(split_list[1])

    elif split_list[0] == "SYSTEM":

        # Use to update background information
        system_list = split_list[1].split("#",1)

        if system_list[0] == "SALT":
            window.send_salted_password(system_list[1])

        if system_list[0] == "LOGIN_SUCCESS":
            window.hide_login_panel()

        if system_list[0] == "UPDATE_ROOM":
            window.locationBox.setText("Location: " + system_list[1])

        if system_list[0] == "UPDATE_HERO_NAME":
            window.heroNameBox.setText("Hero: " + system_list[1])


    else:
        print(split_list)


''' #==============================================================================

                                Main Thread

''' #==============================================================================

def main_thread(clientInfo):
    print("main_thread running")
    clientInfo.connected = False


    ''' #==============================================================================
    
                                    Server Connection
    
    ''' #==============================================================================

    while (clientInfo.connected is False) and (clientInfo.running is True):

        try:

            if clientInfo.server_socket is None:

                clientInfo.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if clientInfo.server_socket is not None:

                clientInfo.server_socket.connect(("127.0.0.1", 8222))

            clientInfo.connected = True

            clientInfo.current_receive_thread = threading.Thread(target=receive_thread, args=(clientInfo,))
            clientInfo.current_receive_thread.start()

            print("Connected to Server.")
            #window.text_to_display("Client: Server Connected\n")

            window.display_login_panel()

            while clientInfo.connected is True:
                time.sleep(1.0)


        except socket.error:
            print("No connection to Server.")
            time.sleep(1.0)
            clientInfoLock.acquire()
            clientInfoLock.release()


''' #==============================================================================

                                Main

''' #==============================================================================

if __name__ == "__main__":

    if running:

        # Create qtApp
        app = QtWidgets.QApplication(sys.argv)

        # Create window
        window = QtWindow()
        window.show()

        # main()
        clientInfo.current_main_thread = threading.Thread(target=main_thread, args=(clientInfo,))
        clientInfo.current_main_thread.start()

        # Event loop
        sys.exit(app.exec_())
