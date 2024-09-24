from modules.taiga import TaigaServer
from modules.database import DBServer
from modules.generator import SSHServer
from modules.parser import get_analytic_dictionary
from modules import monitoring, report


def main():

    board = TaigaServer()
    user_token, user_id = board.get_auth_token_and_user_id()

    if user_token:

        existed_cards = board.get_card_list()

        clear_kanban = input('Are you want to clear a kanban board before you collect a new metrics [y/n], default: no: ')
        if clear_kanban.lower() == 'y':
            board.delete_all_card(existed_cards)
            existed_cards = {}

        team_data = ''

        source_metric = input('Please input the metrics source - HTTP or DB [http/db]: ')

        if source_metric == 'http':
            team_data = monitoring.get_metric()
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

            new_card_list = board.get_new_card_list(data=analytic_dictionary, card_list=existed_cards)
            board.create_new_cards(new_card_list)

            report_filename = 'report.csv'
            report.save_report(analytic_dictionary, report_filename)
            # uncomment if you want to print report file
            # report.print_report(report_filename)


if __name__ == '__main__':
    main()
