#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import data
import psycopg2
from functools import partial
from sqlalchemy.sql import exists
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QMessageBox, QPushButton,
                             QToolTip, QDialog, QLineEdit, QCheckBox, QComboBox,
                             QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QListView, QInputDialog, QAbstractButton, QListWidget)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtCore import Qt, QSize

class ConfigureAdresses(QDialog):
    def __init__(self, session):
        QDialog.__init__(self)       
        self.session = session
        self.init_ui()
        self.show()

    def init_ui(self):
        QToolTip.setFont(QFont('Font', 15))
        self.resize(500, 500)
        self.setWindowModality(2)
        self.setWindowTitle('Адреса')
        self.setWindowIcon(QIcon(r'pics\home.png'))

        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.address_layout())
        self.layout.addLayout(self.address_buttons_layout())

    def address_layout(self):
        layout = QFormLayout()
        for address in self.session.query(data.Address):
            open_address_button = QPushButton(address.name)
            open_address_button.setFixedSize(300, 80)
            open_address_button.clicked.connect(partial(self.open_address, address=address))
            delete_button = QPushButton("Удалить")
            delete_button.adjustSize()
            delete_button.setFixedSize(70, 25)
            delete_button.clicked.connect(partial(self.delete_address, address=address))
            layout.addRow(open_address_button, delete_button)
        return layout

    def address_buttons_layout(self):
        layout = QHBoxLayout()
        new_address_input = QPushButton("Добавить новый адрес")
        new_address_input.clicked.connect(self.add_address)
        ok_button = QPushButton("Сохранить и выйти")
        ok_button.clicked.connect(self.accept)
        layout.addStretch()
        layout.addWidget(new_address_input)
        layout.addWidget(ok_button)
        return layout
      
    @QtCore.pyqtSlot()
    def add_address(self):
        text, ok = QInputDialog.getText(self, 'Добавление нового адреса', 'Адрес:')
        if ok:
            if self.session.query(data.Address).filter_by(name=str(text)).first():
                QMessageBox.warning(self,'Предупреждение','Введенный адрес уже существует в базе')
            else:
                self.session.add(data.Address(name=str(text)))
                ConfigureAdresses.clear_layout(self.layout.takeAt(0).layout())
                self.layout.insertLayout(0, self.address_layout())

    @QtCore.pyqtSlot()
    def delete_address(self, address):
        reply = QMessageBox.question(self, 'Уведомление',
            "Удалить адрес {}?".format(address.name),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.session.delete(address)
            ConfigureAdresses.clear_layout(self.layout.takeAt(0).layout())
            self.layout.insertLayout(0, self.address_layout())

    @QtCore.pyqtSlot()
    def open_address(self, address):
        ConfigureAdresses.clear_layout(self.layout)

        obj = Address(address)

    def clear_layout(layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                else:
                    ConfigureAdresses.clear_layout(item.layout())

    def closeEvent(self, evnt):
        reply = QMessageBox.question(self, 'Уведомление',
            "Данные не сохранятся, точно выйти?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QDialog.closeEvent(self, evnt)
        else:
            evnt.ignore()

    def accept(self):
        reply = QMessageBox.question(self, 'Уведомление',
            "Подтвердить ввод данных?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QDialog.accept(self)


class Address:
    def __init__(self, address, session):
        self.address = address
        self.session = session

    def blocks_layout(self, address):
        layout = QFormLayout()
        list = QListWidget()

        for block.name in self.session.query(data.Block).join(data.Address).filter(data.Address==address):
            list.addItem(block.name)

    def blocks_buttons_layout(self):
        layout = QHBoxLayout()
        back_button = QPushButton("Вернуться")
        new_blocks_input.clicked.connect()
        new_blocks_input = QPushButton("Добавить новый корпус")
        new_blocks_input.clicked.connect()
        ok_button = QPushButton("Сохранить и выйти")
        ok_button.clicked.connect(self.accept)
        layout.addStretch()
        layout.addWidget(back_button)
        layout.addWidget(new_blocks_input)
        layout.addWidget(ok_button)
        return layout

    @QtCore.pyqtSlot()
    def add_block(self, address):
        text, ok = QInputDialog.getText(self, 'Добавление нового корпуса', 'Корпус:')
        if ok:
            if self.session.query(data.Block).join(data.Address).\
                filter(data.Address.name==address).\
                filter(data.Block.name==str(text)).first():
                QMessageBox.warning(self,'Предупреждение', 'Введенный корпус уже существует в базе')
            else:
                instance = session.query(data.Address).filter_by(name=addres).first()
                new_block = data.Block(name=str(text))
                self.session.add(new_block)

    @QtCore.pyqtSlot()
    def delete_block(self, address):
        pass



