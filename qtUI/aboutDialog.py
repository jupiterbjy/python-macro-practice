# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aboutDialog.ui'
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


class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(428, 428)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(About.sizePolicy().hasHeightForWidth())
        About.setSizePolicy(sizePolicy)
        About.setMaximumSize(QSize(428, 428))
        self.centralwidget = QWidget(About)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(410, 410))
        self.frame.setMaximumSize(QSize(410, 410))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(-7, 30, 400, 400))
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(400, 400))
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setFrameShadow(QFrame.Plain)
        self.label.setPixmap(QPixmap(u"../icons/About.png"))
        self.label.setScaledContents(True)
        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(129, 3, 281, 201))
        self.textEdit.setLayoutDirection(Qt.LeftToRight)
        self.textEdit.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setFrameShadow(QFrame.Plain)
        self.textEdit.setLineWrapColumnOrWidth(2)
        self.textEdit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.versionArea = QTextEdit(self.frame)
        self.versionArea.setObjectName(u"versionArea")
        self.versionArea.setGeometry(QRect(240, 200, 171, 61))
        self.versionArea.setLayoutDirection(Qt.LeftToRight)
        self.versionArea.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.versionArea.setFrameShape(QFrame.NoFrame)
        self.versionArea.setFrameShadow(QFrame.Plain)
        self.versionArea.setLineWrapColumnOrWidth(2)
        self.versionArea.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        About.setCentralWidget(self.centralwidget)

        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"About", None))
        self.label.setText("")
        self.textEdit.setHtml(QCoreApplication.translate("About", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Gulim'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas'; font-size:11pt; color:#664a26;\">Copyright (c) 2019 ~ 2020 jupiterbjy<br /></span></p>\n"
"<p align=\"right\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas'; font-size:11pt; color:#664a26;\">Python Image-matching GUI Macro Sequencer Project.<br /><br />Contact me to:<br />nyarukoishi@gmail.com<br /></span></p></body></html>", None))
        self.textEdit.setPlaceholderText("")
        self.versionArea.setHtml(QCoreApplication.translate("About", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Gulim'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas'; font-size:11pt; color:#664a26;\">DATE<br />VERSION</span></p></body></html>", None))
        self.versionArea.setPlaceholderText("")
    # retranslateUi

