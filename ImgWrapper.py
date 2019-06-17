from colorama import init, Fore, Style
import time
import imgsrch

init(convert=False, strip=False)


def PosVariableAvailable():
    global p1, p2

    try:
        import GlobalVar

    except NameError:
        p1 = [1920, 0]
        p2 = [0, 1080]

    else:
        p1 = [GlobalVar.x, GlobalVar.y]
        p2 = [GlobalVar.x2, GlobalVar.y2]


def ImgSearchArea(image, index, pre_delay=2, timeout=5):

    # Wrapper to skip coordination input and support timeout functionality
    # Convert imagesearcharea's return - 'relative' position to Absolute one.

    # Literally wrapper for wrapper! wrap-seption!
    # Split from MacroProcessor to be used in CustomAction.py

    PosVariableAvailable()

    pos = imgsrch.imagesearcharea(image, p1[0], p1[1], p2[0], p2[1])
    time.sleep(pre_delay)
    time_a = time.time()

    symbol = ['|', '/', '-', '＼']
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
            pos = imgsrch.imagesearcharea(image, p1[0], p1[1], p2[0], p2[1])

    if pos[0] != -1:
        pos2 = [pos[0] + p1[0], pos[1] + p1[1]]
        print(' - found at', pos2)
        return pos2
    else:
        return pos
