import os
import sys

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

from codeMarbleMaker import config
from codeMarbleMaker.src import boardSetting

class ModeSelect(QtWidgets.QDialog):
    def __init__(self, ruleData, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.modeSelect = uic.loadUi(os.path.join(config.config.ROOT_PATH, 'modeSelect.ui'), self)
        self.ruleData = ruleData

        self.modeSelect.makerBtn.clicked.connect(self.makerSlot)
        self.modeSelect.testerBtn.clicked.connect(self.testerSlot)

    @pyqtSlot()
    def makerSlot(self):
        print('maker calling...')
        self.boardSetting = boardSetting.BoardSetting(self.ruleData)
        self.modeSelect.close()
        self.boardSetting.exec_()
        # print(self.boardSetting.boardSize)

    @pyqtSlot()
    def testerSlot(self):
        print('tester calling...')
