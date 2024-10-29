# -*- coding: utf-8 -*-

from flectra import models, fields, api


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Proyecto', store=True, index=True)
    x_name = fields.Char(related='invoice_id.x_name')
    invoice_date = fields.Date(related='invoice_id.date')
    x_floor = fields.Char(string='Nº Piso', store=True)
    x_office_number = fields.Char(string='Nº de Oficina', store=True)
    x_type_measure = fields.Char(string='Tipo de Medida', store=True)
    x_procedence = fields.Selection(
        [
            ('adquirido', 'Adquirido por el proyecto'),
            ('destinado', 'Destinado por el servicio'),
            ('traspaso', 'Traspaso desde otro proyecto'),
            ('donacion', 'Donación'),
            ('comodato', 'Comodato')
        ],
        string='Procedencia',
        store=True
    )
    x_account_move_id = fields.Many2one('account.move', string='Egreso asociado', inverse_name='x_account_asset_asset_ids', store=True, index=True)
    x_expense_n = fields.Char(string='Nº de Egreso', store=True)
    x_expense_number = fields.Char(string='Tipo de documento', store=True)
    x_expense_date = fields.Date(string='Fecha Doc. Egreso', index=True, default=fields.Date.context_today)
    x_invoice_number = fields.Char(string='Nº de Factura', store=True)
    x_transfer_record_number = fields.Char(string='Nº Acta de Traspaso', store=True)
    x_location = fields.Char(string='Ubicación Actual', store=True)
    x_inventory_unsubscribe_number = fields.Char(string='Nº Acta de Baja', store=True)
    x_quantity_unsubscribe = fields.Integer(string='Cantidad dada de Baja', store=True)
    x_status_active = fields.Selection([
        ('vigente', 'Vigente'),
        ('dado_baja', 'Dado de Baja')
    ], string='Estado-activo', store=True, default='vigente')
    x_status = fields.Char(string='Estado', store=True)
    x_description = fields.Text('Observaciones')
    x_used_by = fields.Char(string='Usado por', store=True)
    x_brand = fields.Char(string='Marca', store=True)
    x_model = fields.Char(string='Modelo', store=True)
    x_color = fields.Char(string='Color', store=True)
    x_quantity = fields.Integer(string='Cantidad', store=True)

    @api.onchange('x_account_move_id')
    def _onchange_x_account_move_id(self):
        if self.x_account_move_id._origin != self.x_account_move_id:
            self.x_account_move_id = self.x_account_move_id._origin
            self.x_account_analytic_account_id = self.x_account_move_id.x_account_analytic_account_id
        self.x_expense_n = self.x_account_move_id.x_name
    @api.onchange('x_expense_n', 'x_account_analytic_account_id', 'x_expense_date','id')
    def _onchange_x_code(self):
        for asset in self:
            expense = ''
            project = ''
            year = ''
            id = ''
            if asset._origin:
                id = asset._origin.id
            elif asset.id:
                id = asset.id
            if asset.x_expense_n:
                expense = asset.x_expense_n
            if asset.x_account_analytic_account_id:
                project = asset.x_account_analytic_account_id.code
            if asset.x_account_move_id:
                year = asset.x_account_move_id.date.year
                expense = asset.x_account_move_id.x_correlative
            else:
                if self.date:
                    year = asset.x_expense_date.year

            code = f"{id}-{project}-{expense}-{year}"
            asset.code = code



    def validate(self):
        for asset in self:
            asset._onchange_x_code()
        return super().validate()
  #  @api.model
   # def default_get(self, fields):
        #active_model = self.env.context.get('account_oove')