import cv2
import os
import sys
import pyautogui as pgui
import time
# import shutil
import numpy as np
from math import sqrt
from datetime import datetime


class Base:
    def __init__(self):
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

        return self.action

