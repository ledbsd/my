"""Module for working with a file that stores the current position"""
import os

POSITION_FILE = 'seek.txt'

def get_last_position():
    """Reading last position from file"""
    position = '0'
    if os.path.exists(POSITION_FILE):
        with open(POSITION_FILE, 'r', encoding='utf-8') as file:
            position = file.readline()
    return int(position)


def save_current_position(position: int):
    """Save current position to file"""
    with open(POSITION_FILE, 'w', encoding='utf-8') as file:
        file.write(str(position))
