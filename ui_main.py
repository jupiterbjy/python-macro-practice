import sys
import pickle
from PIL.ImageQt import ImageQt
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Toolset import FrozenDetect, ObjectDispatch, Tools, TextTools
from pymacro import Ui_MainWindow
import MacroMethods

# https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
# TODO: refer this and create icons for listWidgetItem.
# TODO: disable 'insert' button if condition is not met.
# TODO: separate 'edit' and 'insert'
# TODO: assign progress bar to time left for action.
# TODO: give property to base to get remaining time.
# TODO: fix loaded sequence disabling searchClickGroup
# TODO; fix sequence variables not loading when loaded.
# Nyaruko kawaii!

ICON_LOCATION = './icons/methods/'


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
    if type(name) != type:
        name = type(name)

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
        self.cachedImage = {
            'search': None,
            'count': None
        }

        self.searchInsert.released.connect(self.addMethodMain)
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

    def selectedMethod(self):
        # TODO: change color of 'selected:' with TextTools.
        out = MacroMethods.class_dict[str(self.methodList.currentItem().text())]
        print('selected:', ClassNameRip(out))
        return out()

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

    # TODO: reorder functions

    def searchImageUpdate(self, obj=None):
        if obj is None:
            self.searchImgLabel.clear()
            self.searchImgNameLabel.setText('No Image')
        else:
            self.searchImgNameLabel.setText(obj.name)
            self.searchImgLabel.setPixmap(_setPix(obj.targetImage))

    def searchLoadImage(self):
        img, file_name = _loadImage()
        self.cachedImage['search'] = img

        if img is not None:
            self.searchImgLabel.setPixmap(_setPix(img))
            self.searchImgNameLabel.setText(file_name)

    def countImageUpdate(self, obj=None):
        if obj is None:
            self.countImgLabel.clear()
            self.countImgNameLabel.setText('No Image')
        else:
            self.countImgNameLabel.setText(obj.name)
            self.countImgLabel.setPixmap(_setPix(obj.targetImage))

    def countLoadImage(self):
        img, file_name = _loadImage()
        self.cachedImage['count'] = img

        if img is not None:
            self.countImgLabel.setPixmap(QPixmap(_setPix(img)))
            self.countImgNameLabel.setText(file_name)

    def seqSave(self):
        name = QFileDialog.getSaveFileName(self, 'Save file')[0]
        target = MacroMethods.NextSetter(self.seqStorage)
        try:
            pickle.dump(target, open(name, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            print('seqSave:')
            print('save canceled.')
            pass

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

    def _append_text(self, msg):
        self.outputTextEdit.moveCursor(QTextCursor.End)
        self.outputTextEdit.insertPlainText(msg)
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def initializing(self, manual=False):
        if not manual:
            self.listAvailableMethods()
        self.refreshSequence()
        self.disableOptions(passed_object=MacroMethods.Click())

    def updateToSelected(self):
        # Assuming that wrong class will never inserted here.
        if not self.seqStorage:
            print('something went wrong in updateToSelected.')
            return

        obj = self.seqStorage[self.sequenceList.currentRow()]

        self.disableOptions(passed_object=obj)
        print('update2selected:')

        def default(obj_):
            print(f'{ClassNameRip(obj_)} is supplied.')

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

    def listAvailableMethods(self):
        print('Loading Methods:')

        def setItems(item_list):    # is this proper way of utilizing coroutine?
            for name in item_list:
                item = QListWidgetItem()
                item.setText(name)
                yield item
                # TODO: add icon assignment, will use this function then.

        self.methodList.clear()
        for i in setItems(MacroMethods.__all__):
            self.methodList.addItem(i)

        # self.methodList.addItems(setItems(macro.__all__))
        # Not using above to maintain order of items. Not sure if setItems ruins it.

        self.methodList.setCurrentRow(0)

        # TODO: hide LoopStart & LoopEnd from UI.

    def refreshSequence(self):
        # TODO: refresh all option sections upon selecting seq list.
        self.sequenceList.clear()
        print('Refreshing Sequence.')
        pass

    # -------------------------------------------------

    def addMethodMain(self, tgt=None):
        if tgt is None:
            target = self.selectedMethod()
            obj, img = self.addObjectDispatch(target)
            obj.name = self.nameLine.text()
        else:
            obj = tgt
            _, img = self.addObjectDispatch(tgt, new=False)

        print(f'Add: {ClassNameRip(obj)} object "{obj.name}"')

        if img is None:
            img = 'template.png'

        txt2 = str(type(obj))

        item = SeqItemWidget()
        item.setup(txt2, obj.name, ''.join([ICON_LOCATION, img]))

        list_item = QListWidgetItem(self.sequenceList)
        list_item.setSizeHint(item.sizeHint())

        self.sequenceList.addItem(list_item)
        self.sequenceList.setItemWidget(list_item, item)

        self.seqStorage.append(obj)
        print(self.seqStorage)

    # -------------------------------------------------

    def setXYFromImage(self):
        pass

    def addObjectDispatch(self, target, new=True):
        # Not sure if modularizing this is better or not.

        def defaultBehavior(obj):
            print('addObjectDispatch:')
            print(f'Object {str(obj)} Not dispatched.')
            return obj

        dispatch = ObjectDispatch.dispatcher(defaultBehavior)

        @dispatch.register(MacroMethods.Click)
        def _(obj):
            obj.target.set(self.xSpin.value(), self.ySpin.value())
            return obj, 'click.png'

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
            return obj, 'image.png'

        @dispatch.register(MacroMethods.Loop)
        def _(obj):
            return obj, None

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(obj):
            if new:
                obj.target = self.cachedImage['count']
            return obj, 'count.png'

        @dispatch.register(MacroMethods.Variable)
        def _(obj):
            return obj, None

        @dispatch.register(MacroMethods.Wait)
        def _(obj):
            obj.delay = self.waitSpin.value()
            obj.onFail = None
            obj.onSuccess = None
            return obj, 'wait.png'

        return dispatch(target)


def _setPix(image):
    return QPixmap(ImageQt(image).scaled(226, 151, Qt.KeepAspectRatio))


def _loadImage():

    file_dir = QFileDialog.getOpenFileName()[0]
    file_name = Tools.fileNameExtract(file_dir)
    try:
        img = Image.open(file_dir).convert('RGB')

    except NameError:
        print(f'{file_name} not found.')
        return None, None

    except Image.UnidentifiedImageError:
        print(f'{file_name} is not image.')
        return None, None

    else:
        return img, file_name


def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    FrozenDetect.IsFrozen()
    main()
