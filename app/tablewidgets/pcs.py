#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Вкладка компьютеров
"""
from app.db import data
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *


class PcsTable(QWidget):
    def __init__(self, session, parent):
        QDialog.__init__(self)
        self.session = session
        self.parent = parent
        self.build_layout()

    def build_layout(self):
        QVBoxLayout(self)

        self.model = QStandardItemModel()
        self.update_table_content()

        self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterKeyColumn(0)

        self.search_filter = QLineEdit()
        self.search_filter.setFixedWidth(500)
        self.search_filter.setClearButtonEnabled(True)
        self.search_filter.setPlaceholderText('Поиск по домену/имени компьютера')
        self.search_filter.textChanged.connect(self.filter_proxy_model.setFilterRegExp)

        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setTextElideMode(Qt.ElideNone)
        self.table.setAlternatingRowColors(True)
        self.table.setModel(self.filter_proxy_model)
        self.table.resizeColumnsToContents()

        self.layout().addWidget(self.search_filter)
        self.layout().addWidget(self.table)

    def update_table_content(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            ['Домен/Имя компьютера', 'ФИО пользователя', 'MAC-адрес', 'Номер розетки',
             'Как подключен', 'Серверные приложения',
             'Windows OS', 'Windows OS key', 'Microsoft Office',
             'Microsoft Office key', 'Антивирус', 'Клиент электронной почты',
             'Прочее', 'Агент KES', 'Консультант', 'Гарант', '1C', 'КДС']
        )
        for pc in self.session.query(data.Pc):
            self.model.appendRow([
                QStandardItem(QIcon(r'pics\pc.png'), pc.pcname.domain.name + '/' + pc.pcname.name),
                QStandardItem(QIcon(r'pics\employee.png'), ';\n'.join([emp.fullname for emp in pc.employee])),
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
        try:
            self.table.resizeColumnsToContents()
        except Exception:
            pass