
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
from PIL.ImageQt import ImageQt
import sys
import pyautogui
import keyboard

from Toolset import Tools
from Toolset.Tools import nameCaller
from Toolset.TextTools import QtColorize
from ImageModule import Pos, Area

"""
Module to store all necessary Qt-Related tools.
"""

IMG_CONVERT = (226, 151, Qt.KeepAspectRatio)
ICON_LOCATION = './icons/methods/'
ICON_ASSIGN = {
    'Click': 'click.png',
    'Loop': 'loop.png',
    'sLoopEnd': 'loopEnd.png',
    'sLoopStart': 'loopStart.png',
    'ImageSearch': 'imageSearch.png',
    'Variable': 'variable.png',
    'Wait': 'wait.png',
    'default': 'template.png',
    'SearchOccurrence': 'count.png',
}


class StdoutRedirect(QObject):
    # Codes from below.
    # https://4uwingnet.tistory.com/9

    printOccur = pyqtSignal(str, name="print")

    def __init__(self):
        QObject.__init__(self, None)
        self.daemon = True
        self.sys_stdout = sys.stdout.write
        self.sys_stderr = sys.stderr.write

    def stop(self):
        sys.stdout.write = self.sys_stdout
        sys.stderr.write = self.sys_stderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg: self.write(msg)

    def write(self, s):
        sys.stdout.flush()
        self.printOccur.emit(s)


# https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
class SeqItemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.textLayOut = QVBoxLayout()
        self.textUpLabel = QLabel()
        self.textDownLabel = QLabel()
        self.textLayOut.addWidget(self.textUpLabel)
        self.textLayOut.addWidget(self.textDownLabel)
        self.allHBoxLayOut = QHBoxLayout()
        self.iconLabel = QLabel()
        self.iconLabel.setMinimumSize(QSize(48, 48))
        self.iconLabel.setMaximumSize(QSize(48, 48))
        self.allHBoxLayOut.addWidget(self.iconLabel)
        self.allHBoxLayOut.addLayout(self.textLayOut, 1)
        self.setLayout(self.allHBoxLayOut)

        self.textUpLabel.setStyleSheet('''
                    color: rgb(0, 0, 255);
                ''')
        self.textDownLabel.setStyleSheet('''
                    color: rgb(255, 0, 0);
                ''')

    def setup(self, t_up, t_down, img_path):
        self.textUpLabel.setText(t_up)
        self.textDownLabel.setText(t_down)
        self.iconLabel.setPixmap(setPix(img_path))
        self.iconLabel.setScaledContents(True)


class MethodItemWidget(QWidget):
    def __init__(self, img_path, name):
        super().__init__()
        self.methodLayout = QGridLayout()

        self.itemIcon = QLabel()
        self.itemIcon.setMinimumSize(QSize(24, 24))
        self.itemIcon.setMaximumSize(QSize(24, 24))
        self.itemIcon.setPixmap(setPix(img_path))
        self.itemIcon.setScaledContents(True)
        self.methodLayout.addWidget(self.itemIcon, 0, 0, 1, 1)

        self.itemName = QLabel()
        self.itemName.setText(name)
        self.methodLayout.addWidget(self.itemName, 0, 1, 1, 1)
        self.setLayout(self.methodLayout)


def setPix(image):
    if isinstance(image, str):
        return QPixmap(image)
    else:
        tmp = ImageQt(image).copy()     # Plain ImageQt() call don't return QImage.
        # TransformMode => Qt::SmoothTransformation for better quality is possible.
        return QPixmap(tmp)


def loadImage(self):
    nameCaller()

    file_dir = QFileDialog.getOpenFileName(self)[0]
    file_name = Tools.fileNameExtract(file_dir)

    if not file_dir:
        print('└ Canceled')
        return False

    try:
        img = Image.open(file_dir)

    except NameError:
        print(f'└ {file_name} not found.')
        return None, None

    except Image.UnidentifiedImageError:
        print(f'└ {file_name} is not image.')
        return None, None

    else:
        return img, file_name


def GenerateWidget(tgt):
    img = ICON_ASSIGN.setdefault(type(tgt).__name__, 'default')

    item = SeqItemWidget()
    item.setup(tgt.name, str(type(tgt).__name__ + 'Object'), ''.join([ICON_LOCATION, img]))

    return item


def AddToListWidget(tgt, item_list_widget):
    """
    Adds macro object to given QItemListWidget.
    :param tgt: macro object to Add
    :param item_list_widget: QItemListWidget
    """
    nameCaller((100, 100, 100))

    print(f'└ Add: {type(tgt).__name__} "{QtColorize(tgt.name, (0, 217, 127))}"')

    item = GenerateWidget(tgt)

    list_item = QListWidgetItem(item_list_widget)
    list_item.setSizeHint(item.sizeHint())

    item_list_widget.addItem(list_item)
    item_list_widget.setItemWidget(list_item, item)


TIMER_RUNNING = []


def AbortTimers():
    for timer in TIMER_RUNNING:
        timer.stop()


def QSleep(delay, output=False):
    # https://stackoverflow.com/questions/21079941
    # https://stackoverflow.com/questions/41309833

    def wait():
        # loop = QEventLoop()
        # QTimer.singleShot(delay * 1000, loop.quit)
        # loop.exec_()

        timer = QTimer()
        timer.setSingleShot(True)
        # timer.timeout.connect()
        TIMER_RUNNING.append(timer)
        timer.start(delay * 1000)

    class context:
        def __enter__(self):
            nameCaller()
            print(f'└ Wait {delay} start')

        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f'└ Finish')

    if output:
        with context():
            wait()

    else:
        wait()


def getCaptureArea():
    p1 = Pos()
    p2 = Pos()
    kill_key = 'f2'

    class breakKeyInput:
        # Delays until key is up, to prevent next input skipping.
        def __enter__(self):
            nameCaller()
            print(f'└ Waiting for press:{kill_key}')

            while not keyboard.is_pressed(kill_key):
                QSleep(0.05)

        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f'└ Waiting for release:{kill_key}')

            while keyboard.is_pressed(kill_key):
                QSleep(0.05)

    def getPos(p):
        nonlocal kill_key

        with breakKeyInput():
            p.set(*pyautogui.position())

    getPos(p1)
    getPos(p2)

    return Area.fromPos(p1, p2)


def appendText(text_edit, msg, newline=True):
    text_edit.moveCursor(QTextCursor.End)
    text_edit.insertHtml(msg + '<br>' if newline else msg)
    QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)


def returnRow(q_list):
    """
    Simple Wrapper for QListWidget.currentRow().
    Qt consider -1 as false, but List count it as last element. So this exist.
    :param q_list: QListWidgetItem
    """
    try:
        row = q_list.currentRow()
    except AttributeError:
        raise AttributeError(f'Expected QListWidget, got {type(q_list)}.')

    else:
        if row == -1:
            raise IndexError('Nothing Selected.')
        else:
            return row
