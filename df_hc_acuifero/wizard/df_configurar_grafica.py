
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime, time
from odoo.exceptions import MissingError, _logger, Warning


class df_configurar_grafica(models.TransientModel):
    _name = "df.configurar.grafica"
    _description = "Wizard to config graphic"

    @api.model
    def onchange_tipo_calculo(self, tipo):
        res = {}
        if tipo == 'formula':
            res.update({'metodo_aritmetico': False, 'metodo_formula': True})
        else:
            res.update({'metodo_aritmetico': True, 'metodo_formula': False})
        return {'value': res}

    @api.onchange('desde', 'hasta')
    def _reset_state(self):
        self.state = 'choose'
        if self.desde and self.hasta and self.desde > self.hasta:
            raise Warning(('La fecha inicial no puede ser mayor que la final, verifique.'))

    def _default_initial_date(self):
        date = datetime.datetime(1982, 1, 1, 0, 0)
        return date.strftime('%Y-%m-%d')



    def graficar(self):
       desde = str(self.desde)
       hasta = str(self.hasta)
       desde = datetime.datetime(int(desde[0:4]), int(desde[5:7]), int(desde[8:]))
       hasta = datetime.datetime(int(hasta[0:4]), int(hasta[5:7]), int(hasta[8:]))
       if desde > hasta:
           raise Warning('La fecha inicial no puede ser mayor que la final, verifique.')

       datos = {
                 'desde': str(self.desde),
                 'hasta': str(self.hasta),
                 'elemento_graficar': self.elemento_graficar,
                 'metodo_aritmetico': self.metodo_aritmetico,
                 'metodo_formula':self.metodo_formula,
                 'pozo_id': self.pozo_id.id,
                 'bloque_id':self.bloque_id.id,
                 'sector_id':self.sector_id.id,
                 'cuenca_id':self.cuenca_id.id,
                 'pozo_bloque_ids':self.pozo_bloque_ids.ids,
                 'pozo_cuenca_ids':self.pozo_cuenca_ids.ids,
                 'pozo_sector_ids':self.pozo_sector_ids.ids,
                }
       grafico_escala = {
            'name': 'Con Escala',
            'type': 'ir.actions.client',
            'tag': 'grafico_limnigrama_cotas_view',
            'target': 'main',
            'params': datos,
        }

       return grafico_escala

    desde = fields.Date(string='From', required=True, default=_default_initial_date)
    hasta = fields.Date(string='To', required=True, default=models.date_utils.date.today())
    elemento_graficar = fields.Selection(
        [('pozo', 'Well'), ('bloque', 'Block'), ('sector', 'Sector'), ('cuenca', 'Basin')],
        string='Element to graphic', required=True, help="", default='pozo')

    metodo_aritmetico = fields.Boolean(string='Arithmetic', default=True)
    metodo_formula = fields.Boolean(string='Formula')

    cuenca_id = fields.Many2one('df.cuenca.subterranea', string='Basin', required=False, ondelete='cascade')
    sector_id = fields.Many2one('df.sector.hidrologico', string='Sector', required=False, ondelete='cascade')
    bloque_id = fields.Many2one('df.bloque', string='Block', required=False, ondelete='cascade')
    pozo_id = fields.Many2one('df.pozo', string='Well', required=False, ondelete='cascade')

    pozo_bloque_ids = fields.Many2many('df.pozo', 'mm_config_grafica_bloque_pozos', 'config_if', 'pozo_id')
    pozo_sector_ids = fields.Many2many('df.pozo', 'mm_config_grafica_sector_pozos', 'config_if', 'pozo_id')
    pozo_cuenca_ids = fields.Many2many('df.pozo', 'mm_config_grafica_cuenca_pozos', 'config_if', 'pozo_id')

    


