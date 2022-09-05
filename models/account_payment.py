from flectra import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Proyecto', store=True)
    x_name = fields.Char(string='Glosa', store=True);
    x_income_document_number = fields.Char(string='Nº Doc. Ingreso', store=True, index=True);
    x_is_charged = fields.Boolean(default=True, string='Cobrado?')

    _sql_constraints = [
        ('x_income_document_number', 'unique (x_income_document_number, payment_method_id, payment_type)', 'El Nº de documento debe ser único por método de pago!')
    ]
