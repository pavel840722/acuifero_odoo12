# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError
import base64
from odoo.modules import module
from odoo import tools
from xlrd import open_workbook
import os
import fnmatch


class df_importar_pozos(models.TransientModel):
    _name = 'df.importar.pozos'
    _description = 'Wizard to import wells'

    # def _list_files(self):
    #     # returns a list of names (with extension, without full path) of all files
    #     # in folder path
    #
    #     shared_directory_obj = self.env['df.directorio.compartido']
    #     active_dir_id = shared_directory_obj.search(self.env.uid, [('is_active', '=', True)])
    #     files = []
    #     if active_dir_id:
    #         active_dir = shared_directory_obj.browse(self.env.uid, active_dir_id[0])
    #         path = active_dir.path
    #         for name in os.listdir(path):
    #             if os.path.isfile(os.path.join(path, name)):
    #                 if fnmatch.fnmatch(name, '*.xls') or fnmatch.fnmatch(name, '*.xlsx'):
    #                     files.append((name, name))
    #     return files

    excel = fields.Binary('Excel file (recommended format: xlsx) to import')
    # direct_path = fields.Boolean('Having errors?',
    #     help='Check this field if you are having errors at the time of importing data by selection excel file')
    # filename = fields.Selection(_list_files, 'Filename', size=32,
    #                              help='This solution allows to select a file previously uploaded to the server')
    location = fields.Selection([('basin', 'Underground basin'),
                                  ('sector', 'Hydrogeological sector'),
                                  ('block', 'Block')],
                                 'Located in', required=True,
                                 help='All wells to be imported are going to be located in selected location')
    coordinate_system = fields.Selection([('north', 'North'),
                                           ('south', 'South')],
                                          'Coordinate system', required=True,
                        help='All wells to be imported are going to belong to selected coordinate system')
    representatives = fields.Boolean('All representatives',
                                     help='If checked all wells to be imported are representatives')


    def _importar_pozos(self, wb, location, coordinate_system, representatives):
        pozo_obj = self.env['df.pozo']
        location_obj = self.env['df.sector.hidrologico']
        llave = 'sector_hidrologico_id'
        if location == 'block':
            location_obj = self.env['df.bloque']
            llave = 'bloque_id'
        elif location == 'basin':
            location_obj = self.env['df.cuenca.subterranea']
            llave = 'cuenca_subterranea_id'

        numero_hojas = wb.nsheets
        for nro_hoja in range(numero_hojas):
            pestanna = wb.sheet_by_index(nro_hoja)
            numero_filas = pestanna.nrows
            for nro_fila in range(1,numero_filas):
                if location != 'basin':
                    found_location = location_obj.search([('sigla','=',pestanna.cell_value(rowx=nro_fila, colx=2))])
                else:
                    found_location = location_obj.search([('codigo','=',pestanna.cell_value(rowx=nro_fila, colx=2))])
                pozo_ids = pozo_obj.search([('sigla','=',pestanna.cell_value(rowx=nro_fila, colx=1))])
                if found_location:
                    try:
                        if pestanna.cell_value(rowx=nro_fila, colx=6):
                            profundidad_total = float(pestanna.cell_value(rowx=nro_fila, colx=6))
                        else:
                            profundidad_total = None
                    except Exception:
                        raise ValidationError('Ha ocurrido un error durante la importación. Por favor chequee que sea numérico el valor del campo Profundidad en la fila %s!') % (nro_fila + 1)
                    try:
                        if pestanna.cell_value(rowx=nro_fila, colx=7):

                            cota_topografica = float(pestanna.cell_value(rowx=nro_fila, colx=7))
                        else:
                            cota_topografica = None
                    except Exception:

                        raise ValidationError('Ha ocurrido un error durante la importación. Por favor chequee que sea numérico el valor del campo Cota topográfica en la fila %s!') % (nro_fila + 1)
                    try:
                        if pestanna.cell_value(rowx=nro_fila, colx=5):
                            diametro = float(pestanna.cell_value(rowx=nro_fila, colx=5))
                        else:
                            diametro = None
                    except Exception:
                        raise ValidationError('Ha ocurrido un error durante la importación. Por favor chequee que sea numérico el valor del campo Diámetro en la fila %s!') % (nro_fila + 1)
                    try:
                        if pestanna.cell_value(rowx=nro_fila, colx=3):
                            coord_norte = float(pestanna.cell_value(rowx=nro_fila, colx=3))
                        else:
                            coord_norte = None
                    except Exception:
                        raise ValidationError('Ha ocurrido un error durante la importación. Por favor chequee que sea numérico el valor del campo Cooordenadas norte en la fila %s!') % (nro_fila + 1)
                    try:
                        if pestanna.cell_value(rowx=nro_fila, colx=4):
                            coord_este = float(pestanna.cell_value(rowx=nro_fila, colx=4))
                        else:
                            coord_este = None
                    except Exception:
                        raise ValidationError('Ha ocurrido un error durante la importación. Por favor chequee que sea numérico el valor del campo Cooordenadas este en la fila %s!') % (nro_fila + 1)

                    tipo= pestanna.cell_value(rowx=nro_fila, colx=1)
                    if isinstance(tipo, (int, float, complex) ):
                        sigla=int(tipo)
                    else:
                        sigla=tipo
                    if str(pestanna.cell_value(rowx=nro_fila, colx=8))=='x':
                        mensual = True
                    else:
                        mensual = False
                    if str(pestanna.cell_value(rowx=nro_fila, colx=9))=='x':
                        trimestral = True
                    else:
                        trimestral = False
                    if str(pestanna.cell_value(rowx=nro_fila, colx=10))=='x':
                        semestral = True
                    else:
                        semestral = False
                    if str(pestanna.cell_value(rowx=nro_fila, colx=11))=='x':
                        batometrico = True
                    else:
                        batometrico = False
                    vals = {'nombre': pestanna.cell_value(rowx=nro_fila, colx=0),
                            'sigla': sigla, 'ubicado': location,
                            llave: found_location[0].id, 'coordenadas': coordinate_system,
                            'profundidad_total': profundidad_total,
                            'cota_topografica': cota_topografica,
                            'representativo': representatives, 'diametro': diametro,
                            'mensual': mensual,
                            'trimestral':trimestral,
                            'semestral': semestral,
                            'batometrico': batometrico
                            }
                    if coordinate_system == 'north':
                        vals['norte'] = coord_norte
                        vals['este'] = coord_este
                    else:
                        vals['norte1'] = coord_norte
                        vals['este1'] = coord_este
                    # vals['altura'] = pestanna.cell_value(rowx=nro_fila, colx=6)
                    try:
                        if pozo_ids:
                            pozo_ids.write(vals)
                        else:
                            pozo_obj.create(vals)
                    except Exception:
                        raise ValidationError('Ha ocurrido un error durante la importación. Por favor chequee la información del excel!')


    def importar(self, ids):
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
            self._importar_pozos(wb, data['location'], data['coordinate_system'], data['representatives'])
        else:
            raise UserError(_('Seleccione un fichero excel!'))
        return {'type': 'ir.actions.act_window_close'}

        # if self.context is None:
        #     context = {}
        #
        # this = self.browse(self.env.uid, ids[0])
        # if not this.direct_path:
        #     if this.excel:
        #         #################### GUARDANDO EXCEL EN RUTA TEMPORAL #######################################
        #         path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp', 'cc.xlsx')
        #         fileobj = open(path, "wb")
        #         fileobj.write(base64.b64decode(this.excel))
        #         fileobj.flush()
        #         fileobj.close()
        #         #################### TRABAJO CON EXCEL PARA IMPORTAR ########################################
        #     else:
        #         raise osv.except_osv(_('Error: '), _('You must select an excel file!'))
        #
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
        # self._importar_pozos(self.env.uid, wb, this.location, this.coordinate_system, this.representatives)
        #
        # return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
