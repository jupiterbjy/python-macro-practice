# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './pymacro.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
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
        self.waitProgressBar = QtWidgets.QProgressBar(self.frame_3)
        self.waitProgressBar.setAutoFillBackground(False)
        self.waitProgressBar.setProperty("value", 0)
        self.waitProgressBar.setTextVisible(False)
        self.waitProgressBar.setInvertedAppearance(False)
        self.waitProgressBar.setObjectName("waitProgressBar")
        self.gridLayout_3.addWidget(self.waitProgressBar, 3, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(251, 370))
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
        self.trialsGroup.setGeometry(QtCore.QRect(130, 200, 101, 131))
        self.trialsGroup.setObjectName("trialsGroup")
        self.label = QtWidgets.QLabel(self.trialsGroup)
        self.label.setGeometry(QtCore.QRect(15, 20, 81, 20))
        self.label.setObjectName("label")
        self.trialsCountSpin = QtWidgets.QSpinBox(self.trialsGroup)
        self.trialsCountSpin.setGeometry(QtCore.QRect(15, 40, 71, 21))
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
        self.searchClickGroup.setCheckable(True)
        self.searchClickGroup.setChecked(False)
        self.searchClickGroup.setObjectName("searchClickGroup")
        self.label_2 = QtWidgets.QLabel(self.searchClickGroup)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 81, 20))
        self.label_2.setObjectName("label_2")
        self.clickCountSpin = QtWidgets.QSpinBox(self.searchClickGroup)
        self.clickCountSpin.setGeometry(QtCore.QRect(20, 40, 71, 21))
        self.clickCountSpin.setObjectName("clickCountSpin")
        self.label_4 = QtWidgets.QLabel(self.searchClickGroup)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 81, 20))
        self.label_4.setObjectName("label_4")
        self.clickIntervalSpin = QtWidgets.QDoubleSpinBox(self.searchClickGroup)
        self.clickIntervalSpin.setGeometry(QtCore.QRect(20, 90, 71, 21))
        self.clickIntervalSpin.setMaximum(10000.0)
        self.clickIntervalSpin.setSingleStep(0.05)
        self.clickIntervalSpin.setProperty("value", 0.2)
        self.clickIntervalSpin.setObjectName("clickIntervalSpin")
        self.searchImgLoadButton = QtWidgets.QPushButton(self.imgTab)
        self.searchImgLoadButton.setGeometry(QtCore.QRect(161, 164, 75, 23))
        self.searchImgLoadButton.setObjectName("searchImgLoadButton")
        self.searchImgClearButton = QtWidgets.QPushButton(self.imgTab)
        self.searchImgClearButton.setGeometry(QtCore.QRect(80, 164, 75, 23))
        self.searchImgClearButton.setObjectName("searchImgClearButton")
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
        self.loopCountSpin.setObjectName("loopCountSpin")
        self.clickGroup = QtWidgets.QGroupBox(self.funcTab)
        self.clickGroup.setGeometry(QtCore.QRect(10, 130, 91, 161))
        self.clickGroup.setObjectName("clickGroup")
        self.coordFromImg = QtWidgets.QPushButton(self.clickGroup)
        self.coordFromImg.setGeometry(QtCore.QRect(10, 120, 71, 21))
        self.coordFromImg.setObjectName("coordFromImg")
        self.ySpin = QtWidgets.QSpinBox(self.clickGroup)
        self.ySpin.setGeometry(QtCore.QRect(10, 90, 71, 21))
        self.ySpin.setObjectName("ySpin")
        self.label_6 = QtWidgets.QLabel(self.clickGroup)
        self.label_6.setGeometry(QtCore.QRect(10, 70, 81, 20))
        self.label_6.setObjectName("label_6")
        self.xSpin = QtWidgets.QSpinBox(self.clickGroup)
        self.xSpin.setGeometry(QtCore.QRect(10, 40, 71, 21))
        self.xSpin.setObjectName("xSpin")
        self.label_5 = QtWidgets.QLabel(self.clickGroup)
        self.label_5.setGeometry(QtCore.QRect(10, 20, 81, 20))
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.funcTab, "")
        self.debugTab = QtWidgets.QWidget()
        self.debugTab.setObjectName("debugTab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.debugTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.outputTextEdit = QtWidgets.QTextEdit(self.debugTab)
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
        self.gridLayout_6.addWidget(self.outputTextEdit, 0, 0, 1, 1)
        self.tabWidget.addTab(self.debugTab, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.editButton = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editButton.sizePolicy().hasHeightForWidth())
        self.editButton.setSizePolicy(sizePolicy)
        self.editButton.setObjectName("editButton")
        self.gridLayout_5.addWidget(self.editButton, 0, 1, 1, 1)
        self.insertButton = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.insertButton.sizePolicy().hasHeightForWidth())
        self.insertButton.setSizePolicy(sizePolicy)
        self.insertButton.setObjectName("insertButton")
        self.gridLayout_5.addWidget(self.insertButton, 0, 0, 1, 1)
        self.runButton = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setObjectName("runButton")
        self.gridLayout_5.addWidget(self.runButton, 3, 0, 1, 1)
        self.StopButton = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StopButton.sizePolicy().hasHeightForWidth())
        self.StopButton.setSizePolicy(sizePolicy)
        self.StopButton.setObjectName("StopButton")
        self.gridLayout_5.addWidget(self.StopButton, 3, 1, 1, 1)
        self.randOffsetCheck = QtWidgets.QCheckBox(self.frame_3)
        self.randOffsetCheck.setObjectName("randOffsetCheck")
        self.gridLayout_5.addWidget(self.randOffsetCheck, 4, 0, 1, 1)
        self.randOffsetSpin = QtWidgets.QSpinBox(self.frame_3)
        self.randOffsetSpin.setObjectName("randOffsetSpin")
        self.gridLayout_5.addWidget(self.randOffsetSpin, 4, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_5, 1, 0, 1, 1)
        self.runLine = QtWidgets.QLineEdit(self.frame_3)
        self.runLine.setReadOnly(True)
        self.runLine.setObjectName("runLine")
        self.gridLayout_3.addWidget(self.runLine, 2, 0, 1, 1)
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
        self.sequenceList = QtWidgets.QListWidget(self.frame)
        self.sequenceList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.sequenceList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
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
        self.gridLayout_4.addWidget(self.splitter, 0, 0, 1, 1)
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
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuMenu.addAction(self.actionSave)
        self.menuMenu.addAction(self.actionLoad)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionExit)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionHelp)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
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
        self.searchImgNameLabel.setText(_translate("MainWindow", "No Image"))
        self.trialsGroup.setTitle(_translate("MainWindow", "Trials"))
        self.label.setText(_translate("MainWindow", "Count"))
        self.label_3.setText(_translate("MainWindow", "Interval"))
        self.trialsIntervalSpin.setSuffix(_translate("MainWindow", "s"))
        self.searchClickGroup.setTitle(_translate("MainWindow", "Click"))
        self.label_2.setText(_translate("MainWindow", "Count"))
        self.label_4.setText(_translate("MainWindow", "Interval"))
        self.clickIntervalSpin.setSuffix(_translate("MainWindow", "s"))
        self.searchImgLoadButton.setText(_translate("MainWindow", "Load Img"))
        self.searchImgClearButton.setText(_translate("MainWindow", "Clear Img"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.imgTab), _translate("MainWindow", "Search"))
        self.countImgNameLabel.setText(_translate("MainWindow", "No Image"))
        self.countImgLoadButton.setText(_translate("MainWindow", "Load Img"))
        self.countImgClearButton.setText(_translate("MainWindow", "Clear Img"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Count"))
        self.funcButton.setText(_translate("MainWindow", "Insert"))
        self.waitGroup.setTitle(_translate("MainWindow", "Wait"))
        self.waitSpin.setSuffix(_translate("MainWindow", "s"))
        self.loopGroup.setTitle(_translate("MainWindow", "Loop"))
        self.clickGroup.setTitle(_translate("MainWindow", "Click"))
        self.coordFromImg.setText(_translate("MainWindow", "From Img"))
        self.label_6.setText(_translate("MainWindow", "Y"))
        self.label_5.setText(_translate("MainWindow", "X"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.funcTab), _translate("MainWindow", "Etc"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.debugTab), _translate("MainWindow", "Console"))
        self.editButton.setText(_translate("MainWindow", "Edit"))
        self.insertButton.setText(_translate("MainWindow", "Insert"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.StopButton.setText(_translate("MainWindow", "Stop"))
        self.randOffsetCheck.setText(_translate("MainWindow", "Random Offset"))
        self.delButton.setText(_translate("MainWindow", "Delete"))
        self.downButton.setText(_translate("MainWindow", "Move Down"))
        self.upButton.setText(_translate("MainWindow", "Move Up"))
        self.nameLine.setPlaceholderText(_translate("MainWindow", "Name.."))
        __sortingEnabled = self.sequenceList.isSortingEnabled()
        self.sequenceList.setSortingEnabled(False)
        item = self.sequenceList.item(0)
        item.setText(_translate("MainWindow", "placeholder1"))
        item = self.sequenceList.item(1)
        item.setText(_translate("MainWindow", "placeholder2"))
        self.sequenceList.setSortingEnabled(__sortingEnabled)
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionSave.setText(_translate("MainWindow", "Save (ctrl+s)"))
        self.actionLoad.setText(_translate("MainWindow", "Load (ctrl+l)"))
        self.actionExit.setText(_translate("MainWindow", "Exit (ctrl+q)"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
