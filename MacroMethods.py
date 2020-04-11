
from functools import singledispatch
from collections import deque
import time
import pyautogui
import copy
import io
import base64
from PIL import Image

import ImageModule
from Toolset import MemberLoader

SLEEP_FUNCTION = time.sleep     # Will be override-d by ui_main.
IMG_SAVER = ImageModule.saveImg()
ABORT = False
RAND_OFFSET = False
OFFSET_MAX = 5
DEBUG = False


class AbortException(Exception):
    pass


def checkAbort():  # for now call this every action() to implement abort.
    if ABORT:      # inefficient to check if every run.
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


class _Base:
    """
    Defines minimum interfaces that subclasses need to function.
    Override when necessary.
    """

    def __init__(self):
        super(_Base, self).__init__()
        self.name = ''
        self.next = None           # assign obj to run next.
        self.onSuccess = None
        self.onFail = None
        self.screenArea = ImageModule.Area()

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
        self.screenArea = self.screenArea()
        return self.__dict__

    def deserialize(self):
        self.screenArea = ImageModule.Area(*self.screenArea)

    def reset(self):
        self.screenArea = ImageModule.Area()

    def __iter__(self):
        return ExMethodIterator(self)

# --------------------------------------------------------


class _ClickBase:
    """
    Super class for click operation.
    Separated from click object to prevent diamond inherit.
    """
    def __init__(self):
        self.target = ImageModule.Pos()
        self.clickCount = 1
        self.clickDelay = 0.01
        self.randomOffset = 0

    @staticmethod
    def finalPos(target):
        if RAND_OFFSET:
            return ImageModule.RandomOffset(target, OFFSET_MAX)

        return target

    def _click(self, target):

        for i in range(self.clickCount):
            checkAbort()
            SLEEP_FUNCTION(self.clickDelay)
            pyautogui.click(self.finalPos(target))
            print(f'Click: {self.finalPos(target)}')


class Click(_Base, _ClickBase):
    """
    Interface of Simple Click method.
    """
    @property
    def absPos(self):
        return self.screenArea.p1 + self.target

    def action(self):
        self._click(self.absPos)

    def serialize(self):
        self.screenArea = self.screenArea()
        self.target = self.target()
        return self.__dict__

    def deserialize(self):
        self.screenArea = ImageModule.Area(*self.screenArea)
        self.target = ImageModule.Pos(*self.target)


class Loop:
    """
    Interface. Internally generate loopStart, LoopEnd.
    LoopEnd set next to
    """
    def __init__(self):

        self.loopName = ''
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


class ExLoopStart(_Base, Loop):
    """
    Placeholder for Loop. No special functionality is needed for loop start.
    Not for standalone usage.
    """
    def __init__(self):
        super().__init__()

        self.name = ''
        self.next = None

    def action(self):
        return True


class ExLoopEnd(_Base, Loop):
    """
    Implements Loop via setting next/onSuccess to LoopStart Object.
    Not for standalone usage.
    """
    def __init__(self):
        super().__init__()

        self.name = ''
        self.next = None
        # self.onFail = None
        # self.onSuccess = None
        # Will override onSuccess for loop, onFail for loop end.

    def action(self):
        return self.currentLoop < self.loopTime


class Wait(_Base):
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


class Variable(_Base):
    """
    Class that trying to mimic what makes fRep different from plain macros.
    Will expand to simple add, subtract, multiply, divide, mod operation between variables.
    Not worked yet.
    """
    def __init__(self):
        super().__init__()
        self.name = 'variable'
        self.value = 0

    def __iadd__(self, other):
        self.value = self.value + other.value
        return self

    def __isub__(self, other):
        self.value = self.value - other.value
        return self

    def __imul__(self, other):
        self.value = self.value * other.value
        return self

    def __idiv__(self, other):
        self.value = self.value / other.value
        return self

    def __ifloordiv__(self, other):
        self.value = self.value // other.value
        return self

    def __imod__(self, other):
        self.value = self.value // other.value
        return self

    @singledispatch
    def valueType(self):
        pass

    @valueType.register(int)
    def _(self):
        pass

    @valueType.register(float)
    def _(self):
        pass

    @valueType.register(str)
    def _(self):
        pass

    def action(self):
        pass


