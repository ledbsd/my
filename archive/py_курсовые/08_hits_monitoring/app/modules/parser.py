"""Module for parse access logfile"""
import re
from logging import getLogger

from modules.positioning import get_last_position, save_current_position

logger = getLogger(__name__)


def line_parser(line):
    """Parsing line with regex"""
    host = r'(?P<host>.*?)'
    identity = r'(?P<identity>\S+)'
    user = r'(?P<user>\S+)'
    time = r'\[(?P<time>.*?)\]'
    request = r'\"(?P<request>.*?)\"'
    status = r'(?P<status>\d{3})'
    size = r'(?P<size>\S+)'
    ref = r'\"(?P<referer>.*?)\"'
    agent = r'\"(?P<agent>.*?)\"'
    s = r'\s'

    pattern = (host + s + identity + s + user + s + time + s +
               request + s + status + s + size + s + ref + s + agent)
    try:
        parts = re.match(pattern, line)
        return parts.groupdict()
    except Exception as e:
        logger.error('%s: string does not match pattern', e)
        return None


def read_large_file(filepath):
    """Reading log file"""
    position = get_last_position()
    with open(filepath, encoding='utf-8') as file:
        file.seek(position)
        if not file.readline():
            logger.debug('save position was not found, set to 0. filename is %s', filepath)
            file.seek(0)
        yield from file
        current_position = file.tell()
    save_current_position(current_position)
