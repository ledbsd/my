"""Access control agent for configuring SSH-server"""
import argparse
import json
import time
from urllib.parse import urlparse
from modules.parameters import SshAuthorizedKey
from modules.servers import UsersConfigServer

KEY_FILE_NAME = '/root/.ssh/authorized_keys'


def is_valid_url(url):
    """Validating URI address"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_config_from_file(filename):
    """Getting user config from local json file for program test"""
    try:
        with open(filename, encoding='utf-8') as file:
            user_config = json.load(file)
        return user_config
    except FileNotFoundError:
        print(f'File {filename} not found.')
    return None


def main():
    """Main program"""

    parser = argparse.ArgumentParser(description="SSH-server configuration program.")
    parser.add_argument(
        '-u', '--url',
        help='(Required) Configuration server URL. For debug mode set from a local file path.',
        required=True
    )
    parser.add_argument(
        '-p', '--period',
        help='(Required) Configuration server poll period (minutes).',
        required=True
    )

    args = parser.parse_args()

    if str(args.period).isdigit():

        while True:

            key_file = SshAuthorizedKey(KEY_FILE_NAME)

            if is_valid_url(args.url):
                config_server = UsersConfigServer(args.url)
                users_data = config_server.get_config_from_server()
            else:
                users_data = get_config_from_file(args.url)

            if users_data:
                current_keys = key_file.read_keyfile()
                new_keys = SshAuthorizedKey.create_key_list(users_data)

                if current_keys == new_keys:
                    print('Users config have not change.')
                else:
                    new_key_file = key_file.create_temporary_key_file(new_keys)
                    key_file.update_keyfile(new_key_file)

            time.sleep(int(args.period) * 60)

    else:
        print(f'Incorrect value of period minutes: {args.period}.')


if __name__ == '__main__':
    main()
