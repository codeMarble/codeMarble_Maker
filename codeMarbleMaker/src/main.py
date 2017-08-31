#-*- coding: utf-8 -*-
"""
    main.py

    :copyright: Hwang Sek-jin, ngh
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from codeMarbleMaker.src import modeSelect

class Main(QMainWindow):
    def __init__(self, ruleData, parent=None):
        QMainWindow.__init__(self, parent)
        self.ms = modeSelect.ModeSelect(ruleData, self)
        self.ms.exec()
        print(self.ms.bs.boardSize, self.ms.bs.placement)

        self.initUI()

    def initUI(self):
        # window setting
        width, height = 1020, 764
        title = 'Code Marble - main'

        self.setWindowTitle(title)
        resolution = QDesktopWidget().screenGeometry()
        self.setGeometry((resolution.width() / 2) - (width / 2),
                         (resolution.height() / 2) - (height / 2),
                         width, height)

        # menu bar setting
        lstMenu = ['파일', '편집', 'dummy1']
        lstDtlMenu = { '파일': ['dummy1'],
                       '편집': ['dummy1', 'dummy2'],
                       'dummy1': ['dummy1', 'dummy2', 'dummy3'] }

        menuBar = self.menuBar()
        for strMenu in lstMenu:
            menu = menuBar.addMenu(strMenu)
            for strDtlMenu in lstDtlMenu[strMenu]:
                menu.addAction(strDtlMenu)

        # setting list widget
        self.dockDtlSetting = QDockWidget('detail setting list', self)
        self.lstWgSetting = ListWidgetSetting(self.dockDtlSetting)

        self.dockSetting = QDockWidget('setting list', self)
        self.dockSetting.setWidget(self.lstWgSetting)
        self.dockSetting.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockSetting)

        # detail setting list widget
        # self.dockDtlSetting.setWidget(self.lstWgDtlSetting)
        self.dockDtlSetting.setFloating(False)
        # self.dockDtlSetting.setFeatures(QDockWidget.DockWidgetMovable)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockDtlSetting)

        # board image widget
        self.lblBoard = QLabel()
        self.lblBoard.setPixmap(self.ms.bs.boardImage.scaled(400, 400))
        self.lblBoard.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.lblBoard)


class WidgetSetting(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        lay = QHBoxLayout()
        self.setLayout(lay)


class ListWidgetSetting(QListWidget):
    def __init__(self, dockDtlSetting):
        QListWidget.__init__(self)
        self.dockDtlSetting = dockDtlSetting
        self.itemClicked.connect(self.slotItemClick)

        self.lstSetting = ['보드 세팅', '오브젝트 세팅', '보드 초기화', '착수 규칙', '착수 옵션', '착수 후 규칙', '종료 규칙']
        for strSetting in self.lstSetting:
            item = QListWidgetItem(strSetting)
            widget = WidgetSetting()
            item.setSizeHint(widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, widget)

    def slotItemClick(self, item):
        print('setting item clicked! :', item.text())

        if item.text() == '보드 세팅':
            class ListWidgetDtlBoardSetting(QListWidget):
                def __init__(self):
                    QListWidget.__init__(self)
                    self.addItem('board setting')
                    self.addItem('dummy1')

            self.lstWgDtlSetting = ListWidgetDtlBoardSetting()

        elif item.text() == '오브젝트 세팅':
            class ListWidgetDtlObjectSetting(QListWidget):
                def __init__(self):
                    QListWidget.__init__(self)
                    self.addItem('object setting')
                    self.addItem('dummy1')
                    self.addItem('dummy2')

            self.lstWgDtlSetting = ListWidgetDtlObjectSetting()

        elif item.text() == '보드 초기화':
            pass
        elif item.text() == '착수 규칙':
            pass
        elif item.text() == '착수 옵션':
            pass
        elif item.text() == '착수 후 규칙':
            pass
        elif item.text() == '종료 규칙':
            pass

        self.dockDtlSetting.setWidget(self.lstWgDtlSetting)


# if item.text() == 'Board setting':
#     for itemText in ['size', 'placement']:
#         # item = QListWidgetItem(itemText)
#         # self.main.dtlSettingLst.addItem(item)
#         item = QListWidgetItem()
#         dtlSettingWidget = self.DtlSettingWidget(itemText, 'asd')
#         self.main.dtlSettingLst.addItem(item)
#         item.setSizeHint(dtlSettingWidget.sizeHint())
#         self.main.dtlSettingLst.setItemWidget(item, dtlSettingWidget)


# #-*- coding: utf-8 -*-
# """
#     main.py
#
#     Function for user login to server.
#
#     :copyright: Hwang Sek-jin
# """
#
# import os
# import sys
#
# from PyQt5 import QtWidgets
# from PyQt5 import uic
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMessageBox
# from PyQt5.QtCore import pyqtSlot
#
# from codeMarbleMaker.src import modeSelect
# from codeMarbleMaker import config
#
#
# class Main(QtWidgets.QDialog):
#
#     def __init__(self, ruleData, parent=None):
#         QtWidgets.QDialog.__init__(self, parent)
#
#         self.modeSelect = modeSelect.ModeSelect(ruleData)
#         self.modeSelect.exec_()
#
#         self.main = uic.loadUi(os.path.join(config.config.ROOT_PATH, 'main.ui'))
#
#         # from PyQt5.QtWidgets import QSplitter
#         # qq = QSplitter()
#         # qq.setStretchFactor()
#
#         print(self.main.mainSplitter)
#         print(self.modeSelect.boardSetting.boardImageFromUrl)
#
#         boardImage = QPixmap(self.modeSelect.boardSetting.bgImageUrl.path()[1:])
#         boardImage = boardImage.scaled(400, 400)
#         self.main.board.setPixmap(boardImage)
#
#         # for index in range(self.main.mainSplitter.count()):
#         #     self.main.mainSplitter.setStretchFactor(index, True)
#
#         for itemText in ['Board setting', 'Dummy1', 'Dummy2']:
#             item = QListWidgetItem(itemText)
#             self.main.settingLst.addItem(item)
#
#         self.main.settingLst.itemClicked.connect(lambda item: self.func(item))
#         self.main.show()
#
#     def func(self, item):
#         self.main.dtlSettingLst.clear()
#         try:
#             if item.text() == 'Board setting':
#                 for itemText in ['size', 'placement']:
#                     # item = QListWidgetItem(itemText)
#                     # self.main.dtlSettingLst.addItem(item)
#                     item = QListWidgetItem()
#                     dtlSettingWidget = self.DtlSettingWidget(itemText, 'asd')
#                     self.main.dtlSettingLst.addItem(item)
#                     item.setSizeHint(dtlSettingWidget.sizeHint())
#                     self.main.dtlSettingLst.setItemWidget(item, dtlSettingWidget)
#         except Exception as e:
#             print(e)
#
#     class DtlSettingWidget(QtWidgets.QWidget):
#         def __init__(self, name, value):
#             QtWidgets.QWidget.__init__(self)
#             self.setLayout(QtWidgets.QHBoxLayout(self))
#             self.layout().addWidget(QtWidgets.QLabel(name, self))
#             self.layout().addWidget(QtWidgets.QLabel(value, self))
