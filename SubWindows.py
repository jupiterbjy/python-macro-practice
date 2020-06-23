from PySide2.QtCore import QRunnable, Slot, Signal
from PySide2.QtWidgets import QMainWindow, QDialog, QWidget
from PySide2.QtGui import QTextCursor
from threading import Thread, Event
import pyautogui
import re

import Toolset
from Toolset import QtTools, TextTools
from qtUI.Runner import Ui_Form
from qtUI.aboutDialog import Ui_About
from qtUI.debugWindow import Ui_DebugWindow
from Macro import Elements
import Macro


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
            raise from exp


class CaptureCoverage(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.setWindowOpacity(0.7)


# --------------------------------------------------------------
# https://horensic.tistory.com/85
# https://stackoverflow.com/questions/12827305


class RunnerWindow(QWidget, Ui_Form):

    exitSignal = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.sequenceStarted = False

        self.runButton.released.connect(self.runSeq)
        self.stopButton.released.connect(self.stopSeq)
        self.source = None

    def setSource(self, source):
        self.source = source
        self.updateHistory(self.source)

    def injectGlobals(self):
        Elements.ExScope.DUMP = self.dumpImageCheck.isChecked()
        QtTools.LoggingEmitter.info(f"Image Dump: {Elements.ExScope.DUMP}")

        # making sure file is reset.
        for i in self.source:
            i.reset()

    def closeEvent(self, *args, **kwargs):
        self.sequenceList.clear()
        self.currentSeq.clear()

        self.exitSignal.emit()

    def areaInject(self):

        self.runLine.setText("Press f2 at 2 diagonal corner.")
        area = QtTools.getCaptureArea()

        self.runLine.setText(str(area))

        for obj in self.source:
            obj.setArea(*area)

    def updateHistory(self, obj=None):
        try:
            widget = self.currentSeq.itemWidget(self.currentSeq.item(0))
        except RuntimeError:
            QtTools.LoggingEmitter.warning("RuntimeError: Widget already destroyed.")
            widget = QtTools.GenerateWidget(self.source)

        try:
            QtTools.AddToListWidget(widget.source, self.sequenceList, 0)
        except AttributeError:
            pass

        finally:
            try:
                self.currentSeq.clear()
            except RuntimeError as err:
                QtTools.LoggingEmitter.warning(f"RuntimeError: {err}")
                pass
        if obj:
            QtTools.AddToListWidget(obj, self.currentSeq)

    def _sequenceProcess(self, obj):

        seq_count = 0

        while obj:
            self.runLine.setText(f'running "{obj.name}".')
            self.updateHistory(obj)

            try:
                obj = obj.run()

            except pyautogui.FailSafeException:
                QtTools.LoggingEmitter.critical("PyAutoGui FailSafe")
                self.runLine.setText("Cannot Click (0,0)")
                break

            except ZeroDivisionError:
                QtTools.LoggingEmitter.critical("Division by Zero")
                self.runLine.setText("Tried to divide by 0")
                break

            except Macro.AbortException:
                QtTools.LoggingEmitter.warning("Abort Signaled")
                self.runLine.setText("Aborted")
                break

            else:
                seq_count += 1
        else:
            QtTools.LoggingEmitter.info("Macro Finished without error.")
            self.runLine.setText("Macro finished.")
            self.updateHistory()

        self.endSeq()

    def runSeq(self):

        self.sequenceStarted = True

        self.sequenceList.clear()
        self.currentSeq.clear()
        self.updateButtonState()

        self.injectGlobals()
        try:
            self.areaInject()

        except TypeError:
            QtTools.LoggingEmitter.critical("Macro aborted.")
            self.endSeq()
            return

        self.runLine.setText("Macro started.")

        worker = Worker(self._sequenceProcess, self.source)
        try:
            worker.run()

        except Exception as err:
            # Assume no error has line-break.
            QtTools.LoggingEmitter.critical(err)

    def endSeq(self):
        for i in self.source:
            i.reset()

        self.sequenceStarted = False
        self.updateButtonState()
        Elements.ExScope.ABORT = False
        QtTools.ABORT_SIGNALED = False

    def stopSeq(self):
        self.runLine.setText("Macro aborted.")

        Elements.ExScope.ABORT = True
        QtTools.ABORT_SIGNALED = True
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

        image_path = QtTools.ICON_LOCATION + QtTools.ABOUT_IMAGE
        self.label.setPixmap(QtTools.setPix(Toolset.PathData.relative(image_path)))

        source = self.versionArea.toHtml()
        source = source.replace("DATE", version)
        source = source.replace("VERSION", date)

        self.versionArea.setHtml(source)


class DebugWindow(QWidget, Ui_DebugWindow):
    def __init__(self, stream, editor, runner):
        super(DebugWindow, self).__init__()
        self.setupUi(self)

        self.commandLine.returnPressed.connect(self.processCommand)
        self.editor = editor
        self.runner = runner
        self.stream = stream
        self.pushDelayedLog()

        self.commandList = {
            "help": self.help,
            "list": self.listTarget,
            "clear": self.clear,
        }

        TextTools.COLORIZE_ENABLE = True

    # ---------------------------------------------------------

    def pushDelayedLog(self):
        html = self.stream.getvalue() + "\n"
        self.log(html)

    @Slot(str)
    def log(self, text):
        self.logOutput.moveCursor(QTextCursor.End)
        self.logOutput.append(text)

    def print_debug(self, text):
        self.debugOutput.moveCursor(QTextCursor.End)
        self.debugOutput.insertHtml(text.replace("\n", "<br/>"))

    def help(self, *args):
        """help: display this message.\n
        """

        msg = "".join([i.__doc__ for i in self.commandList.values()])
        self.print_debug(msg)
        # self.debugOutput.insertHtml(msg.replace("\n", "<br/>") + "<br/>" * 2)

    def processCommand(self):
        raw = self.commandLine.text()
        line = raw.split()
        self.commandLine.clear()

        formatted = TextTools.QtColorize(raw + "<br/>", (120, 255, 120))
        self.print_debug(formatted)

        try:
            func = self.commandList[line[0]]
            func(*line[1:])  # unexpected arguments? why?

        except KeyError:
            formatted = TextTools.QtColorize(
                f"Unrecognized command: {line[0]}\n\n", (255, 120, 120)
            )
            self.print_debug(formatted)

    def clear(self, *args2):
        """clear: clears logging screen\n
        """
        self.debugOutput.clear()

    def listTarget(self, *args2):
        """list: show list of target. supported are:
        └ list macro: Show list of element in macro.
        └ list variable: Show list of variables. <- Dummy\n
        """
        # this is going messy with html.. counter intuitive

        try:
            argument = args2[0]
        except IndexError:
            self.print_debug(self.listTarget.__doc__)
        else:
            if "var" in argument:
                self.listVariables()
            elif "mac" in argument:
                self.listMacroElements()
            else:
                raise KeyError

    def listVariables(self):
        pass

    def listMacroElements(self):
        reg = re.compile(r'(?<=┠─).+?(?=:)', re.MULTILINE)

        for i in self.editor.seqStorage:
            src = i.__repr__() + '\n\n'
            name = re.findall(reg, src)

            # Nested for, what the..
            for n in name:
                colored = TextTools.QtColorize(n, (0, 165, 255))
                src = src.replace(n, colored)

            self.print_debug(src)
