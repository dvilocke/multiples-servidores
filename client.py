import zmq
import pickle
from ui import *

class Client:

    CONTEXT = zmq.Context()
    URL_PROXY = 'tcp://localhost:5555'
    SIZE = 78
    dictionary_of_links = {}

    def __init__(self):
        self.token : int = 0
        self.socket_request = self.CONTEXT.socket(zmq.REQ)
        self.name_file : str = ''

    def request_token(self):
        self.socket_request.connect(self.URL_PROXY)
        self.socket_request.send_multipart(
            ['get_token_client'.encode()]
        )
        new_token = int(self.socket_request.recv().decode())
        self.socket_request.disconnect(self.URL_PROXY)
        return new_token

    #function to send to servers
    def send_to_servers(self, route):
        file = open(self.name_file, 'rb')
        for file_with_path in route:
            self.socket_request.connect(file_with_path['url_connect'])
            content = file.read(file_with_path['size'])
            self.socket_request.send_multipart(
                ['save_file_part_client'.encode(), content, pickle.dumps(file_with_path)]
            )
            self.socket_request.recv()
            self.socket_request.disconnect(file_with_path['url_connect'])
            
        file.close()

    def download_file(self, link):
        self.socket_request.connect(self.URL_PROXY)
        self.socket_request.send_multipart(
            ['there_is_this_link_client'.encode(), link.encode()]
        )
        message = self.socket_request.recv_multipart()
        Ui.msg_from_proxy(message[1].decode())
        self.socket_request.disconnect(self.URL_PROXY)
        if message[0].decode() == '1':
            pass

    def save_file(self):
        self.socket_request.connect(self.URL_PROXY)
        information_file = Ui.partition(self.name_file, self.SIZE, self.token)
        #show all the information of the file to the client that is going to send
        Ui.msg_new_file(self.token, information_file[2][1]['real_name'], information_file[0], information_file[1])
        self.socket_request.send_multipart(
            ['save_file_client'.encode(), pickle.dumps(information_file), str(self.token).encode()]
        )
        message  = self.socket_request.recv_multipart()
        self.socket_request.disconnect(self.URL_PROXY)
        Ui.msg_from_proxy(message[2].decode())

        if message[0].decode() == '1':
            route = pickle.loads(message[1])
            link_to_share = message[3].decode()
            self.dictionary_of_links[route[0]['real_name']] = link_to_share
            self.send_to_servers(route)


    def menu(self):
        #Before starting, I ask the proxy for the token so that I can get to know myself among many users.
        self.token = self.request_token()
        while True:
            print(Ui.menu_user(), end='')
            option = int(input())
            if option == 1:
                name_file = input('\nEnter file name:')
                if Ui.check_file_existence(name_file):
                    self.name_file = name_file
                    self.save_file()
                else:
                    Ui.show_message(f'The file:{name_file} does not exists')
            elif option == 2:
                new_link = input('enter the link to download:')
                self.download_file(new_link)
            elif option == 3:
                break

if __name__ == '__main__':
    Client().menu()