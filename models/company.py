# -*- coding: utf-8 -*-



from flectra import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    def _validate_fiscalyear_lock(self, values):
        if self.ids:
            values = values
