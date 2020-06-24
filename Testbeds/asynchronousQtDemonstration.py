from PySide2.QtWidgets import QWidget, QApplication, QTextEdit, QVBoxLayout, QPushButton
from PySide2.QtCore import QEventLoop
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
        self.button_1_1 = QPushButton('threading stop')
        self.button_2 = QPushButton('ohno - asyncio')
        self.button_3 = QPushButton('ohno - concurrent.future')
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.aux)
        self.layout.addWidget(self.button_1)
        self.layout.addWidget(self.button_1_1)
        self.layout.addWidget(self.button_2)
        self.layout.addWidget(self.button_3)

        self.setLayout(self.layout)
        self.text.textChanged.connect(self.onChange)
        self.button_1.released.connect(self.threader)
        self.button_1_1.released.connect(self.stopper)
        self.button_2.released.connect(self.asyncer)
        self.button_3.released.connect(self.futurelam)

        self.future_pool = futures.ThreadPoolExecutor(1)
        self.event = threading.Event()

    def stopper(self):
        self.event.set()

    def threader(self):
        self.event = threading.Event()
        t = threading.Thread(target=stoppable_scoot, args=[self.event, 7])
        t.start()
        # can't retrieve data without queue, etc.

    def asyncer(self):
        loop = asyncio.get_event_loop()

        with loop:
            a = self.loop.run_until_complete(async_scoot(7))

        print(a)

    def futurelam(self):
        output = self.future_pool.submit(futuristic_scoot, 7)
        print(output)

    def onChange(self):
        self.aux.setText(self.text.toPlainText())


def stoppable_scoot(event: threading.Event, n):
    for i in range(n):
        print(i)
        event.wait(2)
        if event.is_set():
            print('Boinc!')
            break

    print('Gravity? Who cares about Gravity!')
    return 'Bonk!'


def futuristic_scoot(n):
    for i in range(n):
        print(i)
        time.sleep(0.5)
    print("Gravity? Who cares about Gravity!")
    return 'Bonk!'


async def async_scoot(n):
    for i in range(n):
        print(i)
        await asyncio.sleep(0.5)

    print("Gravity? Who cares about Gravity!")
    return 'Bonk!'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
