# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'methodItem.ui'
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


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(299, 42)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ItemIcon = QLabel(Form)
        self.ItemIcon.setObjectName(u"ItemIcon")
        self.ItemIcon.setMinimumSize(QSize(24, 24))
        self.ItemIcon.setMaximumSize(QSize(24, 24))
        self.ItemIcon.setPixmap(QPixmap(u"C:/Users/jupit/Pictures/cg64_2.png"))
        self.ItemIcon.setScaledContents(True)

        self.gridLayout.addWidget(self.ItemIcon, 0, 0, 1, 1)

        self.ItemName = QLabel(Form)
        self.ItemName.setObjectName(u"ItemName")

        self.gridLayout.addWidget(self.ItemName, 0, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ItemIcon.setText("")
        self.ItemName.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

