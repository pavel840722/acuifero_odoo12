# -*- coding: utf-8 -*-
# from openerp.modules import module
# from osv import osv, fields
from odoo import models, fields, api,_
# from tools.translate import _
# import tools
import datetime, time
from datetime import datetime



class df_config_grafica_pronostico_seco(models.TransientModel):
    _name = 'df.config.grafica.pronostico.seco'
    _description = 'Wizard Grafica periodo seco'

    def _default_initial_date(self):
        date = datetime.datetime(1982, 1, 1, 0, 0)
        return date.strftime('%Y-%m-%d')

    def _default_final_date(self):
        date = datetime.datetime(2013, 12, 1, 0, 0)
        return date.strftime('%Y-%m-%d')

    def _get_year(self):
        res = []
        fecha = time.strftime('%Y-%m-%d')
        fech = int(fecha.split('-')[0])
        f_min = fech-40
        while f_min <= fech:
            res.append((f_min,f_min))
            f_min+=1
        return res

    def _year_select(self):
        # res = {}
        fecha = time.strftime('%Y-%m-%d')
        fech = int(fecha.split('-')[0])
        return fech

    def graficar(self):
        pozo_id = False
        if len(self.pozo_id) > 0:
            pozo_id =  self.pozo_id[0].id
        datos = {'year': int(self.year),
                 'year1': self.year1,
                 'meses': self.meses,
                 'metodo_graficar': self.metodo_graficar,
                 'elemento_graficar': self.elemento_graficar,
                 'duracion': self.duracion,
                 'formula': self.formula,
                 'pronostico': self.pronostico,
                 'cuenca_id': self.cuenca_id.id,
                 'sector_id': self.sector_id.id,
                 'bloque_id': self.bloque_id.id,
                 'pozo_id': pozo_id,
                 'recurso_explotable':self.recurso_explotable,
                 'pozo_bloque_ids':self.pozo_bloque_ids.ids,
                 'pozo_sector_ids':self.pozo_sector_ids.ids,
                 'pozo_cuenca_ids':self.pozo_cuenca_ids.ids,
                 }
        grafico_pronostico_seco = {
            'name': 'Pronóstico seco',
            'type': 'ir.actions.client',
            'tag': 'grafico_pronostico_seco_view',
            'target': 'main',
            'params': datos,
        }
        return grafico_pronostico_seco

    year = fields.Selection(_get_year, 'Year', default=_year_select, required=True)
    year1 = fields.Selection(_get_year, 'Year')
    meses = fields.Selection([('0', 'Enero'),
                                           ('1', 'Febrero'),
                                           ('2', 'Marzo'),
                                           ('3', 'Abril'),
                                           ('4', 'Mayo'),
                                           ('5', 'Junio'),
                                           ('6', 'Julio'),
                                           ('7', 'Agosto'),
                                           ('8', 'Septiembre'),
                                           ('9', 'Octubre'),
                                           ('10', 'Noviembre'),
                                           ('11', 'Diciembre')],
                                          'Mes', required=True,
                                          help="", default='0')
    elemento_graficar = fields.Selection([('pozo', 'Well'),
                                           ('bloque', 'Block'),
                                           ('sector', 'Sector'),
                                           ('cuenca', 'Basin')],
                                          'Element to graphic', required=True,
                                          help="", default='pozo')
    metodo_graficar = fields.Selection([('CA', 'Curve'),
                                           ('EX', 'Explotation'),],
                                          'Methot', required=True,
                                          help="", default='CA')
    duracion = fields.Selection([('P', 'Period'),
                                           ('Y', 'Year'),
                                            ('2Y', '2Year'),],
                                          'Graphic by', required=True,
                                          help="", default='P')
    metodo_aritmetico = fields.Boolean('Arithmetic', default=True)
    formula = fields.Boolean('Formula')
    pronostico = fields.Selection([('puro', 'Pronóstico'),
                                    ('real', 'Real')],
                                          'Pronostic', required=True,
                                          help="", default='puro')
    cuenca_id = fields.Many2one('df.cuenca.subterranea', 'Basin', required=False)
    sector_id = fields.Many2one('df.sector.hidrologico', 'Sector', required=False)
    bloque_id = fields.Many2one('df.bloque', 'Block', required=False)
    pozo_id = fields.Many2one('df.pozo', 'Well', required=False)
    recurso_explotable = fields.Boolean('Calculate exploitable resource')
    pozo_bloque_ids = fields.Many2many('df.pozo', 'mm_config_pronostico_seco_bloque_pozos', 'config_if', 'pozo_id')
    pozo_sector_ids = fields.Many2many('df.pozo', 'mm_config_pronostico_seco_sector_pozos', 'config_if', 'pozo_id')
    pozo_cuenca_ids = fields.Many2many('df.pozo', 'mm_config_pronostico_seco_cuenca_pozos', 'config_if', 'pozo_id')

# df_config_grafica_pronostico_seco()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

