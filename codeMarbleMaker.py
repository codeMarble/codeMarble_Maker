#-*- coding: utf-8 -*-
"""
    codeMarbleMaker.py

    :copyright: Hwang Sek-jin, ngh
"""

import sys

from PyQt5 import QtWidgets

from codeMarbleMaker.src import main

ruleData = {}

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    userLogIn = main.Main(ruleData)
    userLogIn.show()

    sys.exit(app.exec())