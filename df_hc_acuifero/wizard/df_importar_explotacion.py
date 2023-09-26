# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError
import base64
from odoo.modules import module
from odoo import tools
from xlrd import open_workbook
import os
# from openerp.modules import module
# from tools.translate import _
# import tools
# from osv import osv, fields

import fnmatch


class df_importar_explotacion(models.TransientModel):
    _name = 'df.importar.explotacion'
    _description = 'Wizard to import exploitation'

    # def _list_files(self, cr, uid, context=None):
    #     # returns a list of names (with extension, without full path) of all files
    #     # in folder path
    #
    #     shared_directory_obj = self.pool.get('df.directorio.compartido')
    #     active_dir_id = shared_directory_obj.search(cr, uid, [('is_active', '=', True)], context=context)
    #     files = []
    #     if active_dir_id:
    #         active_dir = shared_directory_obj.browse(cr, uid, active_dir_id[0], context)
    #         path = active_dir.path
    #         for name in os.listdir(path):
    #             if os.path.isfile(os.path.join(path, name)):
    #                 if fnmatch.fnmatch(name, '*.xls') or fnmatch.fnmatch(name, '*.xlsx'):
    #                     files.append((name, name))
    #     return files

    excel = fields.Binary('Excel file', help='Excel file (recommended format: xlsx) to import')
    objeto = fields.Selection([('well', 'Well'),
                               ('block', 'Block'),
                               ('sector', 'Sector'),
                               ('underground_basin', 'Underground basin')],
                              string='Object to import', required=True,
                              help='Object that is going to care exploitation values')
    # direct_path = fields.Boolean('Having errors?',
    #                               help='Check this field if you are having errors at the time of importing '
    #                                    'data by selection excel file')
    # filename = fields.Selection(_list_files, 'Filename', size=32,
    #                              help='This solution allows to select a file previously uploaded to the server')


    def lengthmonth(self, year, month):
        if month == 2 and ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))):
            return 29
        return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]

    def lengthyear(self, year):
        if  self.lengthmonth(year,2) == 28:
            return 365
        return 366

    def _importar_explotacion(self, objeto, wb):
        if objeto == 'well':
            obj = self.env['df.pozo']
            exp_plan_obj = self.env['df.plan.explotacion.anual.pozo']
            exp_real_obj = self.env['df.explotacion.anual.pozo']
        elif objeto == 'block':
            obj = self.env['df.bloque']
            exp_plan_obj = self.env['df.explotacion.bloque.plan']
            exp_real_obj = self.env['df.explotacion.bloque.real']
        elif objeto == 'sector':
            obj = self.env['df.sector.hidrologico']
            exp_plan_obj = self.env['df.explotacion.sector.plan']
            exp_real_obj = self.env['df.explotacion.sector.real']
        elif objeto == 'underground_basin':
            obj = self.env['df.cuenca.subterranea']
            exp_plan_obj = self.env['df.explotacion.cuenca.plan']
            exp_real_obj = self.env['df.explotacion.cuenca.real']

        numero_hojas = wb.nsheets
        for nro_hoja in range(numero_hojas):
            pestanna = wb.sheet_by_index(nro_hoja)
            identificador_objeto = pestanna.name
            numero_filas = pestanna.nrows
            identificador_objeto = tools.ustr(identificador_objeto)
            if objeto == 'underground_basin':
                objeto_ids = obj.search([('codigo','=',identificador_objeto)])
            else:
                objeto_ids = obj.search([('sigla','=',identificador_objeto)])
            if objeto_ids:
                for nro_fila in range(2,numero_filas):
                    if pestanna.cell_type(rowx=nro_fila, colx=0) == 2:  # verifico si la fila es la de un anno con datos
                        pestanna.cell_value(rowx=nro_fila, colx=0)
                        vals_plan = {}
                        vals_real = {}
                        if objeto == 'well':
                            vals_plan['pozo_id'] = objeto_ids[0].id
                            vals_real['pozo_id'] = objeto_ids[0].id
                        elif objeto == 'block':
                            vals_plan['bloque_id'] = objeto_ids[0].id
                            vals_real['bloque_id'] = objeto_ids[0].id
                        elif objeto == 'sector':
                            vals_plan['sector_id'] = objeto_ids[0].id
                            vals_real['sector_id'] = objeto_ids[0].id
                        elif objeto == 'underground_basin':
                            vals_plan['cuenca_id'] = objeto_ids[0].id
                            vals_real['cuenca_id'] = objeto_ids[0].id
                        vals_plan['anno'] = pestanna.cell_value(rowx=nro_fila, colx=0)
                        vals_real['anno'] = pestanna.cell_value(rowx=nro_fila, colx=0)
                        vals_plan['media_hiperanual_enero_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=1))),3)
                        vals_real['media_hiperanual_enero_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=2))),3)
                        vals_plan['media_hiperanual_febrero_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=3))),3)
                        vals_real['media_hiperanual_febrero_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=4))),3)
                        vals_plan['media_hiperanual_marzo_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=5))),3)
                        vals_real['media_hiperanual_marzo_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=6))),3)
                        vals_plan['media_hiperanual_abril_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=7))),3)
                        vals_real['media_hiperanual_abril_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=8))),3)
                        vals_plan['media_hiperanual_mayo_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=9))),3)
                        vals_real['media_hiperanual_mayo_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=10))),3)
                        vals_plan['media_hiperanual_junio_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=11))),3)
                        vals_real['media_hiperanual_junio_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=12))),3)
                        vals_plan['media_hiperanual_julio_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=13))),3)
                        vals_real['media_hiperanual_julio_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=14))),3)
                        vals_plan['media_hiperanual_agosto_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=15))),3)
                        vals_real['media_hiperanual_agosto_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=16))),3)
                        vals_plan['media_hiperanual_septiembre_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=17))),3)
                        vals_real['media_hiperanual_septiembre_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=18))),3)
                        vals_plan['media_hiperanual_octubre_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=19))),3)
                        vals_real['media_hiperanual_octubre_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=20))),3)
                        vals_plan['media_hiperanual_noviembre_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=21))),3)
                        vals_real['media_hiperanual_noviembre_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=22))),3)
                        vals_plan['media_hiperanual_diciembre_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=23))),3)
                        vals_real['media_hiperanual_diciembre_string'] = round(float((pestanna.cell_value(rowx=nro_fila, colx=24))),3)

                        if objeto == 'well':
                            string_objeto_id = 'pozo_id'
                        elif objeto == 'block':
                            string_objeto_id = 'bloque_id'
                        elif objeto == 'sector':
                            string_objeto_id = 'sector_id'
                        elif objeto == 'underground_basin':
                            string_objeto_id = 'cuenca_id'
                        explotacion_anno_plan_ids = exp_plan_obj.search([(string_objeto_id,'=',vals_plan[string_objeto_id]),('anno','=',vals_plan['anno'])])
                        explotacion_anno_real_ids = exp_real_obj.search([(string_objeto_id,'=',vals_real[string_objeto_id]),('anno','=',vals_real['anno'])])

                        if explotacion_anno_plan_ids and explotacion_anno_real_ids :
                            explotacion_anno_plan_ids.write(vals_plan)
                            explotacion_anno_real_ids.write(vals_real)
                        else:
                            exp_plan_obj.create(vals_plan)
                            exp_real_obj.create(vals_real)

    def importar(self):
        data = self.read()[0]
        excel = data['excel']
        path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp', 'cc.xlsx')
        fileobj = open(path, "wb")
        if excel != False:
            fileobj.write(base64.b64decode(excel))
            fileobj.flush()
            fileobj.close()
            try:
                wb = open_workbook(path)
            except:
                raise UserError(_('Seleccione un fichero excel!'))
            self._importar_explotacion(data['objeto'], wb)
        else:
            raise UserError(_('Seleccione un fichero excel!'))
        return {'type': 'ir.actions.act_window_close'}

        # if self.context is None:
        #     context = {}
        #
        # this = self.browse(self.env.uid, self.ids[0])
        # if not this.direct_path:
        #     if this.excel:
        #         # ################### GUARDANDO EXCEL EN RUTA TEMPORAL #######################################
        #         excel = this.excel
        #         path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp',
        #                             'prueba.xlsx')  # module.get_module_path('df_hc_embalse/') + "tmp/cc.xlsx"
        #         fileobj = open(path, "wb")
        #         fileobj.write(base64.b64decode(excel))
        #         fileobj.flush()
        #         fileobj.close()
        #         #################### TRABAJO CON EXCEL PARA IMPORTAR ########################################
        #     else:
        #         raise osv.except_osv(_('Error: '), _('You must select an excel file!'))
        # else:
        #     shared_directory_obj = self.env['df.directorio.compartido']
        #     active_dir_id = shared_directory_obj.search(self.env.uid, [('is_active', '=', True)])[0]
        #     active_dir = shared_directory_obj.browse(self.env.uid, active_dir_id)
        #     path = active_dir.path + '/' + this.filename
        #
        # try:
        #     wb = open_workbook(path)
        # except Exception:
        #     raise osv.except_osv(_('Error'), _('An error has ocurred during importation. Please, check if format of selected file is correct!'))
        # self._importar_explotacion(self.env.uid, this.objeto, wb, context)
        #
        # return {'type': 'ir.actions.act_window_close'}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