class _Image(_Base):
    """
    superclass of all Macro classes dealing with image.
    """
    
    def __init__(self):
        super().__init__()

        self._targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.matchPoint = None      # expects pos object
        self.precision = 0.85

    def DumpCaptured(self, name=None):
        IMG_SAVER(self.capturedImage, str(name))

    def DumpTarget(self):
        IMG_SAVER(self.targetImage, self.targetName)

    def DumpCoordinates(self):      # Do I need this?
        return self.screenArea, self.matchPoint

    @property           # not sure if this use-case is for class method.
    def targetImage(self):
        return self._targetImage

    @targetImage.setter
    def targetImage(self, img):
        try:
            img.convert('RGB')

        except AttributeError:
            raise AttributeError('Onl PIL-type images are supported.')

        else:
            if img.format != 'PNG':     # Non-png images has trouble with cv2 conversion

                byte_io = io.BytesIO()
                img.save(byte_io, 'PNG')
                self._targetImage = Image.open(byte_io)

            else:
                self._targetImage = img

    def serialize(self):
        self.screenArea = self.screenArea()

        buffer = io.BytesIO()
        self._targetImage.save(buffer, format='PNG')
        string = base64.b64encode(buffer.getvalue())
        self._targetImage = string.decode('utf-8')
        buffer.close()

        return self.__dict__

    def deserialize(self):
        self.screenArea = ImageModule.Area(*self.screenArea)

        buffer = io.BytesIO()
        string = self._targetImage

        buffer.write(base64.b64decode(string))
        self._targetImage = Image.open(buffer, 'r').copy()
        buffer.close()

    def reset(self):
        self.capturedImage = None
        self.matchPoint = None


class ImageSearch(_Image, _ClickBase):
    """
    Find Image on given screen area.
    Can decide whether to click or not, or how much trials before fail.
    """

    def __init__(self):
        super(ImageSearch, self).__init__()

        self.loopDelay = 0.2
        self.trials = 5

    def ImageSearch(self):
        self.matchPoint, self.capturedImage = \
            ImageModule.imageSearch(self.targetImage, self.screenArea.region, self.precision)

    def ImageSearchMultiple(self):
        for i in range(self.trials):
            self.ImageSearch()
            if self.matchPoint:
                break

            SLEEP_FUNCTION(self.loopDelay)

        if DEBUG:
            self.DumpCaptured(bool(self.matchPoint))

    @property
    def ImageCenter(self):
        w, h = self.targetImage.size
        return self.matchPoint + ImageModule.Pos(w//2, h//2)

    @property
    def absPos(self):
        return self.screenArea.p1 + self.target

    def action(self):
        self.ImageSearchMultiple()

        if self.matchPoint:
            self.target.set(*self.ImageCenter)
            self._click(self.absPos)

            return True
        return False

    def reset(self):
        self.target = ImageModule.Pos()
        self.capturedImage = None


class SearchOccurrence(_Image, _ClickBase):
    """
    Counts occurrences of target image.
    Not solid about what then I should do.
    Expecting variable assign or clicking each occurrences.
    """

    def __init__(self):
        super(SearchOccurrence, self).__init__()

        self.matchCount = 0

    def ScanOccurrence(self):
        self.matchCount, self.capturedImage = \
            ImageModule.scanOccurrence(self.targetImage, self.screenArea.region, self.precision)

        if DEBUG:
            self.DumpCaptured(bool(self.matchCount))

    def action(self):
        self.ScanOccurrence()
        return self.matchCount > 0

    def reset(self):
        self.matchCount = 0
        self.capturedImage = None


class Drag(_Base):
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
        pyautogui.dragTo(*self.To, button='left')
        return True

    def serialize(self):
        self.screenArea = self.screenArea()
        self.p1 = self.p1()
        self.p2 = self.p2()
        return self.__dict__

    def deserialize(self):
        self.screenArea = ImageModule.Area(*self.screenArea)
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

        out.append(copy.deepcopy(element.serialize()))

    return {'type': obj_type, 'data': out, 'reference': reference_list}


def Deserializer(baked):
    """
    Deserialize given json-serialized file.
    error handling should happen outside of this function, where it is called.
    """
    out = []
    inject = deque(baked['data'])
    ref = baked['reference']
    type_list = baked['type']

    for obj in type_list:
        obj = class_dict[obj]()
        dict_source = inject.popleft()
        obj.__dict__.update((k, dict_source[k]) for k in
                            dict_source.keys() & obj.__dict__.keys())
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


blacklist = {'_', 'Ex', 'Abort', 'deque'}
__all__ = MemberLoader.ListClass(__name__, blacklist=blacklist)
class_dict = MemberLoader.ListClass(__name__, blacklist=blacklist, return_dict=True)
