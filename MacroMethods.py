import time
import weakref
import pyautogui as pgui
# import shutil


class pos:
    # referenced vector2d_v0.py from 'Fluent Python' by Luciano.

    def __init__(self, x=-1, y=-1):
        self.x = int(x)
        self.y = int(y)     # limiting what x could be, catching error here.

    def __iter__(self):
        return self.x, self.y

    def __str__(self):
        return str(tuple(self))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __sub__(self, other):
        return abs(self.x - other.x), abs(self.y - other.y)


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
        pgui.click(*pos())


class Image(Base):
    # TODO: add weakref for Image, by adding all targets in single dict.
    __slots__ = ('methodType', 'targetImage', 'targetName', 'capturedImage'
                 'matchingArea', 'clickOnMatch', 'clickDelay', 'clickCount',
                 'loop', 'loopCount', 'loopDelay', 'clickCount')

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


    def ScreenShot(self, p1, p2): # Assuming p1, p2 is 'pos' cls
        self.capturedImage = pgui.screenshot(region=(*p1, p1 - p2))


class ImageClick

# TODO: add GOTO like macro method.
