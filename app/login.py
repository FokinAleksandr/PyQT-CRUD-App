#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Login
"""
import sqlalchemy
import psycopg2
from sqlalchemy.orm import sessionmaker
from PyQt5.QtWidgets import (QPushButton, QLabel, QLineEdit, QDialog,
                             QMessageBox, QFormLayout, QDialogButtonBox)
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
import data

class LoginWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle('Логин')
        self.setWindowIcon(QIcon(r'pics\star.png'))
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        
        self.employeename_input = QLineEdit('bog')
        self.password_input = QLineEdit('1234') 
        self.password_input.setEchoMode(QLineEdit.Password)
        self.db_input = QLineEdit('diplom')

        ip_range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"   # Часть регулярного выржение
        # Само регулярное выражение
        ipRegex = QRegExp("^" + ip_range + "\\." + ip_range + "\\." + ip_range + "\\." + ip_range + "$")
        ipValidator = QRegExpValidator(ipRegex)   # Валидатор для QLineEdit
        self.host_input = QLineEdit('127.0.0.1')
        self.host_input.setValidator(ipValidator)

        self.port_input = QLineEdit('5432')

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        button_box.setCenterButtons(True)
        button_box.accepted.connect(self.handle_login)
        button_box.rejected.connect(self.reject)

        layout = QFormLayout(self)
        layout.addRow('Username', self.employeename_input)
        layout.addRow('Password', self.password_input)
        layout.addRow('Database', self.db_input)
        layout.addRow('Host', self.host_input)
        layout.addRow('Port', self.port_input)
        layout.addRow(button_box)    

    def handle_login(self):
        url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'
        url = url.format(self.employeename_input.text(), self.password_input.text(),
                        self.host_input.text(), self.port_input.text(), self.db_input.text()
        )
        try:
            engine = sqlalchemy.create_engine(url, echo=True)
            data.Base.metadata.create_all(engine)
        except ValueError:
            QMessageBox.warning(self, 'Ошибка!', 'Неправильно введены данные!')
        except Exception:        
            QMessageBox.warning(self, 'Ошибка!', 'Не удается подключиться к базе данных')   
        else:
            data.Session = sessionmaker(bind=engine)
            self.accept()
        