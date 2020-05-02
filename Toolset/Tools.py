import sys
import os

"""
Stores Mostly one-time use functions separated from used sources.
"""


def IsFrozen():
    """
    Checks whether Python instance is Frozen(aka onefile) or not.
    :param change_dir: If true, will set working directory where exe is.
    :return: Returns True-False according to frozen state.
    """
    if getattr(sys, "frozen", False):
        return True

    file_dir = os.path.dirname(sys.argv[0])
    # Fail-safe in terminal path showing relative path.
    try:
        os.chdir(file_dir)
    except OSError:
        pass
    return False


class PathData:
    MAIN_LOCATION = __file__
    ABS_PATH = os.path.abspath(MAIN_LOCATION)
    BASE_PATH = os.path.dirname(ABS_PATH)

    @staticmethod
    def setRelativePath(script_location):
        PathData.MAIN_LOCATION = script_location
        PathData.ABS_PATH = os.path.abspath(script_location)
        PathData.BASE_PATH = os.path.dirname(PathData.ABS_PATH)

    # https://stackoverflow.com/questions/7674790
    @staticmethod
    def pyinstaller_onefile(relative_path):
        base = getattr(sys, "_MEIPASS", PathData.ABS_PATH)
        return os.path.join(base, relative_path)

    @staticmethod
    def relative(relative_path):
        return os.path.join(PathData.BASE_PATH, relative_path)


def nameCaller(color=None, raw=False):
    # https://stackoverflow.com/a/5067654/10909029
    # print(inspect.stack()[0][3]) <- this prints current stack's name

    from inspect import stack
    from Toolset.TextTools import QtColorize

    caller = stack()[1][3]

    if raw:
        print(caller)
        return

    if color:
        out = QtColorize(caller, color)
    else:
        out = caller

    print(out + ":")
