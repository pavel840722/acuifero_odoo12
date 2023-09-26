# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import urllib.request
import json
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError

class df_acuifero_integracion(models.TransientModel):
    _name = "df.acuifero.integracion"
    _description = "Wizard to integration"


    def integrar(self):
        fecha_actual = datetime.now()
        anno_actual = fecha_actual.year
        mes_actual =  fecha_actual.month
        url = "https://rsgia.hidro.gob.cu/reportserver/reportserver/httpauthexport?user=" \
              "hidrocuba&apikey=hidrocuba&format=json&download=false&key=pozonivelmensual&p_anno=%s&p_mes=%s"%(anno_actual,mes_actual)
        try:
            response = urllib.request.urlopen(url)
        except:
            raise UserError(
                _("No hay conexión."))
        todos = json.loads(response.read())
        pozo_obj = self.env['df.pozo']
        nivel_anual_obj = self.env['df.nivel.anual.pozo']
        # todos = [{"id":587,"nombre":"Antes de Camp",
        #           "sigla":"P-24","idprovincia":33,"provincia":"Granma","codigoprovincia":"Pro_33",
        #           "fecha":"2020-02-04","nivel":11.01},{"id":191,"nombre":"Areopuerto Agricola",
        #          "sigla":"P-156","idprovincia":33,"provincia":"Granma","codigoprovincia":"Pro_33","fecha":"2020-02-04","nivel":1.29}]
        for todo in todos:
            sigla = todo['sigla']
            pozo_ids = pozo_obj.search([('sigla','=',sigla)])
            if pozo_ids:
                vals = {}
                vals['anno'] = anno_actual
                vals['pozo_id'] = pozo_ids[0].id
                if mes_actual == 1:
                    vals['media_hiperanual_enero_string'] = todo['nivel']
                if mes_actual == 2:
                    vals['media_hiperanual_febrero_string'] = todo['nivel']
                if mes_actual == 3:
                    vals['media_hiperanual_marzo_string'] = todo['nivel']
                if mes_actual == 4:
                    vals['media_hiperanual_abril_string'] = todo['nivel']
                if mes_actual == 5:
                    vals['media_hiperanual_mayo_string'] = todo['nivel']
                if mes_actual == 6:
                    vals['media_hiperanual_junio_string'] = todo['nivel']
                if mes_actual == 7:
                    vals['media_hiperanual_julio_string'] = todo['nivel']
                if mes_actual == 8:
                    vals['media_hiperanual_agosto_string'] = todo['nivel']
                if mes_actual == 9:
                    vals['media_hiperanual_septiembre_string'] = todo['nivel']
                if mes_actual == 10:
                    vals['media_hiperanual_octubre_string'] = todo['nivel']
                if mes_actual == 11:
                    vals['media_hiperanual_noviembre_string'] = todo['nivel']
                if mes_actual == 12:
                    vals['media_hiperanual_diciembre_string'] = todo['nivel']
                nivel_pozo_anno_ids = nivel_anual_obj.search([('pozo_id','=',pozo_ids[0].id),('anno','=',anno_actual)])
                if nivel_pozo_anno_ids:
                    nivel_pozo_anno_ids.write(vals)
                else:
                    nivel_anual_obj.create(vals)

            else:
                continue

