# -*- coding: utf-8 -*-
from odoo import models, fields, api


class df_zona_hidrografica_pluviometro(models.Model):
    _name = 'df.zona.hidrografica.pluviometro'
    _description = "HC Hydrografic zone - rain equipment"

    cuenca_hidrografica_id = fields.Many2one('df.zona.hidrografica', 'Hydrografic zone', required=True,
                                              ondelete='cascade')
    equipo_ids = fields.Many2many('df.hc.rain.base.equipment', 'mm_zona_hidrografica_pluviometro', 'fk_zona_id',
                                  'fk_pluviometro_id', string='Pluviometers')

    _sql_constraints = [
        ('cuenca_hidrografica_uniq', 'unique(cuenca_hidrografica_id)', 'Only must be one Hydrografic zone!')
    ]

df_zona_hidrografica_pluviometro()