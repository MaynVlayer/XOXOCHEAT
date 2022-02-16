import time

def sleep(ms):
    time.sleep(ms / 1000)
    return ms

def now():
    return time.time() * 1000


def diff(start, end=None):
    if end == None:
        end = now()
    return end - start
