import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False
userpath = os.getenv('USERPROFILE')
CONFIG_FILE = f'{userpath}/.save_pic/config.json'
