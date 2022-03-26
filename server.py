
import zmq
import pickle

from ui import  *

class Server:

    #zmq variables
    CONTEXT = zmq.Context()

    #addresses
    URL_PROXY = 'tcp://localhost:5555'
    PATH_SERVER_COUNT = 'server_count.txt'

    #folder where the files will be saved
    FOLDER = ''

    #server variables
    MEMORY  = 0

    def __init__(self, url:str):
        self.url = url
        self.socket_response = self.CONTEXT.socket(zmq.REP)
        self.socket_request = self.CONTEXT.socket(zmq.REQ)

    def assign_folder(self):
        file = open(self.PATH_SERVER_COUNT, 'r')
        number = file.read()
        new_folder = 'server' + number
        file.close()

        file = open(self.PATH_SERVER_COUNT, 'w')
        file.write(str(int(number) + 1))
        file.close()

        Ui.add_folder(new_folder)

        return new_folder

    def turn_on(self):
        #we are going to create a folder where the files of this server will be stored
        self.FOLDER = self.assign_folder()
        self.socket_request.connect(self.URL_PROXY)

        self.socket_request.send_multipart(
            ['save_server'.encode(), pickle.dumps(
                {
                    'name': self.FOLDER,
                    'url': self.url,
                    'memory': self.MEMORY
                }
            )]
        )
        Ui.msg_acceptance_proxy(self.socket_request.recv().decode())
        self.start()

    def start(self):
        self.socket_response.bind(self.url)
        while True:
            message = self.socket_response.recv_multipart()


if __name__ == '__main__':
    Server(url='tcp://*:6666').turn_on()