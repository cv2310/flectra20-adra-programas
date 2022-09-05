# -*- coding: utf-8 -*-

from flectra import models, fields, api

class User(models.Model):
    _inherit = 'res.users'

    x_account_analytic_account_ids = fields.Many2many('account.analytic.account', string='Proyecto')


