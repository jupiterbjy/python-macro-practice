
import functools
import time
import pyautogui as pgui
import copy
import io
import base64
from PIL import Image

import ImageModule as ImgM
from Toolset import MemberLoader, Tools

SLEEP_FUNCTION = time.sleep     # Will be override-d by ui_main.
imgSaver = ImgM.saveImg()
ABORT = False
RAND_OFFSET = False
OFFSET_MAX = 5

class AbortException(Exception):
    pass


def checkAbort():  # for now call this every action() to implement abort.
    if ABORT:      # inefficient to check if every run.
        raise AbortException


class _Base:
    """
    Super class for all, success-fail-next is at this level.
    """
    # __slots__ = ('name', 'order')

    def __init__(self):
        super(_Base, self).__init__()
        self.name = ''
        self.next = None           # assign obj to run next.
        self.onSuccess = None
        self.onFail = None
        self.screenArea = ImgM.Area()

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
        self.screenArea = ImgM.Area(x1, y1, x2, y2)

    def serialize(self):
        self.screenArea = self.screenArea()
        return self.__dict__

    def deserialize(self):
        self.screenArea = ImgM.Area(*self.screenArea)


# --------------------------------------------------------


class _ClickBase:
    """
    Super class for click operation.
    Separated from click object to prevent diamond inherit.
    """
    def __init__(self):
        self.target = ImgM.Pos()
        self.clickCount = 1
        self.clickDelay = 0.01

    @staticmethod
    def finalPos(target):
        if RAND_OFFSET:
            return ImgM.RandomOffset(target, OFFSET_MAX)

        return target

    def _click(self, target):

        for i in range(self.clickCount):
            checkAbort()
            SLEEP_FUNCTION(self.clickDelay)
            pgui.click(self.finalPos(target))
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
        self.screenArea = ImgM.Area(*self.screenArea)
        self.target = ImgM.Pos(*self.target)


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

        looper = sLoopStart(), sLoopEnd()

        looper[0].next = looper[1]
        looper[1].onSuccess = looper[0]

        for i in looper:
            i.name = name
            i.loopTime = loops

        return looper


class sLoopStart(_Base, Loop):
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


class sLoopEnd(_Base, Loop):
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

    @functools.singledispatch
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
        self.matchPoint = (0, 0)
        self.precision = 0.85

    def DumpCaptured(self, name=None):
        imgSaver(self.capturedImage, str(name))

    def DumpTarget(self):
        imgSaver(self.targetImage, self.targetName)

    def DumpCoordinates(self):      # Do I need this?
        return self.screenArea, self.matchPoint

    @property           # not sure if this use-case is for class method.
    def targetImage(self):
        return self._targetImage

    @targetImage.setter
    def targetImage(self, img):
        img.convert('RGB')

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
        self.screenArea = ImgM.Area(*self.screenArea)

        buffer = io.BytesIO()
        string = self._targetImage

        buffer.write(base64.b64decode(string))
        self._targetImage = Image.open(buffer, 'r').copy()
        buffer.close()


class ImageSearch(_Image, _ClickBase):
    """
    Find Image on given screen area.
    Can decide whether to click or not, or how much trials before fail.
    """

    def __init__(self):
        super(ImageSearch, self).__init__()

        self.loopDelay = 0.2
        self.trials = 5
        self.clickOnMatch = False
        self._foundFlag = False

    def ImageSearch(self):
        self.matchPoint, self.capturedImage = \
            ImgM.imageSearch(self.targetImage, self.screenArea.region, self.precision)
        if self.matchPoint[0] != -1:
            self._foundFlag = True

    def ImageSearchMultiple(self):
        for i in range(self.trials):
            self.ImageSearch()
            if self._foundFlag:
                break

        self.DumpCaptured(self._foundFlag)

    @property
    def ImageCenter(self):
        w, h = self.targetImage.size
        return self.matchPoint[0] + w//2, self.matchPoint[1] + h//2

    @property
    def absPos(self):
        return self.screenArea.p1 + self.target

    def action(self):
        self.ImageSearchMultiple()

        if self._foundFlag:
            if self.clickOnMatch:
                self.target.set(*self.ImageCenter)
                self._click(self.absPos)

            return True
        return False


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
            ImgM.scanOccurrence(self.targetImage, self.screenArea.region, self.precision)

    def action(self):
        self.ScanOccurrence()
        return self.matchCount > 0


class Drag(_Base):
    """
    Drag from p1 to p2.
    """
    def __init__(self):
        super().__init__()

        self.p1 = ImgM.Pos()
        self.p2 = ImgM.Pos()

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
        pgui.moveTo(*self.From)
        pgui.dragTo(*self.To, button='left')

        return True

    def serialize(self):
        self.screenArea = self.screenArea()
        self.p1 = self.p1()
        self.p2 = self.p2()
        return self.__dict__

    def deserialize(self):
        self.screenArea = ImgM.Area(*self.screenArea)
        self.p1 = ImgM.Pos(*self.p1)
        self.p2 = ImgM.Pos(*self.p2)


def NextSetter(sequence):
    """
    Set next for respective object in sequence.
    Will need special case for loop class.
    :param sequence: List containing macro objects.
    """
    if sequence:
        for idx, i in enumerate(sequence):
            if idx + 1 < len(sequence):
                i.next = sequence[idx + 1]
            else:
                break


# Took way too much time on json serialization...
def Serializer(obj_list):
    """
    Due to reference of next object that stored in each objects,
    No serialization other than pickle works.
    Therefore, I'm adding reference_list to map references of each objects.
    """
    obj_type = []
    out = []
    reference_list = [[] for _ in range(len(obj_list))]

    for idx, element in enumerate(obj_list):
        element.next = None
        obj_type.append(type(element).__name__)

        if element.onSuccess is not None:
            index = Tools.listFindInstance(element.onSuccess, obj_list)
            reference_list[idx].append(index)
            element.onSuccess = None

        else:
            reference_list[idx].append(None)

        if element.onFail is not None:
            index = Tools.listFindInstance(element.onFail, obj_list)
            reference_list[idx].append(index)
            element.onFail = None

        else:
            reference_list[idx].append(None)

    for obj in obj_list:
        out.append(copy.deepcopy(obj).serialize())

    output = {'type': obj_type, 'data': out, 'reference': reference_list}

    return output


def Deserializer(baked):
    out = []

    inject = baked['data']
    ref = baked['reference']
    type_list = baked['type']

    for obj in type_list:
        obj = class_dict[obj]()
        obj.__dict__ = inject.pop(0)
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


__all__ = MemberLoader.ListClass(__name__, blacklist={'_', 's', 'Abort'})
class_dict = MemberLoader.ListClass(__name__, blacklist={'_', 's', 'Abort'}, return_dict=True)
