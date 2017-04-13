#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Десктопное приложение с использованием SQLAlchemy и PyQT
"""
import sys
from app.dialogs import login
from app import main

from PyQt5.QtWidgets import QApplication, QDialog

###########################################################################################################
       
def run():
    app = QApplication([])
    
    login_window = login.LoginWindow()

    result = login_window.exec_()
    if result == QDialog.Accepted:
        main_window = main.MainWindow()
    else:
        sys.exit(result)

    sys.exit(app.exec_())