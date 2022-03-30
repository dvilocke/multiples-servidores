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

    def assign_server(self):
        for server in self.server_information:
            if not server['full']:
                partition_counter = server['partition_counter']
                partition_counter += 1
                if partition_counter > server['number_partitions']:
                    server['full'] = True
                else:
                    #the server has more space
                    server['partition_counter'] = partition_counter
                    return server
        return None


    def assign_route(self, information_file, client_token):
        follow = True
        token_id = client_token
        file_name = information_file[2][1]['real_name']
        file_weight = information_file[0]
        number_of_parts = information_file[1]

        Ui.msg_new_assign_servers(token_id, file_name, file_weight, number_of_parts)

        route = []

        for number_file in range(1, information_file[1] + 1):
            #we get the complete file with your information
            file = information_file[2][number_file]
            #weight = file['size']
            server = self.assign_server()
            if server is not None:
                file |= {
                    'toke_correspondent': client_token,
                    'part': number_file,
                    'name': server['name'],
                    'url_bind' : server['url_bind'],
                    'url_connect': server['url_connect']
                }
                route.append(file)
            else:
                #it means that the servers are full, so the files have nowhere to go
                follow = False
                msg = f"Error, the servers are full, the file {file['real_name']} could not be stored"
                Ui.msg_error(msg)
                break

        return route if follow else None

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
                #check if we have registered servers
                if len(self.server_information) != 0:
                    if self.there_are_servers_available():
                        #answer the route well -> check
                        route = self.assign_route(pickle.loads(message[1]), int(message[2].decode()))
                        if route is not None:
                            #save route and generate link -> revisar
                            self.socket_response.send_multipart(
                                ['1'.encode(), pickle.dumps(route), 'Success: route generated successfully'.encode()]
                            )
                        else:
                            #the servers are full -> check
                            Ui.msg_error(f'the token {int(message[2].decode())}, provoke remaining storage exhausted ')
                            self.socket_response.send_multipart(
                                ['0'.encode(), ''.encode(), 'Error: remaining storage exhausted'.encode()]
                            )
                    else:
                        #the servers are already full, they do not accept more requests until a new one is run
                        Ui.msg_error(f'the token {int(message[2].decode())}, provoke full servers')
                        self.socket_response.send_multipart(
                            ['0'.encode(), ''.encode(), 'Error: full servers'.encode()]
                        )
                else:
                    #no server registered in the proxy --> check
                    Ui.msg_error(f'the token {int(message[2].decode())}, provoke no server registered in the proxy')
                    self.socket_response.send_multipart(
                        ['0'.encode(), ''.encode(), 'Error: no server registered in the proxy'.encode()]
                    )
                continue

if __name__ == '__main__':
    Proxy().start()


