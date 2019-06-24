import pyautogui
import time

import ImgWrapper
import KillProcess

# Write Custom action and set Op Mode to 3 4 5 6
# Not sure if I can import file that is importing this file.
# If it does, these can basically do everything.


def CustomAction1(img_result):
    print('CustomAction1')
    CharaSelect(img_result, 1)


def CustomAction2(img_result):
    print('CustomAction2')
    CharaSelect(img_result, 2)


def CustomAction3(img_result):

    print('CustomAction3')


def CustomAction4(img_result):
    print('CustomAction4')


# --------------------------------------------------
# Write Function used in Custom actions bellow here
# -------------------------------------------------

# ----------------------------------------------------------
# deals with chara not existing in visible row

def ScrollDown():
    global p_a, p_b
    print("Scrollin' Down")

    try:
        p_a[0]
    except NameError:
        p_a = ImgWrapper.ImgSearchArea("./CoreImage/CharaOffset.png", "C_Action1")
        p_a[0] = p_a[0] - 430
        p_a[1] = p_a[1] - 25
        p_b = [p_a[0], p_a[1] - 342]

    pyautogui.moveTo(p_a)
    pyautogui.dragTo(p_b[0], p_b[1], 0.5)

# ----------------------------------------------------------
# select preset, only Preset1 Preset2 exists


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


def CharaSelect(img_pos, preset):
    print('Pricone Character select Function Start')

    leader_pos = [img_pos[0] + 184, img_pos[1] + 81]

    # Clear out selected chara

    for _ in range(5):
        pyautogui.click(leader_pos)
        time.sleep(0.1)

    # Start Scanning for chara

    found = [0, 0, 0, 0, 0]
    row = 0
    img_dir = PresetLoader(preset)

    while True:
        print("Row", row, "scanning")

        for i in range(5):

            if found[i] == 0:
                pos = ImgWrapper.ImgSearchArea(img_dir[i], "C_Action1", 0.3, 1, True)

                if pos[0] == -1:
                    continue
                else:
                    pyautogui.click(ImgWrapper.RandomOffset(pos, 5))
                    found[i] = 1
            else:
                continue

        if 0 in found:

            if row < 5:
                row = row + 1
                ScrollDown()

            else:
                print("Could not find target character")
                KillProcess.PressKill()
        else:
            print("All Selected")
            break


# I really don't like PEP8's line spacing limit. It hurts visibility or mybad.
# ----------------------------------------------------------
