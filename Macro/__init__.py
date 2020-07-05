import logging
from threading import Event
from Macro import Imaging
import keyboard
import pyautogui


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


def get_position(event: Event, kill_key='f2'):
    # block method
    # keyboard.wait(kill_key)

    # non-block
    while not keyboard.is_pressed(kill_key):
        stoppable_sleep(0.05, event)

    while keyboard.is_pressed(kill_key):
        stoppable_sleep(0.05, event)

    return Imaging.Pos(*pyautogui.position())


def get_working_area(event: Event, kill_key='f2'):
    return Imaging.Area.from_pos(get_position(event, kill_key),
                                 get_position(event, kill_key))


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
