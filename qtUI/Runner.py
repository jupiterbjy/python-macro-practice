# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Runner.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(305, 587)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(305, 587))
        MainWindow.setMaximumSize(QSize(305, 587))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QSize(287, 321))
        self.tabWidget.setMaximumSize(QSize(287, 321))
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.History = QWidget()
        self.History.setObjectName(u"History")
        self.sequenceList = QListWidget(self.History)
        self.sequenceList.setObjectName(u"sequenceList")
        self.sequenceList.setGeometry(QRect(10, 10, 265, 279))
        self.sequenceList.setFrameShape(QFrame.NoFrame)
        self.sequenceList.setFrameShadow(QFrame.Plain)
        self.sequenceList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.sequenceList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sequenceList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sequenceList.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.sequenceList.setDefaultDropAction(Qt.IgnoreAction)
        self.sequenceList.setAlternatingRowColors(True)
        self.sequenceList.setMovement(QListView.Static)
        self.sequenceList.setFlow(QListView.TopToBottom)
        self.sequenceList.setViewMode(QListView.ListMode)
        self.sequenceList.setSelectionRectVisible(True)
        self.tabWidget.addTab(self.History, "")
        self.Log = QWidget()
        self.Log.setObjectName(u"Log")
        self.gridLayout_4 = QGridLayout(self.Log)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.lockLogCheck = QCheckBox(self.Log)
        self.lockLogCheck.setObjectName(u"lockLogCheck")

        self.gridLayout_4.addWidget(self.lockLogCheck, 0, 0, 1, 1)

        self.outputTextEdit = QTextEdit(self.Log)
        self.outputTextEdit.setObjectName(u"outputTextEdit")
        self.outputTextEdit.setStyleSheet(u"background-color: rgb(30, 30, 30);\n"
"color: rgb(255, 255, 255);")
        self.outputTextEdit.setFrameShape(QFrame.NoFrame)
        self.outputTextEdit.setFrameShadow(QFrame.Raised)
        self.outputTextEdit.setLineWidth(0)
        self.outputTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.outputTextEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.outputTextEdit.setAutoFormatting(QTextEdit.AutoNone)
        self.outputTextEdit.setUndoRedoEnabled(False)
        self.outputTextEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.outputTextEdit.setLineWrapColumnOrWidth(0)
        self.outputTextEdit.setReadOnly(True)

        self.gridLayout_4.addWidget(self.outputTextEdit, 1, 0, 1, 1)

        self.tabWidget.addTab(self.Log, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.currentSeq = QListWidget(self.frame)
        self.currentSeq.setObjectName(u"currentSeq")
        sizePolicy.setHeightForWidth(self.currentSeq.sizePolicy().hasHeightForWidth())
        self.currentSeq.setSizePolicy(sizePolicy)
        self.currentSeq.setMinimumSize(QSize(267, 70))
        self.currentSeq.setMaximumSize(QSize(267, 70))
        self.currentSeq.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.currentSeq.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.currentSeq.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.currentSeq.setAlternatingRowColors(True)
        self.currentSeq.setMovement(QListView.Static)
        self.currentSeq.setViewMode(QListView.ListMode)
        self.currentSeq.setSelectionRectVisible(True)

        self.gridLayout_2.addWidget(self.currentSeq, 0, 0, 1, 1)

        self.runLine = QLineEdit(self.frame)
        self.runLine.setObjectName(u"runLine")
        self.runLine.setEnabled(True)
        sizePolicy.setHeightForWidth(self.runLine.sizePolicy().hasHeightForWidth())
        self.runLine.setSizePolicy(sizePolicy)
        self.runLine.setMinimumSize(QSize(267, 20))
        self.runLine.setMaximumSize(QSize(267, 20))
        self.runLine.setReadOnly(True)

        self.gridLayout_2.addWidget(self.runLine, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.fullScreenCheck = QCheckBox(self.frame)
        self.fullScreenCheck.setObjectName(u"fullScreenCheck")

        self.gridLayout.addWidget(self.fullScreenCheck, 1, 0, 1, 1)

        self.runButton = QPushButton(self.frame)
        self.runButton.setObjectName(u"runButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.runButton, 0, 0, 1, 1)

        self.StopButton = QPushButton(self.frame)
        self.StopButton.setObjectName(u"StopButton")
        self.StopButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.StopButton.sizePolicy().hasHeightForWidth())
        self.StopButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.StopButton, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 1)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(50)
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setTextDirection(QProgressBar.TopToBottom)

        self.gridLayout_2.addWidget(self.progressBar, 2, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.History), QCoreApplication.translate("MainWindow", u"History", None))
        self.lockLogCheck.setText(QCoreApplication.translate("MainWindow", u"Lock to Log tab", None))
        self.outputTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Standby", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Log), QCoreApplication.translate("MainWindow", u"Log", None))
        self.fullScreenCheck.setText(QCoreApplication.translate("MainWindow", u"Full Screen", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.StopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.progressBar.setFormat(QCoreApplication.translate("MainWindow", u"%vs", None))
    # retranslateUi

