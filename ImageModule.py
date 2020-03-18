import cv2
import os
import time
import functools
import numpy as np
import pyautogui as pgui
import keyboard
from math import sqrt

"""
This module will provide any necessary components required by MacroMethod,
especially Image-related functions.
"""
# TODO: add exception handler for functions here.


class pos:
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
        self.p1 = pos(x1, y1)
        self.p2 = pos(x2, y2)
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


def getCaptureArea():
    p1 = pos()
    p2 = pos()
    kill_key = 'f2'
    
    def breakKeyInput(input_key):     # delay until key is up, to prevent input skipping
        while not keyboard.is_pressed(input_key):
            print('Waiting for key:')
            time.sleep(0.05)
    
    def getPos(p):
        nonlocal kill_key

        breakKeyInput(kill_key)
        p.set(*pgui.position())
        breakKeyInput(kill_key)
        
    def getArea():

        # all_clear = False
        # while all_clear:
        #     getPos(p1)
        #     getPos(p2)
        # TODO: add confirmation

        getPos(p1)
        getPos(p2)

    # getArea()
    # return Area(*p1, *p2)

    return Area(80, 80, 600, 600)

    
def saveImg():
    """
    Save Image with ascending ordered numeric names. Closure demonstration.
    Refer docs of function save().
    :return: returns closure function save().
    """
    order = 0
    
    def nameIt(n):
        return str(n) + '.png'

    def save(file, name=None):

        nonlocal order

        if name is None:
            name = nameIt(order)

        cv2.imwrite(name + '.png', file)
        order += 1

    return save


def imageSearch(target, area, precision=0.85):
    """
    position will use tuple(pos(), pos())!
    """
    img = cv2.cvtColor(np.array(pgui.screenshot(region=area)), cv2.COLOR_RGB2BGR)
    cv2.imwrite('test.png', img)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('test2.png', img_gray)

    template = cv2.cvtColor(np.array(target.convert("RGB")), cv2.COLOR_RGB2BGR)
    # Above having issue with zero-filled array.
    img_wh = template.shape[::-1]

    # pgui.locateOnScreen(target, minSearchTime=5, confidence=0.9)
    # didn't know this existed, but I'm sure this is slower per run.

    #https://stackoverflow.com/questions/44955656/how-to-convert-rgb-pil-image-to-numpy-array-with-3-channels

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val < precision:
        return (-1, -1), img
    else:
        cv2.rectangle(img, max_loc, list(x+y for x, y in zip(img_wh, max_loc)), (0, 0, 255), 2)
        cv2.imwrite('test3.png', img_gray)
        return max_loc, img


def scanOccurrence(target, corner_pos, xy, precision=0.8, threshold=0.3):
    
    # TODO: Rework these codes
    
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
            cv2.rectangle(img, pt, tuple(map(sum, zip(pt, image_wh))), (0, 0, 255), 2)
    
    return count, img


def RandomOffset(corner_pos, offset):
    import random
    x_offset = random.randrange(0, offset)
    corner_pos.x = corner_pos.x + offset
    corner_pos.y = corner_pos.y + offset - x_offset
