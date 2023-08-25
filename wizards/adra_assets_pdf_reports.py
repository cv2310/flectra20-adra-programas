from flectra.exceptions import UserError
from flectra import models, _
import datetime


class AdraAssetsPdfReports(models.TransientModel):
    _name = 'report.adra_account_extended.adra_report_sis_pdf'
    _description = 'Generador de Reportes en PDF para activos.'

    def _get_report_values(self, docids, data=None):
        project_name = data.get('project_name')
        project_code = data.get('project_code')
        projects_quantity = data.get('projects_quantity')
        sort_by = data.get('sort_by')
        x_status_active = data.get('x_status_active')
        pro_search = None
        act_search = None

        search = []
        if data['x_date_from']:
            ano, mes, dia = map(int, data['x_date_from'].split('-'))
            date_from = datetime.date(ano, mes, dia)
            dfrom_search = ('date', '>=', date_from)
            search.append(dfrom_search)
        if data['x_date_to']:
            ano, mes, dia = map(int, data['x_date_to'].split('-'))
            date_to = datetime.date(ano, mes, dia)
            dto_search = ('date', '<=', date_to)
            search.append(dto_search)
        if projects_quantity == 'one':
            pro_search = ('x_account_analytic_account_id', '=', project_code)
            search.append(pro_search)
        if x_status_active != 'general':
            act_search = ('x_status_active', '=', x_status_active)
            search.append(act_search)

        # if pro_search and  act_search:
        #     asset_records = self.env['account.asset.asset'].search([pro_search,act_search])
        # elif pro_search and  act_search:
        #     asset_records = self.env['account.asset.asset'].search([pro_search,act_search])
        # elif act_search:
        #     asset_records = self.env['account.asset.asset'].search([act_search])
        # elif pro_search:
        #     asset_records = self.env['account.asset.asset'].search([pro_search])
        # else:
        #     asset_records = self.env['account.asset.asset'].search([])
        asset_records = self.env['account.asset.asset'].search(search)
        if sort_by == 'fecha_ingreso':
            asset_records = sorted(asset_records, key=lambda r: (r.date))
        elif sort_by == 'proyecto_fecha':
            project_name = 'TODOS LOS PROGRAMAS'
            asset_records = sorted(asset_records, key=lambda r: (r.x_account_analytic_account_id.name, r.date))
        else:
            project_name = 'TODOS LOS PROGRAMAS'
            asset_records = sorted(asset_records, key=lambda r: (r.date, r.x_account_analytic_account_id.name))

        return {
            'assets': asset_records,
            'current_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'current_date_dmy': datetime.now().strftime('%d-%m-%Y'),
            'project_name': project_name,
            'sort_by': sort_by
        }