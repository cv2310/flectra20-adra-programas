# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.
from flectra import fields, models, api
from flectra.exceptions import UserError, ValidationError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'
    def write(self, vals):
        if not self.env.user.has_group('base.group_partner_manager'):
            message = ("No se puede modificar o crear Contactos ")
            raise UserError(message)
        return super().write(vals)

    @api.onchange("vat")
    def onchange_document(self):
        if self.vat:
            vat = (re.sub("[^1234567890Kk]", "", str(self.vat))).upper()
            if not self.check_vat_cl(vat):
                self.vat = vat
                raise ValidationError("El rut ingresado no es válido.")
            vat = '%s-%s' % (vat[:-1], vat[-1])
            exist = self.env["res.partner"].search(
                [
                    ("vat", "=", vat),
                    ("vat", "!=", "CL555555555"),
                    ("commercial_partner_id", "!=", self.commercial_partner_id.id),
                ],
                limit=1,
            )
            if exist:
                self.vat =  vat
                raise ValidationError(("El contacto %s está utilizando este rut") % exist.name)
            self.vat = vat


    def check_vat_cl(self, vat):
        body, vdig = "", ""
        if len(vat) > 9:
            return False
        else:
            body, vdig = vat[:-1], vat[-1].upper()
        try:
            vali = list(range(2, 8)) + [2, 3]
            operar = "0123456789K0"[11 - (sum([int(digit) * factor for digit, factor in zip(body[::-1], vali)]) % 11)]
            if operar == vdig:
                return True
            else:
                return False
        except IndexError:
            return False

    @api.constrains("vat")
    def _rut_unique(self):
        for r in self:
            # if not r.vat or r.parent_id:
            #     continue
            # partner = self.env["res.partner"].sudo().search(
            #     [("vat", "=", r.vat), ("id", "!=", r.id), ("commercial_partner_id", "!=", r.commercial_partner_id.id),]
            # )
            # if r.vat != "CL555555555" and partner:
            #     raise UserError("El rut ingresado ya se encuentra registrado en el sistema.")
            #     return False
            if r.vat:
                vat = (re.sub("[^1234567890Kk]", "", str(r.vat))).zfill(9).upper()
                if not r.check_vat_cl(vat):
                    raise ValidationError("El rut ingresado no es válido.")
                    return False
                vat = '%s-%s' % (vat[:-1], vat[-1])
                exist = self.env["res.partner"].search(
                    [
                        ("vat", "=", vat),
                        ("vat", "!=", "CL555555555"),
                        ("commercial_partner_id", "!=", r.commercial_partner_id.id),
                    ],
                    limit=1,
                )
                if exist:
                    raise UserError(("El contacto %s está utilizando este rut") % exist.name)
                    return False
            else:
                #raise UserError("Debe ingresar un rut Válido , que no este ya ingresado.")
                return False
