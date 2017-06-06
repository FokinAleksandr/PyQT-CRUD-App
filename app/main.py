#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Заводим новых работников
"""
import sys
import os
from app import login, excel
from app.regdialogs import address, employee, pc
from app.tablewidgets import employees, pcs
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
        self.set_and_center_the_window(1024, 768)
        self.setWindowTitle('Учет сотрудников и компьютеров РАН')
        self.setWindowIcon(QIcon(r'pics\star.png'))

        employee_action = QAction(
            QIcon(r'pics\add_user.png'), 'Добавить нового сотрудника', self
        )
        employee_action.triggered.connect(self.add_employee)
        pc_action = QAction(
            QIcon(r'pics\add_pc.png'), 'Добавить новый компьютер', self
        )
        pc_action.triggered.connect(self.add_pc)
        address_action = QAction(
            QIcon(r'pics\add_address.png'), 'Добавить новый адрес', self
        )
        address_action.triggered.connect(self.add_address)
        excel_action = QAction(
            QIcon(r'pics\excel.png'), 'Excel', self
        )
        excel_action.triggered.connect(self.excel)
        toolbar = QToolBar()
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        toolbar.addActions(
            [employee_action, pc_action, address_action, excel_action]
        )

    def display_data(self):
        session = data.Session()
        try:
            self.employee_table = employees.EmployeeTable(session, self)
            self.pcs_table = pcs.PcsTable(session, self)
            tab_widget = QTabWidget()
            tab_widget.addTab(self.employee_table, "Сотрудники")
            tab_widget.addTab(self.pcs_table, "Компьютеры")
            self.setCentralWidget(tab_widget)
        except exc.IntegrityError as errmsg:
            print(errmsg)
            session.rollback()
            session.close()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Критическая ошибка базы данных")
            msg.setWindowTitle("Критическая ошибка")
            msg.setDetailedText(errmsg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(sys.exit)
        

    def add_employee(self):
        session = data.Session()
        try:
            reg_employee_window = employee.RegisterEmployee(session)
            if reg_employee_window.exec_() == QDialog.Accepted:
                session.commit()
                QMessageBox.information(
                    self, 'Уведомление',
                    'Сотрудник успешно добавлен'
                )
                QApplication.setOverrideCursor(Qt.WaitCursor)
                self.employee_table.set_filter_comboboxes()
                self.employee_table.fill_table()
                self.pcs_table.update_table_content()
                QApplication.restoreOverrideCursor()
                print("Закоммитили")
        except exc.IntegrityError as errmsg:
            print(errmsg)
            session.rollback()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Критическая ошибка базы данных")
            msg.setWindowTitle("Критическая ошибка")
            msg.setDetailedText(errmsg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(sys.exit)
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
                QMessageBox.information(
                    self, 'Уведомление',
                    'Компьютер успешно добавлен'
                )
                QApplication.setOverrideCursor(Qt.WaitCursor)
                self.employee_table.fill_table()
                self.pcs_table.update_table_content()
                QApplication.restoreOverrideCursor()
        except exc.IntegrityError as errmsg:
            print(errmsg)
            session.rollback()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Критическая ошибка базы данных")
            msg.setWindowTitle("Критическая ошибка")
            msg.setDetailedText(errmsg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(sys.exit)
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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Критическая ошибка базы данных")
            msg.setWindowTitle("Критическая ошибка")
            msg.setDetailedText(errmsg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(sys.exit)
        else:
            print('Все успешно')
        finally:
            session.close()

    def excel(self):
        filename = QFileDialog.getSaveFileName(self, 'Сохрание excel файла', filter='*.xlsx')
        if not filename[1]:
            return
        else:
            filename = filename[0]
        session = data.Session()
        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            excel.run(filename, session)
        except PermissionError:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(
                self, 'Предупреждение',
                'Закройте {}\n' +
                'и попробуйте еще раз'.format(filename)
            )
        except OSError:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(
                self, 'Ошибка!',
                'Попробуйте другой путь'
            )
        else:
            QApplication.restoreOverrideCursor()
            QMessageBox.information(
                self, 'Уведомление',
                'Сгенерирован: {}'.format(filename)
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

    splash_pix = QPixmap(r'pics\splash_loading.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    login_window = login.LoginWindow()
    splash.finish(login_window)
    result = login_window.exec_()

    splash_pix = QPixmap(r'pics\splash_loading.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    if result == QDialog.Accepted:
        main_window = MainWindow()
        splash.finish(main_window)
    else:
        sys.exit(result)

    sys.exit(app.exec_())
