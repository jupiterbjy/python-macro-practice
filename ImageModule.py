import cv2
import os
import numpy as np
import pyautogui as pgui
import keyboard


"""
This module will provide any necessary components required by MacroMethod,
especially Image-related functions.
"""

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
    
    def assign(self, tup):
        self.x, self.y = *tup
        
    # def pgui_region(self, other):
    #     return self.x, self.y, *(self - other)


def getCaptureArea():
    windowArea = pos(), pos()
    kill_key = 'f2'
    
    def breakKeyInput(input_key):     # delay until key is up, to prevent input skipping
        while keyboard.is_pressed(input_key):
            time.sleep(0.05)
    
    def getPos(order):
        nonlocal windowArea, kill_key
        
        while not keyboard.is_pressed(kill_key):
            # TODO: check and rearrange input pos.
            time.sleep(0.5)
        
        windowArea[order].assign(*pyautogui.position())
        
    def getArea():
        getPos(1)
        breakKeyInput(kill_key)
        
        getPos(2)
        breakKeyInput(kill_key)
        
    
def saveImg():
    """
    Save Image with ascending ordered numeric names.
    :return:
    """
    order = 0
    
    def nameIt(n):
        return str(n) + '.png'
        
    def save(file, name=None, overwrite=True):
        nonlocal order

        if name is None:
            name = nameIt(order)

        if overwrite:
            while os.path.isfile(name):
                order += 1
                name = nameIt(order)
                
            print(f'File "{name}" already exists. Renaming. ')
            # name = name.split('.')[0] + '_' + '.png'
            # TODO: add other overwrite methods.

        cv2.imwrite(name + '.png', file)

        order += 1

    return save


def imageSearch(target, pos, xy, precision=0.85):
    """
    position will use tuple(pos(), pos())!
    """
    
    img = np.array(pgui.screenshot(region=(*pos, *xy)))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val < precision:
        return [-1, -1]
    return max_loc
