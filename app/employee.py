#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Заводим новых работников
"""
import sys
import os
import data
import psycopg2
from functions_ import get_or_create
from sqlalchemy.sql import exists
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QMessageBox, QPushButton,
                             QToolTip, QDialog, QLineEdit, QCheckBox, QComboBox,
                             QFormLayout, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtCore import Qt

class RegisterClient(QDialog):
    def __init__(self, session):
        QDialog.__init__(self)  
        self.session = session
        self.init_ui()
        self.show()
     
    def init_ui(self):
        QToolTip.setFont(QFont('Font', 15))
        self.setFixedSize(700, 480)
        self.setWindowModality(2)
        self.setWindowTitle('Регистрируем клиента')
        self.setWindowIcon(QIcon(r'pics\employee.png'))

        buttons_layout = QHBoxLayout()

        back_button = QPushButton('Назад')
        back_button.setToolTip('Возвращаемся назад')
        back_button.clicked.connect(self.close)
        submit_button = QPushButton('Внести в базу данных')
        submit_button.setToolTip('Зарегистрировать очередного <b>работягу</b>?')
        submit_button.clicked.connect(self.process_data)
        buttons_layout.addWidget(back_button, alignment = Qt.AlignRight)
        buttons_layout.addWidget(submit_button)

        form_layout = QFormLayout(self)

        self.name_edit = QLineEdit()
        self.name_edit.setClearButtonEnabled(True)
        form_layout.addRow('Фамилия:<font color="red">*</font>', self.name_edit)

        self.surname_edit = QLineEdit()
        self.surname_edit.setClearButtonEnabled(True)
        form_layout.addRow('Имя:<font color="red">*</font>', self.surname_edit)

        self.patronymic_edit = QLineEdit()
        self.patronymic_edit.setClearButtonEnabled(True)
        form_layout.addRow('Отчество:', self.patronymic_edit)

        self.login_edit = QLineEdit()
        self.login_edit.setClearButtonEnabled(True)
        form_layout.addRow('Логин:<font color="red">*</font>', self.login_edit)

        self.email_edit = QLineEdit()
        self.email_edit.setClearButtonEnabled(True)
        form_layout.addRow('E-MAIL:', self.email_edit)

        self.phone_number_edit = QLineEdit()
        self.phone_number_edit.setClearButtonEnabled(True)

        self.position_edit = QComboBox()
        self.position_edit.setEditable(True)
        items = [row.name for row in self.session.query(data.Position) if row.name]      
        self.position_edit.addItems(items)
        self.position_edit.setCurrentText('')
        form_layout.addRow('Должность:', self.position_edit)

        self.department_edit = QComboBox()
        self.department_edit.setEditable(True)
        items = [row.name for row in self.session.query(data.Department) if row.name]
        self.department_edit.addItems(items)
        self.department_edit.setCurrentText('')
        form_layout.addRow('Отдел:', self.department_edit)

        self.comments_edit = QLineEdit()
        self.comments_edit.setClearButtonEnabled(True)
        form_layout.addRow('Прочее:', self.comments_edit)

        self.shared_folder_edit = QCheckBox()
        form_layout.addRow('Общие папки:', self.shared_folder_edit)

        self.network_printer_edit = QCheckBox()
        form_layout.addRow('Сетевой принтер:', self.network_printer_edit)


        self.labels.append(QLabel('Адрес'))
        self.labels.append(QLabel('№ корпуса'))
        self.labels.append(QLabel('№ комнаты'))

        self.labels.append(QLabel('Телефон'))

        self.labels.append(QLabel('Компьютеры пользователя'))

   


        
        
            
    @QtCore.pyqtSlot()
    def process_data(self):
        pass

    

###############################################################################################