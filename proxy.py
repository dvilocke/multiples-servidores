import zmq
import pickle
import random

from ui import *

class Proxy:

    CONTEXT = zmq.Context()
    URL = 'tcp://*:5555'

    #information of all the servers connected to the proxy
    server_information = []

    #history of save files of all users
    user_history = {}

    def __init__(self):
        self.socket_response = self.CONTEXT.socket(zmq.REP)
        self.socket_request = self.CONTEXT.socket(zmq.REQ)

    def generate_token(self):
        while True:
            new_token = random.randint(0,100)
            if new_token not in self.user_history:
                self.user_history[new_token] = []
                break
        return new_token

    def start(self):
        self.socket_response.bind(self.URL)
        while True:
            message = self.socket_response.recv_multipart()
            if message[0].decode() == 'save_server':
                new_server = pickle.loads(message[1])
                self.server_information.append(new_server)
                msg = f"The server {new_server['name']} was accepted"
                self.socket_response.send(msg.encode())
                Ui.msg_new_server(new_server)
                continue

            elif message[0].decode() == 'get_token_client':
                new_token = self.generate_token()
                Ui.msg_new_token(new_token)
                self.socket_response.send(str(new_token).encode())
                continue


if __name__ == '__main__':
    Proxy().start()


