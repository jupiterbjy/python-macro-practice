import keyboard
import pyautogui
import time
import cv2

from ImgWrapper import ScreenShotArea
from ToolSet.FrozenDetect import DetectFrozen


def GetMousePos(kill_key):              # similar code from pyautogui ex

    pos = [0, 0]
    while not keyboard.is_pressed(kill_key):
        pos[0], pos[1] = pyautogui.position()
        pos_string = 'X:' + str(pos[0]).rjust(4) + str(pos[1]).rjust(4)

        print(pos_string, end='')
        time.sleep(0.05)
        print('', end='\r')

    return pos[0], pos[1]


def BreakKeyInput(input_key):               # delay until key is up
    while keyboard.is_pressed(input_key):
        time.sleep(0.05)


def GetImagePoint(kill_key):

    x1, y1 = GetMousePos(kill_key)
    print("Pos1:", x1, y1)
    BreakKeyInput(kill_key)

    x2, y2 = GetMousePos(kill_key)
    print("Pos2:", x2, y2)
    BreakKeyInput(kill_key)

    print("Area:", abs(x1 - x2), "*", abs(y1 - y2))

    if (x2 - x1) < 0:       # pos1 = is right side?
        temp = [x2, y2]

        x2 = x1
        y2 = y1

        x1 = temp[0]
        y1 = temp[1]

    return [x1, y1, x2, y2]


def capture(input_key='f2'):

    loc = GetImagePoint(input_key)
    img = ScreenShotArea([loc[0], loc[1]], [loc[2], loc[3]])

    name = ''
    while name == '':
        name = input('Input File name:')

    f_name = ''.join([name, '.png'])

    try:
        img.save(f_name)
    except cv2.error:
        print('cv2 error')
        raise

    print('File saved as', f_name, end='\n\n')


# ------------------------------------------------------
Trigger = True
print('press f2 to set Pos')

DetectFrozen()


while Trigger:
    capture()
