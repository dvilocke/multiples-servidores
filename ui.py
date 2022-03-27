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


    #proxy methods
    @staticmethod
    def msg_new_server(new_server : dict):
        msg = f'''
        ----new Server----
        name:{new_server['name']}
        url_bind:{new_server['url_bind']}
        url_connect:{new_server['url_connect']}
        memory:{new_server['memory']}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_new_token(new_token: int):
        msg = f'''
        ----new Token----
        new token delivered to a user:{new_token}
        '''
        print(msg)
        time.sleep(4)

    #server methods
    @staticmethod
    def msg_acceptance_proxy(new_msg: str):
        msg = f'''
        ----msg from proxy----
        message:{new_msg}
        '''
        print(msg)
        time.sleep(4)

    #client methods
    @staticmethod
    def menu_user():
        Ui.clear_console()
        start_menu = '''
        ---File System---
        1.Enter File
        2.Download file
        3.Exit
        Option:'''
        return start_menu

    @staticmethod
    def show_message(msg):
        print(f'\n{msg}')
        time.sleep(4)

    @staticmethod
    def check_file_existence(name_file):
        return os.path.exists(name_file)




