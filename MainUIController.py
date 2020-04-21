from PySide2 import QtCore, QtWidgets
import sys
import MainUI
import SubWindows


class Controller:

    call_runner = QtCore.Signal(object)

    def show_editor(self):
        editor = MainUI.MainWindow()
        editor.windowSwitchSignal.connect(self.sho)

    def show_runner(self):
        runner = SubWindows.RunnerWindow()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_editor()
    sys.exit(app.exec_())
