# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './aboutDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(428, 428)
        self.centralwidget = QtWidgets.QWidget(About)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(410, 410))
        self.frame.setMaximumSize(QtCore.QSize(410, 410))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(-7, 30, 400, 400))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(400, 400))
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(".\\../icons/About.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(129, 3, 281, 281))
        self.textEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEdit.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setLineWrapColumnOrWidth(2)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textEdit.setPlaceholderText("")
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        About.setCentralWidget(self.centralwidget)

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About"))
        self.textEdit.setHtml(_translate("About", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas\'; font-size:11pt; color:#664a26;\">Copyright (c) 2019 jupiterbjy<br /><br />A random hikineet who makes more mistakes than one could accept.<br /><br />Contact me to:<br />nyarukoishi@gmail.com<br /><br />2020-04-04<br />v 0.0.2</span></p></body></html>"))
