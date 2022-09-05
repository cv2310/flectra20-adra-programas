# -*- coding: utf-8 -*-

from flectra import models, fields


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    x_account_analytic_account_id = fields.Many2one('account.analytic.account', string='Proyecto', store=True)
    x_name = fields.Char(string='Glosa', store=True, required=True);
    x_income_document_number = fields.Char(string='Nº Comprobante', store=True, index=True);
    x_is_charged = fields.Boolean(default=True, string='Cobrado?')

    _sql_constraints = [
        ('x_income_document_number', 'unique (x_income_document_number, payment_method_id, journal_id, company_id)', 'El Nº de documento debe ser único por cuenta y método de pago!')
    ]

    def _create_payment_vals_from_wizard(self):
        payment_vals = {
            'date': self.payment_date,
            # 'payment_date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'ref': self.communication,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_id': self.payment_method_id.id,
            'destination_account_id': self.line_ids[0].account_id.id,
            'x_account_analytic_account_id': self.line_ids.move_id.x_account_analytic_account_id.id,
            'x_name': self.x_name,
            'x_income_document_number': self.x_income_document_number,
            'x_is_charged': self.x_is_charged
        }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
            }
        return payment_vals
