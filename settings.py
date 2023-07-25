import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False
if DEBUG:
    CONFIG_FILE = f'{BASE_DIR}/.save_pic/config.json'
else:
    from utils import PlatForm
    if PlatForm.get_local() == PlatForm.LINUX:
        userpath = os.getenv("HOME")
    elif PlatForm.get_local() == PlatForm.WINDOWS:
        userpath = os.getenv('USERPROFILE')
        
    CONFIG_FILE = f'{userpath}/.save_pic/config.json'
