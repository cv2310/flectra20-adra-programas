# -*- coding: utf-8 -*-
import time
from flectra import api, models, _
from flectra.exceptions import UserError


class ReportGeneralLedger(models.AbstractModel):
    _inherit = 'report.accounting_pdf_reports.report_general_ledger'

    @api.model
    def _get_report_values(self, docids, data=None):
        reportData = self.env['report.general.ledger.data']
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids', []))
        # init_balance = data['form'].get('initial_balance', True)
        # sortby = data['form'].get('sortby', 'sort_date')
        # display_account = data['form']['display_account']
        # x_account_analytic_account_id = data['form']['x_account_analytic_account_id']
        x_account_analytic_account_id = data['form'].get('x_account_analytic_account_id', 'project_id')
        x_sort_by = data['form'].get('x_sort_by', 'sort_date')
        x_report_type = data['form'].get('x_report_type', 'adra_type')
        x_document_type = data['form'].get('x_document_type', 'document_type')
        x_bank_final_balance = data['form'].get('x_bank_final_balance', 'bank_final_balance')
        x_report_version = data['form'].get('x_report_version', 'new')
        codes = []
        if data['form'].get('journal_ids', False):
            codes = [journal.code for journal in self.env['account.journal'].search([('id', 'in', data['form']['journal_ids'])])]

        accounts = docs if model == 'account.account' else self.env['account.account'].search([])

        if x_report_version == "new":
            if x_document_type in ['INGRESO', 'EGRESO']:
                accounts_res = reportData.with_context(data['form'].get('used_context',{}))._get_mayor_ledger_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
            elif x_document_type == 'BANCO':
                accounts_res = reportData.with_context(data['form'].get('used_context',{}))._get_bank_ledger_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
            elif x_document_type == 'CONCILIACION':
                accounts_res = reportData.with_context(data['form'].get('used_context',{}))._get_bank_reconciliation_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_bank_final_balance)
            elif x_document_type == 'RENDICION':
                accounts_res = reportData.with_context(data['form'].get('used_context',{}))._get_accountability_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
        else:
            if x_document_type in ['INGRESO', 'EGRESO']:
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_mayor_ledger_entries(
                    accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
            elif x_document_type == 'BANCO':
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_bank_ledger_entries_old(
                    accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
            elif x_document_type == 'CONCILIACION':
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_bank_reconciliation_entries_old(
                    accounts, x_account_analytic_account_id[0], x_sort_by, x_bank_final_balance)
            elif x_document_type == 'RENDICION':
                accounts_res = reportData.with_context(data['form'].get('used_context', {}))._get_accountability_entries_old(
                    accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)

        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': accounts_res,
            'print_journal': codes,
        }
