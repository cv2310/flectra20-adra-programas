# -*- coding: utf-8 -*-



from flectra import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    move_lock_date = fields.Date(string="Fecha actual de bloqueo", readonly=True, store=True)
    move_lock_date_new = fields.Date(string="Nueva fecha de bloqueo", store=True)
    archivo_plano_date = fields.Date(string="Fecha actual de archivo plano", readonly=True, store=True)
    archivo_plano_date_new = fields.Date(string="Nueva fecha de archivo plano", store=True)

    def _validate_fiscalyear_lock(self, values):
        if self.ids:
            values = values