#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Заводим новых работников
"""
from app.editdialogs import employee
from app.db import data
from functools import partial
from sqlalchemy import exc
from sqlalchemy.orm import joinedload
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *


class EmployeeTable(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.session = data.Session()
        QVBoxLayout(self)

        filters_layout = QHBoxLayout()
        #########################################################
        personal_info_layout = QVBoxLayout()

        self.fio_filter = QLineEdit()
        self.fio_filter.setFixedWidth(230)
        self.fio_filter.setPlaceholderText('ФИО')
        personal_info_layout.addWidget(self.fio_filter)

        self.login_filter = QLineEdit()
        self.login_filter.setFixedWidth(230)
        self.login_filter.setPlaceholderText('Логин')
        personal_info_layout.addWidget(self.login_filter)

        self.phone_filter = QLineEdit()
        self.phone_filter.setFixedWidth(100)
        self.phone_filter.setPlaceholderText('Телефон')
        personal_info_layout.addWidget(self.phone_filter)

        personal_info_labels_layout = QVBoxLayout()
        personal_info_labels_layout.addWidget(QLabel('<h4>ФИО</h4>'))
        personal_info_labels_layout.addWidget(QLabel('<h4>Логин</h4>'))
        personal_info_labels_layout.addWidget(QLabel('<h4>Телефон</h4>'))

        filters_layout.addLayout(personal_info_labels_layout)
        filters_layout.addLayout(personal_info_layout)
        #########################################################
        address_info_layout = QHBoxLayout()

        self.address_filter = QComboBox()
        address_info_layout.addWidget(self.address_filter)
        self.block_filter = QComboBox()
        address_info_layout.addWidget(self.block_filter)

        self.room_filter = QLineEdit()
        self.room_filter.setFixedWidth(50)
        self.room_filter.setPlaceholderText('Комната')
        address_info_layout.addWidget(self.room_filter)
        #########################################################
        employee_info_layout = QVBoxLayout()

        self.position_filter = QComboBox()
        self.position_filter.setEditable(True)
        employee_info_layout.addWidget(self.position_filter)

        self.department_filter = QComboBox()
        self.department_filter.setEditable(True)
        employee_info_layout.addWidget(self.department_filter)
        employee_info_layout.addLayout(address_info_layout)

        employee_info_labels_layout = QVBoxLayout()
        employee_info_labels_layout.addWidget(QLabel('<h4>Должность</h4>'))
        employee_info_labels_layout.addWidget(QLabel('<h4>Отдел</h4>'))
        employee_info_labels_layout.addWidget(QLabel('<h4>Место Работы</h4>'))
        filters_layout.addLayout(employee_info_labels_layout)
        filters_layout.addLayout(employee_info_layout)
        #########################################################
        find_button = QPushButton('Найти')
        find_button.setFixedSize(80, 80)
        find_button.clicked.connect(self.build_table)
        filters_layout.addWidget(find_button)
        filters_layout.addStretch()

        self.main_table = QTableWidget()
        self.main_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.main_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_table.setTextElideMode(Qt.ElideNone)
        self.main_table.setAlternatingRowColors(True)
        self.main_table.setColumnCount(9)
        self.main_table.setHorizontalHeaderLabels(
            ['ФИО', 'Логин', 'Должность', 'Отдел', 'Место работы', 'Телефон',
             'Email', 'Домен/Имя компьютера', '']
        )
        self.layout().addLayout(filters_layout)
        self.layout().addWidget(self.main_table)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.set_filter_comboboxes()
        self.build_table()
        QApplication.restoreOverrideCursor()

    def set_filter_comboboxes(self):
        self.address_filter.clear()
        self.address_filter.addItem('Все')
        self.address_filter.addItems(
            self.session.query(data.Address.name).values()
        )

        self.block_filter.clear()
        self.block_filter.addItem('Все')
        self.block_filter.addItems(self.session.query(data.Block.name).distinct(data.Block.name).values())
        self.position_filter.clear()
        self.position_filter.addItem('')
        self.position_filter.addItems(
            row.name for row in self.session.query(data.Position) if row.name
        )

        self.department_filter.clear()
        self.department_filter.addItem('')
        self.department_filter.addItems(
            row.name for row in self.session.query(data.Department) if row.name
        )

    def build_table(self):
        self.main_table.setRowCount(0)
        employees = self.session.query(data.Employee). \
            join(data.Room).\
            join(data.Block).\
            join(data.Address).\
            outerjoin(data.Phone).\
            outerjoin(data.Department).\
            outerjoin(data.Position).\
            filter(
            data.Employee.fullname.ilike('%{}%'.format(self.fio_filter.text()))
        ).\
            filter(
            data.Employee.unique_login.ilike('%{}%'.format(self.login_filter.text()))
        )

        if self.phone_filter.text():
            employees = employees.filter(
                data.Phone.number.like('%{}%'.format(self.phone_filter.text()))
            )
        if self.department_filter.currentText():
            employees = employees.filter(
                data.Department.name.ilike('%{}%'.format(self.department_filter.currentText()))
            )
        if self.position_filter.currentText():
            employees = employees.filter(
                data.Position.name.ilike('%{}%'.format(self.position_filter.currentText()))
            )
        if self.address_filter.currentText() != 'Все':
            employees = employees.filter(
                data.Address.name == self.address_filter.currentText()
            )
        if self.block_filter.currentText() != 'Все':
            employees = employees.filter(
                data.Block.name == self.block_filter.currentText()
            )
        if self.room_filter.text():
            employees = employees.filter(
                data.Room.name.like('%{}%'.format(self.room_filter.text()))
            )

        for row, employee in enumerate(employees):
            self.main_table.insertRow(row)
            self.main_table.setRowHeight(row, 50)
            self.main_table.setItem(row, 0,
                                    QTableWidgetItem(
                                        QIcon(r'pics\employee.png'),
                                        employee.fullname
                                    )
                                    )
            self.main_table.setItem(row, 1,
                                    QTableWidgetItem(
                                        employee.unique_login
                                    )
                                    )
            self.main_table.setItem(row, 2,
                                    QTableWidgetItem(
                                        employee.position.name
                                    )
                                    )
            self.main_table.setItem(row, 3,
                                    QTableWidgetItem(
                                        employee.department.name
                                    )
                                    )
            self.main_table.setItem(row, 4,
                                    QTableWidgetItem(
                                        employee.room.block.address.name +
                                        ', ' +
                                        employee.room.block.name +
                                        '\n' +
                                        employee.room.name
                                    )
                                    )
            self.main_table.setItem(row, 5,
                                    QTableWidgetItem(
                                        ';\n'.join(
                                            phone.number
                                            for phone
                                            in employee.phone
                                        )
                                    )
                                    )
            self.main_table.setItem(row, 6,
                                    QTableWidgetItem(
                                        ';\n'.join(
                                            email.email
                                            for email
                                            in employee.email
                                        )
                                    )
                                    )
            self.main_table.setItem(row, 7,
                                    QTableWidgetItem(
                                        QIcon(r'pics\pc.png'),
                                        ';\n'.join(
                                            pc.pcname.domain.name +
                                            '/' +
                                            pc.pcname.name
                                            for pc
                                            in employee.pc
                                        )
                                    )
                                    )
            edit_button = QPushButton('Просмотреть')
            edit_button.clicked.connect(
                partial(self.edit_employee, employee_query_obj=employee)
            )
            self.main_table.setCellWidget(row, 8, edit_button)
        self.main_table.resizeColumnsToContents()

    @QtCore.pyqtSlot(data.Employee)
    def edit_employee(self, employee_query_obj):
        try:
            edit_employee_window = employee.EmployeeInfo(self.session, employee_query_obj)
            if edit_employee_window.exec_() == QDialog.Accepted:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                for room in self.session.query(data.Room). \
                        options(joinedload(data.Room.employee)). \
                        filter(data.Room.employee == None). \
                        all():
                    self.session.delete(room)

                for position in self.session.query(data.Position). \
                        options(joinedload(data.Position.employee)). \
                        filter(data.Position.employee == None). \
                        all():
                    self.session.delete(position)

                for department in self.session.query(data.Department). \
                        options(joinedload(data.Department.employee)). \
                        filter(data.Department.employee == None). \
                        all():
                    self.session.delete(department)

                self.session.commit()
                self.set_filter_comboboxes()
                self.build_table()
                QApplication.restoreOverrideCursor()
                print("Закоммитили")
        except exc.IntegrityError as errmsg:
            print(errmsg)
            self.session.rollback()
            QMessageBox.critical(self, 'Критическая ошибка', 'Ошибка базы данных. Попробуйте еще раз.')
        else:
            print('Все успешно')
