# -*- coding: utf-8 -*-

from odoo import models, fields, api


class df_probabilidad_sector(models.Model):
    _name = 'df.probabilidad.sector'
    _inherit = 'df.norma.anual'
    _description = "HC Annual level of wells"
    _rec_name = 'sector_id'
    probabilidad = fields.Selection([('50%', '50%'), ('75%', '75%'),
                                     ('95%', '95%')],
                                    string='Probability', required=True,
                                    help="")
    sector_id = fields.Many2one('df.sector.hidrologico', string='Code', required=True, ondelete='cascade')
    anno = fields.Integer(string='Año', required=True)

    _sql_constraints = [
        ('probabilidad_uniq', 'unique(sector_id,probabilidad,anno)', 'The probability already exists for that object!'),
    ]

    @api.model
    def create(self, vals):
        vals['active'] = True
        return super(df_probabilidad_sector, self).create(vals)


