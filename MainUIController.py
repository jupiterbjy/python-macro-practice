from PySide2 import QtCore, QtWidgets
from datetime import datetime
import sys
import MainUI
import SubWindows
from Toolset import Tools

VERSION = 'v0.0.5'
DATE = '2020-04-25'


class Controller:

    def __init__(self):

        call_runner = QtCore.Signal(object)
        call_about = QtCore.Signal()
        abort_signal = QtCore.Signal()

        self.editor = MainUI.MainWindow(VERSION)
        self.editor.windowSwitchSignal.connect(self.show_runner)
        self.editor.showAbout.connect(self.show_about)
        self.runner = None
        self.about = SubWindows.AboutWindow(VERSION, DATE)

    def show_editor(self):
        print('calling Editor')
        self.editor.show()

    def show_runner(self, source):
        print('calling Runner')
        self.runner = SubWindows.RunnerWindow(source)
        self.runner.exitSignal.connect(self.show_editor)
        self.runner.show()

    def show_about(self):
        print('calling About')
        self.about.show()


if __name__ == '__main__':
    Tools.IsFrozen()
    Tools.relative_path_set(__file__)
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_editor()
    sys.exit(app.exec_())
