# -*- coding: utf-8 -*-
{
    'name': "adra_account_extended",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "LOGRA S.A.",
    'website': "http://www.logra.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_asset', 'l10n_cl', 'hr_expense', 'accounting_pdf_reports'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/adra_account_extended_security.xml',
        'data/account_group_parent.xml',
        'data/account_group.xml',
        'data/account_account.xml',
        'data/account_payment_method.xml',
        'data/account.analytic.account.csv',
        'views/res_users_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/account_asset_views.xml',
        'views/account_payment_views.xml',
        'views/account_payment_register_views.xml',
        'views/hr_expense_sheet_views.xml',
        'views/hr_expense_views.xml',
        'reports/account_report_back_view.xml',
        'wizards/general_ledger.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
}
