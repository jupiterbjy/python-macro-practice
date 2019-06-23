
from colorama import init, Fore, Style
import pyautogui
import keyboard
import time
import os

import GlobalVar
import MacroProcessor
import GenerateMacroStep
import KillProcess


def DetectFrozen():
    # From PyInstaller Run-Time Information
    import sys
    if getattr(sys, 'frozen', False):
        # One-file
        SetWorkingDirectory(GetExecutablePath())
    else:
        # .py mode
        print("!! DEBUG MODE")


def SetWorkingDirectory(exe_dir):
    tmp = exe_dir.split('\\')
    tmp[-1] = ''
    path = '\\'.join(tmp)
    os.chdir(path)


def GetExecutablePath():
    # https://github.com/pyinstaller/pyinstaller/issues/1726#issuecomment-166146333

    from sys import executable
    base_dir = executable

    return base_dir


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


def GetWindowPoint(kill_key):
    global trigger

    trigger = True

    while trigger:

        GlobalVar.x, GlobalVar.y = GetMousePos(kill_key)
        print("Pos1:", GlobalVar.x, GlobalVar.y)
        BreakKeyInput(kill_key)

        GlobalVar.x2, GlobalVar.y2 = GetMousePos(kill_key)
        print("Pos2:", GlobalVar.x2, GlobalVar.y2)
        BreakKeyInput(kill_key)

        print("Area:", abs(GlobalVar.x - GlobalVar.x2), "*", abs(GlobalVar.y - GlobalVar.y2))

        if abs(GlobalVar.x - GlobalVar.x2) < 1280 or abs(GlobalVar.y - GlobalVar.y2) < 720:

            print("\nDesignated Size is smaller than 1280*720!!")
            print("Try again!\n")

        else:
            trigger = False

        if (GlobalVar.x2 - GlobalVar.x) < 0:       # pos1 = is right side?
            temp = [GlobalVar.x2, GlobalVar.y2]

            GlobalVar.x2 = GlobalVar.x
            GlobalVar.y2 = GlobalVar.y

            GlobalVar.x = temp[0]
            GlobalVar.y = temp[1]

            print("Swapping Pos1 & Pos2 for imgsrch.py")


def GetWindowPoint_INFORM():
    init(convert=False, strip=False)                 # colorama initialization

    print(Fore.RED + '\n  +', Style.RESET_ALL, end='', sep='')
    print("___________________ ")
    print("   |                 | ")
    print("   |                 | ")
    print("   |     N  O  X     | ")
    print("   |                 | ")
    print("   |                 | ")
    print("   ￣￣￣￣￣￣￣￣￣￣", end='', sep='')
    print(Fore.RED + '+\n', Style.RESET_ALL)

    print("Press", GlobalVar.halt_key, "While pointing indicated points\n")


def GetFileInfo():
    print('\nInput Macro file name with .txt extension.')
    print('Leave it blank and press enter to auto-load macro1.txt')

    file_name = input("File Name: ")
    if file_name is '':
        file_name = 'macro1.txt'

    '''
    global lines

    with open(file_name, 'r', encoding='utf-8') as f:
    lines = sum(1 for _ in f)
    '''

    return file_name


def main():
    DetectFrozen()
    GetWindowPoint_INFORM()
    GetWindowPoint(GlobalVar.halt_key)

    seq_file = GenerateMacroStep.FileAvailable(GetFileInfo(), 'open')
    while seq_file == -1:
        seq_file = GenerateMacroStep.FileAvailable(GetFileInfo(), 'open')

    MacroProcessor.MainSequence(seq_file)

    print('\nScript Ended.')
    KillProcess.PressKill()


# ---------------------------------------------------------------

main()          # Looks so sad!
