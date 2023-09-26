# -*- coding: utf-8 -*-

from odoo import models, fields, api


class df_cuenca_subterranea_acuifero(models.Model):
    _name = 'df.cuenca.subterranea.acuifero'
    _description = "HC underground basin and equipment"

    cuenca_subterranea_id = fields.Many2one('df.cuenca.subterranea', 'Underground basin', required=True,
                                            ondelete='cascade')
    #equipo_ids = fields.Many2many('df.hc.rain.base.equipment', 'df_equipo_cuenca_subterranea', 'fk_cuenca_id','fk_equipo_id', string='Pluviometers')

#Este campo equipo_ids es de otro modulo que no se ha hecho todav�a en ODOO 12

# AQUI NO TRABAJO FRANK
