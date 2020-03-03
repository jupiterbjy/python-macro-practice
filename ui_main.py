import sys
from PyQt5.QtWidgets import *

from Toolset import FrozenDetect
from pymacro import Ui_MainWindow
import MacroMethods as macro


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.insertButton.released.connect(self.addMethod)

    def addMethod(self):
        self.loopCountSpin
        self.loopDelaySpin
        self.clickCountSpin
        self.clickIntervalSpin
        self.clickTargetCheck

        self.ImgLabel
        self.ImgNameLabel

    def loadMethods(self):
        item = QListWidgetItem()
        item.setText("")
        self.methodList.addItem(item)

        macro.Click()
        macro.LoopStart()
        macro.




def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    FrozenDetect.IsFrozen()
    main()
