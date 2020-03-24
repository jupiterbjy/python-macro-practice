
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import pickle

from Toolset import QtTools, FrozenDetect, ObjectDispatch
from Toolset.QtTools import IMG_CONVERT, ICON_LOCATION, ICON_ASSIGN
from Qt_UI.pymacro import Ui_MainWindow
from Toolset.Tools import nameCaller
from SubWindow import SubWindow
import MacroMethods

# <Implementation>
# TODO: assign progress bar to time left for action.
# TODO: give property to base to get remaining time.
# TODO: add undo
# TODO: add about screen.
# TODO: add precision tab.
# TODO: Check Sequence and find if CaptureCoverage call is needed.
# TODO: connect onFail / onSuccess to object

# <Improvement>
# TODO: change color of 'selected:' with TextTools.
# TODO: implement random offset via option.
# TODO: rework scanOccurrence function in ImageModule.
# TODO: hide edit window while runner window is up and running.
# TODO: change how debugging images are generated.
# TODO: generate icon with target image.

# <Optimization TO-DO>
# TODO: Rewrite runner code to utilize QThread.
# TODO: cleanup unnecessary properties in MacroMethods.

# <Bug fix>
# TODO: fix font color reset upon print event.

# <References>
# https://doc.qt.io/qt-5/qthread.html
# https://devblogs.microsoft.com/python/idiomatic-python-eafp-versus-lbyl/
# https://stackoverflow.com/questions/44955656/how-to-convert-rgb-pil-image-to-numpy-array-with-3-channels


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

        self.insertButton.released.connect(self.AddToSequence)
        self.methodList.currentRowChanged.connect(self._disableOptions)
        self.delButton.released.connect(self.remove)
        self.runButton.released.connect(self.runSeq)
        self.editButton.released.connect(self.editSelected)

        self.searchImgLoadButton.released.connect(self.searchLoadImage)
        self.searchImgClearButton.released.connect(self.searchImageUpdate)

        self.countImgLoadButton.released.connect(self.countLoadImage)
        self.countImgClearButton.released.connect(self.countImageUpdate)
        self.sequenceList.clicked.connect(self._updateToSelected)

        self.actionSave.triggered.connect(self.seqSave)
        self.actionLoad.triggered.connect(self.seqLoad)
        self.initializing()

    def remove(self):
        """
        When called, removes selected item from both seqStorage & GUI.
        """
        self.backupSeq()
        del self.seqStorage[self.sequenceList.currentRow()]

        item = self.sequenceList.currentRow()
        self.sequenceList.takeItem(item)

    def backupSeq(self):
        """
        Planing to support proper undo functionality, but not complete yet.
        """
        if len(self.seqBackup) >= 4:
            self.seqBackup.pop(0)
        self.seqBackup.append(self.seqStorage)

    def undoSeq(self):
        """
        Planing to support proper undo functionality, but not complete yet.
        """
        self.seqStorage = self.seqBackup.pop()
        # if self.seqBackup:
        #     source = self.seqBackup.pop()
        #     self.seqUndo.append(source)
        #     self.seqStorage = source

    def runSeq(self, full_screen=False):
        """
        Prepares and Calls subWindow to run macro.
        :param full_screen: Not implemented yet.
        """
        MacroMethods.NextSetter(self.seqStorage)

        try:
            window = SubWindow(self, self.seqStorage)
        except IndexError:

            self._stdout = QtTools.StdoutRedirect()
            self._stdout.start()
            self._stdout.printOccur.connect(lambda x: self._appendText(x))

            nameCaller()
            print('└ Nothing To play.')
        else:
            window.show()
            # self.setWindowOpacity(0.7)

    def selectedClass(self):
        out = MacroMethods.class_dict[MacroMethods.__all__[self.methodList.currentRow()]]
        return out()

    def selectedSequence(self):
        return self.seqStorage[self.sequenceList.currentRow()]

    def searchImageUpdate(self, obj=None):
        self._ImageUpdate(self.searchImgLabel, self.searchImgNameLabel, obj)

    def countImageUpdate(self, obj=None):
        self._ImageUpdate(self.countImgLabel, self.countImgNameLabel, obj)

    def searchLoadImage(self):
        self._LoadImage(self.searchImgLabel, self.searchImgNameLabel, 'search')

    def countLoadImage(self):
        self._LoadImage(self.countImgLabel, self.countImgNameLabel, 'count')

    def editSelected(self):
        self._configObject(self.selectedSequence())

    # noinspection PyCallByClass,PyArgumentList
    def seqSave(self):
        """
        Saves current sequence into Pickle byte file.
        """
        nameCaller()
        name = QFileDialog.getSaveFileName(self, 'Save file')[0]
        MacroMethods.NextSetter(self.seqStorage)

        try:
            pickle.dump(self.seqStorage, open(name, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

        except FileNotFoundError:
            print('└ save canceled.')

    # noinspection PyCallByClass,PyArgumentList
    def seqLoad(self):
        """
        Loads Saved sequence stored as Bytes - aka HIGHEST_PROTOCOL - pickle file.
        """
        nameCaller()

        name = QFileDialog.getOpenFileName(self)[0]
        self.initializing(manual=True)

        try:
            target = pickle.load(open(name, 'rb'))
            for i in target:
                self.AddToSequence(tgt=i)

        except pickle.UnpicklingError:
            print('└ Wrong file is supplied.')

        except FileNotFoundError:
            print('└ File does not exist.')

        except AttributeError:
            print('└ File is Outdated.')

        except TypeError:
            print('└ File is Damaged.')

        else:
            # This is too expensive.. Might be better generate ordered dict.
            last = type(self.seqStorage[-1]).__name__
            self.methodList.setCurrentRow(MacroMethods.__all__.index(last))

    def initializing(self, manual=False):
        """
        Clears up program state, but not all yet. Ran upon program startup.
        :param manual: Set to True when loading from saved pickle file.
        """
        if not manual:
            self.listAvailableMethods()
            MacroMethods.SLEEP_FUNCTION = QtTools.QSleep
        else:
            self.seqStorage.clear()

        self.sequenceList.clear()
        self._comboBoxUpdate()
        self._disableOptions(MacroMethods.Click())

    def listAvailableMethods(self):
        """
        Looks for MacroMethods's usable classes and list those on MethodList.
        Only runs once per program execution.
        """

        def iconSet(name):
            """
            Find corresponding icon in image dict with method name.
            """
            return ICON_LOCATION + ICON_ASSIGN.setdefault(name, 'default')

        def setItems(item_list):
            """
            Coroutine to generate respective items from given method lists.
            """
            for name in item_list:
                item = QtTools.MethodItemWidget(iconSet(name), name)
                yield item

        self.methodList.clear()

        for i in setItems(MacroMethods.__all__):

            list_item = QListWidgetItem(self.methodList)
            list_item.setSizeHint(i.sizeHint())

            self.methodList.addItem(list_item)
            self.methodList.setItemWidget(list_item, i)

        self.methodList.setCurrentRow(0)

    def AddToSequence(self, tgt=None):
        """
        store object in seqStorage AND call AddToListWidget to display it on ListWidget.
        :param tgt: If not specified, will create new object from selected method.
        """

        if tgt is None:
            target = self.selectedClass()

            try:
                self._configObject(target)

            except AttributeError as err:
                nameCaller()
                print(*err.args)
                print('└ Object config Failed.')
                return

            obj = target
            text = self.nameLine.text()
            obj.name = type(obj).__name__ if text == '' else text
            self.nameLine.clear()

        else:
            obj = tgt
            self._updateToSelected(obj)

        QtTools.AddToListWidget(obj, self.sequenceList)
        self.seqStorage.append(obj)
        self._comboBoxUpdate()

    def _comboBoxUpdate(self):
        self.onSuccessCombo.clear()
        self.onFailCombo.clear()

        self.onSuccessCombo.addItem('Default')
        self.onFailCombo.addItem('Default')

        for i in self.seqStorage:
            self.onSuccessCombo.addItem(i.name)
            self.onFailCombo.addItem(i.name)

    def _setXYFromImage(self):
        """
        Set coordinates from given Image.
        Not cemented how click method will act - Absolute or Relative?
        Unlike freps, on PC one might not use full screen capture at all due to speed.
        Therefore nothing is concrete clear about what this function will be.
        """
        pass

    def _appendText(self, msg):
        self.outputTextEdit.moveCursor(QTextCursor.End)
        self.outputTextEdit.append(msg)
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def _LoadImage(self, img_label, name_label, cache_name):
        """
        Subroutine of countLoadImage & searchLoadImage.
        Loads from external images and config widgets accordingly.
        :param img_label: QLabel to display image.
        :param name_label: QLabel to display image name.
        :param cache_name: string key for cached image name.
        :return: return false on TypeError.
        """
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
        Update image from image inside object.
        Similar roles with _LoadImage.
        :param img_label: QLabel to display image.
        :param name_label: QLabel to display image name.
        :param obj: MacroMethod _Image subclasses. Expects PIL type Image inside.
        """
        if obj is None:
            img_label.clear()
            name_label.setText('No Image')
            img_label.setStyleSheet('background-color: rgba(240, 240, 240, 255);')

        else:
            img_label.setPixmap(QtTools.setPix(obj.targetImage).scaled(*IMG_CONVERT))
            name_label.setText(obj.name)
            img_label.setStyleSheet('background-color: rgba(40, 40, 40, 255);')

    def _configObject(self, target):
        """
        Configs given object with values from GUI.
        :param target: Instance of one of methods from MacroMethods.
        """
        dispatch = ObjectDispatch.preset()

        @dispatch.register(MacroMethods.Click)
        def _(obj):
            obj.target.set(self.xSpin.value(), self.ySpin.value())

        @dispatch.register(MacroMethods.ImageSearch)
        def _(obj):
            try:
                obj.targetImage = self.cachedImage['search']
            except AttributeError:
                raise AttributeError('└ No Image specified.')

            obj.clickOnMatch = self.searchClickGroup.isEnabled()
            obj.trials = self.trialsCountSpin.value()
            obj.loopDelay = self.trialsIntervalSpin.value()
            obj.clickCount = self.searchClickCount.value()
            obj.clickDelay = self.searchClickInterval.value()
            obj.precision = self.searchPrecisionSpin.value() / 100

        @dispatch.register(MacroMethods.Loop)
        def _(obj):
            pass

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(obj):
            obj.targetImage = self.cachedImage['count']
            obj.precision = self.countPrecisionSpin.value() / 100

        @dispatch.register(MacroMethods.Variable)
        def _(obj):
            pass

        @dispatch.register(MacroMethods.Wait)
        def _(obj):
            obj.delay = self.waitSpin.value()
            obj.onFail = None
            obj.onSuccess = None

        return dispatch(target)

    def _updateToSelected(self, target=None):
        """
        Updates configuration GUI with selected object.
        :param target: If specified, will try to update with given object.
        """

        # 'onClick' signal args with QModel. Making case for it.
        if target is None or isinstance(target, QModelIndex):
            try:
                obj = self.seqStorage[self.sequenceList.currentRow()]
            except IndexError:
                nameCaller()
                print('└ Sequence is Empty.')
                return
            else:
                src = type(obj).__name__
                self.methodList.setCurrentRow(MacroMethods.__all__.index(src))
        else:
            obj = target

        self.nameLine.setText(obj.name)
        self._disableOptions(obj)

        dispatch = ObjectDispatch.preset()

        @dispatch.register(MacroMethods.Click)
        def _(obj_):
            self.xSpin.setValue(obj_.target.x)
            self.ySpin.setValue(obj_.target.y)

        @dispatch.register(MacroMethods.ImageSearch)
        def _(obj_):
            self.searchClickGroup.setChecked(obj_.clickOnMatch)

            self.searchClickCount.setValue(obj_.clickCount)
            self.searchClickInterval.setValue(obj_.clickDelay)

            self.trialsCountSpin.setValue(obj_.trials)
            self.trialsIntervalSpin.setValue(obj_.loopDelay)

            self.searchImgNameLabel.setText(obj_.targetName)
            self.searchImageUpdate(obj_)

            self.searchPrecisionSpin.setValue(int(obj_.precision * 100))

            self.cachedImage['search'] = obj_.targetImage

        @dispatch.register(MacroMethods.Loop)
        def _(obj_):
            pass

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(obj_):
            self.countImageUpdate(obj_)
            pass

        @dispatch.register(MacroMethods.Variable)
        def _(obj_):
            pass

        @dispatch.register(MacroMethods.Wait)
        def _(obj_):
            self.waitSpin.setValue(obj_.delay)

        dispatch.dispatch(obj)

    def _disableOptions(self, target=None):
        """
        Subroutine of _updateToSelected.
        Setup GUI according to given target object or selected Methods,
        or triggered upon change of selection in Method List.
        :param target: If not specified, will config with selection from method list.
        """
        if self.lockLogCheck.isChecked():
            # Assuming users are in log tab as they have toggled checkbox.
            return

        # release-connect args with row index for currentRowChanged.
        if target is None or isinstance(target, int):
            selected = self.selectedClass()
        else:
            selected = target

        groups = [self.waitGroup, self.searchClickGroup, self.clickGroup,
                  self.loopGroup, self.trialsGroup, self.varGroup]

        for g in groups:
            g.setEnabled(False)

        for i in range(3):
            self.tabWidget.setTabEnabled(i, False)

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
            self.varGroup.setEnabled(True)

        @dispatch.register(MacroMethods.Wait)
        def _(_):
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget.setTabEnabled(2, True)
            self.waitGroup.setEnabled(True)

        dispatch.dispatch(selected)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    FrozenDetect.IsFrozen()
    main()
