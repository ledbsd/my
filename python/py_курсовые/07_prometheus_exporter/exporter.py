""" Prometheus exporter
    Getting metric from monitoring script
    (monitoring_module.py)
    Metrics are available at http://localhost:5000/metrics
"""
import time
import threading
from flask import Flask, Response
from prometheus_client.core import REGISTRY, HistogramMetricFamily
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import monitoring
import metric_parser

app = Flask(__name__)


class CustomMetricExporter:
    """Class for returned metric"""
    stored_load = {}
    BUCKETS = {
        "10": 0,
        "20": 0,
        "30": 0,
        "40": 0,
        "50": 0,
        "60": 0,
        "70": 0,
        "80": 0,
        "90": 0,
        "100": 0
    }

    def collect(self):
        """The method used by prometheus to get the metric"""
        load = HistogramMetricFamily(
            "resource_percent_load",
            "Load of resources in %",
            labels=["command", "resource", "resource_type"]
        )

        for labels, storage in self.stored_load.items():
            command, resource, resource_type = labels.split(',')
            load.add_metric(
                [command, resource, resource_type],
                list(storage["buckets"].items()),
                storage["sum"]
            )
        yield load


REGISTRY.register(CustomMetricExporter())


@app.route("/metrics")
def metrics():
    """Return metric in prometheus standard"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


def get_data():
    """Getting metric from monitoring script"""
    while True:
        mon_server = monitoring.MonitoringServer()
        team_data = mon_server.metric_data

        if team_data:
            analytic_dictionary = metric_parser.get_analytic_dictionary(team_data)
            for command, resources in analytic_dictionary.items():
                for resource, resource_types in resources.items():
                    for resource_type, values in resource_types.items():
                        for value in values:
                            build_histogram(f'{command},{resource},{resource_type}', int(value))
        time.sleep(10)


def build_histogram(labels, value):
    """Creating histogram"""
    load_storage = CustomMetricExporter.stored_load.setdefault(labels, {})
    bucket_storage = load_storage.setdefault("buckets", CustomMetricExporter.BUCKETS.copy())
    for bucket in bucket_storage.keys():
        if value < int(bucket):
            bucket_storage[bucket] += 1

    load_storage["sum"] = load_storage.get("sum", 0) + value


if __name__ == '__main__':
    thread = threading.Thread(target=get_data)
    thread.start()
    app.run()
