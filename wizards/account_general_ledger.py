# -*- coding: utf-8 -*-
from datetime import datetime
from flectra.tools import get_lang
from flectra import fields, models, _
from flectra.exceptions import UserError


class AccountReportGeneralLedger(models.TransientModel):
    _inherit = "account.report.general.ledger"

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Proyecto', store=True)
    x_program_name = fields.Char(string='Nombre Proyecto', copy=False, store=True)
    x_sort_by = fields.Selection([('fecha_ingreso', 'Fecha'), ('nro_comprobante', 'Nro. Comprobante')], string='Ordenado por', required=True, default='nro_comprobante')
    x_report_type = fields.Selection([('cuenta', 'ADRA'), ('cuenta_senainfo', 'SENAINFO')], string='Tipo de Reporte', required=True, default='cuenta')
    x_document_type = fields.Selection([('INGRESO', 'Libro Ingresos'), ('EGRESO', 'Libro Egresos'), ('BANCO', 'Libro Banco'), ('RENDICION', 'Rendición de Cuentas'), ('CONCILIACION', 'Conciliación Bancaria')], string='Tipo de Movimientos', required=True, default='BANCO')
    x_bank_final_balance = fields.Float(string='Saldo Cartola Bancaria', store=True, default=0)
    journal_ids = fields.Many2many('account.journal', 'account_report_general_ledger_journal_rel', 'account_id', 'journal_id', string='Journals', required=True)
    x_report_version = fields.Selection([('new', 'Nueva'), ('old', 'Antigua')], string='Versión Reportes', required=True, default='new')

    def _print_report(self, data):
        self.x_program_name = self.x_account_analytic_account_id.name
        data = self.pre_print_report(data)
        data['form'].update(self.read(['x_account_analytic_account_id', 'x_sort_by', 'x_report_type', 'x_document_type', 'x_program_name', 'x_bank_final_balance','x_report_version'])[0])
        if not data['form'].get('date_from'):
            raise UserError(_("Debe seleccionar una fecha de inicio."))
        if not data['form'].get('date_to'):
            raise UserError(_("Debe seleccionar una fecha final."))
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('accounting_pdf_reports.action_report_general_ledger').with_context(landscape=True).report_action(records, data=data)

    def _print_report_xls(self, data):
        self.x_program_name = self.x_account_analytic_account_id.name
        data = self.pre_print_report(data)
        data['form'].update(self.read(['x_account_analytic_account_id', 'x_sort_by', 'x_report_type', 'x_document_type', 'x_program_name', 'x_bank_final_balance','x_report_version'])[0])
        if not data['form'].get('date_from'):
            raise UserError(_("Debe seleccionar una fecha de inicio."))
        if not data['form'].get('date_to'):
            raise UserError(_("Debe seleccionar una fecha final."))
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('adra_account_extended.report_xlsx_general_ledger').with_context(landscape=True).report_action(records, data=data)


    def print_report_xls(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)
        return self.with_context(discard_logo_check=True)._print_report_xls(data)