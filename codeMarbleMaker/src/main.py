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
from codeMarbleMaker import config

class Main(QtWidgets.QDialog):
    def __init__(self,ruleData, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(config.config.ROOT_PATH,'main.ui'))

        self.ui.show()
