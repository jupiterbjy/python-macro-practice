from colorama import init, Fore, Style
import time
import pyautogui as p_gui
import numpy as np
import cv2

init(convert=False, strip=False)

# Wrapper to skip coordination input and support timeout functionality
# Convert imagesearcharea's return - 'relative' position to Absolute one.

# ImageSearch function is from OpenCV documentation & StackOverFlow
# Plus drov0's github repository 'python-imagesearch'


def ScreenShotArea(pos1, pos2):
    im = p_gui.screenshot(region=(pos1[0], pos1[1], pos2[0] - pos1[0], pos2[1] - pos1[1]))
    # im.save('test.png')
    return im


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


def RandomOffset(pos, offset):
    import random
    x_offset = random.randrange(0, offset)
    pos[0] = pos[0] + offset
    pos[1] = pos[1] + offset - x_offset
    return pos


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


# --------------------------------------------------------------------------


def ImgSearchArea(image, pre_delay=2, timeout=5, no_warn=False):

    pos = ImageSearch(image)
    time.sleep(pre_delay)
    time_a = time.time()

    symbol = ['|', '/', '-', '＼']
    sym = 0

    print('looking for', Fore.YELLOW, image, Style.RESET_ALL, end=' ')

    while pos[0] == -1:
        sym = sym + 1
        time.sleep(0.3)
        print('', sep='', end='\b')

        if time.time() - time_a > timeout:
            if not no_warn:
                print(Fore.RED, '\r!! Image', image, 'timeout!', Style.RESET_ALL)
            break
        else:
            print(symbol[sym % 4], sep='', end='')
            pos = ImageSearch(image)

    if pos[0] != -1:
        pos2 = [pos[0] + p1[0], pos[1] + p1[1]]
        print('\n\r - found at', pos2)
        return pos2
    else:
        return pos


def ScanOccurrence(image, precision=0.8, threshold=0.3):
    # threshold decides how much clipping between occurrences is accepted.
    from math import sqrt

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
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv2.imwrite('last_result.png', img)
    return count
