"""Module of used classes"""
from dataclasses import dataclass
from enum import Enum
from prometheus_client import CollectorRegistry


class Flag(Enum):
    """Class of flag values"""
    OK = 0
    ERROR = 1


@dataclass
class Metric:
    """Class of metric fields"""
    name: str
    description: str
    labels: list
    filepath: str
    data: dict
    registry: CollectorRegistry
