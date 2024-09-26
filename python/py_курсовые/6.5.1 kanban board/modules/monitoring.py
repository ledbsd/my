"""Working with monitoring server"""
import requests


class MonitoringServer():
    """Monitoring server with endpoint name and data getters"""
    def __init__(self):
        self.metric_url = 'http://localhost:21122/monitoring/infrastructure/using/summary/0'
        self.billing_url = 'http://localhost:21122/monitoring/infrastructure/using/prices'

    @staticmethod
    def get_data(url: str):
        """
        Getting metrics from monitoring server over http
        :return: metric data
        """
        data = ''
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.text
            else:
                print(f'Connection to mon_server was failed with code: {response.status_code}.')
        except requests.exceptions.ConnectionError:
            print('Connection to mon_server was failed')
        return data

    @property
    def metric_data(self):
        """Getting metric data"""
        return self.get_data(self.metric_url)

    @property
    def billing_data(self):
        """Getting billing data"""
        return self.get_data(self.billing_url)
