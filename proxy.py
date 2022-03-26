import zmq
import pickle

from ui import *

class Proxy:

    CONTEXT = zmq.Context()
    URL = 'tcp://*:5555'

    server_information = []

    def __init__(self):
        self.socket_response = self.CONTEXT.socket(zmq.REP)
        self.socket_request = self.CONTEXT.socket(zmq.REQ)

    def start(self):
        self.socket_response.bind(self.URL)
        while True:
            message = self.socket_response.recv_multipart()
            if message[0].decode() == 'save_server':
                new_server = pickle.loads(message[1])
                self.server_information.append(new_server)
                msg = f"The server {new_server['name']} was accepted"
                self.socket_response.send(msg.encode())
                print(self.server_information)
                Ui.msg_new_server(new_server)
                continue


if __name__ == '__main__':
    Proxy().start()


