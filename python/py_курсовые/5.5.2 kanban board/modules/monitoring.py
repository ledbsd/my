import requests

def get_metric():
    """
    Getting metrics from monitoring server over http
    :return: metric data
    """
    monitoring_server_url = 'http://localhost:21122/monitoring/infrastructure/using/summary/0'
    team_data = ''
    try:
        response = requests.get(monitoring_server_url, timeout=5)
        if response.status_code == 200:
            team_data = response.text
        else:
            print(f'Connection to monitoring server was failed with code: {response.status_code}.')
    except requests.exceptions.ConnectionError:
        print('Connection to monitoring server was failed')
    return team_data
