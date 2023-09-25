from flectra import models
import datetime


class ReportXlsExpensesGrouped(models.AbstractModel):
    _name = 'report.adra_account_extended.report_xlsx_expenses_grouped'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        worksheet = workbook.add_worksheet("Report")

        year, mes, dia = map(int, data['x_date_from'].split('-'))

        date_from = datetime.date(year, 1, 1)
        date_to = (datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1))
        ano_str = str(year)
        x_project = data['x_project']
        x_account_analytic_account_id = data['x_account_analytic_account_id']

        reportData = self.env['report.general.ledger.data']
        move_lines = reportData._get_budget_report_data(x_account_analytic_account_id, date_from.strftime('%Y-%m-%d'), date_to.strftime('%Y-%m-%d'),
                                                        '2023-04-30')

        title_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 12, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
        first_month_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'align': 'center', 'valign': 'vcenter',
             'left': True, 'bottom': True, 'top': True})
        middle_month_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'align': 'center', 'valign': 'vcenter',
             'bottom': True, 'top': True})
        initial_month_first_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 12, 'bold': True, 'valign': 'vcenter',
             'left': True, 'bottom': True, 'top': True})
        initial_month_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'valign': 'vcenter', 'bottom': True,
             'top': True, 'num_format': '"$"#,##0', 'align': 'right'})
        initial_month_last_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'valign': 'vcenter', 'align': 'right',
             'bottom': True, 'top': True, 'right': True, 'num_format': '"$"#,##0'})
        acc_acc_type_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'left', 'valign': 'vcenter'})
        table_content_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'right', 'valign': 'vcenter', 'num_format': '"$"#,##0'})
        table_content_total_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'align': 'right', 'valign': 'vcenter',
             'num_format': '"$"#,##0'})
        total_header_month_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'align': 'center', 'valign': 'vcenter',
             'right': True, 'bottom': True, 'top': True})
        table_header = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 12, 'bold': True, 'align': 'center', 'valign': 'vcenter',
             'border': 1})
        total_first_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'valign': 'vcenter',
             'left': True, 'bottom': True, 'top': True})
        total_month_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'valign': 'vcenter', 'bottom': True,
             'top': True, 'num_format': '"$"#,##0', 'align': 'right'})
        total_month_last_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'valign': 'vcenter', 'align': 'right',
             'bottom': True, 'top': True, 'right': True, 'num_format': '"$"#,##0'})
        total_first_red_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 12, 'bold': True, 'valign': 'vcenter',
             'left': True, 'bottom': True, 'top': True, 'bg_color': 'red', 'color': 'white'})
        total_month_red_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'valign': 'vcenter', 'bottom': True,
             'top': True, 'num_format': '"$"#,##0', 'align': 'right', 'bg_color': 'red', 'color': 'white'})
        total_month_last_red_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'valign': 'vcenter', 'align': 'right',
             'bottom': True, 'top': True, 'right': True, 'num_format': '"$"#,##0', 'bg_color': 'red', 'color': 'white'})

        worksheet.set_column('A:A', 42)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 12)
        worksheet.set_column('D:D', 12)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 12)
        worksheet.set_column('G:G', 12)
        worksheet.set_column('H:H', 12)
        worksheet.set_column('I:I', 12)
        worksheet.set_column('J:J', 12)
        worksheet.set_column('K:K', 12)
        worksheet.set_column('L:L', 12)
        worksheet.set_column('M:M', 12)
        worksheet.set_column('N:N', 12)
        worksheet.set_column('O:O', 14)

        worksheet.set_row(2, 16)
        worksheet.set_row(5, 16)
        worksheet.set_row(7, 16)

        worksheet.merge_range('A2:N2', f'ANÁLISIS DE PROYECTO {x_project} AÑO {ano_str}', title_format)

        worksheet.write('C5', 'ENERO', initial_month_first_format)
        worksheet.write('D5', 'FEBRERO', middle_month_format)
        worksheet.write('E5', 'MARZO', middle_month_format)
        worksheet.write('F5', 'ABRIL', middle_month_format)
        worksheet.write('G5', 'MAYO', middle_month_format)
        worksheet.write('H5', 'JUNIO', middle_month_format)
        worksheet.write('I5', 'JULIO', middle_month_format)
        worksheet.write('J5', 'AGOSTO', middle_month_format)
        worksheet.write('K5', 'SEPTIEMBRE', middle_month_format)
        worksheet.write('L5', 'OCTUBRE', middle_month_format)
        worksheet.write('M5', 'NOVIEMBRE', middle_month_format)
        worksheet.write('N5', 'DICIEMBRE', middle_month_format)
        worksheet.write('O5', 'TOTAL', total_header_month_format)

        saldo_inicial = move_lines['saldo_inicial'][0]
        worksheet.write('A6', 'SALDO INICIAL', initial_month_first_format)
        worksheet.write('B6', '', initial_month_format)
        worksheet.write('C6', saldo_inicial['mes_01'], initial_month_format)
        worksheet.write('D6', saldo_inicial['mes_02'], initial_month_format)
        worksheet.write('E6', saldo_inicial['mes_03'], initial_month_format)
        worksheet.write('F6', saldo_inicial['mes_04'], initial_month_format)
        worksheet.write('G6', saldo_inicial['mes_05'], initial_month_format)
        worksheet.write('H6', saldo_inicial['mes_06'], initial_month_format)
        worksheet.write('I6', saldo_inicial['mes_07'], initial_month_format)
        worksheet.write('J6', saldo_inicial['mes_08'], initial_month_format)
        worksheet.write('K6', saldo_inicial['mes_09'], initial_month_format)
        worksheet.write('L6', saldo_inicial['mes_10'], initial_month_format)
        worksheet.write('M6', saldo_inicial['mes_11'], initial_month_format)
        worksheet.write('N6', saldo_inicial['mes_12'], initial_month_format)
        worksheet.write('O6', '', initial_month_last_format)

        worksheet.merge_range('A7:O7', 'INGRESOS', table_header)

        current_row = 7

        for line in move_lines['ingresos']:
            worksheet.write(current_row, 0, line['tipo_cuenta'], acc_acc_type_format)
            worksheet.write(current_row, 1, line['cuenta'], acc_acc_type_format)
            worksheet.write(current_row, 2, line['mes_01'], table_content_format)
            worksheet.write(current_row, 3, line['mes_02'], table_content_format)
            worksheet.write(current_row, 4, line['mes_03'], table_content_format)
            worksheet.write(current_row, 5, line['mes_04'], table_content_format)
            worksheet.write(current_row, 6, line['mes_05'], table_content_format)
            worksheet.write(current_row, 7, line['mes_06'], table_content_format)
            worksheet.write(current_row, 8, line['mes_07'], table_content_format)
            worksheet.write(current_row, 9, line['mes_08'], table_content_format)
            worksheet.write(current_row, 10, line['mes_09'], table_content_format)
            worksheet.write(current_row, 11, line['mes_10'], table_content_format)
            worksheet.write(current_row, 12, line['mes_11'], table_content_format)
            worksheet.write(current_row, 13, line['mes_12'], table_content_format)
            worksheet.write(current_row, 14, line['mes_total'], table_content_total_format)
            current_row += 1

        total_ingresos = move_lines['ingresos_totales'][0]
        worksheet.write(current_row, 0, 'TOTAL INGRESOS', total_first_format)
        worksheet.write(current_row, 1, '', total_month_format)
        worksheet.write(current_row, 2, total_ingresos['mes_01'], total_month_format)
        worksheet.write(current_row, 3, total_ingresos['mes_02'], total_month_format)
        worksheet.write(current_row, 4, total_ingresos['mes_03'], total_month_format)
        worksheet.write(current_row, 5, total_ingresos['mes_04'], total_month_format)
        worksheet.write(current_row, 6, total_ingresos['mes_05'], total_month_format)
        worksheet.write(current_row, 7, total_ingresos['mes_06'], total_month_format)
        worksheet.write(current_row, 8, total_ingresos['mes_07'], total_month_format)
        worksheet.write(current_row, 9, total_ingresos['mes_08'], total_month_format)
        worksheet.write(current_row, 10, total_ingresos['mes_09'], total_month_format)
        worksheet.write(current_row, 11, total_ingresos['mes_10'], total_month_format)
        worksheet.write(current_row, 12, total_ingresos['mes_11'], total_month_format)
        worksheet.write(current_row, 13, total_ingresos['mes_12'], total_month_format)
        worksheet.write(current_row, 14, total_ingresos['mes_total'], total_month_last_format)

        current_row += 2

        worksheet.merge_range(current_row, 0, current_row, 14, 'EGRESOS', table_header)

        current_row += 1

        for line in move_lines['gastos']:
            worksheet.write(current_row, 0, line['tipo_cuenta'], acc_acc_type_format)
            worksheet.write(current_row, 1, line['cuenta'], acc_acc_type_format)
            worksheet.write(current_row, 2, line['mes_01'], table_content_format)
            worksheet.write(current_row, 3, line['mes_02'], table_content_format)
            worksheet.write(current_row, 4, line['mes_03'], table_content_format)
            worksheet.write(current_row, 5, line['mes_04'], table_content_format)
            worksheet.write(current_row, 6, line['mes_05'], table_content_format)
            worksheet.write(current_row, 7, line['mes_06'], table_content_format)
            worksheet.write(current_row, 8, line['mes_07'], table_content_format)
            worksheet.write(current_row, 9, line['mes_08'], table_content_format)
            worksheet.write(current_row, 10, line['mes_09'], table_content_format)
            worksheet.write(current_row, 11, line['mes_10'], table_content_format)
            worksheet.write(current_row, 12, line['mes_11'], table_content_format)
            worksheet.write(current_row, 13, line['mes_12'], table_content_format)
            worksheet.write(current_row, 14, line['mes_total'], table_content_total_format)
            current_row += 1

        total_egresos = move_lines['gastos_totales'][0]
        worksheet.write(current_row, 0, 'TOTAL EGRESOS', total_first_format)
        worksheet.write(current_row, 1, '', total_month_format)
        worksheet.write(current_row, 2, total_egresos['mes_01'], total_month_format)
        worksheet.write(current_row, 3, total_egresos['mes_02'], total_month_format)
        worksheet.write(current_row, 4, total_egresos['mes_03'], total_month_format)
        worksheet.write(current_row, 5, total_egresos['mes_04'], total_month_format)
        worksheet.write(current_row, 6, total_egresos['mes_05'], total_month_format)
        worksheet.write(current_row, 7, total_egresos['mes_06'], total_month_format)
        worksheet.write(current_row, 8, total_egresos['mes_07'], total_month_format)
        worksheet.write(current_row, 9, total_egresos['mes_08'], total_month_format)
        worksheet.write(current_row, 10, total_egresos['mes_09'], total_month_format)
        worksheet.write(current_row, 11, total_egresos['mes_10'], total_month_format)
        worksheet.write(current_row, 12, total_egresos['mes_11'], total_month_format)
        worksheet.write(current_row, 13, total_egresos['mes_12'], total_month_format)
        worksheet.write(current_row, 14, total_egresos['mes_total'], total_month_last_format)

        current_row += 1

        saldo_final = move_lines['saldos'][0]
        worksheet.write(current_row, 0, 'SALDO FINAL MES', total_first_red_format)
        worksheet.write(current_row, 1, '', total_month_red_format)
        worksheet.write(current_row, 2, saldo_final['mes_01'], total_month_red_format)
        worksheet.write(current_row, 3, saldo_final['mes_02'], total_month_red_format)
        worksheet.write(current_row, 4, saldo_final['mes_03'], total_month_red_format)
        worksheet.write(current_row, 5, saldo_final['mes_04'], total_month_red_format)
        worksheet.write(current_row, 6, saldo_final['mes_05'], total_month_red_format)
        worksheet.write(current_row, 7, saldo_final['mes_06'], total_month_red_format)
        worksheet.write(current_row, 8, saldo_final['mes_07'], total_month_red_format)
        worksheet.write(current_row, 9, saldo_final['mes_08'], total_month_red_format)
        worksheet.write(current_row, 10, saldo_final['mes_09'], total_month_red_format)
        worksheet.write(current_row, 11, saldo_final['mes_10'], total_month_red_format)
        worksheet.write(current_row, 12, saldo_final['mes_11'], total_month_red_format)
        worksheet.write(current_row, 13, saldo_final['mes_12'], total_month_red_format)
        worksheet.write(current_row, 14, saldo_final['mes_total'], total_month_last_red_format)

        workbook.close()
