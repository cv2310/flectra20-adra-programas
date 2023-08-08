import base64
from datetime import datetime

from flectra.exceptions import UserError
from flectra import fields, models, _

class AdraAssetsPdfReports(models.TransientModel):
    _name = 'report.adra_account_extended.adra_report_sis_pdf'
    _description = 'Generador de Reportes en PDF para activos.'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Seleccione un proyecto')

    def _get_report_values(self, docids, data=None):
        proyecto_code = data.get('proyecto_code')
        proyecto_name = data.get('proyecto_name')
        # Verificar si se seleccionó un proyecto antes de generar el informe
        if proyecto_code is None:
            raise UserError(_("Debe seleccionar un proyecto."))

        # Obtener los registros de activos relacionados con el proyecto seleccionado
        asset_records = self.env['account.asset.asset'].search([
            ('x_account_analytic_account_id', '=', proyecto_code)
        ])

        # Construir el diccionario de datos para el informe
        assets = []

        # Llenar la lista de activos con los datos de los registros encontrados
        for index, asset in enumerate(asset_records, start=1):
            asset_data = {
                'index': index,
                'ce': asset.x_expense_number if asset.x_expense_number else "-",
                'fecha': asset.date if asset.date else "-",
                'codigo': asset.code if asset.code else "-",
                'clasificacion': asset.name if asset.name else "-",
                'descripcion': asset.x_description if asset.x_description else "-",
                'estado': asset.x_status if asset.x_status else "-",
                'observacion': asset.x_description if asset.x_description else "-",
                'ubicacion': asset.x_location if asset.x_location else "-",
                'cantidad': asset.x_quantity if asset.x_quantity else "-",
                'monto': asset.value if asset.value else "-"
            }
            assets.append(asset_data)
        return {
            'assets': asset_records,
            'current_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'current_date_dmy': datetime.now().strftime('%d-%m-%Y'),
            'proyecto_name' : proyecto_name
        }


    def print_report(self):
        # Obtener el proyecto seleccionado desde el formulario
        proyecto = self.x_account_analytic_account_id

        # Verificar si se seleccionó un proyecto antes de generar el informe
        if not proyecto:
            raise UserError(_("Debe seleccionar un proyecto."))

        # Generar el informe en formato PDF y pasar el diccionario de datos al informe como argumento
        data = {'proyecto_code': proyecto.code,
                'proyecto_name': proyecto.name}
        report = self.env.ref('adra_account_extended.report_pdf_assets')
        return report.report_action(self, data=data)

    def cancel_report(self):
        # Agregar la lógica para cancelar el informe aquí
        pass
