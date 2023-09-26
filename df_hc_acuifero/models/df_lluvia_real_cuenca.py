from odoo import fields, models, api


class df_lluvia_real_cuenca (models.Model):
    _name = 'df.lluvia.real.cuenca'
    _description = 'Description'
    _inherit = 'df.norma.anual'
    _rec_name = 'cuenca_id'
    anno = fields.Integer(string='Year', required=True)
    cuenca_id = fields.Many2one('df.cuenca.subterranea', string='Code', required=True, ondelete='cascade')

    _sql_constraints = [
        ('anno_uniq', 'unique(cuenca_id,anno)', 'The basin information for the selected year already exists!'),
    ]
    _order = 'anno desc'
    


