from flectra.exceptions import UserError

from flectra import fields, models

class AdraDj1945Reports(models.TransientModel):
    _name = 'adra.dj1945.reports'
    _description = 'Generador de Reportes en Excel para Dj1945.'

    x_date_from = fields.Date(string='Desde')
    x_date_to = fields.Date(string='Hasta')

    def generate_excel_report(self):
        if not self.x_date_from and not self.x_date_to:
            raise UserError("Por favor, asegúrese de seleccionar tanto la fecha de inicio como la fecha de término para el informe.")
        if not self.x_date_from:
            raise UserError("Por favor, asegúrese de seleccionar la fecha de inicio para el informe.")
        if not self.x_date_to:
            raise UserError("Por favor, asegúrese de seleccionar la fecha de término para el informe.")
        data = {'x_date_from': self.x_date_from,
                'x_date_to': self.x_date_to
                }
        report = self.env.ref('adra_account_extended.report_xlsx_dj1945')
        return report.report_action(self, data=data)