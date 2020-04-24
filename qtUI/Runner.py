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


class Ui_RunnerWindow(object):
    def setupUi(self, RunnerWindow):
        if not RunnerWindow.objectName():
            RunnerWindow.setObjectName(u"RunnerWindow")
        RunnerWindow.resize(305, 587)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RunnerWindow.sizePolicy().hasHeightForWidth())
        RunnerWindow.setSizePolicy(sizePolicy)
        RunnerWindow.setMinimumSize(QSize(305, 587))
        RunnerWindow.setMaximumSize(QSize(305, 587))
        RunnerWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(RunnerWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.stopButton = QPushButton(self.frame)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.stopButton, 1, 0, 1, 1)

        self.runButton = QPushButton(self.frame)
        self.runButton.setObjectName(u"runButton")
        sizePolicy1.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.runButton, 0, 0, 1, 1)

        self.fullScreenCheck = QCheckBox(self.frame)
        self.fullScreenCheck.setObjectName(u"fullScreenCheck")

        self.gridLayout.addWidget(self.fullScreenCheck, 0, 1, 1, 1)

        self.dumpImageCheck = QCheckBox(self.frame)
        self.dumpImageCheck.setObjectName(u"dumpImageCheck")

        self.gridLayout.addWidget(self.dumpImageCheck, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.runLine = QLineEdit(self.frame)
        self.runLine.setObjectName(u"runLine")
        self.runLine.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.runLine.sizePolicy().hasHeightForWidth())
        self.runLine.setSizePolicy(sizePolicy2)
        self.runLine.setMinimumSize(QSize(0, 20))
        self.runLine.setMaximumSize(QSize(287, 20))
        self.runLine.setReadOnly(True)

        self.verticalLayout.addWidget(self.runLine)

        self.currentSeq = QListWidget(self.frame)
        self.currentSeq.setObjectName(u"currentSeq")
        sizePolicy2.setHeightForWidth(self.currentSeq.sizePolicy().hasHeightForWidth())
        self.currentSeq.setSizePolicy(sizePolicy2)
        self.currentSeq.setMinimumSize(QSize(267, 70))
        self.currentSeq.setMaximumSize(QSize(287, 70))
        self.currentSeq.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.currentSeq.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.currentSeq.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.currentSeq.setAlternatingRowColors(True)
        self.currentSeq.setMovement(QListView.Static)
        self.currentSeq.setViewMode(QListView.ListMode)
        self.currentSeq.setSelectionRectVisible(True)

        self.verticalLayout.addWidget(self.currentSeq)

        self.historyButton = QPushButton(self.frame)
        self.historyButton.setObjectName(u"historyButton")
        sizePolicy1.setHeightForWidth(self.historyButton.sizePolicy().hasHeightForWidth())
        self.historyButton.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.historyButton)


        self.verticalLayout_2.addWidget(self.frame)

        self.sequenceList = QListWidget(self.centralwidget)
        self.sequenceList.setObjectName(u"sequenceList")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.sequenceList.sizePolicy().hasHeightForWidth())
        self.sequenceList.setSizePolicy(sizePolicy3)
        self.sequenceList.setMaximumSize(QSize(16777215, 16777215))
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

        self.verticalLayout_2.addWidget(self.sequenceList)

        RunnerWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RunnerWindow)

        QMetaObject.connectSlotsByName(RunnerWindow)
    # setupUi

    def retranslateUi(self, RunnerWindow):
        RunnerWindow.setWindowTitle(QCoreApplication.translate("RunnerWindow", u"Macro Controller", None))
        self.stopButton.setText(QCoreApplication.translate("RunnerWindow", u"Stop", None))
        self.runButton.setText(QCoreApplication.translate("RunnerWindow", u"Run", None))
        self.fullScreenCheck.setText(QCoreApplication.translate("RunnerWindow", u"Full Screen", None))
        self.dumpImageCheck.setText(QCoreApplication.translate("RunnerWindow", u"Dump Image", None))
        self.runLine.setPlaceholderText(QCoreApplication.translate("RunnerWindow", u"Standby...", None))
        self.historyButton.setText(QCoreApplication.translate("RunnerWindow", u"Show / Hide History", None))
    # retranslateUi

