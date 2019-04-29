import threading
import socket
import time
import json
from queue import *
from player import player
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

''' #==============================================================================

                                Client Information

''' #==============================================================================

class ClientInfo:

    # Allows switching of game states in input.py
    LoginPanel = 0
    InGame = 1
    HeroSelectScreen = 2

    ''' #==============================================================================
    
                                    Initialise Client
    
    ''' #==============================================================================
    def __init__(self, client_socket, dungeon):


        self.clientID = ""
        self.encryption_key = b"ATERRIBLEKEYYYYY" # must match key in client and be 16 chars
        self.username = "USERNAME"
        self.current_player = player(self, dungeon)

        # Queues
        self.input_queue = Queue()
        self.output_queue = Queue()

        self.client_socket = client_socket

        # Game states
        self.state = ClientInfo.LoginPanel

        self.connected = True
        self.can_receive = True
        self.can_send = True

        # client_receive_thread starter
        client_receive_thread = threading.Thread(target=ClientInfo.receive_thread, args=(self,))
        client_receive_thread.start()

        # client_send_thread starter
        client_send_thread = threading.Thread(target=ClientInfo.send_thread, args=(self,))
        client_send_thread.start()



    ''' #==============================================================================
    
                                    Cryptography
    
    ''' #==============================================================================

    def encrypt_info(self, data):

        print("Encrypting information to send")

        data2 = data
        key = self.encryption_key

        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data2, AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')

        result = json.dumps({'iv': iv, 'ciphertext': ct})
        print(data)
        return result


    def decrypt_info(self, info, key):
        print("Decrypting received information")

        try:

            b64 = json.loads(info)
            iv = b64decode(b64['iv'])
            ct = b64decode(b64['ciphertext'])
            cipher = AES.new(key, AES.MODE_CBC, iv)

            result = unpad(cipher.decrypt(ct), AES.block_size)

            return result.decode('utf-8')

        except:
            print("Decryption Error...")

    ''' #==============================================================================
    
                                    Receive Thread
    
    ''' #==============================================================================

    def receive_thread(self):

        print("client receive_thread running")

        while self.can_receive:

            try:
                data = self.client_socket.recv(4096)

                decrypted_info = self.decrypt_info(data, self.encryption_key)
                received_text = decrypted_info

                self.input_queue.put(received_text)

            except socket.error:

                self.can_receive = False
                self.connected = False

                print("receive_thread: Connection to client lost...")

    ''' #==============================================================================
    
                                    Send Thread
    
    ''' #==============================================================================

    def send_thread(self):

        print("send_thread running")

        while self.can_send:
            info_dict = {"Time": time.ctime(), "Message": ""}

            try:
                if self.output_queue.qsize() > 0:

                    # Get the output message to be sent
                    output_string = self.output_queue.get()

                    info_dict['Message'] = output_string
                    json_packet = json.dumps(info_dict)

                    header = len(json_packet).to_bytes(2, byteorder='little')

                    # Send data packets to the player
                    self.client_socket.send(header)
                    data = json_packet.encode()

                    print(self.username + ": " + output_string)

                    encrypted_data = self.encrypt_info(data).encode("utf-8")

                    self.client_socket.send(encrypted_data)
                    time.sleep(0.5)

            except socket.error:
                self.can_send = False
                self.connected = False
                print("send_thread: Connection to client lost...")


    ''' #==============================================================================
    
                                    Data Transmission
    
    ''' #==============================================================================

    # adds a new message to the output queue to be sent to the client of this user
    def add_to_output_queue(self, message, hidden = False):

        if hidden:
            self.output_queue.put("SYSTEM:" + message) # Use to send hidden information
        else:
            self.output_queue.put("DISPLAY:" + message) # Otherwise output to display