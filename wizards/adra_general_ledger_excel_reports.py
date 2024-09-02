import os
import time
from datetime import datetime
from flectra import models, api, _
from flectra.exceptions import UserError

class ReportXlsGeneralLedger(models.AbstractModel):
    _name = 'report.adra_account_extended.report_xlsx_general_ledger'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        worksheet = workbook.add_worksheet("Report")

        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path_adra = os.path.join(module_path, 'static', 'src', 'img', 'logo_adra_mn.png')
        logo_path_mejornines = os.path.join(module_path, 'static', 'src', 'img', 'mejor_niñez.jpg')

        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_date_dmy = datetime.now().strftime('%d-%m-%Y')
        p_data = data.get('form')
        x_document_type = p_data['x_document_type']
        if x_document_type == 'BANCO':
            x_document_type = 'LIBRO BANCO'
        elif x_document_type == 'CONCILIACION':
            x_document_type = 'CONCILIACIÓN BANCARIA'
        elif x_document_type == 'RENDICION':
            x_document_type = 'RENDICIÓN DE CUENTAS'
        x_program_name = p_data['x_program_name']
        x_sort_by = p_data['x_sort_by']
        if x_sort_by == 'fecha_ingreso':
            x_sort_by = 'Fecha'
        elif x_sort_by == 'nro_comprobante':
            x_sort_by = 'Nº Comprobante'
        x_report_type = p_data['x_report_type']
        if x_report_type == 'cuenta':
            x_report_type = 'ADRA'
        elif x_report_type == 'cuenta_senainfo':
            x_report_type = 'SIS'

        accounts = objs['Accounts']


        base_format = workbook.add_format({'font_name': 'Liberation Sans', 'font_size': 11})
        base_format_center = workbook.add_format({'font_name': 'Liberation Sans', 'font_size': 11, 'align': 'center'})
        base_format_bold = workbook.add_format({'font_name': 'Liberation Sans', 'font_size': 11, 'bold': True})
        base_format_bold_align_right = workbook.add_format({'font_name': 'Liberation Sans', 'font_size': 11,
                                                            'bold': True, 'align': 'right'})
        base_format_align_right = workbook.add_format({'font_name': 'Liberation Sans', 'font_size': 11,
                                                       'align': 'right'})
        column_header = workbook.add_format({'top': 1, 'bottom': 1, 'font_name': 'Liberation Sans', 'font_size': 11,
                                             'bold': True, 'align': 'center', 'valign': 'vcenter'})
        column_content = workbook.add_format({'top': 1, 'bottom': 1, 'font_name': 'Liberation Sans', 'font_size': 10,
                                             'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        column_content_monetary = workbook.add_format({'top': 1, 'bottom': 1, 'font_name': 'Liberation Sans',
        'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '$#,##0'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'font_name': 'Liberation Sans', 'font_size': 10,
                                'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'top' :1, 'bottom': 1})
        current_date_dmy_format = workbook.add_format({'font_name': 'Liberation Sans', 'font_size': 16,
                                                       'align': 'right'})
        movement_type_format = workbook.add_format({'font_name': 'Liberation Sans', 'font_size': 21, 'bold': True})
        cell_border_top_bottom_format = workbook.add_format({'top': 1, 'bottom': 1, 'font_name': 'Liberation Sans',
                                                             'font_size': 17, 'align': 'center', 'valign': 'vcenter'})
        cell_border_top_bottom_format_money = workbook.add_format({'top': 1, 'bottom': 1, 'font_name':
            'Liberation Sans', 'font_size': 17, 'align': 'center', 'valign': 'vcenter', 'num_format': '$#,##0'})
        cell_border_top_bottom_format_final = workbook.add_format({'font_name': 'Liberation Sans', 'font_size': 19,
                                                                   'align': 'center', 'valign': 'vcenter'})
        cell_border_top_bottom_format_final_money = workbook.add_format({'font_name': 'Liberation Sans',
                                        'font_size': 19,'align': 'center', 'valign': 'vcenter', 'num_format': '$#,##0'})
        cell_border_top_bottom_format_conc = workbook.add_format({'top': 1, 'bottom': 1, 'font_name': 'Liberation Sans',
                                                'font_size': 13, 'align': 'center', 'valign': 'vcenter', 'bold': True})
        cell_border_top_bottom_format_conc_money = workbook.add_format({'top': 1, 'bottom': 1, 'font_name':
                                        'Liberation Sans', 'num_format': '$#,##0', 'font_size': 13, 'align': 'center',
                                        'valign': 'vcenter', 'bold': True})
        cell_border_top_bottom_format_conc_money_no_borders = workbook.add_format({'font_name': 'Liberation Sans',
                        'num_format': '$#,##0', 'font_size': 13, 'align': 'center', 'valign': 'vcenter'})
        cell_border_top_bottom_format_conc_total = workbook.add_format({'font_name': 'Liberation Sans', 'font_size': 13,
                                                                        'align': 'center', 'valign': 'vcenter'})
        cell_border_top_bottom_format_align_left = workbook.add_format({'top': 1, 'bottom': 1, 'font_name':
            'Liberation Sans', 'font_size': 16, 'align': 'left', 'valign': 'vcenter'})
        cell_border_top_bottom_format_align_right = workbook.add_format({'top': 1, 'bottom': 1, 'font_name':
            'Liberation Sans', 'font_size': 16, 'align': 'right', 'valign': 'vcenter', 'num_format': '$#,##0'})
        cell_border_top_bottom_format_little_align_left = workbook.add_format({'top': 1, 'bottom': 1, 'font_name':
            'Liberation Sans', 'font_size': 13, 'align': 'left', 'valign': 'vcenter'})
        cell_border_top_bottom_format_little_align_right = workbook.add_format({'top': 1, 'bottom': 1, 'font_name':
            'Liberation Sans', 'font_size': 13, 'align': 'right', 'valign': 'vcenter', 'num_format': '$#,##0'})

        worksheet.set_row(12, 30)

        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 25)
        worksheet.set_column('E:E', 25)
        worksheet.set_column('F:F', 25)
        worksheet.set_column('G:G', 25)
        worksheet.set_column('H:H', 25)
        worksheet.set_column('I:I', 25)
        worksheet.set_column('J:J', 25)


        if p_data['x_document_type'] == 'BANCO' and p_data['x_report_type'] == 'cuenta':

            worksheet.set_row(6, 30)
            worksheet.set_row(13, 30)
            worksheet.set_row(14, 30)

            worksheet.write('A1', current_date, base_format)
            worksheet.insert_image('A3', logo_path_adra, {'x_scale': 0.6, 'y_scale': 0.6})
            worksheet.write('B3', '                Agencia Adventista de Desarrollo y Recursos Asistenciales', base_format)
            worksheet.write('B4', '                RUT: 70051600-8', base_format)
            worksheet.write('F1', 'ADRA CHILE', base_format)
            worksheet.merge_range('A7:F7', x_document_type, movement_type_format)
            worksheet.write('I7', current_date_dmy, current_date_dmy_format)
            worksheet.merge_range('A10:B10', 'Programa:', base_format_bold)
            worksheet.merge_range('A11:C11', x_program_name, base_format)
            worksheet.merge_range('D10:E10', 'Ordenado por:', base_format_bold)
            worksheet.merge_range('D11:E11', x_sort_by, base_format)
            worksheet.merge_range('F10:G10', 'Fecha desde: ' + p_data['date_from'], base_format_bold)
            worksheet.merge_range('F11:G11', 'Fecha hasta: ' + p_data['date_to'], base_format_bold)
            worksheet.merge_range('H10:I10', 'Tipo de Reporte:', base_format_bold)
            worksheet.merge_range('H11:I11', x_report_type, base_format)
            worksheet.merge_range('A13:G13', '', cell_border_top_bottom_format)
            worksheet.write('H13', 'Saldo inicial: ', cell_border_top_bottom_format)
            for account in accounts:
                worksheet.write('I13', account['initial_balance'], cell_border_top_bottom_format_money)
            worksheet.merge_range('A14:B14', 'INGRESOS:', cell_border_top_bottom_format)
            worksheet.merge_range('C14:I14', '', cell_border_top_bottom_format)
            worksheet.write('A15', 'FECHA', column_header)
            worksheet.write('B15', 'N° COMP', column_header)
            worksheet.write('C15', 'FORMA DE PAGO', column_header)
            worksheet.write('D15', 'N° COMP PAGO', column_header)
            worksheet.write('E15', 'FECHA DE PAGO', column_header)
            worksheet.write('F15', 'GLOSA', column_header)
            worksheet.write('G15', 'BENEFICIARIO', column_header)
            worksheet.write('H15', 'MONTO', column_header)
            worksheet.write('I15', 'SALDO', column_header)
            current_row = 15
            for account in accounts:
                for line in account['move_lines']:
                    if line['tipo_documento'] == 'INGRESO':
                        worksheet.write(current_row, 0, line.get('fecha_ingreso', ''), date_format)
                        worksheet.write(current_row, 1, line.get('nro_comprobante', ''), column_content)
                        worksheet.write(current_row, 2, line.get('medio_pago', ''), column_content)
                        worksheet.write(current_row, 3, line.get('nro_comprobante_pago', ''), column_content)
                        worksheet.write(current_row, 4, line.get('fecha_pago', ''), date_format)
                        worksheet.write(current_row, 5, line.get('glosa', ''), column_content)
                        worksheet.write(current_row, 6, line.get('beneficiario', ''), column_content)
                        worksheet.write_number(current_row, 7, line.get('ingreso', 0), column_content_monetary)
                        worksheet.write_number(current_row, 8, line.get('saldo', 0), column_content_monetary)
                        current_row += 1
            current_row += 3
            worksheet.set_row(current_row, 30)
            worksheet.merge_range(current_row, 0, current_row, 1, 'EGRESOS:', cell_border_top_bottom_format)
            worksheet.merge_range(current_row, 2, current_row, 8, '', cell_border_top_bottom_format)
            current_row += 1
            worksheet.set_row(current_row, 30)
            worksheet.write(current_row, 0, 'FECHA', column_header)
            worksheet.write(current_row, 1, 'N° COMP', column_header)
            worksheet.write(current_row, 2, 'FORMA DE PAGO', column_header)
            worksheet.write(current_row, 3, 'N° COMP PAGO', column_header)
            worksheet.write(current_row, 4, 'FECHA DE PAGO', column_header)
            worksheet.write(current_row, 5, 'GLOSA', column_header)
            worksheet.write(current_row, 6, 'BENEFICIARIO', column_header)
            worksheet.write(current_row, 7, 'MONTO', column_header)
            worksheet.write(current_row, 8, 'SALDO', column_header)
            current_row += 1
            for account in accounts:
                for line in account['move_lines']:
                    if line['tipo_documento'] == 'EGRESO':
                        worksheet.write(current_row, 0, line.get('fecha_ingreso', ''), date_format)
                        worksheet.write(current_row, 1, line.get('nro_comprobante', ''), column_content)
                        worksheet.write(current_row, 2, line.get('medio_pago', ''), column_content)
                        worksheet.write(current_row, 3, line.get('nro_comprobante_pago', ''), column_content)
                        worksheet.write(current_row, 4, line.get('fecha_pago', ''), date_format)
                        worksheet.write(current_row, 5, line.get('glosa', ''), column_content)
                        worksheet.write(current_row, 6, line.get('beneficiario', ''), column_content)
                        worksheet.write_number(current_row, 7, line.get('egreso', 0), column_content_monetary)
                        worksheet.write_number(current_row, 8, line.get('saldo', 0), column_content_monetary)
                        current_row += 1
                worksheet.set_row(current_row, 30)
                worksheet.merge_range(current_row, 0, current_row, 2, '', cell_border_top_bottom_format_conc)
                worksheet.write(current_row, 3, 'Total Ingresos:', cell_border_top_bottom_format_conc)
                worksheet.write(current_row, 4, account['total_income'], cell_border_top_bottom_format_conc_money)
                worksheet.merge_range(current_row, 5, current_row, 6, '', cell_border_top_bottom_format_conc)
                worksheet.write(current_row, 7, 'Total Egresos: ', cell_border_top_bottom_format_conc)
                worksheet.write(current_row, 8, account['total_expenses'], cell_border_top_bottom_format_conc_money)
                current_row += 1
                worksheet.write(current_row, 7, 'Saldo Final:', cell_border_top_bottom_format_final)
                worksheet.write(current_row, 8, account['final_balance'], cell_border_top_bottom_format_final_money)


        elif p_data['x_document_type'] == 'BANCO' and p_data['x_report_type'] == 'cuenta_senainfo':
            worksheet.set_row(6, 30)
            worksheet.set_row(13, 30)
            worksheet.write('A1', current_date, base_format)
            worksheet.insert_image('A3', logo_path_adra, {'x_scale': 0.6, 'y_scale': 0.6})
            worksheet.write('B3', '                Agencia Adventista de Desarrollo y Recursos Asistenciales', base_format)
            worksheet.write('B4', '                RUT: 70051600-8', base_format)
            worksheet.write('F1', 'ADRA CHILE', base_format_align_right)
            worksheet.merge_range('A7:F7', x_document_type, movement_type_format)
            worksheet.write('J7', current_date_dmy, current_date_dmy_format)
            worksheet.merge_range('A10:B10', 'Programa:', base_format_bold)
            worksheet.merge_range('A11:C11', x_program_name, base_format)
            worksheet.merge_range('E10:F10', 'Ordenado por:', base_format_bold)
            worksheet.merge_range('E11:F11', x_sort_by, base_format)
            worksheet.merge_range('G10:H10', 'Fecha desde: ' + p_data['date_from'], base_format_bold)
            worksheet.merge_range('G11:H11', 'Fecha hasta: ' + p_data['date_to'], base_format_bold)
            worksheet.merge_range('I10:J10', 'Tipo de Reporte:', base_format_bold)
            worksheet.merge_range('I11:J11', x_report_type, base_format)
            worksheet.merge_range('A13:H13', '', cell_border_top_bottom_format)
            worksheet.write('I13', 'Saldo inicial: ', cell_border_top_bottom_format)
            for account in accounts:
                worksheet.write('J13', account['initial_balance'], cell_border_top_bottom_format_money)
            worksheet.write('A14', 'FECHA', column_header)
            worksheet.write('B14', 'N° COMP', column_header)
            worksheet.write('C14', 'FORMA DE PAGO', column_header)
            worksheet.write('D14', 'N° COMP PAGO', column_header)
            worksheet.write('E14', 'FECHA DE PAGO', column_header)
            worksheet.write('F14', 'GLOSA', column_header)
            worksheet.write('G14', 'BENEFICIARIO', column_header)
            worksheet.write('H14', 'INGRESO', column_header)
            worksheet.write('I14', 'EGRESO', column_header)
            worksheet.write('J14', 'SALDO', column_header)
            current_row = 14
            for account in accounts:
                for line in account['move_lines']:
                    worksheet.write(current_row, 0, line.get('fecha_ingreso', ''), date_format)
                    worksheet.write(current_row, 1, line.get('nro_comprobante', ''), column_content)
                    worksheet.write(current_row, 2, line.get('medio_pago', ''), column_content)
                    worksheet.write(current_row, 3, line.get('nro_comprobante_pago', ''), column_content)
                    worksheet.write(current_row, 4, line.get('fecha_pago', ''), date_format)
                    worksheet.write(current_row, 5, line.get('glosa', ''), column_content)
                    worksheet.write(current_row, 6, line.get('beneficiario', ''), column_content)
                    worksheet.write_number(current_row, 7, line.get('ingreso', 0), column_content_monetary)
                    worksheet.write_number(current_row, 8, line.get('egreso', 0), column_content_monetary)
                    worksheet.write_number(current_row, 9, line.get('saldo', 0), column_content_monetary)
                    current_row += 1

        if p_data['x_document_type'] == 'CONCILIACION':
            worksheet.set_row(6, 30)
            worksheet.write('A1', current_date, base_format)
            worksheet.insert_image('A3', logo_path_adra, {'x_scale': 0.6, 'y_scale': 0.6})
            worksheet.write('B3', '                Agencia Adventista de Desarrollo y Recursos Asistenciales', base_format)
            worksheet.write('B4', '                RUT: 70051600-8', base_format)
            worksheet.write('F1', 'ADRA CHILE', base_format_align_right)
            worksheet.merge_range('A7:F7', x_document_type, movement_type_format)
            worksheet.write('I7', current_date_dmy, current_date_dmy_format)
            worksheet.merge_range('A10:B10', 'Programa:', base_format_bold)
            worksheet.merge_range('A11:C11', x_program_name, base_format)
            worksheet.merge_range('D10:E10', 'Ordenado por:', base_format_bold)
            worksheet.merge_range('D11:E11', x_sort_by, base_format)
            worksheet.merge_range('F10:G10', 'Fecha desde: ' + p_data['date_from'], base_format_bold)
            worksheet.merge_range('F11:G11', 'Fecha hasta: ' + p_data['date_to'], base_format_bold)
            worksheet.merge_range('H10:I10', 'Tipo de Reporte:', base_format_bold)
            worksheet.merge_range('H11:I11', x_report_type, base_format)
            worksheet.set_column('D:D', 25)
            worksheet.set_column('E:E', 25)
            worksheet.set_row(13, 30)
            worksheet.set_row(14, 30)
            worksheet.set_row(15, 30)
            worksheet.set_row(16, 30)
            worksheet.set_row(17, 30)
            worksheet.set_row(18, 30)
            worksheet.set_row(19, 30)
            worksheet.set_row(20, 40)
            worksheet.set_row(21, 30)
            for account in accounts:
                worksheet.merge_range('A13:F13', '  SALDO INICIAL:', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G13:I13', account['initial_balance'], cell_border_top_bottom_format_align_right)
                worksheet.merge_range('A14:F14', '  TOTAL INGRESOS', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G14:I14', account['total_income'], cell_border_top_bottom_format_align_right)
                worksheet.merge_range('A15:F15', '  TOTAL EGRESOS', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G15:I15', account['total_expenses'], cell_border_top_bottom_format_align_right)
                worksheet.merge_range('A16:F16', '  CHEQUES GIRADOS NO PAGADOS:', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G16:I16', account['total_checks_drawn_uncharged'], cell_border_top_bottom_format_align_right)
                worksheet.merge_range('A17:F17', '  TOTAL CONCILIADO:', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G17:I17', account['reconciled_balance'], cell_border_top_bottom_format_align_right)
                worksheet.merge_range('A18:F18', '  SALDO FINAL:', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G18:I18', account['final_balance'], cell_border_top_bottom_format_align_right)
                worksheet.merge_range('A19:F19', '  SALDO FINAL CARTOLA BANCO:', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G19:I19', account['bank_final_balance'], cell_border_top_bottom_format_align_right)
                worksheet.merge_range('A20:F20', '  DIFERENCIA:', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G20:I20', account['difference'], cell_border_top_bottom_format_align_right)
            worksheet.merge_range('A21:E21', '  Detalle de Cheques Girados No Pagados:',
                                  cell_border_top_bottom_format_align_left)
            worksheet.write('A22', '', cell_border_top_bottom_format_conc)
            worksheet.write('B22', '', cell_border_top_bottom_format_conc)
            worksheet.write('C22', 'DOCUMENTO', cell_border_top_bottom_format_conc)
            worksheet.write('D22', 'N° CHEQUE', cell_border_top_bottom_format_conc)
            worksheet.write('E22', 'FECHA DE PAGO', cell_border_top_bottom_format_conc)
            worksheet.write('F22', 'BENEFICIARIO', cell_border_top_bottom_format_conc)
            worksheet.write('G22', 'REFERENCIA', cell_border_top_bottom_format_conc)
            worksheet.write('H22', 'MONTO', cell_border_top_bottom_format_conc)
            worksheet.write('I22', '', cell_border_top_bottom_format_conc)
            current_row = 22
            for account in accounts:
                for line in account['move_lines']:
                    worksheet.write(current_row, 2, line.get('documento', ''), column_content)
                    worksheet.write(current_row, 3, line.get('nro_cheque', ''), column_content)
                    worksheet.write(current_row, 4, line.get('fecha_pago', ''), date_format)
                    worksheet.write(current_row, 5, line.get('beneficiario', ''), column_content)
                    worksheet.write(current_row, 6, line.get('referencia', ''), column_content)
                    worksheet.write(current_row, 7, line.get('monto', ''), column_content_monetary)
                    current_row += 1
            current_row += 1
            worksheet.write(current_row, 7, 'Total:', cell_border_top_bottom_format_conc_total)
            for account in accounts:
                worksheet.write(current_row, 8,account['total_checks_drawn_uncharged'], cell_border_top_bottom_format_conc_money_no_borders)
            current_row += 6
            worksheet.merge_range(current_row, 0, current_row, 8, 'Firma Responsable Conciliación', cell_border_top_bottom_format_conc_total)
            current_row += 2
            worksheet.merge_range(current_row, 0, current_row, 8, ' NOTA: El saldo de la conciliación debe coincidir con los saldos del'
                                             ' libro banco y rendición de cuentas. En el evento de detectar alguna'
                                             ' diferencia, deberá ser regularizada en dicha Conciliación',
                                  base_format_center)

        if p_data['x_document_type'] == 'RENDICION':
            worksheet.set_row(6, 30)
            worksheet.set_row(14, 30)
            worksheet.set_row(15, 30)
            worksheet.set_row(16, 30)
            worksheet.set_row(17, 30)
            worksheet.set_row(18, 30)
            worksheet.set_row(19, 30)
            worksheet.write('A1', current_date, base_format)
            worksheet.insert_image('A3', logo_path_adra, {'x_scale': 0.6, 'y_scale': 0.6})
            worksheet.write('B3', '                Agencia Adventista de Desarrollo y Recursos Asistenciales', base_format)
            worksheet.write('B4', '                RUT: 70051600-8', base_format)
            worksheet.write('F1', 'ADRA CHILE', base_format_align_right)
            worksheet.merge_range('A7:F7', x_document_type, movement_type_format)
            worksheet.write('I7', current_date_dmy, current_date_dmy_format)
            worksheet.merge_range('A10:B10', 'Programa:', base_format_bold)
            worksheet.merge_range('A11:C11', x_program_name, base_format)
            worksheet.merge_range('D10:E10', 'Ordenado por:', base_format_bold)
            worksheet.merge_range('D11:E11', x_sort_by, base_format)
            worksheet.merge_range('F10:G10', 'Fecha desde: ' + p_data['date_from'], base_format_bold)
            worksheet.merge_range('F11:G11', 'Fecha hasta: ' + p_data['date_to'], base_format_bold)
            worksheet.merge_range('H10:I10', 'Tipo de Reporte:', base_format_bold)
            worksheet.merge_range('H11:I11', x_report_type, base_format)
            indent = '    '
            for account in accounts:
                worksheet.merge_range('A13:F13', 'SALDO INICIAL:', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G13:I13', account['initial_balance'], cell_border_top_bottom_format_align_right)
                worksheet.merge_range('A14:F14', 'INGRESOS DEL PERIODO:', cell_border_top_bottom_format_align_left)
                worksheet.merge_range('G14:I14', account['total_income_from_period'], cell_border_top_bottom_format_align_right)
                current_row = 14
                for line in account['move_lines_income']:
                    worksheet.merge_range(current_row, 0, current_row, 5, line['cuenta_senainfo'], cell_border_top_bottom_format_align_left)
                    worksheet.merge_range(current_row, 6, current_row, 8, line['total'], cell_border_top_bottom_format_align_right)
                    current_row += 1
                worksheet.merge_range(current_row, 0, current_row, 5, 'TOTAL INGRESOS (Saldo Inicial + Ingresos del Periodo):', cell_border_top_bottom_format_align_left)
                worksheet.merge_range(current_row, 6, current_row, 8, account['total_income'], cell_border_top_bottom_format_align_right)
                current_row += 1
                worksheet.merge_range(current_row, 0, current_row, 5, 'EGRESOS DEL PERIODO', cell_border_top_bottom_format_little_align_left)
                worksheet.merge_range(current_row, 6, current_row, 8, account['total_expenses_from_period'], cell_border_top_bottom_format_little_align_right)
                current_row += 1
                for line in account['move_lines_expenses']:
                    worksheet.merge_range(current_row, 0, current_row, 5, indent+line['cuenta_senainfo'], cell_border_top_bottom_format_little_align_left)
                    worksheet.merge_range(current_row, 6, current_row, 8, line['total'], cell_border_top_bottom_format_little_align_right)
                    current_row += 1
                worksheet.merge_range(current_row, 0, current_row, 5, 'SALDO FINAL:', cell_border_top_bottom_format_align_left)
                worksheet.merge_range(current_row, 6, current_row, 8, account['final_balance'], cell_border_top_bottom_format_align_right)

            worksheet.merge_range('B22:C22', 'Representante OCA:', base_format_bold)
            worksheet.write('E22', 'Firma:', base_format_bold)
            worksheet.write('F22', 'Timbre:', base_format_bold_align_right)
            worksheet.write('H22', 'Fecha de presentación:', base_format_bold_align_right)


            workbook.close()

    @api.model
    def _get_objs_for_report(self, docids, data):
        reportData = self.env['report.general.ledger.data']
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids', []))
        # init_balance = data['form'].get('initial_balance', True)
        # sortby = data['form'].get('sortby', 'sort_date')
        # display_account = data['form']['display_account']
        # x_account_analytic_account_id = data['form']['x_account_analytic_account_id']
        x_account_analytic_account_id = data['form'].get('x_account_analytic_account_id', 'project_id')
        x_sort_by = data['form'].get('x_sort_by', 'sort_date')
        x_report_type = data['form'].get('x_report_type', 'adra_type')
        x_document_type = data['form'].get('x_document_type', 'document_type')
        x_bank_final_balance = data['form'].get('x_bank_final_balance', 'bank_final_balance')
        x_report_version = data['form'].get('x_report_version', 'new')
        codes = []
        if data['form'].get('journal_ids', False):
            codes = [journal.code for journal in
                     self.env['account.journal'].search([('id', 'in', data['form']['journal_ids'])])]

        accounts = docs if model == 'account.account' else self.env['account.account'].search([])

        if x_report_version == "new":
            if x_document_type in ['INGRESO', 'EGRESO']:
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_mayor_ledger_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
            elif x_document_type == 'BANCO':
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_bank_ledger_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
            elif x_document_type == 'CONCILIACION':
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_bank_reconciliation_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_bank_final_balance)
            elif x_document_type == 'RENDICION':
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_accountability_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
        else:
            if x_document_type in ['INGRESO', 'EGRESO']:
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_mayor_ledger_entries(
                    accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
            elif x_document_type == 'BANCO':
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_bank_ledger_entries_old(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
            elif x_document_type == 'CONCILIACION':
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_bank_reconciliation_entries_old(accounts, x_account_analytic_account_id[0], x_sort_by, x_bank_final_balance)
            elif x_document_type == 'RENDICION':
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_accountability_entries_old(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
        data = {
            'doc_ids': docids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': accounts_res,
            'print_journal': codes,
        }

        return data