
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyautogui

from Toolset import QtTools
from Toolset.Tools import nameCaller
from Qt_UI.Runner import Ui_MainWindow as Ui_Runner


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

        self._stdout = QtTools.StdoutRedirect()
        self._stdout.start()
        self._stdout.printOccur.connect(lambda x: self._appendText(x))

        self.runButton.released.connect(self.runSeq)
        self.source = list(seq)
        self.updateCurrentItem(self.source[0])

    def areaInject(self):

        if not self.fullScreenCheck.isChecked():
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

    def runSeq(self):

        nameCaller()

        self.sequenceList.clear()

        self.runButton.setDisabled(True)
        self.StopButton.setEnabled(True)

        self.areaInject()
        self.runLine.setText('Macro started.')

        try:
            obj = self.source[0].run()

        except pyautogui.FailSafeException:
            print('└ FailSafe Trigger')
            self.runLine.setText('Cannot Click (0,0), Aborted.')

        else:
            seq_count = 0
            while obj:
                self.runLine.setText(f'running "{obj.name}".')
                self.updateCurrentItem(obj)
                obj = obj.run()
                seq_count += 1

            self.runLine.setText('Macro finished.')
            self.runButton.setEnabled(True)
            self.StopButton.setDisabled(True)

    def _getPos(self):
        pass

    def _appendText(self, msg):
        self.outputTextEdit.moveCursor(QTextCursor.End)
        self.outputTextEdit.insertPlainText(msg)
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
