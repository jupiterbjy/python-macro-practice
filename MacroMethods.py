from collections import deque
from PIL import Image
import time
import pyautogui
import io
import base64
import copy
import logging

from Toolset import MemberLoader, ImageModule

SLEEP_FUNCTION = time.sleep  # Will be override-d by ui_main.
LOGGER = logging.getLogger()
IMG_SAVER = False
ABORT = False
RAND_OFFSET = False
OFFSET_MAX = 5
DUMP = False


class AbortException(Exception):
    pass


def checkAbort():  # for now call this every action() to implement abort.
    if ABORT:  # inefficient to check if every run.
        raise AbortException


class ExMethodIterator:
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


class ExBase:  # Excluded - Ex
    """
    Defines minimum interfaces that subclasses need to function.
    Override action, reset, serialize and deserialize when necessary.
    """

    variables = dict()

    # https://stackoverflow.com/questions/30849383/
    # meaning-of-the-super-keyword-in-the-parent-class-python

    def __init__(self):
        super(ExBase, self).__init__()  # Refer above link for this call
        self.name = ""
        self.next = None  # Assign next object here when running.
        self.onSuccess = None
        self.onFail = None
        self.screenArea = None

    def setName(self, text):
        self.name = str(text)

    def run(self):
        checkAbort()

        if self.action():

            if self.onSuccess is None:
                return self.next

            return self.onSuccess

        if self.onFail is None:
            return self.next

        return self.onFail

    def action(self):
        return True

    def setArea(self, x1, y1, x2, y2):
        self.screenArea = ImageModule.Area(x1, y1, x2, y2)

    def serialize(self):
        return self.__dict__

    def deserialize(self):
        pass

    def reset(self):
        self.screenArea = None

    def __iter__(self):
        return ExMethodIterator(self)


# --------------------------------------------------------


class _ClickBase:
    """
    Super class for click operation.
    Separated from click object to prevent diamond inherit.
    """

    def __init__(self):
        super(_ClickBase, self).__init__()
        self.target = ImageModule.Pos()
        self.clickCount = 1
        self.clickDelay = 0.01
        self.randomOffset = 0

    def finalPos(self, target=None):
        if target is None:
            target = self.target

        if self.randomOffset:
            out = ImageModule.RandomOffset(target, self.randomOffset)

        else:
            out = target

        return out()

    def _click(self, target=None):

        for i in range(self.clickCount):
            checkAbort()
            SLEEP_FUNCTION(self.clickDelay)
            pyautogui.click(self.finalPos(target))
            print(f"Click: {self.finalPos(target)}")


class Click(ExBase, _ClickBase):
    """
    Interface of Simple Click method.
    """

    def __init__(self):
        super().__init__()

    @property
    def absPos(self):
        return self.screenArea.p1 + self.target

    def action(self):
        self._click(self.absPos)
        return True

    def serialize(self):
        self.target = self.target()
        return self.__dict__

    def deserialize(self):
        self.target = ImageModule.Pos(*self.target)


class Loop:
    """
    Interface. Internally generate loopStart, LoopEnd.
    LoopEnd set next to
    """

    def __init__(self):
        super(Loop, self).__init__()
        self.loopName = ""
        self.loopTime = 3
        self.currentLoop = 0

    @staticmethod
    def generate(name, loops):

        start, end = ExLoopStart(), ExLoopEnd()

        start.next = end
        end.onSuccess = start

        for i in (start, end):
            i.name = name
            i.loopTime = loops

        return start, end


class ExLoopStart(ExBase, Loop):
    """
    Placeholder for Loop. No special functionality is needed for loop start.
    Not for standalone usage.
    """

    def __init__(self):
        super().__init__()

        self.name = ""
        self.next = None

    def action(self):
        return True


class ExLoopEnd(ExBase, Loop):
    """
    Implements Loop via setting next/onSuccess to LoopStart Object.
    Not for standalone usage.
    """

    def __init__(self):
        super().__init__()

        self.name = ""
        self.next = None
        # self.onFail = None
        # self.onSuccess = None
        # Will override onSuccess for loop, onFail for loop end.

    def action(self):
        return self.currentLoop < self.loopTime


