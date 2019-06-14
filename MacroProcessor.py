from colorama import init, Fore, Style
import cv2
import pyautogui

import CustomAction
import KillProcess
import ImgWrapper


init(convert=False, strip=False)


def MainSequence(coord_1, coord_2, file):

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

                # Will consider trailing '&' after Line process as end of Sub-Sequence

                i = i + 1

                # TODO: Fix IndexOutOfRange After Failing Image Search

                if '&' in file[i]:
                    break
                elif '#' in file[i]:
                    continue

                spl = file[i].split()

                print(Fore.LIGHTBLACK_EX, spl, Style.RESET_ALL, sep='')

                try:

                    if len(spl) == 2:
                        pos = ImgWrapper.ImgSearchArea(coord_1, coord_2, [0], i)

                    elif len(spl) == 3:
                        pos = ImgWrapper.ImgSearchArea(coord_1, coord_2, spl[0], i, int(spl[2]))

                    else:
                        pos = ImgWrapper.ImgSearchArea(coord_1, coord_2, spl[0], i, int(spl[2]), int(spl[3]))

                except cv2.error:
                    print('At Line', i, spl[0], 'does not exist!!')
                    KillProcess.PressKill()

                # Operation Mode Start

                else:

                    if spl[1] == '3':
                        CustomAction.CustomAction1(pos)

                    elif spl[1] == '4':
                        CustomAction.CustomAction2(pos)

                    elif spl[1] == '5':
                        CustomAction.CustomAction3(pos)

                    elif spl[1] == '6':
                        CustomAction.CustomAction4(pos)

                    elif pos[1] == -1:

                        if spl[1] == '0' or spl[1] == '1':
                            while True:
                                i = i + 1
                                if '&' in file[i]:
                                    break

                        elif spl[1] == '2':
                            continue

                        else:
                            print(Fore.RED, 'wrong index is given in file!', Style.RESET_ALL, sep='')
                            KillProcess.PressKill()
                    else:

                        if spl[1] == '1':
                            print(' - click on', pos)
                            pyautogui.click(pos)
