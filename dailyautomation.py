
from colorama import init, Fore, Style
import pyautogui
import keyboard
import time
import imgsrch
import sys
import cv2

import GenerateMacroStep
import CustomAction

killkey = 'f2'


class MacroStep:
    def __init__(self, index, imagename, priordelay, option):
        self.Index = index
        self.imgName = imagename
        self.pDelay = priordelay
        self.Option = option


class Coordination:                     # Do I need __init__? idk,
    def __init__(self, x, y):           # Using list is way better but-
        self.X = x                      # I wanted to learn class a bit
        self.Y = y


def GetMousePos(kill_key):              # similar code from pyautogui ex

    pos = Coordination(0, 0)
    while not keyboard.is_pressed(kill_key):
        pos.X, pos.Y = pyautogui.position()
        pos_string = 'X:' + str(pos.X).rjust(4) + str(pos.Y).rjust(4)

        print(pos_string, end='')
        time.sleep(0.05)
        print('\b' * len(pos_string), end='', flush=True)

    return pos.X, pos.Y


def BreakKeyInput(input_key):               # delay until key is up
    while keyboard.is_pressed(input_key):
        time.sleep(0.05)


def GetWindowPoint(kill_key):
    global Pos1, Pos2
    global trigger

    trigger = True

    Pos1 = Coordination(0, 0)
    Pos2 = Coordination(0, 0)

    while trigger:

        Pos1.X, Pos1.Y = GetMousePos(kill_key)
        print("Pos1:", Pos1.X, Pos1.Y)
        BreakKeyInput(kill_key)

        Pos2.X, Pos2.Y = GetMousePos(kill_key)
        print("Pos2:", Pos2.X, Pos2.Y)
        BreakKeyInput(kill_key)

        print("Area:", abs(Pos1.X - Pos2.X), "*", abs(Pos1.Y - Pos2.Y))

        if abs(Pos1.X - Pos2.X) < 1280 or abs(Pos1.Y - Pos2.Y) < 720:

            print("\nDesignated Size is smaller than 1280*720!!")
            print("Try again!\n")

        else:
            trigger = False

        if (Pos2.X - Pos1.X) < 0:       # pos1 = is right side?
            temp = Coordination(Pos2.X, Pos2.Y)

            Pos2.X = Pos1.X
            Pos2.Y = Pos1.Y

            Pos1.X = temp.X
            Pos1.Y = temp.Y

            print("Swapping Pos1 & Pos2 for imgsrch.py")


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
            print('Script shutdown in 10 seconds.')
            time.sleep(10)
            sys.exit()

        else:
            pos = imgsrch.imagesearcharea(image, Pos1.X, Pos1.Y, Pos2.X, Pos2.Y)

    if pos[0] != -1:
        print('found at', pos)
    else:
        print('image not found')
    return pos


def GetWindowPoint_INFORM():
    init()                              # colorama initialization

    print(Fore.RED + '\n  +', Style.RESET_ALL, end='', sep='')
    print("___________________ ")
    print("   |                 | ")
    print("   |                 | ")
    print("   |     N  O  X     | ")
    print("   |                 | ")
    print("   |                 | ")
    print("    ￣￣￣￣￣￣￣￣￣￣", end='', sep='')
    print(Fore.RED + '+\n', Style.RESET_ALL)

    print("Press", killkey, "While pointing indicated points\n")


'''
def PreStart_INFORM():
    print("Waiting for Main page")
    ImgSearchArea("./CoreImage/main.png")
'''


def MacroMainSequence(file):

    # Reads Macro Sequence File and process it
    # line starts with & means start of sub-sequence, which all operation is wrapped with.
    # Any failure inside it skips sub-sequence as latter part of it become useless.
    # spl[0] = image / [1] = operation mode / [2] = pre_delay / [3] = max waiting time
    # Operation Mode 0: Search only / 1: Search and Click / 2: 1 with failure acceptance
    #                3: Custom Action written in CustomAction.py

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

                    if len(spl) < 4:
                        pos = ImgSearchArea(spl[0], i)
                    else:
                        pos = ImgSearchArea(spl[0], i, int(spl[2]), int(spl[3]))

                except cv2.error:
                    print('At Line', i, spl[0], 'does not exist!!')
                    print('Script shutdown in 10 seconds.')
                    time.sleep(10)
                    sys.exit()

                # Operation Mode Start

                else:

                    if pos[0] == -1:

                        if spl[0] == '0' or spl[0] == '1':
                            break

                        elif spl[0] == '2':
                            continue

                        else:
                            print('wrong index is given in file.')

                    else:

                        if spl[0] == '1':
                            pyautogui.click(pos)


def GetFileInfo():
    print('Input Macro file name with .txt extension.')
    print('Leave it blank and press enter to auto-load macro1.txt')

    file_name = input("File Name: ")
    if file_name is '':
        file_name = 'macro1.txt'

    global lines

    with open(file_name, 'r', encoding='utf-8') as f:
        lines = sum(1 for _ in f)

    return file_name


def main():
    GetWindowPoint_INFORM()
    GetWindowPoint(killkey)

    seq_file = GenerateMacroStep.FileAvailable(GetFileInfo())

    MacroMainSequence(seq_file)





# ---------------------------------------------------------------


main()
