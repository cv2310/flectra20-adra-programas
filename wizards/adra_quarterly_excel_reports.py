import os
from flectra import models
import datetime

class ReportXlsQuarterly(models.AbstractModel):
    _name = 'report.adra_account_extended.report_xlsx_quarterly'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        worksheet = workbook.add_worksheet("Report")

        column_header_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
        column_content_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9, 'align': 'center', 'valign': 'vcenter'})

        meses = {
            1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL', 5: 'MAYO', 6: 'JUNIO',
            7: 'JULIO', 8: 'AGOSTO', 9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE', 12: 'DICIEMBRE'
        }

        mes_str = data.get('x_date')
        ano, mes, dia = map(int, mes_str.split('-'))

        ano_1 = ano
        ano_2 = ano
        ano_3 = ano
        mes_1 = mes
        mes_2 = mes
        mes_3 = mes

        month_01 = meses[mes]

        if mes == 11:
            mes_2 = mes + 1
            mes_3 = 1
            month_02 = meses[mes + 1]
            month_03 = meses[1]
            ano_3 = ano + 1
        elif mes == 12:
            mes_2 = 1
            mes_3 = 2
            month_02 = meses[1]
            month_03 = meses[2]
            ano_2 = ano + 1
            ano_3 = ano + 1
        else:
            mes_2 = mes + 1
            mes_3 = mes + 2
            month_02 = meses[mes + 1]
            month_03 = meses[mes + 2]
        h_month_01 = f"{ano_1}-{str(mes_1).zfill(2)}"
        h_month_02 = f"{ano_2}-{str(mes_2).zfill(2)}"
        h_month_03 = f"{ano_3}-{str(mes_3).zfill(2)}"
        date_from = datetime.date(ano_1, mes_1 , 1)
        if mes_3 == 12:
            date_to = (datetime.date(ano_3 +1, 1, 1) - datetime.timedelta(days=1))
        else:
            date_to = (datetime.date(ano_3, mes_3 + 1, 1) - datetime.timedelta(days=1))
        worksheet.set_column('A:A', 25.29)
        worksheet.set_column('B:B', 19.57)
        worksheet.set_column('C:C', 13.57)
        worksheet.set_column('D:D', 14.57)
        worksheet.set_column('E:E', 15)

        worksheet.write('A1', 'PROYECTOS', column_header_format)
        worksheet.write('B1', 'CODIGOS', column_header_format)
        worksheet.write('C1', month_01 + '-' + str(ano_1), column_header_format)
        worksheet.write('D1', month_02 + '-' + str(ano_2), column_header_format)
        worksheet.write('E1', month_03 + '-' + str(ano_3), column_header_format)

        date_close = datetime.date(2025, 4, 30)
        reportData = self.env['report.general.ledger.data']
        month = { h_month_01: 'month_01',
                  h_month_02: 'month_02',
                  h_month_03: 'month_03',}
        move_lines = reportData._get_quarterly_report_data(date_from, date_to, date_close, month)

        current_row = 1
        for line in move_lines:
            worksheet.write(current_row, 0, line['project'])
            worksheet.write(current_row, 1, line['code'])
            worksheet.write(current_row, 2, line['month_01'])
            worksheet.write(current_row, 3, line['month_02'])
            worksheet.write(current_row, 4, line['month_03'])
            current_row += 1
        workbook.close()