#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Полная информация о сотруднике
"""
from app.db import data
from app.tools.functions import get_or_create
from app.tools.exitmethods import Dialog
from app.tablewidgets.pcsadd import PCAdd
from _functools import partial
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

class EmployeeInfo(Dialog):
    def __init__(self, session, employee):
        QDialog.__init__(self)
        self.session = session
        self.employee = employee
        self.sti = QStandardItemModel()
        self.fill_table_model()

        QStackedLayout(self)
       
        self.read_only_widget = self.get_read_only_widget()
        self.setLabelsText()
        self.edit_info_widget = self.get_edit_info_widget()
        self.setLineEdits()

        self.layout().addWidget(self.read_only_widget)
        self.layout().addWidget(self.edit_info_widget)
        self.layout().setCurrentIndex(0)

        self.init_window()

    def init_window(self):
        self.setFixedSize(800, 450)
        self.setWindowModality(2)
        self.setWindowTitle(
            '{} <{}>'.format(
                self.employee.fullname,
                self.employee.unique_login
                )
            )
        self.setWindowIcon(QIcon(r'pics\employee.png'))

    def fill_table_model(self):
        self.sti.setHorizontalHeaderLabels(
            ['Домен', 'Имя компьютера', 'MAC-адрес', 'Номер розетки',
             'Как подключен', 'Серверные приложения',
             'Windows OS', 'Windows OS key', 'Microsoft Office',
             'Microsoft Office key', 'Антивирус', 'Клиент электронной почты',
             'Прочее', 'Агент KES', 'Консультант', 'Гарант', '1C', 'КДС']
            )
        for pc in self.employee.pc:
            self.new_row(pc)

    def get_read_only_widget(self):
        read_only_widget = QWidget()
        read_only_layout = QFormLayout(read_only_widget)
        read_only_layout.setSpacing(10);
        ############################################################
        self.back_button = QPushButton('Выйти')
        self.back_button.clicked.connect(self.reject)
        self.edit_button = QPushButton('Редактировать')
        self.edit_button.clicked.connect(self.edit_employee_info)
        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.delete_employee)
        ############################################################
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.back_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)

        self.fio_label = QLabel()
        self.fio_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        read_only_layout.addRow(
            '<b>Фамилия:</b>', self.fio_label
            )
        self.login_label = QLabel()
        self.login_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        read_only_layout.addRow(
            '<b>Логин:</b>', self.login_label
            )
        self.phone_label = QLabel()
        self.phone_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        read_only_layout.addRow(
            '<b>Телефоны:</b>', self.phone_label
            )
        self.email_label = QLabel()
        self.email_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        read_only_layout.addRow(
            '<b>Emails:</b>', self.email_label
            )
        self.position_label = QLabel()
        self.position_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        read_only_layout.addRow(
            '<b>Должность:</b>', self.position_label
            )
        self.department_label = QLabel()
        self.department_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        read_only_layout.addRow(
            '<b>Отдел:</b>', self.department_label
            )       
        self.address_label = QLabel()
        self.address_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        read_only_layout.addRow(
            '<b>Место работы:</b>', self.address_label
            )
        self.shared_folder_label = QLabel()
        read_only_layout.addRow(
            '<b>Общие папки:</b>', self.shared_folder_label
            )       
        self.network_printer_label = QLabel()
        read_only_layout.addRow(
            '<b>Сетевой принтер:</b>', self.network_printer_label
            )
        self.comments_label = QLabel()
        self.comments_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        read_only_layout.addRow(
            '<b>Прочее:</b>', self.comments_label
            )

        table = QTableView()
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setTextElideMode(Qt.ElideNone)
        table.setAlternatingRowColors(True)
        table.setModel(self.sti)
        table.resizeColumnsToContents()
        read_only_layout.addRow(table)
        read_only_layout.addRow(buttons_layout)
        return read_only_widget

    def setLabelsText(self):
        self.fio_label.setText(
            ' '.join(
                [self.employee.surname,
                 self.employee.name,
                 self.employee.patronymic]
                )
            )
        self.login_label.setText(self.employee.unique_login)
        self.phone_label.setText(
            '; '.join([phone.number for phone in self.employee.phone])
            )
        self.email_label.setText(
            '; '.join([email.email for email in self.employee.email])
            )
        self.position_label.setText(self.employee.position.name)
        self.department_label.setText(self.employee.department.name)
        self.address_label.setText(
            "{}; {}; {}".format(
                self.employee.room.block.address.name,
                self.employee.room.block.name,
                self.employee.room.name
                )
            )
        self.shared_folder_label.setText(
            'Есть' if self.employee.shared_folder else 'Нет'
            )  
        self.network_printer_label.setText(
            'Есть' if self.employee.network_printer else 'Нет'
            )
        self.comments_label.setText(self.employee.comments)

    def get_edit_info_widget(self):
        edit_info_widget = QWidget()
        edit_info_layout = QFormLayout(edit_info_widget)
        ############################################################
        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.back)
        self.refresh_button = QPushButton('Сбросить')
        self.refresh_button.clicked.connect(self.refresh)
        self.edit_button = QPushButton('Сохранить и выйти')
        self.edit_button.clicked.connect(self.validate_input)
        ############################################################
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.back_button)
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addWidget(self.edit_button)

        self.surname_edit = QLineEdit()
        self.surname_edit.setValidator(QRegExpValidator(QRegExp("[^ ]+")))
        edit_info_layout.addRow('<b>Фамилия:<font color="red">*</font></b>', self.surname_edit)
        self.name_edit = QLineEdit()
        self.name_edit.setValidator(QRegExpValidator(QRegExp("[^ ]+")))
        edit_info_layout.addRow('<b>Имя:<font color="red">*</font></b>', self.name_edit)
        self.patronymic_edit = QLineEdit()
        self.patronymic_edit.setValidator(QRegExpValidator(QRegExp("[^ ]+")))
        edit_info_layout.addRow('<b>Отчество:</b>', self.patronymic_edit)
        self.login_edit = QLineEdit()
        self.login_edit.setValidator(QRegExpValidator(QRegExp("[^ ]+")))
        edit_info_layout.addRow('<b>Логин:<font color="red">*</font></b>', self.login_edit)
        ############################################################################################
        phones_layout = QHBoxLayout()
        self.phone1_edit = QLineEdit()
        self.phone2_edit = QLineEdit()
        self.phone3_edit = QLineEdit()
        phones_layout.addWidget(self.phone1_edit)
        phones_layout.addWidget(self.phone2_edit)
        phones_layout.addWidget(self.phone3_edit)   
        edit_info_layout.addRow('<b>Телефоны:</b>', phones_layout)
        ############################################################################################  
        emails_layout = QHBoxLayout()
        self.email1_edit = QLineEdit()
        self.email2_edit = QLineEdit()
        self.email3_edit = QLineEdit()
        emails_layout.addWidget(self.email1_edit)
        emails_layout.addWidget(self.email2_edit)
        emails_layout.addWidget(self.email3_edit)   
        edit_info_layout.addRow(
            '<b>Emails:</b>', emails_layout
            )
        ############################################################################################       
        self.position_edit = QComboBox()
        self.position_edit.setEditable(True)   
        edit_info_layout.addRow(
            '<b>Должность:</b>', self.position_edit
            )
        ############################################################################################
        self.department_edit = QComboBox()
        self.department_edit.setEditable(True)
        edit_info_layout.addRow(
            '<b>Отдел:</b>', self.department_edit
            )
        ############################################################################################
        self.address_edit = QComboBox()
        self.address_edit.currentIndexChanged[str].connect(
            self.changed_item_in_address_combobox
            )
        edit_info_layout.addRow(
            '<b>Адрес:<font color="red">*</font></b>', self.address_edit
            )
        ############################################################################################
        self.block_edit = QComboBox()
        edit_info_layout.addRow(
            '<b>Корпус:<font color="red">*</font></b>', self.block_edit
            )
        ############################################################################################
        self.room_edit = QLineEdit()
        edit_info_layout.addRow(
            '<b>Комната:<font color="red">*</font></b>', self.room_edit
            )
        ############################################################################################
        self.comments_edit = QLineEdit()
        edit_info_layout.addRow(
            '<b>Прочее:</b>', self.comments_edit
            )       
        ############################################################################################
        self.shared_folder_edit = QCheckBox()
        edit_info_layout.addRow(
            '<b>Общие папки:</b>', self.shared_folder_edit
            )
        ############################################################################################      
        self.network_printer_edit = QCheckBox()
        edit_info_layout.addRow(
            '<b>Сетевой принтер:</b>', self.network_printer_edit
            )
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setTextElideMode(Qt.ElideNone)
        self.table.setAlternatingRowColors(True)
        self.table.setModel(self.sti)
        self.table.resizeColumnsToContents()
        edit_info_layout.addRow(self.table)

        table_buttons_layout = QHBoxLayout()
        add_table_row_button = QPushButton('Добавить компьютер')
        add_table_row_button.setFixedSize(add_table_row_button.sizeHint())
        add_table_row_button.clicked.connect(self.add_table_row)
        delete_table_row_button = QPushButton('Открепить компьютер')
        delete_table_row_button.setFixedSize(delete_table_row_button.sizeHint())
        delete_table_row_button.clicked.connect(self.delete_table_row)
        table_buttons_layout.addWidget(delete_table_row_button)
        table_buttons_layout.addWidget(add_table_row_button)
        table_buttons_layout.addStretch()

        edit_info_layout.addRow(table_buttons_layout)
        edit_info_layout.addRow(buttons_layout)
        return edit_info_widget

    def setLineEdits(self):
        self.surname_edit.setText(self.employee.surname)
        self.name_edit.setText(self.employee.name)
        self.patronymic_edit.setText(self.employee.patronymic)
        self.login_edit.setText(self.employee.unique_login)

        try:
            self.phone1_edit.setText(self.employee.phone[0].number)
        except IndexError:
            pass
        try:
            self.phone2_edit.setText(self.employee.phone[1].number)
        except IndexError:
            pass
        try:
            self.phone3_edit.setText(self.employee.phone[2].number)
        except IndexError:
            pass

        try:
            self.email1_edit.setText(self.employee.email[0].email)
        except IndexError:
            pass
        try:
            self.email2_edit.setText(self.employee.email[1].email)
        except IndexError:
            pass
        try:
            self.email3_edit.setText(self.employee.email[2].email)
        except IndexError:
            pass

        self.position_edit.addItems(
            self.session.query(data.Position.name).values()
            )
        self.position_edit.setCurrentText(self.employee.position.name)

        self.department_edit.addItems(
            self.session.query(data.Department.name).values()
            )
        self.department_edit.setCurrentText(self.employee.department.name)

        self.address_edit.addItems(
            self.session.query(data.Address.name).values()
            )
        index = self.address_edit.findText(self.employee.room.block.address.name, Qt.MatchFixedString)
        if index >= 0:
            self.address_edit.setCurrentIndex(index)

        self.block_edit.addItems(
            self.session.query(data.Block.name).\
                join(data.Address).\
                filter(data.Address.name==self.address_edit.currentText()).\
                values()
            )
        index = self.block_edit.findText(self.employee.room.block.name, Qt.MatchFixedString)
        if index >= 0:
            self.block_edit.setCurrentIndex(index)

        self.room_edit.setText(self.employee.room.name)
        self.comments_edit.setText(self.employee.comments)
        if self.employee.shared_folder:
            self.shared_folder_edit.setChecked(True)
        if self.employee.network_printer:
            self.network_printer_edit.setChecked(True)

    @QtCore.pyqtSlot()  
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

    @QtCore.pyqtSlot()  
    def edit_employee_info(self):
        self.layout().setCurrentIndex(1)
        self.setFixedSize(800, 600)

    @QtCore.pyqtSlot()  
    def back(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Уведомление')
        msg_box.setText('Данные не сохранятся')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = msg_box.button(QMessageBox.Yes)
        buttonY.setText('Ок')
        buttonN = msg_box.button(QMessageBox.No)
        buttonN.setText('Отменить')
        msg_box.exec_()

        if msg_box.clickedButton() == buttonY:
            self.session.rollback()
            self.sti.clear()
            self.fill_table_model()
            self.setLabelsText()
            self.setLineEdits()
            self.layout().setCurrentIndex(0)
            self.setFixedSize(800, 450)

    @QtCore.pyqtSlot(data.Pc) 
    def new_row(self, pc):
        self.sti.appendRow([
                QStandardItem(QIcon(r'pics\pc.png'),pc.pcname.domain.name),
                QStandardItem(pc.pcname.name),
                QStandardItem(pc.mac_address),
                QStandardItem(pc.powersocket.name),
                QStandardItem(pc.connectiontype.name),
                QStandardItem(pc.app_server),
                QStandardItem(pc.windows.name),
                QStandardItem(pc.windows_os_key),
                QStandardItem(pc.office.name),
                QStandardItem(pc.ms_office_key),
                QStandardItem(pc.antivirus.name),
                QStandardItem(pc.mail_client),
                QStandardItem(pc.comments),
                QStandardItem('Есть' if pc.kes else 'Нет'),
                QStandardItem('Есть' if pc.consultant else 'Нет'),
                QStandardItem('Есть' if pc.guarantee else 'Нет'),
                QStandardItem('Есть' if pc.odin_s else 'Нет'),
                QStandardItem('Есть' if pc.kdc else 'Нет')
                ])

    @QtCore.pyqtSlot()
    def delete_table_row(self):
        index = self.table.selectionModel().selectedRows()
        try:
            element = self.sti.takeRow(index[0].row())
        except IndexError:
            QMessageBox.warning(
                    self, 'Ошибка',
                    'Выделите строку в таблице'
                    )
            return
        pc = self.session.query(data.Pc).\
            with_parent(self.employee).\
            filter(data.Pc.mac_address==element[2].text()).\
            one()
        self.employee.pc.remove(pc)

    @QtCore.pyqtSlot()
    def add_table_row(self):
        add_pcs = PCAdd(self.session, self.employee.pc)
        if add_pcs.exec_() == QDialog.Accepted:
            for pc in add_pcs.added_pcs:
                self.new_row(pc)
                self.employee.pc.append(pc)

    @QtCore.pyqtSlot()
    def refresh(self):
        self.session.rollback()
        self.setLineEdits()
        self.sti.clear()
        self.fill_table_model()

    @QtCore.pyqtSlot()        
    def validate_input(self):
        if not self.surname_edit.text()\
           or not self.name_edit.text()\
           or not self.room_edit.text()\
           or not self.login_edit.text():
            QMessageBox.warning(
                self,'Предупреждение',
                "Поля: 'Фамилия', 'Имя', 'Логин', 'Комната'" +
                " -- обязательныe"
                )
            return

        phones = [self.phone1_edit.text(), self.phone2_edit.text(), self.phone3_edit.text()]
        phones[:] = [phone for phone in phones if phone]
        if len(set(phones)) < len(phones) and len(phones) > 0:
            QMessageBox.warning(
                    self, 'Предупреждение', 'Телефоны совпадают'
                    )
            return

        emails = [self.email1_edit.text(), self.email2_edit.text(), self.email3_edit.text()]
        emails[:] = [email for email in emails if email]
        if len(set(emails)) < len(emails) and len(emails) > 0:
            QMessageBox.warning(
                    self, 'Предупреждение', 'Email совпадают'
                    )
            return

        for phone in [self.phone1_edit, self.phone2_edit, self.phone3_edit]:
            stmt = self.session.query(data.Phone).\
                join(data.Employee).\
                filter(data.Employee.name!=self.employee.name).\
                filter(data.Phone.number==phone.text())

            if self.session.query(stmt.exists()).scalar():
                QMessageBox.warning(
                    self, 'Предупреждение', 'Введенный телефон уже есть в базе'
                    )
                return

        for email in [self.email1_edit, self.email2_edit, self.email3_edit]:
            stmt = self.session.query(data.Email).\
                join(data.Employee).\
                filter(data.Employee.name!=self.employee.name).\
                filter(data.Email.email==email.text())

            if self.session.query(stmt.exists()).scalar():
                QMessageBox.warning(
                    self, 'Предупреждение', 'Введенный email уже есть в базе'
                    )
                return
        
        stmt = self.session.query(data.Employee).\
            filter(data.Employee.unique_login==self.login_edit.text()).\
            filter(data.Employee.unique_login!=self.employee.unique_login)
        if self.session.query(stmt.exists()).scalar():
            QMessageBox.warning(
                self, 'Предупреждение', 'Введенный логин уже есть в базе'
                )
            return

        if self.employee.surname != self.surname_edit.text():
            self.employee.surname = self.surname_edit.text()
        if self.employee.name != self.name_edit.text():
            self.employee.name = self.name_edit.text()
        if self.employee.patronymic != self.patronymic_edit.text():
            self.employee.patronymic = self.patronymic_edit.text()
        if self.employee.unique_login != self.login_edit.text():
            self.employee.unique_login = self.login_edit.text()
        
        for phone in self.employee.phone:
            if phone.number not in phones:
                self.session.delete(phone)
            else:
                phones.remove(phone.number)
        self.employee.phone.extend([data.Phone(number=phone) for phone in phones])

        for email in self.employee.email:
            if email.email not in emails:
                self.session.delete(email)
            else:
                emails.remove(email.email)
        self.employee.email.extend([data.Email(email=email) for email in emails])

        if self.employee.position.name != self.position_edit.currentText():
            self.employee.position = (
            get_or_create(
                self.session, data.Position,
                name=self.position_edit.currentText()
                )
            )
            
        if self.employee.department.name != self.department_edit.currentText():
            self.employee.department = (
                get_or_create(
                    self.session, data.Department, 
                    name=self.department_edit.currentText()
                    )
                )

        block = self.session.query(data.Block).\
                    join(data.Address).\
                    filter(data.Block.name==self.block_edit.currentText()).\
                    filter(data.Address.name==self.address_edit.currentText()).\
                    one()
        room = self.session.query(data.Room).\
                    join(data.Block).\
                    filter(data.Room.name==self.room_edit.text()).\
                    first()
        if not room:
            room = data.Room(name=self.room_edit.text())
            room.block = block
            self.employee.room = room
        elif self.employee.room != room:
            self.employee.room = room
        else:
            pass
        if self.employee.comments != self.comments_edit.text():
            self.employee.comments = self.comments_edit.text()
        if self.employee.shared_folder != self.shared_folder_edit.isChecked():
            self.employee.shared_folder = self.shared_folder_edit.isChecked()
        if self.employee.network_printer != self.network_printer_edit.isChecked():
            self.employee.network_printer = self.network_printer_edit.isChecked()

        if not self.accept():
            self.session.rollback()
            self.sti.clear()
            self.fill_table_model()

    @QtCore.pyqtSlot(str)
    def changed_item_in_address_combobox(self, index):
        self.block_edit.clear()
        items = self.session.query(data.Block.name).\
            join(data.Address).\
            filter(data.Address.name==index).\
            values()
        self.block_edit.addItems(items)

    def closeEvent(self, evnt):
        if self.layout().currentIndex() == 0:
            QDialog.closeEvent(self, evnt)
        else:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle('Уведомление')
            msg_box.setText('Данные не сохранятся')
            msg_box.setStandardButtons(
                QMessageBox.Yes | QMessageBox.Cancel
            )
            buttonY = msg_box.button(QMessageBox.Yes)
            buttonY.setText('Выйти')
            buttonN = msg_box.button(QMessageBox.Cancel)
            buttonN.setText('Отмена')
            msg_box.exec_()

            if msg_box.clickedButton() == buttonY:
                QDialog.closeEvent(self, evnt)
            elif msg_box.clickedButton() == buttonN:
                evnt.ignore()
