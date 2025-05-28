import os
from flectra import models

class ReportXlsDj1945(models.AbstractModel):
    _name = 'report.adra_account_extended.report_xlsx_dj1945'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        worksheet = workbook.add_worksheet("Report")

        x_date_from = data.get('x_date_from')
        x_date_to = data.get('x_date_to')

        reportData = self.env['report.general.ledger.data']
        move_lines = reportData._get_DJ1945_data(x_date_from, x_date_to, '2025-04-30')


        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 11.86)
        worksheet.set_column('C:C', 83.86)
        worksheet.set_column('D:D', 7.29)
        worksheet.set_column('E:E', 14)
        worksheet.set_column('F:F', 13.86)
        worksheet.set_column('G:G', 13)
        worksheet.set_column('H:H', 12)
        worksheet.set_column('I:I', 11.29)
        worksheet.set_column('J:J', 18)
        worksheet.set_column('K:K', 34)
        worksheet.set_column('L:L', 16.71)
        worksheet.set_column('M:M', 13.57)
        worksheet.set_column('N:N', 14.71)

        worksheet.write('A1', 'tipo_seccion')
        worksheet.write('B1', 'rut')
        worksheet.write('C1', 'nombre')
        worksheet.write('D1', 'pais')
        worksheet.write('E1', 'tipo_ing_egr')
        worksheet.write('F1', 'origen_ing')
        worksheet.write('G1', 'destino_egr')
        worksheet.write('H1', 'tipo_relacion')
        worksheet.write('I1', 'monto')
        worksheet.write('J1', 'lote')
        worksheet.write('K1', 'tipo_n_ing_egr')
        worksheet.write('L1', 'origen_n_ing')
        worksheet.write('M1', 'destino_n_egr')
        worksheet.write('N1', 'tipo_n_relacion')

        current_row = 1
        index = 0

        for line in move_lines:
            index += 1
            worksheet.write(current_row, 0, 1)
            worksheet.write(current_row, 1, line['rut'])
            worksheet.write(current_row, 2, line['beneficiario'])
            worksheet.write(current_row, 8, line['total'])
            worksheet.write(current_row, 9, index)
            current_row += 1

        workbook.close()