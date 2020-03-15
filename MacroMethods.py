
import time
import functools
import pyautogui as pgui
import ImageModule as ImgM
from Toolset import MemberLoader

# TODO: somehow implement coroutine
# TODO: utilize sys.path.insert?


class _Base:
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
        if self.action():
            # self.onSuccess.run()          <- this might trigger depth limit..?
            if self.onSuccess is None:
                return self.next.run
            else:
                return self.onSuccess.run

        else:
            if self.onFail is None:
                return self.next.run
            else:
                return self.onFail.run

    def action(self):
        return True

    def setArea(self, x1, y1, x2, y2):
        self.screenArea = ImgM.Area(x1, y1, x2, y2)

# --------------------------------------------------------


class _ClickBase:
    # __slots__ = ('target', 'clickCount', 'clickDelay', 'preDelay')

    def __init__(self):
        self.target = ImgM.pos()
        self.clickCount = 0
        self.clickDelay = 0.01
        self.preDelay = 0

    def _click(self, abs_target=ImgM.pos()):
        time.sleep(self.preDelay)

        for i in range(self.clickCount - 1):
            pgui.click(*(self.target + abs_target))
            time.sleep(self.clickDelay)

        pgui.click(*self.target)


class Click(_Base, _ClickBase):
    @property
    def absoluteTarget(self):
        return self.target

    def action(self):
        self._click()


# --------------------------------------------------------
# TODO: find better way to embed loop.


class Loop:
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
    def __init__(self):
        super().__init__()

        self.name = ''
        self.next = None

    def action(self):
        return True


class sLoopEnd(_Base, Loop):
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


# class Goto(Base):
#     def __init__(self):
#         super().__init__()
#         self.gotoOrder = None
#
#     def action(self):
#         pass
#         # loop and goto will be handled by MacroSequencer.py.
#         # this is placeholder.


class Wait(_Base):
    # __slots__ = ('delay', 'actionState')

    def __init__(self):
        super().__init__()
        self.delay = 0
        self.actionState = -2

    def action(self):
        self.actionState = -1

        time.sleep(self.delay)
        self.actionState = 1
        return True


class Variable(_Base):
    def __init__(self):
        super().__init__()
        self.name = 'variable'
        self.value = 0

    # TODO: complete below parts. Will support simple variable calculation with these.
    # TODO: implement variable assign

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


class _Image(_Base):
    # TODO: add weakref for Image, by adding all targets in single dict.
    
    imgSaver = ImgM.saveImg()
    
    def __init__(self):
        super().__init__()

        self.targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.matchPoint = ImgM.pos()
        self.precision = 0.85
        self.offsetMax = 5

    def DumpCaptured(self, name=None):
        self.imgSaver(self.capturedImage, name)
        
    def DumpTarget(self):
        self.imgSaver(self.targetImage, self.targetName)

    def DumpCoordinates(self):      # Do I need this?
        return self.screenArea, self.matchPoint


class ImageSearch(_Image, _ClickBase):

    def __init__(self):
        super(ImageSearch, self).__init__()

        self.loopDelay = 0.2
        self.trials = 5
        self.clickOnMatch = False
        self._foundFlag = False

    def ImageSearch(self):
        self.matchPoint, self.capturedImage = \
            ImgM.imageSearch(self.targetImage, self.screenArea.pygui, self.precision)
        if self.matchPoint[0] == -1:
            self._foundFlag = False

    def ImageSearchMultiple(self):
        for i in range(self.trials):
            self.ImageSearch()
            if self._foundFlag:
                self.actionState = 1
                break

        else:
            self.actionState = 0

    def ImageClick(self):
        pgui.click(ImgM.RandomOffset(self.matchPoint, self.offsetMax))

    def action(self):
        self.actionState = -1

        self.ImageSearchMultiple()
        if self._foundFlag:
            if self.clickOnMatch:
                self.target = self.matchPoint
                self._click()

            self.actionState = 1
            return True
        else:
            self.actionState = 0
            return False


class SearchOccurrence(_Image, _ClickBase):

    def __init__(self):
        super(SearchOccurrence, self).__init__()

        self.matchCount = 0

    def ScanOccurrence(self):
        self.matchCount, self.capturedImage = \
            ImgM.scanOccurrence(self.targetImage, self.screenArea.pygui, self.precision)

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
    pass


def NextSetter(sequence):
    if sequence:
        # This is waste of memory
        for idx, i in enumerate(sequence):
            if idx + 1 < len(sequence):
                i.next = sequence[idx + 1]
            else:
                break


__all__ = MemberLoader.ListClass(__name__, blacklist={'_', 's'})
class_dict = MemberLoader.ListClass(__name__, blacklist={'_', 's'}, return_dict=True)
