# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './pymacro.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(735, 587)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(735, 587))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame_2 = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMaximumSize(QtCore.QSize(170, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.methodList = QtWidgets.QListWidget(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.methodList.sizePolicy().hasHeightForWidth())
        self.methodList.setSizePolicy(sizePolicy)
        self.methodList.setMinimumSize(QtCore.QSize(150, 0))
        self.methodList.setMaximumSize(QtCore.QSize(150, 16777215))
        self.methodList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.methodList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.methodList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.methodList.setAlternatingRowColors(True)
        self.methodList.setProperty("isWrapping", False)
        self.methodList.setResizeMode(QtWidgets.QListView.Fixed)
        self.methodList.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.methodList.setSelectionRectVisible(True)
        self.methodList.setObjectName("methodList")
        item = QtWidgets.QListWidgetItem()
        self.methodList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.methodList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.methodList.addItem(item)
        self.gridLayout_2.addWidget(self.methodList, 0, 0, 1, 1)
        self.debugCheck = QtWidgets.QCheckBox(self.frame_2)
        self.debugCheck.setChecked(True)
        self.debugCheck.setObjectName("debugCheck")
        self.gridLayout_2.addWidget(self.debugCheck, 1, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 431))
        self.tabWidget.setMaximumSize(QtCore.QSize(252, 16777215))
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setObjectName("tabWidget")
        self.imgTab = QtWidgets.QWidget()
        self.imgTab.setObjectName("imgTab")
        self.searchImgLabel = QtWidgets.QLabel(self.imgTab)
        self.searchImgLabel.setGeometry(QtCore.QRect(10, 10, 226, 151))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchImgLabel.sizePolicy().hasHeightForWidth())
        self.searchImgLabel.setSizePolicy(sizePolicy)
        self.searchImgLabel.setMaximumSize(QtCore.QSize(226, 151))
        self.searchImgLabel.setAutoFillBackground(True)
        self.searchImgLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.searchImgLabel.setText("")
        self.searchImgLabel.setScaledContents(False)
        self.searchImgLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.searchImgLabel.setObjectName("searchImgLabel")
        self.searchImgNameLabel = QtWidgets.QLabel(self.imgTab)
        self.searchImgNameLabel.setGeometry(QtCore.QRect(14, 146, 218, 12))
        self.searchImgNameLabel.setAutoFillBackground(False)
        self.searchImgNameLabel.setStyleSheet("background-color: rgba(0, 0, 0, 120);\n"
"color: rgb(255, 255, 255);")
        self.searchImgNameLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.searchImgNameLabel.setLineWidth(0)
        self.searchImgNameLabel.setTextFormat(QtCore.Qt.RichText)
        self.searchImgNameLabel.setWordWrap(False)
        self.searchImgNameLabel.setObjectName("searchImgNameLabel")
        self.trialsGroup = QtWidgets.QGroupBox(self.imgTab)
        self.trialsGroup.setGeometry(QtCore.QRect(130, 200, 103, 131))
        self.trialsGroup.setObjectName("trialsGroup")
        self.label = QtWidgets.QLabel(self.trialsGroup)
        self.label.setGeometry(QtCore.QRect(15, 20, 81, 20))
        self.label.setObjectName("label")
        self.trialsCountSpin = QtWidgets.QSpinBox(self.trialsGroup)
        self.trialsCountSpin.setGeometry(QtCore.QRect(15, 40, 71, 21))
        self.trialsCountSpin.setMinimum(1)
        self.trialsCountSpin.setMaximum(99999)
        self.trialsCountSpin.setProperty("value", 1)
        self.trialsCountSpin.setObjectName("trialsCountSpin")
        self.label_3 = QtWidgets.QLabel(self.trialsGroup)
        self.label_3.setGeometry(QtCore.QRect(14, 70, 81, 20))
        self.label_3.setObjectName("label_3")
        self.trialsIntervalSpin = QtWidgets.QDoubleSpinBox(self.trialsGroup)
        self.trialsIntervalSpin.setGeometry(QtCore.QRect(14, 90, 71, 21))
        self.trialsIntervalSpin.setMaximum(10000.0)
        self.trialsIntervalSpin.setSingleStep(0.05)
        self.trialsIntervalSpin.setProperty("value", 0.2)
        self.trialsIntervalSpin.setObjectName("trialsIntervalSpin")
        self.searchClickGroup = QtWidgets.QGroupBox(self.imgTab)
        self.searchClickGroup.setEnabled(True)
        self.searchClickGroup.setGeometry(QtCore.QRect(10, 200, 111, 131))
        self.searchClickGroup.setCheckable(False)
        self.searchClickGroup.setChecked(False)
        self.searchClickGroup.setObjectName("searchClickGroup")
        self.label_2 = QtWidgets.QLabel(self.searchClickGroup)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 81, 20))
        self.label_2.setObjectName("label_2")
        self.searchClickCount = QtWidgets.QSpinBox(self.searchClickGroup)
        self.searchClickCount.setGeometry(QtCore.QRect(20, 40, 71, 21))
        self.searchClickCount.setMaximum(99999)
        self.searchClickCount.setObjectName("searchClickCount")
        self.label_4 = QtWidgets.QLabel(self.searchClickGroup)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 81, 20))
        self.label_4.setObjectName("label_4")
        self.searchClickInterval = QtWidgets.QDoubleSpinBox(self.searchClickGroup)
        self.searchClickInterval.setGeometry(QtCore.QRect(20, 90, 71, 21))
        self.searchClickInterval.setMaximum(10000.0)
        self.searchClickInterval.setSingleStep(0.05)
        self.searchClickInterval.setProperty("value", 0.2)
        self.searchClickInterval.setObjectName("searchClickInterval")
        self.searchImgLoadButton = QtWidgets.QPushButton(self.imgTab)
        self.searchImgLoadButton.setGeometry(QtCore.QRect(161, 164, 75, 23))
        self.searchImgLoadButton.setObjectName("searchImgLoadButton")
        self.searchImgClearButton = QtWidgets.QPushButton(self.imgTab)
        self.searchImgClearButton.setGeometry(QtCore.QRect(80, 164, 75, 23))
        self.searchImgClearButton.setObjectName("searchImgClearButton")
        self.label_11 = QtWidgets.QLabel(self.imgTab)
        self.label_11.setGeometry(QtCore.QRect(13, 340, 81, 20))
        self.label_11.setObjectName("label_11")
        self.searchPrecisionSpin = QtWidgets.QSpinBox(self.imgTab)
        self.searchPrecisionSpin.setGeometry(QtCore.QRect(72, 340, 51, 21))
        self.searchPrecisionSpin.setPrefix("")
        self.searchPrecisionSpin.setMaximum(100)
        self.searchPrecisionSpin.setProperty("value", 85)
        self.searchPrecisionSpin.setObjectName("searchPrecisionSpin")
        self.tabWidget.addTab(self.imgTab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.countImgLabel = QtWidgets.QLabel(self.tab)
        self.countImgLabel.setGeometry(QtCore.QRect(10, 10, 226, 151))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.countImgLabel.sizePolicy().hasHeightForWidth())
        self.countImgLabel.setSizePolicy(sizePolicy)
        self.countImgLabel.setMaximumSize(QtCore.QSize(226, 151))
        self.countImgLabel.setAutoFillBackground(True)
        self.countImgLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.countImgLabel.setText("")
        self.countImgLabel.setScaledContents(False)
        self.countImgLabel.setObjectName("countImgLabel")
        self.countImgNameLabel = QtWidgets.QLabel(self.tab)
        self.countImgNameLabel.setGeometry(QtCore.QRect(14, 146, 218, 12))
        self.countImgNameLabel.setAutoFillBackground(False)
        self.countImgNameLabel.setStyleSheet("background-color: rgba(0, 0, 0, 120);\n"
"color: rgb(255, 255, 255);")
        self.countImgNameLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.countImgNameLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.countImgNameLabel.setLineWidth(0)
        self.countImgNameLabel.setTextFormat(QtCore.Qt.RichText)
        self.countImgNameLabel.setObjectName("countImgNameLabel")
        self.countImgLoadButton = QtWidgets.QPushButton(self.tab)
        self.countImgLoadButton.setGeometry(QtCore.QRect(161, 164, 75, 23))
        self.countImgLoadButton.setObjectName("countImgLoadButton")
        self.countImgClearButton = QtWidgets.QPushButton(self.tab)
        self.countImgClearButton.setGeometry(QtCore.QRect(80, 164, 75, 23))
        self.countImgClearButton.setObjectName("countImgClearButton")
        self.countClickGroup = QtWidgets.QGroupBox(self.tab)
        self.countClickGroup.setEnabled(True)
        self.countClickGroup.setGeometry(QtCore.QRect(10, 200, 111, 131))
        self.countClickGroup.setCheckable(False)
        self.countClickGroup.setChecked(False)
        self.countClickGroup.setObjectName("countClickGroup")
        self.label_7 = QtWidgets.QLabel(self.countClickGroup)
        self.label_7.setGeometry(QtCore.QRect(20, 20, 81, 20))
        self.label_7.setObjectName("label_7")
        self.clickCountSpin_2 = QtWidgets.QSpinBox(self.countClickGroup)
        self.clickCountSpin_2.setGeometry(QtCore.QRect(20, 40, 71, 21))
        self.clickCountSpin_2.setObjectName("clickCountSpin_2")
        self.label_8 = QtWidgets.QLabel(self.countClickGroup)
        self.label_8.setGeometry(QtCore.QRect(20, 70, 81, 20))
        self.label_8.setObjectName("label_8")
        self.clickIntervalSpin_2 = QtWidgets.QDoubleSpinBox(self.countClickGroup)
        self.clickIntervalSpin_2.setGeometry(QtCore.QRect(20, 90, 71, 21))
        self.clickIntervalSpin_2.setMaximum(10000.0)
        self.clickIntervalSpin_2.setSingleStep(0.05)
        self.clickIntervalSpin_2.setProperty("value", 0.2)
        self.clickIntervalSpin_2.setObjectName("clickIntervalSpin_2")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(11, 340, 81, 20))
        self.label_12.setObjectName("label_12")
        self.countPrecisionSpin = QtWidgets.QSpinBox(self.tab)
        self.countPrecisionSpin.setGeometry(QtCore.QRect(70, 340, 51, 21))
        self.countPrecisionSpin.setPrefix("")
        self.countPrecisionSpin.setMaximum(100)
        self.countPrecisionSpin.setProperty("value", 85)
        self.countPrecisionSpin.setObjectName("countPrecisionSpin")
        self.tabWidget.addTab(self.tab, "")
        self.funcTab = QtWidgets.QWidget()
        self.funcTab.setObjectName("funcTab")
        self.funcButton = QtWidgets.QPushButton(self.funcTab)
        self.funcButton.setGeometry(QtCore.QRect(320, 460, 61, 21))
        self.funcButton.setObjectName("funcButton")
        self.waitGroup = QtWidgets.QGroupBox(self.funcTab)
        self.waitGroup.setEnabled(True)
        self.waitGroup.setGeometry(QtCore.QRect(10, 10, 91, 51))
        self.waitGroup.setCheckable(False)
        self.waitGroup.setObjectName("waitGroup")
        self.waitSpin = QtWidgets.QDoubleSpinBox(self.waitGroup)
        self.waitSpin.setGeometry(QtCore.QRect(10, 20, 71, 21))
        self.waitSpin.setDecimals(1)
        self.waitSpin.setMaximum(100000000000.0)
        self.waitSpin.setSingleStep(0.5)
        self.waitSpin.setProperty("value", 5.0)
        self.waitSpin.setObjectName("waitSpin")
        self.loopGroup = QtWidgets.QGroupBox(self.funcTab)
        self.loopGroup.setEnabled(True)
        self.loopGroup.setGeometry(QtCore.QRect(10, 70, 91, 51))
        self.loopGroup.setCheckable(False)
        self.loopGroup.setObjectName("loopGroup")
        self.loopCountSpin = QtWidgets.QSpinBox(self.loopGroup)
        self.loopCountSpin.setGeometry(QtCore.QRect(10, 20, 71, 21))
        self.loopCountSpin.setMaximum(9999)
        self.loopCountSpin.setObjectName("loopCountSpin")
        self.clickGroup = QtWidgets.QGroupBox(self.funcTab)
        self.clickGroup.setGeometry(QtCore.QRect(10, 130, 91, 111))
        self.clickGroup.setObjectName("clickGroup")
        self.clickFromImg = QtWidgets.QPushButton(self.clickGroup)
        self.clickFromImg.setGeometry(QtCore.QRect(10, 80, 71, 21))
        self.clickFromImg.setObjectName("clickFromImg")
        self.label_6 = QtWidgets.QLabel(self.clickGroup)
        self.label_6.setGeometry(QtCore.QRect(10, 50, 21, 20))
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.clickGroup)
        self.label_5.setGeometry(QtCore.QRect(10, 20, 21, 20))
        self.label_5.setObjectName("label_5")
        self.clickX = QtWidgets.QSpinBox(self.clickGroup)
        self.clickX.setGeometry(QtCore.QRect(40, 20, 41, 22))
        self.clickX.setFrame(True)
        self.clickX.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.clickX.setMaximum(99999)
        self.clickX.setObjectName("clickX")
        self.clickY = QtWidgets.QSpinBox(self.clickGroup)
        self.clickY.setGeometry(QtCore.QRect(40, 50, 41, 22))
        self.clickY.setFrame(True)
        self.clickY.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.clickY.setMaximum(99999)
        self.clickY.setObjectName("clickY")
        self.varGroup = QtWidgets.QGroupBox(self.funcTab)
        self.varGroup.setGeometry(QtCore.QRect(110, 10, 127, 294))
        self.varGroup.setObjectName("varGroup")
        self.intRadio = QtWidgets.QRadioButton(self.varGroup)
        self.intRadio.setGeometry(QtCore.QRect(10, 20, 90, 16))
        self.intRadio.setObjectName("intRadio")
        self.doubleRadio = QtWidgets.QRadioButton(self.varGroup)
        self.doubleRadio.setGeometry(QtCore.QRect(10, 70, 90, 16))
        self.doubleRadio.setObjectName("doubleRadio")
        self.doubleSpin = QtWidgets.QDoubleSpinBox(self.varGroup)
        self.doubleSpin.setGeometry(QtCore.QRect(30, 90, 81, 22))
        self.doubleSpin.setObjectName("doubleSpin")
        self.integerSpin = QtWidgets.QSpinBox(self.varGroup)
        self.integerSpin.setGeometry(QtCore.QRect(30, 40, 81, 22))
        self.integerSpin.setObjectName("integerSpin")
        self.variableArg2 = QtWidgets.QComboBox(self.varGroup)
        self.variableArg2.setGeometry(QtCore.QRect(10, 200, 101, 22))
        self.variableArg2.setCurrentText("")
        self.variableArg2.setObjectName("variableArg2")
        self.variableArg1 = QtWidgets.QComboBox(self.varGroup)
        self.variableArg1.setGeometry(QtCore.QRect(10, 140, 101, 22))
        self.variableArg1.setCurrentText("")
        self.variableArg1.setObjectName("variableArg1")
        self.operatorArg1 = QtWidgets.QComboBox(self.varGroup)
        self.operatorArg1.setGeometry(QtCore.QRect(40, 170, 41, 22))
        self.operatorArg1.setCurrentText("")
        self.operatorArg1.setObjectName("operatorArg1")
        self.variableArg3 = QtWidgets.QComboBox(self.varGroup)
        self.variableArg3.setGeometry(QtCore.QRect(10, 260, 101, 22))
        self.variableArg3.setCurrentText("")
        self.variableArg3.setObjectName("variableArg3")
        self.operatorArg2 = QtWidgets.QComboBox(self.varGroup)
        self.operatorArg2.setGeometry(QtCore.QRect(40, 230, 41, 22))
        self.operatorArg2.setCurrentText("")
        self.operatorArg2.setObjectName("operatorArg2")
        self.operatorArg2.addItem("")
        self.operatorArg2.setItemText(0, "")
        self.operatorArg2.addItem("")
        self.calRadio = QtWidgets.QRadioButton(self.varGroup)
        self.calRadio.setGeometry(QtCore.QRect(10, 120, 90, 16))
        self.calRadio.setObjectName("calRadio")
        self.dragGroup = QtWidgets.QGroupBox(self.funcTab)
        self.dragGroup.setGeometry(QtCore.QRect(10, 250, 91, 151))
        self.dragGroup.setObjectName("dragGroup")
        self.dragFromImg = QtWidgets.QPushButton(self.dragGroup)
        self.dragFromImg.setGeometry(QtCore.QRect(10, 120, 71, 21))
        self.dragFromImg.setObjectName("dragFromImg")
        self.label_15 = QtWidgets.QLabel(self.dragGroup)
        self.label_15.setGeometry(QtCore.QRect(10, 20, 81, 20))
        self.label_15.setObjectName("label_15")
        self.dragFromX = QtWidgets.QSpinBox(self.dragGroup)
        self.dragFromX.setGeometry(QtCore.QRect(10, 40, 31, 22))
        self.dragFromX.setFrame(True)
        self.dragFromX.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dragFromX.setMaximum(99999)
        self.dragFromX.setObjectName("dragFromX")
        self.dragFromY = QtWidgets.QSpinBox(self.dragGroup)
        self.dragFromY.setGeometry(QtCore.QRect(50, 40, 31, 22))
        self.dragFromY.setFrame(True)
        self.dragFromY.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dragFromY.setMaximum(99999)
        self.dragFromY.setObjectName("dragFromY")
        self.label_16 = QtWidgets.QLabel(self.dragGroup)
        self.label_16.setGeometry(QtCore.QRect(10, 70, 81, 20))
        self.label_16.setObjectName("label_16")
        self.dragToY = QtWidgets.QSpinBox(self.dragGroup)
        self.dragToY.setGeometry(QtCore.QRect(50, 90, 31, 22))
        self.dragToY.setFrame(True)
        self.dragToY.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dragToY.setMaximum(99999)
        self.dragToY.setObjectName("dragToY")
        self.dragToX = QtWidgets.QSpinBox(self.dragGroup)
        self.dragToX.setGeometry(QtCore.QRect(10, 90, 31, 22))
        self.dragToX.setFrame(True)
        self.dragToX.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dragToX.setMaximum(99999)
        self.dragToX.setObjectName("dragToX")
        self.tabWidget.addTab(self.funcTab, "")
        self.debugTab = QtWidgets.QWidget()
        self.debugTab.setObjectName("debugTab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.debugTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.outputTextEdit = QtWidgets.QTextEdit(self.debugTab)
        self.outputTextEdit.setStyleSheet("background-color: rgb(30, 30, 30);\n"
"color: rgb(230, 230, 230);")
        self.outputTextEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.outputTextEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.outputTextEdit.setLineWidth(1)
        self.outputTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.outputTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.outputTextEdit.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.outputTextEdit.setUndoRedoEnabled(False)
        self.outputTextEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.outputTextEdit.setLineWrapColumnOrWidth(0)
        self.outputTextEdit.setReadOnly(True)
        self.outputTextEdit.setObjectName("outputTextEdit")
        self.gridLayout_6.addWidget(self.outputTextEdit, 1, 0, 1, 1)
        self.lockLogCheck = QtWidgets.QCheckBox(self.debugTab)
        self.lockLogCheck.setObjectName("lockLogCheck")
        self.gridLayout_6.addWidget(self.lockLogCheck, 0, 0, 1, 1)
        self.tabWidget.addTab(self.debugTab, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 0, 1, 1, 1)
        self.onSuccessCombo = QtWidgets.QComboBox(self.frame_3)
        self.onSuccessCombo.setObjectName("onSuccessCombo")
        self.gridLayout_5.addWidget(self.onSuccessCombo, 1, 0, 1, 1)
        self.onFailCombo = QtWidgets.QComboBox(self.frame_3)
        self.onFailCombo.setObjectName("onFailCombo")
        self.gridLayout_5.addWidget(self.onFailCombo, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_5, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.runButton = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setObjectName("runButton")
        self.horizontalLayout.addWidget(self.runButton)
        self.insertButton = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.insertButton.sizePolicy().hasHeightForWidth())
        self.insertButton.setSizePolicy(sizePolicy)
        self.insertButton.setObjectName("insertButton")
        self.horizontalLayout.addWidget(self.insertButton)
        self.editButton = QtWidgets.QPushButton(self.frame_3)
        self.editButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editButton.sizePolicy().hasHeightForWidth())
        self.editButton.setSizePolicy(sizePolicy)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout.addWidget(self.editButton)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.sequenceList = QtWidgets.QListWidget(self.frame)
        self.sequenceList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.sequenceList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sequenceList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.sequenceList.setAlternatingRowColors(True)
        self.sequenceList.setMovement(QtWidgets.QListView.Static)
        self.sequenceList.setViewMode(QtWidgets.QListView.ListMode)
        self.sequenceList.setSelectionRectVisible(True)
        self.sequenceList.setObjectName("sequenceList")
        item = QtWidgets.QListWidgetItem()
        self.sequenceList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.sequenceList.addItem(item)
        self.gridLayout.addWidget(self.sequenceList, 1, 0, 1, 3)
        self.delButton = QtWidgets.QPushButton(self.frame)
        self.delButton.setObjectName("delButton")
        self.gridLayout.addWidget(self.delButton, 2, 2, 1, 1)
        self.downButton = QtWidgets.QPushButton(self.frame)
        self.downButton.setObjectName("downButton")
        self.gridLayout.addWidget(self.downButton, 2, 1, 1, 1)
        self.upButton = QtWidgets.QPushButton(self.frame)
        self.upButton.setObjectName("upButton")
        self.gridLayout.addWidget(self.upButton, 2, 0, 1, 1)
        self.nameLine = QtWidgets.QLineEdit(self.frame)
        self.nameLine.setInputMask("")
        self.nameLine.setObjectName("nameLine")
        self.gridLayout.addWidget(self.nameLine, 0, 0, 1, 3)
        self.gridLayout_4.addWidget(self.splitter, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuMenu.addAction(self.actionSave)
        self.menuMenu.addAction(self.actionLoad)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionExit)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionAbout)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python ImageMacro - Test Build"))
        __sortingEnabled = self.methodList.isSortingEnabled()
        self.methodList.setSortingEnabled(False)
        item = self.methodList.item(0)
        item.setText(_translate("MainWindow", "test1"))
        item = self.methodList.item(1)
        item.setText(_translate("MainWindow", "test2"))
        item = self.methodList.item(2)
        item.setText(_translate("MainWindow", "test3"))
        self.methodList.setSortingEnabled(__sortingEnabled)
        self.debugCheck.setText(_translate("MainWindow", "DEBUG"))
        self.searchImgNameLabel.setText(_translate("MainWindow", "No Image"))
        self.trialsGroup.setTitle(_translate("MainWindow", "Trials"))
        self.label.setText(_translate("MainWindow", "Count"))
        self.label_3.setText(_translate("MainWindow", "Interval"))
        self.trialsIntervalSpin.setSuffix(_translate("MainWindow", "s"))
        self.searchClickGroup.setTitle(_translate("MainWindow", "Click"))
        self.label_2.setText(_translate("MainWindow", "Count"))
        self.label_4.setText(_translate("MainWindow", "Interval"))
        self.searchClickInterval.setSuffix(_translate("MainWindow", "s"))
        self.searchImgLoadButton.setText(_translate("MainWindow", "Load Img"))
        self.searchImgClearButton.setText(_translate("MainWindow", "Clear Img"))
        self.label_11.setText(_translate("MainWindow", "Precision"))
        self.searchPrecisionSpin.setSuffix(_translate("MainWindow", "%"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.imgTab), _translate("MainWindow", "Search"))
        self.countImgNameLabel.setText(_translate("MainWindow", "No Image"))
        self.countImgLoadButton.setText(_translate("MainWindow", "Load Img"))
        self.countImgClearButton.setText(_translate("MainWindow", "Clear Img"))
        self.countClickGroup.setTitle(_translate("MainWindow", "Click"))
        self.label_7.setText(_translate("MainWindow", "Count"))
        self.label_8.setText(_translate("MainWindow", "Interval"))
        self.clickIntervalSpin_2.setSuffix(_translate("MainWindow", "s"))
        self.label_12.setText(_translate("MainWindow", "Precision"))
        self.countPrecisionSpin.setSuffix(_translate("MainWindow", "%"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Count"))
        self.funcButton.setText(_translate("MainWindow", "Insert"))
        self.waitGroup.setTitle(_translate("MainWindow", "Wait"))
        self.waitSpin.setSuffix(_translate("MainWindow", "s"))
        self.loopGroup.setTitle(_translate("MainWindow", "Loop"))
        self.clickGroup.setTitle(_translate("MainWindow", "Click"))
        self.clickFromImg.setText(_translate("MainWindow", "From Img"))
        self.label_6.setText(_translate("MainWindow", "Y"))
        self.label_5.setText(_translate("MainWindow", "X"))
        self.varGroup.setTitle(_translate("MainWindow", "Variable"))
        self.intRadio.setText(_translate("MainWindow", "Integer"))
        self.doubleRadio.setText(_translate("MainWindow", "Double"))
        self.operatorArg2.setItemText(1, _translate("MainWindow", "="))
        self.calRadio.setText(_translate("MainWindow", "Calculation"))
        self.dragGroup.setTitle(_translate("MainWindow", "Drag"))
        self.dragFromImg.setText(_translate("MainWindow", "From Img"))
        self.label_15.setText(_translate("MainWindow", "From X / Y"))
        self.label_16.setText(_translate("MainWindow", "To    X / Y"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.funcTab), _translate("MainWindow", "Etc"))
        self.outputTextEdit.setPlaceholderText(_translate("MainWindow", "Standby"))
        self.lockLogCheck.setText(_translate("MainWindow", "Lock to Log tab"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.debugTab), _translate("MainWindow", "Log"))
        self.label_9.setText(_translate("MainWindow", "On Success"))
        self.label_10.setText(_translate("MainWindow", "On Fail"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.insertButton.setText(_translate("MainWindow", "Insert"))
        self.editButton.setText(_translate("MainWindow", "Edit"))
        __sortingEnabled = self.sequenceList.isSortingEnabled()
        self.sequenceList.setSortingEnabled(False)
        item = self.sequenceList.item(0)
        item.setText(_translate("MainWindow", "placeholder1"))
        item = self.sequenceList.item(1)
        item.setText(_translate("MainWindow", "placeholder2"))
        self.sequenceList.setSortingEnabled(__sortingEnabled)
        self.delButton.setText(_translate("MainWindow", "Delete"))
        self.downButton.setText(_translate("MainWindow", "Move Down"))
        self.upButton.setText(_translate("MainWindow", "Move Up"))
        self.nameLine.setPlaceholderText(_translate("MainWindow", "Name.."))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionSave.setText(_translate("MainWindow", "Save (ctrl+s)"))
        self.actionLoad.setText(_translate("MainWindow", "Load (ctrl+l)"))
        self.actionExit.setText(_translate("MainWindow", "Exit (ctrl+q)"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
