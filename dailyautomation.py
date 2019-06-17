
from colorama import init, Fore, Style
import pyautogui
import keyboard
import time
import os
import sys

import MacroProcessor
import GenerateMacroStep
import KillProcess

halt_key = 'f2'


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
        print('', end='\r')

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

    print("Press", halt_key, "While pointing indicated points\n")


def GetFileInfo():
    print('Input Macro file name with .txt extension.')
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
    GetWindowPoint_INFORM()
    GetWindowPoint(halt_key)

    seq_file = GenerateMacroStep.FileAvailable(GetFileInfo(), 'open')
    while seq_file == -1:
        seq_file = GenerateMacroStep.FileAvailable(GetFileInfo(), 'open')

    MacroProcessor.MainSequence(Pos1, Pos2, seq_file)

    print('\nScript Ended.')
    KillProcess.PressKill()


# ---------------------------------------------------------------

main()
