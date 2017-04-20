#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import psycopg2
from app import data
from app.functions import get_or_create
from app.dialogs.exitmethods import Dialog
from sqlalchemy.sql.operators import exists
from PyQt5.QtWidgets import (QWidget, QMessageBox, QPushButton,
                             QToolTip, QDialog, QLineEdit, QCheckBox,
                             QComboBox, QFormLayout, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.Qt import QRegExpValidator, QRegExp



class RegisterPC(Dialog):
    def __init__(self, session):
        QDialog.__init__(self)       
        self.session = session
        self.init_ui()
        self.show()
        
    def init_ui(self):
        QToolTip.setFont(QFont('Font', 15))
        self.setFixedSize(700, 480)
        self.setWindowModality(2)
        self.setWindowTitle('Регистрируем компьютер')
        self.setWindowIcon(QIcon(r'pics\pc.png'))

        buttons_layout = QHBoxLayout()

        back_button = QPushButton('Назад')
        back_button.setToolTip('Возвращаемся назад')
        back_button.clicked.connect(self.close)
        submit_button = QPushButton('Внести в базу данных')
        submit_button.setToolTip('Зарегистрировать <b>работягу</b>?')
        submit_button.clicked.connect(self.validate_input)
        buttons_layout.addWidget(back_button, alignment = Qt.AlignRight)
        buttons_layout.addWidget(submit_button)

        form_layout = QFormLayout(self)

        self.pc_name_edit = QLineEdit()
        self.pc_name_edit.setValidator(QRegExpValidator(QRegExp("[^А-ЯA-Z ]+")))
        self.pc_name_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Имя компьютера:<font color="red">*</font>', self.pc_name_edit
            )

        self.mac_edit = QLineEdit()
        self.mac_edit.setValidator(QRegExpValidator(QRegExp("[A-F-0-9]+")))
        self.mac_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'MAC-адрес:<font color="red">*</font>', self.mac_edit
            )

        self.power_socket_edit = QComboBox()
        self.power_socket_edit.setEditable(True)
        self.session.query(data.PowerSocket.name).values()
        self.power_socket_edit.addItems(
            self.session.query(data.PowerSocket.name).values()
            )
        self.power_socket_edit.setCurrentText('')
        form_layout.addRow('Номер розетки:', self.power_socket_edit)

        self.connection_type_edit = QComboBox()
        self.connection_type_edit.setEditable(True)
        self.connection_type_edit.setValidator(QRegExpValidator(QRegExp("[^А-ЯA-Z]+")))    
        self.connection_type_edit.addItems(
            self.session.query(data.ConnectionType.name).values()
            )
        self.connection_type_edit.setCurrentText('')
        form_layout.addRow('Как подлючен:', self.connection_type_edit)

        self.domain_edit = QComboBox()
        self.domain_edit.setEditable(True)
        self.domain_edit.addItems(
            self.session.query(data.Domain.name).values()
            )
        self.domain_edit.setCurrentText('')
        form_layout.addRow('Домен:', self.domain_edit)

        self.app_server_edit = QLineEdit()
        self.app_server_edit.setClearButtonEnabled(True)
        form_layout.addRow('Серверные приложения:', self.app_server_edit)

        self.windows_os_edit = QComboBox()
        self.windows_os_edit.setEditable(True)
        self.windows_os_edit.setValidator(QRegExpValidator(QRegExp("[^A-Z]+")))
        self.windows_os_edit.addItems(
            self.session.query(data.Windows.name).values()
            )
        self.windows_os_edit.setCurrentText('')
        form_layout.addRow('Windows OS:', self.windows_os_edit)

        self.ms_office_edit = QComboBox()
        self.ms_office_edit.setEditable(True)
        self.ms_office_edit.setValidator(QRegExpValidator(QRegExp("[^A-Z]+")))       
        self.ms_office_edit.addItems(
            self.session.query(data.Office.name).values()
            )
        self.ms_office_edit.setCurrentText('')
        form_layout.addRow('Microsoft Office:', self.ms_office_edit)

        self.antivirus_edit = QComboBox()
        self.antivirus_edit.setEditable(True)
        self.antivirus_edit.setValidator(QRegExpValidator(QRegExp("[^A-Z]+")))   
        self.antivirus_edit.addItems(
            self.session.query(data.Antivirus.name).values()
            )
        self.antivirus_edit.setCurrentText('')
        form_layout.addRow('Антивирус:', self.antivirus_edit)

        self.windows_os_key_edit = QLineEdit()
        self.windows_os_key_edit.setClearButtonEnabled(True)
        form_layout.addRow('Windows OS key:', self.windows_os_key_edit)

        self.ms_office_key_edit = QLineEdit()
        self.ms_office_key_edit.setClearButtonEnabled(True)
        form_layout.addRow('Microsoft Office key:', self.ms_office_key_edit)

        self.mail_client_edit = QLineEdit()
        self.mail_client_edit.setClearButtonEnabled(True)
        form_layout.addRow('Клиент электронной почты:', self.mail_client_edit)

        self.comments_edit = QLineEdit()
        self.comments_edit.setClearButtonEnabled(True)
        form_layout.addRow('Прочее:', self.comments_edit)

        self.kes_edit = QCheckBox()
        form_layout.addRow('Агент KES:', self.kes_edit)

        self.consultant_edit = QCheckBox()
        form_layout.addRow('Консультант:', self.consultant_edit)

        self.guarantee_edit = QCheckBox()
        form_layout.addRow('Гарант:', self.guarantee_edit)

        self.odin_s_edit = QCheckBox()
        form_layout.addRow('1С:', self.odin_s_edit)

        self.kdc_edit = QCheckBox()
        form_layout.addRow('КДС:', self.kdc_edit)

        form_layout.addRow(buttons_layout)

    @QtCore.pyqtSlot()
    def validate_input(self):
        if not self.mac_edit.text() or not self.pc_name_edit.text():
            QMessageBox.warning(
                self,'Предупреждение',
                "Поля: 'Имя компьютера' и 'MAC-адрес' -- обязательные"
                )
            return

        stmt = self.session.query(data.PcName).join(data.Domain).\
            filter(data.PcName.name==self.pc_name_edit.text()).\
            filter(data.Domain.name==self.domain_edit.currentText())
        if self.session.query(stmt.exists()).scalar():
            QMessageBox.warning(self,
                'Предупреждение', 
                'Введенное имя компьютера уже существует в базе'
                )
            return

        stmt = self.session.query(data.Pc).\
            filter(data.Pc.mac_address==self.mac_edit.text())
        if self.session.query(stmt.exists()).scalar():
            QMessageBox.warning(
                self, 'Предупреждение', 'Введенный мак-адрес уже существует'
                )
            return

        self.process_data()
        if not self.accept():
            self.session.rollback()

    def process_data(self):
        pcname = data.PcName(
            name = self.pc_name_edit.text()
        )

        pcname.domain = get_or_create(
            self.session, data.Domain, 
            name=self.domain_edit.currentText()
        )

        pc = data.Pc(
            mac_address     = self.mac_edit.text(),
            windows_os_key  = self.windows_os_key_edit.text(),
            ms_office_key   = self.ms_office_key_edit.text(),
            kes             = self.kes_edit.isChecked(),
            guarantee       = self.guarantee_edit.isChecked(),
            odin_s          = self.odin_s_edit.isChecked(),
            kdc             = self.kdc_edit.isChecked(),
            mail_client     = self.mail_client_edit.text(),
            app_server      = self.app_server_edit.text(),
            consultant      = self.consultant_edit.isChecked(),
            comments        = self.comments_edit.text(),
        )
        pc.pcname = pcname
        pc.connectiontype = get_or_create(
            self.session, data.ConnectionType,             
            name=self.connection_type_edit.currentText()
        )
        pc.powersocket = get_or_create(
            self.session, data.PowerSocket, 
            name=self.power_socket_edit.currentText()
        )
        pc.windows = get_or_create(
            self.session, data.Windows, 
            name=self.windows_os_edit.currentText()
        )
        pc.office = get_or_create(
            self.session, data.Office, 
            name=self.ms_office_edit.currentText()
        )
        pc.antivirus = get_or_create(
            self.session, data.Antivirus, 
            name=self.antivirus_edit.currentText()
        )
