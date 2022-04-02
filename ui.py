import os
import time

class Ui:
    def __init__(self):
        pass

    @staticmethod
    def add_folder(new_folder : str):
        os.mkdir(new_folder)

    @staticmethod
    def get_file_weight(filename: str):
        return os.path.getsize(filename)


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
        ---new Server---
        name:{new_server['name']}
        url_bind:{new_server['url_bind']}
        url_connect:{new_server['url_connect']}
        number_partitions:{new_server['number_partitions']}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_information_new(new_msg):
        msg  = f'''
        --- New Information --
        msg:{new_msg}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_new_token(new_token: int):
        msg = f'''
        ---new Token---
        new token delivered to a user:{new_token}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_new_assign_servers(token_id, file_name, file_weight, number_of_parts):
        msg = f'''
        ---new Save---
        token_id:{token_id}
        file_name:{file_name}
        file_weight:{file_weight}
        number_of_parts:{number_of_parts}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_error(msg_error):
        msg = f'''
        --- msg Error --
        message:{msg_error}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_information(name_file, token_user, link):
        msg = f'''
        --- msg Information ---
        new link for the file:{name_file}
        the user token that generated it:{token_user}
        link to get the file:{link}
        '''
        print(msg)
        time.sleep(4)
    #server methods
    @staticmethod
    def msg_acceptance_proxy(new_msg: str):
        msg = f'''
        ---msg from proxy---
        message:{new_msg}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_save_part_file(information_file):
        msg = f"""
        ---msg server(upload information) :D ---
        file_name: {information_file['real_name']}
        size: {information_file['size']}
        part_number: {information_file['part']}
        url_connect: {information_file['url_connect']}
        user_token: {information_file['toke_correspondent']}
        modified_name : {information_file['modified_name']}
        file_location : {information_file['name']}
        """
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
    def msg_new_file(your_token, file_name, file_weight, number_of_parts):
        msg = f'''
        ---New File---
        Your_token:{your_token}
        file_name:{file_name}
        file_weight:{file_weight}
        number_of_parts:{number_of_parts}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_from_proxy(msg):
        msg = f'''
        ---Proxy Response---
        msg:{msg}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def msg_from_server(msg):
        msg = f'''
        --- Server Response ---
        msg: {msg}
        '''
        print(msg)
        time.sleep(4)

    @staticmethod
    def show_message(msg):
        print(f'\n{msg}')
        time.sleep(4)

    @staticmethod
    def check_file_existence(name_file):
        return os.path.exists(name_file)

    @staticmethod
    def partition(name_file, size, token):
        #function to know in how many parts the file that we are going to upload fits
        file_information = {}
        i = 1
        with open(name_file, 'rb') as f:
            content = f.read(size)
            if content:
                while content:
                    file_information[i] = {
                        'real_name' : name_file,
                        'modified_name' : f'{token}_' + 'part_' + str(i) + f'_{name_file}',
                        'size': len(content)
                    }
                    content = f.read(size)
                    i += 1
        return Ui.get_file_weight(name_file), len(file_information), file_information

    @staticmethod
    def delete_file(path):
        estado = None
        try:
            os.remove(path)
            Ui.show_message(f'the base file {path} is deleted because it exists')
            estado = True
        except:
            Ui.show_message(f'the base file {path} did not exist')
            estado = False
        return estado

    @staticmethod
    def get_token(link):
        token = ''
        for c in link:
            if c != '_':
                token += c
            else:
                break
        return token

