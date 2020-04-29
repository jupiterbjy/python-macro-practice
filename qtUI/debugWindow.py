# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'debugWindow.ui'
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


class Ui_DebugWindow(object):
    def setupUi(self, DebugWindow):
        if not DebugWindow.objectName():
            DebugWindow.setObjectName(u"DebugWindow")
        DebugWindow.resize(442, 459)
        self.verticalLayout = QVBoxLayout(DebugWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logSaveCheck = QCheckBox(DebugWindow)
        self.logSaveCheck.setObjectName(u"logSaveCheck")

        self.verticalLayout.addWidget(self.logSaveCheck)

        self.tabWidget = QTabWidget(DebugWindow)
        self.tabWidget.setObjectName(u"tabWidget")
        self.Log = QWidget()
        self.Log.setObjectName(u"Log")
        self.verticalLayout_3 = QVBoxLayout(self.Log)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.logOutput = QTextEdit(self.Log)
        self.logOutput.setObjectName(u"logOutput")
        self.logOutput.setStyleSheet(u"background-color: rgb(30, 30, 30);\n"
"color: rgb(230, 230, 230);\n"
"selection-color: rgb(30, 30, 30);\n"
"selection-background-color: rgb(30, 30, 30);\n"
"gridline-color: rgb(30, 30, 30);")
        self.logOutput.setFrameShape(QFrame.NoFrame)
        self.logOutput.setUndoRedoEnabled(False)
        self.logOutput.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.logOutput)

        self.tabWidget.addTab(self.Log, "")
        self.Debug = QWidget()
        self.Debug.setObjectName(u"Debug")
        self.verticalLayout_2 = QVBoxLayout(self.Debug)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.debugOutput = QTextEdit(self.Debug)
        self.debugOutput.setObjectName(u"debugOutput")
        self.debugOutput.setStyleSheet(u"background-color: rgb(30, 30, 30);\n"
"color: rgb(230, 230, 230);\n"
"selection-color: rgb(30, 30, 30);\n"
"selection-background-color: rgb(30, 30, 30);\n"
"gridline-color: rgb(30, 30, 30);")
        self.debugOutput.setFrameShape(QFrame.NoFrame)
        self.debugOutput.setUndoRedoEnabled(False)
        self.debugOutput.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.debugOutput)

        self.commandLine = QLineEdit(self.Debug)
        self.commandLine.setObjectName(u"commandLine")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLine.sizePolicy().hasHeightForWidth())
        self.commandLine.setSizePolicy(sizePolicy)
        self.commandLine.setMinimumSize(QSize(0, 22))
        self.commandLine.setCursor(QCursor(Qt.IBeamCursor))
        self.commandLine.setStyleSheet(u"background-color: rgb(30, 30, 30);\n"
"color: rgb(230, 230, 230);\n"
"selection-color: rgb(30, 30, 30);\n"
"selection-background-color: rgb(30, 30, 30);\n"
"gridline-color: rgb(30, 30, 30);")
        self.commandLine.setFrame(False)
        self.commandLine.setClearButtonEnabled(False)

        self.verticalLayout_2.addWidget(self.commandLine)

        self.tabWidget.addTab(self.Debug, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(DebugWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DebugWindow)
    # setupUi

    def retranslateUi(self, DebugWindow):
        DebugWindow.setWindowTitle(QCoreApplication.translate("DebugWindow", u"Debugger", None))
        self.logSaveCheck.setText(QCoreApplication.translate("DebugWindow", u"Save to file on Exit", None))
        self.logOutput.setPlaceholderText(QCoreApplication.translate("DebugWindow", u"Standby..", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Log), QCoreApplication.translate("DebugWindow", u"Log", None))
        self.debugOutput.setPlaceholderText(QCoreApplication.translate("DebugWindow", u"Standby..", None))
        self.commandLine.setInputMask("")
        self.commandLine.setPlaceholderText(QCoreApplication.translate("DebugWindow", u"type 'help' for commands..", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Debug), QCoreApplication.translate("DebugWindow", u"Debug", None))
    # retranslateUi

