# -*- coding: utf-8 -*-
import time
from flectra import api, models, _
from flectra.exceptions import UserError


class ReportGeneralLedgerData(models.AbstractModel):
    _name = 'report.general.ledger.data'
    LIBRO_BANCO = 'Libro Banco'
    RECONCILIACION_BANCO = 'Reconciliacion Banco'
    RENDICION_CUENTAS = 'RendiciOn de Cuentas'
    REPORTE_DJ1945 ='DJ1945'

    @staticmethod
    def getSqlBase():
        sql = ''' SELECT %s FROM
                 (   SELECT %s
               FROM account_move m
                 JOIN account_move_line ml ON m.id = ml.move_id
                 LEFT JOIN account_analytic_account aa ON m.x_account_analytic_account_id = aa.id
                 LEFT JOIN account_account ac ON ml.account_id = ac.id
                 LEFT JOIN account_group ag ON ac.group_id = ag.id
                 LEFT JOIN account_move_line mlr on (
                    EXISTS (SELECT 1
    			    FROM account_move_line as account_move_line3
    			    WHERE (account_move_line3.move_id = ml.move_id AND account_move_line3.id <> ml.id)
    			    AND (mlr.id = account_move_line3.id)))
                 LEFT JOIN account_partial_reconcile pr ON mlr.id = pr.credit_move_id OR mlr.id = pr.debit_move_id
                 LEFT JOIN account_move_line mlp ON mlp.id = pr.debit_move_id OR mlp.id = pr.credit_move_id
                 LEFT JOIN account_payment p ON p.id = mlp.payment_id
                 LEFT JOIN account_payment_method pm ON pm.id = p.payment_method_id
                 LEFT JOIN res_partner rp ON rp.id = p.partner_id
              WHERE %s m.x_document_type IS NOT NULL AND ml.expense_id IS NULL AND ac.group_id IS NOT NULL AND p.is_reconciled IS TRUE
            UNION ALL
             SELECT %s
               FROM account_move m
                 JOIN account_move_line ml ON m.id = ml.move_id
                 LEFT JOIN account_analytic_account aa ON m.x_account_analytic_account_id = aa.id
                 LEFT JOIN account_account ac ON ml.account_id = ac.id
                 LEFT JOIN account_group ag ON ac.group_id = ag.id
                 LEFT JOIN account_account acc ON ml.account_id = acc.id
                 LEFT JOIN hr_expense_sheet hes ON m.id = hes.account_move_id
                 LEFT JOIN hr_expense he ON ml.expense_id = he.id
                 LEFT JOIN account_payment_method pm ON pm.id = m.x_payment_method_id
              WHERE %s (ml.account_id IN ( SELECT account_account.id
                       FROM account_account
                      WHERE (account_account.user_type_id IN ( SELECT account_account_type.id
                               FROM account_account_type
                              WHERE account_account_type.name::text = 'Expenses'::text)))) AND m.move_type::text = 'entry'::text AND hes.state::text = 'done'::text AND he.payment_mode::text = 'company_account'::text
                ) arb '''
        return sql

    @staticmethod
    def getSqlOpen():
        sql = '''      SELECT {sqlFiled1}
                           FROM account_move m
                             JOIN account_move_line ml ON m.id = ml.move_id
                             LEFT JOIN account_analytic_account aa ON m.x_account_analytic_account_id = aa.id
                             LEFT JOIN account_account ac ON ml.account_id = ac.id
                             LEFT JOIN account_group ag ON ac.group_id = ag.id
                             LEFT JOIN account_move_line mlr on (
                                EXISTS (SELECT 1
                			    FROM account_move_line as account_move_line3
                			    WHERE (account_move_line3.move_id = ml.move_id AND account_move_line3.id <> ml.id)
                			    AND (mlr.id = account_move_line3.id)))
                             LEFT JOIN account_partial_reconcile pr ON mlr.id = pr.credit_move_id OR mlr.id = pr.debit_move_id
                             LEFT JOIN account_move_line mlp ON mlp.id = pr.debit_move_id OR mlp.id = pr.credit_move_id
                             LEFT JOIN account_payment p ON p.id = mlp.payment_id
                             LEFT JOIN account_payment_method pm ON pm.id = p.payment_method_id
                             LEFT JOIN res_partner rp ON rp.id = p.partner_id
                          WHERE {sqlWhere1} m.x_document_type IS NOT NULL AND ml.expense_id IS NULL AND ac.group_id IS NOT NULL AND p.is_reconciled IS TRUE
                        UNION ALL
                         SELECT {sqlFiled2}
                           FROM account_move m
                             JOIN account_move_line ml ON m.id = ml.move_id
                             LEFT JOIN account_analytic_account aa ON m.x_account_analytic_account_id = aa.id
                             LEFT JOIN account_account ac ON ml.account_id = ac.id
                             LEFT JOIN account_group ag ON ac.group_id = ag.id
                             LEFT JOIN account_account acc ON ml.account_id = acc.id
                             LEFT JOIN hr_expense_sheet hes ON m.id = hes.account_move_id
                             LEFT JOIN hr_expense he ON ml.expense_id = he.id
                             LEFT JOIN account_payment_method pm ON pm.id = m.x_payment_method_id
                          WHERE {sqlWhere2} (ml.account_id IN ( SELECT account_account.id
                                   FROM account_account
                                  WHERE (account_account.user_type_id IN ( SELECT account_account_type.id
                                           FROM account_account_type
                                          WHERE account_account_type.name::text = 'Expenses'::text)))) AND m.move_type::text = 'entry'::text AND hes.state::text = 'done'::text AND he.payment_mode::text = 'company_account'::text

                           '''
        return sql

    @staticmethod
    def getSqlClose():
        sql = '''
            SELECT {sqlField1}
            FROM account_report_v1
            WHERE {sqlWhere1}

            UNION ALL
            SELECT {sqlField2}
            FROM account_report_v2
            WHERE {sqlWhere2}
            '''
        return sql

    @staticmethod
    def getSqlHead():
        sql = ''' SELECT {sqlFiledBase} FROM
                     (   {sqlOpen}

                {unionAll}

                        {sqlClose}
                     ) arb '''
        return sql

    def datoTipo(self, date_from, date_close, date_to):
        if date_from <= date_close and date_close <= date_to:
            dato_tipo = "OPEN_CLOSE"
        if date_close < date_from:
            dato_tipo = "OPEN"
        if date_to < date_close:
            dato_tipo = "CLOSE"
        return dato_tipo

    def getSql(self, report_name, sql_nro, param):
        if report_name == self.RENDICION_CUENTAS:
            if sql_nro == 1:
                x_account_analytic_account_id = param['x_account_analytic_account_id']
                date_from = param['date_from']
                date_close = param['date_close']
                sqlFiledBase = "tipo_documento, sum(monto) as total"
                if date_close < date_from:
                    sqlFiled1 = '''m.x_document_type AS tipo_documento,\
                                    CASE
                                            WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                            ELSE ml.price_total
                                        END AS monto
                                    '''
                    sqlFiled2 = '''m.x_document_type AS tipo_documento,\
                                    CASE
                                            WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                            ELSE he.total_amount
                                        END AS monto
                                    '''
                    sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                              WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                              ELSE ml.price_total
                                          END AS monto
                                      '''
                    sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                      AND  '{date_close}' < mlp.date  AND mlp.date <'{date_from}' AND \
                                    '''
                    sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                     AND  '{date_close}' < m.date  AND m.date <  '{date_from}'  AND \
                                   '''
                    sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                                       sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen, unionAll='UNION ALL',
                                                       sqlClose='{sqlClose}')
                    sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                AND date <='{date_close}'  \
                                                '''
                else:
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                                       sqlClose='{sqlClose}')
                    sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                AND date <'{date_from}'  \
                                                '''

                sqlField = " tipo_documento, monto "
                sqlClose = self.getSqlClose().format(sqlField1=sqlField, sqlWhere1=sqlWhere,
                                                     sqlField2=sqlField, sqlWhere2=sqlWhere)
                sqlHead = sqlHead.format(sqlClose=sqlClose)
                sql = sqlHead + " GROUP BY tipo_documento"

            if sql_nro == 2:
                x_account_analytic_account_id = param['x_account_analytic_account_id']
                date_from = param['date_from']
                date_to = param['date_to']
                date_close = param['date_close']
                sqlFiledBase = "row_number() OVER () as id, grupo as cuenta_senainfo, sum(monto) as total"
                dato_tipo = self.datoTipo(date_from, date_close, date_to)
                if date_from <= date_close and date_close <= date_to:
                    dato_tipo = "OPEN_CLOSE"
                if date_close < date_from:
                    dato_tipo = "OPEN"
                if date_to < date_close:
                    dato_tipo = "CLOSE"
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "OPEN":
                    sqlFiled1 = '''ac.x_senainfo_group_name AS grupo, CASE
                                            WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                            ELSE ml.price_total
                                        END AS monto
                                    '''
                    sqlFiled2 = '''ac.x_senainfo_group_name AS grupo, CASE
                                            WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                            ELSE he.total_amount
                                        END AS monto
                                    '''

                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id} \
                                          AND m.x_document_type = 'INGRESO' \
                                          AND  '{date_close}' < mlp.date AND  mlp.date <= '{date_to}' AND \
                                        '''
                        sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND m.x_document_type = 'INGRESO' \
                                          AND '{date_close}' < m.date  AND m.date  <= '{date_to}' AND\
                                          '''
                    else:
                        sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                            AND m.x_document_type = 'INGRESO' \
                                            AND mlp.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                            '''
                        sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                            AND m.x_document_type = 'INGRESO' \
                                            AND m.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                              '''
                    sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                                       sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
                    if dato_tipo == "OPEN_CLOSE":
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='UNION ALL',
                                                           sqlClose='{sqlClose}')
                    else:
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='',
                                                           sqlClose='')
                if dato_tipo == "CLOSE":
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                                       sqlClose='{sqlClose}')
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "CLOSE":
                    sqlField = " x_senainfo_group_name as grupo, monto"

                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                            AND tipo_documento = 'INGRESO' \
                                          AND date BETWEEN '{date_from}' AND '{date_close}' \
                                        '''
                    else:
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                        AND tipo_documento = 'INGRESO' \
                                          AND date BETWEEN '{date_from}' AND '{date_to}' \
                                        '''
                    sqlClose = self.getSqlClose().format(sqlField1=sqlField, sqlWhere1=sqlWhere,
                                                         sqlField2=sqlField, sqlWhere2=sqlWhere)
                    sqlHead = sqlHead.format(sqlClose=sqlClose)
                sql = sqlHead + " GROUP BY grupo "

            if sql_nro == 3:
                x_account_analytic_account_id = param['x_account_analytic_account_id']
                date_from = param['date_from']
                date_to = param['date_to']
                date_close = param['date_close']
                sqlFiledBase = "row_number() OVER () as id, grupo as cuenta_senainfo, sum(monto) as total"

                dato_tipo = self.datoTipo(date_from, date_close, date_to)
                if date_from <= date_close and date_close <= date_to:
                    dato_tipo = "OPEN_CLOSE"
                if date_close < date_from:
                    dato_tipo = "OPEN"
                if date_to < date_close:
                    dato_tipo = "CLOSE"
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "OPEN":
                    sqlFiled1 = '''ac.x_senainfo_group_name AS grupo, CASE
                                                   WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                                   ELSE ml.price_total
                                               END AS monto
                                           '''
                    sqlFiled2 = '''ac.x_senainfo_group_name AS grupo, CASE
                                                   WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                                   ELSE he.total_amount
                                               END AS monto
                                           '''
                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id} \
                                          AND m.x_document_type = 'EGRESO' \
                                          AND  '{date_close}' < mlp.date AND  mlp.date <= '{date_to}' AND \
                                        '''
                        sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND m.x_document_type = 'EGRESO' \
                                          AND '{date_close}' < m.date  AND m.date  <= '{date_to}' AND\
                                          '''
                    else:
                        sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                            AND m.x_document_type = 'EGRESO' \
                                            AND mlp.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                            '''
                        sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                            AND m.x_document_type = 'EGRESO' \
                                            AND m.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                              '''
                    sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                                       sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
                    if dato_tipo == "OPEN_CLOSE":
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='UNION ALL',
                                                           sqlClose='{sqlClose}')
                    else:
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='',
                                                           sqlClose='')
                if dato_tipo == "CLOSE":
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                                       sqlClose='{sqlClose}')
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "CLOSE":
                    sqlField = " x_senainfo_group_name as grupo, monto"

                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                            AND tipo_documento = 'EGRESO' \
                                          AND date BETWEEN '{date_from}' AND '{date_close}' \
                                        '''
                    else:
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                        AND tipo_documento = 'EGRESO' \
                                          AND date BETWEEN '{date_from}' AND '{date_to}' \
                                        '''
                    sqlClose = self.getSqlClose().format(sqlField1=sqlField, sqlWhere1=sqlWhere,
                                                         sqlField2=sqlField, sqlWhere2=sqlWhere)
                    sqlHead = sqlHead.format(sqlClose=sqlClose)
                sql = sqlHead + " GROUP BY grupo "

        if report_name == self.RECONCILIACION_BANCO:
            if sql_nro == 1:
                x_account_analytic_account_id = param['x_account_analytic_account_id']
                date_from = param['date_from']
                date_close = param['date_close']
                sqlFiledBase = "tipo_documento, sum(monto) as total"
                if date_close < date_from:
                    sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                              WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                              ELSE ml.price_total
                                          END AS monto
                                      '''
                    sqlFiled2 = '''m.x_document_type AS tipo_documento,             
                                          CASE
                                              WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                              ELSE he.total_amount
                                          END AS monto
                                      '''
                    sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                      AND  '{date_close}' < mlp.date  AND mlp.date <'{date_from}' AND \
                                    '''
                    sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                     AND  '{date_close}' < m.date  AND m.date <  '{date_from}'  AND \
                                   '''
                    sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                                       sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen, unionAll='UNION ALL',
                                                       sqlClose='{sqlClose}')
                    sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                     AND date <='{date_close}'  \
                                                     '''
                else:
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                                       sqlClose='{sqlClose}')
                    sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                     AND date <'{date_from}'  \
                                                     '''

                sqlField = " tipo_documento, monto "

                sqlClose = self.getSqlClose().format(sqlField1=sqlField, sqlWhere1=sqlWhere,
                                                     sqlField2=sqlField, sqlWhere2=sqlWhere)
                sqlHead = sqlHead.format(sqlClose=sqlClose)
                sql = sqlHead + " GROUP BY tipo_documento"
            if sql_nro == 2:
                x_account_analytic_account_id = param['x_account_analytic_account_id']
                date_from = param['date_from']
                date_to = param['date_to']
                date_close = param['date_close']
                sqlFiledBase = "tipo_documento, sum(monto) as total"
                dato_tipo = self.datoTipo(date_from, date_close, date_to)
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "OPEN":
                    sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                            WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                            ELSE ml.price_total
                                        END AS monto
                                    '''
                    sqlFiled2 = '''m.x_document_type AS tipo_documento, CASE
                                            WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                            ELSE he.total_amount
                                        END AS monto
                                    '''
                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND  '{date_close}' < mlp.date AND  mlp.date <= '{date_to}' AND\
                                        '''
                        sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND '{date_close}' < m.date  AND m.date  <= '{date_to}' AND\
                                          '''
                    else:
                        sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND mlp.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                        '''
                        sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND m.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                          '''
                    sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                                       sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
                    if dato_tipo == "OPEN_CLOSE":
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='UNION ALL',
                                                           sqlClose='{sqlClose}')
                    else:
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='',
                                                           sqlClose='')
                if dato_tipo == "CLOSE":
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                                       sqlClose='{sqlClose}')
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "CLOSE":
                    sqlField = "tipo_documento, monto"
                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND date BETWEEN '{date_from}' AND '{date_close}' \
                                        '''
                    else:
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                                  AND date BETWEEN '{date_from}' AND '{date_to}' \
                                                                '''
                    sqlClose = self.getSqlClose().format(sqlField1=sqlField, sqlWhere1=sqlWhere,
                                                         sqlField2=sqlField, sqlWhere2=sqlWhere)
                    sqlHead = sqlHead.format(sqlClose=sqlClose)
                sql = sqlHead + " GROUP BY tipo_documento"
            if sql_nro == 3:
                x_account_analytic_account_id = param['x_account_analytic_account_id']
                date_from = param['date_from']
                date_to = param['date_to']
                date_close = param['date_close']
                x_sort_by = param['x_sort_by']
                sqlFiledBase = 'row_number() OVER () as id, documento, nro_cheque,fecha_pago, monto, beneficiario, referencia'
                dato_tipo = self.datoTipo(date_from, date_close, date_to)
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "OPEN":
                    sql_base = f'''SELECT row_number() OVER () as id, m2.x_name AS documento, p.x_income_document_number AS nro_cheque,\
                            m.date AS fecha_pago, p.amount AS monto, m.invoice_partner_display_name AS beneficiario, p.x_name AS referencia\
                            FROM account_payment p\
                            LEFT JOIN account_move m ON (m.payment_id = p.id)\
                            LEFT JOIN account_move m2 ON (m.ref = m2.name)\
                            WHERE p.x_is_charged = FALSE\
                            AND m2.x_account_analytic_account_id = %s\
                            AND m.date BETWEEN %s AND %s\
                            '''
                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere = f''' m2.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND '{date_close}' < m.date  AND m.date  <= '{date_to}' \
                                          '''
                    else:
                        sqlWhere = f''' m2.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                                  AND m.date BETWEEN '{date_from}' AND '{date_to}' \
                                                                  '''
                    sqlOpen = f'''SELECT row_number() OVER () as id, m2.x_name AS documento, p.x_income_document_number AS nro_cheque,\
                            m.date AS fecha_pago, p.amount AS monto, m.invoice_partner_display_name AS beneficiario, p.x_name AS referencia\
                            FROM account_payment p\
                            LEFT JOIN account_move m ON (m.payment_id = p.id)\
                            LEFT JOIN account_move m2 ON (m.ref = m2.name)\
                            WHERE p.x_is_charged = FALSE\
                            AND {sqlWhere}\
                            '''
                    if dato_tipo == "OPEN_CLOSE":
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='UNION ALL',
                                                           sqlClose='{sqlClose}')
                    else:
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='',
                                                           sqlClose='')
                if dato_tipo == "CLOSE":
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                                       sqlClose='{sqlClose}')
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "CLOSE":
                    sqlFiled = 'row_number() OVER () as id, documento, nro_cheque, date as fecha_pago, monto, beneficiario, referencia'
                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND date BETWEEN '{date_from}' AND '{date_close}' \
                                        '''
                    else:
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                                  AND date BETWEEN '{date_from}' AND '{date_to}' \
                                        '''
                    sqlClose = f''' select {sqlFiled} 
                                        from account_bank_reconciliation_v
                                        where {sqlWhere} 
                                    '''
                    sqlHead = sqlHead.format(sqlClose=sqlClose)
                sql = sqlHead + ' ORDER BY ' + x_sort_by

        if report_name == self.LIBRO_BANCO:
            if sql_nro == 1:
                x_account_analytic_account_id = param['x_account_analytic_account_id']
                date_from = param['date_from']
                date_close = param['date_close']
                sqlFiledBase = "tipo_documento, sum(monto) as saldo"
                if date_close < date_from:
                    sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                              WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                              ELSE ml.price_total
                                          END AS monto
                                      '''
                    sqlFiled2 = '''m.x_document_type AS tipo_documento,             
                                          CASE
                                              WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                              ELSE he.total_amount
                                          END AS monto
                                      '''
                    sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                      AND  '{date_close}' < mlp.date  AND mlp.date <'{date_from}' AND \
                                    '''
                    sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                     AND  '{date_close}' < m.date  AND m.date <  '{date_from}'  AND \
                                   '''
                    sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                                       sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen, unionAll='UNION ALL',
                                                       sqlClose='{sqlClose}')

                    sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                 AND date <='{date_close}'  \
                                                 '''

                else:
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                                       sqlClose='{sqlClose}')
                    sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                 AND date <'{date_from}'  \
                                                 '''

                sqlField = " tipo_documento, monto "

                sqlClose = self.getSqlClose().format(sqlField1=sqlField, sqlWhere1=sqlWhere,
                                                     sqlField2=sqlField, sqlWhere2=sqlWhere)
                sqlHead = sqlHead.format(sqlClose=sqlClose)
                sql = sqlHead + " GROUP BY tipo_documento"
            if sql_nro == 2:
                x_account_analytic_account_id = param['x_account_analytic_account_id']
                date_from = param['date_from']
                date_to = param['date_to']
                date_close = param['date_close']
                x_sort_by = param['x_sort_by']
                sqlFiledBase = '''row_number() OVER () as id, tipo_documento, fecha_ingreso, nro_comprobante, medio_pago, nro_comprobante_pago, fecha_pago, glosa, beneficiario,\
                                                      CASE tipo_documento WHEN 'INGRESO' THEN monto ELSE 0 END AS ingreso,\
                                                      CASE tipo_documento WHEN 'EGRESO' THEN monto ELSE 0 END AS egreso\
                                                      '''
                if date_from <= date_close and date_close <= date_to:
                    dato_tipo = "OPEN_CLOSE"
                if date_close < date_from:
                    dato_tipo = "OPEN"
                if date_to < date_close:
                    dato_tipo = "CLOSE"
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "OPEN":

                    sqlFiled1 = '''row_number() OVER () as id, m.x_document_type AS tipo_documento, m.invoice_date AS fecha_ingreso,  m.x_correlative AS nro_comprobante,  pm.name AS medio_pago, p.x_income_document_number::text AS nro_comprobante_pago,  mlp.date AS fecha_pago, upper(p.x_name::text) AS glosa, CASE
                                              WHEN m.x_document_type::text = 'EGRESO'::character varying::text THEN upper(rp.name::text)
                                              ELSE upper(rp.name::text)
                                          END AS beneficiario,\
                                      CASE
                                              WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                              ELSE ml.price_total
                                          END AS monto
                                      '''

                    sqlFiled2 = '''row_number() OVER () as id, m.x_document_type as tipo_documento,m.invoice_date AS fecha_ingreso,  m.x_correlative AS nro_comprobante,  pm.name AS medio_pago, he.x_income_document_number::text AS nro_comprobante_pago, m.invoice_date AS fecha_pago,  upper(ml.name::text) AS glosa,  upper(m.x_beneficiary::text) AS beneficiario,\
                                      CASE
                                              WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                              ELSE he.total_amount
                                          END AS monto
                                      '''
                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND  '{date_close}' < mlp.date AND  mlp.date <= '{date_to}' AND\
                                        '''
                        sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND '{date_close}' < m.date  AND m.date  <= '{date_to}' AND\
                                          '''
                    else:
                        sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                                  AND mlp.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                                                '''
                        sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                                  AND m.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                                                  '''
                    sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                                       sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
                    if dato_tipo == "OPEN_CLOSE":
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='UNION ALL',
                                                           sqlClose='{sqlClose}')
                    else:
                        sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                           unionAll='',
                                                           sqlClose='')
                if dato_tipo == "CLOSE":
                    sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                                       sqlClose='{sqlClose}')
                if dato_tipo == "OPEN_CLOSE" or dato_tipo == "CLOSE":
                    sqlField1 = 'row_number() OVER () as id, tipo_documento,  fecha_ingreso,  nro_comprobante, medio_pago,  nro_comprobante_pago, date AS fecha_pago,  glosa, beneficiario, monto'
                    sqlField2 = 'row_number() OVER () as id, tipo_documento,  fecha_ingreso,  nro_comprobante, medio_pago,  nro_comprobante_pago, fecha_pago,  glosa, beneficiario, monto'

                    if dato_tipo == "OPEN_CLOSE":
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                          AND date BETWEEN '{date_from}' AND '{date_close}' \
                                        '''
                    else:
                        sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id}\
                                                                  AND date BETWEEN '{date_from}' AND '{date_to}' \
                                                                '''
                    sqlClose = self.getSqlClose().format(sqlField1=sqlField1, sqlWhere1=sqlWhere,
                                                         sqlField2=sqlField2, sqlWhere2=sqlWhere)
                    sqlHead = sqlHead.format(sqlClose=sqlClose)
                sql = sqlHead + " ORDER BY " + x_sort_by + ", nro_comprobante "
        return sql

    #reporte de hasto trismestra
    def _get_quarterly_report_data(self, date_from, date_to, date_close, month):

        sqlFiledBase = '''row_number() OVER () as id,  project, code , DATE_TRUNC('month', date) AS date, sum(monto) as expense\
                                                 '''
        if date_from <= date_close and date_close <= date_to:
            dato_tipo = "OPEN_CLOSE"
        if date_close < date_from:
            dato_tipo = "OPEN"
        if date_to < date_close:
            dato_tipo = "CLOSE"
        if dato_tipo == "OPEN_CLOSE" or dato_tipo == "OPEN":

            sqlFiled1 = '''row_number() OVER () as id,  
                                     aa.name as project,
                                     aa.code as code,
                                     mlp.date AS date,
                                     CASE
                                         WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                         ELSE ml.price_total
                                     END AS monto
                                 '''

            sqlFiled2 = '''row_number() OVER () as id,  
                                     aa.name as project,
                                     aa.code as code,
                                     m.date AS date,
                                 CASE
                                         WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                         ELSE he.total_amount
                                     END AS monto
                                 '''
            if dato_tipo == "OPEN_CLOSE":
                sqlWhere1 = f'''  m.x_document_type = 'EGRESO' AND '{date_close}' < mlp.date AND  mlp.date <= '{date_to}' AND\
                                   '''
                sqlWhere2 = f'''  m.x_document_type = 'EGRESO' AND '{date_close}' < m.date  AND m.date  <= '{date_to}' AND\
                                     '''
            else:
                sqlWhere1 = f'''  m.x_document_type = 'EGRESO' AND mlp.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                                           '''
                sqlWhere2 = f'''  m.x_document_type = 'EGRESO' AND m.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                                             '''
            sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                               sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
            if dato_tipo == "OPEN_CLOSE":
                sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                   unionAll='UNION ALL',
                                                   sqlClose='{sqlClose}')
            else:
                sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                   unionAll='',
                                                   sqlClose='')
        if dato_tipo == "CLOSE":
            sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                               sqlClose='{sqlClose}')
        if dato_tipo == "OPEN_CLOSE" or dato_tipo == "CLOSE":
            sqlField1 = 'row_number() OVER () as id,  x_account_analytic_account_name as project, x_account_analytic_account_code as code, date, monto'
            sqlField2 = 'row_number() OVER () as id,  x_account_analytic_account_name as project, x_account_analytic_account_code as code, date, monto'

            if dato_tipo == "OPEN_CLOSE":
                sqlWhere = f'''  tipo_documento = 'EGRESO' AND date BETWEEN '{date_from}' AND '{date_close}' \
                                   '''
            else:
                sqlWhere = f'''  tipo_documento = 'EGRESO' AND date BETWEEN '{date_from}' AND '{date_to}' \
                                                           '''
            sqlClose = self.getSqlClose().format(sqlField1=sqlField1, sqlWhere1=sqlWhere,
                                                 sqlField2=sqlField2, sqlWhere2=sqlWhere)
            sqlHead = sqlHead.format(sqlClose=sqlClose)
        sqlNew = sqlHead + " GROUP BY  project, code , DATE_TRUNC('month',date) "
        cr = self.env.cr
        cr.execute(sqlNew)
        projects = []
        for row in cr.dictfetchall():
            year_month = month[row['date'].strftime("%Y-%m")]
            self.add_trimestre(projects, row['code'], row['project'], year_month, row['expense'])
        return projects

    def add_trimestre(self, projects, project_code, project_name, month, gasto):
        for project in projects:
            if project['code'] == project_code:
                project[month] = gasto
                return True
        project={'project': project_name,
                  'code':project_code,
                  'month_01':0,
                  'month_02':0,
                  'month_03':0}
        project[month] = gasto
        projects.append(project)
        return False
    #  presupuesto
    def _get_budget_report_data(self,x_account_analytic_account_id, date_from, date_to, date_close):

        ingresos = [
            {'tipo I': 'tipo i 1', 'mes_01': 24, 'mes_02': 4500, 'mes_03': 24, 'mes_04': 4500, 'mes_05': 24, 'mes_06': 4500, 'mes_07': 24, 'mes_08': 4500, 'mes_09': 24, 'mes_10': 4500, 'mes_11': 24, 'mes_12': 4500, 'mes_total': 10000},
            {'tipo I 1': 'tipo i 2', 'mes_01': 24, 'mes_02': 4500, 'mes_03': 24, 'mes_04': 4500, 'mes_05': 24, 'mes_06': 4500, 'mes_07': 24, 'mes_08': 4500, 'mes_09': 24, 'mes_10': 4500, 'mes_11': 24, 'mes_12': 4500, 'mes_total': 10000},
            {'tipo I 2': 'tipo i 3', 'mes_01': 24, 'mes_02': 4500, 'mes_03': 24, 'mes_04': 4500, 'mes_05': 24, 'mes_06': 4500, 'mes_07': 24, 'mes_08': 4500, 'mes_09': 24, 'mes_10': 4500, 'mes_11': 24, 'mes_12': 4500, 'mes_total': 10000},
        ]
        ingresos_total = [
            {'mes_01': 24, 'mes_02': 4500, 'mes_03': 24, 'mes_04': 4500, 'mes_05': 24, 'mes_06': 4500, 'mes_07': 24, 'mes_08': 4500, 'mes_09': 24, 'mes_10': 4500, 'mes_11': 24, 'mes_12': 4500, 'mes_total': 10000},
                   ]
        gastos = [
            {'tipo G': 'tipo g 1', 'mes_01': 24, 'mes_02': 4500, 'mes_03': 24, 'mes_04': 4500, 'mes_05': 24, 'mes_06': 4500, 'mes_07': 24, 'mes_08': 4500, 'mes_09': 24, 'mes_10': 4500, 'mes_11': 24, 'mes_12': 4500, 'mes_total': 10000},
            {'tipo G 1': 'tipo g 2', 'mes_01': 24, 'mes_02': 4500, 'mes_03': 24, 'mes_04': 4500, 'mes_05': 24, 'mes_06': 4500, 'mes_07': 24, 'mes_08': 4500, 'mes_09': 24, 'mes_10': 4500, 'mes_11': 24, 'mes_12': 4500, 'mes_total': 10000},
            {'tipo G 2': 'tipo g 3', 'mes_01': 24, 'mes_02': 4500, 'mes_03': 24, 'mes_04': 4500, 'mes_05': 24, 'mes_06': 4500, 'mes_07': 24, 'mes_08': 4500, 'mes_09': 24, 'mes_10': 4500, 'mes_11': 24, 'mes_12': 4500, 'mes_total': 10000},
        ]
        gastos_total = [
            {'mes_01': 24, 'mes_02': 4500, 'mes_03': 24, 'mes_04': 4500, 'mes_05': 24, 'mes_06': 4500, 'mes_07': 24, 'mes_08': 4500, 'mes_09': 24, 'mes_10': 4500, 'mes_11': 24, 'mes_12': 4500, 'mes_total': 10000},
            ]
        return { 'ingreso': ingresos, 'ingresos_total': ingresos_total, 'gastos':gastos, 'gastos_total': gastos_total}

        sqlFiledBase = '''row_number() OVER () as id, account_type, account, sum(monto) as expense\
                                              '''
        if date_from <= date_close and date_close <= date_to:
            dato_tipo = "OPEN_CLOSE"
        if date_close < date_from:
            dato_tipo = "OPEN"
        if date_to < date_close:
            dato_tipo = "CLOSE"
        if dato_tipo == "OPEN_CLOSE" or dato_tipo == "OPEN":

            sqlFiled1 = '''row_number() OVER () as id,  
                                  ag.name as account_type,
                                  ac.name as account,
                                  CASE
                                      WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                      ELSE ml.price_total
                                  END AS monto
                              '''

            sqlFiled2 = '''row_number() OVER () as id,  
                                    ag.name as account_type,
                                  ac.name as account,
                              CASE
                                      WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                      ELSE he.total_amount
                                  END AS monto
                              '''
            if dato_tipo == "OPEN_CLOSE":
                sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id} AND m.x_document_type = 'EGRESO' AND '{date_close}' < mlp.date AND  mlp.date <= '{date_to}' AND\
                                '''
                sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id} AND m.x_document_type = 'EGRESO' AND '{date_close}' < m.date  AND m.date  <= '{date_to}' AND\
                                  '''
            else:
                sqlWhere1 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id} AND m.x_document_type = 'EGRESO' AND mlp.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                                        '''
                sqlWhere2 = f''' m.x_account_analytic_account_id = {x_account_analytic_account_id} AND m.x_document_type = 'EGRESO' AND m.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                                          '''
            sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                               sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
            if dato_tipo == "OPEN_CLOSE":
                sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                   unionAll='UNION ALL',
                                                   sqlClose='{sqlClose}')
            else:
                sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                   unionAll='',
                                                   sqlClose='')
        if dato_tipo == "CLOSE":
            sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                               sqlClose='{sqlClose}')
        if dato_tipo == "OPEN_CLOSE" or dato_tipo == "CLOSE":
            sqlField1 = 'row_number() OVER () as id,  grupo_name as account_type, account as account, monto'
            sqlField2 = 'row_number() OVER () as id,  grupo_name as account_type, account as account, monto'

            if dato_tipo == "OPEN_CLOSE":
                sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id} AND tipo_documento = 'EGRESO' AND date BETWEEN '{date_from}' AND '{date_close}' \
                                '''
            else:
                sqlWhere = f''' x_account_analytic_account_id = {x_account_analytic_account_id} AND tipo_documento = 'EGRESO' AND date BETWEEN '{date_from}' AND '{date_to}' \
                                                        '''
            sqlClose = self.getSqlClose().format(sqlField1=sqlField1, sqlWhere1=sqlWhere,
                                                 sqlField2=sqlField2, sqlWhere2=sqlWhere)
            sqlHead = sqlHead.format(sqlClose=sqlClose)
        sqlNew = sqlHead + " GROUP BY  account_type,account "
        cr = self.env.cr
        cr.execute(sqlNew)

        move_lines = []
        for row in cr.dictfetchall():
            line = {}
            line['account_type'] = row['account_type']
            line['account'] = row['account']
            line['expense'] = row['expense']
            move_lines.append(line)
        return move_lines

    #  DJ1945
    def _get_DJ1945_data(self, date_from, date_to, date_close):

        sqlFiledBase = '''row_number() OVER () as id, beneficiario, rut, sum(monto) as total\
                                                 '''
        if date_from <= date_close and date_close <= date_to:
            dato_tipo = "OPEN_CLOSE"
        if date_close < date_from:
            dato_tipo = "OPEN"
        if date_to < date_close:
            dato_tipo = "CLOSE"
        if dato_tipo == "OPEN_CLOSE" or dato_tipo == "OPEN":

            sqlFiled1 = '''row_number() OVER () as id,  
                                     upper(rp.name::text)AS beneficiario,
                                     rp.vat as rut,\
                                     CASE
                                         WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                         ELSE ml.price_total
                                     END AS monto
                                 '''

            sqlFiled2 = '''row_number() OVER () as id,  
                               upper(m.x_beneficiary::text) AS beneficiario,\
                               upper(m.x_rut_beneficiary::text) AS rut,\
                                 CASE
                                         WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                         ELSE he.total_amount
                                     END AS monto
                                 '''
            if dato_tipo == "OPEN_CLOSE":
                sqlWhere1 = f'''   m.x_document_type = 'EGRESO' AND '{date_close}' < mlp.date AND  mlp.date <= '{date_to}' AND\
                                   '''
                sqlWhere2 = f''' m.x_document_type = 'EGRESO' AND '{date_close}' < m.date  AND m.date  <= '{date_to}' AND\
                                     '''
            else:
                sqlWhere1 = f''' m.x_document_type = 'EGRESO' AND mlp.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                                           '''
                sqlWhere2 = f''' m.x_document_type = 'EGRESO' AND m.date BETWEEN '{date_from}' AND '{date_to}' AND\
                                                             '''
            sqlOpen = self.getSqlOpen().format(sqlFiled1=sqlFiled1, sqlWhere1=sqlWhere1,
                                               sqlFiled2=sqlFiled2, sqlWhere2=sqlWhere2)
            if dato_tipo == "OPEN_CLOSE":
                sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                   unionAll='UNION ALL',
                                                   sqlClose='{sqlClose}')
            else:
                sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen=sqlOpen,
                                                   unionAll='',
                                                   sqlClose='')
        if dato_tipo == "CLOSE":
            sqlHead = self.getSqlHead().format(sqlFiledBase=sqlFiledBase, sqlOpen='', unionAll='',
                                               sqlClose='{sqlClose}')
        if dato_tipo == "OPEN_CLOSE" or dato_tipo == "CLOSE":
            sqlField1 = 'row_number() OVER () as id,  beneficiario, rut, monto'
            sqlField2 = 'row_number() OVER () as id,  beneficiario, rut, monto'

            if dato_tipo == "OPEN_CLOSE":
                sqlWhere = f''' tipo_documento = 'EGRESO' AND date BETWEEN '{date_from}' AND '{date_close}' \
                                   '''
            else:
                sqlWhere = f''' tipo_documento = 'EGRESO' AND date BETWEEN '{date_from}' AND '{date_to}' \
                                                           '''
            sqlClose = self.getSqlClose().format(sqlField1=sqlField1, sqlWhere1=sqlWhere,
                                                 sqlField2=sqlField2, sqlWhere2=sqlWhere)
            sqlHead = sqlHead.format(sqlClose=sqlClose)
        sqlNew = sqlHead + " GROUP BY beneficiario, rut "
        cr = self.env.cr
        cr.execute(sqlNew)
        # SQL 2
        # cr.execute(sqlNew)

        total_income_from_period = 0
        move_lines = []
        for row in cr.dictfetchall():
            line = {}
            line['beneficiario'] = row['beneficiario']
            line['rut'] = row['rut']
            line['total'] = row['total']
            move_lines.append(line)
        return move_lines

    #ASINET
    def _get_asinet_data(self, date_from, date_to, date_close):
        proyectos = self.env['account.analytic.account'].search([])

        asinets=[]
        for proyecto in proyectos:
            if proyecto.code != '6902':
                #'2023-04-30'
                sql_param = {
                    'x_account_analytic_account_id': proyecto.id,
                    'date_from': date_from,
                    'date_to': date_to,
                    'date_close': date_close,
                }
                cr = self.env.cr
                sqlNew = self.getSql(self.RENDICION_CUENTAS, 2, sql_param)
                cr.execute(sqlNew)
                # SQL 2
                # cr.execute(sqlNew)
                move_lines_income = []
                total_income_from_period = 0
                for row in cr.dictfetchall():
                    line = {}
                    line['id'] = row['id']
                    line['cuenta_senainfo'] = row['cuenta_senainfo']
                    line['total'] = row['total']
                    move_lines_income.append(line)
                    total_income_from_period += row['total']
                #1112001 + T
                #2151025 -
                if move_lines_income:
                    asinet = {}
                    asinet['Project'] = proyecto.name
                    asinet['AccountCode'] = 1112001
                    asinet['SubAccountCode'] = proyecto.x_sub_account_code_expense
                    asinet['FundCode'] = 10
                    asinet['FunctionCode'] = proyecto.x_function_code
                    asinet['RestrictionCode'] = '0A'
                    asinet['EntityValue'] = total_income_from_period
                    asinet['SendMemo'] = 'False'
                    asinet['Description'] = 'TOTAL INGRESO -'
                    asinets.append(asinet)
                    for line in move_lines_income:
                        asinet = {}
                        asinet['Project'] = proyecto.name
                        asinet['AccountCode'] = 2151025
                        asinet['SubAccountCode'] = proyecto.x_sub_account_code_income
                        asinet['FundCode'] = 10
                        asinet['FunctionCode'] = proyecto.x_function_code
                        asinet['RestrictionCode'] = '0A'
                        asinet['EntityValue'] = -1 * line['total']
                        asinet['SendMemo'] = 'False'
                        if line['cuenta_senainfo']:
                            asinet['Description'] = 'TOTAL ' + line['cuenta_senainfo'] +  ' -'
                        else:
                            asinet['Description'] = 'TOTAL ' +  ' -'
                        asinets.append(asinet)

                cr = self.env.cr
                sqlNew = self.getSql(self.RENDICION_CUENTAS, 3, sql_param)
                cr.execute(sqlNew)
                # SQL 3
                # cr.execute(sql, params)
                total_expenses_from_period = 0
                move_lines_expenses = []
                for row in cr.dictfetchall():
                    line = dict((fn, (0)) for fn in ['id'])
                    line['id'] = row['id']
                    line['cuenta_senainfo'] = row['cuenta_senainfo']
                    line['total'] = row['total']
                    move_lines_expenses.append(line)
                    total_expenses_from_period += row['total']
                # 2151025 -
                # 1112001 + T
                if move_lines_expenses:
                    for line in move_lines_expenses:
                        asinet = {}
                        asinet['Project'] = proyecto.name
                        asinet['AccountCode'] = 2151025
                        asinet['SubAccountCode'] = proyecto.x_sub_account_code_income
                        asinet['FundCode'] = 10
                        asinet['FunctionCode'] = proyecto.x_function_code
                        asinet['RestrictionCode'] = '0A'
                        asinet['EntityValue'] = line['total']
                        asinet['SendMemo'] = 'False'
                        if line['cuenta_senainfo']:
                            asinet['Description'] = 'TOTAL ' + line['cuenta_senainfo'] + ' -'
                        else:
                            asinet['Description'] = 'TOTAL ' + ' -'
                        asinets.append(asinet)
                    asinet = {}
                    asinet['Project'] = proyecto.name
                    asinet['AccountCode'] = 1112001
                    asinet['SubAccountCode'] = proyecto.x_sub_account_code_expense
                    asinet['FundCode'] = 10
                    asinet['FunctionCode'] = proyecto.x_function_code
                    asinet['RestrictionCode'] = '0A'
                    asinet['EntityValue'] = -1 * total_expenses_from_period
                    asinet['SendMemo'] = 'False'
                    asinet['Description'] = 'TOTAL EGRESO -'
                    asinets.append(asinet)
        return asinets

    # income/expense ledger - Libro Ingresos - Libro Egresos
    def _get_mayor_ledger_entries(self, accounts, x_account_analytic_account_id, x_sort_by, x_report_type,
                                  x_document_type):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        account_res = []

        if x_report_type == 'cuenta':

            # Get movements of mayor ledger
            sqlFiled = ''' grupo, account_id, cod_cuenta, nro_comprobante,\
                    tipo_docto_respaldo, nro_docto_respaldo, beneficiario, medio_pago,\
                    nro_comprobante_pago, fecha_pago, glosa, monto, monto as total\
                    '''

            sql = ('''SELECT grupo, account_id, cod_cuenta, nro_comprobante,\
                    tipo_docto_respaldo, nro_docto_respaldo, beneficiario, medio_pago,\
                    nro_comprobante_pago, fecha_pago, glosa, monto, monto as total\
                    FROM account_report_back\
                    WHERE tipo_documento = %s\
                    AND x_account_analytic_account_id = %s\
                    AND fecha_ingreso BETWEEN %s AND %s\
                    ORDER BY account_id, ''' + x_sort_by)

            sqlFiledBase = ''' grupo, account_id, cod_cuenta, nro_comprobante,\
                                tipo_docto_respaldo, nro_docto_respaldo, beneficiario, medio_pago,\
                                nro_comprobante_pago, fecha_pago, glosa, monto, monto as total\
                                '''

            sqlFiled1 = ''' ag.name AS grupo, ac.id AS account_id, ac.code AS cod_cuenta,  m.x_correlative AS nro_comprobante,\
                                CASE
                                    WHEN m.x_in_back_up_document_type IS NOT NULL THEN m.x_in_back_up_document_type
                                    WHEN m.x_out_back_up_document_type IS NOT NULL THEN m.x_out_back_up_document_type
                                    ELSE ''::character varying
                                END AS tipo_docto_respaldo,  m.x_back_up_document_number AS nro_docto_respaldo,  CASE
                                    WHEN m.x_document_type::text = 'EGRESO'::character varying::text THEN upper(rp.name::text)
                                    ELSE upper(rp.name::text)
                                END AS beneficiario,  pm.name AS medio_pago,\
                                p.x_income_document_number::text AS nro_comprobante_pago, mlp.date AS fecha_pago, upper(p.x_name::text) AS glosa, CASE
                                    WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                    ELSE ml.price_total
                                END AS monto\
                                '''

            sqlFiled2 = ''' ag.name AS grupo, ac.id AS account_id, ac.code AS cod_cuenta, m.x_correlative AS nro_comprobante,\
                                CASE
                                    WHEN m.x_in_back_up_document_type IS NOT NULL THEN m.x_in_back_up_document_type
                                    WHEN m.x_out_back_up_document_type IS NOT NULL THEN m.x_out_back_up_document_type
                                    ELSE ''::character varying
                                END AS tipo_docto_respaldo,  m.x_back_up_document_number AS nro_docto_respaldo,  upper(m.x_beneficiary::text) AS beneficiario, pm.name AS medio_pago,\
                                 he.x_income_document_number::text AS nro_comprobante_pago,  m.date AS fecha_pago, upper(ml.name::text) AS glosa,  CASE
                                    WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                    ELSE he.total_amount
                                END AS monto\
                                '''

            sqlWhere1 = ''' m.x_document_type = %s\
                        AND m.x_account_analytic_account_id = %s\
                        AND m.invoice_date BETWEEN %s AND %s AND\
                    '''
            sqlWhere2 = '''  m.x_document_type = %s\
                        AND m.x_account_analytic_account_id = %s\
                        AND m.date BETWEEN %s AND %s AND \
                    '''
            sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
            sql = sql + " ORDER BY account_id," + x_sort_by

            params = (x_document_type, x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                      x_document_type, x_account_analytic_account_id, where_params[2][1], where_params[2][0])

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

            sqlFiledBase = "cod_grupo as code, grupo as name, sum(monto) AS total"
            sqlFiled1 = '''ac.group_id AS cod_grupo, ag.name AS grupo, CASE
                                    WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                    ELSE ml.price_total
                                END AS monto
                             '''
            sqlFiled2 = '''ac.group_id AS cod_grupo, ag.name AS grupo, CASE
                                    WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                    ELSE he.total_amount
                                END AS monto
                             '''

            sqlWhere1 = ''' m.x_document_type = %s\
                    AND m.x_account_analytic_account_id = %s\
                    AND m.invoice_date BETWEEN %s AND %s AND \
                  '''
            sqlWhere2 = ''' m.x_document_type = %s\
                    AND m.x_account_analytic_account_id = %s\
                    AND m.date BETWEEN %s AND %s AND \
                  '''
            sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
            sql = sql + " GROUP BY cod_grupo, grupo"

            params = (x_document_type, x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                      x_document_type, x_account_analytic_account_id, where_params[2][1], where_params[2][0])

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

            sqlFiledBase = '''cod_grupo as code, nro_comprobante, tipo_docto_respaldo, nro_docto_respaldo, beneficiario,\
                                medio_pago, nro_comprobante_pago, fecha_pago, glosa, monto\
                               '''
            sqlFiled1 = '''ac.group_id AS cod_grupo,m.x_correlative AS nro_comprobante, CASE
                                    WHEN m.x_in_back_up_document_type IS NOT NULL THEN m.x_in_back_up_document_type
                                    WHEN m.x_out_back_up_document_type IS NOT NULL THEN m.x_out_back_up_document_type
                                    ELSE ''::character varying
                                END AS tipo_docto_respaldo, m.x_back_up_document_number AS nro_docto_respaldo,  CASE
                                    WHEN m.x_document_type::text = 'EGRESO'::character varying::text THEN upper(rp.name::text)
                                    ELSE upper(rp.name::text)
                                END AS beneficiario,  pm.name AS medio_pago, p.x_income_document_number::text AS nro_comprobante_pago, mlp.date AS fecha_pago, upper(p.x_name::text) AS glosa, CASE
                                    WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                    ELSE ml.price_total
                                END AS monto\
                               '''
            sqlFiled2 = '''ac.group_id AS cod_grupo,m.x_correlative AS nro_comprobante,CASE
                                    WHEN m.x_in_back_up_document_type IS NOT NULL THEN m.x_in_back_up_document_type
                                    WHEN m.x_out_back_up_document_type IS NOT NULL THEN m.x_out_back_up_document_type
                                    ELSE ''::character varying
                                END AS tipo_docto_respaldo, m.x_back_up_document_number AS nro_docto_respaldo,  upper(m.x_beneficiary::text) AS beneficiario, pm.name AS medio_pago,\
                                he.x_income_document_number::text AS nro_comprobante_pago,  m.date AS fecha_pago, upper(ml.name::text) AS glosa,  CASE
                                    WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                    ELSE he.total_amount
                                END AS monto\
                               '''
            sqlWhere1 = ''' m.x_document_type = %s\
                            AND m.x_account_analytic_account_id = %s\
                            AND m.invoice_date BETWEEN %s AND %s AND \
                          '''
            sqlWhere2 = ''' m.x_document_type = %s\
                            AND m.x_account_analytic_account_id = %s\
                            AND m.date BETWEEN %s AND %s AND \
                          '''

            sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
            sql = sql + " ORDER BY cod_grupo, " + x_sort_by

            params = (x_document_type, x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                      x_document_type, x_account_analytic_account_id, where_params[2][1], where_params[2][0])

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

    # bank ledger - Libro Banco
    def _get_bank_ledger_entries(self, accounts, x_account_analytic_account_id, x_sort_by, x_report_type,
                                 x_document_type):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        # Get initial balance
        sql = ('''SELECT amount_total\
                FROM account_move\
                WHERE x_account_analytic_account_id = %s\
                AND x_name = 'SALDO INICIAL'\
                ''')

        params = (x_account_analytic_account_id,)
        cr.execute(sql, params)

        initial_balance = 0
        for row in cr.dictfetchall():
            initial_balance = row['amount_total']

        sqlFiledBase = "tipo_documento, sum(monto) as saldo"
        sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''m.x_document_type AS tipo_documento,             
                            CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''

        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                        AND mlp.date < %s AND \
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.date <  %s  AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY tipo_documento"

        params = (x_account_analytic_account_id, where_params[2][1],
                  x_account_analytic_account_id, where_params[2][1])
        sql_param = {
            'x_account_analytic_account_id': x_account_analytic_account_id,
            'date_from': where_params[2][1],
            'date_close': '2023-06-30',
        }
        sqlNew = self.getSql(self.LIBRO_BANCO, 1, sql_param)
        cr.execute(sqlNew)
        # Banco SQL 1
        # cr.execute(sql, params)

        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['saldo']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['saldo']

        #     if total_income and total_expenses:
        initial_balance += total_income - total_expenses

        # Get ids movements of bank ledger
        sql = ('''SELECT row_number() OVER () as id\
                FROM account_report_back\
                WHERE x_account_analytic_account_id = %s\
                AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
                AND fecha_pago BETWEEN %s AND %s''')

        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0])

        # cr.execute(sql, params)

        # moves = []
        # for row in cr.dictfetchall():
        #    moves.append(row['id'])

        # if not moves:
        #    raise UserError(_("No existen datos para las fechas seleccionadas."))

        # move_lines = {x: [] for x in moves}
        move_lines = []

        if x_sort_by == 'fecha_ingreso':
            x_sort_by = 'fecha_pago'

        sqlFiledBase = '''row_number() OVER () as id, tipo_documento, fecha_ingreso, nro_comprobante, medio_pago, nro_comprobante_pago, fecha_pago, glosa, beneficiario,\
                        CASE tipo_documento WHEN 'INGRESO' THEN monto ELSE 0 END AS ingreso,\
                        CASE tipo_documento WHEN 'EGRESO' THEN monto ELSE 0 END AS egreso\
                        '''
        sqlFiled1 = '''row_number() OVER () as id, m.x_document_type AS tipo_documento, m.invoice_date AS fecha_ingreso,  m.x_correlative AS nro_comprobante,  pm.name AS medio_pago, p.x_income_document_number::text AS nro_comprobante_pago,  mlp.date AS fecha_pago, upper(p.x_name::text) AS glosa, CASE
                                WHEN m.x_document_type::text = 'EGRESO'::character varying::text THEN upper(rp.name::text)
                                ELSE ''::text
                            END AS beneficiario,\
                        CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''

        sqlFiled2 = '''row_number() OVER () as id, m.x_document_type as tipo_documento,m.invoice_date AS fecha_ingreso,  m.x_correlative AS nro_comprobante,  pm.name AS medio_pago, he.x_income_document_number::text AS nro_comprobante_pago, m.invoice_date AS fecha_pago,  upper(ml.name::text) AS glosa,  upper(m.x_beneficiary::text) AS beneficiario,\
                        CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''

        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                        AND mlp.date BETWEEN %s AND %s AND\
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.date BETWEEN %s AND %s AND\
                      '''

        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " ORDER BY " + x_sort_by + ", nro_comprobante "
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                  x_account_analytic_account_id, where_params[2][1], where_params[2][0])
        sql_param = {
            'x_account_analytic_account_id': x_account_analytic_account_id,
            'date_from': where_params[2][1],
            'date_to': where_params[2][0],
            'date_close': '2023-06-30',
            'x_sort_by': x_sort_by
        }
        sqlNew = self.getSql(self.LIBRO_BANCO, 2, sql_param)
        cr.execute(sqlNew)
        # cr.execute(sql, params)
        total_income = 0
        total_expenses = 0
        balance = initial_balance
        moves = cr.dictfetchall()
        if not moves:
            raise UserError(_("No existen datos para las fechas seleccionadas."))
        else:
            for row in moves:
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

    # bank reconciliation - Conciliación Bancaria
    def _get_bank_reconciliation_entries(self, accounts, x_account_analytic_account_id, x_sort_by,
                                         x_bank_final_balance):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        # Get initial balance
        sql = ('''SELECT amount_total\
                FROM account_move\
                WHERE x_account_analytic_account_id = %s\
                AND x_name = 'SALDO INICIAL'\
                ''')

        params = (x_account_analytic_account_id,)
        cr.execute(sql, params)

        initial_balance = 0
        for row in cr.dictfetchall():
            initial_balance = row['amount_total']

        sqlFiledBase = "tipo_documento, sum(monto) as total"
        sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''m.x_document_type AS tipo_documento, CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''
        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                        AND mlp.date < %s AND\
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.date < %s AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY tipo_documento"
        params = (x_account_analytic_account_id, where_params[2][1],
                  x_account_analytic_account_id, where_params[2][1])
        sql_param = {
            'x_account_analytic_account_id': x_account_analytic_account_id,
            'date_from': where_params[2][1],
            'date_close': '2023-06-30',
        }
        sqlNew = self.getSql(self.RECONCILIACION_BANCO, 1, sql_param)
        cr.execute(sqlNew)
        # cr.execute(sql, params)

        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['total']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['total']

        # if total_income and total_expenses:
        initial_balance += total_income - total_expenses

        # Get income and expenses from period

        sqlFiledBase = "tipo_documento, sum(monto) as total"
        sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''m.x_document_type AS tipo_documento, CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''
        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                        AND mlp.date BETWEEN %s AND %s AND\
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.date BETWEEN %s AND %s AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY tipo_documento"
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                  x_account_analytic_account_id, where_params[2][1], where_params[2][0])

        sql_param = {
            'x_account_analytic_account_id': x_account_analytic_account_id,
            'date_from': where_params[2][1],
            'date_to': where_params[2][0],
            'date_close': '2023-06-30'
        }
        sqlNew = self.getSql(self.RECONCILIACION_BANCO, 2, sql_param)
        cr.execute(sqlNew)
        # cr.execute(sql, params)

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
                AND m.date BETWEEN %s AND %s\
                ORDER BY ''' + x_sort_by)

        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0])

        sql_param = {
            'x_account_analytic_account_id': x_account_analytic_account_id,
            'date_from': where_params[2][1],
            'date_to': where_params[2][0],
            'date_close': '2023-06-30',
            'x_sort_by': x_sort_by
        }
        sqlNew = self.getSql(self.RECONCILIACION_BANCO, 3, sql_param)
        # cr.execute(sqlNew)

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

    # accountability - Rendición de Cuentas
    def _get_accountability_entries(self, accounts, x_account_analytic_account_id, x_sort_by, x_report_type,
                                    x_document_type):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        # Get initial balance
        sql = ('''SELECT amount_total\
                FROM account_move\
                WHERE x_account_analytic_account_id = %s\
                AND x_name = 'SALDO INICIAL'\
                ''')

        params = (x_account_analytic_account_id,)
        cr.execute(sql, params)

        initial_balance = 0
        for row in cr.dictfetchall():
            initial_balance = row['amount_total']

        # Get income and expenses

        sqlFiledBase = "tipo_documento, sum(monto) as total"
        sqlFiled1 = '''m.x_document_type AS tipo_documento,\
                        CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''m.x_document_type AS tipo_documento,\
                        CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''
        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                        AND mlp.date < %s AND\
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.date < %s AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY tipo_documento"
        params = (x_account_analytic_account_id, where_params[2][1],
                  x_account_analytic_account_id, where_params[2][1])
        sql_param = {
            'x_account_analytic_account_id': x_account_analytic_account_id,
            'date_from': where_params[2][1],
            'date_close': '2023-06-30',
        }
        sqlNew = self.getSql(self.RENDICION_CUENTAS, 1, sql_param)
        # SQL 1
        cr.execute(sqlNew)
        # cr.execute(sql, params)

        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['total']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['total']

        # if total_income and total_expenses:
        initial_balance += total_income - total_expenses

        # Get income from period group by SENAINFO accounts

        sqlFiledBase = "row_number() OVER () as id, grupo as cuenta_senainfo, sum(monto) as total"
        sqlFiled1 = '''ac.x_senainfo_group_name AS grupo, CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''ac.x_senainfo_group_name AS grupo, CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''
        sqlWhere1 = ''' m.x_account_analytic_account_id   = %s\
                        AND m.x_document_type = 'INGRESO'\
                        AND mlp.date BETWEEN %s AND %s AND \
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.x_document_type = 'INGRESO'\
                        AND m.date BETWEEN %s AND %s AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY grupo"
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                  x_account_analytic_account_id, where_params[2][1], where_params[2][0])
        sql_param = {
            'x_account_analytic_account_id': x_account_analytic_account_id,
            'date_from': where_params[2][1],
            'date_to': where_params[2][0],
            'date_close': '2023-06-30',
        }
        sqlNew = self.getSql(self.RENDICION_CUENTAS, 2, sql_param)
        cr.execute(sqlNew)
        # SQL 2
        # cr.execute(sqlNew)

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
        sqlFiledBase = "row_number() OVER () as id,grupo as cuenta_senainfo, sum(monto) as total"
        sqlFiled1 = '''ac.x_senainfo_group_name AS grupo, CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''ac.x_senainfo_group_name AS grupo, CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''
        sqlWhere1 = ''' m.x_account_analytic_account_id   = %s\
                        AND m.x_document_type = 'EGRESO'\
                        AND mlp.date BETWEEN %s AND %s AND \
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.x_document_type = 'EGRESO'\
                        AND m.date BETWEEN %s AND %s AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY grupo"

        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                  x_account_analytic_account_id, where_params[2][1], where_params[2][0])
        sql_param = {
            'x_account_analytic_account_id': x_account_analytic_account_id,
            'date_from': where_params[2][1],
            'date_to': where_params[2][0],
            'date_close': '2023-06-30',
        }
        sqlNew = self.getSql(self.RENDICION_CUENTAS, 3, sql_param)
        cr.execute(sqlNew)
        # SQL 2
        # cr.execute(sql, params)

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



    # Anterior
    # bank ledger - Libro Banco Old
    def _get_bank_ledger_entries_old(self, accounts, x_account_analytic_account_id, x_sort_by, x_report_type,
                                     x_document_type):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        # Get initial balance
        sql = ('''SELECT amount_total\
                FROM account_move\
                WHERE x_account_analytic_account_id = %s\
                AND x_name = 'SALDO INICIAL'\
                ''')

        params = (x_account_analytic_account_id,)
        cr.execute(sql, params)

        initial_balance = 0
        for row in cr.dictfetchall():
            initial_balance = row['amount_total']

        sqlFiledBase = "tipo_documento, sum(monto) as saldo"
        sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''m.x_document_type AS tipo_documento,             
                            CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''

        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                        AND mlp.date < %s AND \
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.date <  %s  AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY tipo_documento"

        params = (x_account_analytic_account_id, where_params[2][1],
                  x_account_analytic_account_id, where_params[2][1])
        cr.execute(sql, params)

        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['saldo']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['saldo']

        #     if total_income and total_expenses:
        initial_balance += total_income - total_expenses

        # Get ids movements of bank ledger
        sql = ('''SELECT row_number() OVER () as id\
                FROM account_report_back\
                WHERE x_account_analytic_account_id = %s\
                AND EXTRACT(YEAR FROM fecha_pago) = ''' + where_params[2][1][0:4] + ''' \
                AND fecha_pago BETWEEN %s AND %s''')

        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0])

        # cr.execute(sql, params)

        # moves = []
        # for row in cr.dictfetchall():
        #    moves.append(row['id'])

        # if not moves:
        #    raise UserError(_("No existen datos para las fechas seleccionadas."))

        # move_lines = {x: [] for x in moves}
        move_lines = []

        if x_sort_by == 'fecha_ingreso':
            x_sort_by = 'fecha_pago'

        sqlFiledBase = '''row_number() OVER () as id, tipo_documento, fecha_ingreso, nro_comprobante, medio_pago, nro_comprobante_pago, fecha_pago, glosa, beneficiario,\
                        CASE tipo_documento WHEN 'INGRESO' THEN monto ELSE 0 END AS ingreso,\
                        CASE tipo_documento WHEN 'EGRESO' THEN monto ELSE 0 END AS egreso\
                        '''
        sqlFiled1 = '''row_number() OVER () as id, m.x_document_type AS tipo_documento, m.invoice_date AS fecha_ingreso,  m.x_correlative AS nro_comprobante,  pm.name AS medio_pago, p.x_income_document_number::text AS nro_comprobante_pago,  mlp.date AS fecha_pago, upper(p.x_name::text) AS glosa, CASE
                                WHEN m.x_document_type::text = 'EGRESO'::character varying::text THEN upper(rp.name::text)
                                ELSE ''::text
                            END AS beneficiario,\
                        CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''

        sqlFiled2 = '''row_number() OVER () as id, m.x_document_type as tipo_documento,m.invoice_date AS fecha_ingreso,  m.x_correlative AS nro_comprobante,  pm.name AS medio_pago, he.x_income_document_number::text AS nro_comprobante_pago, m.invoice_date AS fecha_pago,  upper(ml.name::text) AS glosa,  upper(m.x_beneficiary::text) AS beneficiario,\
                        CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''

        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                        AND mlp.date BETWEEN %s AND %s AND\
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.date BETWEEN %s AND %s AND\
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " ORDER BY " + x_sort_by + ", nro_comprobante "
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                  x_account_analytic_account_id, where_params[2][1], where_params[2][0])

        cr.execute(sql, params)

        total_income = 0
        total_expenses = 0
        balance = initial_balance
        moves = cr.dictfetchall()
        if not moves:
            raise UserError(_("No existen datos para las fechas seleccionadas."))
        else:
            for row in moves:
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

    # bank reconciliation - Conciliación Bancaria Old
    def _get_bank_reconciliation_entries_old(self, accounts, x_account_analytic_account_id, x_sort_by,
                                             x_bank_final_balance):
        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        # Get initial balance
        sql = ('''SELECT amount_total\
                    FROM account_move\
                    WHERE x_account_analytic_account_id = %s\
                    AND x_name = 'SALDO INICIAL'\
                    ''')

        params = (x_account_analytic_account_id,)
        cr.execute(sql, params)

        initial_balance = 0
        for row in cr.dictfetchall():
            initial_balance = row['amount_total']

        sqlFiledBase = "tipo_documento, sum(monto) as total"
        sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                    WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                    ELSE ml.price_total
                                END AS monto
                            '''
        sqlFiled2 = '''m.x_document_type AS tipo_documento, CASE
                                    WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                    ELSE he.total_amount
                                END AS monto
                            '''
        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                            AND mlp.date < %s AND\
                          '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                            AND m.date < %s AND \
                          '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY tipo_documento"
        params = (x_account_analytic_account_id, where_params[2][1],
                  x_account_analytic_account_id, where_params[2][1])
        cr.execute(sql, params)

        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['total']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['total']

        # if total_income and total_expenses:
        initial_balance += total_income - total_expenses

        # Get income and expenses from period

        sqlFiledBase = "tipo_documento, sum(monto) as total"
        sqlFiled1 = '''m.x_document_type AS tipo_documento, CASE
                                    WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                    ELSE ml.price_total
                                END AS monto
                            '''
        sqlFiled2 = '''m.x_document_type AS tipo_documento, CASE
                                    WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                    ELSE he.total_amount
                                END AS monto
                            '''
        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                            AND mlp.date BETWEEN %s AND %s AND\
                          '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                            AND m.date BETWEEN %s AND %s AND \
                          '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY tipo_documento"
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                  x_account_analytic_account_id, where_params[2][1], where_params[2][0])
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

    # accountability - Rendición de Cuentas Old
    def _get_accountability_entries_old(self, accounts, x_account_analytic_account_id, x_sort_by, x_report_type,
                                        x_document_type):

        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = {x: [] for x in accounts.ids}

        # Prepare sql query base on selected parameters from wizard
        where_params = MoveLine._query_get()

        # Get initial balance
        sql = ('''SELECT amount_total\
                FROM account_move\
                WHERE x_account_analytic_account_id = %s\
                AND x_name = 'SALDO INICIAL'\
                ''')

        params = (x_account_analytic_account_id,)
        cr.execute(sql, params)

        initial_balance = 0
        for row in cr.dictfetchall():
            initial_balance = row['amount_total']

        # Get income and expenses

        sqlFiledBase = "tipo_documento, sum(monto) as total"
        sqlFiled1 = '''m.x_document_type AS tipo_documento,\
                        CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''m.x_document_type AS tipo_documento,\
                        CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''
        sqlWhere1 = ''' m.x_account_analytic_account_id = %s\
                        AND mlp.date < %s AND\
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.date < %s AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY tipo_documento"
        params = (x_account_analytic_account_id, where_params[2][1],
                  x_account_analytic_account_id, where_params[2][1])
        cr.execute(sql, params)

        total_income = 0
        total_expenses = 0
        for row in cr.dictfetchall():
            if row['tipo_documento'] == 'INGRESO':
                total_income = row['total']
            elif row['tipo_documento'] == 'EGRESO':
                total_expenses = row['total']

        # if total_income and total_expenses:
        initial_balance += total_income - total_expenses

        # Get income from period group by SENAINFO accounts

        sqlFiledBase = "row_number() OVER () as id, grupo as cuenta_senainfo, sum(monto) as total"
        sqlFiled1 = '''ac.x_senainfo_group_name AS grupo, CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''ac.x_senainfo_group_name AS grupo, CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''
        sqlWhere1 = ''' m.x_account_analytic_account_id   = %s\
                        AND m.x_document_type = 'INGRESO'\
                        AND mlp.date BETWEEN %s AND %s AND \
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.x_document_type = 'INGRESO'\
                        AND m.date BETWEEN %s AND %s AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY grupo"
        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                  x_account_analytic_account_id, where_params[2][1], where_params[2][0])
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
        sqlFiledBase = "row_number() OVER () as id,grupo as cuenta_senainfo, sum(monto) as total"
        sqlFiled1 = '''ac.x_senainfo_group_name AS grupo, CASE
                                WHEN ac.group_id = 17 THEN ml.price_total * '-1'::integer::numeric
                                ELSE ml.price_total
                            END AS monto
                        '''
        sqlFiled2 = '''ac.x_senainfo_group_name AS grupo, CASE
                                WHEN ac.group_id = 17 THEN he.total_amount * '-1'::integer::numeric
                                ELSE he.total_amount
                            END AS monto
                        '''
        sqlWhere1 = ''' m.x_account_analytic_account_id   = %s\
                        AND m.x_document_type = 'EGRESO'\
                        AND mlp.date BETWEEN %s AND %s AND \
                      '''
        sqlWhere2 = ''' m.x_account_analytic_account_id = %s\
                        AND m.x_document_type = 'EGRESO'\
                        AND m.date BETWEEN %s AND %s AND \
                      '''
        sql = self.getSqlBase() % (sqlFiledBase, sqlFiled1, sqlWhere1, sqlFiled2, sqlWhere2)
        sql = sql + " GROUP BY grupo"

        params = (x_account_analytic_account_id, where_params[2][1], where_params[2][0],
                  x_account_analytic_account_id, where_params[2][1], where_params[2][0])
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
