#-*- coding: utf-8 -*-
"""
    main.py

    Function for user login to server.

    :copyright: Hwang Sek-jin
"""

import os
import sys

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import pyqtSlot

from codeMarbleMaker.src import modeSelect
from codeMarbleMaker import config


class Main(QtWidgets.QDialog):
    def __init__(self, ruleData, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.modeSelect = modeSelect.ModeSelect(ruleData)
        self.modeSelect.exec_()

        self.main = uic.loadUi(os.path.join(config.config.ROOT_PATH, 'main.ui'))

        # from PyQt5.QtWidgets import QSplitter
        # qq = QSplitter()
        # qq.setStretchFactor()

        print(self.main.mainSplitter)
        print(self.modeSelect.boardSetting.boardImageFromUrl)

        boardImage = QPixmap(self.modeSelect.boardSetting.bgImageUrl.path()[1:])
        boardImage = boardImage.scaled(400, 400)
        self.main.board.setPixmap(boardImage)

        # for index in range(self.main.mainSplitter.count()):
        #     self.main.mainSplitter.setStretchFactor(index, True)

        for itemText in ['Board setting', 'Dummy1', 'Dummy2']:
            item = QListWidgetItem(itemText)
            self.main.settingLst.addItem(item)

        self.main.settingLst.itemClicked.connect(lambda item: self.func(item))
        self.main.show()

    def func(self, item):
        self.main.dtlSettingLst.clear()
        try:
            if item.text() == 'Board setting':
                for itemText in ['size', 'placement']:
                    # item = QListWidgetItem(itemText)
                    # self.main.dtlSettingLst.addItem(item)
                    item = QListWidgetItem(itemText)
                    dtlSettingWidget = self.DtlSettingWidget(itemText, 'asd')
                    self.main.dtlSettingLst.addItem(item)
                    item.setSizeHint(dtlSettingWidget.sizeHint())
                    self.main.dtlSettingLst.setItemWidget(item, dtlSettingWidget)
        except Exception as e:
            print(e)

    class DtlSettingWidget(QtWidgets.QWidget):
        def __init__(self, name, value):
            QtWidgets.QWidget.__init__(self)
            self.setLayout(QtWidgets.QHBoxLayout(self))
            self.layout().addWidget(QtWidgets.QLabel(name, self))
            self.layout().addWidget(QtWidgets.QLabel(value, self))
