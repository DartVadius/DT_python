#!/usr/bin/python3 -u

from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QDialog, QMessageBox, QDesktopWidget, QToolTip, QPushButton, QTextEdit, QBoxLayout, QVBoxLayout, QHBoxLayout, \
    QFrame, QLineEdit, QFormLayout, QGroupBox, QScrollArea
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from classes.LeftMenu import LeftMenu
from connector import Connector


def action_decorator(method_to_decorate):
    def action_wrapper(self):
        self.main_window.removeItem(self.main_field)
        self.main_field = QVBoxLayout()
        method_to_decorate(self)
        # self.main_field.addStretch()
        self.main_window.addLayout(self.main_field)
        self.main_window.setStretchFactor(self.main_field, 9)

    return action_wrapper


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    central_widget = None
    grid_layout = None

    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.connector = Connector()

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
        self.main_window = QHBoxLayout()
        self.main_field = QVBoxLayout()
        self.main_widget = QFrame(self)
        self.main_field.addWidget(self.main_widget)
        self.left_menu = self.left_menu()
        self.main_window.addLayout(self.left_menu)
        self.main_window.addLayout(self.main_field)
        self.main_window.setStretchFactor(self.left_menu, 1)
        self.main_window.setStretchFactor(self.main_field, 9)
        return self.main_window

    def left_menu(self):
        left_menu = QVBoxLayout()
        names = [
            'Адресная книга',
            'Добавить запись',
            'Заметки',
            'Добавить заметку',
            'Настройки',
        ]
        actions = [
            self.show_addresses,
            self.show_test,
            self.show_test,
            self.show_test,
            self.show_test,
        ]
        for name, action in zip(names, actions):
            button = QPushButton(name)
            button.clicked.connect(action)
            button.setStyleSheet("width: 120px; height: 40px;")
            left_menu.addWidget(button)
        left_menu.addStretch()
        return left_menu

    @action_decorator
    def show_addresses(self):
        addresses = self.connector.get_all('addresses')
        self.main_widget = QScrollArea()
        self.main_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.main_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        widget = QWidget()
        layout = QVBoxLayout()
        for row in addresses:
            view = self.address_view(row)
            layout.addWidget(view)
        layout.addStretch()
        widget.setLayout(layout)
        self.main_widget.setWidget(widget)
        self.main_widget.setWidgetResizable(False)
        self.main_field.addWidget(self.main_widget)

    @action_decorator
    def show_test(self):
        addresses = self.connector.get_all('addresses')
        for row in addresses:
            print(row)

    def address_view(self, row=None):
        # print(row)
        formGroupBox = QGroupBox()
        # field_second_name = QLabel('Фамилия: ' + row['first_name'])
        # field_first_name = QLabel('Имя: ' + row['second_name'])
        user = QGridLayout()
        user.addWidget(QLabel('Фамилия:'), 0, 1)
        user.addWidget(QLabel(row['second_name']), 0, 2)
        user.addWidget(QLabel('Имя:'), 1, 1)
        user.addWidget(QLabel(row['first_name']), 1, 2)
        user.addWidget(QLabel('День рождения: '), 2, 1)
        user.addWidget(QLabel(row['birthday']), 2, 2)
        if row is not None and row['phone'] is not None:
            count = 4
            for number in row['phone']:
                user.addWidget(QLabel('Телефон: '), count, 1)
                user.addWidget(QLabel(number['phone']), count, 2)
                user.addWidget(QLabel('Тип: '), count, 3)
                user.addWidget(QLabel(number['type']), count, 4)
                count += 1

        # user.addWidget(field_first_name)
        user.addWidget(QLabel('Примечание: '), count + 1, 1)
        user.addWidget(QLabel(row['notes']), count + 1, 2, 10, 10)
        # user.addWidget(QLabel(''), 0, 5, 1, 10)
        formGroupBox.setLayout(user)
        # scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(400)
        # form = QFormLayout(self)
        # field_second_name = QLineEdit(self)
        # form.addRow(QLabel("Фамилия:"), field_second_name)
        # field_first_name = QLineEdit(self)
        # form.addRow(QLabel("Имя:"), field_first_name)
        # field_phone = QLineEdit(self)
        # field_phone_type = QLineEdit(self)
        # form.addRow(QLabel("Тип:"), field_phone_type)
        # form.addRow(QLabel("Телефон:"), field_phone)
        # if row is not None and row['phone'] is not None:
        #     for number in row['phone']:
        #         form.addRow(QLabel("Тип:"), QLineEdit(self).setText(number['type']))
        #         form.addRow(QLabel("Телефон:"), QLineEdit(self).setText(number['phone']))
        #         print(number['phone'])
        # formGroupBox.setLayout(form)
        return formGroupBox


    # настраиваем окно приложения
    def setup_app(self):
        self.setMinimumSize(QSize(800, 600))  # Устанавливаем размеры
        self.center()
        self.setWindowTitle("Address book")  # Устанавливаем заголовок окна
        self.setWindowIcon(QIcon('icon.png'))

    # настраиваем трей
    def set_tray(self):
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
