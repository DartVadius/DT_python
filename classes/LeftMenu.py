#!/usr/bin/python3 -u

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QDialog, QMessageBox, QDesktopWidget, QToolTip, QPushButton, QTextEdit, QVBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
import os
import sys


class LeftMenu(QVBoxLayout):
    def __init__(self):
        QVBoxLayout.__init__(self)
        names = [
            'Адресная книга',
            'Добавить запись',
            'Заметки',
            'Добавить заметку',
            'Настройки',
        ]
        for name in names:
            button = QPushButton(name)
            button.setStyleSheet("width: 120px; height: 40px;")
            self.addWidget(button)
        self.addStretch()
