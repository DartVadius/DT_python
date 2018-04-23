#!/usr/bin/python3 -u

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QDialog, QMessageBox, QDesktopWidget, QToolTip, QPushButton, QTextEdit, QBoxLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from classes.LeftMenu import LeftMenu
import os
import sys


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    central_widget = None
    grid_layout = None

    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setup_app()
        self.set_main_menu()
        self.set_tray()
        self.statusBar()

        # создаем центральный виджет
        self.central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(self.central_widget)  # Устанавливаем центральный виджет
        self.central_widget.setLayout(self.set_main_window())  # Устанавливаем представление в центральный виджет

    # настраиваем рабочую область приложения
    def set_main_window(self):
        main_window = QHBoxLayout()
        main_field = QVBoxLayout()
        left_menu = LeftMenu()
        main_window.addLayout(left_menu)
        main_window.addLayout(main_field)
        main_window.setStretchFactor(left_menu, 1)
        main_window.setStretchFactor(main_field, 9)
        return main_window

    def set_main_window2(self):
        # устанавливаем грид лейаут в центральные виджет
        self.grid_layout = QGridLayout(self)  # Создаём QGridLayout
        # grid_layout.setSpacing(10)
        names = [
            'Адресная книга',
            'Добавить запись',
            'Заметки',
            'Добавить заметку',
            'Настройки',
        ]
        pos = 1
        for name in names:
            button = QPushButton(name)
            button.setStyleSheet("width: 120px; height: 40px;")
            # button.setStyleSheet("text-align: left;")
            self.grid_layout.addWidget(button, pos, 0)
            pos += 1
        main_window = QTextEdit()
        # title = QLabel("Address book on the PyQt5", self)  # Создаём лейбл
        # title.setAlignment(QtCore.Qt.AlignCenter)  # Устанавливаем позиционирование текста
        # main_window.addWidget(title)  # и добавляем его в размещение
        self.grid_layout.addWidget(main_window, 1, 1, 15, 1)
        # self.grid_layout.addWidget(main_window, 1, 0)
        return self.grid_layout

    # настраиваем окно приложения
    def setup_app(self):
        self.setMinimumSize(QSize(800, 600))  # Устанавливаем размеры
        self.center()
        self.setWindowTitle("Address book")  # Устанавливаем заголовок окна
        self.setWindowIcon(QIcon('icon.png'))

    # настраиваем трей
    def set_tray(self):
        # сворачивание приложения в трей
        tray_icon = QSystemTrayIcon(self)
        icon = QIcon("icon.png")
        tray_icon.setIcon(icon)
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()
        tray_icon.setToolTip('Address book')
        # tray_icon.showMessage('Title', 'Text')

    # настраиваем главное меню и тулбар
    def set_main_menu(self):
        # экшены
        hide_action = QAction(QIcon("icon.png"), "&Hide", self)
        hide_action.triggered.connect(self.hide)
        exit_action = QAction("&Exit", self)  # Создаём Action с помощью которого будем выходить из приложения
        exit_action.setShortcut('Ctrl+Q')  # Задаём для него хоткей
        exit_action.triggered.connect(self.close)  # Подключаем сигнал triggered к слоту quit у qApp.
        test_action = QAction("&Test", self)
        test_action.triggered.connect(self.test)

        # панель меню
        main_menu = self.menuBar()
        hide_menu = main_menu.addMenu('Hide')
        file_menu = main_menu.addMenu('Exit')
        test_menu = main_menu.addMenu('Test')
        hide_menu.addAction(hide_action)
        file_menu.addAction(exit_action)
        test_menu.addAction(test_action)

        # тулбар
        # toolbar = self.addToolBar('Exit')
        # toolbar.addAction(exit_action)

    def test(self):
        print('test')
        return True

    # переопределяем событие close
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение', "Вы уверены?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # центрируем окно приложения
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
