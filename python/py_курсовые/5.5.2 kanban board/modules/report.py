import csv


def save_report(analytic_dictionary: dict, filename: str):
    """
    Save report to CSV-file
    :param analytic_dictionary: dictionary
    :param filename: report filename
    """
    column_names = ['Team', 'Resource', 'Dimension', 'mean', 'mediana', 'last_date', 'usage_type', 'intensivity', 'decision']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)

        for team_name, resource_id in analytic_dictionary.items():
            for resource, metrics in resource_id.items():
                for metric_name, metric_data in metrics.items():
                    data = [team_name, resource, metric_name, str(metric_data['mean']), str(metric_data['mediana']),
                            metric_data['last_date'], metric_data['usage_type'], metric_data['intensivity'],
                            metric_data['decision']]
                    writer.writerow(data)


def print_report(filename: str):
    """
    Reading report file and printing to the screen
    :param filename: report filename
    """
    with open(filename, 'r') as csvfile:
        print(csvfile.readlines())
