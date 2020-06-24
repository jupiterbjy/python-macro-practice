from PySide2.QtWidgets import QWidget, QApplication, QTextEdit, QVBoxLayout
import sys


# Test bed for StackOverFlow Qt-related questions


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.text = QTextEdit()
        self.aux = QTextEdit()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.aux)

        self.setLayout(self.layout)
        self.text.textChanged.connect(self.onChange)

    def onChange(self):
        self.aux.setText(self.text.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
