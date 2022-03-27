import zmq
from ui import *

class Client:

    CONTEXT = zmq.Context()
    URL_PROXY = 'tcp://localhost:5555'
    SIZE = 1024

    def __init__(self):
        self.token : int = 0
        self.socket_request = self.CONTEXT.socket(zmq.REQ)

    def request_token(self):
        self.socket_request.connect(self.URL_PROXY)
        self.socket_request.send_multipart(
            ['get_token_client'.encode()]
        )
        new_token = int(self.socket_request.recv().decode())
        return new_token

    def save_file(self, name_file):
        pass

    def menu(self):
        #Before starting, I ask the proxy for the token so that I can get to know myself among many users.
        self.token = self.request_token()

        while True:
            print(Ui.menu_user(), end='')
            option = int(input())
            if option == 1:
                name_file = input('\nEnter file name:')
                if Ui.check_file_existence(name_file):
                    self.save_file(name_file)
                else:
                    Ui.show_message(f'The file:{name_file} does not exists')
            elif option == 2:
                pass
            elif option == 3:
                break

if __name__ == '__main__':
    Client().menu()