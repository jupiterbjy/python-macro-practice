
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyautogui

from Toolset import QtTools
from Toolset.QtTools import appendText
from Toolset.Tools import nameCaller
from qtUI.Runner import Ui_MainWindow as Ui_Runner
import MacroMethods


# https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
class Worker(QRunnable):
    """
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        try:
            self.fn(*self.args, **self.kwargs)
        except Exception as exa:
            print(exa)


class CaptureCoverage(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.setWindowFlag(
            self.windowFlags() |
            Qt.FramelessWindowHint
        )

        self.setWindowOpacity(0.7)


# --------------------------------------------------------------
# https://horensic.tistory.com/85
# https://stackoverflow.com/questions/12827305

class Runner(QMainWindow, Ui_Runner):
    def __init__(self, parent, seq, finish_signal, debug):
        super(Runner, self).__init__(parent)
        self.setupUi(self)

        self.debug = debug
        self._stdout = QtTools.StdoutRedirect()
        self.StdRedirect()

        self.finish_signal = finish_signal
        self.finish_signal.signal.connect(self.close)

        self.sequenceStarted = False

        self.runButton.released.connect(self.runSeq)
        self.StopButton.released.connect(self.stopSeq)
        self.source = list(seq)
        self.updateHistory(self.source[0])

        print('GOT: ', self.source)

    def closeEvent(self, *args, **kwargs):
        self.deleteLater()

    def StdRedirect(self):
        if self.debug:
            self._stdout.start()
            self._stdout.printOccur.connect(lambda x: appendText(self.outputTextEdit, x))
        else:
            self._stdout.stop()

    def areaInject(self):

        if not self.fullScreenCheck.isChecked():
            self.runLine.setText('Press f2 at 2 diagonal corner.')
            area = QtTools.getCaptureArea()

            self.runLine.setText(str(area))

            for obj in self.source:
                obj.setArea(*area)

    def callCaptureCoverage(self):
        sub_window = Runner(self, self.seqStorage)
        sub_window.show()

# https://stackoverflow.com/questions/52522218/

    def updateHistory(self, obj=None):
        widget = self.currentSeq.itemWidget(self.currentSeq.item(0))

        try:
            size = widget.sizeHint()
        except AttributeError:
            pass
        else:
            new = QListWidgetItem(self.sequenceList)
            new.setSizeHint(size)

            self.sequenceList.addItem(new)
            self.sequenceList.setItemWidget(new, widget)
            self.currentSeq.clear()

        if obj:
            QtTools.AddToListWidget(obj, self.currentSeq)

    def updateHistory_workaround(self, obj=None):

        widget = self.currentSeq.itemWidget(self.currentSeq.item(0))

        try:
            QtTools.AddToListWidget(widget.source, self.sequenceList)
        except AttributeError:
            pass
        finally:
            self.currentSeq.clear()

        if obj:
            QtTools.AddToListWidget(obj, self.currentSeq)

    def runSeq_Threaded(self, obj):

        seq_count = 0

        while obj:
            self.runLine.setText(f'running "{obj.name}".')
            self.updateHistory_workaround(obj)

            try:
                obj = obj.run()

            except pyautogui.FailSafeException:
                print('└ PyAutoGui FailSafe')
                self.runLine.setText('Cannot Click (0,0)')
                break

            except ZeroDivisionError:
                print('└ Division by Zero')
                self.runLine.setText('Tried to divide by 0')
                break

            except MacroMethods.AbortException:
                print('└ Abort Signaled')
                self.runLine.setText('Aborted')
                break

            else:
                seq_count += 1
        else:
            self.runLine.setText('Macro finished.')
            self.updateHistory_workaround()

        self.sequenceStarted = False
        self.updateButtonState()
        MacroMethods.CLEAR()

    def runSeq(self):
        nameCaller()

        self.sequenceStarted = True

        self.sequenceList.clear()
        self.currentSeq.clear()
        self.updateButtonState()

        self.areaInject()
        self.runLine.setText('Macro started.')

        worker = Worker(self.runSeq_Threaded, self.source[0])
        worker.run()

    @staticmethod
    def stopSeq():
        MacroMethods.abort()
        QtTools.AbortTimers()

    def updateButtonState(self):

        if self.sequenceStarted:
            self.runButton.setDisabled(True)
            self.StopButton.setEnabled(True)
        else:
            self.runButton.setEnabled(True)
            self.StopButton.setDisabled(True)

    def _getPos(self):
        pass
