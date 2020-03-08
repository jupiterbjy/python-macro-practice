import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ToolSet import FrozenDetect, ObjectDispatch
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
        self.allHBoxLayOut.addLayout(self.textLayOut, 1)
        self.setLayout(self.allHBoxLayOut)

        self.textUpLabel.setStyleSheet('''
                    color: rgb(0, 0, 255);
                ''')
        self.textDownLabel.setStyleSheet('''
                    color: rgb(255, 0, 0);
                ''')

    def setup(self, t_up, t_down, img_path):
        print(img_path)
        self.textUpLabel.setText(t_up)
        self.textDownLabel.setText(t_down)
        self.iconLabel.setPixmap(QPixmap(img_path).scaledToHeight(44))


def ClassNameRip(name):
    out = str(name).split('.')[-1]
    return out.replace('\'>', '')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
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
        out = MacroMethods.classes[self.methodList.currentRow()]
        print('selected:', ClassNameRip(out))
        return out()

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
        print('Loading Methods:')

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
        dispatch = self.CreateDispatcher()
        obj = dispatch(target)
        print(obj)
        obj.name = self.nameLine.text()

        print(f'Adding "{obj.name}" type {ClassNameRip(obj)}.')
        img = 'template.png'
        txt2 = str(type(obj))

        item = SeqItemWidget()
        item.setup(txt2, obj.name, img)

        list_item = QListWidgetItem(self.sequenceList)
        list_item.setSizeHint(item.sizeHint())

        self.sequenceList.addItem(list_item)
        self.sequenceList.setItemWidget(list_item, item)

    # -------------------------------------------------

    def CreateDispatcher(self):
        def defaultBehavior(obj):
            print(f'Object {str(obj)} Not dispatched.')
            return obj

        dispatch = ObjectDispatch.dispatchObject(defaultBehavior)

        @ObjectDispatch.register(dispatch, MacroMethods.Click)
        def _(obj):
            return obj

        @ObjectDispatch.register(dispatch, MacroMethods.ImageSearch)
        def _(obj):
            obj.clickOnMatch = self.clickTargetCheck.isChecked()
            obj.trials = self.loopCountSpin.value()
            obj.loopDelay = self.loopDelaySpin.value()
            obj.targetImage = None
            return obj

        @ObjectDispatch.register(dispatch, MacroMethods.Loop)
        def _(obj):
            return obj

        @ObjectDispatch.register(dispatch, MacroMethods.LoopStart)
        def _(obj):
            return obj

        @ObjectDispatch.register(dispatch, MacroMethods.LoopEnd)
        def _(obj):
            return obj

        @ObjectDispatch.register(dispatch, MacroMethods.SearchOccurrence)
        def _(obj):
            return obj

        @ObjectDispatch.register(dispatch, MacroMethods.Variable)
        def _(obj):
            return obj

        @ObjectDispatch.register(dispatch, MacroMethods.Wait)
        def _(obj):
            obj.delay = self.waitSpin.value
            obj.onFail = None
            obj.onSuccess = None
            return obj

        return dispatch


def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    FrozenDetect.IsFrozen()
    main()
