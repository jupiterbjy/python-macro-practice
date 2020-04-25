from PySide2 import QtCore, QtWidgets
import sys
import MainUI
import SubWindows
from Toolset import Tools


class Controller:

    def __init__(self):

        call_runner = QtCore.Signal(object)
        abort_signal = QtCore.Signal()

        self.editor = MainUI.MainWindow()
        self.editor.windowSwitchSignal.connect(self.show_runner)
        self.runner = None

    def show_editor(self):
        print('calling Editor')
        self.editor.show()

    def show_runner(self, source):
        print('calling Runner')
        self.runner = SubWindows.RunnerWindow(source)
        self.runner.exitSignal.connect(self.show_editor)
        self.runner.show()

    # def show_about(self):
    #     about = SubWindows.AboutWindow()


if __name__ == '__main__':
    Tools.IsFrozen()
    Tools.relative_path_set(__file__)
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_editor()
    sys.exit(app.exec_())
