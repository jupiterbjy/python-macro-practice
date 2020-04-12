
from PySide2.QtWidgets import QFileDialog, QListWidgetItem, QApplication, QMainWindow
import sys
import os
import json

from Toolset import QtTools, ObjectDispatch, Tools, TextTools
from Toolset.QtTools import IMG_CONVERT, ICON_LOCATION, ICON_ASSIGN, appendText
from qtUI.pymacro import Ui_MainWindow
from Toolset.Tools import nameCaller
from SubWindow import Runner, About
import MacroMethods

# <Bug fix>

# <To-Do>
# Change pyinstaller to cx-freeze << hardly works
# implement order up/down
# implement loop

# <References>
# https://doc.qt.io/qt-5/qthread.html
# https://devblogs.microsoft.com/python/idiomatic-python-eafp-versus-lbyl/
# https://stackoverflow.com/questions/44955656/
# https://machinekoder.com/how-to-not-shoot-yourself-in-the-foot-using-python-qt/
# https://doc.qt.io/qt-5/threads-technologies.html
# https://wikidocs.net/22413

# <Reference To-Do>
# https://stackoverflow.com/questions/17129362


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.seqStorage = []
        self.seqBackup = []     # Consumes memory!

        self.runner_signal = QtTools.runnerSignal()
        self.runner_signal.signal.connect(self.SeqStopped)

        self.insertButton.released.connect(self.AddToSequence)
        self.methodList.currentRowChanged.connect(self._disableOptions)

        self.delButton.released.connect(self.removeElement)
        self.runButton.released.connect(self.runSeq)
        self.editButton.released.connect(self.editSelected)

        self.upButton.released.connect(lambda: self._moveOrder(up=True))
        self.downButton.released.connect(lambda: self._moveOrder())

        self.searchImgLoadButton.released.connect(lambda: self.searchLoadImage())
        self.searchImgClearButton.released.connect(lambda: self.searchImageUpdate())

        self.countImgLoadButton.released.connect(self.countLoadImage)
        self.countImgClearButton.released.connect(self.countImageUpdate)

        self.sequenceList.clicked.connect(lambda: self._updateToSelected())

        self.actionSave.triggered.connect(self.seqSave)
        self.actionLoad.triggered.connect(self.seqLoad)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.openAbout)

        self._stdout = QtTools.StdoutRedirect()
        self.StdRedirect()
        self.debugCheck.stateChanged.connect(self.StdRedirect)

        self.initializing()

        self.recentImageDir = os.getcwd()
        self.recentIoDir = os.getcwd()

        self.cachedImage = {
            'search': None,
            'count': None
        }

    def _moveOrder(self, up=True):

        sel_idx = self.sequenceList.currentRow()
        move_idx = (sel_idx - 1) if up else (sel_idx + 1)

        if move_idx == -1:      # Qt set -1 as False
            print('Cannot move selected object.')
            return

        try:
            element_move = self.seqStorage[move_idx]
        except IndexError:
            print('Cannot move selected object.')
        else:
            element_current = self.seqStorage[sel_idx]

            self.seqStorage[sel_idx], self.seqStorage[move_idx] = \
                element_move, element_current

            item_move = self.sequenceList.item(move_idx)
            item_sel = self.sequenceList.currentItem()

            widget_move = QtTools.GenerateWidget(element_move)
            widget_sel = QtTools.GenerateWidget(element_current)

            self.sequenceList.setItemWidget(item_move, widget_sel)
            self.sequenceList.setItemWidget(item_sel, widget_move)

            self._updateToSelected()

    def StdRedirect(self):
        if self.debugCheck.isChecked():
            self._stdout.stop()
            TextTools.COLORIZE_ENABLE = False
        else:
            self._stdout.start()
            self._stdout.printOccur.connect(lambda x: appendText(self.outputTextEdit, x))
            TextTools.COLORIZE_ENABLE = True

    def openAbout(self):
        ui = About(self)
        ui.show()

    def removeElement(self, idx=None):
        """
        When called, removes selected item from both seqStorage & GUI.
        """
        self.backupSeq()

        try:
            out = self.seqStorage.pop(idx if idx else QtTools.returnRow(self.sequenceList))

        except IndexError as err:
            print(err)

        except AttributeError as err:
            print(err)

        else:
            item = self.sequenceList.itemFromIndex(idx)
            self.sequenceList.takeItem(item)
            return out

    def backupSeq(self):
        """
        Planing to support proper undo functionality, but not complete yet.
        """
        if len(self.seqBackup) >= 4:
            self.seqBackup.pop(0)

        self.seqBackup.append(self.seqStorage)
        print(f'└ Backup: {len(self.seqBackup)}')

    def undoSeq(self):
        """
        Planing to support proper undo functionality, but not complete yet.
        """
        self.seqStorage = self.seqBackup.pop()

    def runSeq(self):
        """
        Prepares and Calls subWindow to run macro.
        """
        MacroMethods.SetNext(self.seqStorage)

        try:
            runner = Runner(self, self.seqStorage[0], self.runner_signal,
                            self.debugCheck.isChecked())
        except IndexError:
            self.StdRedirect()
            nameCaller()
            print('└ Nothing To play.')

        else:
            self._stdout.stop()
            # self.hide()
            runner.show()

    def SeqStopped(self):
        """
        Runs when SubWindow is closed.
        """
        if self.debugCheck.isChecked():
            self._stdout.start()

    def selectedMethod(self):
        out = MacroMethods.class_dict[MacroMethods.__all__[self.methodList.currentRow()]]
        return out()

    def selectedElement(self):
        widget = self.sequenceList.itemWidget(self.sequenceList.currentItem())
        return widget.source

    def searchImageUpdate(self, obj=None):
        self._ImageUpdateToObject(self.searchImgLabel, self.searchImgNameLabel, obj)

    def countImageUpdate(self, obj=None):
        self._ImageUpdateToObject(self.countImgLabel, self.countImgNameLabel, obj)

    def searchLoadImage(self):
        self._LoadImage(self.searchImgLabel, self.searchImgNameLabel, 'search')

    def countLoadImage(self):
        self._LoadImage(self.countImgLabel, self.countImgNameLabel, 'count')

    def editSelected(self):
        print(f'Edit: {self.selectedElement().name}')
        self._configObject(self.selectedElement(), clear_text=False)
        self._comboBoxUpdateNew()
        item = QtTools.GenerateWidget(self.selectedElement())

        self.sequenceList.setItemWidget(self.sequenceList.currentItem(), item)

    def seqSave(self):
        """
        Saves current sequence into json serialized format.
        """

        print(self.recentImageDir, self.recentIoDir)
        nameCaller((225, 8, 0))

        name = QFileDialog.getSaveFileName(self, 'Save file',
                                           self.recentIoDir, filter='*.json')[0]
        for i in self.seqStorage:
            i.reset()

        baked = MacroMethods.Serializer(self.seqStorage)
        try:
            json.dump(baked, open(name, 'w'), indent=2, default=lambda x: x.__dict__)
        except FileNotFoundError:
            print('└ Save canceled')
        else:
            self.recentIoDir = os.path.dirname(name)

    def seqLoad(self):
        """
        Loads json serialized Macro Sequence.
        """

        print(self.recentImageDir, self.recentIoDir)
        nameCaller((225, 8, 0))

        name = QFileDialog.getOpenFileName(self, 'Load File',
                                           self.recentIoDir, filter='*.json')[0]

        try:
            baked = json.load(open(name, 'r'))

        except json.JSONDecodeError:
            print('└ JSONDecodeError')
            return

        except UnicodeDecodeError:
            if name is None:
                raise FileNotFoundError

            print('└ UnicodeDecodeError')
            return

        except FileNotFoundError:
            print('└ Load canceled')
            return

        else:
            deserialized = MacroMethods.Deserializer(baked)
            self.recentIoDir = os.path.dirname(name)

        self.initializing(manual=True)

        for i in deserialized:
            self.AddToSequence(i)

        last = type(self.seqStorage[-1]).__name__
        self.methodList.setCurrentRow(MacroMethods.__all__.index(last))
        self.sequenceList.setCurrentRow(len(self.seqStorage) - 1)
        self._updateToSelected()

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
        self._comboBoxUpdateNew()
        self.onFailCombo.setCurrentIndex(0)
        self.onSuccessCombo.setCurrentIndex(0)
        self._disableOptions(MacroMethods.Click())

    def listAvailableMethods(self):
        """
        Looks for MacroMethods's usable classes and list those on MethodList.
        Only runs once per program execution.
        """

        def iconSet(name):
            temp = ICON_LOCATION + ICON_ASSIGN.setdefault(name, 'default')
            return Tools.resource_path(temp)

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
            target = self.selectedMethod()

            try:
                self._configObject(target)

            except AttributeError as err:
                nameCaller()
                print(*err.args)
                print('└ Object config Failed.')
                return

            else:
                obj = target

        else:
            obj = tgt

        QtTools.AddToListWidget(obj, self.sequenceList)
        self.seqStorage.append(obj)
        self._comboBoxUpdateNew()

    def _comboBoxUpdateNew(self):
        success_bk = self.onSuccessCombo.currentIndex()
        fail_bk = self.onFailCombo.currentIndex()

        self.onSuccessCombo.clear()
        self.onFailCombo.clear()

        self.onSuccessCombo.addItem('Default')
        self.onFailCombo.addItem('Default')

        for i in self.seqStorage:
            self.onSuccessCombo.addItem(i.name)
            self.onFailCombo.addItem(i.name)

        self.onSuccessCombo.setCurrentIndex(success_bk)
        self.onFailCombo.setCurrentIndex(fail_bk)

    def _comboBoxUpdateSelected(self):
        obj = self.selectedElement()

        try:
            index = self.seqStorage.index(obj.onSuccess)
        except ValueError:
            self.onSuccessCombo.setCurrentIndex(0)
        else:
            self.onSuccessCombo.setCurrentIndex(index + 1)

        try:
            index = self.seqStorage.index(obj.onFail)
        except ValueError:
            self.onFailCombo.setCurrentIndex(0)
        else:
            self.onFailCombo.setCurrentIndex(index + 1)

    def _setXYFromImage(self):
        """
        Set coordinates from given Image.
        Not cemented how click method will act - Absolute or Relative?
        Unlike freps, on PC one might not use full screen capture at all due to speed.
        Therefore nothing is concrete clear about what this function will be.
        """

    def _LoadImage(self, img_label, name_label, cache_name):
        """
        Subroutine of countLoadImage & searchLoadImage.
        Loads from external images and config widgets accordingly.
        :param img_label: QLabel to display image.
        :param name_label: QLabel to display image name.
        :param cache_name: string key for cached image name.
        :return: return false on TypeError.
        """
        print(self.recentImageDir, self.recentIoDir)

        try:
            img, file_name, self.recentImageDir = \
                QtTools.loadImage(self, self.recentImageDir)

        except TypeError:
            return

        except ValueError:
            return

        else:
            if img is not None:
                self.cachedImage[cache_name] = img
                name_label.setText(file_name)
                img_label.setPixmap(QtTools.setPix(img).scaled(*IMG_CONVERT))
                img_label.setStyleSheet('background-color: rgba(40, 40, 40, 255);')

    @staticmethod
    def _ImageUpdateToObject(img_label, name_label, obj):
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
            # name_label.setText(obj.name)
            img_label.setStyleSheet('background-color: rgba(40, 40, 40, 255);')

    def _configObject(self, target, clear_text=True):
        """
        Configs given object with values from GUI.
        :param target: Instance of one of methods from MacroMethods.
        """

        text = self.nameLine.text()
        target.name = type(target).__name__ if not text else text

        if clear_text:
            self.nameLine.clear()

        try:
            if self.onSuccessCombo.currentIndex() != 0:
                target.onSuccess = self.seqStorage[self.onSuccessCombo.currentIndex() - 1]

            elif self.onFailCombo.currentIndex() != 0:
                target.onFail = self.seqStorage[self.onFailCombo.currentIndex() - 1]

            else:
                target.onSuccess = None
                target.onFail = None
        except IndexError:
            pass

        dispatch = ObjectDispatch.preset()

        # Dispatching =====================================

        @dispatch.register(MacroMethods.Click)
        def _(obj):
            obj.target.set(self.clickX.value(), self.clickY.value())

        @dispatch.register(MacroMethods.Drag)
        def _(obj):
            x1, y1 = self.dragFromX.value(), self.dragFromY.value()
            x2, y2 = self.dragToX.value(), self.dragToY.value()
            obj.set(x1, y1, x2, y2)

        @dispatch.register(MacroMethods.ImageSearch)
        def _(obj):
            try:
                obj.targetImage = self.cachedImage['search']
            except AttributeError:
                raise AttributeError('└ No Image specified.')

            obj.trials = self.trialsCountSpin.value()
            obj.loopDelay = self.trialsIntervalSpin.value()
            obj.randomOffset = self.searchRandSpin.value()

            obj.clickCount = self.searchClickCount.value()
            obj.clickDelay = self.searchClickInterval.value()

            obj.precision = self.searchPrecisionSpin.value() / 100
            obj.targetName = self.searchImgNameLabel.text()

        @dispatch.register(MacroMethods.Loop)
        def _(obj):

            pass

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(obj):
            try:
                obj.targetImage = self.cachedImage['count']
            except AttributeError:
                raise AttributeError('└ No Image specified.')

            obj.randomOffset = self.countRandSpin.value()

            obj.threshold = self.countThreshold.value() / 100

            obj.clickCount = self.countClickCount.value()
            obj.clickDelay = self.countClickInterval.value()

            obj.precision = self.countPrecisionSpin.value() / 100
            obj.targetName = self.countImgNameLabel.text()

        @dispatch.register(MacroMethods.Variable)
        def _(obj):
            pass

        @dispatch.register(MacroMethods.Wait)
        def _(obj):
            obj.delay = self.waitSpin.value()

        # Dispatching =====================================

        return dispatch(target)

    def _updateToSelected(self, target=None):
        """
        Updates configuration GUI with selected object.
        :param target: If specified, will try to update with given object.
        """

        if target is None:

            try:
                source = self.selectedElement()
            except IndexError:
                nameCaller()
                print('└ Sequence is Empty.')
                return
            else:
                src = type(source).__name__
                self.methodList.setCurrentRow(MacroMethods.__all__.index(src))
        else:
            source = target

        if self.sequenceList.currentItem() is not None:
            self.editButton.setEnabled(True)
        else:
            self.editButton.setDisabled(True)

        self.nameLine.setText(source.name)
        self._disableOptions(source)
        self._comboBoxUpdateSelected()

        dispatch = ObjectDispatch.preset()

        # Dispatching =====================================

        @dispatch.register(MacroMethods.Click)
        def _(obj):
            try:
                self.clickX.setValue(obj.target.x)
                self.clickY.setValue(obj.target.y)
            except AttributeError:
                print(AttributeError, obj.target)
                self.clickX.setValue(obj.target[0])
                self.clickY.setValue(obj.target[1])

        @dispatch.register(MacroMethods.Drag)
        def _(obj):
            self.dragFromX.setValue(obj.p1.x)
            self.dragFromY.setValue(obj.p1.y)
            self.dragToX.setValue(obj.p2.x)
            self.dragToY.setValue(obj.p2.y)

        @dispatch.register(MacroMethods.ImageSearch)
        def _(obj):
            self.searchClickCount.setValue(obj.clickCount)
            self.searchClickInterval.setValue(obj.clickDelay)

            self.searchRandSpin.setValue(obj.randomOffset)

            self.trialsCountSpin.setValue(obj.trials)
            self.trialsIntervalSpin.setValue(obj.loopDelay)

            self.searchImgNameLabel.setText(obj.targetName)
            self.searchImageUpdate(obj)

            self.searchPrecisionSpin.setValue(int(obj.precision * 100))

            self.cachedImage['search'] = obj.targetImage

        @dispatch.register(MacroMethods.Loop)
        def _(obj):
            pass

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(obj):
            self.countClickCount.setValue(obj.clickCount)
            self.countClickInterval.setValue(obj.clickDelay)

            self.countRandSpin.setValue(obj.randomOffset)

            self.countThreshold.setValue(int(obj.threshold * 100))

            self.countImgNameLabel.setText(obj.targetName)
            self.countImageUpdate(obj)

            self.countPrecisionSpin.setValue(int(obj.precision * 100))

            self.cachedImage['count'] = obj.targetImage

        @dispatch.register(MacroMethods.Variable)
        def _(obj):
            pass

        @dispatch.register(MacroMethods.Wait)
        def _(obj):
            self.waitSpin.setValue(obj.delay)

        # Dispatching =====================================

        dispatch.dispatch(source)

    def _disableOptions(self, target=None):
        """
        Subroutine of _updateToSelected.
        Setup GUI according to given target object or selected Methods,
        or triggered upon change of selection in Method List.
        :param target: If not specified, will config with selection from method list.
        """

        groups = [self.waitGroup, self.clickGroup,
                  self.loopGroup, self.varGroup, self.dragGroup]

        if self.lockLogCheck.isChecked():
            return

        # release-connect args with row index for currentRowChanged. Counting this in.
        if target is None or isinstance(target, int):
            selected = self.selectedMethod()
            self.nameLine.clear()
        else:
            selected = target

        for g in groups:
            g.setEnabled(False)

        for i in range(3):
            self.tabWidget.setTabEnabled(i, False)

        dispatch = ObjectDispatch.preset()

        # Dispatching =====================================

        @dispatch.register(MacroMethods.Click)
        def _(_):
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget.setTabEnabled(2, True)
            self.clickGroup.setEnabled(True)

        @dispatch.register(MacroMethods.Drag)
        def _(_):
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget.setTabEnabled(2, True)
            self.dragGroup.setEnabled(True)

        @dispatch.register(MacroMethods.ImageSearch)
        def _(_):
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget.setTabEnabled(0, True)

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

        # Dispatching =====================================

        dispatch.dispatch(selected)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    Tools.IsFrozen()
    Tools.MAIN_LOCATION = __file__

    main()
