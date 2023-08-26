from flectra.exceptions import UserError

from flectra import fields, models
class AdraExpensesGroupedReports(models.TransientModel):
    _name = 'adra.expenses.grouped.reports'
    _description = 'Generador de Reportes de Gastos Agrupados.'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Seleccione un proyecto')
    x_date_from = fields.Date(string='Desde')
    x_date_to = fields.Date(string='Hasta')

    def generate_excel_report(self):
        if not self.x_account_analytic_account_id:
            raise UserError("Por favor, asegúrese de seleccionar un proyecto para el informe.")
        if not self.x_date_from and not self.x_date_to:
            raise UserError("Por favor, asegúrese de seleccionar tanto la fecha de inicio como la fecha de término para el informe.")
        if not self.x_date_from:
            raise UserError("Por favor, asegúrese de seleccionar la fecha de inicio para el informe.")
        if not self.x_date_to:
            raise UserError("Por favor, asegúrese de seleccionar la fecha de término para el informe.")
        data = {
            'x_account_analytic_account_id': self.x_account_analytic_account_id.id,
            'x_project': self.x_account_analytic_account_id.name,
            'x_date_from': self.x_date_from,
            'x_date_to': self.x_date_to
        }
        report = self.env.ref('adra_account_extended.report_xlsx_expenses_grouped')
        return report.report_action(self, data=data)