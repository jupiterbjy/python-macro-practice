import time
import functools
# import weakref
import pyautogui as pgui
# import shutil
import ImageModule as ImgM
from Toolset import MemberLoader

# TODO: somehow implement coroutine
# TODO: utilize sys.path.insert?
# TODO: pickle serialize class? Will use simple txt-based for now.


class _Base:
    # __slots__ = ('name', 'order')

    def __init__(self):
        super(_Base, self).__init__()
        self.name = ''
        self.next = None           # assign obj to run next.
        self.actionState = -2      # -2: standby / -1: active / 0: fail / 1: Success
        self.onSuccess = None
        self.onFail = None

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

# --------------------------------------------------------


class _ClickBase:
    # __slots__ = ('target', 'clickCount', 'clickDelay', 'preDelay')

    def __init__(self):
        self.target = ImgM.pos()
        self.clickCount = 0
        self.clickDelay = 0.01
        self.preDelay = 0

    def _click(self):
        time.sleep(self.preDelay)

        for i in range(self.clickCount - 1):
            pgui.click(*self.target)
            time.sleep(self.clickDelay)

        pgui.click(*self.target)


class Click(_Base, _ClickBase):

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

        looper = LoopStart(), LoopEnd()

        looper[0].next = looper[1]
        looper[1].onSuccess = looper[0]

        for i in looper:
            i.name = name
            i.loopTime = loops

        return looper


class LoopStart(_Base, Loop):
    def __init__(self):
        super().__init__()

        self.name = ''
        self.next = None

    def action(self):
        return True


class LoopEnd(_Base, Loop):
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
    # slots_= ('targetImage', 'targetName', 'capturedImage',
    #             'screenArea', 'matchPoint', 'precision', 'offsetMax')
    
    imgSaver = ImgM.saveImg()
    
    def __init__(self):
        super().__init__()

        self.targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.screenArea = ImgM.Area()
        self.matchPoint = ImgM.pos()
        self.precision = 0.85
        self.offsetMax = 5

    def DumpCaptured(self, name=None):
        self.imgSaver(self.capturedImage, name)
        
    def DumpTarget(self):
        self.imgSaver(self.targetImage, self.targetName)

    def DumpCoordinates(self):      # Do I need this?
        return self.screenArea, self.matchPoint

    def SetArea(self, x1, y1, x2, y2):
        self.screenArea.__init__(x1, y1, x2, y2)


class ImageSearch(_Image, _ClickBase):
    # __slots__ = ('loopCount', 'loopDelay', 'trials', 'clickOnMatch', '_foundFlag')

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
    # __slots__ = 'matchCount'

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
        temp = list(sequence)
        for idx, i in enumerate(temp):
            if idx + 1 < len(temp):
                i.next = temp[idx + 1]
            else:
                break

        return temp


__all__ = MemberLoader.ListClass(__name__, blacklist={'_', 's'})
class_dict = MemberLoader.ListClass(__name__, blacklist={'_', 's'}, return_dict=True)
