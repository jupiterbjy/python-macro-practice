import pyautogui

import ImgWrapper
import KillProcess

# Write Custom action and set Op Mode to 3 4 5 6
# Not sure if I can import file that is importing this file.
# If it does, these can basically do everything.


def CustomAction1(img_result):

    # TODO: Test out this custom function

    # ----------------------------------------------------------
    # deals with chara not existing in visible row

    def ScrollDown(num):
        p_a = ImgWrapper.ImgSearchArea("./CoreImage/CharaOffset.png", "C_Action1")
        p_b = [p_a[0], p_a[1]+65]
        for _ in range(num - 1):
            pyautogui.dragTo(p_b, p_a)

    # ----------------------------------------------------------
    # select preset, only Preset1 Preset2 exists

    def PresetLoader(preset):
        tgt = ["1.png", "2.png", "3.png", "4.png", "5.png"]
        if preset == 1:
            imgdir = "./Preset1"
        else:
            imgdir = "./Preset2"

        out = []
        for i in tgt:
            out.append(",".join([imgdir, i]))

        return out

    # ----------------------------------------------------------
    # I really don't like PEP8's line spacing limit. It hurts visibility or mybad

    print('Pricone Character select Function Start')

    leader_pos = [img_result[0] + 600, img_result[1] + 94]

    # Clear out selected chara

    for _ in range(5):
        pyautogui.click(leader_pos)

    # Start Scanning for chara

    found = [0, 0, 0, 0, 0]
    row = 0
    img_dir = PresetLoader(2)

    while True:
        print("Row", row, "scanning")

        while True:
            # index looks so convenient, wow.. did C had one of these?
            a = found.index(0)

            if found[a] == 0:
                pos = ImgWrapper.ImgSearchArea(img_dir[0], "C_Action1", 1, 2, True)

                if pos[0] != -1:
                    continue
                else:
                    pyautogui.click(pos)
                    found[a] = 1

        if 0 in found:

            if row < 5:
                row = row + 1
                ScrollDown(1)

            else:
                print("Could not find target character")
                KillProcess.PressKill()
        else:
            print("All Selected")
            break


def CustomAction2(img_result):
    print('CustomAction2')


def CustomAction3(img_result):
    print('CustomAction3')


def CustomAction4(img_result):
    print('CustomAction4')