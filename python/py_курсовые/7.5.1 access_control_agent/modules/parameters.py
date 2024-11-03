"""Parameters of the authorized_keys file and methods for working with it"""
import os.path
from datetime import datetime


class SshAuthorizedKey():
    """Methods for working with authorized_keys file"""

    def __init__(self, key_file_path):
        self.key_file_path = key_file_path
        self.key_file_permissions = 0o0600

    @staticmethod
    def create_key_list(user_config: list):
        """
        Configuring new authorized_keys file from server config
        :param user_config: users config
        :return: list of user keys for save to server
        """
        new_keys = []

        for user in user_config:
            if datetime.strptime(user['access_until'], '%d-%m-%Y') > datetime.today():
                new_keys.append(f"ssh-rsa {user['rsa_pub_key']} {user['email']}\n")

        return new_keys

    @staticmethod
    def create_temporary_key_file(key_list: list):
        """
        Saving keys list as
        temporary local file before put it to server
        :param key_list: list of user keys
        :return: local filename
        """
        temp_filename = '/root/new_keys'
        with open(temp_filename, 'w', newline='\n', encoding='utf-8') as file:
            file.writelines(key_list)
        return temp_filename

    def read_keyfile(self):
        """
        Reading server authorized_keys file. If it no exist, creating.
        :return: list of server current user keys
        """
        keys = []

        if os.path.isfile(self.key_file_path):
            with open(self.key_file_path, encoding='utf-8') as file:
                keys = file.readlines()
        else:
            with open(self.key_file_path, 'w', encoding='utf-8') as _:
                print(f'File {self.key_file_path} was not found on server '
                      f'and was created.')
            os.chmod(self.key_file_path, self.key_file_permissions)
        return keys

    def update_keyfile(self, new_key_file: str):
        """
        Updating server authorized_keys file
        :param new_key_file: local authorized_keys file
        :return: print update result
        """

        try:
            os.replace(new_key_file, self.key_file_path)
            os.chmod(self.key_file_path, self.key_file_permissions)
            print(f'File {self.key_file_path} was updated.')
        except PermissionError:
            print(f'Permission denied when update file {self.key_file_path}.')
