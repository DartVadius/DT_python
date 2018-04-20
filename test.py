#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QAction, QSystemTrayIcon, QStyle, QMenu, qApp, \
    QMenuBar, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(480, 320)
        self.center()
        # self.move(300, 300)
        self.setWindowTitle('Address book')
        # self.setWindowTitle('Icon')
        path = os.path.join(os.getcwd(), 'icon.png')
        self.setWindowIcon(QIcon(path))
        grid_layout = QGridLayout(self)
        self.setLayout(grid_layout)
        title = QLabel("Address book on the PyQt5", self)  # Создаём лейбл
        title.setAlignment(QtCore.Qt.AlignCenter)  # Устанавливаем позиционирование текста
        grid_layout.addWidget(title)  # и добавляем его в размещение

        # hide_action = QAction("&Hide", self)
        # hide_action.triggered.connect(self.hide)
        #
        # exit_action = QAction("&Exit", self)  # Создаём Action с помощью которого будем выходить из приложения
        # exit_action.setShortcut('Ctrl+Q')  # Задаём для него хоткей
        # # Подключаем сигнал triggered к слоту quit у qApp.
        # exit_action.triggered.connect(qApp.quit)
        #
        # # exit_action.triggered.connect(self.close)
        # # Устанавливаем в панель меню данный Action.
        # # self.statusBar()
        # main_menu = self.
        # hide_menu = main_menu.addMenu('Hide')
        # file_menu = main_menu.addMenu('Exit')
        #
        # hide_menu.addAction(hide_action)
        # file_menu.addAction(exit_action)

        # сворачивание приложения в трей
        # self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        # show_action = QAction("Show", self)
        # quit_action = QAction("Exit", self)
        # hide_action = QAction("Hide", self)
        # show_action.triggered.connect(self.show)
        # hide_action.triggered.connect(self.hide)
        # quit_action.triggered.connect(qApp.quit)
        # tray_menu = QMenu()
        # tray_menu.addAction(show_action)
        # tray_menu.addAction(hide_action)
        # tray_menu.addAction(quit_action)
        # self.tray_icon.setContextMenu(tray_menu)
        # self.tray_icon.show()
        self.show()

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


if __name__ == '__main__':
    import sys
    import os

    app = QApplication(sys.argv)
    # path = os.path.join(os.getcwd(), 'icon.png')
    # print(path)
    # app.setWindowIcon(QIcon(QPixmap('icon.png')))
    widget = Application()
    sys.exit(app.exec_())
