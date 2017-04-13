#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QMessageBox

class Dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

    def closeEvent(self, evnt):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Уведомление')
        msg_box.setText('Сохранить данные')
        msg_box.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        buttonY = msg_box.button(QMessageBox.Yes)
        buttonY.setText('Да')
        buttonN = msg_box.button(QMessageBox.No)
        buttonN.setText('Нет')
        buttonC = msg_box.button(QMessageBox.Cancel)
        buttonC.setText('Отменить')
        msg_box.exec_()

        if msg_box.clickedButton() == buttonY:
            QDialog.accept(self)
        elif msg_box.clickedButton() == buttonN:
            QDialog.closeEvent(self, evnt)
        elif msg_box.clickedButton() == buttonC:
            evnt.ignore()

    def accept(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Уведомление')
        msg_box.setText('Подтвердить ввод данных')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = msg_box.button(QMessageBox.Yes)
        buttonY.setText('Да')
        buttonN = msg_box.button(QMessageBox.No)
        buttonN.setText('Нет')
        msg_box.exec_()

        if msg_box.clickedButton() == buttonY:
            QDialog.accept(self)