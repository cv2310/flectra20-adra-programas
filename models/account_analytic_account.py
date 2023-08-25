# -*- coding: utf-8 -*-
from flectra import models, fields
from flectra.exceptions import UserError

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    x_sub_account_code_income = fields.Integer(string='SubAccountCodeIncome', store=True, help='Sub Cuenta F en C')
    x_sub_account_code_expense = fields.Integer(string='SubAccountCodeExpense', store=True, help='Sub Cuenta Bco')
    x_function_code = fields.Integer(string='FunctionCode', store=True, help='Departamento')