from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, QObject, Signal, QSize, QTimer, QEventLoop
from PySide2.QtWidgets import (
    QFileDialog,
    QListWidgetItem,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout,
)
from PIL import Image, ImageQt
from datetime import datetime
import os
import sys
import logging
import pyautogui
import keyboard

from Toolset.Tools import PathData
from Toolset.ImageModule import Pos, Area

# Module to store all necessary Qt-Related tools for UI.
# Module dependency is getting out of control.

TIMER_RUNNING = []
LOOP_RUNNING = []
ABORT_SIGNALED = False

ABOUT_IMAGE = "About.png"
IMG_CONVERT = (226, 151, Qt.KeepAspectRatio)

ICON_LOCATION = "icons/"
ICON_ASSIGN = {
    "Click": "click.png",
    "Drag": "drag.png",
    "Loop": "loop.png",
    "LoopEnd": "loopEnd.png",
    "LoopStart": "loopStart.png",
    "ImageSearch": "imageSearch.png",
    "Variable": "variable.png",
    "Wait": "wait.png",
    "default": "template.png",
    "SearchOccurrence": "count.png",
}


class StdoutRedirect(QObject):
    # Based off from below.
    # https://4uwingnet.tistory.com/9

    printOccur = Signal(str, name="print")

    def __init__(self):
        QObject.__init__(self, None)
        self.daemon = True
        self.sys_stdout = sys.stdout
        self.sys_stderr = sys.stderr

    def stop(self):
        sys.stdout = self.sys_stdout
        sys.stderr = self.sys_stderr

    def start(self):
        sys.stdout = self.write
        sys.stderr = self.write

    def write(self, s):
        sys.stdout.flush()
        self.printOccur.emit(s)


class LoggingEmitSignal(QObject):
    signal = Signal(str)


class LoggingEmitter:
    """Supportive class to wrap logging call to emit signals."""

    signal = LoggingEmitSignal()
    logger = logging.getLogger()
    levels = ["debug", "info", "warning", "critical"]

    @classmethod
    def log(cls, *texts, level=0):
        """Level 0 ~ 3 respectively DEBUG, INFO, WARNING, CRITICAL."""

        text = " ".join(map(str, texts))
        log_target = getattr(cls.logger, cls.levels[level])

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        str_lvl = cls.levels[level].upper()
        log_target(text)
        cls.signal.signal.emit(f"{date} - {str_lvl} - {text}\n")

    @classmethod
    def debug(cls, *texts):
        cls.log(*texts)

    @classmethod
    def info(cls, *texts):
        cls.log(*texts, level=1)

    @classmethod
    def warning(cls, *texts):
        cls.log(*texts, level=2)

    @classmethod
    def critical(cls, *texts):
        cls.log(*texts, level=3)

    @classmethod
    def setLogger(cls, new_logger):
        try:
            new_logger.debug("Logger passed to LoggingEmitter.")
        except AttributeError:
            cls.logger.critical(f"Received object is NOT a Logger.")
            raise AttributeError(f"Received object is NOT a Logger, but {type(new_logger)}.")
        else:
            cls.logger = new_logger


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

        self.textUpLabel.setStyleSheet("""color: rgb(0, 0, 255);""")
        self.textDownLabel.setStyleSheet("""color: rgb(255, 0, 0);""")

        self.source = None

    def setup(self, t_up, t_down, img_path):
        self.textUpLabel.setText(t_up)
        self.textDownLabel.setText(t_down)
        self.iconLabel.setPixmap(setPix(PathData.relative(img_path)))
        self.iconLabel.setScaledContents(True)

    def assign(self, obj):
        self.source = obj


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

    tmp = ImageQt.ImageQt(image).copy()  # Plain ImageQt() call don't return QImage.
    return QPixmap(tmp)

    # TransformMode => Qt::SmoothTransformation for better quality is possible.


def loadImage(self, recent):

    file_dir = QFileDialog.getOpenFileName(self, "Select Image", recent)[0]
    file_name = os.path.basename(file_dir)

    if not file_dir:
        LoggingEmitter.info("loadImage: Load Canceled")
        return False

    try:
        img = Image.open(file_dir)

    except NameError:
        LoggingEmitter.warning(f"loadImage: {file_name} not found.")
        return False

    except Image.UnidentifiedImageError:
        LoggingEmitter.warning(f"loadImage: {file_name} is not an image.")
        return False

    else:
        return img, file_name, os.path.dirname(file_dir)


def GenerateWidget(tgt):
    img = ICON_ASSIGN.setdefault(type(tgt).__name__, "default")

    item = SeqItemWidget()
    item.setup(
        tgt.name, str(type(tgt).__name__ + "Object"), "".join([ICON_LOCATION, img])
    )
    item.assign(tgt)

    return item


def AddToListWidget(tgt, item_list_widget, index=None):
    """
    Adds macro object to given QItemListWidget.
    :param index: if given, tries to insert item in given index.
    :param tgt: macro object to Add
    :param item_list_widget: QItemListWidget
    """

    LoggingEmitter.debug(f"Add: {type(tgt).__name__} '{tgt.name}'")

    item = GenerateWidget(tgt)

    list_item = QListWidgetItem(item_list_widget)
    list_item.setSizeHint(item.sizeHint())

    if index is not None:
        item_list_widget.insertItem(index, list_item)

    else:
        item_list_widget.addItem(list_item)
    item_list_widget.setItemWidget(list_item, item)


def AbortTimers():
    """
    Kills all Timers currently signed in Global list TIMER_RUNNING.
    Assuming Timers are added in tuple(QTimer, QEventLoop) format.
    """

    for timer in TIMER_RUNNING:
        timer[0].stop()
        timer[1].quit()

    TIMER_RUNNING.clear()


def QSleep(delay, output=False, append=True):
    # https://stackoverflow.com/questions/21079941
    # https://stackoverflow.com/questions/41309833

    def wait():
        # loop = QEventLoop()
        # QTimer.singleShot(delay * 1000, loop.quit)
        # loop.exec_()

        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)

        if append:
            TIMER_RUNNING.append(timer)
            LOOP_RUNNING.append(loop)

            timer.start(delay * 1000)
            loop.exec_()

            TIMER_RUNNING.remove(timer)
            LOOP_RUNNING.remove(loop)
        else:
            timer.start(delay * 1000)
            loop.exec_()

    class context:
        def __enter__(self):
            LoggingEmitter.debug(f"Wait {delay} start")

        def __exit__(self, exc_type, exc_val, exc_tb):
            LoggingEmitter.debug(f"Finish")

    if output:
        with context():
            wait()
    else:
        wait()


def getCaptureArea():

    # Fix not aborting issue here.

    """
    Get area to work with.
    """
    p1 = Pos()
    p2 = Pos()
    kill_key = "f2"

    def getPos(p):
        nonlocal kill_key

        while (not keyboard.is_pressed(kill_key)) and (not ABORT_SIGNALED):
            # fix loop here
            QSleep(0.05, append=False)

        p.set(*pyautogui.position())

        while (keyboard.is_pressed(kill_key)) and (not ABORT_SIGNALED):
            QSleep(0.05, append=False)

    getPos(p1)
    getPos(p2)

    if ABORT_SIGNALED:
        raise TypeError

    return Area.fromPos(p1, p2)
