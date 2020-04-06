import sys
import os


def IsFrozen(change_dir=True):
    """
    Checks whether Python instance is Frozen(aka onefile) or not.
    :param change_dir: If true, will set working directory where exe is.
    :return: Returns True-False according to frozen state.
    """
    if getattr(sys, 'frozen', False):
        if change_dir:
            try:
                os.chdir(os.path.dirname(sys.executable))
            except WindowsError as we:
                print(we)
        return True

    file_dir = os.path.dirname(sys.argv[0])
    # Fail-safe in terminal path showing relative path.
    try:
        os.chdir(file_dir)
    except OSError:
        print('In relative path')
    return False


MAIN_LOCATION = __file__


# https://stackoverflow.com/questions/7674790
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(MAIN_LOCATION)))
    return os.path.join(base_path, relative_path)


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

    print(out + ':')
