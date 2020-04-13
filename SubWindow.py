from PySide2.QtCore import QRunnable, Slot
from PySide2.QtWidgets import QMainWindow, QDialog
import pyautogui

from Toolset import QtTools, Tools
from Toolset.QtTools import appendText, setPix, ABOUT_IMAGE, ICON_LOCATION
from Toolset.Tools import nameCaller
from qtUI.Runner import Ui_MainWindow as Ui_Runner
from qtUI.aboutDialog import Ui_About
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

    @Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        self.fn(*self.args, **self.kwargs)
        # try:
        #     self.fn(*self.args, **self.kwargs)
        # except Exception as exa:
        #     print(exa)


class CaptureCoverage(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

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
        self.source = seq
        self.updateHistory(self.source)

        print("GOT: ", self.source)

    def injectGlobals(self):
        MacroMethods.DEBUG = self.debug

        for i in self.source:
            i.reset()

    def closeEvent(self, *args, **kwargs):
        self.deleteLater()

    def StdRedirect(self):
        if self.debug:
            self._stdout.stop()
        else:
            self._stdout.start()
            self._stdout.printOccur.connect(
                lambda x: appendText(self.outputTextEdit, x)
            )

    def areaInject(self):

        self.runLine.setText("Press f2 at 2 diagonal corner.")
        area = QtTools.getCaptureArea()

        self.runLine.setText(str(area))

        for obj in self.source:
            obj.setArea(*area)

    def updateHistory(self, obj=None):

        widget = self.currentSeq.itemWidget(self.currentSeq.item(0))

        try:
            QtTools.AddToListWidget(widget.source, self.sequenceList, 0)
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
            self.updateHistory(obj)

            try:
                obj = obj.run()

            except pyautogui.FailSafeException:
                print("└ PyAutoGui FailSafe")
                self.runLine.setText("Cannot Click (0,0)")
                break

            except ZeroDivisionError:
                print("└ Division by Zero")
                self.runLine.setText("Tried to divide by 0")
                break

            except MacroMethods.AbortException:
                print("└ Abort Signaled")
                self.runLine.setText("Aborted")
                break

            else:
                seq_count += 1
        else:
            self.runLine.setText("Macro finished.")
            self.updateHistory()

        self.sequenceStarted = False
        self.updateButtonState()
        MacroMethods.ABORT = False

    def runSeq(self):
        nameCaller()

        self.sequenceStarted = True

        self.sequenceList.clear()
        self.currentSeq.clear()
        self.updateButtonState()

        self.injectGlobals()
        self.areaInject()
        self.runLine.setText("Macro started.")

        worker = Worker(self.runSeq_Threaded, self.source)
        worker.run()

    @staticmethod
    def stopSeq():
        MacroMethods.ABORT = True
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


class About(QMainWindow, Ui_About):
    def __init__(self, parent):
        super(About, self).__init__(parent)
        self.setupUi(self)
        self.label.setPixmap(setPix(Tools.resource_path(ICON_LOCATION + ABOUT_IMAGE)))
