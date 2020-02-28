import time
import functools
import weakref
import pyautogui as pgui
# import shutil

from ImageModule import pos, saveImg, imageSearch, RandomOffset, scanOccurrence

# @functools.lru_cache(maxsize=256, typed=false)

class Base:
    
    def __init__(self):
        self.order = None
        self.actionSuccess = None
        self.actionFail = None
        self.methodType = 0

    def action(self):
        print('Call to Base Method')

        
class Wait(Base):

    def __init__(self):
        super().__init__()

        self.methodType = 1
        self.delay = 0

    def action(self):
        time.sleep(self.delay)


class click(Base):

    def __init__(self):
        super().__init__()

        self.methodType = 2
        self.target = pos()

    def action(self):
        pgui.click(*self.target)


class Image(Base):
    # TODO: add weakref for Image, by adding all targets in single dict.
    # TODO: divide Image class to multiple sub-classes
    __slots__ = ('methodType', 'targetImage', 'targetName', 'capturedImage'
                 'screenArea', 'matchPoint', 'clickOnMatch', 'clickDelay',
                 'clickCount', 'loop', 'loopCount', 'loopDelay', 'clickCount',
                 'matchCount')
    
    imgSaver = saveImg()
    
    def __init__(self):
        super().__init__()

        self.methodType = 3
        self.targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.screenArea = (pos(), pos())
        self.matchPoint = pos()
        self.matchCount = 0

        self.clickOnMatch = False
        self.clickDelay = 0.05
        # self.clickCount = 2
        # TODO: make custom number of click possible.

        self.loop = False
        self.loopCount = 0
        self.loopDelay = 0.2
    
    def DumpCaptured(self, name=None):
        self.imgSaver(self.capturedImage, name)
        
    def DumpTarget(self):
        self.imgSaver(self.targetImage, self.targetName)
        
    def pgui_region(self):
        return *self.screenArea[0], *(self.screenArea[0] - self.screenArea[1])

    def ImageSearch(self, precision=0.85):
        self.matchPoint, self.capturedImage = \
                imageSearch(self.targetImage, *self.pgui_region(), precision)
        
    def ImageClick(self, offset_max=5):
        pgui.click(RandomOffset(self.matchPoint, offset_max))
        
    def ScanOccurrence(self, precision=0.85):
        self.matchCount, self.capturedImage = \
                scanOccurrence(self.targetImage, *self.pgui_region(), precision)

# TODO: add GOTO like macro method.
