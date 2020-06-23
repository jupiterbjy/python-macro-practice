from threading import Thread, Event
from copy import deepcopy
import json
import queue
from Macro import EVENT, AbortException, Imaging, SetNext, Elements

# Run only in cli mode, not for gui.
# Will refactor UI to CLI once complete.


def loadJson(location: str):
    if location is None:
        raise FileNotFoundError('No Such File')

    with open(location) as file:  # not needed in CPython, but else all.
        baked = json.load(file)

    return baked


class MacroCLI:
    def __init__(self):
        self.loaded = []
        self.event = Event()

        self.started = False
        self._area = None
        self.thread_quene = queue.SimpleQueue()

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, *args):
        self._area = Imaging.Area.fromPos(*args)

    def clear_macro(self):
        self.loaded.clear()

    def load_macro(self, location=None):
        if location is None:
            location = input()

        try:
            loaded = loadJson(location)
        except FileNotFoundError:
            print("└ No such file.")
        except UnicodeDecodeError:
            print("└ Unicode decode failed.")
        except json.JSONDecodeError:
            print("└ Failed decoding JSON.")
        else:
            deserialized = Elements.Deserializer(loaded)
            self.loaded = deserialized

    def list_macro(self, verbose=False):
        if verbose:
            for i in self.loaded:
                print(i)
        else:
            for i in self.loaded:
                print(i.name)

    def stop_macro(self):
        self.event.set()

    def run_macro(self):
        self.event = Event()
        running = deepcopy(self.loaded)
        SetNext(running)
        thread = Thread(target=self._runThread, args=[running])
        thread.start()

    @staticmethod
    def _runThread(seq):
        head = seq[0]
        for element in seq:  # really tempting to use abc..
            element.run()
