"""Working with SSH-server"""
from os import getenv
import paramiko


class SSHServer():
    """Working with generator server over SSH-connection"""
    def __init__(self):
        self.__hostname = 'localhost'
        self.__port = 2222
        self.__username = getenv('SSH_USERNAME')
        self.__password = getenv('SSH_PASSWORD')
        self.generator_command = 'monitoring_module 0'

    @property
    def cred_params(self):
        """Getting credentials as params"""
        return {
            'hostname': self.__hostname,
            'port': self.__port,
            'username': self.__username,
            'password': self.__password
        }

    def run_metric_generator(self):
        """
        Running metric generator with command over SSH-connection
        :return: True/False
        """
        is_generator_start = False
        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            try:
                ssh_client.connect(**self.cred_params)
                _, _, stderr = ssh_client.exec_command(self.generator_command)
                if stderr.read():
                    print(f'Error to start metric generator: {stderr.read()}')
                else:
                    is_generator_start = True
            except paramiko.ssh_exception.NoValidConnectionsError:
                print('Unable connected to SSH-server')
            except paramiko.ssh_exception.AuthenticationException:
                print('Authentication failed on SSH-server')
        return is_generator_start
