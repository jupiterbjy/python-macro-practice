# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Runner.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(305, 554)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(305, 528))
        MainWindow.setMaximumSize(QtCore.QSize(305, 554))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 321))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 321))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.Sequence = QtWidgets.QWidget()
        self.Sequence.setObjectName("Sequence")
        self.sequenceList = QtWidgets.QListWidget(self.Sequence)
        self.sequenceList.setGeometry(QtCore.QRect(10, 10, 265, 279))
        self.sequenceList.setFrameShape(QtWidgets.QFrame.Box)
        self.sequenceList.setFrameShadow(QtWidgets.QFrame.Raised)
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
        self.tabWidget.addTab(self.Sequence, "")
        self.Log = QtWidgets.QWidget()
        self.Log.setObjectName("Log")
        self.outputTextEdit = QtWidgets.QTextEdit(self.Log)
        self.outputTextEdit.setGeometry(QtCore.QRect(10, 10, 265, 279))
        self.outputTextEdit.setFrameShape(QtWidgets.QFrame.Box)
        self.outputTextEdit.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outputTextEdit.setLineWidth(1)
        self.outputTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.outputTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.outputTextEdit.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.outputTextEdit.setUndoRedoEnabled(False)
        self.outputTextEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.outputTextEdit.setLineWrapColumnOrWidth(0)
        self.outputTextEdit.setReadOnly(True)
        self.outputTextEdit.setObjectName("outputTextEdit")
        self.tabWidget.addTab(self.Log, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.currentSeq = QtWidgets.QListWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currentSeq.sizePolicy().hasHeightForWidth())
        self.currentSeq.setSizePolicy(sizePolicy)
        self.currentSeq.setMinimumSize(QtCore.QSize(267, 51))
        self.currentSeq.setMaximumSize(QtCore.QSize(267, 51))
        self.currentSeq.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.currentSeq.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.currentSeq.setAlternatingRowColors(True)
        self.currentSeq.setMovement(QtWidgets.QListView.Static)
        self.currentSeq.setViewMode(QtWidgets.QListView.ListMode)
        self.currentSeq.setSelectionRectVisible(True)
        self.currentSeq.setObjectName("currentSeq")
        self.gridLayout_2.addWidget(self.currentSeq, 0, 0, 1, 1)
        self.runLine = QtWidgets.QLineEdit(self.frame)
        self.runLine.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runLine.sizePolicy().hasHeightForWidth())
        self.runLine.setSizePolicy(sizePolicy)
        self.runLine.setMinimumSize(QtCore.QSize(267, 20))
        self.runLine.setMaximumSize(QtCore.QSize(267, 20))
        self.runLine.setReadOnly(True)
        self.runLine.setObjectName("runLine")
        self.gridLayout_2.addWidget(self.runLine, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.randOffsetCheck = QtWidgets.QCheckBox(self.frame)
        self.randOffsetCheck.setObjectName("randOffsetCheck")
        self.gridLayout.addWidget(self.randOffsetCheck, 2, 0, 1, 1)
        self.randOffsetSpin = QtWidgets.QSpinBox(self.frame)
        self.randOffsetSpin.setObjectName("randOffsetSpin")
        self.gridLayout.addWidget(self.randOffsetSpin, 2, 1, 1, 1)
        self.StopButton = QtWidgets.QPushButton(self.frame)
        self.StopButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StopButton.sizePolicy().hasHeightForWidth())
        self.StopButton.setSizePolicy(sizePolicy)
        self.StopButton.setObjectName("StopButton")
        self.gridLayout.addWidget(self.StopButton, 0, 1, 1, 1)
        self.runButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 0, 0, 1, 1)
        self.skipButton = QtWidgets.QPushButton(self.frame)
        self.skipButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.skipButton.sizePolicy().hasHeightForWidth())
        self.skipButton.setSizePolicy(sizePolicy)
        self.skipButton.setObjectName("skipButton")
        self.gridLayout.addWidget(self.skipButton, 1, 0, 1, 1)
        self.pauseButton = QtWidgets.QPushButton(self.frame)
        self.pauseButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pauseButton.sizePolicy().hasHeightForWidth())
        self.pauseButton.setSizePolicy(sizePolicy)
        self.pauseButton.setObjectName("pauseButton")
        self.gridLayout.addWidget(self.pauseButton, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setMaximum(50)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.sequenceList.isSortingEnabled()
        self.sequenceList.setSortingEnabled(False)
        item = self.sequenceList.item(0)
        item.setText(_translate("MainWindow", "placeholder1"))
        item = self.sequenceList.item(1)
        item.setText(_translate("MainWindow", "placeholder2"))
        self.sequenceList.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Sequence), _translate("MainWindow", "Sequence"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Log), _translate("MainWindow", "Log"))
        self.randOffsetCheck.setText(_translate("MainWindow", "Random Offset"))
        self.StopButton.setText(_translate("MainWindow", "Stop"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.skipButton.setText(_translate("MainWindow", "Skip"))
        self.pauseButton.setText(_translate("MainWindow", "Pause"))
        self.progressBar.setFormat(_translate("MainWindow", "%vs"))
