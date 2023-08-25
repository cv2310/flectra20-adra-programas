import os
from flectra import models
import datetime

class ReportXls(models.AbstractModel):
    _name = 'report.adra_account_extended.report_xlsx_assets'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        project_code = data.get('project_code')
        projects_quantity = data.get('projects_quantity')
        x_status_active = data.get('x_status_active')
        sort_by = data.get('sort_by')
        date_from = data.get('x_date_from')

        worksheet = workbook.add_worksheet("Report")
        pro_search = None
        act_search = None
        search = []
        if data['x_date_from']:
            ano, mes, dia = map(int, data['x_date_from'].split('-'))
            date_from = datetime.date(ano, mes, dia)
            dfrom_search = ('date', '>=', date_from)
            search.append(dfrom_search)
        if data['x_date_to']:
            ano, mes, dia = map(int, data['x_date_to'].split('-'))
            date_to = datetime.date(ano, mes, dia)
            dto_search = ('date', '<=', date_to)
            search.append(dto_search)
        if projects_quantity == 'one':
            pro_search = ('x_account_analytic_account_id', '=', project_code)
            search.append(pro_search)
        if x_status_active != 'general':
            act_search = ('x_status_active', '=', x_status_active)
            search.append(act_search)

        # if pro_search and  act_search:
        #     asset_records = self.env['account.asset.asset'].search([pro_search,act_search])
        # elif pro_search and  act_search:
        #     asset_records = self.env['account.asset.asset'].search([pro_search,act_search])
        # elif act_search:
        #     asset_records = self.env['account.asset.asset'].search([act_search])
        # elif pro_search:
        #     asset_records = self.env['account.asset.asset'].search([pro_search])
        # else:
        #     asset_records = self.env['account.asset.asset'].search([])
        asset_records = self.env['account.asset.asset'].search(search)
        if sort_by == 'fecha_ingreso':
            asset_records = sorted(asset_records, key=lambda r: (r.date))
        elif sort_by == 'proyecto_fecha':
            asset_records = sorted(asset_records, key=lambda r: (r.x_account_analytic_account_id.name, r.date))
        else:
            asset_records = sorted(asset_records, key=lambda r:  (r.date, r.x_account_analytic_account_id.name))

        date_format = workbook.add_format(
            {'num_format': 'dd/mm/yyyy', 'font_name': 'Calibri', 'font_size': 8, 'align': 'center', 'border': 1,
             'valign': 'vcenter',
             'text_wrap': True})

        number_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'align': 'center', 'border': 1, 'valign': 'vcenter',
             'text_wrap': True, 'num_format': 'General'})

        number_format_with_comma = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'align': 'center', 'border': 1, 'valign': 'vcenter',
             'text_wrap': True, 'num_format': '#,##0'})

        cell_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'border': 1, 'align': 'center', 'valign': 'vcenter',
             'text_wrap': True})

        if projects_quantity == 'all':
            self.all_projects_header(workbook, worksheet, data)
            index_ap = 1

        else:
            self.project_header(workbook, worksheet, data)
            index_ap = 0

        row = 9
        for asset in asset_records:
            worksheet.write(row, 0, asset.date if asset.date else "-", date_format)
            if projects_quantity == 'all':
                worksheet.write(row, 1,
                                asset.x_account_analytic_account_id.name if asset.x_account_analytic_account_id.name
                                else "-", cell_format)
            worksheet.write(row, 1 + index_ap, asset.code if asset.code else "-", number_format)
            worksheet.write(row, 2 + index_ap, asset.x_floor if asset.x_floor else "-", number_format)
            worksheet.write(row, 3 + index_ap, asset.x_office_number if asset.x_office_number else "-", number_format)
            worksheet.write(row, 4 + index_ap, asset.name if asset.name else "-", cell_format)
            worksheet.write(row, 5 + index_ap, asset.x_quantity if asset.x_quantity else "-", cell_format)
            worksheet.write(row, 6 + index_ap, asset.x_type_measure if asset.x_type_measure else "-", cell_format)
            brand = str(asset.x_brand) if asset.x_brand else ''
            model = str(asset.x_model) if asset.x_model else ''
            brand_model = brand + ', ' + model if brand or model else "-"
            worksheet.write(row, 7 + index_ap, brand_model, cell_format)
            worksheet.write(row, 8 + index_ap, asset.x_color if asset.x_color else "-", cell_format)
            worksheet.write(row, 9 + index_ap, asset.x_procedence if asset.x_procedence else "-", cell_format)
            worksheet.write(row, 10 + index_ap, asset.x_expense_number if asset.x_expense_number else "-",
                            number_format)
            worksheet.write(row, 11 + index_ap, asset.x_invoice_number if asset.x_invoice_number else "-",
                            number_format)
            worksheet.write(row, 12 + index_ap, asset.x_expense_date if asset.x_expense_date else "-", date_format)
            worksheet.write(row, 13 + index_ap,
                            asset.x_transfer_record_number if asset.x_transfer_record_number else "-",
                            cell_format)
            worksheet.write(row, 14 + index_ap, asset.x_location if asset.x_location else "-", cell_format)
            worksheet.write(row, 15 + index_ap,
                            asset.x_inventory_unsubscribe_number if asset.x_inventory_unsubscribe_number else "-",
                            cell_format)
            worksheet.write(row, 16 + index_ap, asset.x_quantity_unsubscribe if asset.x_quantity_unsubscribe else "-",
                            number_format)
            worksheet.write(row, 17 + index_ap, asset.x_status if asset.x_status else "-", cell_format)
            worksheet.write(row, 18 + index_ap, asset.x_description if asset.x_description else "-", cell_format)
            worksheet.write(row, 19 + index_ap, asset.value if asset.value else "-", number_format_with_comma)
            worksheet.write(row, 20 + index_ap, asset.x_used_by if asset.x_used_by else "-", cell_format)

            row += 1

        workbook.close()

    def project_header(self, workbook, worksheet, data):
        project_name = data.get('project_name')
        project_code = data.get('project_code')
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path_adra = os.path.join(module_path, 'static', 'src', 'img', 'logo_adra.jpg')
        logo_path_mejornines = os.path.join(module_path, 'static', 'src', 'img', 'mejor_niñez.jpg')

        border_right_format = workbook.add_format({'right': 1})
        worksheet.conditional_format('U1:U6', {'type': 'formula', 'criteria': 'TRUE', 'format': border_right_format})
        border_right_format_u7 = workbook.add_format({'right': 1, 'bottom': 1})
        worksheet.conditional_format('U7', {'type': 'formula', 'criteria': 'TRUE', 'format': border_right_format_u7})

        title_format = workbook.add_format(
            {'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': 'center', 'valign': 'vcenter',
             'text_wrap': True})
        adra_format = workbook.add_format(
            {'font_name': 'Times New Roman', 'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter',
             'text_wrap': True})
        project_info_format_left = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'bold': True, 'align': 'left', 'valign': 'vcenter',
             'text_wrap': True})
        project_info_format_bordered = workbook.add_format(
            {'font_size': 10, 'bold': True, 'align': 'center', 'bottom': True, 'top': True, 'valign': 'vcenter',
             'text_wrap': True})

        worksheet.set_column('A:A', 9.43)
        worksheet.set_column('B:B', 7.14)
        worksheet.set_column('C:C', 6.86, )
        worksheet.set_column('D:D', 10.14, )
        worksheet.set_column('E:E', 17.14, )
        worksheet.set_column('F:F', 1.86, )
        worksheet.set_column('G:G', 5.29, )
        worksheet.set_column('H:H', 47.57, )
        worksheet.set_column('I:I', 8.14, )
        worksheet.set_column('J:J', 16.71, )
        worksheet.set_column('K:K', 3.86, )
        worksheet.set_column('L:L', 16.57, )
        worksheet.set_column('M:M', 9.57, )
        worksheet.set_column('N:N', 14.57, )
        worksheet.set_column('O:O', 13.86, )
        worksheet.set_column('P:P', 18.86, )
        worksheet.set_column('Q:Q', 8.29, )
        worksheet.set_column('R:R', 7.29, )
        worksheet.set_column('S:S', 13.86, )
        worksheet.set_column('T:T', 8, )
        worksheet.set_column('U:U', 11.43, )

        worksheet.set_row(3, 24.75)
        worksheet.set_row(7, 21.75)
        worksheet.set_row(8, 22.5)

        worksheet.merge_range('A1:U1', 'I N V E N T A R I O', title_format)

        worksheet.merge_range('A4:B4', 'ADRA CHILE', adra_format)
        worksheet.insert_image('C3', logo_path_adra)
        worksheet.insert_image('R2', logo_path_mejornines)
        worksheet.write('H3', f'NOMBRE PROYECTO: {project_name}', project_info_format_left)
        worksheet.write('H4', f'CÓDIGO PROYECTO: {project_code}', project_info_format_left)
        worksheet.write('H5', 'INSTITUCIÓN:', project_info_format_left)
        worksheet.merge_range('I3:L3', '   FAE MARGA MARGA 1', project_info_format_bordered)
        worksheet.merge_range('I4:L4', '   1051416', project_info_format_bordered)
        worksheet.merge_range('I5:L5', '   AGENCIA ADVENTISTA Y DESARROLLO', project_info_format_bordered)

        header_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'bold': True, 'align': 'center', 'border': 1,
             'bg_color': '#D9D9D9', 'valign': 'vcenter', 'text_wrap': True})
        worksheet.merge_range('A8:A9', 'Fecha', header_format)
        worksheet.merge_range('B8:B9', 'Código de Inventario', header_format)
        worksheet.merge_range('C8:C9', 'Piso', header_format)
        worksheet.merge_range('D8:D9', 'N° Oficina', header_format)
        worksheet.merge_range('E8:E9', 'Bien', header_format)
        worksheet.merge_range('F8:G8', 'Unidades', header_format)
        worksheet.merge_range('H8:I8', 'Identificación', header_format)
        worksheet.merge_range('J8:J9', 'Procedencia (Subvención/Traspaso/Fundación):', header_format)
        worksheet.merge_range('K8:M8', 'Comp. Egreso', header_format)
        worksheet.merge_range('N8:N9', 'Numero de Acta de Traspaso (A) o Resolución Exenta ( R ) /Año:', header_format)
        worksheet.merge_range('O8:O9', 'Ubicación especie', header_format)
        worksheet.merge_range('P8:P9', 'Baja de Inventario: Nº de Acta/Año', header_format)
        worksheet.merge_range('Q8:Q9', 'Cantidad dada de Baja:', header_format)
        worksheet.merge_range('R8:R9', 'Estado', header_format)
        worksheet.merge_range('S8:S9', 'Observaciones', header_format)
        worksheet.merge_range('T8:T9', 'Valor $', header_format)
        worksheet.merge_range('U8:U9', 'Utilizado por', header_format)

        subheader_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'bold': True, 'align': 'center', 'border': 1,
             'bg_color': '#D9D9D9', 'valign': 'vcenter', 'text_wrap': True})
        worksheet.write('F9', 'Nº', subheader_format)
        worksheet.write('G9', 'Tipo Med.', subheader_format)
        worksheet.write('H9', 'Marca-Especificaciones', subheader_format)
        worksheet.write('I9', 'Color', subheader_format)
        worksheet.write('K9', 'Nº', subheader_format)
        worksheet.write('L9', 'N° Factura', subheader_format)
        worksheet.write('M9', 'Fecha egr.', subheader_format)

    def all_projects_header(self, workbook, worksheet, data):
        projects_quantity = data.get('projects_quantity')
        project_name = data.get('project_name')
        project_code = data.get('project_code')
        if projects_quantity == 'all':
            project_name = 'TODOS LOS PROYECTOS'
            project_code = 'TODOS LOS CÓDIGOS INVOLUCRADOS'
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path_adra = os.path.join(module_path, 'static', 'src', 'img', 'logo_adra.jpg')
        logo_path_mejornines = os.path.join(module_path, 'static', 'src', 'img', 'mejor_niñez.jpg')

        border_right_format = workbook.add_format({'right': 1})
        worksheet.conditional_format('V1:V6', {'type': 'formula', 'criteria': 'TRUE', 'format': border_right_format})
        border_right_format_u7 = workbook.add_format({'right': 1, 'bottom': 1})
        worksheet.conditional_format('V7', {'type': 'formula', 'criteria': 'TRUE', 'format': border_right_format_u7})

        title_format = workbook.add_format(
            {'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': 'center', 'valign': 'vcenter',
             'text_wrap': True})
        adra_format = workbook.add_format(
            {'font_name': 'Times New Roman', 'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter',
             'text_wrap': True})
        project_info_format_left = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'bold': True, 'align': 'left', 'valign': 'vcenter',
             'text_wrap': True})
        project_info_format_bordered = workbook.add_format(
            {'font_size': 10, 'bold': True, 'align': 'center', 'bottom': True, 'top': True, 'valign': 'vcenter',
             'text_wrap': True})

        worksheet.set_column('A:A', 9.43)
        worksheet.set_column('B:B', 30.14)
        worksheet.set_column('C:C', 7.14)
        worksheet.set_column('D:D', 6.86, )
        worksheet.set_column('E:E', 10.14, )
        worksheet.set_column('F:F', 17.14, )
        worksheet.set_column('G:G', 1.86, )
        worksheet.set_column('H:H', 5.29, )
        worksheet.set_column('I:I', 40.57, )
        worksheet.set_column('J:J', 8.14, )
        worksheet.set_column('K:K', 16.71, )
        worksheet.set_column('L:L', 3.86, )
        worksheet.set_column('K:M', 16.57, )
        worksheet.set_column('N:N', 9.57, )
        worksheet.set_column('O:O', 14.57, )
        worksheet.set_column('P:P', 13.86, )
        worksheet.set_column('Q:Q', 18.86, )
        worksheet.set_column('R:R', 8.29, )
        worksheet.set_column('S:S', 7.29, )
        worksheet.set_column('T:T', 13.86, )
        worksheet.set_column('U:U', 8, )
        worksheet.set_column('V:V', 11.43, )

        worksheet.set_row(3, 24.75)
        worksheet.set_row(7, 21.75)
        worksheet.set_row(8, 22.5)

        worksheet.merge_range('A1:V1', 'I N V E N T A R I O', title_format)

        worksheet.write('A4', 'ADRA CHILE', adra_format)
        worksheet.insert_image('B3', logo_path_adra)
        worksheet.insert_image('T2', logo_path_mejornines)
        worksheet.merge_range('C3:F3', f'NOMBRE PROYECTO: {project_name}', project_info_format_left)
        worksheet.merge_range('C4:F4', f'CÓDIGO PROYECTO: {project_code}', project_info_format_left)
        worksheet.merge_range('C5:F5', 'INSTITUCIÓN:', project_info_format_left)
        worksheet.merge_range('I3:N3', '                   FAE MARGA MARGA 1', project_info_format_bordered)
        worksheet.merge_range('I4:N4', '                   1051416', project_info_format_bordered)
        worksheet.merge_range('I5:N5', '                   AGENCIA ADVENTISTA Y DESARROLLO',
                              project_info_format_bordered)

        header_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'bold': True, 'align': 'center', 'border': 1,
             'bg_color': '#D9D9D9', 'valign': 'vcenter', 'text_wrap': True})
        worksheet.merge_range('A8:A9', 'Fecha', header_format)
        worksheet.merge_range('B8:B9', 'Proyecto', header_format)
        worksheet.merge_range('C8:C9', 'Código de Inventario', header_format)
        worksheet.merge_range('D8:D9', 'Piso', header_format)
        worksheet.merge_range('E8:E9', 'N° Oficina', header_format)
        worksheet.merge_range('F8:F9', 'Bien', header_format)
        worksheet.merge_range('G8:H8', 'Unidades', header_format)
        worksheet.merge_range('I8:J8', 'Identificación', header_format)
        worksheet.merge_range('K8:K9', 'Procedencia (Subvención/Traspaso/Fundación):', header_format)
        worksheet.merge_range('L8:N8', 'Comp. Egreso', header_format)
        worksheet.merge_range('O8:O9', 'Numero de Acta de Traspaso (A) o Resolución Exenta ( R ) /Año:', header_format)
        worksheet.merge_range('P8:P9', 'Ubicación especie', header_format)
        worksheet.merge_range('Q8:Q9', 'Baja de Inventario: Nº de Acta/Año', header_format)
        worksheet.merge_range('R8:R9', 'Cantidad dada de Baja:', header_format)
        worksheet.merge_range('S8:S9', 'Estado', header_format)
        worksheet.merge_range('T8:T9', 'Observaciones', header_format)
        worksheet.merge_range('U8:U9', 'Valor $', header_format)
        worksheet.merge_range('V8:V9', 'Utilizado por', header_format)

        subheader_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'bold': True, 'align': 'center', 'border': 1,
             'bg_color': '#D9D9D9', 'valign': 'vcenter', 'text_wrap': True})
        worksheet.write('G9', 'Nº', subheader_format)
        worksheet.write('H9', 'Tipo Med.', subheader_format)
        worksheet.write('I9', 'Marca-Especificaciones', subheader_format)
        worksheet.write('J9', 'Color', subheader_format)
        worksheet.write('L9', 'Nº', subheader_format)
        worksheet.write('M9', 'N° Factura', subheader_format)
        worksheet.write('N9', 'Fecha egr.', subheader_format)
