import pyautogui as pgui
import numpy as np
import cv2

"""
This module will provide any necessary components required by MacroMethod,
especially Image-related functions.
"""

IMG_PATH = "./testingEnv/"


class Pos:
    # referenced vector2d_v0.py from 'Fluent Python' by Luciano.

    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)  # limiting what x could be, catching error here.

    def __iter__(self):
        return iter((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))

    def __bool__(self):
        return True if all((self.x, self.y)) else False

    def __str__(self):
        return str(tuple(self))

    def __mul__(self, other):
        return Pos(int(self.x * other), (self.y * other))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __add__(self, other):
        try:
            return Pos(self.x + other.x, self.y + other.y)
        except AttributeError:
            tmp = Pos(*other)
            return Pos(self.x + tmp.x, self.y + tmp.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def __abs__(self):
        return Pos(abs(self.x), abs(self.y))

    def __call__(self):
        return self.x, self.y

    def __ge__(self, other):
        return (self.x >= other.x) & (self.y >= other.y)

    def __le__(self, other):
        return (self.x <= other.x) & (self.y <= other.y)

    def set(self, x, y=None):
        self.x, self.y = x, y


class Area:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.p1 = Pos(x1, y1)
        self.p2 = Pos(x2, y2)
        self.sort()

    def __call__(self, *args, **kwargs):
        return *self.p1(), *self.p2()

    def __iter__(self):
        return iter((*self.p1, *self.p2))

    def __str__(self):
        return str(tuple(self))

    @property
    def region(self):
        return *self.p1, *abs(self.p1 - self.p2)

    def sort(self):
        if all((self.p1, self.p2)):
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
            name = ""

        cv2.imwrite(f"{IMG_PATH}{str(order)}_{name}.png", img)
        order += 1

    return save


IMG_SAVE = saveImg()  # can't move this up..


def imageSearch(target, area, precision=0.85):

    array = np.array(pgui.screenshot(region=area))

    img = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    template = cv2.cvtColor(np.array(target), cv2.COLOR_RGB2GRAY)
    img_wh = template.shape[::-1]

    # pgui.locateOnScreen(target, minSearchTime=5, confidence=0.9)
    # didn't know this existed, but can't customize it anyway.

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val < precision:
        return False, img
    else:
        pt2 = tuple(x + y for x, y in zip(img_wh, max_loc))
        cv2.rectangle(img, max_loc, pt2, (0, 0, 255), 2)

        return Pos(*max_loc), img


def scanOccurrence(target, area, precision=0.85, threshold=0.1):

    array = np.array(pgui.screenshot(region=area))

    img = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    template = cv2.cvtColor(np.array(target), cv2.COLOR_RGB2GRAY)
    img_wh = Pos(*template.shape[::-1])

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= precision)

    count = 0
    found = []
    threshold_pixel = img_wh * threshold

    for pt in sorted(zip(*loc[::-1])):
        try:
            if (
                (found[-1] + img_wh + threshold_pixel)
                >= Pos(*pt)
                >= (found[-1] - threshold_pixel)
            ):
                continue
        except IndexError:  # intentionally causing first run of for loop catch this
            pass

        found.append(Pos(*pt))
        count = count + 1
        cv2.rectangle(img, pt, (Pos(*pt) + img_wh)(), (0, 0, 255), 2)
        # need to explicitly give cv2 tuple, not tuple-type.

    return count, img, found


def RandomOffset(pos, offset):
    import random

    x_offset = random.randrange(0, offset)
    y_offset = random.randrange(0, offset - x_offset)
    off = Pos(x_offset, y_offset)
    try:
        return pos + off
    except TypeError:
        return Pos(*pos) + off
