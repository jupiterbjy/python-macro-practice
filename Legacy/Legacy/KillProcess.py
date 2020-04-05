from colorama import init, Fore, Style
import sys
import keyboard
import time

'''
PressKill() will stop process when designated key is pressed.

CountKill() Counts before finishing process.
Originally CountKill() had counter function but thought it was unnecessary and removed it. 
'''


def PressKill(key='f2'):
    init(convert=False, strip=False)
    print(Style.RESET_ALL, sep='', end='')
    print(Fore.CYAN, 'Press ', Fore.RED, key, Fore.CYAN, ' to kill script!', Style.RESET_ALL, sep='')

    while not keyboard.is_pressed(key):
        time.sleep(0.05)

    print('\nGoodBye!')
    time.sleep(2)
    sys.exit()


def CountKill(delay=10):
    init(convert=False, strip=False)
    print(Style.RESET_ALL, sep='', end='')
    print(Fore.CYAN, 'Script shutdown in', Style.RESET_ALL, sep='', end='')

    for i in range(delay):
        print(delay - i, end='')
        time.sleep(0.95)
        print('\b' * len(str(delay - i)), end='', flush=True)

    print('\nGoodBye!')
    time.sleep(2)
    sys.exit()
