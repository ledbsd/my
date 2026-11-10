"""Server types description for work"""
import requests


class UsersConfigServer():
    """Users configuration storing server"""

    def __init__(self, url: str):
        """
        Users configuration storing server
        :param url: configuration server URl
        """
        self.url = url

    def get_config_from_server(self):
        """
        Getting metrics from monitoring server over http
        :return: metric data
        """
        users_data = None
        try:
            response = requests.get(self.url, timeout=5)
            if response.status_code == 200:
                users_data = response.json()
            else:
                print(f'Connection to conf_server was failed with code: {response.status_code}.')
        except requests.exceptions.JSONDecodeError:
            print('Server answer is not JSON.')
        except requests.exceptions.ConnectionError:
            print('Connection to conf_server was failed.')

        return users_data
