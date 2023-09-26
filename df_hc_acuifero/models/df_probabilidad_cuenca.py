# -*- coding: utf-8 -*-

from odoo import models, fields, api


class df_probabilidad_cuenca(models.Model):
    _name = 'df.probabilidad.cuenca'
    _inherit = 'df.norma.anual'
    _description = "HC Annual level of wells"
    _rec_name = 'cuenca_id'
    probabilidad = fields.Selection([('50%', '50%'),('75%', '75%'),
                                         ('95%', '95%')],
                                        string = 'Probability', required=True,
                                        help="")
    cuenca_id = fields.Many2one('df.cuenca.subterranea', string='Code', required=True, ondelete='cascade')
    anno = fields.Integer(string='Año', required=True)

    _sql_constraints = [
        ('probabilidad_uniq', 'unique(cuenca_id,probabilidad,anno)', 'The probability already exists for that object!'),
        ]

    @api.model
    def create(self, vals):
        vals['active'] = True
        return super(df_probabilidad_cuenca, self).create(vals)
