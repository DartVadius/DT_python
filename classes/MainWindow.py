#!/usr/bin/python3 -u

from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QDialog, QMessageBox, QDesktopWidget, QToolTip, QPushButton, QTextEdit, QBoxLayout, QVBoxLayout, QHBoxLayout, \
    QFrame, QLineEdit, QFormLayout, QGroupBox, QScrollArea, QComboBox, QCalendarWidget, QDateEdit
from PyQt5.QtCore import QSize, Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap, QFont
from connector import Connector
from classes.AddressForm import AddressForm
from classes.NotesForm import NotesForm


def clear_layout(layout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        if not item:
            continue
        w = item.widget()
        if w:
            w.deleteLater()


def action_decorator(method_to_decorate):
    def action_wrapper(self):
        clear_layout(self.main_field)
        method_to_decorate(self)

    return action_wrapper


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    main_window = None
    main_field = None
    main_widget = None
    left_menu = None
    form_layout = None

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
            self.add_address,
            self.show_notes,
            self.add_notes,
            self.show_test,
        ]
        for name, action in zip(names, actions):
            button = QPushButton(name)
            button.clicked.connect(action)
            button.setStyleSheet("width: 130px; height: 40px;")
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
    def show_notes(self):
        notes = self.connector.get_all('notes')
        self.main_widget = QScrollArea()
        self.main_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.main_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        widget = QWidget()
        layout = QVBoxLayout()
        for row in notes:
            view = self.note_view(row)
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

    @action_decorator
    def add_address(self):
        self.main_widget = QGroupBox()
        self.form_layout = AddressForm()
        self.main_widget.setLayout(self.form_layout.get_layout())
        self.main_field.addWidget(self.main_widget)
        self.main_field.addStretch()
        button_layout = self.button_layout()
        group_box = QGroupBox(self)
        group_box.setLayout(button_layout)

        self.main_field.addWidget(group_box)

    @action_decorator
    def add_notes(self):
        self.main_widget = QGroupBox()
        self.form_layout = NotesForm()
        self.main_widget.setLayout(self.form_layout.get_layout())
        self.main_field.addWidget(self.main_widget)
        self.main_field.addStretch()
        button_layout = self.button_layout_notes()
        group_box = QGroupBox(self)
        group_box.setLayout(button_layout)

        self.main_field.addWidget(group_box)

    @action_decorator
    def edit_address(self):
        source = self.sender()
        user = self.connector.get_by_id(source.table, source.id)
        self.main_widget = QGroupBox()
        self.form_layout = AddressForm(user)
        self.main_widget.setLayout(self.form_layout.get_layout())
        self.main_field.addWidget(self.main_widget)
        self.main_field.addStretch()
        button_layout = self.button_layout()
        group_box = QGroupBox(self)
        group_box.setLayout(button_layout)

        self.main_field.addWidget(group_box)

    @action_decorator
    def edit_note(self):
        pass

    def button_layout_notes(self):
        button_layout = QGridLayout()

        button = QPushButton('Сохранить')
        button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')))
        button.clicked.connect(self.save_note)
        button.setStyleSheet("width: 90px; height: 20px;")

        button_layout.addWidget(button, 1, 1, 1, 1)

        if self.form_layout.get_note_id() is not None:
            button = QPushButton('Удалить')
            button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogCancelButton')))
            button.clicked.connect(self.remove_note())
            button.setStyleSheet("width: 90px; height: 20px;")

            button_layout.addWidget(button, 1, 2, 1, 1)

        button_layout.addWidget(QLabel(), 1, 3, 1, 10)
        return button_layout

    def button_layout(self):
        button_layout = QGridLayout()

        button = QPushButton('Телефон')
        button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_ArrowUp')))
        button.clicked.connect(self.add_field)
        button.setStyleSheet("width: 90px; height: 20px;")

        button_layout.addWidget(button, 1, 0, 1, 1)

        button = QPushButton('Сохранить')
        button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')))
        button.clicked.connect(self.save_user)
        button.setStyleSheet("width: 90px; height: 20px;")

        button_layout.addWidget(button, 1, 1, 1, 1)

        if self.form_layout.get_user_id() is not None:
            button = QPushButton('Удалить')
            button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogCancelButton')))
            button.clicked.connect(self.remove_user)
            button.setStyleSheet("width: 90px; height: 20px;")

            button_layout.addWidget(button, 1, 2, 1, 1)

        button_layout.addWidget(QLabel(), 1, 3, 1, 10)
        return button_layout

    def save_note(self):
        pass

    def save_user(self):
        user = self.connector.get_by_id('addresses', self.form_layout.get_user_id())
        user['first_name'] = self.form_layout.get_first_name()
        user['second_name'] = self.form_layout.get_second_name()
        user['notes'] = self.form_layout.get_notes()
        user['birthday'] = self.form_layout.get_birthday()
        user['phone'] = list()
        for phone in self.form_layout.get_phones():
            if phone['phone'].text() != '':
                if phone['type'].currentIndex() == 0:
                    phone_type = 'home'
                else:
                    phone_type = 'work'
                user['phone'].append({
                    'phone': phone['phone'].text(),
                    'type': phone_type
                })
        if 'id' not in user or user['id'] is None:
            self.connector.add_row('addresses', user)
        else:
            self.connector.update_by_id('addresses', user['id'], user)
        self.show_addresses()

    def remove_user(self):
        self.connector.delete_by_id('addresses', self.form_layout.get_user_id())
        self.show_addresses()

    def remove_note(self):
        pass

    def add_field(self):
        phone_type = QComboBox(self)
        phone_type.addItem('Домашний')
        phone_type.addItem('Рабочий')
        phone = QLineEdit()
        self.form_layout.phones.append({
            'phone': phone,
            'type': phone_type
        })
        self.form_layout.add_row(phone_type, phone)

    def note_view(self, row=None):
        group_box = QGroupBox(self)
        note = QGridLayout()
        note.addWidget(QLabel('Дата: '), 0, 1)
        note.addWidget(QLabel(row['date']), 0, 2)
        note.addWidget(QLabel('Примечание: '), 1, 1)
        note.addWidget(QLabel(row['notes']), 1, 2, 1, 10)
        button = QPushButton('Редактировать')
        button.clicked.connect(self.edit_note)
        button.setStyleSheet("width: 110px; height: 20px;")
        button.id = row['id']
        button.table = 'notes'
        note.addWidget(button, 0, 10, 2, 1)
        group_box.setLayout(note)
        return group_box

    def address_view(self, row=None):
        group_box = QGroupBox(self)
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
                phone = QLabel(number['phone'])
                phone.setTextInteractionFlags(Qt.TextSelectableByMouse)
                user.addWidget(phone, count, 2)
                user.addWidget(QLabel('Тип: '), count, 3)
                user.addWidget(QLabel(number['type']), count, 4)
                count += 1
        user.addWidget(QLabel('Примечание: '), count + 1, 1)
        user.addWidget(QLabel(row['notes']), count + 1, 2, 1, 10)
        button = QPushButton('Редактировать')
        button.clicked.connect(self.edit_address)
        button.setStyleSheet("width: 110px; height: 20px;")
        button.id = row['id']
        button.table = 'addresses'
        user.addWidget(button, 0, 10, 2, 1)
        group_box.setLayout(user)
        return group_box

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
        show_action = QAction("Показать", self)
        quit_action = QAction("Выйти", self)
        hide_action = QAction("Спрятать", self)
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
        hide_action = QAction(QIcon("icon.png"), "&Спрятать", self)
        hide_action.triggered.connect(self.hide)
        exit_action = QAction("&Выйти", self)  # Создаём Action с помощью которого будем выходить из приложения
        exit_action.setShortcut('Ctrl+Q')  # Задаём для него хоткей
        exit_action.triggered.connect(self.close)  # Подключаем сигнал triggered к слоту quit у qApp.
        # test_action = QAction("&Test", self)
        # test_action.triggered.connect(self.test)

        # панель меню
        main_menu = self.menuBar()
        hide_menu = main_menu.addMenu('Спрятать')
        file_menu = main_menu.addMenu('Выйти')
        # test_menu = main_menu.addMenu('Test')
        hide_menu.addAction(hide_action)
        file_menu.addAction(exit_action)
        # test_menu.addAction(test_action)

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
