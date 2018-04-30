#!/usr/bin/python3 -u

from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QDialog, QMessageBox, QDesktopWidget, QToolTip, QPushButton, QTextEdit, QBoxLayout, QVBoxLayout, QHBoxLayout, \
    QFrame, QLineEdit, QFormLayout, QGroupBox, QScrollArea, QComboBox, QCalendarWidget, QDateEdit
from PyQt5.QtCore import QSize, Qt, QDate


class AddressForm:

    def __init__(self, user=None):
        print(user)
        self.form_layout = QFormLayout()
        self.second_name = QLineEdit()
        self.first_name = QLineEdit()
        self.birthday = QDateEdit()
        self.notes = QTextEdit()
        self.phones = list()
        if user is not None and user['second_name'] is not None:
            self.second_name.setText(user['second_name'])
        second_name_label = QLabel('Фамилия:')
        if user is not None and user['first_name'] is not None:
            self.first_name.setText(user['first_name'])
        first_name_label = QLabel('Имя:')
        self.birthday.setCalendarPopup(True)
        self.birthday.setDisplayFormat('dd.MM.yyyy')
        if user is not None and user['birthday'] is not None:
            self.birthday.setDate(QDate.fromString(user['birthday'], "d.M.yyyy"))
        birthday_label = QLabel('Дата рождения:')
        notes_label = QLabel('Примечание:')
        if user is not None and user['notes'] is not None:
            self.notes.setText(user['notes'])

        self.form_layout.addRow(second_name_label, self.second_name)
        self.form_layout.addRow(first_name_label, self.first_name)
        self.form_layout.addRow(birthday_label, self.birthday)
        self.form_layout.addRow(notes_label, self.notes)

        phone_label = QLabel('Телефон')
        self.form_layout.addRow(phone_label)
        if user is not None and user['phone'] is not None:
            for phone_row in user['phone']:
                phone = QLineEdit()
                phone.setText(phone_row['phone'])
                phone_type = QComboBox()
                phone_type.addItem('Домашний')
                phone_type.addItem('Рабочий')
                if phone_row['type'] == 'home':
                    phone_type.setCurrentIndex(0)
                if phone_row['type'] == 'work':
                    phone_type.setCurrentIndex(1)

                self.phones.append({
                    'phone': phone,
                    'type': phone_type
                })
                self.form_layout.addRow(phone_type, phone)
        phone = QLineEdit()
        phone_type = QComboBox()
        phone_type.addItem('Домашний')
        phone_type.addItem('Рабочий')
        self.phones.append({
            'phone': phone,
            'type': phone_type
        })

        self.form_layout.addRow(phone_type, phone)

    def add_row(self, *args):
        self.form_layout.addRow(*args)

    def get_layout(self):
        return self.form_layout

    def get_second_name(self):
        return self.second_name.text()

    def get_first_name(self):
        return self.first_name.text()

    def get_birthday(self):
        return self.birthday

    def get_notes(self):
        return self.notes.toPlainText()

    def get_phones(self):
        return self.phones
