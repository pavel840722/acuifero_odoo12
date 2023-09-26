# -*- coding: utf-8 -*-

from datetime import datetime
from time import time
from odoo import models, fields, api,_


class df_lluvia_real_pozo(models.Model):
    _name = 'df.lluvia.real.pozo'
    _inherit = 'df.norma.anual'
    _description = "HC Annual level of wells"
    _rec_name = 'pozo_id'
    anno = fields.Integer(string='Year', required=True)
    pozo_id = fields.Many2one('df.pozo', string='Abbreviation', required=True, ondelete='cascade')
        # 'anno_final': fields.integer(string='Year', required=False),
        # 'anno': fields.char('Year', size=4, readonly=True),
        # 'anno': fields.char('Year', size=4, required=True),


    _sql_constraints = [
        ('anno_uniq', 'unique(pozo_id,anno)', 'Well information already exists for the selected year!'),
        ]
    _order = 'anno desc'
df_lluvia_real_pozo()
