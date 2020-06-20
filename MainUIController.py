from PySide2 import QtWidgets
from io import StringIO
import logging
import sys
import os
from MainUI import MainWindow
import SubWindows
import MacroMethods
from Toolset import Tools, QtTools


# <To-Do>
# Support variable assign on objects other than Variables.
# Add image showing on double-click to object in history.
# figure out white image causing crash on matching image.
# Cleanup messy import chains
# implement undo

# Set Debug to False on build.
DEBUG = True
VERSION = "v0.0.6"
DATE = "2020-05-17"
LOG_STREAM = StringIO()
LOGGER = logging.getLogger("Third Eye")


class Controller:
    def __init__(self):

        self.editor = MainWindow(VERSION, LOGGER)
        self.editor.macroExecute.connect(self.show_runner)
        self.editor.showAbout.connect(self.show_about)
        self.editor.showLogger.connect(self.show_debugger)
        self.editor.exitSignal.connect(self.kill_all)

        self.runner = SubWindows.RunnerWindow()
        self.about = SubWindows.AboutWindow(VERSION, DATE)

        self.debugger = SubWindows.DebugWindow(LOG_STREAM, self.editor, self.runner)
        self.logInstance = QtTools.LoggingEmitter
        self.logInstance.signal.signal.connect(self.debugger.log)

    def show_editor(self):
        self.logInstance.info("Calling Editor.")
        self.editor.show()

    def show_runner(self, source):
        self.logInstance.info("Calling Runner.")
        self.runner.setSource(source)
        self.runner.exitSignal.connect(self.show_editor)
        self.runner.show()

    def show_about(self):
        self.logInstance.info("Calling About.")
        self.about.show()

    def show_debugger(self):
        self.logInstance.info("Calling Logger/Debugger.")
        self.debugger.show()

    def kill_all(self):
        for window in (self.about, self.runner, self.debugger):
            try:
                window.close()
            except RuntimeError:
                pass
            except AttributeError:
                pass


def log_initialize():
    # ref: https://hamait.tistory.com/880
    LOGGER.setLevel(level=logging.DEBUG if DEBUG else logging.WARN)

    for handler in LOGGER.handlers:
        LOGGER.removeHandler(handler)

    # Formatter = logging.Formatter(
    #     "[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
    #     "%Y-%m-%d %H:%M:%S",
    # )

    Formatter = logging.Formatter('%(asctime)s - %(levelname)-10s - %(message)s',
                                  "%Y-%m-%d %H:%M:%S")

    handler = logging.StreamHandler(LOG_STREAM)
    handler.setFormatter(Formatter)
    LOGGER.addHandler(handler)

    if DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(Formatter)
        LOGGER.addHandler(console_handler)

    QtTools.LoggingEmitter.setLogger(LOGGER)

    LOGGER.debug(f"{VERSION} built at {DATE}")
    LOGGER.info("Real-Time log feeds may have different time-frame.")
    LOGGER.debug("_____ Logging Started _____")


if __name__ == "__main__":
    log_initialize()

    Tools.PathData.setRelativePath(__file__)
    LOGGER.info(f"Freeze State: {Tools.IsFrozen()}")

    if not os.path.exists(Tools.PathData.relative("history")):
        LOGGER.info("Image dumping folder not found, creating new.")
        os.mkdir(Tools.PathData.relative("history"))

    MacroMethods.IMG_SAVER = MacroMethods.setSaver(Tools.PathData.relative("history"))

    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_editor()
    sys.exit(app.exec_())
