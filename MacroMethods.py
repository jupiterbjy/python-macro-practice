import cv2
import sys
import pyautogui as pgui
import time
import numpy as np
from math import sqrt
from datetime import datetime

class Dependency:
    
    p1 = [0,0]
    p2 = [0,0]
    
    
def saveImg():
    index = 0

    def save(name=''):
        nonlocal index

        if name:
            cv2.imwrite(name + '.png')
            # TODO: add duplicate support
        else:
            cv2.imwrite(index + '.png', img)

        index += 1
    return save


# def fileSaveDecor(func):
#     def fileSave:
        
#         saveImg

        
class ImageMacro(Dependency):
    
    def __init__(self):
        pass
    
    

    
    
    def ScreenShotArea(pos1, pos2):
        "Takes a screenshot of area as a file-like object. (probably)"
        "Will get position of target with 2 lists or tuples containing xy coordinates."
        
        return pgui.screenshot(region=(pos1*, pos1[1], pos2[0] - pos1[0], pos2[1] - pos1[1]))
    
    
    def ImgSearchArea(image, pre_delay=2, timeout=5, no_warn=False):

        time.sleep(pre_delay)
        pos = ImageSearch(image)
        time_a = time.time()

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
        
        
    def ScanOccurrence(image, precision=0.8, threshold=0.3, output=True):
        
        if 'img_id' not in globals():
            global img_id
            img_id = 1

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
                
                # Move this to outside of this function
                if output:
                    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        if output:
            cv2.imwrite('last_image.png', img)
            #cv2.imwrite(img_id + '.png', img)
            img_id += 1
        return (count, img)


class Wait:
    def __init__(self, )
    

