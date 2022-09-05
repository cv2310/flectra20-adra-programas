# -*- coding: utf-8 -*-

import time
from flectra import api, models, _
from flectra.exceptions import UserError


class ReportGeneralLedger(models.AbstractModel):
    _inherit = 'report.accounting_pdf_reports.report_general_ledger'

    # income/expense ledger
    def _get_mayor_ledger_entries(self, accounts, x_account_analytic_account_id, x_sort_by, x_report_type, x_document_type):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        account_res = []

        if x_report_type == 'cuenta':

            # Get movements of mayor ledger
            sql = ('''SELECT grupo, account_id, cod_cuenta, nro_comprobante,\
                tipo_docto_respaldo, nro_docto_respaldo, beneficiario, medio_pago,\
                nro_comprobante_pago, fecha_pago, glosa, monto, monto as total\
                FROM account_report_back\
                WHERE tipo_documento = %s\
                AND x_account_analytic_account_id = %s\
                AND fecha_ingreso BETWEEN %s AND %s\
                ORDER BY account_id, ''' + x_sort_by)
            
            params = (x_document_type, x_account_analytic_account_id, where_params[2][1], where_params[2][0])

            cr.execute(sql, params)

            for row in cr.dictfetchall():
                total = 0
                for line in move_lines.get(row['account_id']):
                    total += line['monto']
                row['total'] += total
                move_lines[row.pop('account_id')].append(row)

            for account in accounts:
                res = dict((fn, 0.0) for fn in ['total'])
                res['code'] = account.code
                res['name'] = account.name
                res['move_lines'] = move_lines[account.id]
                for line in res.get('move_lines'):
                    res['total'] = line['total']
                if res.get('move_lines'):
                    account_res.append(res)

        elif x_report_type == 'cuenta_senainfo':

            # Get total group by cod_grupo
            sql = ('''SELECT cod_grupo as code, grupo as name, sum(monto) AS total\
                FROM account_report_back\
                WHERE tipo_documento = %s\
                AND x_account_analytic_account_id = %s\
                AND fecha_ingreso BETWEEN %s AND %s\
                GROUP BY cod_grupo, grupo''')
            
            params = (x_document_type, x_account_analytic_account_id, where_params[2][1], where_params[2][0])

            cr.execute(sql, params)

            groups = []
            ids = []
            for row in cr.dictfetchall():
                groups.append(row)
                ids.append(row['code'])

            move_lines = {x: [] for x in ids}

            # Get movements of mayor ledger
            sql = ('''SELECT cod_grupo as code, nro_comprobante, tipo_docto_respaldo, nro_docto_respaldo, beneficiario,\
                medio_pago, nro_comprobante_pago, fecha_pago, glosa, monto\
                FROM account_report_back\
                WHERE tipo_documento = %s\
                AND x_account_analytic_account_id = %s\
                AND fecha_ingreso BETWEEN %s AND %s\
                ORDER BY cod_grupo, ''' + x_sort_by)
            
            params = (x_document_type, x_account_analytic_account_id, where_params[2][1], where_params[2][0])

            cr.execute(sql, params)

            for row in cr.dictfetchall():
                move_lines[row.pop('code')].append(row)

            for group in groups:
                res = dict((fn, group['total']) for fn in ['total'])
                res['code'] = ''
                res['name'] = group['name']
                res['move_lines'] = move_lines[group['code']]
                if res.get('move_lines'):
                    account_res.append(res)

        if not account_res:
            raise UserError(_("No existen datos para las fechas seleccionadas."))
        return account_res

    # bank ledger
    def _get_bank_ledger_entries(self, accounts, x_account_analytic_account_id, x_sort_by, x_report_type, x_document_type):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        # Get initial balance
        sql = ('''SELECT tipo_documento, sum(monto) as saldo\
            FROM account_report_back\
            WHERE x_account_analytic_account_id = %s\
            AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
            AND fecha_pago < %s\
            GROUP BY tipo_documento''')
        
        params = (x_account_analytic_account_id, where_params[2][1])
        cr.execute(sql, params)

        initial_balance = 0
        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['saldo']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['saldo']

        if total_income and total_expenses:
            initial_balance = total_income - total_expenses

        # Get ids movements of bank ledger
        sql = ('''SELECT row_number() OVER () as id\
            FROM account_report_back\
            WHERE x_account_analytic_account_id = %s\
            AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
            AND fecha_pago BETWEEN %s AND %s''')
        
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0])

        cr.execute(sql, params)

        moves = []
        for row in cr.dictfetchall():
            moves.append(row['id'])

        if not moves:
            raise UserError(_("No existen datos para las fechas seleccionadas."))

        # move_lines = {x: [] for x in moves}
        move_lines = []

        if x_sort_by == 'fecha_ingreso':
            x_sort_by = 'fecha_pago'

        # Get movements of bank ledger
        sql = ('''SELECT row_number() OVER () as id, tipo_documento, fecha_ingreso, nro_comprobante, medio_pago, nro_comprobante_pago, fecha_pago, glosa, beneficiario,\
            CASE tipo_documento WHEN 'INGRESO' THEN monto ELSE 0 END AS ingreso,\
            CASE tipo_documento WHEN 'EGRESO' THEN monto ELSE 0 END AS egreso\
            FROM account_report_back\
            WHERE x_account_analytic_account_id = %s\
            AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
            AND fecha_pago BETWEEN %s AND %s\
            ORDER BY ''' + x_sort_by)
        
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0])

        cr.execute(sql, params)

        total_income = 0
        total_expenses = 0
        balance = initial_balance
        for row in cr.dictfetchall():
            line = dict((fn, (balance)) for fn in ['saldo'])
            line['tipo_documento'] = row['tipo_documento']
            line['fecha_ingreso'] = row['fecha_ingreso']
            line['nro_comprobante'] = row['nro_comprobante']
            line['medio_pago'] = row['medio_pago']
            line['nro_comprobante_pago'] = row['nro_comprobante_pago']
            line['fecha_pago'] = row['fecha_pago']
            line['glosa'] = row['glosa']
            line['beneficiario'] = row['beneficiario']
            line['ingreso'] = row['ingreso']
            line['egreso'] = row['egreso']
            if row['tipo_documento'] == 'INGRESO':
                line['saldo'] += row['ingreso'] 
                total_income += row['ingreso']
            elif row['tipo_documento'] == 'EGRESO':
                line['saldo'] -= row['egreso'] 
                total_expenses += row['egreso']
            move_lines.append(line)
            balance = line['saldo']
            
        account_res = []
        res = dict((fn, 0.0) for fn in ['final_balance'])
        res['initial_balance'] = initial_balance
        res['total_income'] = total_income
        res['total_expenses'] = total_expenses
        res['final_balance'] = (initial_balance + total_income) - total_expenses
        res['move_lines'] = move_lines
        account_res.append(res)

        return account_res

    # bank reconciliation
    def _get_bank_reconciliation_entries(self, accounts, x_account_analytic_account_id, x_sort_by, x_bank_final_balance):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        # Get initial balance
        sql = ('''SELECT tipo_documento, sum(monto) as total\
            FROM account_report_back\
            WHERE x_account_analytic_account_id = %s\
            AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
            AND fecha_pago < %s\
            GROUP BY tipo_documento''')
        
        params = (x_account_analytic_account_id, where_params[2][1])
        cr.execute(sql, params)

        initial_balance = 0
        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['total']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['total']

        if total_income and total_expenses:
            initial_balance = total_income - total_expenses

        # Get income and expenses from period
        sql = ('''SELECT tipo_documento, sum(monto) as total\
            FROM account_report_back\
            WHERE x_account_analytic_account_id = %s\
            AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
            AND fecha_pago BETWEEN %s AND %s\
            GROUP BY tipo_documento''')
        
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0])
        cr.execute(sql, params)

        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['total']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['total']

        x_sort_by = 'fecha_pago'

        # Get checks drawn uncharged
        sql = ('''SELECT row_number() OVER () as id, m2.x_name AS documento, p.x_income_document_number AS nro_cheque,\
            m.date AS fecha_pago, p.amount AS monto, m.invoice_partner_display_name AS beneficiario, p.x_name AS referencia\
            FROM account_payment p\
            LEFT JOIN account_move m ON (m.payment_id = p.id)\
            LEFT JOIN account_move m2 ON (m.ref = m2.name)\
            WHERE p.x_is_charged = FALSE\
            AND m2.x_account_analytic_account_id = %s\
            AND EXTRACT(YEAR FROM m.date) = ''' + where_params[2][1][0:4] + ''' \
            AND m.date BETWEEN %s AND %s\
            ORDER BY ''' + x_sort_by)
        
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0])

        cr.execute(sql, params)

        total_checks_drawn_uncharged = 0
        move_lines = []
        for row in cr.dictfetchall():
            line = dict((fn, (0)) for fn in ['id'])
            line['id'] = row['id']
            line['documento'] = row['documento']
            line['nro_cheque'] = row['nro_cheque']
            line['fecha_pago'] = row['fecha_pago']
            line['monto'] = row['monto']
            line['beneficiario'] = row['beneficiario']
            line['referencia'] = row['referencia']
            move_lines.append(line)
            total_checks_drawn_uncharged += row['monto']
            
        account_res = []
        final_balance = 0
        res = dict((fn, 0.0) for fn in ['final_balance'])
        res['initial_balance'] = initial_balance
        res['total_income'] = total_income
        res['total_expenses'] = total_expenses
        res['total_checks_drawn_uncharged'] = total_checks_drawn_uncharged
        res['reconciled_balance'] = ((initial_balance + total_income) - total_expenses) - total_checks_drawn_uncharged
        final_balance = (initial_balance + total_income) - total_expenses
        res['final_balance'] = final_balance
        res['bank_final_balance'] = x_bank_final_balance
        res['difference'] = x_bank_final_balance - final_balance
        res['move_lines'] = move_lines
        account_res.append(res)

        return account_res
    
    # accountability
    def _get_accountability_entries(self, accounts, x_account_analytic_account_id, x_sort_by, x_report_type, x_document_type):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        # Get initial balance
        sql = ('''SELECT tipo_documento, sum(monto) as total\
            FROM account_report_back\
            WHERE x_account_analytic_account_id = %s\
            AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
            AND fecha_pago < %s\
            GROUP BY tipo_documento''')
        
        params = (x_account_analytic_account_id, where_params[2][1])
        cr.execute(sql, params)

        initial_balance = 0
        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['total']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['total']

        if total_income and total_expenses:
            initial_balance = total_income - total_expenses

        # Get income from period group by SENAINFO accounts
        sql = ('''SELECT row_number() OVER () as id, grupo as cuenta_senainfo, sum(monto) as total\
            FROM account_report_back\
            WHERE x_account_analytic_account_id = %s\
            AND tipo_documento = 'INGRESO'\
            AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
            AND fecha_pago BETWEEN %s AND %s\
            GROUP BY grupo''')
        
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0])
        cr.execute(sql, params)

        total_income_from_period = 0
        move_lines_income = []
        for row in cr.dictfetchall():
            line = dict((fn, (0)) for fn in ['id'])
            line['id'] = row['id']
            line['cuenta_senainfo'] = row['cuenta_senainfo']
            line['total'] = row['total']
            move_lines_income.append(line)
            total_income_from_period += row['total']

        # Get expenses from period group by SENAINFO accounts
        sql = ('''SELECT row_number() OVER () as id, grupo as cuenta_senainfo, sum(monto) as total\
            FROM account_report_back\
            WHERE x_account_analytic_account_id = %s\
            AND tipo_documento = 'EGRESO'\
            AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
            AND fecha_pago BETWEEN %s AND %s\
            GROUP BY grupo''')
        
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0])
        cr.execute(sql, params)

        total_expenses_from_period = 0
        move_lines_expenses = []
        for row in cr.dictfetchall():
            line = dict((fn, (0)) for fn in ['id'])
            line['id'] = row['id']
            line['cuenta_senainfo'] = row['cuenta_senainfo']
            line['total'] = row['total']
            move_lines_expenses.append(line)
            total_expenses_from_period += row['total']

        account_res = []
        res = dict((fn, 0.0) for fn in ['final_balance'])
        res['initial_balance'] = initial_balance
        res['total_income_from_period'] = total_income_from_period
        res['total_expenses_from_period'] = total_expenses_from_period
        res['total_income'] = initial_balance + total_income_from_period
        res['final_balance'] = (initial_balance + total_income_from_period) - total_expenses_from_period
        res['move_lines_income'] = move_lines_income
        res['move_lines_expenses'] = move_lines_expenses
        account_res.append(res)

        return account_res

    @api.model
    def _get_report_values(self, docids, data=None):
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
        
        codes = []
        if data['form'].get('journal_ids', False):
            codes = [journal.code for journal in self.env['account.journal'].search([('id', 'in', data['form']['journal_ids'])])]

        accounts = docs if model == 'account.account' else self.env['account.account'].search([])
        
        if x_document_type in ['INGRESO', 'EGRESO']:
            accounts_res = self.with_context(data['form'].get('used_context',{}))._get_mayor_ledger_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
        elif x_document_type == 'BANCO':
            accounts_res = self.with_context(data['form'].get('used_context',{}))._get_bank_ledger_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)
        elif x_document_type == 'CONCILIACION':
            accounts_res = self.with_context(data['form'].get('used_context',{}))._get_bank_reconciliation_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_bank_final_balance)
        elif x_document_type == 'RENDICION':
            accounts_res = self.with_context(data['form'].get('used_context',{}))._get_accountability_entries(accounts, x_account_analytic_account_id[0], x_sort_by, x_report_type, x_document_type)

        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': accounts_res,
            'print_journal': codes,
        }
