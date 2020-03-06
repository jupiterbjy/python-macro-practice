import sys
from functools import singledispatch
from PyQt5.QtWidgets import *

from ToolSet import FrozenDetect
from pymacro import Ui_MainWindow
import MacroMethods as macro

# https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
# TODO: refer this and create icons for listWidgetItem.
# Nyaruko kawaii~~~!!


class SeqItemWidget(QWidget):
    def __init__(self, flags, parent=None, *args, **kwargs):
        super().__init__(flags, parent, *args, **kwargs)
        self.textLayOut = QVBoxLayout()
        self.textUpLabel = QLabel()
        self.textDownLabel = QLabel()
        self.textLayOut.addItem(self.textUpLabel)
        self.textLayOut.addItem(self.textDownLabel)
        self.allHBoxLayOut = QHBoxLayout()
        self.iconLabel = QLabel()
        self.allHBoxLayOut.addItem(self.iconLabel)
        self.allHBoxLayOut.addLayout(self.textLayOut)
        self.setLayout(self.allHBoxLayOut)

        self.textUpQLabel.setStyleSheet('''
                    color: rgb(0, 0, 255);
                ''')
        self.textDownQLabel.setStyleSheet('''
                    color: rgb(255, 0, 0);
                ''')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.insertButton.released.connect(self.addMethod)
        self.listAvailableMethods()
        self.sequenceList.clear()
        self.seqStorage = []

        # TODO: remove placeholders when testing is complete.

    def initializing(self):
        pass

    def updateToSelected(self):
        selected = self.sequenceList.selectedItems()
        for i in selected:
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

        # TODO: hide LoopStart & LoopEnd from UI.

    def addMethodMain(self):
        selected = self.methodList.selectedItems()  # only one object will be in list.

        for i in selected:
            obj = macro.classes[i]()
            obj.name = self.nameLine

        get = self.addMethod(obj)
        item = SeqItemWidget()
        # TODO: find way to assign target

    @singledispatch
    def addMethod(self, obj):
        print(f'Wrong Object {str(obj)} supplied.')

    @addMethod.register(macro.Click)
    def _(self, obj):
        pass

    @addMethod.register(macro.ImageSearch)
    def _(self, obj):
        obj.clickOnMatch = self.clickTargetCheck.isChecked()
        obj.trials = self.loopCountSpin.value()
        obj.loopDelay = self.loopDelaySpin.value()
        obj.name = self.nameLine.text()
        obj.targetImage = None
        return obj

    @addMethod.register(macro.Loop)
    def _(self, obj):
        pass

    @addMethod.register(macro.LoopStart)
    def _(self, obj):
        pass

    @addMethod.register(macro.LoopEnd)
    def _(self, obj):
        pass

    @addMethod.register(macro.SearchOccurrence)
    def _(self, obj):
        pass

    @addMethod.register(macro.Variable)
    def _(self, obj):
        pass

    @addMethod.register(macro.Wait)
    def _(self, obj):
        obj.delay = None
        obj.name = None
        obj.onFail = None
        obj.onSuccess = None

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
