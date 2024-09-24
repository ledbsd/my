class PullModelMetricCollectionAgent():
    """
    Pull-model metric collection agent
    """
    def __init__(self, server_ip:str, server_key: str, collection_period: int):
        """
        Constructor
        :param server_ip: connection server IP-address
        :param server_key: connection server access key
        :param collection_period: metric collection period (in seconds)
        :
        :event_collection_count: the number of event collecting count
        """
        self.server_ip_address = server_ip
        self.server_key = server_key
        self._collection_period = collection_period
        self._event_collection_count = 0

    def collect_metrics(self):
        """
        Collecting events
        :return: increment event collecting count
        """
        print(f'Server {self.server_ip_address} events were collected. Next collection in {self._collection_period} seconds.')
        self._event_collection_count += 1

    def clear_agent_cache(self):
        """
        Clearing agent cache
        :return: resetting the number of collection events
        """
        self._event_collection_count = 0
        print('Agent cache was clear')

    def get_event_collection_calls(self):
        """
        Getting information about the current number of event collecting count
        :return:
        """
        print(f'There are {self._event_collection_count} events collected from server {self.server_ip_address}.')

    @staticmethod
    def _calculate_second(line: str):
        """
        Calculating value to string
        :param line: like '1h32m14s', '32m14s', '14s' etc
        :return: number of second
        """
        if line.find('-') != -1:
            raise ValueError('Period must be positive value')
        hours = '0'
        minutes = '0'
        seconds = '0'

        position_h = line.find('h')
        if position_h != -1:
            hours = line[:position_h]

        position_m = line.find('m')
        if position_m != -1:
            minutes = line[position_h + 1:position_m]

        position_s = line.find('s')
        if position_s != -1:
            if position_m != -1:
                seconds = line[position_m + 1:position_s]
            else:
                seconds = line[position_h + 1:position_s]

        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

    @property
    def collection_period(self):
        """
        Getter: collection_period
        :return: collection_period value
        """
        return self._collection_period

    @collection_period.setter
    def collection_period(self, new_value: str):
        """
        Setter: collection_period
        :param new_value: new collection_period
        """
        self._collection_period = self._calculate_second(new_value)


class PushModelMetricCollectionAgent(PullModelMetricCollectionAgent):
    """"
    Push-model metric collection agent
    """
    def __init__(self, server_ip: str, server_key: str, collection_period: int, sending_period: int):
        """
        Constructor
        :param server_ip: connection server IP-address
        :param server_key: connection server access key
        :param collection_period: metric collection period (in seconds)
        :param sending_period: event sending period (in seconds)
        """
        super().__init__(server_ip, server_key, collection_period)
        self._sending_period = sending_period

    def send_metrics(self):
        """
        Sending events to the metrics collection server
        :return:
        """
        print(f'Server {self.server_ip_address} events were collected, sent to metrics collection server. Next sending in {self._sending_period} seconds.')

    @property
    def sending_period(self):
        """
        Getter: sending_period
        :return: sending_period value
        """
        return self._sending_period

    @sending_period.setter
    def sending_period(self, new_value: str):
        """
        Setter: sending_period
        :param new_value: new sending period
        """
        self._sending_period = self._calculate_second(new_value)


class PrometheusMetricCollectionAgent(PullModelMetricCollectionAgent):
    """
    Metric collection agent for Prometheus
    """
    def send_metrics(self):
        """
        Sending events to the metrics collection server by request from Prometheus.
        :return:
        """
        print(f'Server {self.server_ip_address} events were collected, sent by request from Prometheus.')


class CarbonMetricCollectionAgent(PushModelMetricCollectionAgent):
    """
        Metric collection agent for Carbon
    """
    def __init__(self, server_ip: str, server_key: str, collection_period: int, sending_period: int, carbon_ip: str):
        """
        Constructor
        :param server_ip: connection server IP-address
        :param server_key: connection server access key
        :param collection_period: metric collection period (in seconds)
        :param sending_period: event sending period (in seconds)
        :param carbon_ip: carbon server IP-address
        """
        super().__init__(server_ip, server_key, collection_period, sending_period)
        self.carbon_ip = carbon_ip

    def send_metrics(self):
        """
        Sending events to the metrics collection server from Carbon agent
        :return:
        """
        print(f'Server {self.server_ip_address} events were collected, sent to Carbon. Next sending in {self._sending_period} seconds.')


def main():

    separator_line = 60 * '-'
    
    print('Step1. I define two agents with different types.')
    carbon_agent = CarbonMetricCollectionAgent(server_ip='192.168.1.3', server_key='qwerty', collection_period=500, sending_period=40, carbon_ip = '10.0.0.1')
    prom_agent = PrometheusMetricCollectionAgent(server_ip='192.168.1.4', server_key='qwerty', collection_period=500)
    print(separator_line)

    print('Step2. I call collect_method for agents.')
    print('The program must be print info about agents, and now event_collection_count agents must be stay "1".')
    carbon_agent.collect_metrics()
    prom_agent.collect_metrics()
    carbon_agent.get_event_collection_calls()
    prom_agent.get_event_collection_calls()
    print(separator_line)

    print('Step3. I call send_metrics for agents.')
    print('The program must be print different info about agents.')
    carbon_agent.send_metrics()
    prom_agent.send_metrics()
    print(separator_line)

    print('Step4. I twice call collect_method for agents.')
    print('The program must be print info about agents, and now event_collection_count agents must be stay "3".')
    carbon_agent.collect_metrics()
    prom_agent.collect_metrics()
    carbon_agent.collect_metrics()
    prom_agent.collect_metrics()
    carbon_agent.get_event_collection_calls()
    prom_agent.get_event_collection_calls()
    print(separator_line)

    print('Step5. I call clear_agent_cache for Prometheus agents.')
    print('The program must be print info about agents, and now event_collection_count Prometheus agents must be stay "0".')
    print('Event_collection_count Carbon agents must be stay "3".')
    prom_agent.clear_agent_cache()
    carbon_agent.get_event_collection_calls()
    prom_agent.get_event_collection_calls()
    print(separator_line)

    print('Step6. I call current values of collection period for agents and request new values.')
    print('Format: like "1h32m14s", "32m14s", "14s", etc.')
    print(carbon_agent.collection_period)
    print(prom_agent.collection_period)
    new_collection_period_for_carbon_agent = input('Input new collection period for carbon agent:')
    new_collection_period_for_prom_agent = input('Input new collection period for prom agent:')
    print(separator_line)

    print('Step8. I call collection period for agents. If new value have "-", the program must be stop,')
    print('else the program must be print info about new collection period for agents.')
    carbon_agent.collection_period = new_collection_period_for_carbon_agent
    prom_agent.collection_period = new_collection_period_for_prom_agent
    print(carbon_agent.collection_period)
    print(prom_agent.collection_period)
    print(separator_line)

    print('Step9. I call current values of sending period for Carbon agent and request new values.')
    print('Format: like "1h32m14s", "32m14s", "14s", etc.')
    print(carbon_agent.sending_period)
    new_sending_period_for_carbon_agent = input('Input new sending period for carbon agent:')
    print(separator_line)

    print('Step10. I call sending_period period for Carbon agent. If new value have "-", the program must be stop,')
    print('else the program must be print info about new sending period for Carbon agent.')
    carbon_agent.sending_period = new_sending_period_for_carbon_agent
    print(carbon_agent.sending_period)


if __name__ == '__main__':
    main()
