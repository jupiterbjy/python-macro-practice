import sys
from PyQt5.QtWidgets import *

from ToolSet import FrozenDetect
from pymacro import Ui_MainWindow
import MacroMethods as macro

# https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
# TODO: refer this and create icons for listWidgetItem.
# Nyaruko kawaii~~~!

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.insertButton.released.connect(self.addMethod)
        self.listAvailableMethods()

    def initializing(self):
        pass

    def listAvailableMethods(self):

        def setItems(item_list):    # is this proper way of utilizing coroutine?
            for name in item_list:
                item = QListWidgetItem()
                item.setText(name)
                yield item
                # TODO: add icon assignment, will use this function then.

        self.methodList.clear()
        # self.methodList.addItems(setItems(macro.__all__))
        for i in setItems(macro.__all__):
            self.methodList.addItem(i)

    def addMethod(self):
        self.method
        self.item = self.methodList.addItem()
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



def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    FrozenDetect.IsFrozen()
    main()
