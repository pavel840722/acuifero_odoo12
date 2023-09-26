# -*- coding: utf-8 -*-

from odoo import models, fields, api


class df_probabilidad_bloque(models.Model):
    _name = 'df.probabilidad.bloque'
    _inherit = 'df.norma.anual'
    _description = "HC Annual level of wells"
    _rec_name = 'bloque_id'
    probabilidad = fields.Selection([('50%', '50%'), ('75%', '75%'),
                                     ('95%', '95%')],
                                    string='Probability', required=True,
                                    help="")
    bloque_id = fields.Many2one('df.bloque', string='Code', required=True, ondelete='cascade')
    anno = fields.Integer(string='Año', required=True)

    _sql_constraints = [
        ('probabilidad_uniq', 'unique(bloque_id,probabilidad,anno)', 'The probability already exists for that object!'),
    ]

    @api.model
    def create(self, vals):
        vals['active'] = True
        return super(df_probabilidad_bloque, self).create(vals)

