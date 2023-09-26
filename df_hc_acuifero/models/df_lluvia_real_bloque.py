# -*- coding: utf-8 -*-

from datetime import datetime
from time import time
from odoo import models, fields, api,_


class df_lluvia_real_bloque(models.Model):
    _name = 'df.lluvia.real.bloque'
    # _rec_name = 'id'
    _inherit = 'df.norma.anual'
    _rec_name = 'bloque_id'
    _description = "HC Annual level of wells"
    anno = fields.Integer(string='Year', required=True)
    bloque_id = fields.Many2one('df.bloque', string='Abbreviation', required=True, ondelete='cascade')
        # 'anno_final': fields.integer(string='Year', required=False),
        # 'anno': fields.char('Year', size=4, readonly=True),
        # 'anno': fields.char('Year', size=4, required=True),


    _sql_constraints = [
        ('anno_uniq', 'unique(bloque_id,anno)', 'Block information already exists for the selected year!'),
        ]
    _order = 'anno desc'
df_lluvia_real_bloque()
