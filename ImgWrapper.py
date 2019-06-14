from colorama import init, Fore, Style
import time
import imgsrch


init(convert=False, strip=False)


class Coordination:                     # Do I need __init__? idk,
    def __init__(self, x, y):           # Using list is way better but-
        self.X = x                      # I wanted to learn class a bit
        self.Y = y


def ImgSearchArea(pos1, pos2, image, index, pre_delay=2, timeout=5, ):

    # Wrapper to skip coordination input and support timeout functionality
    # Convert imagesearcharea's return - 'relative' position to Absolute one.

    # Literally wrapper for wrapper! wrap-seption!
    # Split from MacroProcessor to be used in CustomAction.py

    pos = imgsrch.imagesearcharea(image, pos1.X, pos1.Y, pos2.X, pos2.Y)
    time.sleep(pre_delay)
    time_a = time.time()

    symbol = ['|', '/', '-', '\\']
    sym = 0

    while pos[0] == -1:
        print('looking for', Fore.YELLOW, image, Style.RESET_ALL, symbol[sym % 4], end='')
        sym = sym + 1
        time.sleep(0.5)
        print('', end='\r')

        if time.time() - time_a > timeout:
            print(Fore.RED, 'At line', index, '- image', image, 'timeout!', Style.RESET_ALL)
            break
        else:
            pos = imgsrch.imagesearcharea(image, pos1.X, pos1.Y, pos2.X, pos2.Y)

    if pos[0] != -1:
        pos2 = [pos[0] + pos1.X, pos[1] + pos1.Y]
        print(' - found at', pos2)
        return pos2
    else:
        return pos
