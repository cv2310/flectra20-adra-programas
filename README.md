# README #

## Problema con archivo
El archivo `account_report_back_view.xml` actualmente posee un error debido a que falta un argumento. Aunque este argumento no es necesario, este error puede prevenir la actualización del módulo de manera correcta en ciertos casos particulares. Para prevenir posibles errores, la línea 43 en el archivo `__manifest__.py` del proyecto está comentada, ya que contiene la ruta a la vista en cuestión. En caso de necesitar modificar la vista, se debe descomentar esta línea en el archivo `__manifest__.py` para permitir su actualización. Se recomienda mantener la línea comentada luego de realizar cambios.

## Cambios Directos en Vistas
En algunos casos, se realizaron cambios directamente sobre el ERP en ciertas vistas debido a problemas técnicos. Esto significa que estas vistas no se encuentran disponibles dentro del proyecto y deben ser manejadas directamente a través del editor de vistas de Flectra con el modo desarrollador.

#### A continuación se listan las vistas involucradas y su respectivo contenido:

1. ### `report_general_ledger`
```html
<?xml version="1.0"?>
<t t-name="accounting_pdf_reports.report_general_ledger">
        <t t-call="web.html_container">
            <t t-set="data_report_margin_top" t-value="12"/>
            <t t-set="data_report_header_spacing" t-value="9"/>
            <t t-set="data_report_dpi" t-value="110"/>
            <t t-call="web.internal_layout">
                <div class="page">
                    <div class="row">
                        <div class="col-2 mb4">
                            <img t-if="res_company.logo" t-att-src="image_data_uri(res_company.logo)" style="max-height: 90px;" alt="Logo"/>
                        </div>
                        <div style="font-size:11px" class="col-10">
                            <span>Agencia Adventista de Desarrollo y Recursos Asistenciales</span><br/>
                            <span>RUT: </span><span t-if="res_company.vat" t-field="res_company.vat"></span>
                        </div>
                    </div>
                    <br/>
                    <div class="row">
                      <div class="col-6">
                        <h2 style="font-size:18px">
                          <span t-if="data['x_document_type'] == 'INGRESO'">LIBRO INGRESOS</span>
                          <span t-if="data['x_document_type'] == 'EGRESO'">LIBRO EGRESOS</span>
                          <span t-if="data['x_document_type'] == 'BANCO'">LIBRO BANCO</span>
                          <span t-if="data['x_document_type'] == 'CONCILIACION'">CONCILIACIÓN BANCARIA</span>
                          <span t-if="data['x_document_type'] == 'RENDICION'">RENDICIÓN DE CUENTAS</span>
                        </h2>
                      </div>
                      <div class="col-6 text-right">
                        <h4 style="font-size:16px">
                          <span t-esc="context_timestamp(datetime.datetime.now()).strftime('%d-%m-%Y')"/>
                        </h4>
                      </div>
                    </div>
                    <br/>
                    <div style="font-size:11px" class="row mb32">
                        <div class="col-3">
                            <strong>Programa:</strong><br/>
                            <t t-if="data['x_program_name']"><span t-esc="data['x_program_name']"/></t>
                        </div>
                        <div class="col-3">
                            <strong>Ordenado por:</strong>
                            <p t-if="data['x_sort_by'] == 'fecha_ingreso'">Fecha</p>
                            <p t-if="data['x_sort_by'] == 'nro_comprobante'">Nº Comprobante</p>
                        </div>
                        <div class="col-3">
                            <t t-if="data['date_from']"><strong>Fecha desde :</strong> <span t-esc="data['date_from']" t-options='{"widget": "date"}'/><br/></t>
                            <t t-if="data['date_to']"><strong>Fecha hasta :</strong> <span t-esc="data['date_to']" t-options='{"widget": "date"}'/></t>
                        </div>
                        <div class="col-3">
                            <strong>Tipo de Reporte:</strong>
                            <p t-if="data['x_report_type'] == 'cuenta'">ADRA</p>
                            <p t-if="data['x_report_type'] == 'cuenta_senainfo'">SENAINFO</p>
                        </div>
                    </div>
                    <br/>
                    <t t-if="data['x_document_type'] == 'INGRESO' or data['x_document_type'] == 'EGRESO'">
                        <t t-foreach="Accounts" t-as="account">
                            <table class="table table-sm table-reports">
                                <thead>
                                    <tr>
                                        <td colspan="12">
                                        <h5>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span t-esc="account['code']"/>
                                            <span t-esc="account['name']"/>
                                        </h5>
                                        </td>
                                    </tr>
                                    <tr class="text-center">
                                        <th class="text-center">Nº COMP.</th>
                                        <th class="text-center">DOCTO. RESPALDO</th>
                                        <th class="text-center">Nº DOCTO. RESP.</th>
                                        <th class="text-center">PROVEEDOR</th>
                                        <th class="text-center">FORMA DE PAGO</th>
                                        <th class="text-center">Nº COMP. PAGO</th>
                                        <th class="text-center">FECHA DE PAGO</th>
                                        <th class="text-center">GLOSA</th>
                                        <th class="text-center">MONTO</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr t-foreach="account['move_lines']" t-as="line">
                                        <td class="text-center"><span t-esc="line['nro_comprobante']"/></td>
                                        <td class="text-center"><span t-esc="line['tipo_docto_respaldo']"/></td>
                                        <td class="text-center"><span t-esc="line['nro_docto_respaldo']"/></td>
                                        <td class="text-center"><span t-esc="line['beneficiario']"/></td>
                                        <td class="text-center"><span t-esc="line['medio_pago']"/></td>
                                        <td class="text-center"><span t-esc="line['nro_comprobante_pago']"/></td>
                                        <td class="text-center"><span t-esc="line['fecha_pago']" t-options='{"widget": "date"}'/></td>
                                        <td class="text-center"><span t-esc="line['glosa']"/></td>
                                        <td class="text-right">
                                            <span t-esc="line['monto']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </td>
                                    </tr>
                                    <tr style="font-weight: bold;">
                                        <td class="text-right" colspan="12">
                                        <br/>
                                        <h5>
                                            <span>Total: </span>
                                            <span t-esc="account['total']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h5>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <br/>
                        </t>
                    </t>
                    <t t-if="data['x_document_type'] == 'BANCO'">
                        <t t-if="data['x_report_type'] == 'cuenta'">
                            <t t-foreach="Accounts" t-as="account">
                                <table class="table table-sm table-reports">
                                    <tr>
                                        <td colspan="12" class="text-right">
                                        <h3 style="font-size:14px">
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>Saldo Inicial: </span>
                                            <span t-esc="account['initial_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h3>
                                        </td>
                                    </tr>
                                    <table class="table table-sm table-reports">
                                    <thead>
                                    <tr>
                                        <td colspan="12" class="text-left">
                                        <h3 style="font-size:16px">
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>INGRESOS: </span>
                                        </h3>
                                        </td>
                                    </tr>
                                    <tr style="font-size:15px;font-weight:bold" class="text-center">
                                        <th class="text-center">FECHA</th>
                                        <th class="text-center">Nº COMP.</th>
                                        <th class="text-center">FORMA DE PAGO</th>
                                        <th class="text-center">Nº COMP. PAGO</th>
                                        <th class="text-center">FECHA DE PAGO</th>
                                        <th class="text-center">GLOSA</th>
                                        <th class="text-center">BENEFICIARIO</th>
                                        <th class="text-center">MONTO</th>
                                        <th class="text-center">SALDO</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                        <tr style="font-size:14px" t-foreach="account['move_lines']" t-as="line">
                                            <t t-if="line['tipo_documento'] == 'INGRESO'">
                                                <td class="text-center"><span t-esc="line['fecha_ingreso']" t-options='{"widget": "date"}'/></td>
                                                <td class="text-center"><span t-esc="line['nro_comprobante']"/></td>
                                                <td class="text-center"><span t-esc="line['medio_pago']"/></td>
                                                <td class="text-center"><span t-esc="line['nro_comprobante_pago']"/></td>
                                                <td class="text-center"><span t-esc="line['fecha_pago']" t-options='{"widget": "date"}'/></td>
                                                <td class="text-center"><span t-esc="line['glosa']"/></td>
                                                <td class="text-center"><span t-esc="line['beneficiario']"/></td>
                                                <td class="text-right">
                                                    <span t-esc="line['ingreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                                </td>
                                                <td class="text-right">
                                                    <span t-esc="line['saldo']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                                </td>
                                            </t>
                                        </tr>
                                    </tbody>
                                    </table>
                                    <table class="table table-sm table-reports">
                                    <thead>
                                        <tr>
                                            <td colspan="12" class="text-left">
                                            <br/><br/>
                                            <h3 style="font-size:16px">
                                                <span style="color: white;" t-esc="'..'"/>
                                                <span>EGRESOS: </span>
                                            </h3>
                                            </td>
                                        </tr>
                                        <tr style="font-size:15px;font-weight:bold" class="text-center">
                                            <th class="text-center">FECHA</th>
                                            <th class="text-center">Nº COMP.</th>
                                            <th class="text-center">FORMA DE PAGO</th>
                                            <th class="text-center">Nº COMP. PAGO</th>
                                            <th class="text-center">FECHA DE PAGO</th>
                                            <th class="text-center">GLOSA</th>
                                            <th class="text-center">BENEFICIARIO</th>
                                            <th class="text-center">MONTO</th>
                                            <th class="text-center">SALDO</th>
                                        </tr>
                                    </thead>
                                    <tbody style="font-size:14px">
                                        <t t-set="total_sum" t-value="0"/>
    <t t-set="nro_doc" t-value="-1"/>
    <tr t-foreach="account['move_lines']" t-as="line">
        <t t-if="line['tipo_documento'] == 'EGRESO'">
            <t t-if="line_first">
                <td class="text-center"><span t-esc="line['fecha_ingreso']" t-options='{"widget": "date"}'/></td>
                <td class="text-center"><span t-esc="line['nro_comprobante']"/></td>
                <td class="text-center"><span t-esc="line['medio_pago']"/></td>
                <td class="text-center"><span t-esc="line['nro_comprobante_pago']"/></td>
                <td class="text-center"><span t-esc="line['fecha_pago']" t-options='{"widget": "date"}'/></td>
                <td class="text-center"><span t-esc="line['glosa']"/></td>
                <td class="text-center"><span t-esc="line['beneficiario']"/></td>
                <td class="text-right">
                    <span t-esc="line['egreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                </td>
                <td class="text-right">
                    <span t-esc="line['saldo']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                </td>
                <t t-set="total_sum" t-value="total_sum + line['egreso']"/>
                <t t-set="nro_doc" t-value="line['nro_comprobante']"/>
            </t>
            <t t-if="not line_first and not line_last">
                <t t-if="nro_doc == line['nro_comprobante']">
                    <t t-set="total_sum" t-value="total_sum + line['egreso']"/>
                </t>
                <t t-else="">
                    <tr>
                        <t t-if="nro_doc != -1">
                          <td colspan="4"></td>
                          <td class="text-right" colspan="5" style="font-weight:bold">
                              <span>Total comprobante Nro <t t-esc="nro_doc"/>:</span>
                              <span t-esc="total_sum" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                          </td>
                        </t>
                    </tr>
                    <t t-set="total_sum" t-value="line['egreso']"/>
                    <t t-set="nro_doc" t-value="line['nro_comprobante']"/>
                </t>
                <td class="text-center"><span t-esc="line['fecha_ingreso']" t-options='{"widget": "date"}'/></td>
                <td class="text-center"><span t-esc="line['nro_comprobante']"/></td>
                <td class="text-center"><span t-esc="line['medio_pago']"/></td>
                <td class="text-center"><span t-esc="line['nro_comprobante_pago']"/></td>
                <td class="text-center"><span t-esc="line['fecha_pago']" t-options='{"widget": "date"}'/></td>
                <td class="text-center"><span t-esc="line['glosa']"/></td>
                <td class="text-center"><span t-esc="line['beneficiario']"/></td>
                <td class="text-right">
                    <span t-esc="line['egreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                </td>
                <td class="text-right">
                    <span t-esc="line['saldo']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                </td>
            </t>
            <t t-if="line_last">
                 <t t-if="not line_first">
                    <t t-if="nro_doc == line['nro_comprobante']">
                        <t t-set="total_sum" t-value="total_sum + line['egreso']"/>
                    </t>
                    <t t-else="">
                        <tr>
                            <t t-if="nro_doc != -1">
                              <td colspan="4"></td>
                              <td class="text-right" colspan="5" style="font-weight:bold">
                                  <span>Total comprobante Nro <t t-esc="nro_doc"/>:</span>
                                  <span t-esc="total_sum" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                              </td>
                            </t>
                        </tr>
                        <t t-set="total_sum" t-value="line['egreso']"/>
                        <t t-set="nro_doc" t-value="line['nro_comprobante']"/>
                    </t>
                    <td class="text-center"><span t-esc="line['fecha_ingreso']" t-options='{"widget": "date"}'/></td>
                    <td class="text-center"><span t-esc="line['nro_comprobante']"/></td>
                    <td class="text-center"><span t-esc="line['medio_pago']"/></td>
                    <td class="text-center"><span t-esc="line['nro_comprobante_pago']"/></td>
                    <td class="text-center"><span t-esc="line['fecha_pago']" t-options='{"widget": "date"}'/></td>
                    <td class="text-center"><span t-esc="line['glosa']"/></td>
                    <td class="text-center"><span t-esc="line['beneficiario']"/></td>
                    <td class="text-right">
                        <span t-esc="line['egreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                    </td>
                                    <td class="text-right">
                        <span t-esc="line['saldo']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                    </td>
                </t>
                <tr>
                    <t t-if="nro_doc != -1">
                      <td colspan="4"></td>
                      <td class="text-right" colspan="5" style="font-weight:bold">
                          <span>Total comprobante Nro <t t-esc="nro_doc"/>:</span>
                          <span t-esc="total_sum" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                      </td>
                    </t>
                </tr>
            </t>
        </t>
    </tr>
                                    </tbody>
                                    </table>
                                    <table class="table table-sm table-reports">
                                    <tr style="font-weight: bold;">
                                        <td class="text-right" colspan="6">
                                        <br/>
                                        <h5 style="font-size:14px">
                                            <span>Total Ingresos: </span>
                                            <span t-esc="account['total_income']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h5>
                                        </td>
                                        <td class="text-right" colspan="6">
                                        <br/>
                                        <h5 style="font-size:14px">
                                            <span>Total Egresos: </span>
                                            <span t-esc="account['total_expenses']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h5>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="12" class="text-right">
                                        <br/>
                                        <h3 style="font-size:16px">
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>Saldo Final: </span>
                                            <span t-esc="account['final_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h3>
                                        </td>
                                    </tr>
                                    </table>
                                </table>
                                <br/>
                            </t>
                        </t>
                        <t t-if="data['x_report_type'] == 'cuenta_senainfo'">
                            <t t-foreach="Accounts" t-as="account">
                                <table class="table table-sm table-reports">
                                    <thead>
                                        <tr>
                                            <td colspan="12" class="text-right">
                                            <h3>
                                                <span style="color: white;" t-esc="'..'"/>
                                                <span>Saldo Inicial: </span>
                                                <span t-esc="account['initial_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                            </h3>
                                            </td>
                                        </tr>
                                        <tr class="text-center">
                                            <th class="text-center">FECHA</th>
                                            <th class="text-center">Nº COMP.</th>
                                            <th class="text-center">FORMA DE PAGO</th>
                                            <th class="text-center">Nº COMP. PAGO</th>
                                            <th class="text-center">FECHA DE PAGO</th>
                                            <th class="text-center">GLOSA</th>
                                            <th class="text-center">BENEFICIARIO</th>
                                            <th class="text-center">INGRESO</th>
                                            <th class="text-center">EGRESO</th>
                                            <th class="text-center">SALDO</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <t t-set="total_sum_egreso" t-value="0"/>
    <t t-set="total_sum_ingreso" t-value="0"/>
    <t t-set="nro_doc" t-value="-1"/>
    <tr t-foreach="account['move_lines']" t-as="line">
        <t t-if="line_first">
            <td class="text-center"><span t-esc="line['fecha_ingreso']" t-options='{"widget": "date"}'/></td>
            <td class="text-center"><span t-esc="line['nro_comprobante']"/></td>
            <td class="text-center"><span t-esc="line['medio_pago']"/></td>
            <td class="text-center"><span t-esc="line['nro_comprobante_pago']"/></td>
            <td class="text-center"><span t-esc="line['fecha_pago']" t-options='{"widget": "date"}'/></td>
            <td class="text-center"><span t-esc="line['glosa']"/></td>
            <td class="text-center"><span t-esc="line['beneficiario']"/></td>
            <td class="text-right">
                <span t-esc="line['ingreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
            </td>
            <td class="text-right">
                <span t-esc="line['egreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
            </td>
            <td class="text-right">
                <span t-esc="line['saldo']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
            </td>
            <t t-set="total_sum_egreso" t-value="total_sum_egreso + line['egreso']"/>
            <t t-set="total_sum_ingreso" t-value="total_sum_ingreso + line['ingreso']"/>
            <t t-set="nro_doc" t-value="line['nro_comprobante']"/>
        </t>
        <t t-if="not line_first and not line_last">
            <t t-if="nro_doc == line['nro_comprobante']">
                <t t-set="total_sum_egreso" t-value="total_sum_egreso + line['egreso']"/>
                <t t-set="total_sum_ingreso" t-value="total_sum_ingreso + line['ingreso']"/>
            </t>
            <t t-else="">
                <tr>
                    <t t-if="nro_doc != -1">
                      <td colspan="5"></td>
                      <td class="text-right" colspan="5" style="font-weight:bold">
                          <span>Total comprobante Nro <t t-esc="nro_doc"/>:</span>
                          <t t-if="total_sum_egreso > 0">
                              <span t-esc="total_sum_egreso" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                          </t>
                          <t t-if="total_sum_ingreso > 0">
                              <span t-esc="total_sum_ingreso" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                          </t>
                      </td>
                    </t>
                </tr>
                <t t-set="total_sum_egreso" t-value="line['egreso']"/>
                <t t-set="total_sum_ingreso" t-value="line['ingreso']"/>
                <t t-set="nro_doc" t-value="line['nro_comprobante']"/>
            </t>
            <td class="text-center"><span t-esc="line['fecha_ingreso']" t-options='{"widget": "date"}'/></td>
            <td class="text-center"><span t-esc="line['nro_comprobante']"/></td>
            <td class="text-center"><span t-esc="line['medio_pago']"/></td>
            <td class="text-center"><span t-esc="line['nro_comprobante_pago']"/></td>
            <td class="text-center"><span t-esc="line['fecha_pago']" t-options='{"widget": "date"}'/></td>
            <td class="text-center"><span t-esc="line['glosa']"/></td>
            <td class="text-center"><span t-esc="line['beneficiario']"/></td>
            <td class="text-right">
                <span t-esc="line['ingreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
            </td>
            <td class="text-right">
                <span t-esc="line['egreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
            </td>
            <td class="text-right">
                <span t-esc="line['saldo']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
            </td>
        </t>
        <t t-if="line_last">
                <t t-if="not line_first">
                <t t-if="nro_doc == line['nro_comprobante']">
                    <t t-set="total_sum_egreso" t-value="total_sum_egreso + line['egreso']"/>
                    <t t-set="total_sum_ingreso" t-value="total_sum_ingreso + line['ingreso']"/>
                </t>
                <t t-else="">
                    <tr>
                        <t t-if="nro_doc != -1">
                          <td colspan="5"></td>
                          <td class="text-right" colspan="5" style="font-weight:bold">
                              <span>Total comprobante Nro <t t-esc="nro_doc"/>:</span>
                              <t t-if="total_sum_egreso > 0">
                                  <span t-esc="total_sum_egreso" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                              </t>
                              <t t-if="total_sum_ingreso > 0">
                                  <span t-esc="total_sum_ingreso" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                              </t>
                          </td>
                        </t>
                    </tr>
                    <t t-set="total_sum_egreso" t-value="line['egreso']"/>
                    <t t-set="total_sum_ingreso" t-value="line['ingreso']"/>
                    <t t-set="nro_doc" t-value="line['nro_comprobante']"/>
                </t>
                <td class="text-center"><span t-esc="line['fecha_ingreso']" t-options='{"widget": "date"}'/></td>
                <td class="text-center"><span t-esc="line['nro_comprobante']"/></td>
                <td class="text-center"><span t-esc="line['medio_pago']"/></td>
                <td class="text-center"><span t-esc="line['nro_comprobante_pago']"/></td>
                <td class="text-center"><span t-esc="line['fecha_pago']" t-options='{"widget": "date"}'/></td>
                <td class="text-center"><span t-esc="line['glosa']"/></td>
                <td class="text-center"><span t-esc="line['beneficiario']"/></td>
                <td class="text-right">
                    <span t-esc="line['ingreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                </td>
                <td class="text-right">
                    <span t-esc="line['egreso']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                </td>
                <td class="text-right">
                    <span t-esc="line['saldo']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                </td>
            </t>
            <tr>
                <t t-if="nro_doc != -1">
                  <td colspan="5"></td>
                  <td class="text-right" colspan="5" style="font-weight:bold">
                      <span>Total comprobante Nro <t t-esc="nro_doc"/>:</span>
                      <t t-if="total_sum_egreso > 0">
                          <span t-esc="total_sum_egreso" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                      </t>
                      <t t-if="total_sum_ingreso > 0">
                          <span t-esc="total_sum_ingreso" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                      </t>
                  </td>
                </t>
            </tr>
            <table class="table table-sm table-reports">
                <tr>
                  <td colspan="12" class="text-right">
                    <br/>
                    <h3>
                      <span style="color: white;" t-esc="'..'"/>
                      <span>Saldo Final: </span>
                      <span t-esc="account['final_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                    </h3>
                  </td>
                </tr>
            </table>
        </t>
    </tr>
                                    </tbody>
                                </table>
                                <br/>
                            </t>
                        </t>
                    </t>
                    <t t-if="data['x_document_type'] == 'CONCILIACION'">
                        <t t-foreach="Accounts" t-as="account">
                            <table class="table table-sm table-reports">
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>SALDO INICIAL: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['initial_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>TOTAL INGRESOS: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['total_income']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>TOTAL EGRESOS: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['total_expenses']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>CHEQUES GIRADOS NO PAGADOS: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['total_checks_drawn_uncharged']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>TOTAL CONCILIADO: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['reconciled_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>SALDO FINAL: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['final_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>SALDO FINAL CARTOLA BANCO: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['bank_final_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>DIFERENCIA: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['difference']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr><td colspan="12"></td></tr>
                            </table>
                            <table class="table table-reports">
                                <thead>
                                    <div>
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>Detalle de Cheques Girados No Pagados: </span>
                                        </h4>
                                    </div>
                                    <tr class="text-center">
                                        <th class="text-center">DOCUMENTO</th>
                                        <th class="text-center">Nº CHEQUE</th>
                                        <th class="text-center">FECHA DE PAGO</th>
                                        <th class="text-center">BENEFICIARIO</th>
                                        <th class="text-center">REFERENCIA</th>
                                        <th class="text-center">MONTO</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr t-foreach="account['move_lines']" t-as="line">
                                        <td class="text-center"><span t-esc="line['documento']"/></td>
                                        <td class="text-center"><span t-esc="line['nro_cheque']"/></td>
                                        <td class="text-center"><span t-esc="line['fecha_pago']" t-options='{"widget": "date"}'/></td>
                                        <td class="text-center"><span t-esc="line['beneficiario']"/></td>
                                        <td class="text-center"><span t-esc="line['referencia']"/></td>
                                        <td class="text-right">
                                            <span t-esc="line['monto']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="10" class="text-right">
                                            <h5>
                                                <span>Total: </span>
                                                <span t-esc="account['total_checks_drawn_uncharged']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                            </h5>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <br/><br/>
                            <table>
                                <tr>
                                    <td colspan="12" class="text-center">
                                    <h5>
                                        <span>Firma Responsable Conciliación</span>
                                    </h5>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="3" class="text-center">
                                    <br/>
                                    <h6>
                                        <span style="color: white;" t-esc="'..'"/>
                                        <span>NOTA:</span>
                                        <span style="color: white;" t-esc="'..'"/>
                                    </h6>
                                    </td>
                                    <td colspan="9" class="text-left">
                                    <br/>
                                    <h6>
                                        <span>El saldo de la conciliación debe coincidir con los saldos del libro banco y rendición de cuentas. En el evento de detectar alguna diferencia, deberá ser regularizada en dicha Conciliación.</span>
                                    </h6>
                                    </td>
                                </tr>
                            </table>
                        </t>
                    </t>
                    <t t-if="data['x_document_type'] == 'RENDICION'">
                        <t t-foreach="Accounts" t-as="account">
                            <table class="table table-sm table-reports">
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>SALDO INICIAL: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['initial_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>INGRESOS DEL PERIODO: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['total_income_from_period']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr t-foreach="account['move_lines_income']" t-as="line">
                                    <td colspan="6" class="text-left">
                                        <h5>
                                            <span style="color: white;" t-esc="'......'"/>
                                            <span t-esc="line['cuenta_senainfo']"/>
                                        </h5>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h5>
                                            <span t-esc="line['total']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h5>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>TOTAL INGRESOS (Saldo Inicial + Ingresos del Periodo): </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['total_income']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>EGRESOS DEL PERIODO: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['total_expenses_from_period']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr t-foreach="account['move_lines_expenses']" t-as="line">
                                    <td colspan="6" class="text-left">
                                        <h5>
                                            <span style="color: white;" t-esc="'......'"/>
                                            <span t-esc="line['cuenta_senainfo']"/>
                                        </h5>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h5>
                                            <span t-esc="line['total']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h5>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="6" class="text-left">
                                        <h4>
                                            <span style="color: white;" t-esc="'..'"/>
                                            <span>SALDO FINAL: </span>
                                        </h4>
                                    </td>
                                    <td colspan="6" class="text-right">
                                        <h4>
                                            <span t-esc="account['final_balance']" t-options="{'widget': 'monetary', 'display_currency': res_company.currency_id}"/>
                                        </h4>
                                    </td>
                                </tr>
                                <tr><td colspan="12"></td></tr>
                            </table>
                        </t>
                        <div class="row mb32">
                            <div class="col-3 text-center">
                                <br/><br/>
                                <strong>Representante OCA:</strong>
                            </div>
                            <div class="col-3 text-center">
                                <br/><br/>
                                <strong>Firma:</strong>
                            </div>
                            <div class="col-3 text-center">
                                <br/><br/>
                                <strong>Timbre:</strong>
                            </div>
                            <div class="col-3 text-center">
                                <br/><br/>
                                <strong>Fecha Presentación:</strong>
                            </div>
                        </div>
                    </t>
                </div>
            </t>
        </t>
    </t>
```
2. ### `report_expense_sheet
```html
?xml version="1.0"?>
<t t-name="hr_expense.report_expense_sheet">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="o">
                <t t-call="web.external_layout">
                    <div class="page">
<!--
                        <h2>Expenses Report</h2>
-->
                        <h2>
                            <t t-if="o.account_move_id.x_correlative == 0">
                              <span>DETALLE FONDOS POR RENDIR</span>
                            </t>
                            <t t-else="o.account_move_id.x_correlative > 0">
                              <span>COMPROBANTE DE </span><span class="text-uppercase" t-esc="o.account_move_id.x_document_type"/>
                              <span>Nº </span><span style="line-height: 200%;" t-esc="o.account_move_id.x_correlative"/>
                              <span> / </span>
                              <t t-if="o.account_move_id.date">
                                <span style="line-height: 200%;" t-esc="o.account_move_id.date.year"/>
                              </t>
                            </t>
                        </h2>
                        <br/>
                        <t t-if="o.account_move_id.x_correlative > 0">
                            <div id="informations" class="row mt8 mb8">
                                <div class="col-6">
                                    <P>ANTECEDENTES CONTABLES</P>
                                    <strong>
                                        <span t-att-style="'color: %s;' % o.company_id.secondary_color">Fecha:</span>
                                    </strong>
                                    <span style="color:gray" t-esc="o.account_move_id.invoice_date" t-options='{"widget": "date"}'/>
                                    <br/>
                    
                                    <strong>Empleado:</strong>
                                    <span style="color:gray" t-field="o.employee_id.name"/>
                                    <br/>
    <!--                
                                    <strong>Tipo Cuenta Ingreso:</strong>
                                    <span style="color:gray" t-field="o.account_move_id.x_account_group_id.name"/>
                                    <br/>
                    
                                    <strong>Documento Respaldo:</strong>
                                    <t t-if="o.account_move_id.x_document_type == 'INGRESO'">
                                        <span style="color:gray" t-field="o.account_move_id.x_in_back_up_document_type"/>
                                    </t>
                                    <t t-if="o.account_move_id.x_document_type == 'EGRESO'">
                                        <span style="color:gray" t-field="o.account_move_id.x_out_back_up_document_type"/>
                                    </t>
                                    <br/>
    -->                
                                    <strong>Descripción:</strong>
                                    <span style="color:gray" t-field="o.account_move_id.ref"/>
                                    <br/>
    
                                    <strong>Doc. Respaldo:</strong>
                                    <span style="color:gray">Rendición de Gastos</span>
                                    <br/>
    <!--                
                                    <strong>Nº Doc. Respaldo:</strong>
                                    <span style="color:gray" t-field="o.id"/>
                                    <br/>
    
                                    <strong>
                                        <span t-att-style="'color: %s;' % o.company_id.secondary_color">Fecha Doc. Resp.:</span>
                                    </strong>
                                    <span style="color:gray" t-esc="o.accounting_date" t-options='{"widget": "date"}'/>
                                    <br/>
                                    <br/>
    -->                
                                </div>
                                <div class="col-6">
                                    <P>ANTECEDENTES PROYECTO</P>
                                    <strong>Código Proyecto:</strong>
                                    <span style="color:gray" t-esc="o.account_move_id.x_account_analytic_account_id.code"/>
                                    <br/>
                    
                                    <strong>Nombre Proyecto:</strong>
                                    <span style="color:gray" t-esc="o.account_move_id.x_account_analytic_account_id.name"/>
                                    <br/>
                    
                                    <strong>Entidad Colaboradora:</strong>
                                    <span style="color:gray" t-field="o.account_move_id.company_id.partner_id.name"/>
                                    <br/>
                    
                                    <strong>Modalidad de Atención:</strong>
                                    <br/>
                                    <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'FAE'">
                                      <span style="color:gray">Familia de Acogida Especializada</span>
                                    </t>
                                    <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'PRO'">
                                      <span style="color:gray">Programa de Protección Especializado</span>
                                    </t>
                                    <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'PIE'">
                                      <span style="color:gray">Programas de Intervención Especializada</span>
                                    </t>
                                    <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'PRI'">
                                      <span style="color:gray">Programa de Intervención para niños Institucionalizados</span>
                                    </t>
                                    <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'PRM'">
                                      <span style="color:gray">Programas De Protección Especializada En Maltrato Y Abuso Sexual Grave</span>
                                    </t>
                                    <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'ADR'">
                                      <span style="color:gray">INSTITUCIÓN</span>
                                    </t>
                                    <br/>
                    
                                </div>
                            </div>
                        </t>
                        <br/>
<!--
                        <div class="row mt32 mb32">
                            <div class="col-2">
                                <strong>Employee:</strong>
                                <p t-field="o.employee_id.name"/>
                            </div>
                            <div class="col-2">
                                <strong>Date:</strong>
                                <p t-field="o.accounting_date"/>
                            </div>
                            <div class="col-3">
                                <strong>Description:</strong>
                                <p t-field="o.name"/>
                            </div>
                            <div class="col-2">
                                <strong>Validated By:</strong>
                                <p t-field="o.user_id"/>
                            </div>
                            <div class="col-3">
                                <strong>Payment By:</strong>
                                <p t-field="o.payment_mode"/>
                            </div>
                        </div>
-->
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Gasto</th>
                                    <th>Cuenta</th>
                                    <th>Tipo Doc.</th>
                                    <th>N° Doc.</th>
<!--
                                    <th class="text-right">P. Unitario</th>
                                    <th>Taxes</th>
                                    <th class="text-center">Cantidad</th>
-->
                                    <th class="text-right">Subtotal</th>
                                    <th t-if="o.is_multiple_currency" class="text-right">Price in Company Currency</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr t-foreach="o.expense_line_ids" t-as="line">
                                    <td><span t-field="line.date"/></td>
                                    <td>
                                        <span t-field="line.name"/>
<!--
                                        <span t-field="line.description"/><br/>
                                        <span t-field="line.analytic_account_id.name"/>
-->
                                    </td>
                                    <td style="text-center">
                                        <span t-field="line.account_id.name"/>
                                    </td>
                                    <td style="text-center">
                                        <span t-field="line.x_out_back_up_document_type"/>
                                    </td>
                                    <td style="text-center">
                                        <span t-field="line.x_back_up_document_number"/>
                                    </td>
<!--   
                                    <td class="text-right">
                                        <span t-field="line.unit_amount" t-options="{&quot;widget&quot;: &quot;monetary&quot;}"/>
                                    </td>
                                    <td>
                                        <t t-foreach="line.tax_ids" t-as="tax">
                                          <t t-if="tax.description">
                                            <span t-field="tax.description"/>
                                          </t>
                                          <t t-if="not tax.description">
                                            <span t-field="tax.name"/>
                                          </t>
                                        </t>
                                    </td>
                                    <td class="text-center">
                                        <span t-field="line.quantity" t-options="{&quot;widget&quot;: &quot;float&quot;, &quot;precision&quot;: 0}"/>
                                    </td>
-->   
                                    <td class="text-right">
                                        <span t-field="line.total_amount" t-options="{&quot;widget&quot;: &quot;monetary&quot;, &quot;display_currency&quot;: line.currency_id}"/>
                                    </td>
                                    <td t-if="o.is_multiple_currency" class="text-right">
                                        <span t-field="line.total_amount_company"/>
                                    </td>
                                </tr>
                            </tbody>
                        </table>

                        <div class="row justify-content-end">
                            <div class="col-4">
                                <table class="table table-sm">
                                    <tr class="border-black">
                                        <td><strong>Total</strong></td>
                                        <td class="text-right">
                                            <span t-field="o.total_amount" t-options="{&quot;widget&quot;: &quot;monetary&quot;, &quot;display_currency&quot;: o.currency_id}"/>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </div>

                        <br/><br/><br/><br/><br/><br/><br/>
                        <div class="clearfix row" style="align-items-center">
                          <div class="col-4">
                            <table class="table table-sm" border="1">
                              <tr class="border-black">
                                <td class="text-center">
                                    <span>FIRMA CONFORME</span>
                                 </td>
                                 <td></td>
                              </tr>
                            </table>                      
                          </div>
                          <div class="col-4">
                            <table class="table table-sm" border="1">
                              <tr class="border-black">
                                <td class="text-center">
                                    <span>FIRMA Y TIMBRE DIRECTOR (A)</span>
                                 </td>
                                 <td></td>
                              </tr>
                            </table>                      
                          </div>
                        </div>
<!--
                        <p>Certified honest and conform,<br/>(Date and signature).<br/><br/></p>
-->
                    </div>
                </t>
            </t>
        </t>
    </t>
```
3. ### `report_invoice_document`
```html
<?xml version="1.0"?>
<t t-name="account.report_invoice_document">
            <t t-call="web.external_layout">
                <t t-set="o" t-value="o.with_context(lang=lang)"/>
<!--
                <t t-set="address" invisible="1">
                    <address t-field="o.partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;], &quot;no_marker&quot;: True}"/>
                    <div t-if="o.partner_id.vat" class="mt16">
                        <t t-if="o.company_id.country_id.vat_label" t-esc="o.company_id.country_id.vat_label" id="inv_tax_id_label"/>
                        <t t-else="">Tax ID</t>: <span t-field="o.partner_id.vat"/></div>
                </t>
-->
                <div class="page">
                    <h2>
                          <span>COMPROBANTE DE </span><span class="text-uppercase" t-esc="o.x_document_type"/>
                          <span>Nº </span><span style="line-height: 200%;" t-esc="o.x_correlative"/>
                          <span> / </span><span style="line-height: 200%;" t-esc="o.invoice_date.year"/>
<!--
                        <span t-if="o.move_type == 'out_invoice' and o.state == 'posted'">Invoice</span>
                        <span t-if="o.move_type == 'out_invoice' and o.state == 'draft'">Draft Invoice</span>
                        <span t-if="o.move_type == 'out_invoice' and o.state == 'cancel'">Cancelled Invoice</span>
                        <span t-if="o.move_type == 'out_refund'">Credit Note</span>
                        <span t-if="o.move_type == 'in_refund'">Vendor Credit Note</span>
                        <span t-if="o.move_type == 'in_invoice'">Vendor Bill</span>
                        <span t-if="o.name != '/'" t-field="o.name"/>
-->
                    </h2>
                    <br/>
<!--
                    <div id="informations" class="row mt32 mb32">
                        <div class="col-auto col-3 mw-100 mb-2" t-if="o.invoice_date" name="invoice_date">
                            <strong>Invoice Date:</strong>
                            <p class="m-0" t-field="o.invoice_date"/>
                        </div>
                        <div class="col-auto col-3 mw-100 mb-2" t-if="o.invoice_date_due and o.move_type == 'out_invoice' and o.state == 'posted'" name="due_date">
                            <strong>Due Date:</strong>
                            <p class="m-0" t-field="o.invoice_date_due"/>
                        </div>
                        <div class="col-auto col-3 mw-100 mb-2" t-if="o.invoice_origin" name="origin">
                            <strong>Source:</strong>
                            <p class="m-0" t-field="o.invoice_origin"/>
                        </div>
                        <div class="col-auto col-3 mw-100 mb-2" t-if="o.partner_id.ref" name="customer_code">
                            <strong>Customer Code:</strong>
                            <p class="m-0" t-field="o.partner_id.ref"/>
                        </div>
                        <div class="col-auto col-3 mw-100 mb-2" t-if="o.ref" name="reference">
                            <strong>Reference:</strong>
                            <p class="m-0" t-field="o.ref"/>
                        </div>
                    </div>

                    <t t-set="display_discount" t-value="any(l.discount for l in o.invoice_line_ids)"/>
-->

                    <div id="informations" class="row mt8 mb8">
                        <div class="col-6">
                            <P>ANTECEDENTES CONTABLES</P>
                            <strong>
                                <span t-att-style="'color: %s;' % o.company_id.secondary_color">Fecha:</span>
                            </strong>
                            <span style="color:gray" t-esc="o.invoice_date" t-options='{"widget": "date"}'/>
                            <br/>
            
                            <strong t-if="o.move_type == 'out_invoice'">Benefactor:</strong>
                            <strong t-if="o.move_type == 'in_invoice'">Proveedor:</strong>
                            <span style="color:gray" t-field="o.invoice_partner_display_name"/>
                            <br/>
                            
                            <strong t-if="o.move_type == 'out_invoice'">Rut Benefactor:</strong>
                            <strong t-if="o.move_type == 'in_invoice'">Rut Proveedor:</strong>
                            <span style="color:gray" t-field="o.partner_id.vat"/>
                            <br/>
            
                            <strong>Tipo Cuenta Ingreso:</strong>
                            <span style="color:gray" t-field="o.x_account_group_id.name"/>
                            <br/>
            
                            <strong>Documento Respaldo:</strong>
                            <t t-if="o.move_type == 'out_invoice'">
                                <span style="color:gray" t-field="o.x_in_back_up_document_type"/>
                            </t>
                            <t t-if="o.move_type == 'in_invoice'">
                                <span style="color:gray" t-field="o.x_out_back_up_document_type"/>
                            </t>
                            <br/>
            
                            <strong>Nº Doc. Respaldo:</strong>
                            <span style="color:gray" t-field="o.x_back_up_document_number"/>
                            <br/>
            
                            <strong>
                                <span t-att-style="'color: %s;' % o.company_id.secondary_color">Fecha Doc. Resp.:</span>
                            </strong>
                            <span style="color:gray" t-esc="o.x_back_up_document_date" t-options='{"widget": "date"}'/>
                            <br/>
                            <br/>
            
                        </div>
                        <div class="col-6">
                            <P>ANTECEDENTES PROYECTO</P>
                            <strong>Código Proyecto:</strong>
                            <span style="color:gray" t-esc="o.x_account_analytic_account_id.code"/>
                            <br/>
            
                            <strong>Nombre Proyecto:</strong>
                            <span style="color:gray" t-esc="o.x_account_analytic_account_id.name"/>
                            <br/>
            
                            <strong>Entidad Colaboradora:</strong>
                            <span style="color:gray" t-field="o.company_id.partner_id.name"/>
                            <br/>
            
                            <strong>Modalidad de Atención:</strong>
                            <br/>
                            <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'FAE'">
                              <span style="color:gray">Familia de Acogida Especializada</span>
                            </t>
                            <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'PRO'">
                              <span style="color:gray">Programa de Protección Especializado</span>
                            </t>
                            <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'PIE'">
                              <span style="color:gray">Programas de Intervención Especializada</span>
                            </t>
                            <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'PRI'">
                              <span style="color:gray">Programa de Intervención para niños Institucionalizados</span>
                            </t>
                            <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'PRM'">
                              <span style="color:gray">Programas De Protección Especializada En Maltrato Y Abuso Sexual Grave</span>
                            </t>
                            <t t-if="str(o.x_account_analytic_account_id.name)[:3] == 'ADR'">
                              <span style="color:gray">INSTITUCIÓN</span>
                            </t>
                            <br/>
                        </div>
                    </div>

                    <table class="table table-sm o_main_table" name="invoice_line_table">
                        <thead>
                            <tr>
                                <th name="th_account_id" class="text-left"><span>Cuenta</span></th>
                                <th name="th_description" class="text-left"><span>Description</span></th>
                                <th name="th_analytic_account_id" class="text-left"><span>Prorrateo</span></th>
<!--
                                <th name="th_quantity" class="text-right"><span>Quantity</span></th>
                                <th name="th_priceunit" t-attf-class="text-right {{ 'd-none d-md-table-cell' if report_type == 'html' else '' }}"><span>Unit Price</span></th>
                                <th name="th_price_unit" t-if="display_discount" t-attf-class="text-right {{ 'd-none d-md-table-cell' if report_type == 'html' else '' }}">
                                    <span>Disc.%</span>
                                </th>
                                <th name="th_taxes" t-attf-class="text-left {{ 'd-none d-md-table-cell' if report_type == 'html' else '' }}"><span>Taxes</span></th>
-->
                                <th name="th_subtotal" class="text-right">
                                    <span groups="account.group_show_line_subtotals_tax_excluded">Monto</span>
                                    <span groups="account.group_show_line_subtotals_tax_included">Total Price</span>
                                </th>
                            </tr>
                        </thead>
                        <tbody class="invoice_tbody">
                            <t t-set="current_subtotal" t-value="0"/>
                            <t t-set="lines" t-value="o.invoice_line_ids.sorted(key=lambda l: (-l.sequence, l.date, l.move_name, -l.id), reverse=True)"/>

                            <t t-foreach="lines" t-as="line">
                                <t t-set="current_subtotal" t-value="current_subtotal + line.price_subtotal" groups="account.group_show_line_subtotals_tax_excluded"/>
                                <t t-set="current_subtotal" t-value="current_subtotal + line.price_total" groups="account.group_show_line_subtotals_tax_included"/>

                                <tr t-att-class="'bg-200 font-weight-bold o_line_section' if line.display_type == 'line_section' else 'font-italic o_line_note' if line.display_type == 'line_note' else ''">
                                    <t t-if="not line.display_type" name="account_invoice_line_accountable">
                                        <td class="text-left">
                                            <span t-field="line.account_id.name"/>
                                        </td>
                                        <td name="account_invoice_line_name"><span t-field="line.name" t-options="{'widget': 'text'}"/></td>
                                        <td class="text-left">
                                            <span t-field="line.analytic_account_id.name"/>
                                        </td>
<!--
                                        <td class="text-right">
                                            <span t-field="line.quantity"/>
                                            <span t-field="line.product_uom_id" groups="uom.group_uom"/>
                                        </td>
                                        <td t-attf-class="text-right {{ 'd-none d-md-table-cell' if report_type == 'html' else '' }}">
                                            <span class="text-nowrap" t-field="line.price_unit"/>
                                        </td>
                                        <td t-if="display_discount" t-attf-class="text-right {{ 'd-none d-md-table-cell' if report_type == 'html' else '' }}">
                                            <span class="text-nowrap" t-field="line.discount"/>
                                        </td>
                                        <td t-attf-class="text-left {{ 'd-none d-md-table-cell' if report_type == 'html' else '' }}">
                                            <span t-esc="', '.join(map(lambda x: (x.description or x.name), line.tax_ids))" id="line_tax_ids"/>
                                        </td>
-->
                                        <td class="text-right o_price_total">
<!--
                                            <span class="text-nowrap" t-field="line.price_subtotal" groups="account.group_show_line_subtotals_tax_excluded"/>
-->
                                            <span class="text-nowrap" t-field="line.price_total" groups="account.group_show_line_subtotals_tax_excluded"/>
                                            <span class="text-nowrap" t-field="line.price_total" groups="account.group_show_line_subtotals_tax_included"/>
                                        </td>
                                    </t>
                                    <t t-if="line.display_type == 'line_section'">
                                        <td colspan="99">
                                            <span t-field="line.name" t-options="{'widget': 'text'}"/>
                                        </td>
                                        <t t-set="current_section" t-value="line"/>
                                        <t t-set="current_subtotal" t-value="0"/>
                                    </t>
                                    <t t-if="line.display_type == 'line_note'">
                                        <td colspan="99">
                                            <span t-field="line.name" t-options="{'widget': 'text'}"/>
                                        </td>
                                    </t>
                                </tr>

                                <t t-if="current_section and (line_last or lines[line_index+1].display_type == 'line_section')">
                                    <tr class="is-subtotal text-right">
                                        <td colspan="99">
                                            <strong class="mr16">Subtotal</strong>
                                            <span t-esc="current_subtotal" t-options="{&quot;widget&quot;: &quot;monetary&quot;, &quot;display_currency&quot;: o.currency_id}"/>
                                        </td>
                                    </tr>
                                </t>
                            </t>
                        </tbody>
                    </table>
                    <br/>
                    <div class="clearfix">
                        <div id="total" class="row">
                            <div t-attf-class="#{'col-6' if report_type != 'html' else 'col-sm-7 col-md-6'} ml-auto">
                                <table class="table table-sm" style="page-break-inside: avoid;">
<!--
                                    <tr class="border-black o_subtotal" style="">
                                        <td><strong>Subtotal</strong></td>
                                        <td class="text-right">
                                            <span t-field="o.amount_untaxed"/>
                                        </td>
                                    </tr>
                                    <t t-foreach="o.amount_by_group" t-as="amount_by_group">
                                        <tr style="">
                                            <t t-if="len(o.line_ids.filtered(lambda line: line.tax_line_id)) in [0, 1] and o.amount_untaxed == amount_by_group[2]">
                                                <td><span class="text-nowrap" t-esc="amount_by_group[0]"/></td>
                                                <td class="text-right o_price_total">
                                                    <span class="text-nowrap" t-esc="amount_by_group[3]"/>
                                                </td>
                                            </t>
                                            <t t-else="">
                                                <td>
                                                    <span t-esc="amount_by_group[0]"/>
                                                    <span class="text-nowrap"> on
                                                        <t t-esc="amount_by_group[4]"/>
                                                    </span>
                                                </td>
                                                <td class="text-right o_price_total">
                                                    <span class="text-nowrap" t-esc="amount_by_group[3]"/>
                                                </td>
                                            </t>
                                        </tr>
                                    </t>
-->
                                    <tr class="border-black o_total">
                                        <td><strong>Total</strong></td>
                                        <td class="text-right">
                                            <span class="text-nowrap" t-field="o.amount_total"/>
                                        </td>
                                    </tr>
<!--
                                    <t t-if="print_with_payments">
                                        <t t-if="o.payment_state != 'invoicing_legacy'">
                                            <t t-set="payments_vals" t-value="o.sudo()._get_reconciled_info_JSON_values()"/>
                                            <t t-foreach="payments_vals" t-as="payment_vals">
                                                <tr>
                                                    <td>
                                                        <i class="oe_form_field text-right oe_payment_label">Pagado con <t t-esc="payment_vals['payment_method_name']"/> el <t t-esc="payment_vals['date']" t-options="{&quot;widget&quot;: &quot;date&quot;}"/></i>
                                                    </td>
                                                    <td class="text-right">
                                                        <span t-esc="payment_vals['amount']" t-options="{&quot;widget&quot;: &quot;monetary&quot;, &quot;display_currency&quot;: o.currency_id}"/>
                                                    </td>
                                                </tr>
                                            </t>
                                            <t t-if="len(payments_vals) &gt; 0">
                                                <tr class="border-black">
                                                    <td><strong>Pendiente de pago:</strong></td>
                                                    <td class="text-right">
                                                        <span t-field="o.amount_residual"/>
                                                    </td>
                                                </tr>
                                            </t>
                                        </t>
                                    </t>
-->
                                </table>
                            </div>
                        </div>
                    </div>
                    <br/>
                    <table class="table table-sm o_main_table" name="payments_line_table">
                        <p>REGISTRO DE PAGOS</p>
                        <thead>
                            <tr>
                                <th name="th_payment_bank" class="text-left"><span>Banco</span></th>
                                <th name="th_payment_bank_acc_number" class="text-center"><span>Nº Cuenta</span></th>
                                <th name="th_payment_date" class="text-center"><span>Fecha</span></th>
                                <th name="th_payment_method" class="text-left"><span>Forma de Pago</span></th>
                                <th name="th_payment_number" class="text-center"><span>Nº Comprobante</span></th>
                                <th name="th_payment_amount" class="text-right"><span>Monto</span></th>
                            </tr>
                        </thead>
                        <tbody class="invoice_tbody">
                            <t t-if="print_with_payments">
                                <t t-if="o.payment_state != 'invoicing_legacy'">
                                    <t t-set="payments_vals" t-value="o.sudo()._get_reconciled_info_JSON_values()"/>
                                    <t t-foreach="payments_vals" t-as="payment_vals">
                                        <tr>
                                            <td class="text-left">
                                                <t t-esc="payment_vals['bank_name']"/>
                                            </td>
                                            <td class="text-center">
                                                <t t-esc="payment_vals['bank_acc_number']"/>
                                            </td>
                                            <td class="text-center">
                                                <t t-esc="payment_vals['date']" t-options="{&quot;widget&quot;: &quot;date&quot;}"/>
                                            </td>
                                            <td class="text-left">
                                                <t t-esc="payment_vals['payment_method_name']"/>
                                            </td>
                                            <td class="text-center">
                                                <t t-esc="payment_vals['x_income_document_number']"/>
                                            </td>
                                            <td class="text-right">
                                                <span t-esc="payment_vals['amount']" t-options="{&quot;widget&quot;: &quot;monetary&quot;, &quot;display_currency&quot;: o.currency_id}"/>
                                            </td>
                                        </tr>
                                    </t>
                                </t>
                            </t>
                        </tbody>
                    </table>
<!--
                    <t t-if="o.amount_residual &gt; 0">
                      <div class="clearfix">
                          <div id="payment_total" class="row">
                              <div t-attf-class="#{'col-6' if report_type != 'html' else 'col-sm-7 col-md-6'} ml-auto">
                                  <table class="table table-sm" style="page-break-inside: avoid;">
                                        <tr class="border-black" style="">
                                            <td><strong>Pendiente de pago:</strong></td>
                                            <td class="text-right">
                                                <span t-field="o.amount_residual"/>
                                            </td>
                                        </tr>
                                  </table>
                              </div>
                          </div>
                      </div>
                    </t>
-->
                    <br/><br/><br/><br/><br/><br/><br/>
                    <div class="clearfix row" style="align-items-center">
                      <div class="col-4">
                        <table class="table table-sm" border="1">
                          <tr class="border-black">
                            <td class="text-center">
                                <span>FIRMA CONFORME</span>
                             </td>
                             <td></td>
                          </tr>
                        </table>                      
                      </div>
                      <div class="col-4">
                        <table class="table table-sm" border="1">
                          <tr class="border-black">
                            <td class="text-center">
                                <span>FIRMA Y TIMBRE DIRECTOR (A)</span>
                             </td>
                             <td></td>
                          </tr>
                        </table>                      
                      </div>
                    </div>
<!--
                    <p t-if="o.move_type in ('out_invoice', 'in_refund') and o.payment_reference" name="payment_communication">
                        Please use the following communication for your payment : <b><span t-field="o.payment_reference"/></b>
                    </p>
                    <p t-if="o.invoice_payment_term_id" name="payment_term">
                        <span t-field="o.invoice_payment_term_id.note"/>
                    </p>
                    <p t-if="o.narration" name="comment">
                        <span t-field="o.narration"/>
                    </p>
                    <p t-if="o.fiscal_position_id.note" name="note">
                        <span t-field="o.fiscal_position_id.note"/>
                    </p>
                    <p t-if="o.invoice_incoterm_id" name="incoterm">
                        <strong>Incoterm: </strong><span t-field="o.invoice_incoterm_id.code"/> - <span t-field="o.invoice_incoterm_id.name"/>
                    </p>
                    <div id="qrcode" t-if="o.display_qr_code">
                        <p t-if="qr_code_urls.get(o.id)">
                            <strong class="text-center">Scan me with your banking app.</strong><br/><br/>
                            <img class="border border-dark rounded" t-att-src="qr_code_urls[o.id]"/>
                        </p>
                    </div>
-->
                </div>
            </t>
        </t>
```

 