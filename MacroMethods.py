import time
import functools
import weakref
import pyautogui as pgui
# import shutil

from ImageModule import pos, saveImg, imageSearch, RandomOffset, scanOccurrence


class Click:
    __slots__ = ('target', 'clickCount', 'clickDelay')

    def __init__(self):
        self.target = pos()
        self.clickCount = 0
        self.clickDelay = 0.01

    def click(self):
        for i in range(self.clickCount):
            pgui.click(*self.target)
            time.sleep(self.clickDelay)


class Wait:
    __slots__ = 'delay'

    def __init__(self):

        self.delay = 0

    def action(self):
        time.sleep(self.delay)


class Base:
    __slots__ = ('order', 'actionSuccess', 'actionFail')
    
    def __init__(self):
        self.order = None
        self.actionSuccess = None
        self.actionFail = None

    def action(self):
        print('Call to Base Method')


class Image(Base):
    # TODO: add weakref for Image, by adding all targets in single dict.
    # TODO: divide Image class to multiple sub-classes
    __slots__ = ('targetImage', 'targetName', 'capturedImage',
                 'screenArea', 'matchPoint', 'precision')
    
    imgSaver = saveImg()
    
    def __init__(self):
        super().__init__()

        self.targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.screenArea = (pos(), pos())
        self.matchPoint = pos()
        self.precision = 0.85

    @functools.lru_cache(maxsize=256, typed=False)
    def _region(self, pos_tuple):
        # change x/y x/y to x/y w/h for pyautogui.
        return *pos_tuple[0], *(pos_tuple[0] - pos_tuple[1])

    def DumpCaptured(self, name=None):
        self.imgSaver(self.capturedImage, name)
        
    def DumpTarget(self):
        self.imgSaver(self.targetImage, self.targetName)

    def DumpCoordinates(self):      # Do I need this?
        return self.screenArea, self.matchPoint


class ImageSearch(Image, Click):
    __slots__ = ('loopCount', 'loopDelay', 'trials', 'clickOnMatch', '_foundFlag')

    def __init__(self):
        super(ImageSearch, self).__init__()

        self.loopCount = 0
        self.loopDelay = 0.2
        self.trials = 5
        self.clickOnMatch = False
        self._foundFlag = False

    def _ImageSearch(self, precision=0.85):
        self.matchPoint, self.capturedImage = \
            imageSearch(self.targetImage, *self._region(self.screenArea), precision)

    def _ImageSearchMultiple(self, precision=0.85):
        for i in range(self.trials):
            self._ImageSearch()
            sefl.


    def ImageClick(self, offset_max=5):
        pgui.click(RandomOffset(self.matchPoint, offset_max))

    def action(self):




class SearchOccurrence(Image):
    __slots__ = 'matchCount'

    def __init__(self):
        super(SearchOccurrence, self).__init__()

        self.matchCount = 0

    def ScanOccurrence(self, precis=0.85):
        self.matchCount, self.capturedImage = \
            scanOccurrence(self.targetImage, *self._region(self.screenArea), precis)


# TODO: add GOTO like macro method.
