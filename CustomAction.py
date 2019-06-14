import pyautogui

import ImgWrapper

# Write Custom action and set Op Mode to 3 4 5 6
# Not sure if I can import file that is importing this file.
# If it does, these can basically do everything.


def CustomAction1(img_result):
    print('Pricone Charactor select Function')

    leader_pos = [img_result[0] + 600, img_result[1] + 94]

    # Clear out selected chara
    for _ in range(5):
        pyautogui.click(leader_pos)


def CustomAction2(img_result):
    print('CustomAction2')


def CustomAction3(img_result):
    print('CustomAction3')


def CustomAction4(img_result):
    print('CustomAction4')