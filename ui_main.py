import sys
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Toolset import QtTools, FrozenDetect, ObjectDispatch, Tools
from ImageModule import getCaptureArea
from pymacro import Ui_MainWindow
import MacroMethods

# TODO: disable 'insert' button if condition is not met.
# TODO: separate 'edit' and 'insert'
# TODO: assign progress bar to time left for action.
# TODO: give property to base to get remaining time.
# TODO: fix loaded sequence disabling searchClickGroup
# TODO; fix sequence variables not loading when loaded.
# TODO: reorder functions
# TODO: change color of 'selected:' with TextTools.
# TODO: add undo
# TODO: add methods auto selection upon change in seq selection.
# TODO: implement random offset via option.

ICON_LOCATION = './icons/methods/'
ICON_ASSIGN = {
    MacroMethods.Click: 'click.png',
    MacroMethods.Loop: 'loop.png',
    MacroMethods.sLoopEnd: 'loopEnd.png',
    MacroMethods.sLoopStart: 'loopStart.png',
    MacroMethods.ImageSearch: 'imageSearch.png',
    MacroMethods.Variable: 'variable.png',
    MacroMethods.Wait: 'wait.png',
    'default': 'template.png',
}


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self._stdout = QtTools.StdoutRedirect()
        self._stdout.start()
        self._stdout.printOccur.connect(lambda x: self._append_text(x))

        self.seqStorage = []
        self.cachedImage = {
            'search': None,
            'count': None
        }

        self.insertButton.released.connect(self.addMethodMain)
        self.methodList.currentRowChanged.connect(self.disableOptions)

        self.searchImgLoadButton.released.connect(self.searchLoadImage)
        self.searchImgClearButton.released.connect(self.searchImageUpdate)

        self.countImgLoadButton.released.connect(self.countLoadImage)
        self.countImgClearButton.released.connect(self.countImageUpdate)
        self.sequenceList.currentRowChanged.connect(self.updateToSelected)

        self.actionSave.triggered.connect(self.seqSave)
        self.actionLoad.triggered.connect(self.seqLoad)
        self.initializing()
        # Create QListWidget

    def runSeq(self, full_screen=False):
        MacroMethods.NextSetter(self.seqStorage)
        # self.waitProgressBar
        print('runSeq:')

        area = getCaptureArea()
        for obj in self.seqStorage:
            obj.SetArea(area)

        self.seqStorage[0].action()

    def selectedMethod(self):
        out = MacroMethods.class_dict[str(self.methodList.currentItem().text())]
        print('selected:', Tools.ClassNameRip(out))
        return out()

    def searchImageUpdate(self, obj=None):
        # Clears image when arg are not given.
        if obj is None:
            self.searchImgLabel.clear()
            self.searchImgNameLabel.setText('No Image')
        else:
            self.searchImgNameLabel.setText(obj.name)
            self.searchImgLabel.setPixmap(QtTools.setPix(obj.targetImage))

    def searchLoadImage(self):
        img, file_name = QtTools.loadImage(self)
        self.cachedImage['search'] = img

        if img is not None:
            self.searchImgLabel.setPixmap(QtTools.setPix(img))
            self.searchImgNameLabel.setText(file_name)

    def countImageUpdate(self, obj=None):
        if obj is None:
            self.countImgLabel.clear()
            self.countImgNameLabel.setText('No Image')
        else:
            self.countImgNameLabel.setText(obj.name)
            self.countImgLabel.setPixmap(QtTools.setPix(obj.targetImage))

    def countLoadImage(self):
        img, file_name = QtTools.loadImage(self)
        self.cachedImage['count'] = img

        if img is not None:
            self.countImgLabel.setPixmap(QtTools.setPix(img))
            self.countImgNameLabel.setText(file_name)

    # noinspection PyCallByClass,PyArgumentList
    def seqSave(self):
        name = QFileDialog.getSaveFileName(self, 'Save file')[0]
        target = MacroMethods.NextSetter(self.seqStorage)
        try:
            pickle.dump(target, open(name, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            print('seqSave:')
            print('save canceled.')
            pass

    # noinspection PyCallByClass,PyArgumentList
    def seqLoad(self):
        name = QFileDialog.getOpenFileName(self)[0]
        try:
            target = pickle.load(open(name, 'rb'))
        except FileNotFoundError:
            print('seqLoad:')
            print('FileNotFound.')
            pass
        else:
            self.initializing(manual=True)
            for i in target:
                self.addMethodMain(tgt=i)

    def initializing(self, manual=False):
        if not manual:
            self.listAvailableMethods()
        self.sequenceList.clear()
        self.disableOptions(passed_object=MacroMethods.Click())

    def listAvailableMethods(self):
        print('Loading Methods:')

        def setItems(item_list):
            for name in item_list:
                item = QListWidgetItem()
                item.setText(name)
                yield item

        self.methodList.clear()
        for i in setItems(MacroMethods.__all__):
            self.methodList.addItem(i)

        self.methodList.setCurrentRow(0)

    def addMethodMain(self, tgt=None):
        if tgt is None:
            target = self.selectedMethod()
            obj = self.configObject(target)
            obj.name = self.nameLine.text()
        else:
            obj = tgt
            self.configObject(tgt, new=False)

        print(f'Add: {Tools.ClassNameRip(obj)} object "{obj.name}"')

        img = ICON_ASSIGN.setdefault(type(obj), 'default')

        txt2 = str(type(obj))

        item = QtTools.SeqItemWidget()
        item.setup(txt2, obj.name, ''.join([ICON_LOCATION, img]))

        list_item = QListWidgetItem(self.sequenceList)
        list_item.setSizeHint(item.sizeHint())

        self.sequenceList.addItem(list_item)
        self.sequenceList.setItemWidget(list_item, item)

        self.seqStorage.append(obj)
        print(self.seqStorage)

    def setXYFromImage(self):
        pass

    def _append_text(self, msg):
        self.outputTextEdit.moveCursor(QTextCursor.End)
        self.outputTextEdit.insertPlainText(msg)
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def configObject(self, target, new=True):

        def defaultBehavior(obj):
            print('configObject:')
            print(f'Object {str(obj)} Not dispatched.')

        dispatch = ObjectDispatch.dispatcher(defaultBehavior)

        @dispatch.register(MacroMethods.Click)
        def _(obj):
            obj.target.set(self.xSpin.value(), self.ySpin.value())

        @dispatch.register(MacroMethods.ImageSearch)
        def _(obj):
            obj.clickOnMatch = self.searchClickGroup.isEnabled()
            print(self.searchClickGroup.isEnabled())
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
            obj.delay = self.waitSpin.value()
            obj.onFail = None
            obj.onSuccess = None

        return dispatch(target)

    def updateToSelected(self):
        # Assuming that wrong class will never inserted here.
        if not self.seqStorage:
            print('something went wrong in updateToSelected.')
            return

        obj = self.seqStorage[self.sequenceList.currentRow()]

        self.disableOptions(passed_object=obj)
        print('update2selected:')

        def default(obj_):
            print(f'{Tools.ClassNameRip(obj_)} is supplied.')

        dispatch = ObjectDispatch.dispatcher(default)

        @dispatch.register(MacroMethods.Click)
        def _(obj_):
            self.xSpin.setValue(obj_.target.x)
            self.ySpin.setValue(obj_.target.y)

        @dispatch.register(MacroMethods.ImageSearch)
        def _(obj_):
            print('dispatched to image')
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
            print('dispatched to wait')
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

        def default(obj):
            print('disableOptions:')
            print(f'Function for {obj} is not designated.')

        dispatch = ObjectDispatch.dispatcher(default)

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
