import sys
import zmq
import pickle
import  shutil

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
    NUMBER_PARTITIONS  = 0

    def __init__(self, url:str, number_partitions):
        self.url = url
        self.socket_response = self.CONTEXT.socket(zmq.REP)
        self.socket_request = self.CONTEXT.socket(zmq.REQ)
        self.NUMBER_PARTITIONS = number_partitions

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

    def save_file(self, contents, information_file):
        with open(information_file['modified_name'], 'ab') as f:
            f.write(contents)
        #move it to the appropriate folder
        Ui.msg_save_part_file(information_file)
        shutil.move(information_file['modified_name'], self.FOLDER)

    def get_url_connect(self):
        new_list = list(self.url)
        return ''.join(new_list[-4::])

    def turn_on(self):
        #we are going to create a folder where the files of this server will be stored
        self.FOLDER = self.assign_folder()
        self.socket_request.connect(self.URL_PROXY)

        self.socket_request.send_multipart(
            ['save_server'.encode(), pickle.dumps(
                {
                    'name': self.FOLDER,
                    'url_bind': self.url,
                    'url_connect': 'tcp://localhost:' + self.get_url_connect(),
                    'number_partitions': self.NUMBER_PARTITIONS,
                    'partition_counter': 0,
                    'full': False
                }
            )]
        )
        Ui.msg_acceptance_proxy(self.socket_request.recv().decode())
        self.start()

    def get_file_client(self, name_file, size):
        url = self.FOLDER + '/' + name_file
        with open(url, 'rb') as f:
            content = f.read(size)
        return content

    def start(self):
        self.socket_response.bind(self.url)
        while True:
            message = self.socket_response.recv_multipart()
            if message[0].decode() == 'save_file_part_client':
                self.save_file(message[1], pickle.loads(message[2]))
                self.socket_response.send(b'ok')
                continue
            elif message[0].decode() == 'get_file_client':
                name_file = message[1].decode()
                size = int(message[2].decode())
                content = self.get_file_client(name_file, size)
                self.socket_response.send(content)
                continue

if __name__ == '__main__':
    number = sys.argv[1]
    NUMBER_PARTITIONS = int(sys.argv[2])
    connection = 'tcp://*:' + str(number)
    server = Server(url=connection, number_partitions=NUMBER_PARTITIONS)
    server.turn_on()
