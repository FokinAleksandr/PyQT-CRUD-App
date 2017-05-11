#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Редактирование информации о компьютерах
"""
from app.tools.exitmethods import Dialog
from app.db import data
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *


class EditPc(Dialog):
    def __init__(self, session, pc):
        QDialog.__init__(self)
        self.session = session
        self.pc = pc
        self.init_window()
        self.build()
        self.fill()

    def init_window(self):
        self.setFixedSize(700, 480)
        self.setWindowModality(2)
        self.setWindowTitle(
            '{}/{}'.format(
                self.pc.pcname.domain.name,
                self.pc.pcname.name
            )
        )
        self.setWindowIcon(QIcon(r'pics\pc.png'))

    def build(self):
        QVBoxLayout(self)

        form_layout = QFormLayout()
        self.pc_name_edit = QLineEdit()
        self.pc_name_edit.setValidator(
            QRegExpValidator(QRegExp("[^А-ЯA-Z ]+"))
        )
        self.pc_name_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Имя компьютера:<font color="red">*</font>', self.pc_name_edit
        )
        self.mac_edit = QLineEdit()
        self.mac_edit.setValidator(
            QRegExpValidator(QRegExp("[A-F-0-9]+"))
        )
        self.mac_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'MAC-адрес:<font color="red">*</font>', self.mac_edit
        )
        self.power_socket_edit = QComboBox()
        self.power_socket_edit.setEditable(True)
        self.power_socket_edit.addItems([
            pow_socket
            for pow_socket, in self.session.query(data.PowerSocket.name)
            if pow_socket
        ])
        form_layout.addRow(
            'Номер розетки:', self.power_socket_edit
        )
        self.connection_type_edit = QComboBox()
        self.connection_type_edit.setEditable(True)
        self.connection_type_edit.setValidator(
            QRegExpValidator(QRegExp("[^А-ЯA-Z]+"))
        )
        self.connection_type_edit.addItems([
            conn_type
            for conn_type, in self.session.query(data.ConnectionType.name)
            if conn_type
        ])
        form_layout.addRow(
            'Как подлючен:', self.connection_type_edit
        )
        self.domain_edit = QComboBox()
        self.domain_edit.setEditable(True)
        self.domain_edit.addItems([
            domain
            for domain, in self.session.query(data.Domain.name)
            if domain
        ])
        form_layout.addRow(
            'Домен:', self.domain_edit
        )
        self.app_server_edit = QLineEdit()
        self.app_server_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Серверные приложения:', self.app_server_edit
        )
        self.windows_os_edit = QComboBox()
        self.windows_os_edit.setEditable(True)
        self.windows_os_edit.setValidator(
            QRegExpValidator(QRegExp("[^A-Z]+"))
        )
        self.windows_os_edit.addItems([
            windows
            for windows, in self.session.query(data.Windows.name)
            if windows
        ])
        form_layout.addRow(
            'Windows OS:', self.windows_os_edit
        )
        self.ms_office_edit = QComboBox()
        self.ms_office_edit.setEditable(True)
        self.ms_office_edit.setValidator(
            QRegExpValidator(QRegExp("[^A-Z]+"))
        )
        self.ms_office_edit.addItems([
            office
            for office, in self.session.query(data.Office.name)
            if office
        ])
        form_layout.addRow(
            'Microsoft Office:', self.ms_office_edit
        )
        self.antivirus_edit = QComboBox()
        self.antivirus_edit.setEditable(True)
        self.antivirus_edit.setValidator(
            QRegExpValidator(QRegExp("[^A-Z]+"))
        )
        self.antivirus_edit.addItems([
            antivirus
            for antivirus, in self.session.query(data.Antivirus.name)
            if antivirus
        ])
        form_layout.addRow(
            'Антивирус:', self.antivirus_edit
        )
        self.windows_os_key_edit = QLineEdit()
        self.windows_os_key_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Windows OS key:', self.windows_os_key_edit
        )
        self.ms_office_key_edit = QLineEdit()
        self.ms_office_key_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Microsoft Office key:', self.ms_office_key_edit
        )
        self.mail_client_edit = QLineEdit()
        self.mail_client_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Клиент электронной почты:', self.mail_client_edit
        )
        self.comments_edit = QLineEdit()
        self.comments_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Прочее:', self.comments_edit
        )
        self.kes_edit = QCheckBox()
        form_layout.addRow(
            'Агент KES:', self.kes_edit
        )
        self.consultant_edit = QCheckBox()
        form_layout.addRow(
            'Консультант:', self.consultant_edit
        )
        self.guarantee_edit = QCheckBox()
        form_layout.addRow(
            'Гарант:', self.guarantee_edit
        )
        self.odin_s_edit = QCheckBox()
        form_layout.addRow(
            '1С:', self.odin_s_edit
        )
        self.kdc_edit = QCheckBox()
        form_layout.addRow(
            'КДС:', self.kdc_edit
        )

        buttons_layout = QHBoxLayout()
        refresh_button = QPushButton('Сбросить')
        refresh_button.clicked.connect(self.fill)
        buttons_layout.addWidget(refresh_button)
        exit_button = QPushButton('Выйти')
        exit_button.clicked.connect(self.reject)
        buttons_layout.addWidget(exit_button)
        accept_button = QPushButton('Сохранить')
        accept_button.clicked.connect(self.accept)
        buttons_layout.addWidget(accept_button)

        self.layout().addLayout(form_layout)
        self.layout().addLayout(buttons_layout)

    def fill(self):
        self.pc_name_edit.setText(self.pc.pcname.name)
        self.mac_edit.setText(self.pc.mac_address)
        self.power_socket_edit.setCurrentText(self.pc.powersocket.name)
        self.connection_type_edit.setCurrentText(self.pc.connectiontype.name)
        self.domain_edit.setCurrentText(self.pc.pcname.domain.name)
        self.app_server_edit.setText(self.pc.app_server)
        self.windows_os_edit.setCurrentText(self.pc.windows.name)
        self.ms_office_edit.setCurrentText(self.pc.office.name)
        self.antivirus_edit.setCurrentText(self.pc.antivirus.name)
        self.windows_os_key_edit.setText(self.pc.windows_os_key)
        self.ms_office_key_edit.setText(self.pc.ms_office_key)
        self.mail_client_edit.setText(self.pc.mail_client)
        self.comments_edit.setText(self.pc.comments)
        if self.pc.kes:
            self.kes_edit.setChecked(True)
        if self.pc.consultant:
            self.consultant_edit.setChecked(True)
        if self.pc.guarantee:
            self.guarantee_edit.setChecked(True)
        if self.pc.odin_s:
            self.odin_s_edit.setChecked(True)
        if self.pc.kdc:
            self.kdc_edit.setChecked(True)
