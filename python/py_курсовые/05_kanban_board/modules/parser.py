"""Parsing the metric data"""
from enum import Enum


class ConstantType(Enum):
    """Class Enum with value call override"""
    def __get__(self, *args):
        return self.value


class UsageType(ConstantType):
    """List of constants for the usage type characteristic"""
    STABLE = 'Stable'
    JUMP = 'Jumps'
    DECREASE = 'Decrease'


class IntensivityType(ConstantType):
    """List of constants for the intensity type characteristic"""
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    EXTREME = 'Extreme'


class DecisionType(ConstantType):
    """List of constants for the decision characteristic"""
    DELETE = 'delete resource'
    EXTEND = 'extend resource'
    NORMAL = 'normal using'


def calculate_average(data: list):
    """
    Calculate average value from list
    :param data: list
    :return: average value
    """
    data = list(map(float, data))
    return sum(data) / len(data)


def calculate_median(data: list):
    """
    Calculate median value from list
    :param data: list
    :return: median value
    """
    data = sorted(list(map(float, data)))
    quotient, remainder = divmod(len(data), 2)
    return int(data[quotient] if remainder else sum(data[quotient - 1:quotient + 1]) / 2)


def check_usage_type(mean: float, median: float):
    """
    Analyzing load pattern and selecting usage_type
    :param mean: mean value
    :param median: median value
    :return: usage_type
    """
    load_pattern = (mean - median) / mean * 100
    if load_pattern < -25:
        return UsageType.DECREASE
    if load_pattern > 25:
        return UsageType.JUMP

    return UsageType.STABLE


def check_intensivity(median: float):
    """
    Analyzing median value and selecting intensivity
    :param median: median value
    :return: intensivity type
    """
    if 0 < median <= 30:
        return IntensivityType.LOW
    if 30 < median <= 60:
        return IntensivityType.MEDIUM
    if 60 < median <= 90:
        return IntensivityType.HIGH

    return IntensivityType.EXTREME


def check_decision(usage_type: str, intensivity: str):
    """
    Analyze usage_type value and intensivity value and selecting decision
    :param usage_type: usage_type value
    :param intensivity: intensivity value
    :return: decision type
    """
    if intensivity == IntensivityType.LOW:
        return DecisionType.DELETE
    if intensivity == IntensivityType.MEDIUM and usage_type == UsageType.DECREASE:
        return DecisionType.DELETE
    if intensivity == IntensivityType.HIGH and usage_type == UsageType.JUMP:
        return DecisionType.EXTEND
    if intensivity == IntensivityType.EXTREME:
        return DecisionType.EXTEND

    return DecisionType.NORMAL


def analyze_metrics(metrics: dict):
    """
    Analyzing metrics to calculate all parameters that needed
    :param metrics: metrics dictionary
    :return: dictionary of metric parameters
    """
    metrics_dictionary = {}
    last_date = None

    for metric_name in ('CPU', 'RAM', 'NetFlow'):

        metric_list = []
        for metric in metrics:
            for name, data in metric.items():
                if name == metric_name:
                    date, value = data.split(',')
                    metric_list.append(value)
                    # Taiga accepts a due_date value only as '%Y-%m-%d' format
                    last_date = date.split(' ')[0]

        mean = calculate_average(metric_list)
        median = calculate_median(metric_list)

        usage_type = check_usage_type(mean, median)
        intensivity = check_intensivity(median)

        decision = check_decision(usage_type, intensivity)

        metrics_dictionary[metric_name] = {
            'mean': mean, 'mediana': median,
            'last_date': last_date, 'usage_type': usage_type,
            'intensivity': intensivity, 'decision': decision
        }

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
