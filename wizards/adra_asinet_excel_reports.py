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
        move_lines = reportData._get_asinet_data(x_date_from, x_date_to, '2024-06-30')

        column_content_format = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
        column_content_format_number = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0'})

        worksheet.set_column(0, 0, 36)
        worksheet.set_column(1, 1, 12)
        worksheet.set_column(2, 2, 15.43)
        worksheet.set_column(3, 3, 9.29)
        worksheet.set_column(4, 4, 12.57)
        worksheet.set_column(5, 5, 16.71)
        worksheet.set_column(6, 6, 11.57)
        worksheet.set_column(7, 7, 10.43)
        worksheet.set_column(8, 8, 45.29)

        worksheet.write(0, 0, 'Project', column_content_format)
        worksheet.write(0, 1, 'AccountCode', column_content_format)
        worksheet.write(0, 2, 'SubAccountCode', column_content_format)
        worksheet.write(0, 3, 'FundCode', column_content_format)
        worksheet.write(0, 4, 'FunctionCode', column_content_format_number)
        worksheet.write(0, 5, 'RestrictionCode', column_content_format)
        worksheet.write(0, 6, 'EntityValue', column_content_format)
        worksheet.write(0, 7, 'SendMemo', column_content_format)
        worksheet.write(0, 8, 'Description', column_content_format)

        current_row = 1

        for line in move_lines:
            worksheet.write(current_row, 0, line['Project'])
            worksheet.write(current_row, 1, line['AccountCode'])
            worksheet.write(current_row, 2, line['SubAccountCode'])
            worksheet.write(current_row, 3, line['FundCode'])
            worksheet.write(current_row, 4, line['FunctionCode'])
            worksheet.write(current_row, 5, line['RestrictionCode'])
            worksheet.write(current_row, 6, line['EntityValue'])
            worksheet.write(current_row, 7, line['SendMemo'])
            worksheet.write(current_row, 8, line['Description'] + str_mes)
            current_row += 1
        workbook.close()
