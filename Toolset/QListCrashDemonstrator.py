from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


class Ui_MainWindow(object):        # Ignore this, just UI generation.
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
        self.currentSeq.setMaximumSize(QSize(267, 70))
        self.gridLayout.addWidget(self.currentSeq, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.runButton.setText('Run')
        self.crashCheck.setText('Check this and Run to Crash')


class Wait:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def action():
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)
        loop.exec_()


class SeqItemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.textLayOut = QVBoxLayout()
        self.textUpLabel = QLabel()
        self.textLayOut.addWidget(self.textUpLabel)
        self.setLayout(self.textLayOut)

    def setup(self, t_up):
        self.textUpLabel.setText(t_up)


class SubWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(SubWindow, self).__init__(parent)
        self.setupUi(self)

        self.source = [Wait('3'), Wait('2'), Wait('1')]

        self.updateHistory(self.source[0])
        self.runButton.released.connect(self.runSeq)

    def GenerateItemWidget(self, target):

        item = SeqItemWidget()
        item.setup(target.name)

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
            self.GenerateItemWidget(item)

    def runSeq(self):
        self.sequenceList.clear()
        self.currentSeq.clear()

        for i in self.source:
            self.updateHistory(i)
            i.action()

        if self.crashCheck.isChecked():     # << crashes here with DLL error
            self.updateHistory()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubWindow()
    window.show()
    sys.exit(app.exec())
