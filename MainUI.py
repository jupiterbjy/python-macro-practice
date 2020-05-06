from PySide2.QtWidgets import QFileDialog, QListWidgetItem, QMainWindow
from PySide2.QtCore import Signal
from PySide2.QtGui import QCloseEvent
import os
import json

from Toolset import QtTools, ObjectDispatch, Tools
from qtUI.pymacro import Ui_MainWindow
import MacroMethods


class MainWindow(QMainWindow, Ui_MainWindow):

    exitSignal = Signal()
    macroExecute = Signal(object)
    showAbout = Signal()
    showLogger = Signal()

    def __init__(self, version, logger):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Python Macro Sequence - " + version)

        self.seqStorage = []
        self.seqBackup = []  # Consumes memory!

        self.insertButton.released.connect(self.AddToSequence)
        self.methodList.currentRowChanged.connect(self._disableOptions)

        self.delButton.released.connect(self.removeElement)
        self.runButton.released.connect(self.runSeq)
        self.editButton.released.connect(self.editSelected)

        self.upButton.released.connect(self.moveOrder)
        self.downButton.released.connect(lambda up=False: self.moveOrder(up))

        self.searchImgLoadButton.released.connect(self.searchLoadImage)
        self.searchImgClearButton.released.connect(self.searchImageUpdate)

        self.countImgLoadButton.released.connect(self.countLoadImage)
        self.countImgClearButton.released.connect(self.countImageUpdate)

        self.sequenceList.clicked.connect(self._updateToSelected)

        self.actionSave.triggered.connect(self.seqSave)
        self.actionLoad.triggered.connect(self.seqLoad)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.showAbout.emit)
        self.actionLogger.triggered.connect(self.showLogger.emit)

        self.initializing()

        self.recentDir = {"Image": os.getcwd(), "IO": os.getcwd()}
        self.cachedImage = {"search": None, "count": None}

    def closeEvent(self, event: QCloseEvent):
        self.exitSignal.emit()

    def moveOrder(self, up=True):
        """
        Move up or down selected element.
        """

        sel_idx = self.sequenceList.currentRow()
        move_idx = (sel_idx - 1) if up else (sel_idx + 1)

        try:
            if move_idx == -1:  # Qt set -1 as false, sadly.
                raise IndexError
            element_move = self.seqStorage[move_idx]

        except IndexError:
            QtTools.LOGGER_INSTANCE.debug("Move " + ("up" if up else "down") + ":")
            QtTools.LOGGER_INSTANCE.debug("Cannot move selected object.")

        else:
            element_current = self.seqStorage[sel_idx]

            self.seqStorage[sel_idx], self.seqStorage[move_idx] = (
                element_move,
                element_current,
            )

            item_move = self.sequenceList.item(move_idx)
            item_sel = self.sequenceList.currentItem()

            widget_move = QtTools.GenerateWidget(element_move)
            widget_sel = QtTools.GenerateWidget(element_current)

            self.sequenceList.setItemWidget(item_move, widget_sel)
            self.sequenceList.setItemWidget(item_sel, widget_move)

            self.sequenceList.setCurrentRow(move_idx)
            self._updateToSelected()

    def removeElement(self, idx=None):
        """
        When called, removes selected item from both seqStorage & GUI.
        :return returns removed object.
        """
        self.backupSeq()
        idx = idx if idx else self.sequenceList.currentRow()

        try:
            if idx == -1:
                raise IndexError
            out = self.seqStorage.pop(idx)

        except IndexError:
            QtTools.LOGGER_INSTANCE.debug("remove: Index out of range")

        else:
            self.sequenceList.takeItem(idx)
            self._updateToSelected()

            return out

    def backupSeq(self):
        """
        Planing to support proper undo functionality, but not complete yet.
        """
        if len(self.seqBackup) >= 4:
            self.seqBackup.pop(0)

        self.seqBackup.append(self.seqStorage)
        QtTools.LOGGER_INSTANCE.debug(f"- Backup: {len(self.seqBackup)}")

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
            self.macroExecute.emit(self.seqStorage[0])

        except IndexError:
            QtTools.LOGGER_INSTANCE.debug("runSeq: Nothing To play.")

        else:
            self.hide()

    def selectedMethod(self):
        out = MacroMethods.class_dict[
            MacroMethods.__all__[self.methodList.currentRow()]
        ]
        return out()

    def selectedElement(self):
        try:
            widget = self.sequenceList.itemWidget(self.sequenceList.currentItem())
            source = widget.source
        except AttributeError:
            pass
        else:
            return source

    def searchImageUpdate(self, obj=None):
        self._ImageUpdateToObject(self.searchImgLabel, self.searchImgNameLabel, obj)

    def countImageUpdate(self, obj=None):
        self._ImageUpdateToObject(self.countImgLabel, self.countImgNameLabel, obj)

    def searchLoadImage(self):
        self._LoadImage(self.searchImgLabel, self.searchImgNameLabel, "search")

    def countLoadImage(self):
        self._LoadImage(self.countImgLabel, self.countImgNameLabel, "count")

    def editSelected(self):
        QtTools.LOGGER_INSTANCE.debug(f"Edit: {self.selectedElement().name}")
        self._configObject(self.selectedElement(), clear_text=False)
        self._comboBoxUpdateNew()
        item = QtTools.GenerateWidget(self.selectedElement())

        self.sequenceList.setItemWidget(self.sequenceList.currentItem(), item)

    def seqSave(self):
        """
        Saves current sequence into json serialized format.
        """

        name = QFileDialog.getSaveFileName(
            self, "Save file", self.recentDir["IO"], filter="*.json"
        )[0]
        for i in self.seqStorage:
            i.reset()

        baked = MacroMethods.Serializer(self.seqStorage)
        try:
            json.dump(baked, open(name, "w"), indent=2, default=lambda x: x.__dict__)
        except FileNotFoundError:
            QtTools.LOGGER_INSTANCE.debug("└ Save canceled")
        else:
            self.recentDir["IO"] = os.path.dirname(name)

    def seqLoad(self):
        """
        Loads json serialized Macro Sequence.
        """

        name = QFileDialog.getOpenFileName(
            self, "Load File", self.recentDir["IO"], filter="*.json"
        )[0]

        try:
            baked = json.load(open(name))

        except json.JSONDecodeError:
            QtTools.LOGGER_INSTANCE.debug("└ JSONDecodeError")
            return

        except UnicodeDecodeError:
            if name is None:
                raise FileNotFoundError

            QtTools.LOGGER_INSTANCE.debug("└ UnicodeDecodeError")
            return

        except FileNotFoundError:
            QtTools.LOGGER_INSTANCE.debug("└ Load canceled")
            return

        else:
            deserialized = MacroMethods.Deserializer(baked)
            self.recentDir["IO"] = os.path.dirname(name)

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
            MacroMethods.ExScope.SLEEP_FUNCTION = QtTools.QSleep
        else:
            self.seqStorage.clear()

        self.sequenceList.clear()
        self._comboBoxUpdateNew()
        self._comboBoxLoopUpdate()
        self.onFailCombo.setCurrentIndex(0)
        self.onSuccessCombo.setCurrentIndex(0)
        self.loopStartCombo.setCurrentIndex(0)
        self._disableOptions(MacroMethods.Click())

    def listAvailableMethods(self):
        """
        Looks for MacroMethods's usable classes and list those on MethodList.
        Only runs once per program execution.
        """

        def iconSet(name):
            temp = QtTools.ICON_LOCATION + QtTools.ICON_ASSIGN.setdefault(
                name, "default"
            )
            return Tools.PathData.relative(temp)

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
                QtTools.LOGGER_INSTANCE.info("AddToSequence: " + err.args[0])
                QtTools.LOGGER_INSTANCE.info("AddToSequence: Object config Failed.")
                return

            except IndexError as err:
                QtTools.LOGGER_INSTANCE.info(err.args[0])
                QtTools.LOGGER_INSTANCE.info("Object config Failed.")
                return

            else:
                obj = target

        else:
            obj = tgt

        QtTools.AddToListWidget(obj, self.sequenceList)
        self.seqStorage.append(obj)
        self.sequenceList.setCurrentRow(self.seqStorage.index(obj))
        self._comboBoxUpdateNew()
        self._updateToSelected(obj)

    def _comboBoxUpdateNew(self):
        success_bk = self.onSuccessCombo.currentIndex()
        fail_bk = self.onFailCombo.currentIndex()

        self.onSuccessCombo.clear()
        self.onFailCombo.clear()

        self.onSuccessCombo.addItem("Default")
        self.onFailCombo.addItem("Default")

        for i in self.seqStorage:
            self.onSuccessCombo.addItem(i.name)
            self.onFailCombo.addItem(i.name)

        self.onSuccessCombo.setCurrentIndex(success_bk)
        self.onFailCombo.setCurrentIndex(fail_bk)

    @property
    def listLoopStarts(self):
        return [i for i in self.seqStorage if isinstance(i, MacroMethods.LoopStart)]

    def _comboBoxLoopUpdate(self):
        curr = self.loopStartCombo.currentIndex()

        self.loopStartCombo.clear()

        self.loopStartCombo.addItem("Select..")

        for e in self.listLoopStarts:
            self.loopStartCombo.addItem(e.name)

        self.loopStartCombo.setCurrentIndex(curr)

    def _comboBoxUpdateSelected(self, target=None):
        if target:
            obj = target
        else:
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

        try:
            img, file_name, self.recentDir["Image"] = QtTools.loadImage(
                self, self.recentDir["Image"]
            )
        except TypeError:
            return

        except ValueError:
            return
        else:
            if img is not None:
                self.cachedImage[cache_name] = img
                name_label.setText(file_name)
                img_label.setPixmap(QtTools.setPix(img).scaled(*QtTools.IMG_CONVERT))
                img_label.setStyleSheet("background-color: rgba(40, 40, 40, 255);")

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
            name_label.setText("No Image")
            img_label.setStyleSheet("background-color: rgba(240, 240, 240, 255);")

        else:
            img_label.setPixmap(
                QtTools.setPix(obj.targetImage).scaled(*QtTools.IMG_CONVERT)
            )
            img_label.setStyleSheet("background-color: rgba(40, 40, 40, 255);")

    def _configObject(self, target, clear_text=True):
        """
        Configs given object with values from GUI.
        :param target: Instance of one of methods from MacroMethods.
        """

        text = self.nameLine.text()
        target.setName(type(target).__name__ if not text else text)

        if clear_text:
            self.nameLine.clear()

        try:
            if self.onSuccessCombo.currentIndex() != 0:
                target.onSuccess = self.seqStorage[
                    self.onSuccessCombo.currentIndex() - 1
                ]

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
                obj.targetImage = self.cachedImage["search"]
            except AttributeError:
                raise AttributeError("configObject: No Image specified.")

            obj.trials = self.trialsCountSpin.value()
            obj.loopDelay = self.trialsIntervalSpin.value()
            obj.randomOffset = self.searchRandSpin.value()

            obj.clickCount = self.searchClickCount.value()
            obj.clickDelay = self.searchClickInterval.value()

            obj.precision = self.searchPrecisionSpin.value() / 100
            obj.targetName = self.searchImgNameLabel.text()

        @dispatch.register(MacroMethods.LoopStart)
        def _(obj):
            pass

        @dispatch.register(MacroMethods.LoopEnd)
        def _(obj):
            obj.loopCount = self.loopCountSpin.value()

            if self.loopStartCombo.currentIndex() > 0:
                idx = self.loopStartCombo.currentIndex()
                obj.onSuccess = self.listLoopStarts[idx - 1]

            else:
                raise IndexError("LoopEnd: No Target specified.")

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(obj):
            try:
                obj.targetImage = self.cachedImage["count"]
            except AttributeError:
                raise AttributeError("SearchOccurrence: No Image specified.")

            obj.randomOffset = self.countRandSpin.value()

            obj.threshold = self.countThreshold.value() / 100

            obj.clickCount = self.countClickCount.value()
            obj.clickDelay = self.countClickInterval.value()

            obj.precision = self.countPrecisionSpin.value() / 100
            obj.targetName = self.countImgNameLabel.text()

        @dispatch.register(MacroMethods.Variable)
        def _(obj):
            obj.setValue(self.variableLine.text())

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
                QtTools.LOGGER_INSTANCE.debug("updateSel: Sequence is Empty.")
                return

        else:
            try:
                source = self.seqStorage[target.row()]

            except AttributeError:
                source = target

        src = type(source).__name__

        if self.sequenceList.currentItem() is not None:
            self.methodList.setCurrentRow(MacroMethods.__all__.index(src))
            self.editButton.setEnabled(True)
            self.nameLine.setText(source.name)
            self._disableOptions(source)
            self._comboBoxUpdateSelected(source)
        else:
            self.editButton.setDisabled(True)

        dispatch = ObjectDispatch.preset()

        # Dispatching =====================================

        @dispatch.register(MacroMethods.Click)
        def _(obj):
            try:
                self.clickX.setValue(obj.target.x)
                self.clickY.setValue(obj.target.y)
            except AttributeError:
                QtTools.LOGGER_INSTANCE.debug(AttributeError, obj.target)
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

            self.cachedImage["search"] = obj.targetImage

        @dispatch.register(MacroMethods.LoopStart)
        def _(obj):
            pass

        @dispatch.register(MacroMethods.LoopEnd)
        def _(obj):
            idx = self.listLoopStarts.index(obj.onSuccess)
            self.loopStartCombo.setCurrentIndex(idx + 1)

        @dispatch.register(MacroMethods.SearchOccurrence)
        def _(obj):
            self.countClickCount.setValue(obj.clickCount)
            self.countClickInterval.setValue(obj.clickDelay)

            self.countRandSpin.setValue(obj.randomOffset)

            self.countThreshold.setValue(int(obj.threshold * 100))

            self.countImgNameLabel.setText(obj.targetName)
            self.countImageUpdate(obj)

            self.countPrecisionSpin.setValue(int(obj.precision * 100))

            self.cachedImage["count"] = obj.targetImage

        @dispatch.register(MacroMethods.Variable)
        def _(obj):
            self.variableLine.setText(str(obj.value))

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

        groups = [
            self.waitGroup,
            self.clickGroup,
            self.loopGroup,
            self.varGroup,
            self.dragGroup,
        ]

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

        self.onSuccessCombo.setEnabled(True)

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

        @dispatch.register(MacroMethods.LoopStart)
        def _(_):
            self._comboBoxLoopUpdate()
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget.setTabEnabled(2, True)

        @dispatch.register(MacroMethods.LoopEnd)
        def _(_):
            self._comboBoxLoopUpdate()
            self.tabWidget.setCurrentIndex(2)
            self.tabWidget.setTabEnabled(2, True)
            self.loopGroup.setEnabled(True)
            self.loopStartCombo.setEnabled(True)
            self.onSuccessCombo.setDisabled(True)

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
