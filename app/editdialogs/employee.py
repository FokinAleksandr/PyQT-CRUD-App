#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Полная информация о сотруднике
"""
from app.db import data
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

class EmployeeInfo(QDialog):
    def __init__(self, session, employee):
        QDialog.__init__(self)
        self.session = session
        self.employee = employee
        self.init_window()
        self.init_layouts()
        
    def init_window(self):
        self.setFixedWidth(550)
        self.setMaximumHeight(470)
        self.setWindowModality(2)
        self.setWindowTitle(
            '{} <{}>'.format(
                self.employee.fullname,
                self.employee.unique_login
                )
            )
        self.setWindowIcon(QIcon(r'pics\employee.png'))

    def init_layouts(self):
        buttons_layout = QHBoxLayout()

        back_button = QPushButton('Назад')
        back_button.clicked.connect(self.reject)

        edit_button = QPushButton('Редактировать')
        edit_button.clicked.connect(self.edit_employee_info)

        delete_button = QPushButton('Удалить')
        delete_button.setStyleSheet('QPushButton {color: red;}')
        delete_button.clicked.connect(self.delete_employee)

        submit_button = QPushButton('Сохранить')
        submit_button.clicked.connect(self.validate_input)

        buttons_layout.addStretch()
        buttons_layout.addWidget(back_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(submit_button)

        QVBoxLayout(self)
        self.layout().addLayout(buttons_layout)

    def edit_employee_info(self):
        pass
    def delete_employee(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Уведомление')
        msg_box.setText('Подтвердить удаление')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = msg_box.button(QMessageBox.Yes)
        buttonY.setText('Да')
        buttonN = msg_box.button(QMessageBox.No)
        buttonN.setText('Нет')
        msg_box.exec_()

        if msg_box.clickedButton() == buttonY:
            self.session.delete(self.employee)
            QDialog.accept(self)
            
    def validate_input(self):
        pass