class Wait(ExBase):
    """
    Using Asynchronous sleep for Qt.
    but will default to normal time.sleep in case this is used on CLI.
    """

    def __init__(self):
        super().__init__()
        self.delay = 0

    def action(self):
        SLEEP_FUNCTION(self.delay)
        return True


class Variable(ExBase):
    """
    Class that trying to mimic what makes fRep different from plain macros.
    Creating Same-name Variable will overwrite existing variable.
    """

    _created_instances = 0
    _deleted_instances = 0

    def __init__(self):
        super().__init__()
        Variable._created_instances += 1
        self.name = "variable-" + str(type(self)._created_instances)
        self.value = 0

    def __del__(self):
        # Variable._deleted_instances += 1
        ExBase.variables.pop(self.name, None)

    def setValue(self, text):

        try:
            value = int(text)
        except ValueError:
            print("int failed, Passing to float")
            pass
        else:
            self.value = value
            return

        try:
            value = float(text)
        except ValueError:
            raise AttributeError("String is not convertible.")
        else:
            self.value = value

    def action(self):
        if self.name in ExBase.variables.keys():
            self.name = self.name + str(self._created_instances)

        ExBase.variables[self.name] = self.value
        return True


class _Image(ExBase):
    """
    superclass of all Macro classes dealing with image.
    """

    def __init__(self):
        super().__init__()

        self._targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.matchPoint = None  # expects pos object
        self.precision = 0.85

    def DumpCaptured(self, name=None):
        IMG_SAVER(self.capturedImage, str(name))

    def DumpTarget(self):
        IMG_SAVER(self.targetImage, self.targetName)

    def DumpCoordinates(self):  # Do I need this?
        return self.screenArea, self.matchPoint

    @property  # not sure if this use-case is for class method.
    def targetImage(self):
        return self._targetImage

    @targetImage.setter
    def targetImage(self, img):
        try:
            img.convert("RGB")

        except AttributeError:
            raise AttributeError("Onl PIL-type images are supported.")

        else:
            if img.format != "PNG":  # Non-png images has trouble with cv2 conversion

                byte_io = io.BytesIO()
                img.save(byte_io, "PNG")
                self._targetImage = Image.open(byte_io)

            else:
                self._targetImage = img

    def serialize(self):
        try:
            self.target = self.target()
        except AttributeError:
            pass

        buffer = io.BytesIO()
        self._targetImage.save(buffer, format="PNG")
        string = base64.b64encode(buffer.getvalue())
        self._targetImage = string.decode("utf-8")
        buffer.close()

        return self.__dict__

    def deserialize(self):
        try:
            self.target = ImageModule.Pos(*self.target)
        except AttributeError:
            pass
        except TypeError:
            print("Old value found, save file again for update.")
            if isinstance(self.target, dict):
                self.target = ImageModule.Pos(self.target["x"], self.target["y"])
            else:
                raise Exception("File is damaged.")

        buffer = io.BytesIO()
        string = self._targetImage

        buffer.write(base64.b64decode(string))
        self._targetImage = Image.open(buffer, "r").copy()
        buffer.close()

    def reset(self):
        self.screenArea = None
        self.capturedImage = None
        self.matchPoint = None


