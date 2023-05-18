import os
from contextlib import ContextDecorator
from traceback import format_tb
import datetime

class exceptlogger(ContextDecorator):
    DEFAULT_FLENAME = 'weather.errors.log'
    label: str
    logpath: str

    def __init__(self, label = None, logpath = os.path.join(os.path.curdir, DEFAULT_FLENAME)):
        self.label = label
        self.logpath = logpath

    def __call__(self, func):
        if self.label is None:
            self.label = func.__name__
        return super().__call__(func)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type, exc_value, traceback):
        if exc_type:
            with open(self.logpath, '+a') as file:
                file.write(';'.join(map(str, [
                    datetime.datetime.now(),
                    self.label,
                    exc_type.__name__,
                    exc_value, format_tb(traceback)
                ])) + '\n')
        return False
