"""Parsing the billing data"""
from modules.parser import DecisionType
import yaml


def analyze_billing_data(analytic: dict, billing_data: str):
    """
    Analyze billing data
    :return: two dictionaries: charge and economy information
    """
    resources = yaml.safe_load(billing_data)['values']

    # list of tuples ([(delete_id: delete_metric), ...])
    resource_to_delete = []

    for _, resource_id in analytic.items():
        for resource, metrics in resource_id.items():
            for metric_name, metric_data in metrics.items():
                if metric_data['decision'] == DecisionType.DELETE:
                    # list of tuples ([(id: metric), (id: metric), ...])
                    resource_to_delete.append((resource, metric_name))

    charge_dictionary = {}
    economy_dictionary = {}

    for resource, cost_data in resources.items():
        summary_resource_cost = 0
        economy_metric_dictionary = {}
        for metric_name, metric_cost in cost_data.items():
            summary_resource_cost += int(metric_cost)
            for delete_name, delete_metric in resource_to_delete:
                if resource == delete_name and metric_name == delete_metric:
                    economy_metric_dictionary[metric_name] = int(metric_cost)
        if len(economy_metric_dictionary) != 0:
            economy_dictionary[resource] = economy_metric_dictionary
        charge_dictionary[resource] = summary_resource_cost

    return charge_dictionary, economy_dictionary
