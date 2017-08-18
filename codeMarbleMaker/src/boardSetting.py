import os
import sys

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog

from codeMarbleMaker import config

class BoardSetting(QtWidgets.QDialog):
    def __init__(self, ruleData, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.boardSetting = uic.loadUi(os.path.join(config.config.ROOT_PATH, 'boardSetting.ui'), self)
        self.ruleData = ruleData
        self.boardSize = 0
        self.placement = ''
        self.bgImageUrl = QUrl()


        # from PyQt5.QtWidgets import QRadioButton
        # qq = QRadioButton()
        # qq.setChecked()

        self.boardSetting.boardSizeRadioBtn1.clicked.connect(self.boardSizeClickedSlot)
        self.boardSetting.boardSizeRadioBtn2.clicked.connect(self.boardSizeClickedSlot)

        self.boardSetting.placementRadioBtn1.clicked.connect(self.placementClickedSlot)
        self.boardSetting.placementRadioBtn2.clicked.connect(self.placementClickedSlot)

        self.boardSetting.bgImageBtn.clicked.connect(self.bgImageClickedSlot)
        self.boardSetting.okBtn.clicked.connect(self.saveClickedSlot)

    @pyqtSlot()
    def boardSizeClickedSlot(self):
        if self.boardSetting.boardSizeRadioBtn1.isChecked():
            self.boardSize = 8
        elif self.boardSetting.boardSizeRadioBtn2.isChecked():
            self.boardSize = 11
        else:
            # error!
            pass
        print(self.boardSize)


    @pyqtSlot()
    def placementClickedSlot(self):
        if self.boardSetting.placementRadioBtn1.isChecked():
            self.placement = 'cell'
        elif self.boardSetting.placementRadioBtn2.isChecked():
            self.placement = 'cross'
        else:
            pass
            # error!
        print(self.placement)

    @pyqtSlot()
    def bgImageClickedSlot(self):
        imageBrowser = QFileDialog(self)

        imageBrowser.setNameFilters(["All Files (*)", "Image Files (*.png *.jpg *.bmp)"])
        imageBrowser.selectNameFilter("Image Files (*.png *.jpg *.bmp)")
        imageBrowser.setOption(QFileDialog.DontUseNativeDialog)
        # self.bgImageUrl, _ = imageBrowser.getOpenFileUrl(self, "Board Background Image")
        imageBrowser.setWindowTitle('Board image')

        if imageBrowser.exec() == QFileDialog.Accepted:
           try:
               print(imageBrowser.selectedUrls())
               self.bgImageUrl = imageBrowser.selectedUrls()[0]
               self.boardImageFromUrl = QPixmap(self.bgImageUrl.path()[1:])
               self.boardSetting.boardImage.setPixmap(self.boardImageFromUrl)
               self.boardSetting.boardImage.show()
           except Exception as e:
               print(e)

    @pyqtSlot()
    def saveClickedSlot(self):
        if not self.isBoardSetting():
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("fill in blank")
            msgBox.exec()
        else:
            self.close()

    def isBoardSetting(self):
        return False if self.boardSize is 0 or self.placement is '' or self.bgImageUrl.isEmpty() else True