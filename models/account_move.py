# -*- coding: utf-8 -*-

from flectra import models, fields, api
from flectra.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from flectra.tools.misc import formatLang, format_date, get_lang
import datetime
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'
    _rec_name = 'x_name'
    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Proyecto', store=True, index=True)
    x_account_group_id = fields.Many2one('account.group', string='Tipo de Cuenta', store=True)
    x_account_asset_asset_ids = fields.One2many('account.asset.asset', 'x_account_move_id', string='Activo(s) asociado(s)', store=True, index=True)
    x_correlative = fields.Integer(string='Nº Documento', store=True, index=True);
    x_document_type = fields.Char(string='Tipo Documento', copy=False, store=True, index=True)
    x_name = fields.Char(string='Documento', copy=False, store=True)
    x_year = fields.Integer(string='Año Documento', store=True, index=True);
    x_payment_method_id = fields.Integer(string='Metodo de Pago', store=True);
    x_income_document_number = fields.Char(string='Nº Comprobante', store=True);
    x_rut_beneficiary = fields.Char(string='RUT Beneficiario', copy=False, store=True)
    x_beneficiary = fields.Char(string='Beneficiario', copy=False, store=True)
    x_back_up_document_number = fields.Char(string='Nº Doc. Respaldo', store=True);

    x_in_back_up_document_type = fields.Selection(
        selection=[
            ('Liquidación Subvención', 'Liquidación Subvención'),
            ('Comprobante Depósito de Terceros', 'Comprobante Depósito de Terceros'),
            ('Comprobante de Transferencia', 'Comprobante de Transferencia'),
            ('Otro', 'Otro')], string='Tipo Doc. Respaldo', store=True, 
            index=True, change_default=True)

    x_out_back_up_document_type = fields.Selection(
        selection=[
            ('Boleta', 'Boleta'),
            ('Boleta de Honorarios', 'Boleta de Honorarios'),
            ('Comprobante Interno', 'Comprobante Interno'),
            ('Factura', 'Factura'),
            ('Finiquito', 'Finiquito'),
            ('Formulario 29', 'Formulario 29'),
            ('Imposiciones', 'Imposiciones'),
            ('Liquidación de Sueldo', 'Liquidación de Sueldo'),
            ('Recibo', 'Recibo'),
            ('Otro', 'Otro')], string='Tipo Doc. Respaldo', store=True, 
            index=True, change_default=True)

    x_back_up_document_date = fields.Date(
        string='Fecha Doc. Respaldo',
        required=True,
        index=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False,
        default=fields.Date.context_today
    )

    _sql_constraints = [
        ('x_correlative', 'unique (x_correlative, x_account_analytic_account_id, x_year, x_document_type, company_id)', 'El Nº de Documento debe ser único por proyecto y tipo de documento!')
    ]

    @api.onchange('x_account_group_id')
    def _onchange_group_id_clear_line_ids(self):
        for line in self.line_ids:
            if line.account_id:
                line.unlink()

    def _get_document_type(self):
        ''' gets the document type whith SENAME's logic.
        '''
        document_type = ""

        if self.move_type == 'out_invoice':
            document_type = "INGRESO"
        elif self.move_type == 'in_invoice':
            document_type = "EGRESO"
        elif self.move_type == 'entry':
            document_type = "EGRESO"

        if self.env['account.account'].browse(self.line_ids.account_id.ids[1]).group_id.id == 17: # Devolutions
            document_type = "EGRESO"

        return document_type

    def _get_next_correlative(self):
        ''' gets the correlative whith SENAME's logic.
        '''
        for rec in self.line_ids.expense_id:
            if rec.payment_mode == 'own_account': # Paid expenses by the employee
                return None

        ''' if it already has a correlative, do not assign '''
        if self.x_correlative:
            return self.x_correlative
        query = """
                    SELECT MAX(x_correlative)
                    FROM account_move
                    WHERE x_account_analytic_account_id = %s
                    AND company_id = %s
                    AND x_document_type = %s
                    AND EXTRACT(YEAR FROM invoice_date) = %s
        """

        self.env.cr.execute(query, (self.x_account_analytic_account_id.id, self.company_id.id, self.x_document_type,  self.invoice_date.year))
        max_sequence = self.env.cr.fetchone()[0]
        if max_sequence is None:
            return 1
        return max_sequence + 1

    def _check_document_types_post(self):
        if self.x_account_analytic_account_id.id and self.invoice_date:
            for rec in self.filtered(
                    lambda r: r.company_id.country_id.code == "CL" and
                            r.journal_id.type in ['sale', 'purchase', 'bank']):
                rec.x_document_type = self._get_document_type()
                rec.x_correlative = self._get_next_correlative()
                rec.x_name = rec.x_document_type[0:3] + "/" + str(rec.x_correlative) + "/" + str(rec.invoice_date.year)
                rec.x_year = rec.invoice_date.year

    def _post(self, soft=True):
        self._check_document_types_post()
        return super()._post(soft)

    def write(self, vals):
        for move in self:
            vals.get('date')
            date = vals.get('date')
            if date is not None:
                if isinstance(date, str):
                    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                lock_date = datetime.date(2025, 4, 30)
                #lock_date = move.company_id._get_user_fiscal_lock_date()
                if date <= lock_date:
                    message = ("No se puede modificar o crear movimientos antes del ", format_date(self.env, lock_date))
                    raise UserError(message)
        return super().write(vals)

    # def _get_name_invoice_report(self):
    #     self.ensure_one()
    #     if self.company_id.country_id.code == 'CL':
    #         return 'adra_account_extended.report_invoice_document'
    #     return super()._get_name_invoice_report()

    def _get_reconciled_info_JSON_values(self):
        self.ensure_one()

        reconciled_vals = []
        for partial, amount, counterpart_line in self._get_reconciled_invoices_partials():
            if counterpart_line.move_id.ref:
                reconciliation_ref = '%s (%s)' % (counterpart_line.move_id.name, counterpart_line.move_id.ref)
            else:
                reconciliation_ref = counterpart_line.move_id.name

            reconciled_vals.append({
                'name': counterpart_line.name,
                'journal_name': counterpart_line.journal_id.name,
                'amount': amount,
                'currency': self.currency_id.symbol,
                'digits': [69, self.currency_id.decimal_places],
                'position': self.currency_id.position,
                'date': counterpart_line.date,
                'payment_id': counterpart_line.id,
                'partial_id': partial.id,
                'account_payment_id': counterpart_line.payment_id.id,
                'x_income_document_number': counterpart_line.payment_id.x_income_document_number,
                'x_back_up_document_number': counterpart_line.payment_id.x_back_up_document_number,
                'x_back_up_document_date': counterpart_line.payment_id.x_back_up_document_date,
                'x_name': counterpart_line.move_id.x_name,
                'payment_method_name': counterpart_line.payment_id.payment_method_id.name if counterpart_line.journal_id.type == 'bank' else None,
                'bank_name': counterpart_line.payment_id.journal_id.bank_id.name,
                'bank_acc_number': counterpart_line.payment_id.journal_id.bank_acc_number,
                'move_id': counterpart_line.move_id.id,
                'ref': reconciliation_ref,
            })
        return reconciled_vals

    @api.constrains('name', 'journal_id', 'state')
    def _check_unique_sequence_number(self):
        _logger.warning("nw _check_unique_sequence_number")
        return
 #   def name_get(self):
  #      return [(accountMove.id, accountMove.x_name ) for accountMove in self]
    def name_get(self):
        result = []
        for accountMove in self:
            if accountMove.x_name:
                name = accountMove.x_name
            elif accountMove.name:
                name = accountMove.name
            else:
                name = "Sin Definir"
            result.append((accountMove.id, name))
        return result
