import logging
from threading import Event
from Macro import Imaging


class EnvVariables:
    """
    Pass this to base class.
    """
    file = __file__

    def __init__(self):
        self.logger = logging.getLogger()
        self.img_saver = Imaging.asc_save(self.file)
        self.dump = False
        self.event = Event()
        self.screen_area = Imaging.Area()

    def check_event(self):
        if self.event.is_set():
            raise AbortException


class AbortException(Exception):
    pass


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


def stoppable_sleep(time: float, event: Event):
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
