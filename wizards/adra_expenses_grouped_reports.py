from flectra.exceptions import UserError

from flectra import fields, models
class AdraExpensesGroupedReports(models.TransientModel):
    _name = 'adra.expenses.grouped.reports'
    _description = 'Generador de Reportes de Gastos Agrupados.'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Seleccione un proyecto')
    x_date_from = fields.Date(string='Año')

    def generate_excel_report(self):
        if not self.x_account_analytic_account_id:
            raise UserError("Por favor, asegúrese de seleccionar un proyecto para el informe.")
        if not self.x_date_from:
            raise UserError("Por favor, asegúrese de seleccionar el año.")
        data = {
            'x_account_analytic_account_id': self.x_account_analytic_account_id.id,
            'x_project': self.x_account_analytic_account_id.name,
            'x_date_from': self.x_date_from
        }
        report = self.env.ref('adra_account_extended.report_xlsx_expenses_grouped')
        return report.report_action(self, data=data)