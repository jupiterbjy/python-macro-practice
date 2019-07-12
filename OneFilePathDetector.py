import os
'''
Run DetectFrozen() to set your working directory depending on 'frozen' state.
in other words, whether used --onefile in pyinstaller or not.
If file is running as onefile.exe, will return 1 otherwise 0.

SetWorkingDirectory() will rip trailing 'filename.exe' to get a directory
which it received from GetExecutablePath() and set as working directory.
'''


def DetectFrozen():
    # From PyInstaller Run-Time Information
    import sys
    if getattr(sys, 'frozen', False):
        # One-file
        SetWorkingDirectory(GetExecutablePath())
        return 1

    else:
        return 0


def SetWorkingDirectory(exe_dir):
    tmp = exe_dir.split('\\')
    tmp[-1] = ''
    path = '\\'.join(tmp)
    os.chdir(path)


def GetExecutablePath():
    # https://github.com/pyinstaller/pyinstaller/issues/1726#issuecomment-166146333

    from sys import executable
    base_dir = executable

    return base_dir
