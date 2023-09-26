# -*- coding: utf-8 -*-

from odoo import tools
from odoo import fields, models, api


class df_report_provincia_cuenca (models.Model):
    _description = "Country state"
    _auto = False
    _name = 'df.report.provincia.cuenca'

    id = fields.Integer(string='Name', size=100, required=False, invisible=True)
    nombre = fields.Char(string='Name', size=100, required=False)
    codigo = fields.Char(string='Code', size=100, required=False)
    region_id = fields.Many2one('df.administrative.region', string='Region', required=False)
    # area = fields.Float('Area', digits=(3, 3), required=False, help="Area for calc")
    estado = fields.Char(compute='_estado_cuenca', string='State')

    @api.model_cr  # cr
    def init(self):
        cr = self.env.cr
        tools.drop_view_if_exists(cr, self._table)
        self._cr.execute("""
                create or replace view df_report_provincia_cuenca as (
                  SELECT res_country_state.name AS nombre,
                    res_country_state.code AS codigo,
                    res_country_state.region_id,
                    res_country_state.id
                   FROM res_country_state
                   WHERE res_country_state.region_id = 1 OR res_country_state.region_id = 2 OR res_country_state.region_id = 3
                )
        """)
    @api.multi
    def _estado_cuenca(self):
        cuenca_obj = self.env['df.cuenca.subterranea']
        pozo_obj = self.env['df.pozo']
        res = {}
        objeto_cuencas = cuenca_obj.search([]).ids
        posicion = 11

        provincia_obj = self.env['df.report.provincia.cuenca']
        objeto_provincias = provincia_obj.browse(provincia_obj.search([]).ids)
        for objeto_provincia in objeto_provincias:
            ok = 0
            lista_prioridades = []
            cuenca_ids = cuenca_obj.search([('provincia_id', '=', objeto_provincia.id)]).ids
            if cuenca_ids:
                objeto_cuencas = cuenca_obj.browse(cuenca_ids)
                for objeto_cuenca in objeto_cuencas:
                    vals = {'id': ('objeto_cuenca.id')}
                    temp = 0
                    obj_bloque = self.env['df.bloque']
                    bloque_ids = obj_bloque.search([('sector_id.cuenca_subterranea_id', 'in', ['objeto_cuenca.id'])]).ids
                    obj_sector = self.env['df.sector.hidrologico']
                    sector_ids = obj_sector.search([('cuenca_subterranea_id', 'in', ['objeto_cuenca.id'])]).ids
                    pozo_ids = pozo_obj.search(
                        ['|', ('bloque_id', 'in', bloque_ids), ('sector_hidrologico_id', 'in', sector_ids),
                         ('representativo', '=', True)]).ids
                    if len(pozo_ids) > 0:
                        pozo_ids = pozo_ids.ids
                    pozo_ids1 = pozo_obj.search(
                        [('representativo', '=', True), ('cuenca_subterranea_id', 'in', ['objeto_cuenca.id'])]).ids
                    if len(pozo_ids1) > 0:
                        pozo_ids1 = pozo_ids1.ids
                    pozo_ids.extend([element for element in pozo_ids1 if element not in pozo_ids])
                    encontro = 0
                    if pozo_ids:
                        elementos = self.calcular_media_aritmetica(['objeto_cuenca.id'], pozo_ids, None, None)
                        niveles_ordenados = sorted(elementos[temp], key=lambda tup: tup['anno'], reverse=True)
                        datos_vistas = self.ordenar_diccionario(niveles_ordenados)
                        deltah = self.search([('objeto_cuenca.id')]).promedio_h_periodo

                        max_fijo = self.search([('objeto_cuenca.id')]).maximo_h_periodo_fijo
                        max_calculado = self.search([('objeto_cuenca.id')]).maximo_h_periodo
                        if max_fijo <= 0:
                            max = max_calculado
                        else:
                            max = max_fijo
                        if datos_vistas:
                            for datos_vista in datos_vistas:
                                if encontro == 1:
                                    break
                                while posicion >= 1:
                                    if datos_vista[posicion] and datos_vista[posicion] != None:
                                        nivel_alerta = max - deltah
                                        nivel_alarma = max - (deltah / 2)
                                        if datos_vista[posicion] >= nivel_alerta and datos_vista[
                                            posicion] <= nivel_alarma:
                                            estado = 2  # desfavorable
                                            objeto_provincia.estado = 'regular'
                                            vals['estado1'] = 'regular'
                                        elif datos_vista[posicion] >= nivel_alarma and datos_vista[posicion] <= max:
                                            estado = 1  # muy desfavorable
                                            objeto_provincia.estado = 'mal'
                                            vals['estado1'] = 'mal'
                                            encontro = 1
                                            break
                                        elif datos_vista[posicion] <= nivel_alerta:
                                            estado = 3  # favorable
                                            objeto_provincia.estado = 'bien'
                                            vals['estado1'] = 'bien'
                                        elif datos_vista[posicion] >= max:
                                            estado = 4  # crítico
                                        else:
                                            estado = 'no hay nivel'
                                            objeto_provincia.estado = 'no hay nivel'
                                            vals['estado1'] = 'no hay nivel'
                                        objeto_cuenca.write(vals)
                                        encontro = 1
                                        break
                                    posicion -= 1
                                posicion = 11
                                lista_prioridades.append(estado)
                                objeto_provincia.estado = estado
                        else:
                            objeto_provincia.estado = 'no hay nivel'
                            vals['estado1'] = 'no hay nivel'
                            objeto_cuenca.write(vals)
                    else:
                        objeto_provincia.estado = 'no hay nivel'
                        vals['estado1'] = 'no hay nivel'
                        objeto_cuenca.write(vals)
                bandera = 0
                valor = 1
                while ok < len(lista_prioridades):
                    pos = 0
                    ok = ok + 1
                    if bandera == 1:
                        break
                    for lista_prioridade in lista_prioridades:
                        if lista_prioridade == valor:
                            bandera = 1
                            break
                        pos = pos + 1
                    valor = valor + 1
                valor = valor - 1
                if valor == 1:
                    objeto_provincia.estado = 'muy desfavorable'
                elif valor == 2:
                    objeto_provincia.estado = 'desfavorable'
                elif valor == 3:
                    objeto_provincia.estado = 'favorable'
                elif valor == 4:
                    objeto_provincia.estado = u'crítico'
                else:
                    objeto_provincia.estado = 'no hay nivel'
            else:
                objeto_provincia.estado = 'no hay nivel'
        #return res

