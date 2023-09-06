from flectra import fields, models

class AdraCompanyWizard(models.TransientModel):
    _name = 'adra.company.wizard'
    _description = 'Modelo transitorio para leer y actualizar campos adicionales del modelo res.company.'

    move_lock_date = fields.Date(string="Fecha actual de bloqueo", readonly=True, store=True)
    move_lock_date_new = fields.Date(string="Nueva fecha de bloqueo", store=True)
    archivo_plano_date = fields.Date(string="Fecha actual de archivo plano", readonly=True, store=True)
    archivo_plano_date_new = fields.Date(string="Nueva fecha de archivo plano", store=True)