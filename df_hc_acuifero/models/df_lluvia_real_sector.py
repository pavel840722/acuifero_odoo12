from odoo import fields, models, api


class df_lluvia_real_sector (models.Model):
    _name = 'df.lluvia.real.sector'
    _inherit = 'df.norma.anual'
    _description = "HC Annual level of wells"
    _rec_name = 'sector_id'
    anno = fields.Integer(string='Year', required=True)

    sector_id = fields.Many2one('df.sector.hidrologico', string='Abbreviation', required=True, ondelete='cascade')

    _sql_constraints = [
        ('anno_uniq', 'unique(sector_id,anno)', 'Sector information already exists for the selected year!'),
    ]
    _order = 'anno desc'
    


