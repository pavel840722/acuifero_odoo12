# -*- coding: utf-8 -*-
# from openerp.modules import module
from odoo import models, fields, api,_
from odoo.modules import module
from odoo.exceptions import UserError, ValidationError
import base64
import xlrd
from xlrd import open_workbook
# from tools.translate import _
from odoo import tools
# from osv import osv, fields
import os
import fnmatch


class df_importar_niveles_pozos(models.TransientModel):
    _name = 'df.importar.niveles.pozos'
    _description = 'Wizard to import wells levels'

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

    excel = fields.Binary('Excel file (recommended format: xlsx) to import')
    # direct_path = fields.Boolean('Having errors?',
    #                                   help='Check this field if you are having errors at the time '
    #                                        'of importing data by selection excel file')
    # filename = fields.Selection(_list_files, 'Filename', size=32,
    #                                  help='This solution allows to select a file previously uploaded to the server')


    def lengthmonth(self, year, month):
        if month == 2 and ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))):
            return 29
        return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]

    def lengthyear(self, year):
        if  self.lengthmonth(year,2) == 28:
            return 365
        return 366

    def _importar_niveles(self, wb):
        pozo_obj = self.env['df.pozo']
        nivel_pozo_obj = self.env['df.nivel.anual.pozo']
        pozo_ids_actualizar = []
        # cuenca_obj = self.pool.get('df.cuenca.subterranea')
        # sector_obj = self.pool.get('df.sector.hidrologico')
        # bloque_obj = self.pool.get('df.bloque')
        # pozo_obj = self.pool.get('df.pozo')
        # pozo_obj.obtener_promedio_alturas(cr,uid)
        # bloque_obj.obtener_promedio_alturas(cr,uid)
        # bloque_obj.obtener_promedio_alturas_formula(cr,uid)
        # sector_obj.obtener_promedio_alturas(cr,uid)
        # sector_obj.obtener_promedio_alturas_formula(cr,uid)
        # cuenca_obj.obtener_promedio_alturas(cr,uid)
        # cuenca_obj.obtener_promedio_alturas_formula(cr,uid)
        # return True

        numero_hojas = wb.nsheets
        for nro_hoja in range(numero_hojas):
            pestanna = wb.sheet_by_index(nro_hoja)
            identificador_pozo = pestanna.name
            numero_filas = pestanna.nrows
            identificador_pozo = tools.ustr(identificador_pozo)
            pozo_ids = pozo_obj.search([('sigla','=',identificador_pozo)])
            if pozo_ids:
                pozo_ids_actualizar.append(pozo_ids[0])
                for nro_fila in range(2,numero_filas):
                    if pestanna.cell_type(rowx=nro_fila, colx=0) == 2:  # verifico si la fila es la de un anno con datos
                        pestanna.cell_value(rowx=nro_fila, colx=0)
                        vals = {}
                        vals['pozo_id'] = pozo_ids[0].id
                        vals['anno'] = int(pestanna.cell_value(rowx=nro_fila, colx=0))
                        vals['media_hiperanual_enero_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=1))
                        vals['media_hiperanual_febrero_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=2))
                        vals['media_hiperanual_marzo_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=3))
                        vals['media_hiperanual_abril_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=4))
                        vals['media_hiperanual_mayo_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=5))
                        vals['media_hiperanual_junio_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=6))
                        vals['media_hiperanual_julio_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=7))
                        vals['media_hiperanual_agosto_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=8))
                        vals['media_hiperanual_septiembre_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=9))
                        vals['media_hiperanual_octubre_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=10))
                        vals['media_hiperanual_noviembre_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=11))
                        vals['media_hiperanual_diciembre_string'] = str(pestanna.cell_value(rowx=nro_fila, colx=12))
                        nivel_pozo_anno_ids = nivel_pozo_obj.search([('pozo_id','=',vals['pozo_id']),('anno','=',vals['anno'])])
                        if nivel_pozo_anno_ids:
                            nivel_pozo_anno_ids.write(vals)
                        else:
                            nivel_pozo_obj.create(vals)
        return pozo_ids_actualizar

    def importar(self):
        data = self.read()[0]
        excel = data['excel']
        # path = os.path.join(module.get_module_path('df_hc_embalse'), 'tmp', 'cc.xlsx')  # module.get_module_path('df_hc_embalse/') + "tmp/cc.xlsx"
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
            # self._importar_normas(wb)
            self._importar_niveles(wb)
        else:
            raise UserError(_('Seleccione un fichero excel!'))
        return {'type': 'ir.actions.act_window_close'}

        # cuenca_obj = self.env['df.cuenca.subterranea']
        # sector_obj = self.env['df.sector.hidrologico']
        # bloque_obj = self.env['df.bloque']
        # pozo_obj = self.env['df.pozo']
        # if self.env.context is None:
        #     context = {}

        # this = self.browse(self.env.uid, self.ids[0])
        # this = self.search([])[0]
        # this = self.read([])[0]
        # excel = this['excel']
        # if not this.direct_path:
        # if this.excel:
            #################### GUARDANDO EXCEL EN RUTA TEMPORAL #######################################
            # excel = this.excel
        # path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp', 'cc.xlsx') # module.get_module_path('df_hc_embalse/') + "tmp/cc.xlsx"
        # fileobj = open(path, 'wb')
        # if excel != False:
        #     fileobj.write(base64.b64decode(excel))
        #     fileobj.flush()
        #     fileobj.close()
        #     #################### TRABAJO CON EXCEL PARA IMPORTAR ########################################
        # else:
        #     raise osv.except_osv(_('Error: '), _('You must select an excel file!'))
        # else:
        #     shared_directory_obj = self.env['df.directorio.compartido']
        #     active_dir_id = shared_directory_obj.search(self.env.uid, [('is_active', '=', True)])[0]
        #     active_dir = shared_directory_obj.browse(self.env.uid, active_dir_id, context)
        #     path = active_dir.path + '/' + this.filename

        # try:
        #     wb = open_workbook(path)
        # except Exception:
        #     raise osv.except_osv(_('Error'), _('An error has ocurred during importation. Please, check if format of selected file is correct!'))
        # ok=True
        # pozo_ids_actualizar = self._importar_niveles(wb)

        # pozo_obj.obtener_promedio_alturas(self.env.uid,pozo_ids_actualizar,ok)
        # bloque_obj.obtener_promedio_alturas(self.env.uid,pozo_ids_actualizar,ok)
        # bloque_obj.obtener_promedio_alturas_formula(self.env.uid,pozo_ids_actualizar,ok)
        # sector_obj.obtener_promedio_alturas(self.env.uid,pozo_ids_actualizar,ok)
        # sector_obj.obtener_promedio_alturas_formula(self.env.uid,pozo_ids_actualizar,ok)
        # cuenca_obj.obtener_promedio_alturas(self.env.uid,pozo_ids_actualizar,ok)
        # cuenca_obj.obtener_promedio_alturas_formula(self.env.uid,pozo_ids_actualizar,ok)

        # return {'type': 'ir.actions.act_window_close'}
        #except:
        #    raise osv.except_osv(_('Error: '), _('In the import process some error was encountered, please make sure the excel format is correct. If error persist contact to admin!'))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
