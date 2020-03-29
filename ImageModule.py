import cv2
import functools
import numpy as np
import pyautogui as pgui
from math import sqrt

"""
This module will provide any necessary components required by MacroMethod,
especially Image-related functions.
"""

IMG_PATH = './testingEnv/'


class Pos:
    # referenced vector2d_v0.py from 'Fluent Python' by Luciano.

    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)     # limiting what x could be, catching error here.

    def __iter__(self):
        return iter((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return str(tuple(self))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __add__(self, other):
        return (self.x + other.x), (self.y + other.y)

    def __sub__(self, other):
        return abs(self.x - other.x), abs(self.y - other.y)

    def __call__(self):
        return self.x, self.y
    
    def set(self, x, y):
        self.x, self.y = x, y


class Area:

    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.p1 = Pos(x1, y1)
        self.p2 = Pos(x2, y2)
        self.sort()

    def __iter__(self):
        return iter((*self.p1, *self.p2))

    def __str__(self):
        return str(tuple(self))

    @property
    def region(self):
        return *self.p1, *(self.p1 - self.p2)

    @functools.lru_cache(maxsize=128, typed=False)
    def sort(self):
        x, y = [sorted(list(i)) for i in zip(self.p1, self.p2)]
        self.p1.set(x[0], y[0])
        self.p2.set(x[1], y[1])

    def set(self, x1, y1, x2, y2):
        self.__init__(x1, y1, x2, y2)

    @staticmethod
    def fromPos(p1, p2):
        return Area(*p1, *p2)

    
def saveImg():
    """
    Save Image with ascending ordered numeric names. Closure demonstration.
    Refer docs of function save().
    :return: returns closure function save().
    """
    order = 0

    def save(img, name=None):

        nonlocal order

        if name is None:
            name = ''

        cv2.imwrite(f'{IMG_PATH}{str(order)}_{name}.png', img)

        order += 1

    return save


IMG_SAVE = saveImg()      # can't move this up..


def imageSearch(target, area, precision=0.85):
    img = cv2.cvtColor(np.array(pgui.screenshot(region=area)), cv2.COLOR_RGB2BGR)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    template = cv2.cvtColor(np.array(target), cv2.COLOR_RGB2GRAY)
    img_wh = template.shape[::-1]

    # pgui.locateOnScreen(target, minSearchTime=5, confidence=0.9)
    # didn't know this existed, but can't customize it anyway.

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val < precision:
        return (-1, -1), img
    else:
        pt2 = tuple(x+y for x, y in zip(img_wh, max_loc))
        cv2.rectangle(img, max_loc, pt2, (0, 0, 255), 2)

        return max_loc, img


def scanOccurrence(target, corner_pos, xy, precision=0.8, threshold=0.3):
    
    img = np.array(pgui.screenshot(region=(*corner_pos, *xy)))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(target, 0)
    image_wh = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= precision)

    count = 0
    last_pt = [0, 0]

    for pt in sorted(zip(*loc[::-1])):
        if sqrt(abs(last_pt[0]-pt[0])**2 + abs(last_pt[0]-pt[0])**2) < threshold*min(image_wh):
            continue
        else:
            print(last_pt := pt)
            count = count + 1
            cv2.rectangle(img, pt, tuple(map(sum, zip(pt, image_wh))), (0, 0, 255), 1)
            IMG_SAVE('found', img)
    
    return count, img


def RandomOffset(corner_pos, offset):
    import random
    x_offset = random.randrange(0, offset)
    corner_pos.x = corner_pos.x + offset
    corner_pos.y = corner_pos.y + offset - x_offset

