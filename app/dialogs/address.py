#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import psycopg2
from app.dialogs.exitmethods import Dialog
from app import data
from functools import partial
from sqlalchemy.orm import exc
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QMessageBox, QPushButton,
                             QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QInputDialog, QListWidget,
                             QListWidgetItem)

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.Qt import QPixmap

class ConfigureAddresses(Dialog):
    def __init__(self, session):
        QDialog.__init__(self)       
        self.session = session
        self.init_ui()
        self.show()

    def init_ui(self):
        self.resize(900, 800)
        self.setWindowModality(2)
        self.setWindowTitle('Адреса')
        self.setWindowIcon(QIcon(r'pics\home.png'))

        self.addresses_list = QListWidget()        
        self.blocks_list = QListWidget()
        self.blocks_list.itemDoubleClicked[QListWidgetItem].connect(
            self.edit_block_via_double_click
            )
        self.addresses_list.itemClicked.connect(self.fill_blocks)
        self.addresses_list.itemDoubleClicked[QListWidgetItem].connect(
            self.edit_address_via_double_click
            )

        QVBoxLayout(self)
        lists_layout = QHBoxLayout()
        lists_layout.addWidget(self.addresses_list)
        lists_layout.addWidget(self.blocks_list)
        self.layout().addLayout(lists_layout)

        accept_data_button = QPushButton("Сохранить и выйти")
        accept_data_button.clicked.connect(self.accept)
        accept_data_button.setFixedSize(accept_data_button.sizeHint())
        self.layout().addWidget(
            accept_data_button, alignment=(Qt.AlignRight | Qt.AlignVCenter)
            )

        self.fill_addresses()

    def fill_addresses(self):
        self.addresses_list.clear()
        for address in self.session.query(data.Address).\
                            order_by(data.Address.name).\
                            all():
            address_widget = AddressWidget(address)
            address_widget.delete_button.clicked.connect(
                partial(self.delete_address, address=address)
                )
            address_widget.view_button.clicked.connect(
                partial(self.edit_address, address=address)
                )
            address_item = QListWidgetItem()
            address_item.setSizeHint(QSize(250, 75))
            self.addresses_list.addItem(address_item)
            self.addresses_list.setItemWidget(address_item, address_widget)    
        add_item = QListWidgetItem()
        add_button = QPushButton("Добавить адрес")
        add_button.clicked.connect(self.add_address)
        add_item.setSizeHint(QSize(250, 75))
        self.addresses_list.addItem(add_item)
        self.addresses_list.setItemWidget(add_item, add_button)

    @QtCore.pyqtSlot()
    def add_address(self):
        text, ok = QInputDialog.getText(
            self, 'Добавление нового адреса', 'Адрес:'
            )
        if ok:
            if not text:
                QMessageBox.warning(
                    self, 'Предупреждение', 'Поле не может быть пустым!'
                    )
                return
            try:
                self.session.query(data.Address).\
                filter_by(name=str(text)).one()
            except exc.NoResultFound:
                new_address = data.Address(name=str(text))
                self.session.add(new_address)
                self.fill_addresses()
            else:
                QMessageBox.warning(
                    self, 'Предупреждение', 'Адрес уже существует!'
                    )

    @QtCore.pyqtSlot(QListWidgetItem)
    def edit_address_via_double_click(self, item):
        address_widget = self.addresses_list.itemWidget(item)
        self.edit_address(address_widget.address)

    @QtCore.pyqtSlot(data.Address)
    def edit_address(self, address):
        text, ok = QInputDialog.getText(
            self, 'Изменение адреса', 'Новое название:'
            )
        if ok:
            if not text:
                QMessageBox.warning(
                    self, 'Предупреждение', 'Поле не может быть пустым!'
                    )
                return
            try:
                self.session.query(data.Address).\
                filter_by(name=str(text)).one()
            except exc.NoResultFound:
                address.name = str(text)
                self.fill_addresses()
            else:
                QMessageBox.warning(
                    self, 'Предупреждение', 'Адрес уже существует!'
                    )

    @QtCore.pyqtSlot(data.Address)
    def delete_address(self, address):
        reply = QMessageBox.question(self, 'Уведомление',
            "Удалить адрес {}?".format(address.name),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.session.delete(address)
            self.fill_addresses()

    @QtCore.pyqtSlot()
    def fill_blocks(self):
        self.blocks_list.clear()
        address_widget = self.addresses_list.itemWidget(self.addresses_list.currentItem())
        for block in self.session.query(data.Block).\
                with_parent(address_widget.address).\
                order_by(data.Block.name).\
                all():
            block_item = QListWidgetItem() 
            block_widget = BlockWidget(block)
            block_widget.delete_button.clicked.connect(
                partial(self.delete_block, block=block)
                )
            block_widget.view_button.clicked.connect(
                partial(self.edit_block, block=block)
                )
            block_item.setSizeHint(QSize(250, 75))
            self.blocks_list.addItem(block_item)
            self.blocks_list.setItemWidget(block_item, block_widget)
            
        add_item = QListWidgetItem()
        add_button = QPushButton("Добавить корпус")
        add_button.clicked.connect(
            partial(self.add_block, address=address_widget.address)
            )
        add_item.setSizeHint(QSize(250, 75))
        self.blocks_list.addItem(add_item)
        self.blocks_list.setItemWidget(add_item, add_button)

    @QtCore.pyqtSlot(data.Address)
    def add_block(self, address):
        text, ok = QInputDialog.getText(
            self, 'Добавление нового корпуса', 'Корпус:'
            )
        if ok:
            if not text:
                QMessageBox.warning(
                    self, 'Предупреждение', 'Поле не может быть пустым!'
                    )
                return
            try:
                self.session.query(data.Block).\
                    with_parent(address).\
                    filter_by(name=str(text)).one()
            except exc.NoResultFound:
                new_block = data.Block(name=str(text))
                address.block.append(new_block)
                self.session.add(new_block)
                self.fill_blocks()
            else:
                QMessageBox.warning(
                    self, 'Предупреждение', 'Корпус уже существует!'
                    )

    @QtCore.pyqtSlot(QListWidgetItem)
    def edit_block_via_double_click(self, item):
        block_widget = self.blocks_list.itemWidget(item)
        self.edit_block(block_widget.block)

    @QtCore.pyqtSlot(data.Block)
    def edit_block(self, block):
        text, ok = QInputDialog.getText(
            self, 'Изменение корпуса', 'Новое название:'
            )
        if ok:
            if not text:
                QMessageBox.warning(
                    self, 'Предупреждение', 'Поле не может быть пустым!'
                    )
                return
            try:
                self.session.query(data.Block).\
                    with_parent(block.address).\
                    filter_by(name=str(text)).one()
            except exc.NoResultFound:
                block.name = str(text)
                self.fill_blocks()
            else:
                QMessageBox.warning(
                    self, 'Предупреждение', 'Корпус уже существует!'
                    )

    @QtCore.pyqtSlot(data.Block)
    def delete_block(self, block):
        reply = QMessageBox.question(self, 'Уведомление',
            "Удалить корпус {}?".format(block.name),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.session.delete(block)
            self.fill_blocks()
    

class AddressWidget(QWidget):
    def __init__(self, address):
        QWidget.__init__(self)
        self.address = address
        icon = QLabel()
        pixmap = QPixmap(r'pics\address.png')
        pixmap = pixmap.scaledToWidth(40)
        icon.setPixmap(pixmap)
        name = QLabel("<h3>{}<h3>".format(address.name))
        self.view_button = QPushButton("Изменить")
        self.view_button.setFixedWidth(80)
        self.delete_button = QPushButton("Удалить")
        self.delete_button.setFixedWidth(80)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.view_button)
        buttons_layout.addWidget(self.delete_button)

        layout = QHBoxLayout(self)
        layout.addWidget(icon)
        layout.addWidget(name)
        layout.addStretch()
        layout.addLayout(buttons_layout)
        
class BlockWidget(QWidget):
    def __init__(self, block):
        QWidget.__init__(self)
        self.block = block
        icon = QLabel()
        pixmap = QPixmap(r'pics\block.png')
        pixmap = pixmap.scaledToWidth(40)
        icon.setPixmap(pixmap)
        name = QLabel("<h3>{}<h3>".format(block.name))
        self.view_button = QPushButton("Изменить")
        self.view_button.setFixedWidth(80)
        self.delete_button = QPushButton("Удалить")
        self.delete_button.setFixedWidth(80)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.view_button)
        buttons_layout.addWidget(self.delete_button)

        layout = QHBoxLayout(self)
        layout.addWidget(icon)
        layout.addWidget(name)
        layout.addStretch()
        layout.addLayout(buttons_layout)
        