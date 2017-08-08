import sys
from PyQt5 import QtWidgets

from codeMarbleMaker.src import main

ruleData = {}

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    userLogIn = main.Main(ruleData)

    sys.exit(app.exec())