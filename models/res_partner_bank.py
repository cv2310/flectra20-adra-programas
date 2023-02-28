# -*- coding: utf-8 -*-

import re

from collections.abc import Iterable

from flectra import api, fields, models, _
from flectra.osv import expression


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    def name_get(self):
        return [(partnerBank.id, "%s - %s" % (partnerBank.acc_number, partnerBank.acc_holder_name)) for partnerBank in self]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|',('acc_holder_name',operator,name),('acc_number',operator,name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
