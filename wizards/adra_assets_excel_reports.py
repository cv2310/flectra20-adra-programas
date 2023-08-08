import base64
import os
from datetime import datetime

from flectra.exceptions import UserError
from flectra import fields, models, _

class AdraAssetsExcelReports(models.TransientModel):
    _name = 'adra.assets.excel.reports'
    _description = 'Generador de Reportes en Excel para activos.'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Seleccione un proyecto')


    def print_report(self):
        # Obtener el proyecto seleccionado desde el formulario
        proyecto = self.x_account_analytic_account_id

        # Verificar si se seleccionó un proyecto antes de generar el informe
        if not proyecto:
            raise UserError(_("Debe seleccionar un proyecto."))

        # Construir el diccionario de datos para pasar al informe
        data = {
            'proyecto_name': proyecto.name,
            'proyecto_code' : proyecto.code

        }
        report = self.env.ref('adra_account_extended.report_xlsx_assets')
        return report.report_action(self, data)

    def cancel_report(self):
        # Agregar la lógica para cancelar el informe aquí
        pass

class ReportXls(models.AbstractModel):
    _name = 'report.adra_account_extended.report_xlsx_assets'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, objs):
        proyecto_name = data.get('proyecto_name')
        proyecto_code = data.get('proyecto_code')

        worksheet = workbook.add_worksheet("Report")
        # Obtener la ruta del módulo actual (adra_account_extended)
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Construir la ruta completa a los logos
        logo_path_adra = os.path.join(module_path, 'static', 'src', 'img', 'logo_adra.jpg')
        logo_path_mejornines = os.path.join(module_path, 'static', 'src', 'img', 'mejor_niñez.jpg')

        # Obtener los datos de los activos
        asset_records = self.env['account.asset.asset'].search([
            ('x_account_analytic_account_id', '=', proyecto_name)
        ])

        # Definir el formato de fecha que deseas mostrar en Excel
        date_format = workbook.add_format(
            {'num_format': 'dd/mm/yyyy', 'font_name': 'Calibri', 'font_size': 8, 'align': 'center', 'border': 1,
             'valign': 'vcenter',
             'text_wrap': True})

        # Establecer el formato de fuente para los números
        number_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'align': 'center', 'border': 1, 'valign': 'vcenter',
             'text_wrap': True, 'num_format': 'General'})

        # Establecer el formato de fuente para los números con separador de miles como punto
        number_format_with_comma = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'align': 'center', 'border': 1, 'valign': 'vcenter',
             'text_wrap': True, 'num_format': '#,##0'})

        # Establecer el formato de fuente para toda la tabla
        cell_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'border': 1, 'align': 'center', 'valign': 'vcenter',
             'text_wrap': True})

        # Establecer el formato para el borde derecho y abordar ultima celda aplicando borde inferior
        border_right_format = workbook.add_format({'right': 1})
        format_without_border = workbook.add_format({'border': 0})
        worksheet.conditional_format('U1:U6', {'type': 'formula', 'criteria': 'TRUE', 'format': border_right_format})
        border_right_format_u7 = workbook.add_format({'right': 1, 'bottom': 1})
        worksheet.conditional_format('U7', {'type': 'formula', 'criteria': 'TRUE', 'format': border_right_format_u7})

        # Establecer formatos especiales para el encabezado
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

        # Establecer el ancho de las columnas
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

        # Establecer el alto de las filas
        worksheet.set_row(3, 24.75)
        worksheet.set_row(7, 21.75)
        worksheet.set_row(8, 22.5)

        # Título "INVENTARIO"
        worksheet.merge_range('A1:U1', 'I N V E N T A R I O', title_format)

        # Insertar los logos y texto en el encabezado
        worksheet.merge_range('A4:B4', 'ADRA CHILE', adra_format)
        worksheet.insert_image('C3', logo_path_adra)
        worksheet.insert_image('R2', logo_path_mejornines)
        worksheet.write('H3', f'NOMBRE PROYECTO: {proyecto_name}', project_info_format_left)
        worksheet.write('H4', f'CÓDIGO PROYECTO: {proyecto_code}', project_info_format_left)
        worksheet.write('H5', 'INSTITUCIÓN:', project_info_format_left)
        worksheet.merge_range('I3:L3', '   FAE MARGA MARGA 1', project_info_format_bordered)
        worksheet.merge_range('I4:L4', '   1051416', project_info_format_bordered)
        worksheet.merge_range('I5:L5', '   AGENCIA ADVENTISTA Y DESARROLLO', project_info_format_bordered)

        # Escribir los nombres de las columnas en negrita
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

        # Escribir los nombres de las subcolumnas en negrita en la fila 9
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

        # Insertar datos a partir de la línea 10
        row = 9
        for asset in asset_records:
            worksheet.write(row, 0, asset.date if asset.date else "-", date_format)
            worksheet.write(row, 1, asset.code if asset.code else "-", number_format)
            worksheet.write(row, 2, asset.x_floor if asset.x_floor else "-", number_format)
            worksheet.write(row, 3, asset.x_office_number if asset.x_office_number else "-", number_format)
            worksheet.write(row, 4, asset.name if asset.name else "-", cell_format)
            worksheet.write(row, 5, asset.x_quantity if asset.x_quantity else "-", cell_format)
            worksheet.write(row, 6, asset.x_type_measure if asset.x_type_measure else "-", cell_format)
            brand = str(asset.x_brand) if asset.x_brand else ''
            model = str(asset.x_model) if asset.x_model else ''
            brand_model = brand + ', ' + model if brand or model else "-"
            worksheet.write(row, 7, brand_model, cell_format)
            worksheet.write(row, 8, asset.x_color if asset.x_color else "-", cell_format)
            worksheet.write(row, 9, asset.x_procedence if asset.x_procedence else "-", cell_format)
            worksheet.write(row, 10, asset.x_expense_number if asset.x_expense_number else "-", number_format)
            worksheet.write(row, 11, asset.x_invoice_number if asset.x_invoice_number else "-", number_format)
            worksheet.write(row, 12, asset.x_expense_date if asset.x_expense_date else "-", date_format)
            worksheet.write(row, 13, asset.x_transfer_record_number if asset.x_transfer_record_number else "-",
                            cell_format)
            worksheet.write(row, 14, asset.x_location if asset.x_location else "-", cell_format)
            worksheet.write(row, 15,
                            asset.x_inventory_unsubscribe_number if asset.x_inventory_unsubscribe_number else "-",
                            cell_format)
            worksheet.write(row, 16, asset.x_quantity_unsubscribe if asset.x_quantity_unsubscribe else "-",
                            number_format)
            worksheet.write(row, 17, asset.x_status if asset.x_status else "-", cell_format)
            worksheet.write(row, 18, asset.x_description if asset.x_description else "-", cell_format)
            worksheet.write(row, 19, asset.value if asset.value else "-", number_format_with_comma)
            worksheet.write(row, 20, asset.x_used_by if asset.x_used_by else "-", cell_format)

            row += 1


        workbook.close()

