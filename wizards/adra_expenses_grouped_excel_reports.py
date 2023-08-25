from flectra import models
import datetime

class ReportXlsExpensesGrouped(models.AbstractModel):
    _name = 'report.adra_account_extended.report_xlsx_expenses_grouped'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        worksheet = workbook.add_worksheet("Report")

#        reportData = self.env['report.general.ledger.data']
#        move_lines = reportData._get_budget_report_data(x_account_analytic_account_id,x_date_from, x_date_to, '2023-04-30')

        ano, mes, dia = map(int, data['x_date_from'].split('-'))
        date_from = datetime.date(ano, mes, dia)
        ano, mes, dia = map(int, data['x_date_to'].split('-'))
        date_to = datetime.date(ano, mes, dia)
        x_date_from = data['x_date_from']
        x_date_to = data['x_date_to']
        x_project = data['x_project']

        x_account_analytic_account_id = data['x_account_analytic_account_id']

        header_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
        column_header_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
        column_content_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
        column_content_format_number = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0'})


        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 25)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 25)

        worksheet.write('A1', 'Proyecto:', header_format)
        worksheet.write('A2', 'Desde:', header_format)
        worksheet.write('C2', 'Hastal:', header_format)
        worksheet.write('A3', 'Tipo de cuenta', column_header_format)
        worksheet.write('B3', 'Cuenta', column_header_format)
        worksheet.write('C3', 'Gasto', column_header_format)

        worksheet.merge_range('B1:C1', x_project, column_header_format)
        worksheet.write('B2', x_date_from, column_header_format)
        worksheet.write('D2', x_date_to, column_header_format)

        date_close = datetime.date(2023, 4, 30)
        reportData = self.env['report.general.ledger.data']
        move_lines = reportData._get_budget_report_data( x_account_analytic_account_id, date_from, date_to, date_close)
        current_row = 3
        for line in move_lines:
            worksheet.write(current_row, 0, line['account_type'], column_content_format)
            worksheet.write(current_row, 1, line['account'], column_content_format)
            worksheet.write(current_row, 2, line['expense'], column_content_format_number)
            current_row += 1
        workbook.close()