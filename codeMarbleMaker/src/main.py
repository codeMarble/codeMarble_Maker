#-*- coding: utf-8 -*-
"""
    main.py

    :copyright: Hwang Sek-jin, ngh
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from codeMarbleMaker.src import modeSelect

settingDict = {}

class Main(QMainWindow):
    def __init__(self, ruleData, parent=None):
        QMainWindow.__init__(self, parent)
        self.ms = modeSelect.ModeSelect(ruleData, self)
        self.ms.exec()
        settingDict['보드 크기'] = self.ms.bs.boardSize
        settingDict['착수 규칙'] = self.ms.bs.placement

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
        board = self.ms.bs.boardImage.scaled(400, 400)
        painter = QPainter(board)
        painter.drawPixmap(0, 0, 400, 400, QPixmap('C:/Users/nlp-ngh/PycharmProjects/codeMarble_Maker/water-png-22.png')) # grid path
        painter.end()
        self.lblBoard.setPixmap(board)

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
        self.lstWgDtlSetting = QListWidget()
        self.dockDtlSetting.setWidget(self.lstWgDtlSetting)
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
                    for settingText, widgetClass in [('크기', self.WidgetBoardSize), ('착수 규칙', self.WidgetPlacement)]:
                        item = QListWidgetItem()
                        widget = widgetClass()
                        item.setSizeHint(widget.sizeHint())
                        self.addItem(item)
                        self.setItemWidget(item, widget)

                class WidgetBoardSize(QWidget):
                    def __init__(self):
                        QWidget.__init__(self)
                        label = QLabel('보드 크기')
                        self.radio1 = QRadioButton('8')
                        self.radio2 = QRadioButton('11')
                        self.radio1.clicked.connect(self.slotSize)
                        self.radio2.clicked.connect(self.slotSize)
                        if settingDict['보드 크기'] == 8:
                            self.radio1.setChecked(True)
                        elif settingDict['보드 크기'] == 11:
                            self.radio2.setChecked(True)
                        lay = QHBoxLayout()
                        lay.addWidget(label)
                        lay.addWidget(self.radio1)
                        lay.addWidget(self.radio2)
                        self.setLayout(lay)

                    @pyqtSlot()
                    def slotSize(self):
                        print('detail setting board size radio called!')
                        if self.radio1.isChecked():
                            settingDict['보드 크기'] = 8
                        elif self.radio2.isChecked():
                            settingDict['보드 크기'] = 11

                class WidgetPlacement(QWidget):
                    def __init__(self):
                        QWidget.__init__(self)
                        label = QLabel('착수 규칙')
                        self.radio1 = QRadioButton('cell')
                        self.radio2 = QRadioButton('cross point')
                        self.radio1.clicked.connect(self.slotPlacement)
                        self.radio2.clicked.connect(self.slotPlacement)
                        if settingDict['착수 규칙'] == 'cell':
                            self.radio1.setChecked(True)
                        elif settingDict['착수 규칙'] == 'cross point':
                            self.radio2.setChecked(True)
                        lay = QHBoxLayout()
                        lay.addWidget(label)
                        lay.addWidget(self.radio1)
                        lay.addWidget(self.radio2)
                        self.setLayout(lay)

                    @pyqtSlot()
                    def slotPlacement(self):
                        print('detail setting placement radio called!')
                        if self.radio1.isChecked():
                            settingDict['착수 규칙'] = 'cell'
                        elif self.radio2.isChecked():
                            settingDict['착수 규칙'] = 'cross point'

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
            self.lstWgDtlSetting = QListWidget()
            pass
        elif item.text() == '착수 규칙':
            self.lstWgDtlSetting = QListWidget()
            pass
        elif item.text() == '착수 옵션':
            self.lstWgDtlSetting = QListWidget()
            pass
        elif item.text() == '착수 후 규칙':
            self.lstWgDtlSetting = QListWidget()
            pass
        elif item.text() == '종료 규칙':
            self.lstWgDtlSetting = QListWidget()
            pass

        self.dockDtlSetting.setWidget(self.lstWgDtlSetting)
        self.dockDtlSetting.setWindowTitle(item.text())



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
