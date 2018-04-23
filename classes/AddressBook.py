#!/usr/bin/python3 -u

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QDialog, QMessageBox, QDesktopWidget, QToolTip, QPushButton, QTextEdit
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from classes.MainWindow import MainWindow
import os
import sys


# Наследуемся от QMainWindow
class AddressBook(MainWindow):
    def init(self):
        pass