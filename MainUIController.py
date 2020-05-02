from PySide2 import QtWidgets
from io import StringIO
import logging
import sys
import os
from MainUI import MainWindow
import SubWindows
import MacroMethods
from Toolset import Tools


# <To-Do>
# Support variable assign on objects other than Variables.
# Change to ListView or ScrollArea from ListItem.
# Add image showing on double-click to object in history.
# figure out white image causing crash on matching image
# Cleanup messy import chains
# implement undo
# Change while-loop based log check into signal based.
#   This might cause some serious function call overheads..idk

DEBUG = True
VERSION = "v0.0.6"
DATE = "2020-04-27"
LOG_STREAM = StringIO()
LOGGER = logging.getLogger('Third Eye')


class Controller:
    def __init__(self):

        self.editor = MainWindow(VERSION)
        self.editor.macroExecute.connect(self.show_runner)
        self.editor.showAbout.connect(self.show_about)
        self.editor.showLogger.connect(self.show_debugger)
        self.editor.exitSignal.connect(self.kill_all)

        self.runner = SubWindows.RunnerWindow(LOGGER)
        self.about = SubWindows.AboutWindow(VERSION, DATE)
        self.debugger = SubWindows.DebugWindow(LOGGER, LOG_STREAM, self.editor, self.runner)

    def show_editor(self):
        LOGGER.info("Calling Editor.")
        self.editor.show()

    def show_runner(self, source):
        LOGGER.info("Calling Runner.")
        self.runner.setSource(source)
        self.runner.exitSignal.connect(self.show_editor)
        self.runner.show()

    def show_about(self):
        LOGGER.info("Calling About.")
        self.about.show()

    def show_debugger(self):
        LOGGER.info("Calling Logger/Debugger.")
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
    LOGGER.setLevel(level=logging.DEBUG if DEBUG else logging.WARN)

    for handler in LOGGER.handlers:
        LOGGER.removeHandler(handler)

    LOGGER.addHandler(logging.StreamHandler(LOG_STREAM))
    LOGGER.debug(f"{VERSION} built at {DATE}")
    LOGGER.debug('Logging Started.')


if __name__ == "__main__":
    log_initialize()

    Tools.PathData.setRelativePath(__file__)
    LOGGER.info(f"Freeze State: {Tools.IsFrozen()}")

    if not os.path.exists(Tools.PathData.relative("history")):
        LOGGER.info('Image dumping folder not found, creating new.')
        os.mkdir(Tools.PathData.relative("history"))

    MacroMethods.IMG_SAVER = MacroMethods.IMG_SAVER(Tools.PathData.relative("history"))

    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_editor()
    sys.exit(app.exec_())
