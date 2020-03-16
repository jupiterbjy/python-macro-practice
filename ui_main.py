
import sys
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Toolset import QtTools, FrozenDetect, ObjectDispatch
from ImageModule import getCaptureArea
from Qt_UI.pymacro import Ui_MainWindow
from Toolset.Tools import nameCaller
import MacroMethods

# TODO: disable 'insert' button if condition is not met.
# TODO: separate 'edit' and 'insert'
# TODO: assign progress bar to time left for action.
# TODO: give property to base to get remaining time.
# TODO: fix loaded sequence disabling searchClickGroup
# TODO; fix sequence variables not loading when loaded.
# TODO: change color of 'selected:' with TextTools.
# TODO: add undo
# TODO: implement random offset via option.
# TODO: connect undo

IMG_CONVERT = (226, 151, Qt.KeepAspectRatio)
ICON_LOCATION = './icons/methods/'
ICON_ASSIGN = {
    MacroMethods.Click: 'click.png',
    MacroMethods.Loop: 'loop.png',
    MacroMethods.sLoopEnd: 'loopEnd.png',
    MacroMethods.sLoopStart: 'loopStart.png',
    MacroMethods.ImageSearch: 'imageSearch.png',
    MacroMethods.Variable: 'variable.png',
    MacroMethods.Wait: 'wait.png',
    MacroMethods.SearchOccurrence: 'count.png',
    'Click': 'click.png',
    'Loop': 'loop.png',
    'sLoopEnd': 'loopEnd.png',
    'sLoopStart': 'loopStart.png',
    'ImageSearch': 'imageSearch.png',
    'Variable': 'variable.png',
    'Wait': 'wait.png',
    'default': 'template.png',
    'SearchOccurrence': 'count.png',
}


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self._stdout = QtTools.StdoutRedirect()
        self._stdout.start()
        self._stdout.printOccur.connect(lambda x: self._appendText(x))

        # self.seqUndo = []
        self.seqStorage = []
        self.seqBackup = []     # Consumes memory!

        self.cachedImage = {
            'search': None,
            'count': None
        }

        self.insertButton.released.connect(self.addMethodMain)
        self.methodList.currentRowChanged.connect(self.disableOptions)
        self.delButton.released.connect(self.remove)
        self.runButton.released.connect(self.runSeq)

        self.searchImgLoadButton.released.connect(self.searchLoadImage)
        self.searchImgClearButton.released.connect(self.searchImageUpdate)

        self.countImgLoadButton.released.connect(self.countLoadImage)
        self.countImgClearButton.released.connect(self.countImageUpdate)
        self.sequenceList.clicked.connect(self._updateToSelected)

        self.actionSave.triggered.connect(self.seqSave)
        self.actionLoad.triggered.connect(self.seqLoad)
        self.initializing()

    def remove(self):
        self.backupSeq()
        del self.seqStorage[self.sequenceList.currentRow()]

        item = self.sequenceList.currentRow()
        self.sequenceList.takeItem(item)

    def backupSeq(self):
        if len(self.seqBackup) >= 4:
            self.seqBackup.pop(0)
        self.seqBackup.append(self.seqStorage)

    def undoSeq(self):
        self.seqStorage = self.seqBackup.pop()
        # if self.seqBackup:
        #     source = self.seqBackup.pop()
        #     self.seqUndo.append(source)
        #     self.seqStorage = source

    def runSeq(self, full_screen=False):
        MacroMethods.NextSetter(self.seqStorage)
        # self.waitProgressBar
        print('runSeq:')

        if not full_screen:
            area = getCaptureArea()

            self.runLine.setText(str(area))

            for obj in self.seqStorage:
                obj.setArea(*area)

        try:
            self.runLine.setText('Macro started.')
            obj = self.seqStorage[0].action()

        except IndexError:
            print('└ sequence Empty')
            self.runLine.setText('Nothing To play.')
            return False
        else:
            while obj:
                self.runLine.setText(f'running {obj.name}.')
                obj = obj()
        finally:
            self.runLine.setText('Macro finished.')

    def selectedMethod(self):
        out = MacroMethods.class_dict[MacroMethods.__all__[self.methodList.currentRow()]]
        print(f'\nselected: {out.__name__}')
        return out()

    def searchImageUpdate(self, obj=None):
        self._ImageUpdate(self.searchImgLabel, self.searchImgNameLabel, obj)

    def countImageUpdate(self, obj=None):
        self._ImageUpdate(self.countImgLabel, self.countImgNameLabel, obj)

    def searchLoadImage(self):
        self._LoadImage(self.searchImgLabel, self.searchImgNameLabel, 'search')

    def countLoadImage(self):
        self._LoadImage(self.countImgLabel, self.countImgNameLabel, 'count')

    # noinspection PyCallByClass,PyArgumentList
    def seqSave(self):
        nameCaller()
        name = QFileDialog.getSaveFileName(self, 'Save file')[0]
        MacroMethods.NextSetter(self.seqStorage)

        try:
            pickle.dump(self.seqStorage, open(name, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

        except FileNotFoundError:
            print('└ save canceled.')

    # noinspection PyCallByClass,PyArgumentList
    def seqLoad(self):
        nameCaller()

        name = QFileDialog.getOpenFileName(self)[0]
        self.initializing(manual=True)

        try:
            target = pickle.load(open(name, 'rb'))
            for i in target:
                self.addMethodMain(tgt=i)

        except FileNotFoundError:
            print('└ File doesn\'t exist.')

        except TypeError:
            print('└ File is Damaged.')

        else:
            # This is too expensive.. Might be better generate ordered dict.
            last = type(self.seqStorage[-1]).__name__
            self.methodList.setCurrentRow(MacroMethods.__all__.index(last))

    def initializing(self, manual=False):
        if not manual:
            self.listAvailableMethods()
        else:
            self.seqStorage.clear()

        self.sequenceList.clear()
        self.disableOptions(passed_object=MacroMethods.Click())

    def listAvailableMethods(self):
        nameCaller()

        def iconSet(name):
            return ICON_ASSIGN.setdefault(name, 'default')

        def setItems(item_list):
            for name in item_list:
                item = QtTools.MethodItemWidget(ICON_LOCATION + iconSet(name), name)
                yield item

        self.methodList.clear()

        for i in setItems(MacroMethods.__all__):

            list_item = QListWidgetItem(self.methodList)
            list_item.setSizeHint(i.sizeHint())

            self.methodList.addItem(list_item)
            self.methodList.setItemWidget(list_item, i)

        self.methodList.setCurrentRow(0)

    def addMethodMain(self, tgt=None):
        nameCaller()

        if tgt is None:
            target = self.selectedMethod()
            self._configObject(target)
            obj = target
            obj.name = self.nameLine.text()
            self.nameLine.clear()
        else:
            obj = tgt
            self._updateToSelected(obj)

        print(f'└ Add: {type(obj).__name__} object "{obj.name}"')

        img = ICON_ASSIGN.setdefault(type(obj), 'default')

        item = QtTools.SeqItemWidget()
        item.setup(str(type(obj)), obj.name, ''.join([ICON_LOCATION, img]))

        list_item = QListWidgetItem(self.sequenceList)
        list_item.setSizeHint(item.sizeHint())

        self.sequenceList.addItem(list_item)
        self.sequenceList.setItemWidget(list_item, item)
        self.seqStorage.append(obj)

    def _setXYFromImage(self):
        pass

    def _appendText(self, msg):
        self.outputTextEdit.moveCursor(QTextCursor.End)
        self.outputTextEdit.insertPlainText(msg)
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def _LoadImage(self, img_label, name_label, cache_name):
        try:
            img, file_name = QtTools.loadImage(self)
        except TypeError:
            return False
        else:
            if img is not None:
                self.cachedImage[cache_name] = img
                name_label.setText(file_name)
                img_label.setPixmap(QtTools.setPix(img).scaled(*IMG_CONVERT))

    @staticmethod
    def _ImageUpdate(img_label, name_label, obj):
        """
        Clears image when arg are not given.
        Assuming only MacroMethods._Image subclasses to be passed.
        """
        if obj is None:
            img_label.clear()
            name_label.setText('No Image')
            img_label.setStyleSheet('background-color: rgba(240, 240, 240, 255);')

        else:
            img_label.setPixmap(QtTools.setPix(obj.targetImage).scaled(*IMG_CONVERT))
            name_label.setText(obj.name)
            img_label.setStyleSheet('background-color: rgba(40, 40, 40, 255);')

    def _configObject(self, target, new=True):

        # Can I utilize 'with' context manager here?
        dispatch = ObjectDispatch.preset()

        @dispatch.register(MacroMethods.Click)
        def _(obj):
            obj.target.set(self.xSpin.value(), self.ySpin.value())

        @dispatch.register(MacroMethods.ImageSearch)
        def _(obj):
            obj.clickOnMatch = self.searchClickGroup.isEnabled()
            obj.trials = self.trialsCountSpin.value()
            obj.loopDelay = self.trialsIntervalSpin.value()
            obj.clickCount = self.clickCountSpin.value()
            obj.clickDelay = self.clickIntervalSpin.value()
            if new:
                obj.targetImage = self.cachedImage['search']

        @dispatch.register(MacroMethods.Loop)
        def _(obj):
            pass

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(obj):
            if new:
                obj.target = self.cachedImage['count']

        @dispatch.register(MacroMethods.Variable)
        def _(obj):
            pass

        @dispatch.register(MacroMethods.Wait)
        def _(obj):
            if new:
                obj.delay = self.waitSpin.value()
                obj.onFail = None
                obj.onSuccess = None

        return dispatch(target)

    def _updateToSelected(self, target=None):
        if not self.seqStorage:
            print('self.seqStorage is Empty.')
            return False

        # Assuming that wrong class will never inserted here.
        # And it did. 'onClick' signal args with trash. Making case for it.

        if target is None or isinstance(target, QModelIndex):
            obj = self.seqStorage[self.sequenceList.currentRow()]
        else:
            obj = target

        self.disableOptions(passed_object=obj)

        dispatch = ObjectDispatch.preset()

        @dispatch.register(MacroMethods.Click)
        def _(obj_):
            self.xSpin.setValue(obj_.target.x)
            self.ySpin.setValue(obj_.target.y)

        @dispatch.register(MacroMethods.ImageSearch)
        def _(obj_):
            self.searchClickGroup.setEnabled(obj_.clickOnMatch)

            self.trialsCountSpin.setValue(obj_.trials)
            self.trialsIntervalSpin.setValue(obj_.loopDelay)
            self.cachedImage['search'] = obj_.targetImage
            self.searchImgNameLabel.setText(obj_.targetName)
            self.searchImageUpdate(obj_)

        @dispatch.register(MacroMethods.Loop)
        def _(obj_):
            return obj_

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(obj_):
            self.countImageUpdate(obj_)
            return obj_

        @dispatch.register(MacroMethods.Variable)
        def _(obj_):
            return obj_

        @dispatch.register(MacroMethods.Wait)
        def _(obj_):
            self.waitSpin.setValue(obj_.delay)

        dispatch.dispatch(obj)

    def disableOptions(self, _=None, passed_object=None):
        # Seems like release-connect args with row index for currentRowChanged.

        if passed_object is None:
            selected = self.selectedMethod()
        else:
            selected = passed_object

        groups = [self.waitGroup, self.searchClickGroup, self.clickGroup,
                  self.loopGroup, self.trialsGroup]

        dispatch = ObjectDispatch.preset()

        @dispatch.register(MacroMethods.Click)
        def _(_):
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget.setTabEnabled(2, True)
            self.clickGroup.setEnabled(True)

        @dispatch.register(MacroMethods.ImageSearch)
        def _(_):
            self.tabWidget.setCurrentIndex(0)
            self.trialsGroup.setEnabled(True)
            self.tabWidget.setTabEnabled(0, True)
            self.searchClickGroup.setEnabled(True)

        @dispatch.register(MacroMethods.Loop)
        def _(_):
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget.setTabEnabled(2, True)
            self.loopGroup.setEnabled(True)

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(_):
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget.setTabEnabled(1, True)

        @dispatch.register(MacroMethods.Variable)
        def _(_):
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget.setTabEnabled(2, True)

        @dispatch.register(MacroMethods.Wait)
        def _(_):
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget.setTabEnabled(2, True)
            self.waitGroup.setEnabled(True)

        for g in groups:
            g.setEnabled(False)

        for i in range(3):
            self.tabWidget.setTabEnabled(i, False)

        dispatch.dispatch(selected)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    FrozenDetect.IsFrozen()
    main()
