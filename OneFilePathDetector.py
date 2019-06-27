import os


def DetectFrozen():
    # From PyInstaller Run-Time Information
    import sys
    if getattr(sys, 'frozen', False):
        # One-file
        SetWorkingDirectory(GetExecutablePath())
    else:
        # .py mode
        print("!! DEBUG MODE")


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
