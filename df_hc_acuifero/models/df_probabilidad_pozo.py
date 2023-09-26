# -*- coding: utf-8 -*-

from odoo import models, fields, api


class df_probabilidad_pozo(models.Model):
    _name = 'df.probabilidad.pozo'
    _inherit = 'df.norma.anual'
    _description = "HC Annual level of wells"
    _rec_name = 'pozo_id'
    probabilidad = fields.Selection([('50%', '50%'),('75%', '75%'),
                                         ('95%', '95%')],
                                        string = 'Probability', required=True,
                                        help="")
    pozo_id = fields.Many2one('df.pozo', string='Abbreviation', required=True, ondelete='cascade')
    anno = fields.Integer(string='Year', required=True)

    _sql_constraints = [
        ('probabilidad_uniq', 'unique(pozo_id,probabilidad,anno)', 'The probability already exists for that object!'),
        ]

    @api.model
    def create(self, vals):
        vals['active'] = True
        return super(df_probabilidad_pozo, self).create(vals)

