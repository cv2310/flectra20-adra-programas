import os
from flectra import models

class ReportXlsAsinet(models.AbstractModel):
    _name = 'report.adra_account_extended.report_xlsx_asinet'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        worksheet = workbook.add_worksheet("Report")

        x_date_from = data.get('x_date_from')
        x_date_to = data.get('x_date_to')

        meses = {
            1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL', 5: 'MAYO', 6: 'JUNIO',
            7: 'JULIO', 8: 'AGOSTO', 9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE', 12: 'DICIEMBRE'
        }

        ano, mes, dia = map(int, x_date_from.split('-'))
        str_mes = meses[mes]
        reportData = self.env['report.general.ledger.data']
        move_lines = reportData._get_asinet_data(x_date_from, x_date_to, '2023-04-30')

        column_content_format = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
        column_content_format_number = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0'})

        current_row = 0
        worksheet.set_column(current_row, 0, 12)
        #worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 15.43)
        worksheet.set_column('C:C', 9.29)
        worksheet.set_column('D:D', 12.57)
        worksheet.set_column('E:E', 16.71)
        worksheet.set_column('F:F', 11.57)
        worksheet.set_column('G:G', 10.43)
        worksheet.set_column('H:H', 45.29)


        worksheet.write(current_row, 0 ,'AccountCode', column_content_format)
        worksheet.write('B1', 'SubAccountCode', column_content_format)
        worksheet.write('C1', 'FundCode', column_content_format)
        worksheet.write('D1', 'FunctionCode', column_content_format_number)
        worksheet.write('E1', 'RestrictionCode', column_content_format)
        worksheet.write('F1', 'EntityValue', column_content_format)
        worksheet.write('G1', 'SendMemo', column_content_format)
        worksheet.write('H1', 'Description', column_content_format)

        current_row = 1

        for line in move_lines:
            worksheet.write(current_row, 0, line['AccountCode'])
            worksheet.write(current_row, 1, line['SubAccountCode'])
            worksheet.write(current_row, 2, line['FundCode'])
            worksheet.write(current_row, 3, line['FunctionCode'])
            worksheet.write(current_row, 4, line['RestrictionCode'])
            worksheet.write(current_row, 5, line['EntityValue'])
            worksheet.write(current_row, 6, line['SendMemo'])
            worksheet.write(current_row, 7, line['Description'] + str_mes)
            current_row += 1
        workbook.close()
