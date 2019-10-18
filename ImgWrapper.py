from colorama import init, Fore, Style
import time
import pyautogui as p_gui
import numpy as np
import cv2
import sys

init(convert=False, strip=False)

'''
# Wrapper to skip coordination input and support timeout functionality
# Convert imagesearcharea's return - 'relative' position to Absolute one.

# ImageSearch function is combination of OpenCV documentation & StackOverFlow's example
# Plus drov0's github repository 'python-imagesearch'
'''

# Todo: move getwindowpoint() to ImgWrapper.py

# ----------------------------------------------------------
# Take a screen shot of area and relay it to Other functions.

def ScreenShotArea(pos1, pos2):
    im = p_gui.screenshot(region=(pos1[0], pos1[1], pos2[0] - pos1[0], pos2[1] - pos1[1]))
    # im.save('test.png')
    return im


# ----------------------------------------------------------
# Search Image, and return location.
# Will return [-1, -1] if not found.

def ImageSearch(image, precision=0.8):
    GetGlobalPos()

    img = np.array(ScreenShotArea(p1, p2))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


# ----------------------------------------------------------
# Adds Random offset to prevent anti-bot method, will click with maximum derivation of 'offset'

def RandomOffset(pos, offset):
    import random
    x_offset = random.randrange(0, offset)
    pos[0] = pos[0] + offset
    pos[1] = pos[1] + offset - x_offset
    return pos


# ----------------------------------------------------------
# Get Global Position of Area, if GlobalVar.py is not found, will create variable with
# 1920 1080 Area.

def GetGlobalPos():
    # See whether GlobalVar is available or not
    global p1, p2

    try:
        import GlobalVar
        if GlobalVar.x2 == 0:
            raise NameError

    except NameError:
        p1 = [0, 0]
        p2 = [1920, 1080]

    else:
        p1 = [GlobalVar.x, GlobalVar.y]
        p2 = [GlobalVar.x2, GlobalVar.y2]


# ----------------------------------------------------------
# Keeps searching Image with pre-delay and timeout(or deadline) functionality.

def ImgSearchArea(image, pre_delay=2, timeout=5, no_warn=False):

    # Since Changing erase method to \b now requires stdout.flush().

    pos = ImageSearch(image)
    time.sleep(pre_delay)
    time_a = time.time()

    # symbol = ['|', '/', '-', '＼']
    symbol = ['.   ', '..  ', '... ', '....']
    sym = 0

    print('looking for', Fore.YELLOW, image, Style.RESET_ALL, end='   ')
    sys.stdout.flush()

    while pos[0] == -1:
        sym = sym + 1
        time.sleep(0.3)

        if time.time() - time_a > timeout:
            if not no_warn:
                print(Fore.RED, '\n!! Image', image, 'timeout!', Style.RESET_ALL)
            else:
                print('')
            break
        else:
            print('\b'*len(symbol[(sym-1) % 4]) + symbol[sym % 4], sep='', end='')
            sys.stdout.flush()
            pos = ImageSearch(image)

    if pos[0] != -1:
        pos2 = [pos[0] + p1[0], pos[1] + p1[1]]
        print('\n - found at', pos2)
        return pos2
    else:
        return pos


# ----------------------------------------------------------
# Counts number of Occurrence of target Image.
# Will ignore Overlapping Occurrences which has position smaller than threshold*min([h, w])
# threshold decides how much clipping between occurrences is accepted.


def ScanOccurrence(image, precision=0.8, threshold=0.3, output=True):
    from math import sqrt
    '''
    if 'img_id' not in globals():
        global img_id
        img_id = 1
    '''
    GetGlobalPos()

    img = np.array(ScreenShotArea(p1, p2))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= precision)

    count = 0
    last_pt = [0, 0]

    for pt in sorted(zip(*loc[::-1])):
        if sqrt(abs(last_pt[0]-pt[0])**2 + abs(last_pt[0]-pt[0])**2) < threshold*min([h, w]):
            continue
        else:
            last_pt = pt
            print(pt)
            count = count + 1
            if output:
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    if output:
        cv2.imwrite('last_image.png', img)
        #cv2.imwrite(img_id + '.png', img)
        img_id += 1
    return count
