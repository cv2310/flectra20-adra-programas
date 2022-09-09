# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra import fields, models
from flectra.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    def write(self, vals):
        if   not self.env.user.has_group('base.group_partner_manager'):
            message = ("No se puede modificar o crear Contactos ")
            raise UserError(message)
        return super().write(vals)

