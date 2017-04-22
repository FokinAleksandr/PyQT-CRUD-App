#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Заводим новых работников
"""
import sys
import os
from app.dialogs import employee, pc, address
from app import data, excel
from app.functions import get_or_create
from functools import partial
from sqlalchemy import exc, distinct
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from sqlalchemy.orm import class_mapper, defer

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.init_ui()
        self.display_data()
        self.show()

    def init_ui(self):
        self.set_and_center_the_window(1024,768)
        self.setWindowTitle('Учет сотрудников и компьютеров РАН')
        self.setWindowIcon(QIcon(r'pics\star.png'))
        
        employee_action = QAction(QIcon(r'pics\add_user.png'), 'Добавить нового сотрудника', self)
        employee_action.triggered.connect(self.add_employee)
        pc_action = QAction(QIcon(r'pics\add_pc.png'), 'Добавить новый компьютер', self)
        pc_action.triggered.connect(self.add_pc)
        address_action = QAction(QIcon(r'pics\add_address.png'), 'Добавить новый адрес', self)
        address_action.triggered.connect(self.add_address)
        excel_action = QAction(QIcon(r'pics\excel.png'), 'Excel', self)
        excel_action.triggered.connect(self.excel)
        toolbar = QToolBar()
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        toolbar.addActions(
            [employee_action, pc_action, address_action, excel_action]
            )

    def display_data(self):
        self.employee_table = EmployeeTable()
        self.pc_table = QWidget()
        tab_widget = QTabWidget()
        tab_widget.addTab(self.employee_table, "Сотрудники")
        tab_widget.addTab(self.pc_table, "Компьютеры")
        self.setCentralWidget(tab_widget)
    
    def add_employee(self):
        session = data.Session()
        try:
            reg_employee_window = employee.RegisterClient(session)
            if reg_employee_window.exec_() == QDialog.Accepted:
                session.commit()
                self.employee_table.set_filter_comboboxes()
                self.employee_table.build_table()
                print("Закоммитили")
        except exc.IntegrityError as errmsg:
            print(errmsg)
            session.rollback()
            QMessageBox.critical(self, 'Критическая ошибка', 'Ошибка базы данных. Попробуйте еще раз.')
        else:
            print('Все успешно')
        finally:
            session.close()

    def add_pc(self):
        session = data.Session()
        try:
            reg_pc_window = pc.RegisterPC(session)
            if reg_pc_window.exec_() == QDialog.Accepted:
                session.commit()
                self.employee_table.set_filter_comboboxes()
                print("Закоммитили")
        except exc.IntegrityError as errmsg:
            print(errmsg)
            session.rollback()
            QMessageBox.critical(self, 'Критическая ошибка', 'Ошибка базы данных. Попробуйте еще раз.')
        else:
            print('Все успешно')
        finally:
            session.close()

    def add_address(self):
        session = data.Session()
        try:
            address_window = address.ConfigureAddresses(session)
            if address_window.exec_() == QDialog.Accepted:
                session.commit()
                self.employee_table.set_filter_comboboxes()
                print("Закоммитили")
        except exc.IntegrityError as errmsg:
            print(errmsg)
            session.rollback()
            QMessageBox.critical(
                self, 'Критическая ошибка', 'Ошибка базы данных. Попробуйте еще раз.'
                )
        else:
            print('Все успешно')
        finally:
            session.close()

    def excel(self):
        dlg = QInputDialog(self)                 
        dlg.setInputMode(QInputDialog.TextInput) 
        dlg.setTextValue(os.getcwd())
        dlg.setLabelText("Введите путь до файла:")                        
        dlg.resize(500,100)                             
        ok = dlg.exec_()                                
        path = dlg.textValue()
        if not os.path.exists(path):
            QMessageBox.warning(
                    self, 'Предупреждение', 'Неправильный путь!'
                    )
            return
        if ok:
            session = data.Session()
            try:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                excel.run(path, session)
            except PermissionError:
                QApplication.restoreOverrideCursor()
                QMessageBox.warning(
                    self, 'Предупреждение', 'Закройте файл Employees.xlsx в\n{}\nи попробуйте еще раз'.format(path)
                    )
            else:
                QApplication.restoreOverrideCursor()
                QMessageBox.information(
                    self, 'Уведомление', 'Файл Employees.xlsx сгенерирован в папку\n{}'.format(path)
                    )
            finally:
                session.close()

    def set_and_center_the_window(self, x, y):
        self.resize(1280, 768)
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

class EmployeeTable(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
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
        self.main_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.main_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_table.setColumnCount(9)
        self.main_table.setAlternatingRowColors(True)
        self.main_table.setHorizontalHeaderLabels(
            ['ФИО', 'Логин', 'Должность', 'Отдел', 'Место работы', 'Телефон',
             'Email', 'Домен/Имя компьютера', '']
            )
        self.main_table.setColumnWidth(0, 130)
        self.main_table.setColumnWidth(2, 150)
        self.main_table.setColumnWidth(3, 145)
        self.main_table.setColumnWidth(4, 120)
        self.main_table.setColumnWidth(6, 130)
        self.main_table.setColumnWidth(7, 180)

        self.layout().addLayout(filters_layout)
        self.layout().addWidget(self.main_table)
        self.set_filter_comboboxes()
        self.build_table()

    def set_filter_comboboxes(self):
        self.address_filter.clear()
        self.address_filter.addItem('Все')
        self.address_filter.addItems(
            self.session.query(data.Address.name).values()
            )

        self.block_filter.clear()
        self.block_filter.addItem('Все')
        self.block_filter.addItems(
            self.session.query(data.Block.name).\
                distinct(data.Block.name).\
                values()
            )

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
        employees = self.session.query(data.Employee).\
            join(data.Room).\
            join(data.Block).\
            join(data.Address).\
            outerjoin(data.Phone).\
            outerjoin(data.Department).\
            outerjoin(data.Position).\
            filter(data.Employee.fullname.ilike('%' + self.fio_filter.text() + '%')).\
            filter(data.Employee.unique_login.ilike('%' + self.login_filter.text() + '%'))

        if self.phone_filter.text():
            employees = employees.filter(data.Phone.number.like('%' + self.phone_filter.text() + '%'))
        if self.department_filter.currentText():
            employees = employees.filter(data.Department.name.ilike('%' + self.department_filter.currentText() + '%'))
        if self.position_filter.currentText():
            employees = employees.filter(data.Position.name.ilike('%' + self.position_filter.currentText() + '%'))
        if self.address_filter.currentText() != 'Все':
            employees = employees.filter(data.Address.name==self.address_filter.currentText())
        if self.block_filter.currentText() != 'Все':
            employees = employees.filter(data.Block.name==self.block_filter.currentText())
        if self.room_filter.text():
            employees = employees.filter(data.Room.name.like('%' + self.room_filter.text() + '%'))

        for row, employee in enumerate(employees):
            self.main_table.insertRow(row)
            self.main_table.setRowHeight(row, 50)
            self.main_table.setItem(row, 0, QTableWidgetItem(QIcon(r'pics\employee.png'), employee.fullname))
            self.main_table.setItem(row, 1, QTableWidgetItem(employee.unique_login))
            self.main_table.setItem(row, 2, QTableWidgetItem(employee.position.name))
            self.main_table.setItem(row, 3, QTableWidgetItem(employee.department.name))
            self.main_table.setItem(row, 4, QTableWidgetItem(employee.room.block.address.name + ', ' + employee.room.block.name + '\n' + employee.room.name))
            self.main_table.setItem(row, 5, QTableWidgetItem('\n'.join(phone.number for phone in employee.phone)))
            self.main_table.setItem(row, 6, QTableWidgetItem('\n'.join(email.email for email in employee.email)))
            self.main_table.setItem(row, 7, QTableWidgetItem(QIcon(r'pics\pc.png'), ' \n'.join(pc.pcname.domain.name + '/' + pc.pcname.name for pc in employee.pc)))
            edit_button = QPushButton('Просмотреть')
            edit_button.clicked.connect(
                partial(self.edit_employee, employee=employee)
                )
            self.main_table.setCellWidget(row, 8, edit_button)

    @QtCore.pyqtSlot(data.Employee)
    def edit_employee(self, employee):
        print("Пока не готово")
            
 