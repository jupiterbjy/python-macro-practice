from colorama import init, Fore, Style
import cv2
import pyautogui
import time

import CustomAction as Ca
import KillProcess
import ImgWrapper as Iw

init(convert=False, strip=False)

# TODO: spilt MainSequence into multiple smaller sub-modules


def MainSequence(file):

    # Reads Macro Sequence File and process it
    # line starts with & means start of sub-sequence, which all operation is wrapped with.
    # Any failure inside it skips sub-sequence as latter part of it become useless.
    # spl[0] = image / [1] = operation mode / [2] = pre_delay / [3] = max waiting time
    # Operation Mode 0: Search only / 1: Search and Click / 2: 1 with failure acceptance
    #                3 4 5 6: Custom Action written in CustomAction.py

    for i in range(len(file) - 1):

        if '@' in file[i] or '#' in file[i]:
            continue

        # Sub-Sequence Start

        elif '&' in file[i]:

            # Sub-Sequence Loop START!!
            # Saving i value temporally

            temp = i

            seq_line = file[i].split()
            try:
                loop = int(seq_line[2])
            except IndexError:
                print('No Loop indicator found at Sub-Sequence', seq_line[1])
                print('Considering loop count as 1.')

                loop = 1

            while True:
                last_img = ''
                i = temp

                print("Sub-Sequence", seq_line[1], "Start")

                # Line process Start

                while True:

                    # One-Time trigger for fail-safe - when game didn't recognize click

                    global failsafe
                    failsafe = False

                    # Will consider trailing '%' after Line process as end of Sub-Sequence
                    # Consider '#' as comment

                    i = i + 1

                    # Fix IndexOutOfRange After Failing Image Search
                    # Possibly fixed

                    try:
                        if '%' in file[i]:
                            break
                        elif '#' in file[i]:
                            continue

                    except IndexError:
                        print('End of File reached.')
                        KillProcess.PressKill()

                    spl = file[i].split()

                    print(Fore.LIGHTBLACK_EX, spl, Style.RESET_ALL, sep='')

                    try:
                        # any way to pass array directly to function as argument?
                        print('Line', i)

                        if len(spl) == 2:
                            pos = Iw.ImgSearchArea([0])

                        elif len(spl) == 3:
                            pos = Iw.ImgSearchArea(spl[0], float(spl[2]))

                        else:
                            pos = Iw.ImgSearchArea(spl[0], float(spl[2]), float(spl[3]))

                    except cv2.error:
                        print('!! At Line', i, spl[0], 'does not exist.')
                        print('!! Please check if image name and directory is correct.')
                        KillProcess.PressKill()

                    # Operation Mode Start
                    # TODO: test out fail safe

                    else:

                        if pos[1] == -1:
                            if failsafe or last_img == '':
                                if spl[1] == '0' or spl[1] == '1':
                                    while i < len(file):
                                        i = i + 1
                                        if '%' in file[i]:
                                            break
                                elif spl[1] == '2':
                                    continue

                                else:
                                    print(Fore.RED, 'Wrong index is given in file!', Style.RESET_ALL, sep='')
                                    KillProcess.PressKill()
                                    
                            else:
                                failsafe = True

                                pos_re = Iw.ImgSearchArea(last_img, 'failsafe')
                                if pos_re[0] != -1:
                                    pyautogui.click(pos_re)
                                else:
                                    i = i - 1
                                    continue

                        elif spl[1] == '3':
                            Ca.CustomAction1(pos)

                        elif spl[1] == '4':
                            Ca.CustomAction2(pos)

                        elif spl[1] == '5':
                            Ca.CustomAction3(pos)

                        elif spl[1] == '6':
                            Ca.CustomAction4(pos)

                        else:

                            if spl[1] == '1':
                                last_img = spl[0]
                                pos = Iw.RandomOffset(pos, 5)
                                time.sleep(0.2)
                                print(' - click on', pos)
                                pyautogui.click(pos)

                # If file Sequence has negative value for loop argument, loop until failure.

                if loop < 0:
                    continue
                elif loop == 1:
                    break
                else:
                    loop = loop - 1
                    continue
