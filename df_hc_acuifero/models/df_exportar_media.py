# -*- coding: utf-8 -*-
import datetime

import xlwt
from odoo import models, fields, api
from odoo.modules import module
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import MissingError, _logger, Warning
from xlwt import Workbook,Style,easyxf
from odoo.tools.translate import _
import os
import io
# import StringIO
import base64


class df_exportar_media(models.Model):
    _name = 'df.exportar.media'
    _description = 'Export average level of wells'

    # @api.onchange('metodo_formula')
    # def onchange_tipo_calculo(self):
    #     res = {}
    #     if self.tipo:
    #         res.update({'metodo_aritmetico': False, 'metodo_formula': True})
    #     else:
    #         res.update({'metodo_aritmetico': True, 'metodo_formula': False})
    #     return res

    # @api.onchange
    # def onchange_elemento_exportar(self):
    #     res = {}
    #     res.update({'pozo_bloque_ids': False, 'pozo_sector_ids': False, 'pozo_cuenca_ids': False})
    #     return res

    def _default_initial_date(self):
        date = datetime.datetime(1982, 1, 1, 0, 0)
        return date.strftime('%Y-%m-%d')

    @api.onchange('desde', 'hasta')
    def _reset_state(self):
        self.state = 'choose'
        if self.desde and self.hasta:
            if self.desde > self.hasta:
                # self.fecha_ini = None
                raise Warning(('La fecha inicial no puede ser mayor que la final, verifique.'))


    desde = fields.Date(string='From', required=True, default=_default_initial_date)
    hasta = fields.Date(string='To', required=True, default=fields.Date.context_today)
    elemento_exportar = fields.Selection([('cuenca', 'Basin'),
                                          ('sector', 'Sector'),
                                          ('bloque', 'Block')],
                                         string='Element to export', required=True,
                                         help="", default='sector')

    metodo_formula = fields.Boolean(string='Formula', required=False)

    cuenca_ids = fields.Many2many('df.cuenca.subterranea', 'mm_export_media_cuenca_rel', 'exportar_media_id',
                                  'cuenca_id', required=True)
    sector_ids = fields.Many2many('df.sector.hidrologico', 'mm_export_media_sector_rel', 'exportar_media_id',
                                  'sector_id', required=True)
    bloque_ids = fields.Many2many('df.bloque', 'mm_export_media_bloque_rel', 'exportar_media_id', 'bloque_id',
                                  required=True)

    pozo_bloque_ids = fields.Many2many('df.pozo', 'mm_export_bloque_pozos', 'export_if', 'pozo_id')
    pozo_sector_ids = fields.Many2many('df.pozo', 'mm_export_sector_pozos', 'export_if', 'pozo_id')
    pozo_cuenca_ids = fields.Many2many('df.pozo', 'mm_export_cuenca_pozos', 'export_if', 'pozo_id')

    file = fields.Binary('File', filename="module_filename",)

    
    @api.multi
    def exportar(self):
        data = self.read()[0]
        pozo_obj = self.env['df.pozo']
        if data['elemento_exportar'] == 'sector':
            obj_export = self.env['df.sector.hidrologico']
            obj_ids = data['sector_ids']
            if not obj_ids:
                raise UserError(_("You must select at least one Hydrogeological sector to export"))

            pozo_ids = data['pozo_sector_ids']
            if not pozo_ids:
                pozo_ids = pozo_obj.with_context({'exportar_filtro': 'sector', 'filtro': [[0, False, obj_ids]]}).search([]).ids
        elif data['elemento_exportar'] == 'bloque':
            obj_export = self.env['df.bloque']
            obj_ids = data['bloque_ids']
            if not obj_ids:
                raise UserError(_("You must select at least one Block to export"))
            pozo_ids = data['pozo_bloque_ids']
            if not pozo_ids:
                pozo_ids = pozo_obj.with_context({'exportar_filtro': 'bloque', 'filtro': [[0, False, obj_ids]]}).search([]).ids
        elif data['elemento_exportar'] == 'cuenca':
            obj_export = self.env['df.cuenca.subterranea']
            obj_ids = data['cuenca_ids']
            if not obj_ids:
                raise UserError(_("You must select at least one Underground basin to export"))
            pozo_ids = data['pozo_cuenca_ids']
            if not pozo_ids:
                pozo_ids = pozo_obj.with_context({'exportar_filtro': 'cuenca', 'filtro': [[0, False, obj_ids]]}).search([]).ids

        if not pozo_ids:
            raise UserError(_("There isn't a well in any selected object in system"))

        if data['desde'] and data['hasta']:
            fecha1 = data['desde'],
            fecha2 = data['hasta'],

            fecha_inicio = datetime.datetime.strptime(str(fecha1[0]), '%Y-%m-%d')
            fecha_fin = datetime.datetime.strptime(str(fecha2[0]), '%Y-%m-%d')

            if fecha_inicio > fecha_fin:
                raise UserError(_("La fecha de inicio no puede ser mayor a la de fin"))
        else:
            fecha_inicio = None
            fecha_fin = None

        wb = xlwt.Workbook()
        encabezados = ['Fecha', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sept', 'Oct', 'Nov', 'Dic']

        for obj_id in obj_ids:
            fila = 2
            columna = 0
            obj = obj_export.browse(obj_id)
            if not data['metodo_formula']:
                media = obj_export.calcular_media_aritmetica([obj_id], pozo_ids, fecha_inicio, fecha_fin)
            else:
                # media = obj_export.calcular_media_por_formula(cr, uid, [obj_id], pozo_ids, fecha_inicio, fecha_fin, data['a0'], data['a1'], context)
                media = obj_export.calcular_media_por_formula([obj_id], pozo_ids, fecha_inicio, fecha_fin)
            if data['elemento_exportar'] != 'cuenca':
                identificador = obj.sigla
            else:
                identificador = obj.nombre
            ws = wb.add_sheet(identificador, cell_overwrite_ok=True)
            style0 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                                 'pattern: pattern solid, fore_colour light_blue;')
            style1 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                                 'pattern: pattern solid, fore_colour light_green;')
            style2 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                                 'pattern: pattern solid, fore_colour pale_blue;')
            style3 = xlwt.easyxf('font: name Arial, colour black')
            for encabezado in encabezados:
                if columna == 0:
                    ws.write(fila, columna, encabezado, style0)
                else:
                    ws.write(fila, columna, encabezado, style1)
                columna += 1
            fila += 1
            for valor in media[0]:
                columna = 0
                while columna < 13:
                    if columna == 0:
                        ws.write(fila, columna, valor['anno'], style2)
                    elif valor.get(str(columna)):
                        ws.write(fila, columna, round(valor[str(columna)], 2), style3)
                    columna += 1
                fila += 1
        
        path = 'odoo/addons/mediapozos.xls'

        wb.save(path)
        # value = {
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'df.exportar.media.dialogo',
        #     'views': [],
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        #     'context': {'path': path, 'file_name': 'mediapozos.xls'}
        # }
        # return value
        backup = open(path, 'rb')
        self.file = base64.encodestring(backup.read())
        backup.close()
        return {
            'type': 'ir.actions.act_url',
            'name': 'Salvar BD',
            'url': '/web/content/%s/%s/file/%s?download=true' % (self._name, self.id, "mediapozos.xls"),
        }

        

    


