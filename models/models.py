# -*- coding: utf-8 -*-

# from flectra import models, fields, api


# class adra_account_extended(models.Model):
#     _name = 'adra_account_extended.adra_account_extended'
#     _description = 'adra_account_extended.adra_account_extended'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
