from hashlib import md5
import platform
from enum import Enum
import enum


class PlatForm(Enum):
    LINUX = enum.auto()
    WINDOWS = enum.auto()

    @staticmethod
    def get_local():
        class PlatformError(Exception):
            ...

        if platform.system().lower() == 'windows':
            return PlatForm.WINDOWS
        elif platform.system().lower() == 'linux':
            return PlatForm.LINUX
        raise PlatformError("Unsupported platform")


def md5_hash(string: str):
    return md5(string.encode('utf-8')).hexdigest()
