import cv2
import os
import pyautogui as pgui


def saveImg():
    """
    Save Image with ascending ordered numeric names.
    :return:
    """
    order = 0

    def save(file, name=None, overwrite=True):
        nonlocal order

        if name is None:
            name = str(order) + '.png'

        if overwrite:
            while os.path.isfile(name):
                print(f'File "{name}" already exists. Renaming. ')
                name = name.split('.')[0] + '_' + '.png'

        cv2.imwrite(name + '.png', file)

        order += 1

    return save


def ScreenShotArea(pos1, pos2):
    """
    Takes a screenshot of area as a file-like object. (probably)
    Will get position of target with 2 lists or tuples containing xy coordinates.
    """
    return pgui.screenshot(region=(*pos1, pos1[1], pos2[0] - pos1[0], pos2[1] - pos1[1]))

