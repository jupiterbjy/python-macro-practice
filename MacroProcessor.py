import cv2
import time
import imgsrch
import sys
import pyautogui

import CustomAction


class Coordination:                     # Do I need __init__? idk,
    def __init__(self, x, y):           # Using list is way better but-
        self.X = x                      # I wanted to learn class a bit
        self.Y = y


def SetDefaultBoundary(c1, c2):
    global Pos1
    global Pos2

    Pos1 = Coordination(c1.X, c1.Y)
    Pos2 = Coordination(c2.X, c2.Y)


def ImgSearchArea(image, index, pre_delay=2, timeout=5):

    # Wrapper to skip coordination input and support timeout functionality

    pos = imgsrch.imagesearcharea(image, Pos1.X, Pos1.Y, Pos2.X, Pos2.Y)
    time.sleep(pre_delay)
    time_a = time.time()

    symbol = ['|', '/', '-', '\\']
    sym = 0

    while pos[0] == -1:
        print('looking for', image, symbol[sym % 4], end="\r")
        sym = sym + 1
        time.sleep(0.5)

        if time.time() - time_a > timeout:
            print('At line', index, '- image', image, 'timeout!!')
            break
        else:
            pos = imgsrch.imagesearcharea(image, Pos1.X, Pos1.Y, Pos2.X, Pos2.Y)

    if pos[0] != -1:
        print('found at', pos)
    else:
        print('image not found')
    return pos


def MainSequence(coord_1, coord_2, file):

    SetDefaultBoundary(coord_1, coord_2)

    # Reads Macro Sequence File and process it
    # line starts with & means start of sub-sequence, which all operation is wrapped with.
    # Any failure inside it skips sub-sequence as latter part of it become useless.
    # spl[0] = image / [1] = operation mode / [2] = pre_delay / [3] = max waiting time
    # Operation Mode 0: Search only / 1: Search and Click / 2: 1 with failure acceptance
    #                3 4 5 6: Custom Action written in CustomAction.py

    for i in range(len(file)):

        if '@' in file[i] or '#' in file[i]:
            continue

        # Sub-Sequence Start

        elif '&' in file[i]:
            seq_line = file[i].split()
            print("Sub-Sequence", seq_line[1], "Start")
            del seq_line

            # Line process Start

            while True:

                i = i + 1

                if '&' in file[i]:
                    break
                elif '#' in file[i]:
                    continue

                spl = file[i].split()

                print(spl)

                try:

                    if len(spl) == 2:
                        pos = ImgSearchArea(spl[0], i)

                    elif len(spl) == 3:
                        pos = ImgSearchArea(spl[0], int(spl[2]), i)

                    else:
                        pos = ImgSearchArea(spl[0], i, int(spl[2]), int(spl[3]))

                except cv2.error:
                    print('At Line', i, spl[0], 'does not exist!!')
                    print('Script shutdown in 10 seconds.')
                    time.sleep(10)
                    sys.exit()

                # Operation Mode Start

                else:

                    if spl[0] == '3':
                        CustomAction.CustomAction1(pos)

                    elif spl[0] == '4':
                        CustomAction.CustomAction2(pos)

                    elif spl[0] == '5':
                        CustomAction.CustomAction3(pos)

                    elif spl[0] == '6':
                        CustomAction.CustomAction4(pos)

                    elif pos[0] == -1:

                        if spl[0] == '0' or spl[0] == '1':
                            break

                        elif spl[0] == '2':
                            continue

                        else:
                            print('wrong index is given in file.')

                    else:

                        if spl[0] == '1':
                            pyautogui.moveTo(pos)
                            pyautogui.click()

    print('Script Ended. Shutdown in 10 seconds.')
    time.sleep(10)