import logging
from threading import Event
from Macro import Imaging


LOGGER = logging.getLogger()
IMG_SAVER = Imaging.saveImg(__file__)
DUMP = False
EVENT = Event()


def check_event():
    if EVENT.is_set():
        raise AbortException


class AbortException(Exception):
    pass


def setSaver(path):
    global IMG_SAVER
    IMG_SAVER = Imaging.saveImg(path)


class MethodIterator:
    def __init__(self, head):
        self.method = head

    def __iter__(self):
        return self

    def __next__(self):
        if self.method is None:
            raise StopIteration

        current = self.method
        self.method = self.method.next
        return current


def stoppable_sleep(time: float, event=EVENT):
    if event.wait(time):  # return True immediately when set().
        event.clear()
        raise AbortException  # Eject!


def SetNext(sequence):
    """
    Set next for respective object in sequence.
    Will need special case for loop class.
    :param sequence: List containing macro objects.
    """
    if sequence:
        for idx, i in enumerate(sequence):
            try:
                i.next = sequence[idx + 1]
            except IndexError:
                break

