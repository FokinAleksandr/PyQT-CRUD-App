import xlsxwriter
from app import data


def run(session):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Employees.xlsx')

    for block in session.query(data.Block):
        worksheet = workbook.add_worksheet(block.address.name + '-' + block.name)
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', '№ комнаты', bold)
        worksheet.write('B1', 'ФИО сотрудника', bold)
        worksheet.write('C1', 'Уникальный логин', bold)
        worksheet.write('D1', 'Телефоны', bold)
        worksheet.write('E1', 'Должность', bold)
        worksheet.write('F1', 'Отдел', bold)
        worksheet.write('G1', 'E-Mail', bold)
        worksheet.write('H1', 'Доп информация о сотруднке', bold)
        worksheet.write('I1', 'Домен', bold)
        worksheet.write('J1', 'Имя компьютера', bold)
        worksheet.write('K1', 'MAC-адрес', bold)
        worksheet.write('L1', 'Серверные приложения', bold)
        worksheet.write('M1', '№ розетки', bold)
        worksheet.write('N1', 'Windows OS', bold)
        worksheet.write('O1', 'ключ Windows OS', bold)
        worksheet.write('P1', 'MS Office', bold)
        worksheet.write('Q1', 'ключ MS Office', bold)
        worksheet.write('R1', 'Клиент электронной почты', bold)
        worksheet.write('S1', 'Как подключен', bold)
        worksheet.write('T1', 'Агент KES', bold)
        worksheet.write('U1', 'Антивирус', bold)
        worksheet.write('V1', 'Консультант', bold)
        worksheet.write('W1', 'Гарант', bold)
        worksheet.write('X1', '1С', bold)
        worksheet.write('Y1', 'КДС', bold)
        worksheet.write('Z1', 'Доп информация о компьютере', bold)
        worksheet.write('AA1', 'Общие папки', bold)
        worksheet.write('AB1', 'Сетевой принтер', bold)

        row = 1
        col = 0

        employees = session.query(data.Employee).\
                            join(data.Room).\
                            join(data.Block).\
                            filter(data.Block.name==block.name)
        for employee in employees:
            worksheet.write(row, 0, employee.room.name)
            worksheet.write(row, 1, employee.fullname)
            worksheet.write(row, 2, employee.unique_login)
            worksheet.write(row, 3, '\n'.join(phone.number for phone in employee.phone))
            worksheet.write(row, 4, employee.position.name)
            worksheet.write(row, 5, employee.department.name)
            worksheet.write(row, 6, '\n'.join(email.email for email in employee.email))
            worksheet.write(row, 7, employee.comments)
            worksheet.set_column(0, 7, 30)
            row += 1

    workbook.close()
