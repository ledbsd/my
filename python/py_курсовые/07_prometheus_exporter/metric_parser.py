"""Parsing the metric data"""


def analyze_metrics(metrics: dict):
    """
    Analyzing metrics to calculate all parameters that needed
    :param metrics: metrics dictionary
    :return: dictionary of metric parameters
    """
    metrics_dictionary = {}

    for metric_name in ('CPU', 'RAM', 'NetFlow'):

        metric_list = []
        for metric in metrics:
            for name, data in metric.items():
                if name == metric_name:
                    _, value = data.split(',')
                    metric_list.append(value)
        metrics_dictionary[metric_name] = metric_list

    return metrics_dictionary


def analyze_resource_id(resource_id: dict):
    """
    Analyzing resource ID to find metrics
    :param resource_id: resource_id dictionary
    :return: dictionary of resource
    """
    resource_dictionary = {}
    for resource, metrics in resource_id.items():
        metrics_dictionary = analyze_metrics(metrics)
        resource_dictionary[resource] = metrics_dictionary
    return resource_dictionary


def parsing_row_resource_data(resource_data: str):
    """
    Parsing row data to find resource ID
    :param resource_data: resource data rows
    :return: dictionary of resource ID
    """
    resource_id_dictionary = {}
    for row_resource_data in resource_data.split(';'):
        row_resource_data = row_resource_data[1:-1]
        resource_id, metric_name, metric_value = row_resource_data.split(',', 2)
        resource_id_dictionary.setdefault(resource_id, []).append({metric_name: metric_value})
    return resource_id_dictionary


def parsing_row_data(input_data: str):
    """
    Parsing row data to find teams
    :param input_data: data rows
    :return: dictionary of team
    """
    team_dictionary = {}
    for row_input_data in input_data.split('$'):
        (team_name, resource_data) = row_input_data.split('|')
        team_dictionary[team_name] = parsing_row_resource_data(resource_data)
    return team_dictionary


def get_analytic_dictionary(team_data: str):
    """
    Getting analytic data from metric data
    :param team_data: metric data
    :return: analytic data dictionary
    """

    analytic_dictionary = {}

    team_dictionary = parsing_row_data(team_data)

    for team_name, resource_id in team_dictionary.items():
        analytic_dictionary[team_name] = analyze_resource_id(resource_id)

    return analytic_dictionary
