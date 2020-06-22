from threading import Thread, Event
from copy import deepcopy
import json
from Macro import EVENT, Elements, AbortException, Imaging

# Run only in cli mode, not for gui.


def loadJson(location: str):
    if location is None:
        raise FileNotFoundError('No Such File')

    with open(location) as file:  # not needed in CPython, but else all.
        baked = json.load(file)

    return baked


class MacroCLI:
    def __init__(self):
        self.location = ''
        self.loaded = []
        self.running = []
        self.event = Event()

        self.started = False
        self._area = None

    @property
    def area(self):
        return self._area

    @area.getter
    def area(self, p1, p2):
        self._area = Imaging.Area.fromPos(p1, p2)


    def clear_macro(self):
        self.loaded.clear()

    def load_macro(self):
        self.location = input()
        try:
            loaded = loadJson(self.location)
        except FileNotFoundError:
            print("└ No such file.")
        except UnicodeDecodeError:
            print("└ Unicode decode failed.")
        except json.JSONDecodeError:
            print("└ Failed decoding JSON.")
        else:
            deserialized = Elements.Deserializer(loaded)
            self.loaded = deserialized

    def list_macro(self):
        for i in self.loaded:
            print(i)

    def stop_macro(self):
        self.event.set()

    def run_macro(self):
        self.event = Event()
        self.running = deepcopy(self.loaded)
        thread = Thread(target=self._runThread)
        thread.start()

    def _runThread(self):
        head = self.running[0]
        for element in self.running:  # really tempting to use abc..
            element.run()
