# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _
#from datetime import datetime
from time import time
from dateutil.relativedelta import relativedelta

import time, datetime


# from openerp.osv import osv, fields
# from tools.translate import _


class df_plan_explotacion_anual_pozo(models.Model):
    _name = 'df.plan.explotacion.anual.pozo'
    _rec_name = 'pozo_id'
    _inherit = 'df.norma.anual'
    _description = "HC Annual exploitation plan of wells"

    anno = fields.Integer(string='Year', required=True)
    pozo_id = fields.Many2one('df.pozo', string='Abbreviation', required=True, ondelete='cascade')
    cuenca_id = fields.Many2one('df.cuenca.subterranea', related='pozo_id.cuenca_subterranea_id', readonly=True,
                                string='Underground basin')
    sector_id = fields.Many2one('df.sector.hidrologico', related='pozo_id.sector_hidrologico_id', readonly=True,
                                string='Hydrogeological sector')
    bloque_id = fields.Many2one('df.bloque', related='pozo_id.bloque_id', readonly=True, string='Block')

    _sql_constraints = [
        ('anno_uniq', 'unique(pozo_id,anno)', u'El año ya existe para ese pozo!'),
    ]

    _order = 'anno desc'

    @api.constrains('anno')
    def check_anno(self):
        fecha_actual = datetime.datetime.now()
        for rec in self:
            if rec.anno > fecha_actual.year:
                raise UserError(_('The year must be less than the current year.'))

    @api.model
    def create(self, vals):
        if (vals.get('media_hiperanual_enero_string', None) and vals['media_hiperanual_enero_string'] != False and vals[
            'media_hiperanual_enero_string'] != ''):
            vals['media_hiperanual_enero'] = float(vals['media_hiperanual_enero_string'])
        else:
            vals['media_hiperanual_enero_string'] = ''
            vals['media_hiperanual_enero'] = -999999.110

        if (vals.get('media_hiperanual_febrero_string', None) and vals['media_hiperanual_febrero_string'] != False and
                    vals['media_hiperanual_febrero_string'] != ''):
            vals['media_hiperanual_febrero'] = float(vals['media_hiperanual_febrero_string'])
        else:
            vals['media_hiperanual_febrero_string'] = ''
            vals['media_hiperanual_febrero'] = -999999.110

        if (vals.get('media_hiperanual_marzo_string', None) and vals['media_hiperanual_marzo_string'] != False and vals[
            'media_hiperanual_marzo_string'] != ''):
            vals['media_hiperanual_marzo'] = float(vals['media_hiperanual_marzo_string'])
        else:
            vals['media_hiperanual_marzo_string'] = ''
            vals['media_hiperanual_marzo'] = -999999.110

        if (vals.get('media_hiperanual_abril_string', None) and vals['media_hiperanual_abril_string'] != False and vals[
            'media_hiperanual_abril_string'] != ''):
            vals['media_hiperanual_abril'] = float(vals['media_hiperanual_abril_string'])
        else:
            vals['media_hiperanual_abril_string'] = ''
            vals['media_hiperanual_abril'] = -999999.110

        if (vals.get('media_hiperanual_mayo_string', None) and vals['media_hiperanual_mayo_string'] != False and vals[
            'media_hiperanual_mayo_string'] != ''):
            vals['media_hiperanual_mayo'] = float(vals['media_hiperanual_mayo_string'])
        else:
            vals['media_hiperanual_mayo_string'] = ''
            vals['media_hiperanual_mayo'] = -999999.110

        if (vals.get('media_hiperanual_junio_string', None) and vals['media_hiperanual_junio_string'] != False and vals[
            'media_hiperanual_junio_string'] != ''):
            vals['media_hiperanual_junio'] = float(vals['media_hiperanual_junio_string'])
        else:
            vals['media_hiperanual_junio_string'] = ''
            vals['media_hiperanual_junio'] = -999999.110

        if (vals.get('media_hiperanual_julio_string', None) and vals['media_hiperanual_julio_string'] != False and vals[
            'media_hiperanual_julio_string'] != ''):
            vals['media_hiperanual_julio'] = float(vals['media_hiperanual_julio_string'])
        else:
            vals['media_hiperanual_julio_string'] = ''
            vals['media_hiperanual_julio'] = -999999.110

        if (vals.get('media_hiperanual_agosto_string', None) and vals['media_hiperanual_agosto_string'] != False and
                    vals[
                        'media_hiperanual_agosto_string'] != ''):
            vals['media_hiperanual_agosto'] = float(vals['media_hiperanual_agosto_string'])
        else:
            vals['media_hiperanual_agosto_string'] = ''
            vals['media_hiperanual_agosto'] = -999999.110

        if (vals.get('media_hiperanual_septiembre_string', None) and vals[
            'media_hiperanual_septiembre_string'] != False and vals['media_hiperanual_septiembre_string'] != ''):
            vals['media_hiperanual_septiembre'] = float(vals['media_hiperanual_septiembre_string'])
        else:
            vals['media_hiperanual_septiembre_string'] = ''
            vals['media_hiperanual_septiembre'] = -999999.110

        if (vals.get('media_hiperanual_octubre_string', None) and vals['media_hiperanual_octubre_string'] != False and
                    vals['media_hiperanual_octubre_string'] != ''):
            vals['media_hiperanual_octubre'] = float(vals['media_hiperanual_octubre_string'])
        else:
            vals['media_hiperanual_octubre_string'] = ''
            vals['media_hiperanual_octubre'] = -999999.110

        if (vals.get('media_hiperanual_noviembre_string', None) and vals[
            'media_hiperanual_noviembre_string'] != False and
                    vals['media_hiperanual_noviembre_string'] != ''):
            vals['media_hiperanual_noviembre'] = float(vals['media_hiperanual_noviembre_string'])
        else:
            vals['media_hiperanual_noviembre_string'] = ''
            vals['media_hiperanual_noviembre'] = -999999.110

        if (vals.get('media_hiperanual_diciembre_string', None) and vals[
            'media_hiperanual_diciembre_string'] != False and
                    vals['media_hiperanual_diciembre_string'] != ''):
            vals['media_hiperanual_diciembre'] = float(vals['media_hiperanual_diciembre_string'])
        else:
            vals['media_hiperanual_diciembre_string'] = ''
            vals['media_hiperanual_diciembre'] = -999999.110
        if (vals.get('anno', None)):
            vals['anno_final'] = vals['anno']
        fecha_actual = datetime.datetime.now()
        vals['active'] = True
        if vals['anno'] <= fecha_actual.year + 2:
            return super(df_plan_explotacion_anual_pozo, self).create(vals)
        else:
            raise ValidationError(_('Error !'),
                                  _('Solo se puede insertar la explotación que exceda en dos año,al año actual.'))

    @api.multi
    def write(self, vals):
        if vals.get('media_hiperanual_enero_string', None):
            if (vals['media_hiperanual_enero_string']) != False and vals['media_hiperanual_enero_string'] != '':
                vals['media_hiperanual_enero'] = float(vals['media_hiperanual_enero_string'])
            if (vals['media_hiperanual_enero_string']) == False or (str(vals['media_hiperanual_enero_string'])) == '':
                vals['media_hiperanual_enero'] = -999999.110

        if vals.get('media_hiperanual_febrero_string', None):
            if (vals['media_hiperanual_febrero_string']) != False and vals['media_hiperanual_febrero_string'] != '':
                vals['media_hiperanual_febrero'] = float(vals['media_hiperanual_febrero_string'])
            if (vals['media_hiperanual_febrero_string']) == False or (
                    str(vals['media_hiperanual_febrero_string'])) == '':
                vals['media_hiperanual_febrero'] = -999999.110

        if vals.get('media_hiperanual_marzo_string', None):
            if (vals['media_hiperanual_marzo_string']) != False and vals['media_hiperanual_marzo_string'] != '':
                vals['media_hiperanual_marzo'] = float(vals['media_hiperanual_marzo_string'])
            if (vals['media_hiperanual_marzo_string']) == False or (str(vals['media_hiperanual_marzo_string'])) == '':
                vals['media_hiperanual_marzo'] = -999999.110

        if vals.get('media_hiperanual_abril_string', None):
            if (vals['media_hiperanual_abril_string']) != False and vals['media_hiperanual_abril_string'] != '':
                vals['media_hiperanual_abril'] = float(vals['media_hiperanual_abril_string'])
            if (vals['media_hiperanual_abril_string']) == False or (str(vals['media_hiperanual_abril_string'])) == '':
                vals['media_hiperanual_abril'] = -999999.110

        if vals.get('media_hiperanual_mayo_string', None):
            if (vals['media_hiperanual_mayo_string']) != False and vals['media_hiperanual_mayo_string'] != '':
                vals['media_hiperanual_mayo'] = float(vals['media_hiperanual_mayo_string'])
            if (vals['media_hiperanual_mayo_string']) == False or (str(vals['media_hiperanual_mayo_string'])) == '':
                vals['media_hiperanual_mayo'] = -999999.110

        if vals.get('media_hiperanual_junio_string', None):
            if (vals['media_hiperanual_junio_string']) != False and vals['media_hiperanual_junio_string'] != '':
                vals['media_hiperanual_junio'] = float(vals['media_hiperanual_junio_string'])
            if (vals['media_hiperanual_junio_string']) == False or (str(vals['media_hiperanual_junio_string'])) == '':
                vals['media_hiperanual_junio'] = -999999.110

        if vals.get('media_hiperanual_julio_string', None):
            if (vals['media_hiperanual_julio_string']) != False and vals['media_hiperanual_julio_string'] != '':
                vals['media_hiperanual_julio'] = float(vals['media_hiperanual_julio_string'])
            if (vals['media_hiperanual_julio_string']) == False or (str(vals['media_hiperanual_julio_string'])) == '':
                vals['media_hiperanual_julio'] = -999999.110

        if vals.get('media_hiperanual_agosto_string', None):
            if (vals['media_hiperanual_agosto_string']) != False and vals['media_hiperanual_agosto_string'] != '':
                vals['media_hiperanual_agosto'] = float(vals['media_hiperanual_agosto_string'])
            if (vals['media_hiperanual_agosto_string']) == False or (str(vals['media_hiperanual_agosto_string'])) == '':
                vals['media_hiperanual_agosto'] = -999999.110

        if vals.get('media_hiperanual_septiembre_string', None):
            if (vals['media_hiperanual_septiembre_string']) != False and vals[
                'media_hiperanual_septiembre_string'] != '':
                vals['media_hiperanual_septiembre'] = float(vals['media_hiperanual_septiembre_string'])
            if (vals['media_hiperanual_septiembre_string']) == False or (
                    str(vals['media_hiperanual_septiembre_string'])) == '':
                vals['media_hiperanual_septiembre'] = -999999.110

        if vals.get('media_hiperanual_octubre_string', None):
            if (vals['media_hiperanual_octubre_string']) != False and vals['media_hiperanual_octubre_string'] != '':
                vals['media_hiperanual_octubre'] = float(vals['media_hiperanual_octubre_string'])
            if (vals['media_hiperanual_octubre_string']) == False or (
                    str(vals['media_hiperanual_octubre_string'])) == '':
                vals['media_hiperanual_octubre'] = -999999.110

        if vals.get('media_hiperanual_noviembre_string', None):
            if (vals['media_hiperanual_noviembre_string']) != False and vals['media_hiperanual_noviembre_string'] != '':
                vals['media_hiperanual_noviembre'] = float(vals['media_hiperanual_noviembre_string'])
            if (vals['media_hiperanual_noviembre_string']) == False or (
                    str(vals['media_hiperanual_noviembre_string'])) == '':
                vals['media_hiperanual_noviembre'] = -999999.110

        if vals.get('media_hiperanual_diciembre_string', None):
            if (vals['media_hiperanual_diciembre_string']) != False and vals['media_hiperanual_diciembre_string'] != '':
                vals['media_hiperanual_diciembre'] = float(vals['media_hiperanual_diciembre_string'])
            if (vals['media_hiperanual_diciembre_string']) == False or (
                    str(vals['media_hiperanual_diciembre_string'])) == '':
                vals['media_hiperanual_diciembre'] = -999999.110
        fecha_actual = datetime.datetime.now()
        if vals.get('anno', None):
            if vals['anno'] <= fecha_actual.year + 2:
                return super(df_plan_explotacion_anual_pozo, self).write(vals)
            else:
                raise ValidationError(_('Error !'),
                                      _('Solo se puede insertar la explotación que exceda en dos año,al año actual.'))
        return super(df_plan_explotacion_anual_pozo, self).write(vals)

        # def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        #     if context is None:
        #         context = {}
        #     for arg in args:
        #         arg[2]='2009'
        #         # self._update_args_or_domain(args)
        #     return super(df_nivel_anual_pozo, self).search(cr, uid, args, offset, limit, order, context=context, count=count)


