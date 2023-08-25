from flectra import fields, models
class AdraAssetsChangeProject(models.TransientModel):
    _name = 'adra.assets.change.project'
    _description = 'Cambiar proyecto asociado a activo(s).'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Seleccione el nuevo proyecto:')

    def change_project(self):
        selected_assets = self.env['account.asset.asset'].browse(self._context.get('active_ids', []))

        for asset in selected_assets:
            asset.x_account_analytic_account_id = self.x_account_analytic_account_id

        return {'type': 'ir.actions.act_window_close'}