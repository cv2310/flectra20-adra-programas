# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra import fields, models, tools


class AccountReportBack(models.Model):
    _name = "account.report.back"
    _description = "Accountability to SENAME"
    _auto = False

    id = fields.Float(string='id', readonly=True)
    tipo_docto_senainfo = fields.Integer(string='tipo_docto_senainfo', readonly=True)
    tipo_documento = fields.Char(string='tipo_documento', readonly=True)
    cod_programa = fields.Char(string='cod_programa', readonly=True)
    programa = fields.Char(string='programa', readonly=True)
    codigo_proyecto = fields.Char(string='codigo_proyecto', readonly=True)
    grupo = fields.Char(string='grupo', readonly=True)
    cod_cuenta = fields.Char(string='cod_cuenta', readonly=True)
    cuenta = fields.Char(string='cuenta', readonly=True)
    cuenta_senainfo = fields.Char(string='cuenta_senainfo', readonly=True)
    periodo = fields.Char(string='periodo', readonly=True)
    fecha_ingreso = fields.Date(string='fecha_ingreso', readonly=True)
    nro_comprobante = fields.Integer(string='nro_comprobante', readonly=True)
    correlativo = fields.Float(string='correlativo', readonly=True)
    fecha_pago = fields.Date(string='fecha_pago', readonly=True)
    vigencia = fields.Integer(string='vigencia', readonly=True)
    medio_pago_senainfo = fields.Integer(string='medio_pago_senainfo', readonly=True)
    medio_pago = fields.Char(string='medio_pago', readonly=True)
    monto = fields.Float(string='monto', readonly=True)
    glosa = fields.Char(string='glosa', readonly=True)
    cod_cuenta_senainfo = fields.Integer(string='cod_cuenta_senainfo', readonly=True)
    nro_comprobante_pago = fields.Char(string='nro_comprobante_pago', readonly=True)
    beneficiario = fields.Char(string='beneficiario', readonly=True)
    x_account_analytic_account_id = fields.Integer(string='id_proyecto', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, 'account_report_back')
        self._cr.execute("""
            CREATE OR REPLACE VIEW account_report_back AS
				SELECT row_number() OVER () as id, *
				FROM (
					SELECT
						CASE WHEN m.x_document_type::text = 'INGRESO'::character varying::text THEN 1
							WHEN m.x_document_type::text = 'EGRESO'::character varying::text THEN 0
							ELSE 9
						END AS tipo_docto_senainfo,
						m.x_document_type AS tipo_documento,
						aa.code AS cod_programa,
						aa.name AS programa,
						'6902' AS codigo_proyecto,
						ac.group_id AS cod_grupo,
						ag.name AS grupo,
						ac.id AS account_id,
						ac.code AS cod_cuenta,
						ac.name AS cuenta,
						ac.x_senainfo_name AS cuenta_senainfo,
						to_char(m.invoice_date, 'YYYYMM') AS periodo,
						m.x_back_up_document_number AS nro_docto_respaldo,
						CASE WHEN m.x_in_back_up_document_type IS NOT NULL THEN m.x_in_back_up_document_type
							WHEN m.x_out_back_up_document_type IS NOT NULL THEN m.x_out_back_up_document_type
							ELSE ''
						END AS tipo_docto_respaldo,
						m.invoice_date AS fecha_ingreso,
						m.x_correlative AS nro_comprobante,
						row_number() OVER (partition by m.x_account_analytic_account_id, m.x_document_type, m.x_correlative) AS correlativo,
						mlp.date AS fecha_pago,
						0 AS vigencia,
						CASE WHEN p.payment_method_id = 6 THEN 1
							WHEN p.payment_method_id = 7 THEN 1
							WHEN p.payment_method_id = 8 THEN 2
							WHEN p.payment_method_id = 9 THEN 2
							WHEN p.payment_method_id = 10 THEN 3
							ELSE 0
						END AS medio_pago_senainfo,
						pm.name AS medio_pago,
						CASE WHEN ac.code::text = '360101'::character varying::text THEN (ml.price_total * -1)
						ELSE ml.price_total
						END AS monto,
						UPPER(p.x_name) AS glosa,
						CASE WHEN aa.code::text = '2130613'::character varying::text THEN ac.x_senainfo_institution_code ELSE ac.x_senainfo_project_code END AS cod_cuenta_senainfo,
						p.x_income_document_number::text AS nro_comprobante_pago,
						CASE WHEN m.x_document_type::text = 'EGRESO'::character varying::text THEN UPPER(rp.vat) ELSE '' END AS rut_beneficiario,
						CASE WHEN m.x_document_type::text = 'EGRESO'::character varying::text THEN UPPER(rp.name) ELSE '' END AS beneficiario,
						m.x_account_analytic_account_id AS x_account_analytic_account_id
					FROM account_move m
					INNER JOIN account_move_line ml ON m.id = ml.move_id
					LEFT JOIN account_analytic_account aa ON m.x_account_analytic_account_id = aa.id
					LEFT JOIN account_account ac ON ml.account_id = ac.id
					LEFT JOIN account_group ag ON ac.group_id = ag.id
					LEFT JOIN account_move_line mlr ON mlr.id IN (select id from account_move_line where move_id = ml.move_id and id <> ml.id)
					LEFT JOIN account_partial_reconcile pr ON mlr.id = pr.credit_move_id OR mlr.id = pr.debit_move_id
					LEFT JOIN account_move_line mlp ON mlp.id = pr.debit_move_id OR mlp.id = pr.credit_move_id
					LEFT JOIN account_payment p ON p.id = mlp.payment_id
					LEFT JOIN account_payment_method pm ON pm.id = p.payment_method_id
					LEFT JOIN res_partner rp ON rp.id = p.partner_id
					WHERE m.x_document_type IS NOT NULL
					AND ml.expense_id IS NULL
					AND ac.group_id IS NOT NULL
					AND p.is_reconciled is true
					UNION
					SELECT 
						0 AS tipo_docto_senainfo,
						m.x_document_type AS tipo_documento,
						aa.code AS cod_programa,
						aa.name AS programa,
						'6902' AS codigo_proyecto,
						ac.group_id AS cod_grupo,
						ag.name AS grupo,
						ac.id AS account_id,
						ac.code AS cod_cuenta,
						ac.name AS cuenta,
						ac.x_senainfo_name AS cuenta_senainfo,
						to_char(m.date, 'YYYYMM') AS periodo,
						m.x_back_up_document_number AS nro_docto_respaldo,
						CASE WHEN m.x_in_back_up_document_type IS NOT NULL THEN m.x_in_back_up_document_type
							WHEN m.x_out_back_up_document_type IS NOT NULL THEN m.x_out_back_up_document_type
							ELSE ''
						END AS tipo_docto_respaldo,
						m.date AS fecha_ingreso,
						m.x_correlative AS nro_comprobante,
						row_number() OVER (partition by m.x_account_analytic_account_id, m.x_document_type, m.x_correlative) AS correlativo,
						m.date AS fecha_pago,
						0 AS vigencia,
						CASE WHEN m.x_payment_method_id = 6 THEN 1
							WHEN m.x_payment_method_id = 7 THEN 1
							WHEN m.x_payment_method_id = 8 THEN 2
							WHEN m.x_payment_method_id = 9 THEN 2
							WHEN m.x_payment_method_id = 10 THEN 3
							ELSE 0
						END AS medio_pago_senainfo,
						pm.name AS medio_pago,
						CASE WHEN ac.code::text = '360101'::character varying::text THEN (he.total_amount * -1)
						ELSE he.total_amount
						END AS monto,
						UPPER(ml.name) AS glosa,
						CASE WHEN aa.code::text = '2130613'::character varying::text THEN ac.x_senainfo_institution_code ELSE ac.x_senainfo_project_code END AS cod_cuenta_senainfo,
						he.x_income_document_number::text AS nro_comprobante_pago,
						UPPER(m.x_rut_beneficiary) AS rut_beneficiario,
						UPPER(m.x_beneficiary) AS beneficiario,
						m.x_account_analytic_account_id AS x_account_analytic_account_id
					FROM account_move m
					INNER JOIN account_move_line ml ON m.id = ml.move_id
					LEFT JOIN account_analytic_account aa ON m.x_account_analytic_account_id = aa.id
					LEFT JOIN account_account ac ON ml.account_id = ac.id
					LEFT JOIN account_group ag ON ac.group_id = ag.id
					LEFT JOIN account_account acc ON ml.account_id = acc.id
					LEFT JOIN hr_expense_sheet hes ON m.id = hes.account_move_id
					LEFT JOIN hr_expense he ON ml.expense_id = he.id
					LEFT JOIN account_payment_method pm ON pm.id = m.x_payment_method_id
					WHERE ml.account_id in (
						select id from account_account
						where user_type_id in (select id from account_account_type where name = 'Expenses')
						)
					AND m.move_type = 'entry'
					AND hes.state = 'done'
					AND he.payment_mode = 'company_account') a
				ORDER BY a.tipo_docto_senainfo DESC, a.programa, a.nro_comprobante, a.correlativo
        """)
