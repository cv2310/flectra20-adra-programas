from flectra.exceptions import UserError

from flectra import fields, models
class AdraQuarterlyReports(models.TransientModel):
    _name = 'adra.quarterly.reports'
    _description = 'Generador de Reportes trimestrales en Excel.'

    x_date = fields.Date(string='Seleccione una fecha')

    def generate_excel_report(self):
        if not self.x_date:
            raise UserError("Por favor, asegúrese de seleccionar la fecha para el informe.")
        data = {'x_date': self.x_date}
        report = self.env.ref('adra_account_extended.report_xlsx_quarterly')
        return report.report_action(self, data=data)