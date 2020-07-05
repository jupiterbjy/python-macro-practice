from threading import Thread, Event
from copy import copy
import json
import queue
from Macro import SetNext, Elements, Bases, get_working_area

# Run only in cli mode, not for gui.
# Will refactor UI to CLI once complete.

test_loc = 'Sequence_Sample/discoveryI.json'


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
        self.area = None
        self.kill_key = 'f2'

        self.thread_queue = queue.SimpleQueue()
        self.base = Bases.Base.env_var
        self.base.event = self.event

    def clear_macro(self):
        self.loaded.clear()

    def set_env_variable(self):
        area = get_working_area(self.event, self.kill_key)
        self.base.screen_area = area

    def load_macro(self, location=None):
        self.clear_macro()

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
            # maybe I need to wrap this with another try-except
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
        if not self.loaded:
            print("[W] No macros loaded.")
            return

        self.set_env_variable()

        running = copy(self.loaded)
        SetNext(running)
        thread = Thread(target=self._runThread, args=[running])
        thread.start()

    @staticmethod
    def _runThread(seq):
        head = seq[0]
        for element in head:
            element.run()
