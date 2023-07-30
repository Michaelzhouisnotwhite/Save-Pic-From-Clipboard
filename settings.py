import os
import sys
__all__ = ["BASE_DIR", "DEBUG", "CONFIG_FILE", "userpath"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class PlatFormNotSupport(Exception):
    msg = ""

    def __init__(self, msg="") -> None:
        super().__init__(msg)
        self.msg = msg


DEBUG = False
if DEBUG:
    CONFIG_FILE = f'{BASE_DIR}/.save_pic/config.json'
    userpath = BASE_DIR
else:
    from utils import PlatForm
    if PlatForm.get_local() == PlatForm.LINUX:
        userpath = os.getenv("HOME")
    elif PlatForm.get_local() == PlatForm.WINDOWS:
        userpath = os.getenv('USERPROFILE')
    else:
        raise PlatFormNotSupport("Your OS platform not supported")

    CONFIG_FILE = f'{userpath}/.save_pic/config.json'
