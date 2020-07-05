import os
import sys


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


class PathData:
    MAIN_LOCATION = __file__
    ABS_PATH = os.path.abspath(MAIN_LOCATION)
    BASE_PATH = os.path.dirname(ABS_PATH)

    @classmethod
    def setRelativePath(cls, script_location):
        cls.MAIN_LOCATION = script_location
        cls.ABS_PATH = os.path.abspath(script_location)
        cls.BASE_PATH = os.path.dirname(cls.ABS_PATH)

    # https://stackoverflow.com/questions/7674790
    @classmethod
    def pyinstaller_onefile(cls, relative_path):
        base = getattr(sys, "_MEIPASS", cls.ABS_PATH)
        return os.path.join(base, relative_path)

    @classmethod
    def relative(cls, relative_path):
        return os.path.join(cls.BASE_PATH, relative_path)


def IsFrozen():
    """
    Checks whether Python instance is Frozen(aka onefile) or not.
    :return: Returns True-False according to frozen state.
    """
    if getattr(sys, "frozen", False):
        return True

    file_dir = os.path.dirname(sys.argv[0])

    # Fail-safe
    try:
        os.chdir(file_dir)
    except OSError:
        pass
    return False
