import time
import functools
# import weakref
import pyautogui as pgui
# import shutil

from ImageModule import pos, saveImg, imageSearch, RandomOffset, scanOccurrence

# TODO: convert to default abc module if possible.
# TODO: or convert into coroutine
# TODO: utilize sys.path.insert.


class Base:
    __slots__ = ('name', 'order')

    def __init__(self):
        self.name = None
        self.order = -1

    def action(self):
        print('Call to Base Method')

# --------------------------------------------------------

def click(pre_delay, click_count, pos, )


class Click:
    __slots__ = ('target', 'clickCount', 'clickDelay',
                 'preDelay', 'actionState')

    def __init__(self):
        self.target = pos()
        self.clickCount = 0
        self.clickDelay = 0.01
        self.preDelay = 0

    def click(self):

        time.sleep(self.preDelay)

        for i in range(self.clickCount - 1):
            pgui.click(*self.target)
            time.sleep(self.clickDelay)

        pgui.click(*self.target)

# --------------------------------------------------------
# TODO: find better way to embed loop.


class Loop:
    __slots__ = ('loopTime', 'endOrder', 'currentLoop', 'startOrder', 'loopName')

    def __init__(self):
        self.loopTime = 3
        self.startOrder = None
        self.endOrder = None
        self.currentLoop = 0
        self.loopName = None


class LoopStart(Base):
    def __init__(self, loop_obj):
        super().__init__()

        self.name = loop_obj.loopName
        self.object = loop_obj

    def action(self):
        return self.object.startOrder, self.object.endOrder, self.object.loopTime


class LoopEnd(Base):
    def __init__(self, loop_obj):
        super().__init__()
        self.name = loop_obj.loopName
        self.object = loop_obj

    def action(self):
        pass

# --------------------------------------------------------


class Goto(Base):
    def __init__(self):
        super().__init__()
        self.gotoOrder = None

    def action(self):
        pass
        # loop and goto will be handled by MacroSequencer.py.
        # this is placeholder.


class Wait(Base):
    __slots__ = ('delay', 'actionState')

    def __init__(self):
        super().__init__()
        self.delay = 0
        self.actionState = -2

    def action(self):
        self.actionState = -1

        time.sleep(self.delay)

        self.actionState = 1


class Variable(Base):
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

class ActionBase(Base):
    __slots__ = ('actionSuccess', 'actionFail', 'actionState')
    
    def __init__(self):
        super().__init__()
        self.actionSuccess = None
        self.actionFail = None
        self.actionState = -2      # -2: standby / -1: active / 0: fail / 1: Success


class Image(ActionBase):
    # TODO: add weakref for Image, by adding all targets in single dict.
    # TODO: divide Image class to multiple sub-classes
    __slots__ = ('targetImage', 'targetName', 'capturedImage',
                 'screenArea', 'matchPoint', 'precision', 'offsetMax')
    
    imgSaver = saveImg()
    
    def __init__(self):
        super().__init__()

        self.targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.screenArea = (pos(), pos())
        self.matchPoint = pos()
        self.precision = 0.85
        self.offsetMax = 5

    @functools.lru_cache(maxsize=256, typed=False)
    def _region(self):
        # change x/y x/y to x/y w/h for pyautogui.
        return *self.screenArea[0], *(self.screenArea[0] - self.screenArea[1])

    def DumpCaptured(self, name=None):
        self.imgSaver(self.capturedImage, name)
        
    def DumpTarget(self):
        self.imgSaver(self.targetImage, self.targetName)

    def DumpCoordinates(self):      # Do I need this?
        return self.screenArea, self.matchPoint


class ImageSearch(Image, Click):
    __slots__ = ('loopCount', 'loopDelay', 'trials', 'clickOnMatch',
                 '_foundFlag')

    def __init__(self):
        super(ImageSearch, self).__init__()

        self.loopCount = 0
        self.loopDelay = 0.2
        self.trials = 5
        self.clickOnMatch = False
        self._foundFlag = False

    def ImageSearch(self):
        self.matchPoint, self.capturedImage = \
            imageSearch(self.targetImage, *self._region(), self.precision)
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
        pgui.click(RandomOffset(self.matchPoint, self.offsetMax))

    def action(self):
        self.actionState = -1

        self.ImageSearchMultiple()
        if self._foundFlag:
            if self.clickOnMatch:
                self.target = self.matchPoint
                self.click()

        # TODO: add error handling


class SearchOccurrence(Image, Click):
    # TODO: finish thid
    __slots__ = 'matchCount'

    def __init__(self):
        super(SearchOccurrence, self).__init__()

        self.matchCount = 0

    def ScanOccurrence(self):
        self.actionState = -1
        self.matchCount, self.capturedImage = \
            scanOccurrence(self.targetImage, *self._region(), self.precision)
        if self.matchCount > 0:
            self.actionState = 1

        else:
            self.actionState = 0


class Actions(Wait, Variable, Click, SearchOccurrence, imageSearch):
    pass
