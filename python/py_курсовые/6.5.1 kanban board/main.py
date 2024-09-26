"""
Getting data of selected source, analyzing metric and billing data,
create cards of kanban board for delete resources, and save reports
"""
from modules.monitoring import MonitoringServer
from modules.taiga import TaigaServer
from modules.database import DBServer
from modules.generator import SSHServer
from modules.parser import get_analytic_dictionary
from modules import report, billing
import requests


def main():
    """Main module"""
    board = TaigaServer()
    board_session = requests.Session()
    board_token, board_user_id = board.get_auth_token_and_user_id(board_session)

    if board_token:

        existed_cards = board.get_card_list(session=board_session, token=board_token)

        clear_kanban = input('Are you want to clear a kanban board before '
                             'you collect a new metrics [y/n], default: no: ')
        if clear_kanban.lower() == 'y':
            board.delete_all_card(session=board_session, token=board_token, card_list=existed_cards)
            existed_cards = {}

        team_data = ''
        billing_data = ''

        source_metric = input('Please input the metrics source - HTTP or DB [http/db]: ')

        if source_metric == 'http':

            mon_server = MonitoringServer()
            team_data = mon_server.metric_data
            billing_data = mon_server.billing_data

        elif source_metric == 'db':
            ssh_server = SSHServer()
            is_generator_start = ssh_server.run_metric_generator()
            if is_generator_start:
                db_server = DBServer()
                team_data = db_server.get_metric_from_db()
        else:
            print('Your answer is not "http" or "db". Program was stopped.')

        if team_data:
            analytic_dictionary = get_analytic_dictionary(team_data)

            new_card_list = board.get_new_card_list(
                data=analytic_dictionary,
                card_list=existed_cards,
                user_id=board_user_id
            )

            board.create_new_cards(
                session=board_session,
                token=board_token,
                card_list=new_card_list
            )

            report.save_metric_report(analytic_dictionary, 'report.csv')

            if billing_data:
                charge_dictionary, economy_dictionary = billing.analyze_billing_data(
                    analytic=analytic_dictionary,
                    billing_data=billing_data
                )
                report.save_charge_report(charge_dictionary, 'charge.csv')
                report.save_economy_report(economy_dictionary, 'economy.csv')


if __name__ == '__main__':
    main()
