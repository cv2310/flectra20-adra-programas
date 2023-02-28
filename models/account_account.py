# -*- coding: utf-8 -*-

from flectra import models, fields
from flectra.exceptions import UserError


class AccountGroup(models.Model):
    _inherit = 'account.account'

    x_senainfo_name = fields.Char(string='Cuenta SENAINFO', store=True)
    x_senainfo_project_code = fields.Integer(store=True)
    x_senainfo_institution_code = fields.Integer(store=True)
    x_senainfo_group_name = fields.Char(string='Cuenta grupo SENAINFO', store=True)
    def _compute_account_group(self):
        if self.ids:
            self.env['account.group']._adapt_accounts_for_account_groups(self)


    def write(self, vals):
        if   not self.env.user.has_group('base.group_partner_manager'):
            message = ("No tiene los privilegios para crear o modificar una Cuenta Contable. Comuníquese con un Administrador.")
            raise UserError(message)
        return super().write(vals)


