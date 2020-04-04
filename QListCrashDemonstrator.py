from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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
        print(i)
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
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(287, 382)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.sequenceList = QListWidget(self.centralwidget)
        self.sequenceList.setObjectName("sequenceList")
        self.gridLayout.addWidget(self.sequenceList, 0, 0, 1, 1)
        self.runButton = QPushButton(self.centralwidget)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 1, 0, 1, 1)
        self.currentSeq = QListWidget(self.centralwidget)
        self.currentSeq.setMinimumSize(QSize(267, 70))
        self.currentSeq.setMaximumSize(QSize(267, 70))
        self.currentSeq.setObjectName("currentSeq")
        self.gridLayout.addWidget(self.currentSeq, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.runButton.setText(_translate("MainWindow", "Run"))


class SeqItemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.textLayOut = QVBoxLayout()
        self.textUpLabel = QLabel()
        self.textDownLabel = QLabel()
        self.textLayOut.addWidget(self.textUpLabel)
        self.textLayOut.addWidget(self.textDownLabel)
        self.allHBoxLayOut = QHBoxLayout()
        self.iconLabel = QLabel()
        self.iconLabel.setMinimumSize(QSize(48, 48))
        self.iconLabel.setMaximumSize(QSize(48, 48))
        self.allHBoxLayOut.addWidget(self.iconLabel)
        self.allHBoxLayOut.addLayout(self.textLayOut, 1)
        self.setLayout(self.allHBoxLayOut)

    def setup(self, t_up, t_down):
        self.textUpLabel.setText(t_up)
        self.textDownLabel.setText(t_down)


def setPix(image):
    if isinstance(image, str):
        return QPixmap(image)
    else:
        tmp = ImageQt(image).copy()
        return QPixmap(tmp)


def AddToListWidget(tgt, item_list_widget):

    item = SeqItemWidget()
    item.setup(tgt.name, str(type(tgt).__name__ + 'Object'))

    list_item = QListWidgetItem(item_list_widget)
    list_item.setSizeHint(item.sizeHint())

    item_list_widget.addItem(list_item)
    item_list_widget.setItemWidget(list_item, item)


class SubWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(SubWindow, self).__init__(parent)
        self.setupUi(self)

        self.source = testcase_generate()
        self.updateHistory(self.source[0])
        self.runButton.released.connect(self.runSeq)

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
            AddToListWidget(item, self.currentSeq)

    def runSeq(self):
        print('called')

        self.sequenceList.clear()
        self.currentSeq.clear()

        obj = self.source[0]

        while obj:
            self.updateHistory(obj)
            obj = obj.run()
        else:
            self.updateHistory()    # uncomment this to cause QWidget vaporization.
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubWindow()
    window.show()
    sys.exit(app.exec())

    # https://stackoverflow.com/questions/60908741/