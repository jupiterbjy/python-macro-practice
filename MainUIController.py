from PySide2 import QtWidgets
import sys
import os
import MainUI
import SubWindows
import MacroMethods
from Toolset import Tools, ImageModule


VERSION = 'v0.0.5'
DATE = '2020-04-25'


class Controller:

    def __init__(self):

        self.editor = MainUI.MainWindow(VERSION)
        self.editor.windowSwitchSignal.connect(self.show_runner)
        self.editor.showAbout.connect(self.show_about)
        self.editor.exitSignal.connect(self.kill_all)

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

    def kill_all(self):
        try:
            self.about.close()
            self.runner.close()
        except RuntimeError:
            pass    # making sure it is closed
        except AttributeError:
            pass    # in this case macro never ran.


if __name__ == '__main__':
    Tools.IsFrozen()
    Tools.relative_path_set(__file__)

    if not os.path.exists(Tools.resource_path('history')):
        os.mkdir(Tools.resource_path('history'))

    MacroMethods.IMG_SAVER = ImageModule.saveImg(Tools.resource_path('history'))

    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_editor()
    sys.exit(app.exec_())
