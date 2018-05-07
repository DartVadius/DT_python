#!/usr/bin/python3 -u

from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QDialog, QMessageBox, QDesktopWidget, QToolTip, QPushButton, QTextEdit, QBoxLayout, QVBoxLayout, QHBoxLayout, \
    QFrame, QLineEdit, QFormLayout, QGroupBox, QScrollArea, QComboBox, QCalendarWidget, QDateEdit
from PyQt5.QtCore import QSize, Qt, QDate


class NotesForm:
    note_id = None

    def __init__(self, note=None):
        self.form_layout = QFormLayout()
        self.date = QDateEdit()
        self.notes = QTextEdit()
        self.notes.setMinimumHeight(420)
        if note is not None and note['id'] is not None:
            self.note_id = note['id']

        self.date.setCalendarPopup(True)
        self.date.setDisplayFormat('dd MMMM yyyy')
        if note is not None and note['date'] is not None:
            self.date.setDate(QDate.fromString(note['date'], "d.M.yyyy"))
        date_label = QLabel('Дата:')
        notes_label = QLabel('Примечание:')
        if note is not None and note['notes'] is not None:
            self.notes.setText(note['notes'])

        self.form_layout.addRow(date_label, self.date)
        self.form_layout.addRow(notes_label, self.notes)

    def get_layout(self):
        return self.form_layout

    def get_date(self):
        tmp_date = self.date.date()
        tmp_date = tmp_date.toPyDate()
        return '{0:%d.%m.%Y}'.format(tmp_date)

    def get_notes(self):
        return self.notes.toPlainText()

    def get_note_id(self):
        return self.note_id

    def validate_form(self):
        errors = list()
        # errors.append(self.first_name.validator())