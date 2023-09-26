# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
import datetime
import time

class df_tabla_regresion(models.Model):
    _name = 'df.tabla.regresion'
    _description = "HC Regression table"

    desde = fields.Date('From', required=False)
    hasta = fields.Date('To', required=False)
    objeto_tipo = fields.Selection([('pozo', 'Well'),
                                ('bloque', 'Block'),
                                ('sector', 'Sector'),
                                ('cuenca', 'Basin')],
                               'Element to graphic', required=True)
    objeto_id = fields.Integer('Objeto id', required=True)
    tiempo = fields.Integer('Time', required=True)
    regresion = fields.Float('Regression', digits=(6,2), required=True)
    zt = fields.Float('ZT', digits=(6,2), required=True)

    @api.model
    def guardar(self, vals):
        if len(vals) > 0:
            tabla_previa_objs = self.search([('objeto_tipo','=',vals['data'][0]['objeto_tipo']),('objeto_id','=',vals['data'][0]['objeto_id'])])
            if len(tabla_previa_objs)>0:
                for obj in tabla_previa_objs:
                  obj.unlink()
            for val in vals['data']:
                self.create(val)
        return True





