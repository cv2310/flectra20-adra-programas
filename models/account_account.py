# -*- coding: utf-8 -*-

from flectra import models, fields


class AccountGroup(models.Model):
    _inherit = 'account.account'

    x_senainfo_name = fields.Char(string='Cuenta SENAINFO', store=True)
    x_senainfo_project_code = fields.Integer(store=True)
    x_senainfo_institution_code = fields.Integer(store=True)

    def _compute_account_group(self):
        if self.ids:
            self.env['account.group']._adapt_accounts_for_account_groups(self)
