from flectra import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # x_account_group_id = fields.Many2one('account.group', string='Tipo de Cuenta', store=True)
