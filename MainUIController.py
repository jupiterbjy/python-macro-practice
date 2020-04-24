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

    def show_editor(self):
        print('calling Editor')
        self.editor.show()

    def show_runner(self, source):
        print('calling Runner')
        runner = SubWindows.RunnerWindow(source)
        runner.windowSwitchSignal.connect(self.show_editor)
        runner.show()

    # def show_about(self):
    #     about = SubWindows.AboutWindow()


if __name__ == '__main__':
    Tools.IsFrozen()
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_editor()
    sys.exit(app.exec_())
