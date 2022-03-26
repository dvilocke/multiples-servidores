import os
import time

class Ui:
    def __init__(self):
        pass

    @staticmethod
    def add_folder(new_folder : str):
        os.mkdir(new_folder)

    @staticmethod
    def clear_console():
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    @staticmethod
    def msg_new_server(new_server : dict):
        msg = f'''
        ----new Server----
        name:{new_server['name']}
        url:{new_server['url']}
        memory:{new_server['memory']}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_acceptance_proxy(new_msg: str):
        msg = f'''
        ----msg from proxy----
        message:{new_msg}
        '''
        print(msg)
        time.sleep(4)