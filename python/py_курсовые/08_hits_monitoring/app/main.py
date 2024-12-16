#!/usr/bin/python3
"""Parsing log file and save metrics to prometheus formated file"""
import os
from datetime import date
from logging import getLogger, basicConfig, DEBUG
from prometheus_client import CollectorRegistry, Gauge, write_to_textfile

from modules.parser import read_large_file, line_parser
from modules.classes import Metric, Flag

POD_NAME = '{{ pod }}'
ACCESS_LOG_PATH = '/opt/vmware/vcloud-director/logs'
LOG_FILE = '/var/log/HitsMonitoring.log'

NODE_EXPORTER_DIR = '/var/lib/node_exporter'
PROM_FILE_IP_HITS = 'ip_hits.prom'
PROM_FILE_UA_HITS = 'ua_hits.prom'
PROM_FILE_HEARTBEAT = 'heartbeat_hits.prom'
PROM_FILE_ERROR = 'error_hits.prom'

FORMAT = "%(asctime)s - %(levelname)s - %(processName)s: %(lineno)d - %(message)s"
logger = getLogger()
basicConfig(filename=LOG_FILE, format=FORMAT, level=DEBUG)


def get_hits(filepath):
    """Creating dicts of IP and UA hits"""
    ip_hits = {}
    agent_hits = {}
    error_count = 0

    for line in read_large_file(filepath):
        log_parts = line_parser(line)

        if log_parts:
            host = log_parts["host"]
            agent = log_parts["agent"][:120]

            ip_hits[host] = ip_hits.setdefault(f'{host}', 0) + 1
            agent_hits[agent] = agent_hits.setdefault(f'{agent}', 0) + 1
        else:
            error_count += 1

    return ip_hits, agent_hits, error_count


def write_prom_file(metric: Metric):
    """Saving metrics to prometheus formated file"""
    g = Gauge(
        name=metric.name,
        documentation=metric.description,
        labelnames=metric.labels,
        registry=metric.registry
    )
    for key in metric.data:
        g.labels(key, POD_NAME).set(metric.data[key])
        write_to_textfile(metric.filepath, metric.registry)


def main():
    """Main program"""
    today = date.today().strftime('%Y_%m_%d')
    access_log = f'{ACCESS_LOG_PATH}/{today}.request.log'
    heartbeat_flag = Flag.OK.value

    if os.path.exists(access_log):

        ip_hits, agent_hits, error_count = get_hits(access_log)

        ip_metric = Metric(
            name='vmware_vcd_ip_hits',
            description='IP-address hits',
            labels=['ipaddress', 'pod'],
            filepath=os.path.join(NODE_EXPORTER_DIR, PROM_FILE_IP_HITS),
            data=ip_hits,
            registry=CollectorRegistry()
        )

        ua_metric = Metric(
            name='vmware_vcd_uagent_hits',
            description='User-Agent hits',
            labels=['useragent', 'pod'],
            filepath=os.path.join(NODE_EXPORTER_DIR, PROM_FILE_UA_HITS),
            data=agent_hits,
            registry=CollectorRegistry()
        )

        if error_count:
            error_flag = Flag.ERROR.value
        else:
            error_flag = Flag.OK.value

        error_metric = Metric(
            name='vmware_vcd_hits_parser_errors',
            description='Hits monitoring parser error',
            labels=['error_count', 'pod'],
            filepath=os.path.join(NODE_EXPORTER_DIR, PROM_FILE_ERROR),
            data={f'{error_count}': error_flag},
            registry=CollectorRegistry()
        )

        write_prom_file(ip_metric)
        write_prom_file(ua_metric)
        write_prom_file(error_metric)

    else:
        logger.error('%s was not found', access_log)
        heartbeat_flag = Flag.ERROR.value

    heartbeat_metric = Metric(
        name='vmware_vcd_hits_heartbeat',
        description='Hits monitoring heartbeat',
        labels=['heartbeat', 'pod'],
        filepath=os.path.join(NODE_EXPORTER_DIR, PROM_FILE_HEARTBEAT),
        data={'alive': heartbeat_flag},
        registry=CollectorRegistry()
    )

    write_prom_file(heartbeat_metric)


if __name__ == '__main__':
    main()
