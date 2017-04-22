#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Заводим новых работников
"""
import sys
import os
from app import login, excel
from app.regdialogs import address, employee, pc
from app.tablewidgets.employees import EmployeeTable
from app.db import data
from sqlalchemy import exc
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

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

def run():
    app = QApplication([])
    
    login_window = login.LoginWindow()

    result = login_window.exec_()
    if result == QDialog.Accepted:
        main_window = MainWindow()
    else:
        sys.exit(result)

    sys.exit(app.exec_())