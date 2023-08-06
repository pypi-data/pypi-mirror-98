import hashlib


def md5(str, charset='UTF-8'):
    m = hashlib.md5()
    m.update(str.encode(encoding=charset))
    return m.hexdigest()
