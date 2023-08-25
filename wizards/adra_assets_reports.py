from flectra.exceptions import UserError
from flectra import fields, models
import datetime

class AdraAssetsReports(models.TransientModel):
    _name = 'adra.assets.reports'
    _description = 'Generador de Reportes en PDF y Excel para activos.'

    x_all_projects = fields.Selection([('one', 'Un proyecto'), ('all', 'Todos los proyectos')],
                                      string='Proyecto', default='one')
    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Seleccione un proyecto')
    x_sort_by_project = fields.Selection([('fecha_ingreso', 'Fecha')], string='Ordenado por', default='fecha_ingreso')
    x_sort_by_all = fields.Selection([('fecha_proyecto', 'Fecha/Proyecto'), ('proyecto_fecha', 'Proyecto/Fecha')],
                                     string='Ordenado por', default='fecha_proyecto')
    x_status_active = fields.Selection([('general', 'General'), ('vigente', 'Vigente'), ('dado_baja', 'Dado de baja')],
                                     string='Estado activo;', default='general')
    x_date_from = fields.Date(string='Desde')
    x_date_to = fields.Date(string='Hasta')

    def generate_pdf_report(self):
        sort_by = self.x_sort_by_project if self.x_all_projects == 'one' else self.x_sort_by_all
        projects_quantity = self.x_all_projects
        if projects_quantity == 'one' and not self.x_account_analytic_account_id:
            error_message = ("Por favor, seleccione un proyecto antes de continuar.\n"
                             "Si desea incluir todos los proyectos en el informe, "
                             "asegúrese de seleccionar la opción 'TODOS LOS PROYECTOS'.")
            raise UserError(error_message)

        data = {
            'project_code': self.x_account_analytic_account_id.code,
            'project_name': self.x_account_analytic_account_id.name,
            'sort_by': sort_by,
            'projects_quantity': projects_quantity,
            'x_status_active': self.x_status_active,
            'x_date_from': self.x_date_from,
            'x_date_to': self.x_date_to
        }
        report = self.env.ref('adra_account_extended.report_pdf_assets')
        return report.report_action(self, data=data)

    def generate_excel_report(self):
        sort_by = self.x_sort_by_project if self.x_all_projects == 'one' else self.x_sort_by_all
        projects_quantity = self.x_all_projects
        if projects_quantity == 'one' and not self.x_account_analytic_account_id:
            error_message = ("Por favor, seleccione un proyecto antes de continuar.\n"
                             "Si desea incluir todos los proyectos en el informe, "
                             "asegúrese de seleccionar la opción 'TODOS LOS PROYECTOS'.")
            raise UserError(error_message)
        data = {'project_name': self.x_account_analytic_account_id.name,
                'project_code': self.x_account_analytic_account_id.code,
                'sort_by': sort_by,
                'projects_quantity': projects_quantity,
                'x_status_active': self.x_status_active,
                'x_date_from': self.x_date_from,
                'x_date_to': self.x_date_to
                }
        report = self.env.ref('adra_account_extended.report_xlsx_assets')
        return report.report_action(self, data=data)