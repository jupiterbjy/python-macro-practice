
import functools
import time
import pyautogui as pgui
from PIL import Image

import ImageModule as ImgM
from Toolset import MemberLoader

SLEEP_FUNCTION = time.sleep     # Will be override-d by ui_main.
imgSaver = ImgM.saveImg()
ABORT = False


def abort():
    global ABORT
    ABORT = True


def CLEAR():
    global ABORT
    ABORT = False


def checkAbort():  # for now call this every action() to implement abort.
    if ABORT:      # inefficient to check if every run.
        raise Exception('Abort Signaled.')


class _Base:
    """
    Super class for all, success-fail-next is at this level.
    """
    # __slots__ = ('name', 'order')

    def __init__(self):
        super(_Base, self).__init__()
        self.name = ''
        self.next = None           # assign obj to run next.
        self.actionState = -2      # -2: standby / -1: active / 0: fail / 1: Success
        self.onSuccess = None
        self.onFail = None
        self.screenArea = ImgM.Area()

    def run(self):

        checkAbort()

        if self.action():
            # self.onSuccess.run()          <- this might trigger stack limit..?
            if self.onSuccess is None:
                return self.next
            else:
                return self.onSuccess

        else:
            if self.onFail is None:
                return self.next
            else:
                return self.onFail

    def action(self):
        return True

    def setArea(self, x1, y1, x2, y2):
        self.screenArea = ImgM.Area(x1, y1, x2, y2)

# --------------------------------------------------------


class _ClickBase:
    """
    Super class for click operation.
    Separated from click object to prevent diamond inherit.
    """
    # __slots__ = ('target', 'clickCount', 'clickDelay', 'preDelay')

    def __init__(self):
        self.target = ImgM.Pos()
        self.clickCount = 0
        self.clickDelay = 0.01

    def _click(self, abs_target=ImgM.Pos()):
        p = self.target + abs_target

        for i in range(self.clickCount):
            checkAbort()
            SLEEP_FUNCTION(self.clickDelay)
            pgui.click(p)
            print(f'Click: {p}')


class Click(_Base, _ClickBase):
    """
    Interface of Simple Click method.
    I barely used click on frep too, so I'm not putting empathise on this for now.
    """
    @property
    def absoluteTarget(self):
        return self.target

    def action(self):
        self._click()


# --------------------------------------------------------
# TODO: find better way to embed loop.


class Loop:
    """
    Interface. Internally generate loopStart, LoopEnd.
    LoopEnd set next to
    """
    # __slots__ = ('loopTime', 'endOrder', 'currentLoop', 'startOrder', 'loopName')

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
        if self.currentLoop < self.loopTime:
            return True
        else:
            return False

# --------------------------------------------------------


class Wait(_Base):
    """
    Simple waiting Macro Class.
    Using Asynchronous sleep for Qt - using SLEEP_FUNCTION for now,
    but will support normal time.sleep in case this is used on CLI.
    """
    # __slots__ = ('delay', 'actionState')

    def __init__(self):
        super().__init__()
        self.delay = 0
        self.actionState = -2

    def action(self):

        self.actionState = -1
        SLEEP_FUNCTION(self.delay)
        self.actionState = 1

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

    # TODO: complete below parts. Will support simple variable calculation with these.
    # TODO: implement variable assign

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
        self.matchPoint = ImgM.Pos()
        self.precision = 0.85
        self.offsetMax = 5

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
            from io import BytesIO

            byte_io = BytesIO()
            img.save(byte_io, 'PNG')
            self._targetImage = Image.open(byte_io)

        else:
            self._targetImage = img


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
                self.actionState = 1
                break

        else:
            self.actionState = 0

        self.DumpCaptured(self._foundFlag)

    def ImageClick(self):
        pgui.click(ImgM.RandomOffset(self.matchPoint, self.offsetMax))

    @property
    def ImageCenter(self):
        w, h = self.targetImage.size

        return self.matchPoint[0] + w//2, self.matchPoint[1] + h//2

    def action(self):
        self.actionState = -1

        self.ImageSearchMultiple()

        if self._foundFlag:
            if self.clickOnMatch:
                self.target.set(*self.ImageCenter)
                self._click(self.screenArea.p1)

            self.actionState = 1
            return True
        else:
            self.actionState = 0
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
        self.actionState = -1
        self.ScanOccurrence()

        if self.matchCount > 0:
            self.actionState = 1
            return True
        else:
            self.actionState = 0
            return False


class sActions(Wait, Variable, Click, SearchOccurrence, ImageSearch, Loop):
    """
    Unused yet. Only exists to display clean on UML diagram.
    """
    pass


def NextSetter(sequence):
    """
    Set next for respective object in sequence.
    Will need special case for loop class.
    :param sequence: List containing macro objects.
    """
    if sequence:
        # This is waste of memory
        for idx, i in enumerate(sequence):
            if idx + 1 < len(sequence):
                i.next = sequence[idx + 1]
            else:
                break


__all__ = MemberLoader.ListClass(__name__, blacklist={'_', 's'})
class_dict = MemberLoader.ListClass(__name__, blacklist={'_', 's'}, return_dict=True)
