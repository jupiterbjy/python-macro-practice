
def fileNameExtract(location):
    return (location.split('/'))[-1]


def fileOpen(loc, mode='rt'):
    try:
        f = open(loc, mode)

    except FileNotFoundError:
        print()
    else:
        return f


def arrSwap(arr, idx1, idx2):
    arr[idx1], arr[idx2] = arr[idx2], arr[idx1]


def imageCheck(file_dir):
    import cv2      # Performance issue, but this is portable.

    if file_dir[0] != '':
        # file_name = fileNameExtract(file_dir)

        try:
            temp = cv2.imread(file_dir, 0)
        except cv2.error as err:
            return False
        else:
            if temp.size == 0:
                return False
            return temp


def nameCaller(color=None):
    # https://stackoverflow.com/a/5067654/10909029
    # print(inspect.stack()[0][3]) <- this prints current stack's name
    from inspect import stack
    from Toolset.TextTools import QtColorize

    caller = stack()[1][3]

    if color:
        out = QtColorize(caller, color)
    else:
        out = caller

    print(out + ':')
