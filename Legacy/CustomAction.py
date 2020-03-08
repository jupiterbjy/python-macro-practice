import pyautogui
import time

from Legacy import ImgWrapper as Iw, KillProcess


# Write Custom action and set Op Mode to 3 4 5 6


def CustomAction1(img_result):
    print('\n<< CustomAction1 >>')
    CharaSelect(img_result, 1)


def CustomAction2(img_result):
    print('\n<< CustomAction2 >>')
    CharaSelect(img_result, 2)


def CustomAction3(img_result):
    print('\n<< CustomAction3 >>')


def CustomAction4(img_result):
    print('\n<< CustomAction4 >>')


'''
# ----------------------------------------------------------

#   Write Function to be used in Custom actions below here

# ----------------------------------------------------------
'''


# ----------------------------------------------------------
# Only For CERTAIN GAME.
# deals with chara not existing in visible row
# Only hardcoded for 1280*720 for now, will make it free-scale if I have time later.

def ScrollDown():
    global p_a, p_b
    print("Scrolling Down")

    try:
        p_a[0]
    except NameError:
        p_a = Iw.ImgSearchArea("./CoreImage/CharaOffset.png")
        p_a[0] = p_a[0] - 430
        p_a[1] = p_a[1] - 25
        p_b = [p_a[0], p_a[1] - 300]

    pyautogui.moveTo(p_a)
    pyautogui.dragTo(p_b[0], p_b[1], 0.5)


# ----------------------------------------------------------
# Only For CERTAIN GAME.
# Selects preset, only Preset1 Preset2 exists
# Appends corresponding list to 'out'. Not sure just copying list to other list works.

def PresetLoader(preset):
    tgt = ["1.png", "2.png", "3.png", "4.png", "5.png"]
    if preset == 1:
        imgdir = "./Preset1"
    else:
        imgdir = "./Preset2"

    out = []
    for I in tgt:
        out.append("/".join([imgdir, I]))

    return out


# ----------------------------------------------------------
# Only For CERTAIN GAME.
# Clears out characters if exists.
# Will Scan blank areas and don't click more than needed.

def CharaClear(pos):
    # Clear out selected chara

    blanks = Iw.ScanOccurrence('./CoreImage/Blank.png')
    print(blanks)
    for _ in range(5-blanks):
        time.sleep(0.3)
        pyautogui.click(pos)


# ----------------------------------------------------------
# Only For CERTAIN GAME.
# Selects Characters Based on PresetLoader.
# Will use list 'found' as checklist to see which image is found or not.
# If Some images are not found from 'target_list' list, will scroll down and search again.

def CharaSelect(img_pos, preset):
    print('Pricone Character select Function Start')

    leader_pos = [img_pos[0] + 184, img_pos[1] + 81]
    CharaClear(leader_pos)

    # Start Scanning for chara

    found = [0, 0, 0, 0, 0]
    row = 0
    target_list = PresetLoader(preset)

    while True:
        print("Row", row, "scanning")

        for i in range(5):

            if found[i] == 0:
                pos = Iw.ImgSearchArea(target_list[i], 0.3, 1, True)

                if pos[0] == -1:
                    continue
                else:
                    pyautogui.click(Iw.RandomOffset(pos, 5))
                    time.sleep(0.1)
                    found[i] = 1
            else:
                continue

        if 0 in found:

            if row < 5:
                row = row + 1
                ScrollDown()
                time.sleep(0.2)

            else:
                print("Could not find target character")
                KillProcess.PressKill()
        else:
            print("All Selected")
            break


# I really don't like PEP8's line spacing limit. It hurts visibility or well.. my bad.
# Sometimes it looks good tho.
# ----------------------------------------------------------
