# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError
import base64
from odoo.modules import module
from odoo import tools
from xlrd import open_workbook
import os
import fnmatch


class df_importar_probabilidad_lluvia(models.TransientModel):
    _name = 'df.importar.probabilidad.lluvia'
    _description = 'Wizard to import norms levels'

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
    # direct_path  = fields.Boolean('Having errors?',
    #                help='Check this field if you are having errors at the time of importing data by selection excel file')
    # filename = fields.Selection(_list_files, 'Filename', size=32,
    #                             help='This solution allows to select a file previously uploaded to the server')
    # tipo = fields.Selection([('Historic Volumen', 'Historic Volumen'), ('LIEG', 'LIEG'), ('LSEG', 'LSEG')], 'Type of norm', required=True)

    objeto = fields.Selection([('well', 'Well'),
                                ('block', 'Block'),
                                ('sector', 'Sector'),
                                ('underground_basin', 'Underground basin')],
                               string='Object to import', required=True,
                               help='Object type to which it will care rain values')


    def _importar_probabilidad_lluvia(self, objeto, wb):
        if objeto == 'well':
            obj = self.env['df.pozo']
            probabilidad_obj = self.env['df.probabilidad.pozo']
            tabla_agrupamiento = 'df_probabilidad_pozo'
        elif objeto == 'block':
            obj = self.env['df.bloque']
            probabilidad_obj = self.env['df.probabilidad.bloque']
            tabla_agrupamiento = 'df_probabilidad_bloque'
        elif objeto == 'sector':
            obj = self.env['df.sector.hidrologico']
            probabilidad_obj = self.env['df.probabilidad.sector']
            tabla_agrupamiento = 'df_probabilidad_sector'
        elif objeto == 'underground_basin':
            obj = self.env['df.cuenca.subterranea']
            probabilidad_obj = self.env['df.probabilidad.cuenca']
            tabla_agrupamiento = 'df_probabilidad_cuenca'
        numero_hojas = wb.nsheets
        for nro_hoja in range(numero_hojas):
            pestanna = wb.sheet_by_index(nro_hoja)
            identificador_pozo = pestanna.name
            numero_filas = pestanna.nrows
            identificador_objeto = tools.ustr(identificador_pozo)
            if objeto == 'underground_basin':
                objeto_ids = obj.search([('codigo','=',identificador_objeto)])
            else:
                objeto_ids = obj.search([('sigla','=',identificador_objeto)])
            if objeto_ids:
                for nro_fila in range(2,numero_filas):
                    cont=0
                    if pestanna.cell_type(rowx=nro_fila, colx=0) == 2:  # verifico si la fila es la de un anno con datos
                       pestanna.cell_value(rowx=nro_fila, colx=0)
                       vals = {}
                       if objeto == 'well':
                            vals['pozo_id'] = objeto_ids[0].id
                       elif objeto == 'block':
                            vals['bloque_id'] = objeto_ids[0].id
                       elif objeto == 'sector':
                            vals['sector_id'] = objeto_ids[0].id
                       elif objeto == 'underground_basin':
                            vals['cuenca_id'] = objeto_ids[0].id
                       if str(pestanna.cell_value(rowx=nro_fila, colx=0))=='0.5':
                           vals['probabilidad']='50%'
                       elif str(pestanna.cell_value(rowx=nro_fila, colx=0))=='0.75':
                           vals['probabilidad']='75%'
                       elif str(pestanna.cell_value(rowx=nro_fila, colx=0))=='0.95':
                           vals['probabilidad']='95%'
                       vals['anno'] = int(pestanna.cell_value(rowx=1, colx=0))
                       vals['media_hiperanual_enero'] = str(pestanna.cell_value(rowx=nro_fila, colx=1))
                       vals['media_hiperanual_febrero'] = str(pestanna.cell_value(rowx=nro_fila, colx=2))
                       vals['media_hiperanual_marzo'] = str(pestanna.cell_value(rowx=nro_fila, colx=3))
                       vals['media_hiperanual_abril'] = str(pestanna.cell_value(rowx=nro_fila, colx=4))
                       vals['media_hiperanual_mayo'] = str(pestanna.cell_value(rowx=nro_fila, colx=5))
                       vals['media_hiperanual_junio'] = str(pestanna.cell_value(rowx=nro_fila, colx=6))
                       vals['media_hiperanual_julio'] = str(pestanna.cell_value(rowx=nro_fila, colx=7))
                       vals['media_hiperanual_agosto'] = str(pestanna.cell_value(rowx=nro_fila, colx=8))
                       vals['media_hiperanual_septiembre'] = str(pestanna.cell_value(rowx=nro_fila, colx=9))
                       vals['media_hiperanual_octubre'] = str(pestanna.cell_value(rowx=nro_fila, colx=10))
                       vals['media_hiperanual_noviembre'] = str(pestanna.cell_value(rowx=nro_fila, colx=11))
                       vals['media_hiperanual_diciembre'] = str(pestanna.cell_value(rowx=nro_fila, colx=12))
                       if objeto == 'well':
                          string_objeto_id = 'pozo_id'
                       elif objeto == 'block':
                          string_objeto_id = 'bloque_id'
                       elif objeto == 'sector':
                          string_objeto_id = 'sector_id'
                       elif objeto == 'underground_basin':
                          string_objeto_id = 'cuenca_id'
                       probabilidad_lluvia_ids = probabilidad_obj.search([(string_objeto_id,'=',vals[string_objeto_id]),('probabilidad','=',vals['probabilidad']),('anno','=',vals['anno'])])
                       if probabilidad_lluvia_ids:
                          # context['actualizar_historicos'] = True
                          probabilidad_lluvia_ids.write(vals)
                       else:
                           # sql = """ select *
                           # from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                           # where tabla_objeto.sector_id = '""" + str(vals[string_objeto_id]) + """';"""
                           # cr.execute(sql)
                           # datos_vistas = cr.dictfetchall()
                           # if datos_vistas:
                           #
                           #   probabilidad_obj.unlink(cr, uid, datos_vistas[cont]['id'])
                           #   cont+1

                           probabilidad_obj.create(vals)


    def importar(self):
        cuenca_obj = self.env['df.cuenca.subterranea']
        sector_obj = self.env['df.sector.hidrologico']
        bloque_obj = self.env['df.bloque']
        pozo_obj = self.env['df.pozo']

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
            self._importar_probabilidad_lluvia(data['objeto'], wb)
        else:
            raise UserError(_('Seleccione un fichero excel!'))
        return {'type': 'ir.actions.act_window_close'}

        # if self.context is None:
        #     context = {}
        #
        # this = self.browse(self.env.uid, self.ids[0])
        # if not this.direct_path:
        #     if this.excel:
        #         #################### GUARDANDO EXCEL EN RUTA TEMPORAL #######################################
        #         excel = this.excel
        #         path = os.path.join(modules.module.get_module_path('df_hc_acuifero'), 'tmp',
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
        # self._importar_probabilidad_lluvia(self.env.uid, this.objeto, wb)
        # return {'type': 'ir.actions.act_window_close'}
        #except:
        #    raise osv.except_osv(_('Error: '), _('In the import process some error was encountered, please make sure the excel format is correct. If error persist contact to admin!'))


# df_importar_probabilidad_lluvia()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

