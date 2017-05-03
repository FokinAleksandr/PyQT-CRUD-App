#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Excel generation
"""
import xlsxwriter
import os
from app.db import data

def run(filename, session):
    workbook = xlsxwriter.Workbook(filename)
    for block in session.query(data.Block):
        worksheet = workbook.add_worksheet(block.address.name + '-' + block.name)
        worksheet.autofilter('A1:AC1')
        worksheet.set_column('B1:AC1', 20)
        worksheet.set_column('G1:G1', 30)
        worksheet.set_default_row(30)
        worksheet.set_tab_color('green')
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format({'text_wrap': True})
        worksheet.write('A1', '№ комнаты', bold)
        worksheet.write('B1', 'ФИО сотрудника', bold)
        worksheet.write('C1', 'Уникальный логин', bold)
        worksheet.write('D1', 'Телефоны', bold)
        worksheet.write('E1', 'Должность', bold)
        worksheet.write('F1', 'Отдел', bold)
        worksheet.write('G1', 'E-Mail', bold)
        worksheet.write('H1', 'Общие папки', bold)
        worksheet.write('I1', 'Сетевой принтер', bold)
        worksheet.write('J1', 'Доп информация о сотруднке', bold)
        worksheet.write('K1', 'Домен', bold)
        worksheet.write('L1', 'Имя компьютера', bold)
        worksheet.write('M1', 'MAC-адрес', bold)
        worksheet.write('N1', 'Серверные приложения', bold)
        worksheet.write('O1', '№ розетки', bold)
        worksheet.write('P1', 'Windows OS', bold)
        worksheet.write('Q1', 'Ключ Windows OS', bold)
        worksheet.write('R1', 'MS Office', bold)
        worksheet.write('S1', 'Ключ MS Office', bold)
        worksheet.write('T1', 'Клиент электронной почты', bold)
        worksheet.write('U1', 'Как подключен', bold)
        worksheet.write('V1', 'Агент KES', bold)
        worksheet.write('W1', 'Антивирус', bold)
        worksheet.write('X1', 'Консультант', bold)
        worksheet.write('Y1', 'Гарант', bold)
        worksheet.write('Z1', '1С', bold)
        worksheet.write('AA1', 'КДС', bold)
        worksheet.write('AB1', 'Доп информация о компьютере', bold)
        row = 1
        for employee in session.query(data.Employee).\
                            join(data.Room).\
                            join(data.Block).\
                            filter(data.Block.name==block.name):
            worksheet.set_row(row, 50)
            print(employee.fullname)
            if len(employee.pc) > 1:
                worksheet.merge_range(row, 0, row + len(employee.pc) - 1, 0,
                                      employee.room.name)
                worksheet.merge_range(row, 1, row + len(employee.pc) - 1, 1,
                                      employee.fullname, cell_format)
                worksheet.merge_range(row, 2, row + len(employee.pc) - 1, 2,
                                      employee.unique_login)
                worksheet.merge_range(row, 3, row + len(employee.pc) - 1, 3,
                                      '\n'.join(phone.number for phone in employee.phone), cell_format)
                worksheet.merge_range(row, 4, row + len(employee.pc) - 1, 4,
                                      employee.position.name, cell_format)
                worksheet.merge_range(row, 5, row + len(employee.pc) - 1, 5,
                                      employee.department.name, cell_format)
                worksheet.merge_range(row, 6, row + len(employee.pc) - 1, 6,
                                      '\n'.join(email.email for email in employee.email), cell_format)
                worksheet.merge_range(row, 7, row + len(employee.pc) - 1, 7,
                                      'Есть' if employee.shared_folder else 'Нет')
                worksheet.merge_range(row, 8, row + len(employee.pc) - 1, 8,
                                      'Есть' if employee.network_printer else 'Нет')
                worksheet.merge_range(row, 9, row + len(employee.pc) - 1, 9,
                                      employee.comments)
            else:
                worksheet.write(row, 0, employee.room.name)
                worksheet.write(row, 1, employee.fullname, cell_format)
                worksheet.write(row, 2, employee.unique_login)
                worksheet.write(row, 3, '\n'.join(phone.number for phone in employee.phone), cell_format)
                worksheet.write(row, 4, employee.position.name, cell_format)
                worksheet.write(row, 5, employee.department.name, cell_format)
                worksheet.write(row, 6, '\n'.join(email.email for email in employee.email), cell_format)
                worksheet.write(row, 7, 'Есть' if employee.shared_folder else 'Нет')
                worksheet.write(row, 8, 'Есть' if employee.network_printer else 'Нет')
                worksheet.write(row, 9, employee.comments)

            for pc in employee.pc:
                worksheet.write(row, 10, pc.pcname.domain.name)
                worksheet.write(row, 11, pc.pcname.name)
                worksheet.write(row, 12, pc.mac_address)
                worksheet.write(row, 13, pc.app_server)
                worksheet.write(row, 14, pc.powersocket.name)
                worksheet.write(row, 15, pc.windows.name)
                worksheet.write(row, 16, pc.windows_os_key)
                worksheet.write(row, 17, pc.office.name)
                worksheet.write(row, 18, pc.ms_office_key)
                worksheet.write(row, 19, pc.mail_client)
                worksheet.write(row, 20, pc.connectiontype.name)
                worksheet.write(row, 21, 'Есть' if pc.kes else 'Нет')
                worksheet.write(row, 22, pc.antivirus.name)
                worksheet.write(row, 23, 'Есть' if pc.consultant else 'Нет')
                worksheet.write(row, 24, 'Есть' if pc.guarantee else 'Нет')
                worksheet.write(row, 25, 'Есть' if pc.odin_s else 'Нет')
                worksheet.write(row, 26, 'Есть' if pc.kdc else 'Нет')
                worksheet.write(row, 27, pc.comments)
                row += 1

            if not employee.pc:
                row += 1

    workbook.close()
