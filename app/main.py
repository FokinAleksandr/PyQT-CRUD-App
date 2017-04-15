#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Заводим новых работников
"""
import sys
import os
from app.dialogs import employee, pc, address
from app import data
from app.functions import get_or_create
from sqlalchemy import exc
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTabWidget, QDialog,
                             QPushButton,QToolTip, QAction, QLabel,
                             QLineEdit, QDesktopWidget, QVBoxLayout, QFormLayout,
                             QHBoxLayout, QMessageBox, QFrame, QSplitter, QTextEdit)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.init_ui()
        self.display_data()
        self.show()

    def init_ui(self):
        self.set_and_center_the_window(900,900)
        self.setWindowTitle('РАН НИИ')
        self.setWindowIcon(QIcon(r'pics\star.png'))
        
        employee_action = QAction(QIcon(r'pics\employee.png'), 'Employee', self)
        employee_action.triggered.connect(self.add_employee)
        pc_action = QAction(QIcon(r'pics\pc.png'), 'Pc', self)
        pc_action.triggered.connect(self.add_pc)
        address_action = QAction(QIcon(r'pics\home.png'), 'Address', self)
        address_action.triggered.connect(self.add_address)
        refresh_action = QAction(QIcon(r'pics\refresh.png'), 'Refresh', self)
        refresh_action.triggered.connect(self.refresh)
        toolbar = self.addToolBar('asdf')
        toolbar.addActions([employee_action, pc_action, address_action, refresh_action])

    def display_data(self):
        main_widget = MainWidget()
        self.setCentralWidget(main_widget)
    
    def add_employee(self):
        session = data.Session()
        try:
            reg_employee_window = employee.RegisterClient(session)
            if reg_employee_window.exec_() == QDialog.Accepted:
                session.commit()
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
                print("Закоммитили")
        except exc.IntegrityError as errmsg:
            print(errmsg)
            session.rollback()
            QMessageBox.critical(self, 'Критическая ошибка', 'Ошибка базы данных. Попробуйте еще раз.')
        else:
            print('Все успешно')
        finally:
            session.close()
    
    def refresh(self):
        self.display_data()

    def set_and_center_the_window(self, x, y):
        """ Задаем окно (x, y), выравниваем по центру экрана """
        self.setFixedSize(x, y)
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.init_ui()
        self.show()

    def init_ui(self):
        session = data.Session()
        QVBoxLayout(self)
        address_tab = QTabWidget()
        self.layout().addWidget(address_tab)
        addresses = session.query(data.Address).all()

        for address in addresses:
            block_tab = QTabWidget()

            for block in session.query(data.Block).\
                        with_parent(address):
                block_tab.addTab(QLabel(block.name), block.name)

            address_tab.addTab(block_tab, address.name)
        session.close()