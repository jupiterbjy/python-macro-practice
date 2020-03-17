
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from Toolset import QtTools, FrozenDetect, ObjectDispatch
from ImageModule import getCaptureArea
from Qt_UI.Runner import Ui_MainWindow
from Toolset.Tools import nameCaller
import pyautogui
import MacroMethods


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, seq=None):
        super(MainWindow, self).__init__(parent)

        if seq is not None:
            self.source = list(seq)

    def runSeq(self, full_screen=False):

        MacroMethods.NextSetter(self.seqStorage)
        # self.waitProgressBar
        nameCaller()

        if not full_screen:
            area = getCaptureArea()

            self.runLine.setText(str(area))

            for obj in self.seqStorage:
                obj.setArea(*area)

        try:
            self.runLine.setText('Macro started.')
            obj = self.seqStorage[0].action()

        except IndexError:
            print('└ sequence Empty')
            self.runLine.setText('Nothing To play.')
            return False
        except pyautogui.FailSafeException:
            print('└ FailSafe Trigger')
            self.runLine.setText('Cannot Click (0,0), Aborted.')

        else:
            seq_count = 0
            while obj:
                self.runLine.setText(f'running {obj.name}.')
                obj = obj()
                seq_count += 1

            self.runLine.setText('Macro finished.')
