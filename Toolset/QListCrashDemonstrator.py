from PyQt5.QtCore import QTimer, QEventLoop, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QWidget, QGridLayout, QListWidgetItem, QListWidget, QApplication,\
                            QVBoxLayout, QPushButton, QLabel, QCheckBox, QMainWindow
from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt
import sys


def QSleep(delay):
    loop = QEventLoop()
    QTimer.singleShot(delay * 1000, loop.quit)
    loop.exec_()


class Wait:
    def __init__(self, name):
        self.delay = 1
        self.next = None
        self.name = name

    def action(self):
        QSleep(self.delay)
        return True

    def run(self):
        if self.action():
            return self.next


def testcase_generate():
    seq = []
    for i in range(3):
        obj = Wait(str(i))
        seq.append(obj)

    for idx, obj in enumerate(seq):
        try:
            obj.next = seq[idx + 1]
        except IndexError:
            pass

    return seq


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.centralwidget = QWidget(MainWindow)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.sequenceList = QListWidget(self.centralwidget)
        self.gridLayout.addWidget(self.sequenceList, 0, 0, 1, 1)
        self.runButton = QPushButton(self.centralwidget)
        self.crashCheck = QCheckBox(self.centralwidget)
        self.gridLayout.addWidget(self.runButton, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.crashCheck, 2, 0, 1, 1)
        self.currentSeq = QListWidget(self.centralwidget)
        self.currentSeq.setMinimumSize(QSize(267, 70))
        self.currentSeq.setMaximumSize(QSize(267, 70))
        self.gridLayout.addWidget(self.currentSeq, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.crashCheck.setText(_translate("MainWindow", "Crash"))


class SeqItemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.textLayOut = QVBoxLayout()
        self.textUpLabel = QLabel()
        self.textDownLabel = QLabel()
        self.textLayOut.addWidget(self.textUpLabel)
        self.textLayOut.addWidget(self.textDownLabel)
        self.setLayout(self.textLayOut)

    def setup(self, t_up, t_down):
        self.textUpLabel.setText(t_up)
        self.textDownLabel.setText(t_down)


def setPix(image):
    if isinstance(image, str):
        return QPixmap(image)

    tmp = ImageQt(image).copy()
    return QPixmap(tmp)


class SubWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(SubWindow, self).__init__(parent)
        self.setupUi(self)

        self.source = testcase_generate()
        self.updateHistory(self.source[0])
        self.runButton.released.connect(self.runSeq)

    def AddToListWidget(self, target):

        item = SeqItemWidget()
        item.setup(target.name, 'Test')

        list_item = QListWidgetItem(self.currentSeq)
        list_item.setSizeHint(item.sizeHint())

        self.currentSeq.addItem(list_item)
        self.currentSeq.setItemWidget(list_item, item)

    def updateHistory(self, item=None):
        widget = self.currentSeq.itemWidget(self.currentSeq.item(0))

        try:
            size = widget.sizeHint()
        except AttributeError:
            pass
        else:
            new = QListWidgetItem(self.sequenceList)
            new.setSizeHint(size)

            self.sequenceList.addItem(new)
            self.sequenceList.setItemWidget(new, widget)
            self.currentSeq.clear()

        if item:
            self.AddToListWidget(item)

    def runSeq(self):
        self.sequenceList.clear()
        self.currentSeq.clear()
        obj = self.source[0]

        while obj:
            self.updateHistory(obj)
            obj = obj.run()

        if self.crashCheck.isChecked():
            self.updateHistory()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubWindow()
    window.show()
    sys.exit(app.exec())
