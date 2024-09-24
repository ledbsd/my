from modules.parser import DecisionType
from os import getenv
from datetime import datetime, timedelta
import requests


class TaigaServer():
    """Working with TAIGA server over API"""
    def __init__(self):
        self.__username = getenv('TAIGA_USERNAME')
        self.__password = getenv('TAIGA_PASSWORD')
        self.type = 'normal'
        self.url = 'http://localhost:9000/api/v1'
        self.user_token = ''
        self.user_id = ''
        self.card_list = {}

    @property
    def creds(self):
        return {
        'username': self.__username,
        'password': self.__password,
        'type': self.type
    }

    @property
    def session(self):
        return requests.Session()

    @staticmethod
    def get_due_date(date: str):
        """
        Formating "deadline date" from date of last measurement + 14 days.
        Format '%Y-%m-%d' was selected because Taiga accepts only it a due_date value
        :param date: date of last measurement
        :return: deadline date
        """
        deadline_days = 14
        date_format = '%Y-%m-%d'
        return (datetime.strptime(date, date_format) + timedelta(days=deadline_days)).strftime(date_format)

    def get_auth_token_and_user_id(self):
        """
        Getting auth token and user ID from taiga server
        :return: auth token and user ID
        """
        try:
            response = self.session.post(url=f'{self.url}/auth', json=self.creds, timeout=5)
            if response.status_code == 200:
                self.user_token = response.json()['auth_token']
                self.user_id = response.json()['id']
            else:
                print(f'Connection to TAIGA was failed with code: {response.status_code}.')
        except requests.exceptions.ConnectionError:
            print('Connection to TAIGA was failed')
        return self.user_token, self.user_id

    def get_card_list(self):
        """
        Getting all existed cards list
        :return: existed card list
        """
        headers = {
            'Authorization': f'Bearer {self.user_token}',
            'Content-Type': 'application/json',
            'x-disable-pagination': 'True'
        }
        try:
            response = self.session.get(f'{self.url}/userstories', headers=headers, timeout=5)
            if response.status_code == 200:
                for card in response.json():
                    self.card_list[card['subject']] = card['id']
                print(f'Kanban board cards: {len(self.card_list)}')
            else:
                print(f'Connection to TAIGA was failed with code: {response.status_code}.')
        except requests.exceptions.ConnectionError:
            print('Connection to TAIGA was failed')
        return self.card_list

    def create_new_cards(self, card_list: list):
        """
        Creating new cards
        :param card_list: list of cards than need to create
        :return: printing created card count
        """
        headers = {
            'Authorization': f'Bearer {self.user_token}',
            'Content-Type': 'application/json'
        }

        success_count = 0
        for card in card_list:
            try:
                response = self.session.post(f'{self.url}/userstories', headers=headers, json=card, timeout=5)
                if response.status_code != 201:
                    print(f'Creation task failed with code {response.status_code}.')
                else:
                    success_count += 1
            except requests.exceptions.ConnectionError:
                print('Connection to TAIGA was failed')
                break

        print(f'Cards added: {success_count}.')

    def delete_all_card(self, card_list: dict):
        """
        Deleting all cards
        :param card_list: existed card list
        :return: printing the deleted card count
        """
        delete_card_count = 0
        headers = {
            'Authorization': f'Bearer {self.user_token}',
            'Content-Type': 'application/json'
        }
        for card_id in card_list.values():
            response = self.session.delete(f'{self.url}/userstories/{card_id}', headers=headers, timeout=5)
            if response.status_code != 204:
                print(f'Failed to delete card {card_id}.')
                break
            else:
                delete_card_count += 1
        print(f'Cards deleted: {delete_card_count}')

    def get_new_card_list(self, data: dict, card_list: dict):
        """
        Getting list of cards than need to create.
        The list include all metric with decision 'delete' or 'extend', but exclude cards that already exist on board.
        :param data: metric dictionary
        :param card_list: existed cards
        :return: list of cards than need to create
        """
        new_card_list = []

        for team_name, resource_id in data.items():
            for resource, metrics in resource_id.items():
                for metric_name, metric_data in metrics.items():

                    card_name = None

                    if metric_data['decision'] == DecisionType.DELETE:
                        card_name = f'Cancel the use of resource {resource} for {metric_name} metric'
                    elif metric_data['decision'] == DecisionType.EXTEND:
                        card_name = f'Increase the quotas of resource {resource} for {metric_name} metric'

                    if card_name is not None and card_name not in card_list.keys():
                        new_card = {'subject': card_name,
                                    'tags': [team_name],
                                    'due_date': self.get_due_date(metric_data['last_date']),
                                    'description': f"usage_type: {metric_data['usage_type']},"
                                                   f"intensivity: {metric_data['intensivity']}",
                                    'assigned_to': self.user_id,
                                    'status': 1,
                                    'project': 1
                        }
                        new_card_list.append(new_card)
        return new_card_list
