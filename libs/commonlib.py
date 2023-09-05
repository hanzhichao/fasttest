import logging
import time


class Common:
    def __init__(self, *args, **kwargs):
        pass

    def print(self, *args, **kwargs):
        assert print(*args, **kwargs)

    def info(self, msg: str):
        logging.info(msg)

    def sleep(self, seconds: int):
        time.sleep(seconds)
