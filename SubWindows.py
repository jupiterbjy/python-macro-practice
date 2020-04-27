from PySide2.QtCore import QRunnable, Slot, Signal
from PySide2.QtWidgets import QMainWindow, QDialog, QWidget
import pyautogui

from Toolset import QtTools, Tools
from qtUI.Runner import Ui_Form
from qtUI.aboutDialog import Ui_About
from qtUI.debugWindow import Ui_DebugWindow
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
        try:
            self.fn(*self.args, **self.kwargs)
        except Exception as exp:
            raise exp


class CaptureCoverage(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.setWindowOpacity(0.7)


# --------------------------------------------------------------
# https://horensic.tistory.com/85
# https://stackoverflow.com/questions/12827305


class RunnerWindow(QWidget, Ui_Form):

    exitSignal = Signal()

    def __init__(self, logger):
        super().__init__()
        self.setupUi(self)

        self.logger = logger
        self.sequenceStarted = False

        self.runButton.released.connect(self.runSeq)
        self.stopButton.released.connect(self.stopSeq)
        self.source = None

    def setSource(self, source):
        self.source = source
        self.updateHistory(self.source)

    def injectGlobals(self):
        MacroMethods.DUMP = self.dumpImageCheck.isChecked()

        # making sure file is reset.
        for i in self.source:
            i.reset()

    def closeEvent(self, *args, **kwargs):
        self.exitSignal.emit()
        self.deleteLater()

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
                self.logger.critical("PyAutoGui FailSafe")
                self.runLine.setText("Cannot Click (0,0)")
                break

            except ZeroDivisionError:
                self.logger.critical("Division by Zero")
                self.runLine.setText("Tried to divide by 0")
                break

            except MacroMethods.AbortException:
                self.logger.warning("Abort Signaled")
                self.runLine.setText("Aborted")
                break

            else:
                seq_count += 1
        else:
            self.logger.info("Macro Finished without error.")
            self.runLine.setText("Macro finished.")
            self.updateHistory()

        self.endSeq()

    def runSeq(self):
        Tools.nameCaller()

        self.sequenceStarted = True

        self.sequenceList.clear()
        self.currentSeq.clear()
        self.updateButtonState()

        self.injectGlobals()
        self.areaInject()
        self.runLine.setText("Macro started.")

        worker = Worker(self.runSeq_Threaded, self.source)
        try:
            worker.run()
        except Exception as err:
            # Assume no error has line-break.
            self.logger.critical(str(err))

    def endSeq(self):
        Tools.nameCaller()

        for i in self.source:
            i.reset()

        self.sequenceStarted = False
        self.updateButtonState()
        MacroMethods.ABORT = False

    @staticmethod
    def stopSeq():
        MacroMethods.ABORT = True
        QtTools.AbortTimers()

    def updateButtonState(self):

        if self.sequenceStarted:
            self.runButton.setDisabled(True)
            self.stopButton.setEnabled(True)
        else:
            self.runButton.setEnabled(True)
            self.stopButton.setDisabled(True)


class AboutWindow(QMainWindow, Ui_About):
    def __init__(self, version, date):
        super(AboutWindow, self).__init__()
        self.setupUi(self)

        self.label.setPixmap(
            QtTools.setPix(
                Tools.resource_path(QtTools.ICON_LOCATION + QtTools.ABOUT_IMAGE)
            )
        )

        source = self.versionArea.toHtml()
        source = source.replace("DATE", version)
        source = source.replace("VERSION", date)

        self.versionArea.setHtml(source)


class DebugWindow(QWidget, Ui_DebugWindow):
    def __init__(self, logger, editor, runner):
        super(DebugWindow, self).__init__()
        self.setupUi(self)

        self.commandLine.returnPressed.connect(self.processCommand)
        self.editor = editor
        self.runner = runner
        self.logger = logger

        self.commandList = {
            "help": self.help,
            "list": self.listTarget,
            "clear": self.clear,
        }

    def help(self, *args):
        """
        help: display this message.
        """
        msg = "".join([i.__doc__ for i in self.commandList.values()])

        self.debugOutput.insertHtml(msg.replace("\n", "<br/>"))

    def processCommand(self):
        line = self.commandLine.text().split()
        self.commandLine.clear()
        self.commandList[line[0]](line[:1])

    def clear(self, *args):
        """
        clear: clears logging screen
        """
        self.debugOutput.clear()

    def listTarget(self, arg, *args):
        """
        list: show list of target. supported are:
        └ list macro: Show list of element in macro.
        └ list variable: Show list of variables.
        """

        if "var" in arg:
            self.listVariables()
        elif "mac" in arg:
            self.listMacroElements()
        else:
            self.debugOutput.insertHtml("Unrecognized command:", arg)

    def listVariables(self):
        pass

    def listMacroElements(self):
        for i in self.runner.source:
            self.debugOutput.insertHtml(f"{i.__repr__()}")
        pass

    def inspect(self, arg, *args):
        def inspect_variables(arg2, *args2):
            pass

        def inspect_macro(arg2, *args2):
            # change this into name-based search later, maybe.

            try:
                target = self.runner.source[arg2]
            except IndexError:
                self.debugOutput.insertHtml("Index out of range.")
            else:
                self.debugOutput.insertHtml(target.__repr__())

        if "var" in arg:
            inspect_variables(*args)
        elif "mac" in arg:
            inspect_macro(*args)
        else:
            self.debugOutput.insertHtml("Unrecognized command:", arg)
