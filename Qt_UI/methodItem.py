# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Qt_UI/methodItem.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(299, 42)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.ItemIcon = QtWidgets.QLabel(Form)
        self.ItemIcon.setMinimumSize(QtCore.QSize(24, 24))
        self.ItemIcon.setMaximumSize(QtCore.QSize(24, 24))
        self.ItemIcon.setText("")
        self.ItemIcon.setPixmap(QtGui.QPixmap("C:/Users/jupit/Pictures/cg64_2.png"))
        self.ItemIcon.setScaledContents(True)
        self.ItemIcon.setObjectName("ItemIcon")
        self.gridLayout.addWidget(self.ItemIcon, 0, 0, 1, 1)
        self.ItemName = QtWidgets.QLabel(Form)
        self.ItemName.setObjectName("ItemName")
        self.gridLayout.addWidget(self.ItemName, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ItemName.setText(_translate("Form", "TextLabel"))
