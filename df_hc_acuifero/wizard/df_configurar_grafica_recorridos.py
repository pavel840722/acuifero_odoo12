# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime, time
from odoo.exceptions import MissingError, _logger, Warning


class df_configurar_grafica_recorridos(models.TransientModel):
    _name = 'df.configurar.grafica.recorridos'
    _description = 'Wizard to config travels graphic'

    # def onchange_tipo_calculo(self, cr, uid, ids, tipo, context=None):
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

    @api.onchange('desde', 'hasta')
    def _reset_state(self):
        self.state = 'choose'
        if self.desde and self.hasta:
            if self.desde > self.hasta:
                # self.fecha_ini = None
                raise Warning(('La fecha inicial no puede ser mayor que la final, verifique.'))

    def graficar(self):
        datos = {
                 'desde': str(self.desde),
                 'hasta': str(self.hasta),
                 'elemento_graficar': self.elemento_graficar,
                 'metodo_aritmetico': self.metodo_aritmetico,
                 'metodo_formula': self.metodo_formula,
                 'rango_limpieza': self.rango_limpieza,
                 'bloque_id': self.bloque_id.id,
                 'sector_id': self.sector_id.id,
                 'cuenca_id': self.cuenca_id.id,
                 'pozo_id': self.pozo_id.id,
                 'pozo_bloque_ids': self.pozo_bloque_ids.ids,
                 'pozo_cuenca_ids': self.pozo_cuenca_ids.ids,
                 'pozo_sector_ids': self.pozo_sector_ids.ids,
                 }
        grafico_curva_agotamiento = {
            'name': 'Curva de agotamiento',
            'type': 'ir.actions.client',
            'tag': 'grafico_recorridos_view',
            'target': 'main',
            'params': datos,
        }
        return grafico_curva_agotamiento

    desde = fields.Date(string='From', required=True, default=_default_initial_date)
    hasta = fields.Date(string='To', required=True, default=_default_final_date)
    elemento_graficar = fields.Selection(
        [('pozo', 'Well'), ('bloque', 'Block'), ('sector', 'Sector'), ('cuenca', 'Basin')],
        string='Element to graphic', required=True, help="", default='pozo')
    metodo_aritmetico = fields.Boolean(string='Arithmetic', default=True)
    metodo_formula = fields.Boolean(string='Formula')

    valor_precision = fields.Float('Precision value', digits=(3,3), required=False,
                                   help="Put precision level value for detection algorithm,\n"
                                        "if precision is closer to 0 then algorithm take minnor level diference as an important change",
                                   default=0.2)
    rango_limpieza = fields.Float('Cleaning range value', digits=(3, 3), required=False,
                                  help="Put cleaning range value for detection algorithm,\n"
                                       "if difference in limnigrama between points is lower than value predecesor point will be ignored,\n"
                                       "If value is 0 then detection algorithm ignore cleaning job")
    cuenca_id = fields.Many2one('df.cuenca.subterranea', string='Basin', required=False, ondelete='cascade')
    sector_id = fields.Many2one('df.sector.hidrologico', string='Sector', required=False, ondelete='cascade')
    bloque_id = fields.Many2one('df.bloque', string='Block', required=False, ondelete='cascade')
    pozo_id = fields.Many2one('df.pozo', string='Well', required=False, ondelete='cascade')

    pozo_bloque_ids = fields.Many2many('df.pozo', 'mm_config_recorridos_bloque_pozos', 'config_if', 'pozo_id')
    pozo_sector_ids = fields.Many2many('df.pozo', 'mm_config_recorridos_sector_pozos', 'config_if', 'pozo_id')
    pozo_cuenca_ids = fields.Many2many('df.pozo', 'mm_config_recorridos_cuenca_pozos', 'config_if', 'pozo_id')
