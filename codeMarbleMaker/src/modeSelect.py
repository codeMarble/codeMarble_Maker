#-*- coding: utf-8 -*-
"""
    modeSelect.py

    :copyright: Hwang Sek-jin, ngh
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from codeMarbleMaker.src import boardSetting

class ModeSelect(QDialog):
    def __init__(self, ruleData, parent=None):
        QDialog.__init__(self, parent)
        self.ruleData = ruleData

        self.initUI()
        self.initSlot()

    def initSlot(self):
        self.makerBtn.clicked.connect(self.makerSlot)
        self.testerBtn.clicked.connect(self.testerSlot)

    def initUI(self):
        # dialog setting
        width, height = 640, 480
        title = 'Code Marble'

        self.setWindowTitle(title)
        resolution = QDesktopWidget().screenGeometry()
        self.setGeometry((resolution.width() / 2) - (width / 2),
                         (resolution.height() / 2) - (height / 2),
                         width, height)
        self.setFixedSize(width, height)

        # dialog contents
        # maker button
        self.makerBtn = QPushButton()
        self.makerBtn.setFixedSize(200, 80)
        self.makerBtn.setText('maker')

        # tester button
        self.testerBtn = QPushButton()
        self.testerBtn.setFixedSize(200, 80)
        self.testerBtn.setText('tester')

        # main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignHCenter)
        self.mainLayout.setSpacing(70)

        # layout setting
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.makerBtn)
        self.mainLayout.addWidget(self.testerBtn)

    @pyqtSlot()
    def makerSlot(self):
        print('maker slot called!')
        self.setVisible(False)
        self.bs = boardSetting.DialogBoardSetting(self.ruleData, self)
        self.bs.exec()
        self.close()

    @pyqtSlot()
    def testerSlot(self):
        print('tester slot called!')
        msgBox = QMessageBox()
        msgBox.setText('Sorry, function implementing...')
        msgBox.exec()
