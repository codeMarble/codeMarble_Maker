#-*- coding: utf-8 -*-
"""
    boardSetting.py

    :copyright: Hwang Sek-jin, ngh
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from codeMarbleMaker.src.settingVariable import *

class DialogBoardSetting(QDialog):
    def __init__(self, ruleData, parent):
        QDialog.__init__(self, parent)
        self.ruleData = ruleData
        self.boardSize = ''
        self.placement = ''
        self.bgImageUrl = ''

        self.initUI()
        self.initSlot()

    def initUI(self):
        # dialog setting
        width, height = 640, 400
        title = 'Code Marble - board setting'

        self.setWindowTitle(title)
        resolution = QDesktopWidget().screenGeometry()
        self.setGeometry((resolution.width() / 2) - (width / 2),
                         (resolution.height() / 2) - (height / 2),
                         width, height)
        self.setFixedSize(width, height)

        # board size
        self.radioBoardSize1 = QRadioButton(BoardSetting.size1)
        self.radioBoardSize2 = QRadioButton(BoardSetting.size2)
        self.layBoardSize = QHBoxLayout()
        self.layBoardSize.addWidget(self.radioBoardSize1)
        self.layBoardSize.addWidget(self.radioBoardSize2)
        self.boxBoardSize = QGroupBox('board size')
        self.boxBoardSize.setLayout(self.layBoardSize)

        # placement point
        self.radioPlacement1 = QRadioButton(BoardSetting.placement1)
        self.radioPlacement2 = QRadioButton(BoardSetting.placement2)
        self.layPlacement = QHBoxLayout()
        self.layPlacement.addWidget(self.radioPlacement1)
        self.layPlacement.addWidget(self.radioPlacement2)
        self.boxPlacement = QGroupBox('placement point')
        self.boxPlacement.setLayout(self.layPlacement)

        # background image
        self.lblBackGroundImage = QLabel()
        self.lblBackGroundImage.setFixedSize(300, 300)
        self.btnImageBrowse = QPushButton('browse')
        self.layBackgroundImage = QHBoxLayout()
        self.layBackgroundImage.addWidget(self.lblBackGroundImage)
        self.layBackgroundImage.addWidget(self.btnImageBrowse)
        self.boxBackgroundImage = QGroupBox('background image')
        self.boxBackgroundImage.setLayout(self.layBackgroundImage)

        # board setting layout
        self.layBoardSetting = QVBoxLayout()
        self.layBoardSetting.addWidget(self.boxBoardSize)
        self.layBoardSetting.setStretchFactor(self.boxBoardSize, 1)
        self.layBoardSetting.addWidget(self.boxPlacement)
        self.layBoardSetting.setStretchFactor(self.boxPlacement, 1)
        self.layBoardSetting.addWidget(self.boxBackgroundImage)
        self.layBoardSetting.setStretchFactor(self.boxBackgroundImage, 3)

        # confirm button
        self.btnConfirm = QPushButton('OK')
        self.layConfirm = QVBoxLayout()
        self.layConfirm.addWidget(self.btnConfirm)
        self.layConfirm.setAlignment(Qt.AlignBottom)

        # main layout
        self.layMain = QHBoxLayout()
        self.layMain.addLayout(self.layBoardSetting)
        self.layMain.setStretchFactor(self.layBoardSetting, 3)
        self.layMain.addLayout(self.layConfirm)
        self.layMain.setStretchFactor(self.layConfirm, 1)
        self.setLayout(self.layMain)


    def initSlot(self):
        self.btnImageBrowse.clicked.connect(self.slotImageBrowse)
        self.btnConfirm.clicked.connect(self.slotConfirm)

        self.radioBoardSize1.clicked.connect(self.slotBoardSize)
        self.radioBoardSize2.clicked.connect(self.slotBoardSize)
        self.radioPlacement1.clicked.connect(self.slotPlacement)
        self.radioPlacement2.clicked.connect(self.slotPlacement)

    def isBoardSetting(self):
        return False if self.boardSize is '' or self.placement is '' or self.bgImageUrl == '' else True

    @pyqtSlot()
    def slotImageBrowse(self):
        print('image browse called!')

        imageBrowser = QFileDialog(self)
        imageBrowser.setNameFilters(["All Files (*)", "Image Files (*.png *.jpg *.bmp)"])
        imageBrowser.selectNameFilter("Image Files (*.png *.jpg *.bmp)")
        imageBrowser.setOption(QFileDialog.DontUseNativeDialog)
        imageBrowser.setWindowTitle('Board image')

        if imageBrowser.exec() == QFileDialog.Accepted:
           try:
               print(imageBrowser.selectedUrls())
               self.bgImageUrl = imageBrowser.selectedUrls()[0].path()[1:]
               print(self.bgImageUrl)
               self.boardImage = QPixmap(self.bgImageUrl)
               self.lblBackGroundImage.setPixmap(self.boardImage)
               self.lblBackGroundImage.show()
           except Exception as e:
               print(e)

    @pyqtSlot()
    def slotConfirm(self):
        print('board setting confirm called!')
        if not self.isBoardSetting():
            msgBox = QMessageBox()
            msgBox.setText("fill in blank")
            msgBox.exec()
        else:
            print('finish board setting!')
            self.close()

    @pyqtSlot()
    def slotBoardSize(self):
        print('board size radio called!')
        if self.radioBoardSize1.isChecked():
            self.boardSize = BoardSetting.size1
        elif self.radioBoardSize2.isChecked():
            self.boardSize = BoardSetting.size2
        print(self.boardSize)

    @pyqtSlot()
    def slotPlacement(self):
        print('placement radio called!')
        if self.radioPlacement1.isChecked():
            self.placement = BoardSetting.placement1
        elif self.radioPlacement2.isChecked():
            self.placement = BoardSetting.placement2
        print(self.placement)