class ImageSearch(_Image, _ClickBase):
    """
    Find Image on given screen area.
    Can decide whether to click or not, or how much trials before fail.
    """

    def __init__(self):

        super().__init__()
        self.loopDelay = 0.2
        self.trials = 5

    def ImageSearch(self):
        self.matchPoint, self.capturedImage = ImageModule.imageSearch(
            self.targetImage, self.screenArea.region, self.precision
        )

    def ImageSearchMultiple(self):
        for i in range(self.trials):
            self.ImageSearch()
            if self.matchPoint:
                break

            SLEEP_FUNCTION(self.loopDelay)

        if DUMP:
            self.DumpCaptured(bool(self.matchPoint))

    @property
    def ImageCenter(self):
        w, h = self.targetImage.size
        return self.matchPoint + ImageModule.Pos(w // 2, h // 2)

    @property
    def absPos(self):
        return self.screenArea.p1 + self.target

    def action(self):
        self.ImageSearchMultiple()

        if self.matchPoint:
            self.target.set(*self.ImageCenter)
            self._click(self.absPos)

        return bool(self.matchPoint)

    def reset(self):
        self.screenArea = None
        self.target = ImageModule.Pos()
        self.capturedImage = None


class SearchOccurrence(_Image, _ClickBase):
    """
    Counts occurrences of target image.
    Not solid about what then I should do.
    Expecting variable assign or clicking each occurrences.
    """

    def __init__(self):

        super().__init__()
        self.matchPoints = []
        self.matchCount = 0
        self.threshold = 0

    def ScanOccurrence(self):
        (
            self.matchCount,
            self.capturedImage,
            self.matchPoints,
        ) = ImageModule.scanOccurrence(
            self.targetImage, self.screenArea.region, self.precision, self.threshold
        )

        if DUMP:
            self.DumpCaptured(bool(self.matchCount))

    @property
    def ImageCenter(self):
        w, h = self.targetImage.size
        return self.matchPoint + ImageModule.Pos(w // 2, h // 2)

    @property
    def absPos(self):
        return self.screenArea.p1 + self.target

    def action(self):
        self.ScanOccurrence()
        if state := self.matchCount > 0:
            for p in self.matchPoints:
                self.matchPoint = p
                self.target.set(*self.ImageCenter)
                self._click(self.absPos)

        return state

    def reset(self):
        self.screenArea = None
        self.matchCount = 0
        self.matchPoints = []
        self.capturedImage = None


class Drag(ExBase):
    """
    Drag from p1 to p2.
    """

    def __init__(self):
        super().__init__()

        self.p1 = ImageModule.Pos()
        self.p2 = ImageModule.Pos()

    @property
    def From(self):
        return self.p1 + self.screenArea.p1

    @property
    def To(self):
        return self.p2 + self.screenArea.p1

    def set(self, x1, y1, x2, y2):
        self.p1.set(x1, y1)
        self.p2.set(x2, y2)

    def action(self):
        pyautogui.moveTo(*self.From)
        pyautogui.dragTo(*self.To, button="left")
        return True

    def serialize(self):
        self.p1 = self.p1()
        self.p2 = self.p2()
        return self.__dict__

    def deserialize(self):
        self.p1 = ImageModule.Pos(*self.p1)
        self.p2 = ImageModule.Pos(*self.p2)


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


def Serializer(obj_list):
    """
    Manage serialization of objects and return serialized string.
    No serialization other than pickle works with object references.
    Therefore, I'm adding reference_list to map references of each objects.
    """
    obj_type = []
    out = []
    reference_list = [[] for _ in range(len(obj_list))]

    for idx, element in enumerate(obj_list):
        element.next = None
        obj_type.append(type(element).__name__)

        try:
            index = obj_list.index(element.onSuccess)
        except ValueError:
            reference_list[idx].append(None)
        else:
            reference_list[idx].append(index)

        try:
            index = obj_list.index(element.onFail)
        except ValueError:
            reference_list[idx].append(None)
        else:
            reference_list[idx].append(index)

        element.onFail = None
        element.onSuccess = None

        out.append(copy.deepcopy(element.serialize()))

    return {"type": obj_type, "data": out, "reference": reference_list}


def Deserializer(baked):
    """
    Deserialize given json-serialized file.
    error handling should happen outside of this function, where it is called.
    """
    out = []
    inject = deque(baked["data"])
    ref = baked["reference"]
    type_list = baked["type"]

    for obj in type_list:
        obj = class_dict[obj]()
        dict_source = inject.popleft()
        obj.__dict__.update(
            (k, dict_source[k]) for k in dict_source.keys() & obj.__dict__.keys()
        )
        out.append(obj)

    for obj in out:
        success_idx, fail_idx = ref.pop(0)

        try:
            obj.onSuccess = out[success_idx]
        except TypeError:
            obj.onSuccess = None

        try:
            obj.onFail = out[fail_idx]
        except TypeError:
            obj.onFail = None

        obj.deserialize()

    return out


blacklist = {"_", "Ex", "Abort", "deque"}
__all__ = MemberLoader.ListClass(__name__, blacklist=blacklist)
class_dict = MemberLoader.ListClass(__name__, blacklist=blacklist, return_dict=True)
