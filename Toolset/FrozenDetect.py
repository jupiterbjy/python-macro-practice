import os
import sys
'''
Run DetectFrozen() to set your working directory depending on 'frozen' state.
in other words, whether used --onefile in pyinstaller or not.
If file is running as onefile.exe, will return 1 otherwise 0.

SetWorkingDirectory() will rip trailing 'filename.exe' to get a directory
which it received from GetExecutablePath() and set as working directory.
'''


def IsFrozen(change_dir=True):
    """
    Checks whether Python instance is Frozen(aka onefile) or not.
    :param change_dir: If true, will set working directory where exe is.
    :return: Returns True-False according to frozen state.
    """
    if getattr(sys, 'frozen', False):
        if change_dir:
            SetWorkingDirectory(sys.executable)
        return True
    else:
        file_dir = os.path.dirname(sys.argv[0])
        # Fail-safe in terminal path showing relative path.
        try:
            os.chdir(file_dir)
        except OSError:
            print('In relative path')
        return False


def SetWorkingDirectory(directory):
    """
    Set Working directory to parameter.
    :param directory: Name explains.
    :return: returns nothing.
    """
    tmp = directory.split('\\')[:-1]
    os.chdir('\\'.join(tmp))
