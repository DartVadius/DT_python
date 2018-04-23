#!/usr/bin/python3 -u

from PyQt5 import QtWidgets
import sys
from classes.MainWindow import MainWindow
from classes.AddressBook import AddressBook


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    # ab = AddressBook().init()
    mw.show()
    sys.exit(app.exec())
