from hashlib import md5


def md5_hash(string: str):
    return md5(string.encode('utf-8')).hexdigest()
