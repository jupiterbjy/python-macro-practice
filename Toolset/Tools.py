
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
        file_name = fileNameExtract(file_dir)

        try:
            temp = cv2.imread(file_dir, 0)
        except cv2.error as err:
            return False
        else:
            if temp.size == 0:
                return False
            return True
