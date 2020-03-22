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
        MainWindow.resize(305, 573)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(305, 573))
        MainWindow.setMaximumSize(QtCore.QSize(305, 573))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(287, 321))
        self.tabWidget.setMaximumSize(QtCore.QSize(287, 321))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName("tabWidget")
        self.Sequence = QtWidgets.QWidget()
        self.Sequence.setObjectName("Sequence")
        self.sequenceList = QtWidgets.QListWidget(self.Sequence)
        self.sequenceList.setGeometry(QtCore.QRect(10, 10, 265, 279))
        self.sequenceList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sequenceList.setFrameShadow(QtWidgets.QFrame.Plain)
        self.sequenceList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.sequenceList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sequenceList.setAlternatingRowColors(True)
        self.sequenceList.setMovement(QtWidgets.QListView.Static)
        self.sequenceList.setViewMode(QtWidgets.QListView.ListMode)
        self.sequenceList.setSelectionRectVisible(True)
        self.sequenceList.setObjectName("sequenceList")
        self.tabWidget.addTab(self.Sequence, "")
        self.Log = QtWidgets.QWidget()
        self.Log.setObjectName("Log")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Log)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lockLogCheck = QtWidgets.QCheckBox(self.Log)
        self.lockLogCheck.setObjectName("lockLogCheck")
        self.gridLayout_4.addWidget(self.lockLogCheck, 0, 0, 1, 1)
        self.outputTextEdit = QtWidgets.QTextEdit(self.Log)
        self.outputTextEdit.setStyleSheet("background-color: rgb(30, 30, 30);\n"
"color: rgb(255, 255, 255);")
        self.outputTextEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.outputTextEdit.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outputTextEdit.setLineWidth(0)
        self.outputTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.outputTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.outputTextEdit.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.outputTextEdit.setUndoRedoEnabled(False)
        self.outputTextEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.outputTextEdit.setLineWrapColumnOrWidth(0)
        self.outputTextEdit.setReadOnly(True)
        self.outputTextEdit.setObjectName("outputTextEdit")
        self.gridLayout_4.addWidget(self.outputTextEdit, 1, 0, 1, 1)
        self.tabWidget.addTab(self.Log, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
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
        self.currentSeq.setMinimumSize(QtCore.QSize(267, 70))
        self.currentSeq.setMaximumSize(QtCore.QSize(267, 70))
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
        self.randOffsetSpin = QtWidgets.QSpinBox(self.frame)
        self.randOffsetSpin.setObjectName("randOffsetSpin")
        self.gridLayout.addWidget(self.randOffsetSpin, 2, 1, 1, 1)
        self.randOffsetCheck = QtWidgets.QCheckBox(self.frame)
        self.randOffsetCheck.setObjectName("randOffsetCheck")
        self.gridLayout.addWidget(self.randOffsetCheck, 2, 0, 1, 1)
        self.runButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 0, 0, 1, 1)
        self.StopButton = QtWidgets.QPushButton(self.frame)
        self.StopButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StopButton.sizePolicy().hasHeightForWidth())
        self.StopButton.setSizePolicy(sizePolicy)
        self.StopButton.setObjectName("StopButton")
        self.gridLayout.addWidget(self.StopButton, 0, 1, 1, 1)
        self.fullScreenCheck = QtWidgets.QCheckBox(self.frame)
        self.fullScreenCheck.setObjectName("fullScreenCheck")
        self.gridLayout.addWidget(self.fullScreenCheck, 1, 0, 1, 1)
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Sequence), _translate("MainWindow", "Sequence"))
        self.lockLogCheck.setText(_translate("MainWindow", "Lock to Log tab"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Log), _translate("MainWindow", "Log"))
        self.randOffsetCheck.setText(_translate("MainWindow", "Random Offset"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.StopButton.setText(_translate("MainWindow", "Stop"))
        self.fullScreenCheck.setText(_translate("MainWindow", "Full Screen"))
        self.progressBar.setFormat(_translate("MainWindow", "%vs"))
