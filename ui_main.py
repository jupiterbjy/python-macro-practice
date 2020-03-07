import sys
from functools import singledispatch
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ToolSet import FrozenDetect
from pymacro import Ui_MainWindow
import MacroMethods

# https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
# TODO: refer this and create icons for listWidgetItem.
# Nyaruko kawaii!


class StdoutRedirect(QObject):
    # Codes from below.
    # https://4uwingnet.tistory.com/9

    printOccur = pyqtSignal(str, str, name="print")

    def __init__(self, *param):
        QObject.__init__(self, None)
        self.daemon = True
        self.sys_stdout = sys.stdout.write
        self.sys_stderr = sys.stderr.write

    def stop(self):
        sys.stdout.write = self.sys_stdout
        sys.stderr.write = self.sys_stderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg: self.write(msg, color="red")

    def write(self, s, color="black"):
        sys.stdout.flush()
        self.printOccur.emit(s, color)


class SeqItemWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.textLayOut = QVBoxLayout()
        self.textUpLabel = QLabel()
        self.textDownLabel = QLabel()
        self.textLayOut.addWidget(self.textUpLabel)
        self.textLayOut.addWidget(self.textDownLabel)
        self.allHBoxLayOut = QHBoxLayout()
        self.iconLabel = QLabel()
        self.allHBoxLayOut.addWidget(self.iconLabel)
        self.allHBoxLayOut.addLayout(self.textLayOut)
        self.setLayout(self.allHBoxLayOut)

        self.textUpLabel.setStyleSheet('''
                    color: rgb(0, 0, 255);
                ''')
        self.textDownLabel.setStyleSheet('''
                    color: rgb(255, 0, 0);
                ''')

    def setup(self, t_up, t_down, img_path):
        self.textUpLabel.setText(t_up)
        self.textDownLabel.setText(t_down)
        self.iconLabel.setPixmap(QPixmap(img_path))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self._stdout = StdoutRedirect()
        self._stdout.start()
        self._stdout.printOccur.connect(lambda x: self._append_text(x))

        self.seqStorage = []

        self.searchInsert.released.connect(self.addMethodMain)
        self.methodList.currentRowChanged.connect(self.disableOptions)
        self.initializing()
        # Create QListWidget

    def selectedMethod(self):
        return MacroMethods.classes[self.methodList.currentRow()]

    def disableOptions(self):
        selected = self.selectedMethod()



    def _append_text(self, msg):
        self.outputTextEdit.moveCursor(QTextCursor.End)
        self.outputTextEdit.insertPlainText(msg)
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def initializing(self):
        self.listAvailableMethods()
        self.refreshSequence()

    def updateToSelected(self):
        selected = self.sequenceList.selectedItems()
        for i in selected:
            pass

    def listAvailableMethods(self):
        print('Loading Methods.')

        def setItems(item_list):    # is this proper way of utilizing coroutine?
            for name in item_list:
                item = QListWidgetItem()
                item.setText(name)
                yield item
                # TODO: add icon assignment, will use this function then.

        self.methodList.clear()
        # self.methodList.addItems(setItems(macro.__all__))
        for i in setItems(MacroMethods.__all__):
            self.methodList.addItem(i)

        self.methodList.setCurrentRow(0)

        # TODO: hide LoopStart & LoopEnd from UI.

    def refreshSequence(self):
        # TODO: refresh all option sections upon selecting seq list.
        self.sequenceList.clear()
        print('Refreshing Sequence.')
        pass

    # -------------------------------------------------

    def addMethodMain(self):
        target = self.selectedMethod()
        obj = self.addMethod(target())
        obj.name = self.nameLine.text()

        print(f'Adding {obj.name} in seq.')
        img = 'template.png'
        txt2 = 'test'

        print(str(self.addMethod.registry.keys()))

        item = SeqItemWidget()
        self.sequenceList.addItem(item.setup(obj.name, txt2, img))

        # TODO: find way to assign target

    @singledispatch
    def addMethod(self, obj):
        print(f'Wrong Object {str(obj)} supplied.')
        return obj

    @addMethod.register(MacroMethods.Click)
    def _(self, obj):
        pass

    @addMethod.register(MacroMethods.ImageSearch)
    def _(self, obj):
        obj.clickOnMatch = self.clickTargetCheck.isChecked()
        obj.trials = self.loopCountSpin.value()
        obj.loopDelay = self.loopDelaySpin.value()
        obj.name = self.nameLine.text()
        obj.targetImage = None
        return obj

    @addMethod.register(MacroMethods.Loop)
    def _(self, obj):
        pass

    @addMethod.register(MacroMethods.LoopStart)
    def _(self, obj):
        pass

    @addMethod.register(MacroMethods.LoopEnd)
    def _(self, obj):
        pass

    @addMethod.register(MacroMethods.SearchOccurrence)
    def _(self, obj):
        pass

    @addMethod.register(MacroMethods.Variable)
    def _(self, obj):
        pass

    @addMethod.register(MacroMethods.Wait)
    def _(self, obj):
        print('adding object wait')
        obj.delay = self.waitSpin.value
        obj.onFail = None
        obj.onSuccess = None
        return obj

    # -------------------------------------------------


def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    FrozenDetect.IsFrozen()
    main()
