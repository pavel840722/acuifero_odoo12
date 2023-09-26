# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class df_nivel_anual_pozo(models.Model):
    _name = 'df.nivel.anual.pozo'
    _rec_name = 'pozo_id'
    _inherit = 'df.norma.anual'



    _description = "HC Annual level of wells"

    anno = fields.Integer(string='Año', required=True)
    pozo_id = fields.Many2one('df.pozo', string='Pozo', required=True)

    _sql_constraints = [
        ('anno_uniq', 'unique(id,anno)', 'The year already exists for that object!'),
    ]

    def buscar_ids(self,ids):
        tabla_agrupamiento = 'df_nivel_anual_pozo'
        sql = """ select pozo_id AS ids
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                           where tabla_objeto.id = '""" + str(ids) + """';"""
        self._cr.execute(sql)
        datos_vistas = self._cr.dictfetchall()
        ids = datos_vistas[0]['ids']
        return [ids]

    @api.model
    def create(self, vals):
        if (vals.get('media_hiperanual_enero_string') and vals['media_hiperanual_enero_string'] != False and vals[
            'media_hiperanual_enero_string'] != '' and vals['media_hiperanual_enero_string'] != ' '):
            vals['media_hiperanual_enero'] = float(vals['media_hiperanual_enero_string'])
        else:
            vals['media_hiperanual_enero_string'] = ''
            vals['media_hiperanual_enero'] = -999999.110

        if (vals.get('media_hiperanual_febrero_string') and vals['media_hiperanual_febrero_string'] != False and vals[
            'media_hiperanual_febrero_string'] != '' and vals['media_hiperanual_febrero_string'] != ' '):
            vals['media_hiperanual_febrero'] = float(vals['media_hiperanual_febrero_string'])
        else:
            vals['media_hiperanual_febrero_string'] = ''
            vals['media_hiperanual_febrero'] = -999999.110

        if (vals.get('media_hiperanual_marzo_string') and vals['media_hiperanual_marzo_string'] != False and vals[
            'media_hiperanual_marzo_string'] != '' and vals['media_hiperanual_marzo_string'] != ' '):
            vals['media_hiperanual_marzo'] = float(vals['media_hiperanual_marzo_string'])
        else:
            vals['media_hiperanual_marzo_string'] = ''
            vals['media_hiperanual_marzo'] = -999999.110

        if (vals.get('media_hiperanual_abril_string') and vals['media_hiperanual_abril_string'] != False and vals[
            'media_hiperanual_abril_string'] != '' and vals['media_hiperanual_abril_string'] != ' '):
            vals['media_hiperanual_abril'] = float(vals['media_hiperanual_abril_string'])
        else:
            vals['media_hiperanual_abril_string'] = ''
            vals['media_hiperanual_abril'] = -999999.110

        if (vals.get('media_hiperanual_mayo_string') and vals['media_hiperanual_mayo_string'] != False and vals[
            'media_hiperanual_mayo_string'] != '' and vals['media_hiperanual_mayo_string'] != ' '):
            vals['media_hiperanual_mayo'] = float(vals['media_hiperanual_mayo_string'])
        else:
            vals['media_hiperanual_mayo_string'] = ''
            vals['media_hiperanual_mayo'] = -999999.110

        if (vals.get('media_hiperanual_junio_string') and vals['media_hiperanual_junio_string'] != False and vals[
            'media_hiperanual_junio_string'] != '' and vals['media_hiperanual_junio_string'] != ' '):
            vals['media_hiperanual_junio'] = float(vals['media_hiperanual_junio_string'])
        else:
            vals['media_hiperanual_junio_string'] = ''
            vals['media_hiperanual_junio'] = -999999.110

        if (vals.get('media_hiperanual_julio_string') and vals['media_hiperanual_julio_string'] != False and vals[
            'media_hiperanual_julio_string'] != '' and vals['media_hiperanual_julio_string'] != ' '):
            vals['media_hiperanual_julio'] = float(vals['media_hiperanual_julio_string'])
        else:
            vals['media_hiperanual_julio_string'] = ''
            vals['media_hiperanual_julio'] = -999999.110

        if (vals.get('media_hiperanual_agosto_string') and vals['media_hiperanual_agosto_string'] != False and vals[
            'media_hiperanual_agosto_string'] != '' and vals['media_hiperanual_agosto_string'] != ' '):
            vals['media_hiperanual_agosto'] = float(vals['media_hiperanual_agosto_string'])
        else:
            vals['media_hiperanual_agosto_string'] = ''
            vals['media_hiperanual_agosto'] = -999999.110

        if (vals.get('media_hiperanual_septiembre_string') and vals['media_hiperanual_septiembre_string'] != False and
                vals['media_hiperanual_septiembre_string'] != '' and vals['media_hiperanual_septiembre_string'] != ' '):
            vals['media_hiperanual_septiembre'] = float(vals['media_hiperanual_septiembre_string'])
        else:
            vals['media_hiperanual_septiembre_string'] = ''
            vals['media_hiperanual_septiembre'] = -999999.110

        if (vals.get('media_hiperanual_octubre_string') and vals['media_hiperanual_octubre_string'] != False and vals[
            'media_hiperanual_octubre_string'] != '' and vals['media_hiperanual_octubre_string'] != ' '):
            vals['media_hiperanual_octubre'] = float(vals['media_hiperanual_octubre_string'])
        else:
            vals['media_hiperanual_octubre_string'] = ''
            vals['media_hiperanual_octubre'] = -999999.110

        if (vals.get('media_hiperanual_noviembre_string') and vals['media_hiperanual_noviembre_string'] != False and
                vals['media_hiperanual_noviembre_string'] != '' and vals['media_hiperanual_noviembre_string'] != ' '):
            vals['media_hiperanual_noviembre'] = float(vals['media_hiperanual_noviembre_string'])
        else:
            vals['media_hiperanual_noviembre_string'] = ''
            vals['media_hiperanual_noviembre'] = -999999.110

        if (vals.get('media_hiperanual_diciembre_string') and vals['media_hiperanual_diciembre_string'] != False and
                vals['media_hiperanual_diciembre_string'] != '' and vals['media_hiperanual_diciembre_string'] != ' '):
            vals['media_hiperanual_diciembre'] = float(vals['media_hiperanual_diciembre_string'])
        else:
            vals['media_hiperanual_diciembre_string'] = ''
            vals['media_hiperanual_diciembre'] = -999999.110
        vals['active'] = True
        if (vals.get('anno')):
            fecha_actual = datetime.now()
            if vals['anno'] <= fecha_actual.year:
                return super(df_nivel_anual_pozo, self).create(vals)
            else:
                raise ValidationError('El año debe de ser menor o igual que el año actual')
        else:
             raise ValidationError('Valor incorrecto para el campo año')

    def write(self, vals):
        cuenca_obj = self.env['df.cuenca.subterranea']
        sector_obj = self.env['df.sector.hidrologico']
        bloque_obj = self.env['df.bloque']
        pozo_obj = self.env['df.pozo']
        if vals.get('media_hiperanual_enero_string'):
            if (vals['media_hiperanual_enero_string']) != False and vals['media_hiperanual_enero_string'] != '' and \
                    vals['media_hiperanual_enero_string'] != ' ':
                vals['media_hiperanual_enero'] = float(vals['media_hiperanual_enero_string'])
            if (vals['media_hiperanual_enero_string']) == False:
                vals['media_hiperanual_enero'] = -999999.110

        if vals.get('media_hiperanual_febrero_string'):
            if (vals['media_hiperanual_febrero_string']) != False and vals['media_hiperanual_febrero_string'] != '' and \
                    vals['media_hiperanual_febrero_string'] != ' ':
                vals['media_hiperanual_febrero'] = float(vals['media_hiperanual_febrero_string'])
            if (vals['media_hiperanual_febrero_string']) == False:
                vals['media_hiperanual_febrero'] = -999999.110

        if vals.get('media_hiperanual_marzo_string'):
            if (vals['media_hiperanual_marzo_string']) != False and vals['media_hiperanual_marzo_string'] != '' and \
                    vals['media_hiperanual_marzo_string'] != ' ':
                vals['media_hiperanual_marzo'] = float(vals['media_hiperanual_marzo_string'])
            if (vals['media_hiperanual_marzo_string']) == False:
                vals['media_hiperanual_marzo'] = -999999.110

        if vals.get('media_hiperanual_abril_string'):
            if (vals['media_hiperanual_abril_string']) != False and vals['media_hiperanual_abril_string'] != '' and \
                    vals['media_hiperanual_abril_string'] != ' ':
                vals['media_hiperanual_abril'] = float(vals['media_hiperanual_abril_string'])
            if (vals['media_hiperanual_abril_string']) == False:
                vals['media_hiperanual_abril'] = -999999.110

        if vals.get('media_hiperanual_mayo_string'):
            if (vals['media_hiperanual_mayo_string']) != False and vals['media_hiperanual_mayo_string'] != '' and vals[
                'media_hiperanual_mayo_string'] != ' ':
                vals['media_hiperanual_mayo'] = float(vals['media_hiperanual_mayo_string'])
            if (vals['media_hiperanual_mayo_string']) == False:
                vals['media_hiperanual_mayo'] = -999999.110

        if vals.get('media_hiperanual_junio_string'):
            if (vals['media_hiperanual_junio_string']) != False and vals['media_hiperanual_junio_string'] != '' and \
                    vals['media_hiperanual_junio_string'] != ' ':
                vals['media_hiperanual_junio'] = float(vals['media_hiperanual_junio_string'])
            if (vals['media_hiperanual_junio_string']) == False:
                vals['media_hiperanual_junio'] = -999999.110

        if vals.get('media_hiperanual_julio_string'):
            if (vals['media_hiperanual_julio_string']) != False and vals['media_hiperanual_julio_string'] != '' and \
                    vals['media_hiperanual_julio_string'] != ' ':
                vals['media_hiperanual_julio'] = float(vals['media_hiperanual_julio_string'])
            if (vals['media_hiperanual_julio_string']) == False:
                vals['media_hiperanual_julio'] = -999999.110

        if vals.get('media_hiperanual_agosto_string'):
            if (vals['media_hiperanual_agosto_string']) != False and vals['media_hiperanual_agosto_string'] != '' and \
                    vals['media_hiperanual_agosto_string'] != ' ':
                vals['media_hiperanual_agosto'] = float(vals['media_hiperanual_agosto_string'])
            if (vals['media_hiperanual_agosto_string']) == False:
                vals['media_hiperanual_agosto'] = -999999.110

        if vals.get('media_hiperanual_septiembre_string'):
            if (vals['media_hiperanual_septiembre_string']) != False and vals[
                'media_hiperanual_septiembre_string'] != '' and vals['media_hiperanual_septiembre_string'] != ' ':
                vals['media_hiperanual_septiembre'] = float(vals['media_hiperanual_septiembre_string'])
            if (vals['media_hiperanual_septiembre_string']) == False:
                vals['media_hiperanual_septiembre'] = -999999.110

        if vals.get('media_hiperanual_octubre_string'):
            if (vals['media_hiperanual_octubre_string']) != False and vals['media_hiperanual_octubre_string'] != '' and \
                    vals['media_hiperanual_octubre_string'] != ' ':
                vals['media_hiperanual_octubre'] = float(vals['media_hiperanual_octubre_string'])
            if (vals['media_hiperanual_octubre_string']) == False:
                vals['media_hiperanual_octubre'] = -999999.110

        if vals.get('media_hiperanual_noviembre_string'):
            if (vals['media_hiperanual_noviembre_string']) != False and vals[
                'media_hiperanual_noviembre_string'] != '' and vals['media_hiperanual_noviembre_string'] != ' ':
                vals['media_hiperanual_noviembre'] = float(vals['media_hiperanual_noviembre_string'])
            if (vals['media_hiperanual_noviembre_string']) == False:
                vals['media_hiperanual_noviembre'] = -999999.110

        if vals.get('media_hiperanual_diciembre_string'):
            if (vals['media_hiperanual_diciembre_string']) != False and vals[
                'media_hiperanual_diciembre_string'] != '' and vals['media_hiperanual_diciembre_string'] != ' ':
                vals['media_hiperanual_diciembre'] = float(vals['media_hiperanual_diciembre_string'])
            if (vals['media_hiperanual_diciembre_string']) == False:
                vals['media_hiperanual_diciembre'] = -999999.110
        fecha_actual = datetime.now()
        if vals.get('anno') and vals['anno'] > fecha_actual.year:
            raise ValidationError(('Error !'), ('The year must be less than or equal to current year'))
        return super(df_nivel_anual_pozo, self).write(vals)




