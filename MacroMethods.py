import time
import functools
import weakref
import pyautogui as pgui
# import shutil

from ImageModule import pos, saveImg

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
    __slots__ = ('methodType', 'targetImage', 'targetName', 'capturedImage'
                 'matchingArea', 'clickOnMatch', 'clickDelay', 'clickCount',
                 'loop', 'loopCount', 'loopDelay', 'clickCount')
    
    imgSaver = saveImg.save
    
    def __init__(self):
        super().__init__()

        self.methodType = 3
        self.targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.matchingArea = (pos(), pos())

        self.clickOnMatch = False
        self.clickDelay = 0.05
        # self.clickCount = 2
        # TODO: make custom number of click possible.

        self.loop = False
        self.loopCount = 0
        self.loopDelay = 0.2
    
    def DumpCaptured(self, name=None):
        imgSaver(self.capturedImage, name)
        
    def Dumptarget(self, name=self.targetName)
        imgSaver(self.targetImage, name)


    def ScreenShot(self, p1, p2): # Assuming p1, p2 is 'pos' cls
        self.capturedImage = pgui.screenshot(region=(*p1, p1 - p2))


class ImageClick(Image):
    
    def __init__(self):
        self.target = pos()

    def action(self):
        pgui.click(*self.target)


# TODO: add GOTO like macro method.
