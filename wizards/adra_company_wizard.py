from flectra import fields, models

class AdraCompanyWizard(models.TransientModel):
    _name = 'adra.company.wizard'
    _description = 'Modelo transitorio para leer y actualizar campos adicionales del modelo res.company.'

    move_lock_date = fields.Date(string="Fecha actual de bloqueo", readonly=True, store=True, default=lambda self: self.env.company.move_lock_date)
    move_lock_date_new = fields.Date(string="Nueva fecha de bloqueo", store=True)
    archivo_plano_date = fields.Date(string="Fecha actual de archivo plano", readonly=True, store=True, default=lambda self: self.env.company.archivo_plano_date)
    archivo_plano_date_new = fields.Date(string="Nueva fecha de archivo plano", store=True)

    def update_move_lock_date(self):
        # Obtiene el registro de la compañía actual.
        company = self.env.company

        # Actualiza la fecha de bloqueo de movimientos en el modelo res.company.
        company.write({
            'move_lock_date': self.move_lock_date_new,
        })

    def update_archivo_plano_date(self):
        # Obtiene el registro de la compañía actual.
        company = self.env.company

        # Actualiza la fecha de archivo plano en el modelo res.company.
        company.write({
            'archivo_plano_date': self.archivo_plano_date_new,
        })