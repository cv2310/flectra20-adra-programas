# -*- coding: utf-8 -*-

from flectra import models, fields


class AccountGroup(models.Model):
    _inherit = 'account.group'

    x_ingress_group = fields.Integer(store=True)
    x_egress_group = fields.Integer(store=True)
