#!/usr/bin/python3 -u

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QDialog, QMessageBox, QDesktopWidget, QToolTip
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
import os


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(800, 600))  # Устанавливаем размеры
        self.center()
        self.setWindowTitle("Address book")  # Устанавливаем заголовок окна
        path = os.path.join(os.getcwd(), 'icon.png')
        self.setWindowIcon(QIcon(path))
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        self.set_main_menu()
        self.set_tray()

        grid_layout = QGridLayout(self)  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет
        title = QLabel("Address book on the PyQt5", self)  # Создаём лейбл
        title.setAlignment(QtCore.Qt.AlignCenter)  # Устанавливаем позиционирование текста
        grid_layout.addWidget(title)  # и добавляем его в размещение

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

    def set_main_menu(self):
        hide_action = QAction("&Hide", self)
        hide_action.triggered.connect(self.hide)

        exit_action = QAction("&Exit", self)  # Создаём Action с помощью которого будем выходить из приложения
        exit_action.setShortcut('Ctrl+Q')  # Задаём для него хоткей
        # Подключаем сигнал triggered к слоту quit у qApp.
        exit_action.triggered.connect(self.close)

        test_action = QAction("&Test", self)
        test_action.triggered.connect(self.test)

        # Устанавливаем в панель меню данный Action.
        main_menu = self.menuBar()
        hide_menu = main_menu.addMenu('Hide')
        file_menu = main_menu.addMenu('Exit')
        test_menu = main_menu.addMenu('Test')
        hide_menu.addAction(hide_action)
        file_menu.addAction(exit_action)
        test_menu.addAction(test_action)

    def test(self):
        print('test')
        return True

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение', "Вы уверены?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
