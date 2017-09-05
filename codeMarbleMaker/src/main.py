#-*- coding: utf-8 -*-
"""
    main.py

    :copyright: Hwang Sek-jin, ngh
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from codeMarbleMaker.src import modeSelect
from codeMarbleMaker.src.settingVariable import *

import traceback

settingDict = {}

def imageBrowse(parent):
    imageBrowser = QFileDialog(parent)
    imageBrowser.setNameFilters(["All Files (*)", "Image Files (*.png *.jpg *.bmp)"])
    imageBrowser.selectNameFilter("Image Files (*.png *.jpg *.bmp)")
    imageBrowser.setOption(QFileDialog.DontUseNativeDialog)
    imageBrowser.setWindowTitle('Board image')

    if imageBrowser.exec() == QFileDialog.Accepted:
        bgImageUrl = imageBrowser.selectedUrls()[0].path()[1:]
        settingDict[BoardSetting.background] = bgImageUrl
        return bgImageUrl
    else:
        return False

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class Main(QMainWindow):
    def __init__(self, ruleData, parent=None):
        QMainWindow.__init__(self, parent)
        try:
            # self.ms = modeSelect.ModeSelect(ruleData, self)
            # self.ms.exec()
            # settingDict[BoardSetting.size] = self.ms.bs.boardSize
            # settingDict[BoardSetting.placement] = self.ms.bs.placement
            # settingDict[BoardSetting.background] = self.ms.bs.bgImageUrl

            # todo: debug mode
            settingDict[BoardSetting.size] = '8'
            settingDict[BoardSetting.placement] = 'cell'
            settingDict[BoardSetting.background] = 'C:/Users/nlp-ngh/PycharmProjects/codeMarble_Maker/sampleImg.jpg'
        except Exception as e:
            print(type(e), e)

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
        menuBar = self.menuBar()
        for strMenu in MenuSetting.lst:
            menu = menuBar.addMenu(strMenu)
            for strDtlMenu in MenuSetting.dtlLst[strMenu]:
                # todo : action script
                act = menu.addAction(strDtlMenu)

        # setting list widget
        self.dockDtlSetting = QDockWidget('detail setting list', self)
        self.dockSetting = QDockWidget('setting list', self)
        self.lstWgSetting = ListWidgetSetting(self.dockSetting)

        self.dockSetting.setWidget(self.lstWgSetting)
        self.dockSetting.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockSetting)

        # detail setting list widget
        self.dockDtlSetting.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockDtlSetting)

        # board image widget
        self.lblBoard = QLabel()
        self.setGridBoard(QPixmap(settingDict[BoardSetting.background]))

        self.lblBoard.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.lblBoard)

    def setGridBoard(self, background):
        try:
            board = background.scaled(400, 400)
            painter = QPainter(board)
            gridPath = 'C:/Users/nlp-ngh/PycharmProjects/codeMarble_Maker/water-png-22.png'  # need path class
            painter.drawPixmap(0, 0, 400, 400, QPixmap(gridPath))
            painter.end()
            self.lblBoard.setPixmap(board)
        except Exception as e:
            print(type(e), e)


class WidgetSetting(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        lay = QHBoxLayout()
        self.setLayout(lay)

class ListWidgetSetting(QListWidget):
    def __init__(self, parent): # parent : dockSetting, parent.parent : main
        QListWidget.__init__(self, parent)
        self.lstWgDtlSetting = QListWidget()
        self.parent().parent().dockDtlSetting.setWidget(self.lstWgDtlSetting)

        try:
            self.itemClicked.connect(self.slotItemClick)

            self.lstSetting = getSettingList()
            for strSetting in self.lstSetting:
                item = QListWidgetItem(strSetting)
                widget = WidgetSetting()
                item.setSizeHint(widget.sizeHint())
                self.addItem(item)
                self.setItemWidget(item, widget)

        except Exception as e:
            print(type(e), e)

    @pyqtSlot(QListWidgetItem)
    def slotItemClick(self, item):
        print('setting item clicked! :', item.text())

        class WidgetBase(QWidget):
            def __init__(self, name, parent):
                QWidget.__init__(self, parent)
                self.name = name
                gbox = QGroupBox(self.name)
                vbox = self.contentLayout()
                gbox.setLayout(vbox)
                self.lay = QHBoxLayout()
                self.lay.addWidget(gbox)
                self.endLayout()

            def contentLayout(self): ## override function
                return QVBoxLayout()

            def endLayout(self): ## override function
                self.setLayout(self.lay)

        if item.text() == BoardSetting.name:
            class ListWidgetDtlBoardSetting(QListWidget):
                def __init__(self, parent):
                    QListWidget.__init__(self, parent) # parent : ListWidgetSetting
                    for settingText, widgetClass in \
                            [(BoardSetting.size, self.WidgetBoardSize),
                             (BoardSetting.placement, self.WidgetPlacement),
                             (BoardSetting.background, self.WidgetBackGround)]:
                        item = QListWidgetItem()
                        widget = widgetClass(settingText, self)
                        item.setSizeHint(widget.sizeHint())
                        self.addItem(item)
                        self.setItemWidget(item, widget)

                class WidgetBoardSize(QWidget):
                    def __init__(self, name, parent): # parent : ListWidgetDtlBoardSetting
                        QWidget.__init__(self, parent)
                        label = QLabel(name)
                        self.name = name
                        self.radio1 = QRadioButton(BoardSetting.size1)
                        self.radio2 = QRadioButton(BoardSetting.size2)
                        self.radio1.clicked.connect(self.slotSize)
                        self.radio2.clicked.connect(self.slotSize)
                        if settingDict[name] == BoardSetting.size1:
                            self.radio1.setChecked(True)
                        elif settingDict[name] == BoardSetting.size2:
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
                            settingDict[self.name] = BoardSetting.size1
                        elif self.radio2.isChecked():
                            settingDict[self.name] = BoardSetting.size2

                class WidgetPlacement(QWidget):
                    def __init__(self, name, parent): # parent : ListWidgetDtlBoardSetting
                        QWidget.__init__(self, parent)
                        label = QLabel(name)
                        self.name = name
                        self.radio1 = QRadioButton(BoardSetting.placement1)
                        self.radio2 = QRadioButton(BoardSetting.placement2)
                        self.radio1.clicked.connect(self.slotPlacement)
                        self.radio2.clicked.connect(self.slotPlacement)
                        if settingDict[name] == BoardSetting.placement1:
                            self.radio1.setChecked(True)
                        elif settingDict[name] == BoardSetting.placement2:
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
                            settingDict[self.name] = BoardSetting.placement1
                        elif self.radio2.isChecked():
                            settingDict[self.name] = BoardSetting.placement2

                class WidgetBackGround(QWidget):
                    def __init__(self, name, parent): # parent : ListWidgetDtlBoardSetting
                        QWidget.__init__(self, parent)
                        self.name = name
                        label = QLabel(name)
                        self.browse = QPushButton('browse')
                        self.browse.clicked.connect(self.slotImageBrowse)
                        lay = QHBoxLayout()
                        lay.addWidget(label)
                        lay.addWidget(self.browse)
                        self.setLayout(lay)

                    @pyqtSlot()
                    def slotImageBrowse(self):
                        print('detail setting background called!')
                        bgImageUrl = imageBrowse(self)
                        boardImage = QPixmap(bgImageUrl)
                        self.parent().parent().parent().parent().setGridBoard(boardImage)

            self.lstWgDtlSetting = ListWidgetDtlBoardSetting(self)


        elif item.text() == ObjectSetting.name:
            class ListWidgetDtlObjectSetting(QListWidget):
                def __init__(self, parent): # parent : ListWidgetSetting, parent.parent : dock
                    QListWidget.__init__(self, parent)
                    self.update_new()

                def update_new(self):
                    self.clear()
                    def update_once(settingText, widgetClass):
                        item = QListWidgetItem()
                        widget = widgetClass(settingText, self)
                        item.setSizeHint(widget.sizeHint())
                        self.addItem(item)
                        self.setItemWidget(item, widget)

                    update_once(ObjectSetting.count, self.WidgetCount)
                    update_once(ObjectSetting.image, self.WidgetImage)
                    update_once(ObjectSetting.image1, self.WidgetImages)
                    update_once(ObjectSetting.image2, self.WidgetImages)

                class WidgetCount(QWidget):
                    def __init__(self, name, parent):
                        try:
                            QWidget.__init__(self, parent)
                            self.name = name
                            label = QLabel(name)
                            self.radio1 = QRadioButton(ObjectSetting.count1)
                            self.radio2 = QRadioButton(ObjectSetting.count2)
                            self.radio3 = QRadioButton(ObjectSetting.count3)
                            self.radio1.clicked.connect(self.slotCount)
                            self.radio2.clicked.connect(self.slotCount)
                            self.radio3.clicked.connect(self.slotCount)
                            lay = QHBoxLayout()
                            lay.addWidget(label)
                            lay.addWidget(self.radio1)
                            lay.addWidget(self.radio2)
                            lay.addWidget(self.radio3)
                            self.checkCount()
                            self.setLayout(lay)

                        except Exception as e:
                            print(type(e), e)

                    @pyqtSlot()
                    def slotCount(self):
                        print(self.name, 'called!')
                        if self.radio1.isChecked():
                            settingDict[self.name] = ObjectSetting.count1
                        elif self.radio2.isChecked():
                            settingDict[self.name] = ObjectSetting.count2
                        elif self.radio3.isChecked():
                            settingDict[self.name] = ObjectSetting.count3
                        try:
                            print('!!!', self)
                            print('!!!', self.parent())
                            print('!!!', self.parent().parent())
                            self.parent().parent().update_new()

                        except Exception as e:
                            print(type(e), e)

                    def checkCount(self):
                        if self.name in settingDict:
                            if settingDict[self.name] == ObjectSetting.count1:
                                self.radio1.setChecked(True)
                            elif settingDict[self.name] == ObjectSetting.count2:
                                self.radio2.setChecked(True)
                            elif settingDict[self.name] == ObjectSetting.count3:
                                self.radio3.setChecked(True)

                class WidgetImage(QWidget):
                    def __init__(self, name, parent):
                        try:
                            QWidget.__init__(self, parent)
                            self.name = name
                            label = QLabel(name)
                            self.radio1 = QRadioButton(ObjectSetting.image1)
                            self.radio2 = QRadioButton(ObjectSetting.image2)
                            if ObjectSetting.count not in settingDict:
                                self.setEnabled(False)
                            self.radio1.clicked.connect(self.slotRadio)
                            self.radio2.clicked.connect(self.slotRadio)
                            lay = QHBoxLayout()
                            lay.addWidget(label)
                            lay.addWidget(self.radio1)
                            lay.addWidget(self.radio2)
                            self.checkImage()
                            self.setLayout(lay)

                        except Exception as e:
                            print(type(e), e)

                    def checkImage(self):
                        if self.name in settingDict:
                            if settingDict[self.name] == ObjectSetting.image1:
                                self.radio1.setChecked(True)
                            elif settingDict[self.name] == ObjectSetting.image2:
                                self.radio2.setChecked(True)

                    @pyqtSlot()
                    def slotRadio(self):
                        print(self.name, 'called!')
                        if self.radio1.isChecked():
                            settingDict[self.name] = ObjectSetting.image1
                        elif self.radio2.isChecked():
                            settingDict[self.name] = ObjectSetting.image2
                        self.parent().parent().update_new()

                class WidgetImages(WidgetBase):
                    def __init__(self, name, parent):
                        super().__init__(name, parent)

                    def contentLayout(self):
                        vbox = QVBoxLayout()
                        self.idx2btn = {}
                        self.idx2icon = {}
                        self.idx2slot = {0: self.slotBtn0, 1: self.slotBtn1, 2: self.slotBtn2}
                        if ObjectSetting.count in settingDict:
                            for idx in range(int(settingDict[ObjectSetting.count])):
                                hbox = QHBoxLayout()
                                print(self.name + str(idx))
                                self.idx2icon[idx] = QLabel('image')
                                if self.name + str(idx) in settingDict:
                                    self.idx2icon[idx].setPixmap(QPixmap(settingDict[self.name + str(idx)]).scaled(30, 30))
                                label = QLabel(str(idx))
                                self.idx2btn[idx] = QPushButton('browse')
                                hbox.addWidget(self.idx2icon[idx])
                                hbox.addWidget(label)
                                hbox.addWidget(self.idx2btn[idx])
                                vbox.addLayout(hbox)
                                self.idx2btn[idx].clicked.connect(self.idx2slot[idx])
                        return vbox

                    def endLayout(self):
                        if ObjectSetting.image not in settingDict or settingDict[ObjectSetting.image] != self.name:
                            self.hide()
                        else:
                            self.setLayout(self.lay)

                    def slotBtn0(self):
                        url = imageBrowse(self)
                        settingDict[self.name + '0'] = url
                        self.idx2icon[0].setPixmap(QPixmap(url).scaled(30, 30))

                    def slotBtn1(self):
                        url = imageBrowse(self)
                        settingDict[self.name + '1'] = url
                        self.idx2icon[1].setPixmap(QPixmap(url).scaled(30, 30))

                    def slotBtn2(self):
                        url = imageBrowse(self)
                        settingDict[self.name + '2'] = url
                        self.idx2icon[2].setPixmap(QPixmap(url).scaled(30, 30))

                # class WidgetImages(QWidget):
                #     def __init__(self, name, parent):
                #         QWidget.__init__(self, parent)
                #         self.name = name
                #         gbox = QGroupBox(self.name)
                #         vbox = QVBoxLayout()
                #         self.idx2btn = {}
                #         self.idx2icon = {}
                #         self.idx2slot = {0: self.slotBtn0, 1: self.slotBtn1, 2: self.slotBtn2}
                #         if ObjectSetting.count in settingDict:
                #             for idx in range(int(settingDict[ObjectSetting.count])):
                #                 hbox = QHBoxLayout()
                #                 print(self.name + str(idx))
                #                 self.idx2icon[idx] = QLabel('image')
                #                 if self.name + str(idx) in settingDict:
                #                     self.idx2icon[idx].setPixmap(QPixmap(settingDict[self.name + str(idx)]).scaled(30, 30))
                #                 label = QLabel(str(idx))
                #                 self.idx2btn[idx] = QPushButton('browse')
                #                 hbox.addWidget(self.idx2icon[idx])
                #                 hbox.addWidget(label)
                #                 hbox.addWidget(self.idx2btn[idx])
                #                 vbox.addLayout(hbox)
                #                 self.idx2btn[idx].clicked.connect(self.idx2slot[idx])
                #         gbox.setLayout(vbox)
                #         lay = QHBoxLayout()
                #         lay.addWidget(gbox)
                #         if ObjectSetting.image not in settingDict or settingDict[ObjectSetting.image] != self.name:
                #             self.hide()
                #         else:
                #             self.setLayout(lay)
                #
                #     def slotBtn0(self):
                #         url = imageBrowse(self)
                #         settingDict[self.name + '0'] = url
                #         self.idx2icon[0].setPixmap(QPixmap(url).scaled(30, 30))
                #
                #     def slotBtn1(self):
                #         url = imageBrowse(self)
                #         settingDict[self.name + '1'] = url
                #         self.idx2icon[1].setPixmap(QPixmap(url).scaled(30, 30))
                #
                #     def slotBtn2(self):
                #         url = imageBrowse(self)
                #         settingDict[self.name + '2'] = url
                #         self.idx2icon[2].setPixmap(QPixmap(url).scaled(30, 30))

            self.lstWgDtlSetting = ListWidgetDtlObjectSetting(self)

        elif item.text() == BoardReset.name:
            self.lstWgDtlSetting = QListWidget()
            pass # todo later

        elif item.text() == PlacementRule.name:
            class ListWidgetDtlPlacementRule(QListWidget):
                def __init__(self, parent): # parent : ListWidgetSetting, parent.parent : dock
                    QListWidget.__init__(self, parent)
                    self.update_new()

                def update_new(self):
                    self.clear()
                    def update_once(settingText, widgetClass):
                        item = QListWidgetItem()
                        widget = widgetClass(settingText, self)
                        item.setSizeHint(widget.sizeHint())
                        self.addItem(item)
                        self.setItemWidget(item, widget)

                    update_once(PlacementRule.ruleFirst, self.WidgetRule1)
                    update_once(PlacementRule.ruleSecond, self.WidgetRule2)

                class WidgetRule1(WidgetBase):
                    def __init__(self, name, parent):
                        super().__init__(name, parent)

                    def contentLayout(self):
                        box = QHBoxLayout()
                        self.radio1 = QRadioButton(PlacementRule.ruleFirst1)
                        self.radio2 = QRadioButton(PlacementRule.ruleFirst2)
                        box.addWidget(self.radio1)
                        box.addWidget(self.radio2)
                        self.radio1.clicked.connect(self.slotRadio)
                        self.radio2.clicked.connect(self.slotRadio)
                        self.checkRadio()
                        return box

                    def slotRadio(self):
                        if self.radio1.isChecked():
                            settingDict[self.name] = PlacementRule.ruleFirst1
                        elif self.radio2.isChecked():
                            settingDict[self.name] = PlacementRule.ruleFirst2

                    def checkRadio(self):
                        if self.name in settingDict:
                            if settingDict[self.name] == PlacementRule.ruleFirst1:
                                self.radio1.setChecked(True)
                            elif settingDict[self.name] == PlacementRule.ruleFirst2:
                                self.radio2.setChecked(True)

                class WidgetRule2(WidgetBase): # todo: must modify!
                    def __init__(self, name, parent):
                        super().__init__(name, parent)


                    def contentLayout(self):
                        vbox = QVBoxLayout()

                        self.radios = {}
                        for idx in range(int(settingDict[ObjectSetting.count])):
                            group = QGroupBox(str(idx))
                            hbox = QHBoxLayout()

                            self.radios[idx] = [QRadioButton(PlacementRule.ruleSecond1),
                                                QRadioButton(PlacementRule.ruleSecond2),
                                                QRadioButton(PlacementRule.ruleSecond3),
                                                QRadioButton(PlacementRule.ruleSecond4)]

                            for radio in self.radios[idx]:
                                hbox.addWidget(radio)
                                radio.clicked.connect(self.slotRadio)

                            group.setLayout(hbox)
                            vbox.addWidget(group)
                        self.checkRadio()

                        ######
                        # self.radio1 = QRadioButton(PlacementRule.ruleSecond1)
                        # self.radio2 = QRadioButton(PlacementRule.ruleSecond2)
                        # self.radio3 = QRadioButton(PlacementRule.ruleSecond3)
                        # self.radio4 = QRadioButton(PlacementRule.ruleSecond4)
                        # vbox.addWidget(self.radio1)
                        # vbox.addWidget(self.radio2)
                        # vbox.addWidget(self.radio3)
                        # vbox.addWidget(self.radio4)
                        #
                        # self.radio1.clicked.connect(self.slotRadio)
                        # self.radio2.clicked.connect(self.slotRadio)
                        # self.radio3.clicked.connect(self.slotRadio)
                        # self.radio4.clicked.connect(self.slotRadio)
                        # self.checkRadio()
                        ######

                        return vbox

                    def slotRadio(self):
                        for idx in range(int(settingDict[ObjectSetting.count])):
                            for num, radio in enumerate(self.radios[idx]):
                                if radio.isChecked():
                                    settingDict[self.name + str(idx)] = PlacementRule.ruleSeconds[num]
                                    print(self.name + str(idx), PlacementRule.ruleSeconds[num])

                        # if self.radio1.isChecked():
                        #     settingDict[self.name] = PlacementRule.ruleSecond1
                        # elif self.radio2.isChecked():
                        #     settingDict[self.name] = PlacementRule.ruleSecond2
                        # elif self.radio3.isChecked():
                        #     settingDict[self.name] = PlacementRule.ruleSecond3
                        # elif self.radio4.isChecked():
                        #     settingDict[self.name] = PlacementRule.ruleSecond4

                    def checkRadio(self):
                        if any(self.name + str(idx) in settingDict for idx in range(int(settingDict[ObjectSetting.count]))):
                            for idx in range(int(settingDict[ObjectSetting.count])):
                                for num, radio in enumerate(self.radios[idx]):
                                    if self.name + str(idx) in settingDict and settingDict[self.name + str(idx)] == PlacementRule.ruleSeconds[num]:
                                        radio.setChecked(True)
                                        print(self.name + str(idx), PlacementRule.ruleSeconds[num])

                            # if settingDict[self.name] == PlacementRule.ruleSecond1:
                            #     self.radio1.setChecked(True)
                            # elif settingDict[self.name] == PlacementRule.ruleSecond2:
                            #     self.radio2.setChecked(True)
                            # elif settingDict[self.name] == PlacementRule.ruleSecond3:
                            #     self.radio3.setChecked(True)
                            # elif settingDict[self.name] == PlacementRule.ruleSecond4:
                            #     self.radio4.setChecked(True)


            try:
                self.lstWgDtlSetting = ListWidgetDtlPlacementRule(self)
            except Exception as e:
                print(type(e), e)

        elif item.text() == PlacementOption.name:
            class ListWidgetDtlPlacementOption(QListWidget):
                def __init__(self, parent): # parent : ListWidgetSetting, parent.parent : dock
                    QListWidget.__init__(self, parent)
                    self.update_new()

                def update_new(self):
                    self.clear()
                    def update_once(settingText, widgetClass):
                        item = QListWidgetItem()
                        widget = widgetClass(settingText, self)
                        item.setSizeHint(widget.sizeHint())
                        self.addItem(item)
                        self.setItemWidget(item, widget)

                    update_once(PlacementOption.name, self.WidgetTemp)

                class WidgetTemp(WidgetBase):
                    def __init__(self, name, parent):
                        super().__init__(name, parent)

                    def contentLayout(self):
                        vbox = QVBoxLayout()

                        self.combosRule1 = {}
                        self.combosRule2 = {}

                        slots = { 0: {PlacementOption.row : self.slot1, PlacementOption.col : self.slot2,
                                      PlacementOption.over : self.slot3, PlacementOption.size : self.slot4},
                                  1: {PlacementOption.row: self.slot5, PlacementOption.col: self.slot6,
                                      PlacementOption.over: self.slot7, PlacementOption.size: self.slot8},
                                  2: {PlacementOption.row: self.slot9, PlacementOption.col: self.slot10,
                                      PlacementOption.over: self.slot11, PlacementOption.size: self.slot12}}

                        for idx in range(int(settingDict[ObjectSetting.count])):
                            vbox2 = QVBoxLayout()
                            group = QGroupBox(str(idx))

                            self.combosRule1[idx] = [QComboBox(), QComboBox()]
                            self.combosRule2[idx] = [QComboBox(), QComboBox()]

                            lim = int(settingDict[BoardSetting.size]) - (2 if settingDict[BoardSetting.size] == '8' else 4)
                            hbox = QHBoxLayout()
                            for combo, label in zip(self.combosRule1[idx], [PlacementOption.row, PlacementOption.col]):
                                for num in range(lim):
                                    combo.addItem(str(num + 1))
                                combo.currentIndexChanged.connect(slots[idx][label])
                                hbox.addWidget(QLabel(label))
                                hbox.addWidget(combo)
                            vbox2.addLayout(hbox)

                            for num in range(lim):
                                self.combosRule2[idx][1].addItem(str(num + 1))

                            self.combosRule2[idx][0].addItem(str('O'))
                            self.combosRule2[idx][0].addItem(str('X'))

                            self.combosRule2[idx][0].currentIndexChanged.connect(slots[idx][PlacementOption.over])
                            self.combosRule2[idx][1].currentIndexChanged.connect(slots[idx][PlacementOption.size])

                            hbox = QHBoxLayout()
                            hbox.addWidget(QLabel(PlacementOption.over))
                            hbox.addWidget(self.combosRule2[idx][0])
                            hbox.addWidget(QLabel(PlacementOption.size))
                            hbox.addWidget(self.combosRule2[idx][1])
                            vbox2.addLayout(hbox)

                            group.setLayout(vbox2)
                            vbox.addWidget(group)
                            if idx != int(settingDict[ObjectSetting.count]) - 1:
                                vbox.addWidget(QHLine())

                        self.setCombo()
                        return vbox

                    def endLayout(self):
                        if PlacementRule.ruleFirst not in settingDict or settingDict[PlacementRule.ruleFirst] != PlacementRule.ruleFirst2:
                            self.setEnabled(False)

                        for idx in range(int(settingDict[ObjectSetting.count])):
                            print(idx)
                            try:
                                if settingDict[PlacementRule.ruleSecond + str(idx)] == PlacementRule.ruleSecond1:
                                    for combo in self.combosRule2[idx]:
                                        combo.setEnabled(False)
                                else:
                                    for combo in self.combosRule1[idx]:
                                        combo.setEnabled(False)
                            except:
                                for c1, c2 in zip(self.combosRule1[idx], self.combosRule2[idx]):
                                    c1.setEnabled(False)
                                    c2.setEnabled(False)

                        self.setLayout(self.lay)

                    def setCombo(self):
                        for idx in range(int(settingDict[ObjectSetting.count])):
                            for combo, label in zip(self.combosRule1[idx], [PlacementOption.row, PlacementOption.col]):
                                if self.name + label + str(idx) in settingDict:
                                    index = combo.findText(settingDict[self.name + label + str(idx)])
                                    combo.setCurrentIndex(index)

                        for idx in range(int(settingDict[ObjectSetting.count])):
                            for combo, label in zip(self.combosRule2[idx], [PlacementOption.over, PlacementOption.size]):
                                if self.name + label + str(idx) in settingDict:
                                    index = combo.findText(settingDict[self.name + label + str(idx)])
                                    combo.setCurrentIndex(index)

                    def slot1(self, idx):
                        settingDict[self.name + PlacementOption.row + '0'] = self.combosRule1[0][0].currentText()

                    def slot2(self, idx):
                        settingDict[self.name + PlacementOption.col + '0'] = self.combosRule1[0][1].currentText()

                    def slot3(self, idx):
                        settingDict[self.name + PlacementOption.over + '0'] = self.combosRule2[0][0].currentText()

                    def slot4(self, idx):
                        settingDict[self.name + PlacementOption.size + '0'] = self.combosRule2[0][1].currentText()

                    #
                    def slot5(self, idx):
                        settingDict[self.name + PlacementOption.row + '1'] = self.combosRule1[1][0].currentText()

                    def slot6(self, idx):
                        settingDict[self.name + PlacementOption.col + '1'] = self.combosRule1[1][1].currentText()

                    def slot7(self, idx):
                        settingDict[self.name + PlacementOption.over + '1'] = self.combosRule2[1][0].currentText()

                    def slot8(self, idx):
                        settingDict[self.name + PlacementOption.size + '1'] = self.combosRule2[1][1].currentText()

                    #
                    def slot9(self, idx):
                        settingDict[self.name + PlacementOption.row + '2'] = self.combosRule1[2][0].currentText()

                    def slot10(self, idx):
                        settingDict[self.name + PlacementOption.col + '2'] = self.combosRule1[2][1].currentText()

                    def slot11(self, idx):
                        settingDict[self.name + PlacementOption.over + '2'] = self.combosRule2[2][0].currentText()

                    def slot12(self, idx):
                        settingDict[self.name + PlacementOption.size + '2'] = self.combosRule2[2][1].currentText()


            try:
                self.lstWgDtlSetting = ListWidgetDtlPlacementOption(self)
            except Exception as e:
                print(type(e), e)

        elif item.text() == PlacementAfterRule.name:
            self.lstWgDtlSetting = QListWidget()
            pass # todo later
        elif item.text() == ExitRule.name:
            self.lstWgDtlSetting = QListWidget()
            pass # todo later

        try:
            self.parent().parent().dockDtlSetting.setWidget(self.lstWgDtlSetting)
            self.parent().parent().dockDtlSetting.setWindowTitle(item.text())

        except Exception as e:
            print(type(e), e)

        print(settingDict)
