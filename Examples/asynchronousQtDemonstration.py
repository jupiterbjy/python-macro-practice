from PySide2.QtWidgets import QWidget, QApplication, QTextEdit, QVBoxLayout, QPushButton
import sys
import threading
import asyncio
from concurrent import futures
import multiprocessing
import time


# Checking which blocks UI activity


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.text = QTextEdit()
        self.aux = QTextEdit()
        self.button_1 = QPushButton('ohno - threading')
        self.button_2 = QPushButton('ohno - asyncio')
        self.button_3 = QPushButton('ohno - concurrent.future')
        self.button_4 = QPushButton('ohno - multiprocessing')
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.aux)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        self.text.textChanged.connect(self.onChange)
        self.button.released.connect(self.threader)

        self.future_pool = futures.ThreadPoolExecutor(1) # n of workers

    def threader(self):

        t = threading.Thread(target=scoot)
        t.start()
        # can't retrieve data without queue, etc.

    def asyncer(self):
        pass

    def futurelam(self):
        output = self.future_pool.submit(scoot, 3)
        print(output)


    def onChange(self):
        self.aux.setText(self.text.toPlainText())


def scoot(n):
    for i in range(n):
        print(i)
        time.sleep(0.5)
    print("Gravity? Who cares about Gravity!")
    return 'Bonk!'

def async_scoot(n):
    for i in range(n):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
