
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyautogui
import gc

from Toolset import QtTools
from Toolset.QtTools import append
from Toolset.Tools import nameCaller
from Qt_UI.Runner import Ui_MainWindow as Ui_Runner

DEBUG = True
GARBAGE_PREVENT = []
gc.disable()


class CaptureCoverage(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.setWindowFlag(
            self.windowFlags() |
            Qt.FramelessWindowHint
        )

        self.setWindowOpacity(0.7)


class SubWindow(QMainWindow, Ui_Runner):
    def __init__(self, parent=None, seq=None):
        super(SubWindow, self).__init__(parent)
        self.setupUi(self)

        if not DEBUG:
            self._stdout = QtTools.StdoutRedirect()
            self._stdout.start()
            self._stdout.printOccur.connect(lambda x: append(self.outputTextEdit, x))

        self.runButton.released.connect(self.runSeq)
        self.source = list(seq)
        self.updateHistory(self.source[0])

        print('GOT: ', self.source)

    def areaInject(self):

        if not self.fullScreenCheck.isChecked():
            self.runLine.setText('Press f2 at 2 diagonal corner.')
            area = QtTools.getCaptureArea()

            self.runLine.setText(str(area))

            for obj in self.source:
                obj.setArea(*area)

    def callCaptureCoverage(self):
        sub_window = SubWindow(self, self.seqStorage)
        sub_window.show()

    def updateCurrentItem(self, item):
        _ = self.currentSeq.takeItem(0)
        QtTools.AddToListWidget(item, self.sequenceList)
        QtTools.AddToListWidget(item, self.currentSeq)

    def updateHistory(self, item=None, end=False):
        # https://stackoverflow.com/questions/52522218/getting-qtwidgets-from-my-custom-qlistwidgetitem
        # Fix crashing due to garbage collection.
        if end:

            widget = self.currentSeq.itemWidget(self.currentSeq.item(0))
            previous = self.currentSeq.item(0)
        else:

            widget = self.currentSeq.itemWidget(self.currentSeq.item(0))
            previous = self.currentSeq.takeItem(0)

        GARBAGE_PREVENT.append((widget, previous))

        if previous:
            self.sequenceList.addItem(previous)
            self.sequenceList.setItemWidget(previous, widget)

        if item:
            QtTools.AddToListWidget(item, self.currentSeq)

    @staticmethod
    def garbageCollect():
        GARBAGE_PREVENT.clear()

    def runSeq(self):

        self.garbageCollect()

        nameCaller()

        self.sequenceList.clear()
        self.currentSeq.clear()

        self.runButton.setDisabled(True)
        self.StopButton.setEnabled(True)

        self.areaInject()
        self.runLine.setText('Macro started.')

        obj = self.source[0]
        seq_count = 0

        while obj:
            self.runLine.setText(f'running "{obj.name}".')
            self.updateHistory(obj)

            try:
                obj = obj.run()

            except pyautogui.FailSafeException:
                print('└ PyAutoGui FailSafe')
                self.runLine.setText('Cannot Click (0,0), Aborted.')
                break

            except ZeroDivisionError:
                print('└ Division by Zero')
                self.runLine.setText('Tried to divide by 0.')
                break

            else:
                seq_count += 1

        else:
            self.runLine.setText('Macro finished.')
            self.runButton.setEnabled(True)
            self.StopButton.setDisabled(True)
            self.updateHistory(end=True)

    def _getPos(self):
        pass
