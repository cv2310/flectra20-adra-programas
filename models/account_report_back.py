# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra import fields, models, tools


class AccountReportBack(models.Model):
    _name = "account.report.back"
    _description = "Accountability to SENAME"
    _auto = False
    _order = "programa, tipo_documento desc, nro_comprobante, correlativo"

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
    select 
           id,
           tipo_docto_senainfo,
           tipo_documento,
           cod_programa,
           programa,
           codigo_proyecto,
           cod_grupo,
           grupo,
           account_id,
           cod_cuenta,
           cuenta,
           cuenta_senainfo,
           periodo,
           nro_docto_respaldo,
           tipo_docto_respaldo,
           fecha_ingreso,
           nro_comprobante,
           correlativo,
           fecha_pago,
           vigencia,
           medio_pago_senainfo,
           medio_pago,
           monto,
           glosa,
           cod_cuenta_senainfo,
           nro_comprobante_pago,
           rut_beneficiario,
           beneficiario,
           x_account_analytic_account_id
    FROM account_export_v 
    ORDER BY programa, tipo_documento desc, nro_comprobante, correlativo
        """)
