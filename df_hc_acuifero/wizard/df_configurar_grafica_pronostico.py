# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime, time
from datetime import datetime


class df_configurar_grafica_pronostico(models.TransientModel):
    _name = "df.configurar.grafica.pronostico"
    _description = "Wizard to config graphic"


    # def onchange_tipo_calculo(self, tipo):
    #     res = {}
    #     if tipo == 'formula':
    #         res.update({'metodo_aritmetico': False, 'metodo_formula': True})
    #     else:
    #         res.update({'metodo_aritmetico': True, 'metodo_formula': False})
    #     return {'value': res}

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
        f_min = fech - 40
        while f_min <= fech:
            res.append((f_min, f_min))
            f_min += 1
        return res

    def _year_select(self):

        fecha = datetime.now().strftime('%Y-%m-%d')
        fech = int(fecha.split('-')[0])
        return fech

    def graficar(self):
        datos = {
                 'year':              int(self.year),
                 'elemento_graficar': self.elemento_graficar,
                 'pronostico':        self.pronostico,
                 'metodo_aritmetico': self.metodo_aritmetico,
                 'metodo_formula':    self.metodo_formula,
                 'cuenca_id':         self.cuenca_id.id,
                 'sector_id':         self.sector_id.id,
                 'bloque_id':         self.bloque_id.id,
                 'pozo_id':           self.pozo_id.id,
                 'pozo_bloque_ids':   self.pozo_bloque_ids.ids,
                 'pozo_cuenca_ids':   self.pozo_cuenca_ids.ids,
                 'pozo_sector_ids':   self.pozo_sector_ids.ids,
                }
        grafico_pronostico = {
            'name': 'Pronostico',
            'type': 'ir.actions.client',
            'tag': 'grafico_pronostico_view',
            'target': 'main',
            'params': datos,
        }
        return grafico_pronostico

    year = fields.Selection(_get_year, 'Year', default=_year_select, required=True)
    elemento_graficar = fields.Selection(
        [('pozo', 'Well'), ('bloque', 'Block'), ('sector', 'Sector'), ('cuenca', 'Basin')],
        string='Element to graphic', required=True, help="", default='pozo')
    metodo_aritmetico = fields.Boolean(string='Arithmetic', default=True)
    metodo_formula = fields.Boolean(string='Formula')
    pronostico = fields.Selection([('puro', 'Pronóstico'), ('real', 'Real')], string='Pronostic', required=True,
                                  help="", default='puro')
    cuenca_id = fields.Many2one('df.cuenca.subterranea', string='Basin', required=False, ondelete='cascade')
    sector_id = fields.Many2one('df.sector.hidrologico', string='Sector', required=False, ondelete='cascade')
    bloque_id = fields.Many2one('df.bloque', string='Block', required=False, ondelete='cascade')
    pozo_id = fields.Many2one('df.pozo', string='Well', required=False, ondelete='cascade')

    pozo_bloque_ids = fields.Many2many('df.pozo', 'mm_config_pronostico_bloque_pozos', 'config_if', 'pozo_id')
    pozo_sector_ids = fields.Many2many('df.pozo', 'mm_config_pronostico_sector_pozos', 'config_if', 'pozo_id')
    pozo_cuenca_ids = fields.Many2many('df.pozo', 'mm_config_pronostico_cuenca_pozos', 'config_if', 'pozo_id')








