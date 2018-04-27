#!/usr/bin/python3 -u

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QDialog, QMessageBox, QDesktopWidget, QToolTip, QPushButton, QTextEdit, QVBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
import os
import sys
from connector import Connector


class LeftMenu(QVBoxLayout):
    connector = None

    def __init__(self):
        self.connector = Connector()
        QVBoxLayout.__init__(self)
        names = [
            'Адресная книга',
            'Добавить запись',
            'Заметки',
            'Добавить заметку',
            'Настройки',
        ]
        actions = [
            self.show_addresses,
            self.show_addresses,
            self.show_addresses,
            self.show_addresses,
            self.show_addresses,
        ]
        for name, action in zip(names, actions):
            button = QPushButton(name)
            button.clicked.connect(action)
            button.setStyleSheet("width: 120px; height: 40px;")
            self.addWidget(button)
        self.addStretch()

    def show_addresses(self):
        addresses = self.connector.get_all('addresses')
        for row in addresses:
            print(row)
