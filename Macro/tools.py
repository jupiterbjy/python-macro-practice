import time
import logging
from Toolset import ImageModule


SLEEP_FUNCTION = time.sleep  # Will be override by ui_main.
LOGGER = logging.getLogger()
IMG_SAVER = ImageModule.saveImg(__file__)
ABORT = False
DUMP = False


class AbortException(Exception):
    pass


def checkAbort():  # for now call this every action() to implement abort.
    if ABORT:  # inefficient to check if every run.
        raise AbortException


def setSaver(path):
    global IMG_SAVER
    IMG_SAVER = ImageModule.saveImg(path)


class MethodIterator:
    def __init__(self, head):
        self.method = head

    def __iter__(self):
        return self

    def __next__(self):
        if self.method is None:
            raise StopIteration
        else:
            current = self.method
            self.method = self.method.next
            return current