class df_explotacion_anual_pozo(models.Model):
    _name = 'df.explotacion.anual.pozo'
    _inherit = 'df.norma.anual'
    _description = "HC Annual exploitation of wells"

    anno = fields.Integer(string='Year', required=True)
    pozo_id = fields.Many2one('df.pozo', string='Abbreviation', required=True, ondelete='cascade')
    cuenca_id = fields.Many2one('df.cuenca.subterranea', related='pozo_id.cuenca_subterranea_id', readonly=True,
                                string='Underground basin')
    sector_id = fields.Many2one('df.sector.hidrologico', related='pozo_id.sector_hidrologico_id', readonly=True,
                                string='Hydrogeological sector')
    bloque_id = fields.Many2one('df.bloque', related='pozo_id.bloque_id', readonly=True, string='Block')

    _sql_constraints = [
        ('anno_uniq', 'unique(pozo_id,anno)', u'El año ya existe para ese pozo!'),
    ]

    _order = 'anno desc'

    @api.model
    def create(self, vals):
        if (vals.get('media_hiperanual_enero_string', None) and vals['media_hiperanual_enero_string'] != False and vals[
            'media_hiperanual_enero_string'] != ''):
            vals['media_hiperanual_enero'] = float(vals['media_hiperanual_enero_string'])
        else:
            vals['media_hiperanual_enero_string'] = ''
            vals['media_hiperanual_enero'] = -999999.110

        if (vals.get('media_hiperanual_febrero_string', None) and vals['media_hiperanual_febrero_string'] != False and
                    vals['media_hiperanual_febrero_string'] != ''):
            vals['media_hiperanual_febrero'] = float(vals['media_hiperanual_febrero_string'])
        else:
            vals['media_hiperanual_febrero_string'] = ''
            vals['media_hiperanual_febrero'] = -999999.110

        if (vals.get('media_hiperanual_marzo_string', None) and vals['media_hiperanual_marzo_string'] != False and vals[
            'media_hiperanual_marzo_string'] != ''):
            vals['media_hiperanual_marzo'] = float(vals['media_hiperanual_marzo_string'])
        else:
            vals['media_hiperanual_marzo_string'] = ''
            vals['media_hiperanual_marzo'] = -999999.110

        if (vals.get('media_hiperanual_abril_string', None) and vals['media_hiperanual_abril_string'] != False and vals[
            'media_hiperanual_abril_string'] != ''):
            vals['media_hiperanual_abril'] = float(vals['media_hiperanual_abril_string'])
        else:
            vals['media_hiperanual_abril_string'] = ''
            vals['media_hiperanual_abril'] = -999999.110

        if (vals.get('media_hiperanual_mayo_string', None) and vals['media_hiperanual_mayo_string'] != False and vals[
            'media_hiperanual_mayo_string'] != ''):
            vals['media_hiperanual_mayo'] = float(vals['media_hiperanual_mayo_string'])
        else:
            vals['media_hiperanual_mayo_string'] = ''
            vals['media_hiperanual_mayo'] = -999999.110

        if (vals.get('media_hiperanual_junio_string', None) and vals['media_hiperanual_junio_string'] != False and vals[
            'media_hiperanual_junio_string'] != ''):
            vals['media_hiperanual_junio'] = float(vals['media_hiperanual_junio_string'])
        else:
            vals['media_hiperanual_junio_string'] = ''
            vals['media_hiperanual_junio'] = -999999.110

        if (vals.get('media_hiperanual_julio_string', None) and vals['media_hiperanual_julio_string'] != False and vals[
            'media_hiperanual_julio_string'] != ''):
            vals['media_hiperanual_julio'] = float(vals['media_hiperanual_julio_string'])
        else:
            vals['media_hiperanual_julio_string'] = ''
            vals['media_hiperanual_julio'] = -999999.110

        if (vals.get('media_hiperanual_agosto_string', None) and vals['media_hiperanual_agosto_string'] != False and
                    vals['media_hiperanual_agosto_string'] != ''):
            vals['media_hiperanual_agosto'] = float(vals['media_hiperanual_agosto_string'])
        else:
            vals['media_hiperanual_agosto_string'] = ''
            vals['media_hiperanual_agosto'] = -999999.110

        if (vals.get('media_hiperanual_septiembre_string', None) and vals[
            'media_hiperanual_septiembre_string'] != False and vals['media_hiperanual_septiembre_string'] != ''):
            vals['media_hiperanual_septiembre'] = float(vals['media_hiperanual_septiembre_string'])
        else:
            vals['media_hiperanual_septiembre_string'] = ''
            vals['media_hiperanual_septiembre'] = -999999.110

        if (vals.get('media_hiperanual_octubre_string', None) and vals['media_hiperanual_octubre_string'] != False and
                    vals['media_hiperanual_octubre_string'] != ''):
            vals['media_hiperanual_octubre'] = float(vals['media_hiperanual_octubre_string'])
        else:
            vals['media_hiperanual_octubre_string'] = ''
            vals['media_hiperanual_octubre'] = -999999.110

        if (vals.get('media_hiperanual_noviembre_string', None) and vals[
            'media_hiperanual_noviembre_string'] != False and vals['media_hiperanual_noviembre_string'] != ''):
            vals['media_hiperanual_noviembre'] = float(vals['media_hiperanual_noviembre_string'])
        else:
            vals['media_hiperanual_noviembre_string'] = ''
            vals['media_hiperanual_noviembre'] = -999999.110

        if (vals.get('media_hiperanual_diciembre_string', None) and vals[
            'media_hiperanual_diciembre_string'] != False and vals['media_hiperanual_diciembre_string'] != ''):
            vals['media_hiperanual_diciembre'] = float(vals['media_hiperanual_diciembre_string'])
        else:
            vals['media_hiperanual_diciembre_string'] = ''
            vals['media_hiperanual_diciembre'] = -999999.110
        if (vals.get('anno', None)):
            vals['anno_final'] = vals['anno']
        fecha_actual = datetime.datetime.now()
        vals['active'] = True
        if vals['anno'] <= fecha_actual.year + 1:
            return super(df_explotacion_anual_pozo, self).create(vals)
        else:
            raise ValidationError(_('Error !'),
                                  _('Solo se puede insertar la explotación que exceda en un año,al año actual.'))

    @api.multi
    def write(self, vals):
        if vals.get('media_hiperanual_enero_string', None):
            if (vals['media_hiperanual_enero_string']) != False and vals['media_hiperanual_enero_string'] != '':
                vals['media_hiperanual_enero'] = float(vals['media_hiperanual_enero_string'])
            if (vals['media_hiperanual_enero_string']) == False or (str(vals['media_hiperanual_enero_string'])) == '':
                vals['media_hiperanual_enero'] = -999999.110

        if vals.get('media_hiperanual_febrero_string', None):
            if (vals['media_hiperanual_febrero_string']) != False and vals['media_hiperanual_febrero_string'] != '':
                vals['media_hiperanual_febrero'] = float(vals['media_hiperanual_febrero_string'])
            if (vals['media_hiperanual_febrero_string']) == False or (
            str(vals['media_hiperanual_febrero_string'])) == '':
                vals['media_hiperanual_febrero'] = -999999.110

        if vals.get('media_hiperanual_marzo_string', None):
            if (vals['media_hiperanual_marzo_string']) != False and vals['media_hiperanual_marzo_string'] != '':
                vals['media_hiperanual_marzo'] = float(vals['media_hiperanual_marzo_string'])
            if (vals['media_hiperanual_marzo_string']) == False or (str(vals['media_hiperanual_marzo_string'])) == '':
                vals['media_hiperanual_marzo'] = -999999.110

        if vals.get('media_hiperanual_abril_string', None):
            if (vals['media_hiperanual_abril_string']) != False and vals['media_hiperanual_abril_string'] != '':
                vals['media_hiperanual_abril'] = float(vals['media_hiperanual_abril_string'])
            if (vals['media_hiperanual_abril_string']) == False or (str(vals['media_hiperanual_abril_string'])) == '':
                vals['media_hiperanual_abril'] = -999999.110

        if vals.get('media_hiperanual_mayo_string', None):
            if (vals['media_hiperanual_mayo_string']) != False and vals['media_hiperanual_mayo_string'] != '':
                vals['media_hiperanual_mayo'] = float(vals['media_hiperanual_mayo_string'])
            if (vals['media_hiperanual_mayo_string']) == False or (str(vals['media_hiperanual_mayo_string'])) == '':
                vals['media_hiperanual_mayo'] = -999999.110

        if vals.get('media_hiperanual_junio_string', None):
            if (vals['media_hiperanual_junio_string']) != False and vals['media_hiperanual_junio_string'] != '':
                vals['media_hiperanual_junio'] = float(vals['media_hiperanual_junio_string'])
            if (vals['media_hiperanual_junio_string']) == False or (str(vals['media_hiperanual_junio_string'])) == '':
                vals['media_hiperanual_junio'] = -999999.110

        if vals.get('media_hiperanual_julio_string', None):
            if (vals['media_hiperanual_julio_string']) != False and vals['media_hiperanual_julio_string'] != '':
                vals['media_hiperanual_julio'] = float(vals['media_hiperanual_julio_string'])
            if (vals['media_hiperanual_julio_string']) == False or (str(vals['media_hiperanual_julio_string'])) == '':
                vals['media_hiperanual_julio'] = -999999.110

        if vals.get('media_hiperanual_agosto_string', None):
            if (vals['media_hiperanual_agosto_string']) != False and vals['media_hiperanual_agosto_string'] != '':
                vals['media_hiperanual_agosto'] = float(vals['media_hiperanual_agosto_string'])
            if (vals['media_hiperanual_agosto_string']) == False or (str(vals['media_hiperanual_agosto_string'])) == '':
                vals['media_hiperanual_agosto'] = -999999.110

        if vals.get('media_hiperanual_septiembre_string', None):
            if (vals['media_hiperanual_septiembre_string']) != False and vals[
                'media_hiperanual_septiembre_string'] != '':
                vals['media_hiperanual_septiembre'] = float(vals['media_hiperanual_septiembre_string'])
            if (vals['media_hiperanual_septiembre_string']) == False or (
            str(vals['media_hiperanual_septiembre_string'])) == '':
                vals['media_hiperanual_septiembre'] = -999999.110

        if vals.get('media_hiperanual_octubre_string', None):
            if (vals['media_hiperanual_octubre_string']) != False and vals['media_hiperanual_octubre_string'] != '':
                vals['media_hiperanual_octubre'] = float(vals['media_hiperanual_octubre_string'])
            if (vals['media_hiperanual_octubre_string']) == False or (
            str(vals['media_hiperanual_octubre_string'])) == '':
                vals['media_hiperanual_octubre'] = -999999.110

        if vals.get('media_hiperanual_noviembre_string', None):
            if (vals['media_hiperanual_noviembre_string']) != False and vals['media_hiperanual_noviembre_string'] != '':
                vals['media_hiperanual_noviembre'] = float(vals['media_hiperanual_noviembre_string'])
            if (vals['media_hiperanual_noviembre_string']) == False or (
            str(vals['media_hiperanual_noviembre_string'])) == '':
                vals['media_hiperanual_noviembre'] = -999999.110

        if vals.get('media_hiperanual_diciembre_string', None):
            if (vals['media_hiperanual_diciembre_string']) != False and vals['media_hiperanual_diciembre_string'] != '':
                vals['media_hiperanual_diciembre'] = float(vals['media_hiperanual_diciembre_string'])
            if (vals['media_hiperanual_diciembre_string']) == False or (
            str(vals['media_hiperanual_diciembre_string'])) == '':
                vals['media_hiperanual_diciembre'] = -999999.110
        fecha_actual = datetime.datetime.now()
        if vals.get('anno', None):
            if vals['anno'] <= fecha_actual.year + 1:
                return super(df_explotacion_anual_pozo, self).write(vals)
            else:
                raise ValidationError(_('Error !'),
                                      _('Solo se puede insertar la explotación que exceda en un año,al año actual.'))
        return super(df_explotacion_anual_pozo, self).write(vals)

        # def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        #     if context is None:
        #         context = {}
        #     for arg in args:
        #         arg[2] = '2009'
        #         # self._update_args_or_domain(args)
        #     return super(df_nivel_anual_pozo, self).search(cr, uid, args, offset, limit, order, context=context, count=count)
