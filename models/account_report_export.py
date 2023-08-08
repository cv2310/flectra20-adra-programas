# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

import io
import math

from flectra import http
# from flectra.http import serialize_exception as _serialize_exception
from flectra.exceptions import UserError
from flectra.tools import pycompat

from flectra.addons.web.controllers.main import serialize_exception, Export, ExportFormat  # Import the class


class CustomExportController(Export):

    @http.route('/web/export/formats', type='json', auth="user")
    def formats(self):
        res = super(CustomExportController, self).formats()
        res.append({'tag': 'txt', 'label': 'TXT'})
        return res

class TXTExport(ExportFormat, http.Controller):

    @http.route('/web/export/txt', type='http', auth="user")
    @serialize_exception
    def index(self, data, token):
        return self.base(data, token)

    @property
    def content_type(self):
        return 'text/csv;charset=utf8'

    def filename(self, base):
        return 'ADRA - Ingresos-Egresos Institucion.txt'

    def from_group_data(self, fields, groups):
        raise UserError(_("Exporting grouped data to txt is not supported."))

    def clean_text(self, text):
        words = text.split(' ')
        clear_text = ''
        aux_text = ''
        
        for word in words:
            if word != '':
                aux_text = ''.join(filter(str.isalnum, word)).upper()
                aux_text = aux_text.replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U").replace("Ñ","N")
                clear_text += aux_text + ' '

        return clear_text.rstrip()

    def format_data(self, row):
        line_str = ''
        if row['tipo_docto_senainfo'] == 1: # Ingreso
            line_str += pycompat.to_text(str(row['tipo_docto_senainfo']))
            line_str += pycompat.to_text(row['cod_programa'].zfill(9))
            line_str += pycompat.to_text(row['periodo'])
            line_str += pycompat.to_text(row['fecha_ingreso'].strftime('%d-%m-%Y'))
            line_str += pycompat.to_text(str(row['nro_comprobante']).zfill(9))
            line_str += pycompat.to_text(str(row['correlativo']).zfill(9))
            line_str += pycompat.to_text(row['fecha_pago'].strftime('%d-%m-%Y'))
            line_str += pycompat.to_text(str(row['vigencia']))
            line_str += pycompat.to_text(str(row['cod_cuenta_senainfo']).zfill(9))
            line_str += pycompat.to_text(str(math.trunc(abs(row['monto']))).zfill(9))
            line_str += pycompat.to_text(self.clean_text(row['glosa'][0:20]).ljust(20,' ').ljust(89,'-'))
        elif row['tipo_docto_senainfo'] == 0: # Egreso
            line_str += pycompat.to_text(str(row['tipo_docto_senainfo']))
            line_str += pycompat.to_text(row['cod_programa'].zfill(9))
            line_str += pycompat.to_text(row['periodo'])
            line_str += pycompat.to_text(row['fecha_ingreso'].strftime('%d-%m-%Y'))
            line_str += pycompat.to_text(str(row['nro_comprobante']).zfill(9))
            line_str += pycompat.to_text(str(row['correlativo']).zfill(9))
            line_str += pycompat.to_text(row['fecha_pago'].strftime('%d-%m-%Y'))
            line_str += pycompat.to_text(str(row['vigencia']))
            line_str += pycompat.to_text(str(row['medio_pago_senainfo']).rjust(9,' '))
            line_str += pycompat.to_text(str(math.trunc(abs(row['monto']))).zfill(9))
            row['glosa'] = self.clean_text(row['glosa'])
            if len(row['glosa']) > 19:
                line_str += pycompat.to_text(row['glosa'][0:20])
            else:
                line_str += pycompat.to_text(row['glosa'].ljust(20,' '))
            line_str += pycompat.to_text(str(row['cod_cuenta_senainfo']).zfill(9))
            line_str += pycompat.to_text(row['nro_comprobante_pago'].rjust(20,' '))
            row['beneficiario'] = self.clean_text(row['beneficiario'])
            if len(row['beneficiario']) > 39:
                line_str += pycompat.to_text(row['beneficiario'][0:39].rjust(40,' '))
            else:
                line_str += pycompat.to_text(row['beneficiario'].rjust(40,' '))

        line_str += "\n"

        return line_str

    def from_data(self, fields, rows):
        fp = io.StringIO()

        for data in rows:
            zip_item = zip(fields, data)
            item = dict(zip_item)
            fp.write(self.format_data(item))

        return fp.getvalue()
