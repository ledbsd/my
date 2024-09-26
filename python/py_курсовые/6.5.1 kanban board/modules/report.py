"""Working with CSV-files"""
import csv


def save_metric_report(analytic_dictionary: dict, filename: str):
    """
    Save metrics report to CSV-file
    :param analytic_dictionary: dictionary
    :param filename: report filename
    """
    column_names = [
        'Team', 'Resource', 'Dimension', 'mean', 'mediana',
        'last_date', 'usage_type', 'intensivity', 'decision'
    ]
    with open(filename, 'w', newline='', encoding="cp1252") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)

        for team_name, resource_id in analytic_dictionary.items():
            for resource, metrics in resource_id.items():
                for metric_name, metric_data in metrics.items():
                    data = [
                        team_name, resource, metric_name, str(metric_data['mean']),
                        str(metric_data['mediana']), metric_data['last_date'],
                        metric_data['usage_type'], metric_data['intensivity'],
                        metric_data['decision']
                    ]
                    writer.writerow(data)


def save_charge_report(charge_dictionary: dict, filename: str):
    """
    Save charge report to CSV-file
    :param charge_dictionary: dictionary
    :param filename: report filename
    """
    column_names = ['Resource ID', 'Summary cost']
    with open(filename, 'w', newline='', encoding="cp1252") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)

        for resource, cost in charge_dictionary.items():
            writer.writerow([resource, cost])


def save_economy_report(economy_dictionary: dict, filename: str):
    """
    Save charge report to CSV-file
    :param economy_dictionary: dictionary
    :param filename: report filename
    """
    column_names = ['Delete resource ID', 'Dimension', 'Economy cost']
    with open(filename, 'w', newline='', encoding="cp1252") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)

        for resource, data in economy_dictionary.items():
            for metric_name, metric_cost in data.items():
                writer.writerow([resource, metric_name, metric_cost])
