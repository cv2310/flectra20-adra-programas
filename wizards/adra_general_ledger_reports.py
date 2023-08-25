from datetime import datetime
from flectra import fields, models

class AdraGeneralLedgerXlsReports(models.TransientModel):
    _name = 'adra.general.ledger.xls.reports'
    _description = 'Generador de Reportes en Excel para Libro Mayor.'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Seleccione un proyecto')
    x_document_type = fields.Selection([('CONCILIACION', 'Conciliación'), ('BANCO', 'Banco'), ('RENDICION', 'Rendicion')],
                                 string='Tipo de docuemnto', required=True)

    def generate_excel_report(self):
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_date_dmy = datetime.now().strftime('%d-%m-%Y')
        data = {'current_date': current_date,
                'current_date_dmy': current_date_dmy,
                'x_document_type': self.x_document_type
                }

        report = self.env.ref('adra_account_extended.report_xlsx_general_ledger')
        return report.report_action(self, data=data)