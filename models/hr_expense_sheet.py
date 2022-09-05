# -*- coding: utf-8 -*-

from flectra import models, fields


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Proyecto', store=True, index=True)
    x_name = fields.Char(related='account_move_id.x_name')
    x_correlative = fields.Integer(related='account_move_id.x_correlative');
    x_invoice_date = fields.Date(string='Fecha de Ingreso', readonly=True, index=True, copy=False, states={'draft': [('readonly', False)]})
