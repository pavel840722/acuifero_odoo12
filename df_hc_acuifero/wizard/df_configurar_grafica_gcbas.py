# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime, time
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError

class df_configurar_grafica_gcbas(models.TransientModel):
    _name = "df.configurar.grafica.gcbas"
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

    def graficar(self):
        if self.desde > self.hasta:
          raise UserError(_('La fecha inicial no puede ser mayor que la final, verifique.'))

        datos = {'desde': str(self.desde),
                 'hasta': str(self.hasta),
                 'elemento_graficar': self.elemento_graficar,
                 'duracion_graficar': self.duracion_graficar,
                 'pozo_id': self.pozo_id.id,
                 'pozo_bloque_ids':self.pozo_bloque_ids.ids,
                 'pozo_cuenca_ids':self.pozo_cuenca_ids.ids,
                 'pozo_sector_ids':self.pozo_sector_ids.ids,
                 'metodo_formula':self.metodo_formula,
                 'pronostico':self.pronostico,
                 'presage':self.presage,
                 'meses':self.meses,
                 'bloque_id':self.bloque_id.id,
                 'sector_id':self.sector_id.id,
                 'cuenca_id':self.cuenca_id.id,
                 }
        grafico_acuifero = {
            'name': 'GCBAS',
            'type': 'ir.actions.client',
            'tag': 'grafico_acuifero_view',
            'target': 'main',
            'params': datos,
        }
        return grafico_acuifero

    desde = fields.Date(string='From', required=True, default=_default_initial_date)
    hasta = fields.Date(string='To', required=True, default=_default_final_date)
    year1 = fields.Selection(_get_year, 'Año')

    meses = fields.Selection([('0', 'Enero'), ('1', 'Febrero'), ('2', 'Marzo'), ('3', 'Abril'), ('4', 'Mayo'),
                              ('5', 'Junio'), ('6', 'Julio'), ('7', 'Agosto'), ('8', 'Septiembre'), ('9', 'Octubre'),
                              ('10', 'Noviembre'), ('11', 'Diciembre')], string='Mes', required=True, help="", default='0')

    elemento_graficar = fields.Selection(
        [('pozo', 'Well'), ('bloque', 'Block'), ('sector', 'Sector'), ('cuenca', 'Basin')],
        string='Element to graphic', required=True, help="", default='pozo')

    metodo_aritmetico = fields.Boolean(string='Arithmetic', default=True)
    metodo_formula = fields.Boolean(string='Formula')

    cuenca_id = fields.Many2one('df.cuenca.subterranea', string='Basin', required=False, ondelete='cascade')
    sector_id = fields.Many2one('df.sector.hidrologico', string='Sector', required=False, ondelete='cascade')
    bloque_id = fields.Many2one('df.bloque', string='Block', required=False, ondelete='cascade')
    pozo_id = fields.Many2one('df.pozo', string='Well', required=False, ondelete='cascade')

    pozo_bloque_ids = fields.Many2many('df.pozo', 'mm_config_gcbas_bloque_pozos', 'config_if', 'pozo_id')
    pozo_sector_ids = fields.Many2many('df.pozo', 'mm_config_gcbas_sector_pozos', 'config_if', 'pozo_id')
    pozo_cuenca_ids = fields.Many2many('df.pozo', 'mm_config_gcbas_cuenca_pozos', 'config_if', 'pozo_id')
    presage = fields.Boolean('With presage?')
    pronostico = fields.Selection([('puro', 'Pronóstico'), ('real', 'Real')], string='Pronostic', required=True,
                                  help="", default='puro')

    duracion_graficar = fields.Selection([('Y', 'Year'), ('2Y', '2Year'), ], string='Graphic by', required=True,
                                         help="", default='Y')
