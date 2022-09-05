# -*- coding: utf-8 -*-

from flectra import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Proyecto', store=True)
    bank_statements_source = fields.Selection(
        selection=[('file_import', 'File Import')], 
        string='Bank Feeds', default='undefined', 
        help="Defines how the bank statements will be registered")
