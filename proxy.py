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

    def save_server(self, new_server):
        self.server_information.append(new_server)
        msg = f"The server {new_server['name']} was accepted"
        self.socket_response.send(msg.encode())
        Ui.msg_new_server(new_server)

    #function to consult availability in general of the servers
    def there_are_servers_available(self):
        total_servers = len(self.server_information)
        count_full = 0
        for server in self.server_information:
            if server['full']:
                count_full += 1
        return True if count_full != total_servers else False

    def assign_server(self, number_file):
        #comprobar los errores de asignacion
        for server in self.server_information:
            pass

    def assign_route(self, information_file, client_token):
        token_id = client_token
        file_name = information_file[2][1]['real_name']
        file_weight = information_file[0]
        number_of_parts = information_file[1]

        Ui.msg_new_assign_servers(token_id, file_name, file_weight, number_of_parts)

        for number_file in range(1, information_file[1] + 1):
            #we get the complete file with your information
            file = information_file[2][number_file]
            weight = file['size']
            self.assign_server(number_file, weight)

    def start(self):
        self.socket_response.bind(self.URL)
        while True:
            message = self.socket_response.recv_multipart()
            if message[0].decode() == 'save_server':
                self.save_server(pickle.loads(message[1]))
                continue

            elif message[0].decode() == 'get_token_client':
                new_token = self.generate_token()
                Ui.msg_new_token(new_token)
                self.socket_response.send(str(new_token).encode())
                continue

            elif message[0].decode() == 'save_file_client':
                if self.there_are_servers_available():
                    self.assign_route(pickle.loads(message[1]), int(message[2].decode()))
                    self.socket_response.send(b'ok')
                else:
                    Ui.msg_error('full servers')
                    self.socket_response.send(b'ok')
                continue


if __name__ == '__main__':
    Proxy().start()


