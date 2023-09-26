# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError
import time, datetime
from dateutil.relativedelta import relativedelta
#import math
#from decimal import Decimal, ROUND_HALF_UP
#from tools.translate import _


class df_tramo(models.Model):
    _name = 'df.tramo'
    _inherit = 'df.hidro.base'
    _rec_name = 'sigla'

    # AQUI TRABAJO FRANK Y EVELYN
    def obtener_cotas_tramos(self, pozo_ids, fecha_inicio, fecha_fin):
        if pozo_ids:
            sql = """ SELECT anno,AVG(NULLIF(cota_agua_enero,-999999.110)) as cota_agua_enero,
                             AVG(NULLIF(cota_agua_febrero,-999999.110)) as cota_agua_febrero,
                             AVG(NULLIF(cota_agua_marzo,-999999.110)) as cota_agua_marzo,
                             AVG(NULLIF(cota_agua_abril,-999999.110)) as cota_agua_abril,
                             AVG(NULLIF(cota_agua_mayo,-999999.110)) as cota_agua_mayo,
                             AVG(NULLIF(cota_agua_junio,-999999.110)) as cota_agua_junio,
                             AVG(NULLIF(cota_agua_julio,-999999.110)) as cota_agua_julio,
                             AVG(NULLIF(cota_agua_agosto,-999999.110)) as cota_agua_agosto,
                             AVG(NULLIF(cota_agua_septiembre,-999999.110)) as cota_agua_septiembre,
                             AVG(NULLIF(cota_agua_octubre,-999999.110)) as cota_agua_octubre,
                             AVG(NULLIF(cota_agua_noviembre,-999999.110)) as cota_agua_noviembre,
                             AVG(NULLIF(cota_agua_diciembre,-999999.110)) as cota_agua_diciembre
                      from df_report_cota_agua
                      where pozo_id in %s AND
                      anno BETWEEN """ + str(fecha_inicio.year) + """ AND """ + str(fecha_fin.year) + """
                      group by anno
                      order by anno asc"""
            self.env.cr.execute(sql, (tuple(pozo_ids),))
            datos_vistas = self.env.cr.dictfetchall()
            return datos_vistas
        else:
             raise UserError(_('Debe de seleccionar los pozos.'))
             #raise osv.except_osv(_("Alerta !"), _("Debe de seleccionar los pozos."))

    def formar_fecha_inicio(self, pozo_ids):
        lista = []
        pozo_obj = self.env['df.pozo']
        for pozo in pozo_ids:
            existe = pozo_obj.existe_pozo(pozo)
            if existe:
                datos_vistas = pozo_obj.obtener_nivele_actual_asc(pozo)
                buscar = pozo_obj.buscar_anno(pozo)
                encontro = 0
                dia = 1
                mes = 1
                anno_inicio = buscar[0]['anno']
                fecha_inicio = datetime.datetime(anno_inicio, mes, dia)
                for datos_vista in datos_vistas:
                    if encontro == 1:
                        break
                    temp = 0
                    mes_valor = 0
                    for valor in datos_vista:
                        if temp >= 1 and valor and valor != -999999.110:
                            mes_valor += 1
                            dia = 1
                            mes = mes_valor
                            anno_inicio = datos_vista[0]
                            fecha_inicio = datetime.datetime(anno_inicio, mes, dia)
                            lista.append(fecha_inicio)
                            encontro = 1
                            break
                        temp += 1
        if lista:
            lista.sort()
            return lista[0]
        else:
            return False

    def formar_fecha_fin(self, pozo_ids):
        lista = []
        pozo_obj = self.env['df.pozo']
        for pozo in pozo_ids:
            existe = pozo_obj.existe_pozo(pozo)
            if existe:
                datos_vistas = pozo_obj.obtener_nivele_actual(pozo)
                buscar = pozo_obj.buscar_anno_desc(pozo)
                encontro = 0
                posicion = 12
                dia = 1
                mes = 12
                anno_fin = buscar[0]['anno']
                fecha_fin = datetime.datetime(anno_fin, mes, dia)
                for datos_vista in datos_vistas:
                    if encontro == 1:
                        break
                    while posicion >= 1:
                        if datos_vista[posicion] and datos_vista[posicion] != -999999.110:
                            dia = 1
                            mes = posicion
                            anno_fin = datos_vista[0]
                            fecha_fin = datetime.datetime(anno_fin, mes, dia)
                            lista.append(fecha_fin)
                            encontro = 1
                            break
                        posicion -= 1
                    posicion = 12
        if lista:
            lista.sort(reverse=True)
            return lista[0]
        else:
            return False

    def _periodomonth(self, month):
        if month >= 5 and month <= 10:
            return 'humedo'
        return 'seco'

    def _lengthmonth(self, year, month):
        if month == 2 and ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))):
            return 29
        return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]

    def _numero_mes(self, month):
        if month == 'January' or month == 'Enero':
            return 1
        if month == 'February' or month == 'Febrero':
            return 2
        if month == 'March' or month == 'Marzo':
            return 3
        if month == 'Abril' or month == 'April':
            return 4
        if month == 'May' or month == 'Mayo':
            return 5
        if month == 'June' or month == 'Junio':
            return 6
        if month == 'July' or month == 'Julio':
            return 7
        if month == 'August' or month == 'Agosto':
            return 8
        if month == 'September' or month == 'Septiembre':
            return 9
        if month == 'October' or month == 'Octubre':
            return 10
        if month == 'November' or month == 'Noviembre':
            return 11
        if month == 'December' or month == 'Diciembre':
            return 12
        return 1

    def _numero_mes(self, month):
        if month == 'January' or month == 'Enero':
            return 1
        if month == 'February' or month == 'Febrero':
            return 2
        if month == 'March' or month == 'Marzo':
            return 3
        if month == 'Abril' or month == 'April':
            return 4
        if month == 'May' or month == 'Mayo':
            return 5
        if month == 'June' or month == 'Junio':
            return 6
        if month == 'July' or month == 'Julio':
            return 7
        if month == 'August' or month == 'Agosto':
            return 8
        if month == 'September' or month == 'Septiembre':
            return 9
        if month == 'October' or month == 'Octubre':
            return 10
        if month == 'November' or month == 'Noviembre':
            return 11
        if month == 'December' or month == 'Diciembre':
            return 12
        return 1

    def _mes_numero(self, month):
        if month == 1:
            return 'enero'
        if month == 2:
            return 'febrero'
        if month == 3:
            return 'marzo'
        if month == 4:
            return 'abril'
        if month == 5:
            return 'mayo'
        if month == 6:
            return 'junio'
        if month == 7:
            return 'julio'
        if month == 8:
            return 'agosto'
        if month == 9:
            return 'septiembre'
        if month == 10:
            return 'octubre'
        if month == 11:
            return 'noviembre'
        if month == 12:
            return 'diciembre'
        return 'enero'

    def _mes_numero_full(self, month):
        if month == 1:
            return 'enero'
        if month == 2:
            return 'febrero'
        if month == 3:
            return 'marzo'
        if month == 4:
            return 'abril'
        if month == 5:
            return 'mayo'
        if month == 6:
            return 'junio'
        if month == 7:
            return 'julio'
        if month == 8:
            return 'agosto'
        if month == 9:
            return 'septiembre'
        if month == 10:
            return 'octubre'
        if month == 11:
            return 'noviembre'
        if month == 12:
            return 'diciembre'
        return 'enero'

    sigla = fields.Char(string='Abbreviation', size=64, required=True)
    nombre = fields.Char(string='Name', size=64, required=False)
    codigo = fields.Char(string='Code', size=100, required=False)
    recurso_explotable = fields.Float('Exploitable resource Qe (hm³)', digits=(3, 3), required=False)
    transmisibilidad = fields.Integer('Transmissivity (m²/día)', required=False)
    ancho = fields.Float('Width of section (m)', digits=(3, 2), required=False)
    gradiente_hidraulico = fields.Float('Hydraulic gradient', digits=(3, 5), required=False)
    area = fields.Float('Area (km²)', digits=(3, 2), required=False)
    coeficiente_almacenamiento = fields.Float('Coefficient of storage', digits=(3, 4), required=False)
    coeficiente_almacenamiento_string = fields.Char(string='Coefficient of storage', size=100, required=False)

    # equipo_ids = fields.many2many('df.hc.rain.base.equipment', 'df_equipo_tramo', 'fk_tramo_id', 'fk_equipo_id',string='Pluviometers')
    equipo_ids = fields.Many2many('df.hc.rain.base.equipment', 'df_equipo_tramo', 'fk_tramo_id', 'fk_equipo_id',string='Pluviometers')
    # Este campo equipo_ids es de otro modulo que no se ha hecho todavía en ODOO 12

    promedio_h_periodo = fields.Float('Net reCharge', digits=(3, 3), required=False, readonly=True)
    minimo_h_periodo = fields.Float('Min', digits=(3, 3), required=False, readonly=True)
    maximo_h_periodo = fields.Float('Max', digits=(3, 3), required=False, readonly=True)
    promedio_h_periodo_formula = fields.Float('Net reCharge', digits=(3, 3), required=False, readonly=True)
    minimo_h_periodo_formula = fields.Float('Min', digits=(3, 3), required=False, readonly=True)
    maximo_h_periodo_formula = fields.Float('Max', digits=(3, 3), required=False, readonly=True)
    valor_precision = fields.Float('Precision value', digits=(3, 3), required=False,
                                   help="Put precision level value for detection algorithm,if precision is closer to 0 then algorithm take minnor level diference as an important change")
    a0 = fields.Float('A0', digits=(3, 3), required=False)
    a1 = fields.Float('A1', digits=(3, 3), required=False)
    cota_topografica = fields.Float('Elevation topography avg (m)', digits=(3, 3), required=False)
    promedio_h_periodo_fijo = fields.Float(string='Recarga neta', digits=(3, 3), required=False)
    minimo_h_periodo_fijo = fields.Float(string='Min', digits=(3, 3), required=False)
    maximo_h_periodo_fijo = fields.Float(string='Max', digits=(3, 3), required=False)
    coeficiente_aprovechamiento_hidraulico = fields.Float(string='Coefficient of hydraulic use', digits=(3, 3),
                                                          required=False)
    coeficiente_infiltracion = fields.Float(string='Coefficient infiltration', digits=(3, 3), required=False)
    coeficiente_almacenamiento_calculado = fields.Float('Coefficient of storage1', digits=(3, 3), required=False,
                                                        readonly=True)
    coeficiente_almacenamiento_calculado_formula = fields.Float('Coefficient of storage1', digits=(3, 3),
                                                                required=False, readonly=True)

    ##METODOS PARA CALCULO DE NIVELES PRONOSTICOS

    def calcular_delta_z(self, id, vol_exp):
        """delta_z = vol_explotacion/coeficiente_almacenamiento*area"""
        if vol_exp != None:
            obj = self.browse( [id])[0]
            if obj.coeficiente_almacenamiento != 0 and obj.area != 0:
                return round((vol_exp * 1000000) / (obj.coeficiente_almacenamiento * obj.area * 1000000), 5)
        return None

    def calcular_delta_z1(self, vol_exp, idd, tipo):
        """delta_z = vol_explotacion/coeficiente_almacenamiento*area"""
        val = None
        if tipo == 'sector':
            obj_cuenca = self.env['df.sector.hidrologico']
        if tipo == 'bloque':
            obj_cuenca = self.env['df.bloque']
        if vol_exp != None:
            idd = obj_cuenca.search([('id', '=', [self.id])]).id
            obj = obj_cuenca.browse(idd)[0]
            if obj.coeficiente_almacenamiento != 0 and obj.area != 0:
                val1 = (vol_exp * 1000000) / (obj.coeficiente_almacenamiento * obj.area * 1000000)
                val = round(val1, 2)
            else:
                  raise UserError(_('Debe entrar el área y el coeficiente de almacenamiento de la cuenca seleccionada.'))
            #     raise osv.except_osv(_('Advertencia'), _(
            #         'Debe entrar el área y el coeficiente de almacenamiento de la cuanca seleccionada.'))
        return val

    def calcular_vol_probable(self, id, lluvias_del_mes):
        """
            calculo de delta_z = lluvia * coeficiente_infiltracion * area

        :param cr:
        :param uid:
        :param id: id del pozo
        :param lluvias_del_mes: diccionario con los valores a los diferentes porcientos
        :param context:
        :return: diccionario con los vol probables a los diferentes porcientos
        """
        res = {}
        obj = self.browse( [id])[0]
        if lluvias_del_mes['50'] != None:
            res['50'] = (float(lluvias_del_mes['50']) / 1000) * obj.coeficiente_infiltracion * obj.area * 1000000
        else:
            res['50'] = None
        if lluvias_del_mes['75'] != None:
            res['75'] = (float(lluvias_del_mes['75']) / 1000) * obj.coeficiente_infiltracion * obj.area * 1000000
        else:
            res['75'] = None
        if lluvias_del_mes['95'] != None:
            res['95'] = (float(lluvias_del_mes['95']) / 1000) * obj.coeficiente_infiltracion * obj.area * 1000000
        else:
            res['95'] = None
        return res

    def calcular_delta_h(self, id, mes, anno, lluvias_del_mes):
        """delta_h_% = vol_probable_%/coeficiente_almacenamiento*area"""

        res = {}
        obj = self.browse( [id])[0]
        vol_probables = self.calcular_vol_probable( id, lluvias_del_mes)
        if vol_probables['50'] != None and obj.coeficiente_almacenamiento != 0 and obj.area != 0:
            res['50'] = float(vol_probables['50']) / (obj.coeficiente_almacenamiento * obj.area * 1000000)
        else:
            res['50'] = None
        if vol_probables['75'] != None and obj.coeficiente_almacenamiento != 0 and obj.area != 0:
            res['75'] = float(vol_probables['75']) / (obj.coeficiente_almacenamiento * obj.area * 1000000)
        else:
            res['75'] = None
        if vol_probables['95'] != None and obj.coeficiente_almacenamiento != 0 and obj.area != 0:
            res['95'] = float(vol_probables['95']) / (obj.coeficiente_almacenamiento * obj.area * 1000000)
        else:
            res['95'] = None
        return res

    def calcular_niveles_pronosticos_mes(self, id, nivel_inicial_porcientos, vol_exp, mes, anno,
                                         lluvias_del_mes):
        """
            calculo de nivel_pronostico_% = nivel_inicial - (delta_h_% - delta_z/delta_tiempo)

        :param nivel_inicial_porcientos: valores numericos obligatorios
        :param lluvias_del_mes: diccionario con los valores a los diferentes porcientos,
               EJEMPLO: {'50': 26.7, '75': None, '95': 25.59}
        :param cr:
        :param uid:
        :param id:
        :param mes:
        :param anno:
        :param pozo_ids:
        :param context:
        :return: diccionario con los niveles pronosticos a los diferentes porcientos para un mes
        """
        res = {}
        delta_h = self.calcular_delta_h(id, mes, anno, lluvias_del_mes)
        # delta_z = self.calcular_delta_z( mes, anno)
        delta_z = self.calcular_delta_z(id, vol_exp)
        if nivel_inicial_porcientos['50'] and delta_h['50'] and delta_z:
            res['50'] = round(nivel_inicial_porcientos['50'] - (delta_h['50'] - delta_z), 2)
        else:
            res['50'] = None
        if nivel_inicial_porcientos['75'] and delta_h['75'] and delta_z:
            res['75'] = round(nivel_inicial_porcientos['75'] - (delta_h['75'] - delta_z), 2)
        else:
            res['75'] = None
        if nivel_inicial_porcientos['95'] and delta_h['95'] and delta_z:
            res['95'] = round(nivel_inicial_porcientos['95'] - (delta_h['95'] - delta_z), 2)
        else:
            res['95'] = None
        return res

    def calcular_nivel_lluvia_real(self, id, nreal, vol_exp_de_meses, anno, pozo_ids, metodo):
        res = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
        # obj_pozo = self.pool.get('df.pozo')
        # pozo_ids = obj_pozo.search(cr, uid, [('id', '=', id)])
        # pozo_objeto = obj_pozo.browse(cr, uid, pozo_ids)[0]
        obj = self.browse( [id])[0]
        nivel_real5 = self.calcular_nivel_real( id, 5, anno, pozo_ids, metodo)
        if (obj.coeficiente_infiltracion != 0 and obj.area != 0 and obj.coeficiente_almacenamiento != 0):
            if (nreal.get('5') and nreal['5'] != None and nivel_real5 != None and vol_exp_de_meses['5'] != None):
                volumen5 = ((float(nreal['5']) / 1000) * obj.coeficiente_infiltracion * obj.area * 1000000) / (
                        obj.coeficiente_almacenamiento * obj.area * 1000000)
                delta_z = self.calcular_delta_z( id, vol_exp_de_meses['5'])
                nivel_real_lluvia = nivel_real5 - (volumen5 - delta_z)
                res['5'] = round(nivel_real_lluvia, 2)
            else:
                res['5'] = None
            nivel_real6 = self.calcular_nivel_real( id, 6, anno, pozo_ids, metodo)
            if (nreal.get('6') and nreal['6'] != None and nivel_real6 != None and vol_exp_de_meses['6'] != None):
                volumen6 = ((float(nreal['6']) / 1000) * obj.coeficiente_infiltracion * obj.area * 1000000) / (
                        obj.coeficiente_almacenamiento * obj.area * 1000000)
                delta_z = self.calcular_delta_z( id, vol_exp_de_meses['6'])
                nivel_real_lluvia = nivel_real6 - (volumen6 - delta_z)
                res['6'] = round(nivel_real_lluvia, 2)
            else:
                res['6'] = None
            nivel_real7 = self.calcular_nivel_real( id, 7, anno, pozo_ids, metodo)
            if (nreal.get('7') and nreal['7'] != None and nivel_real7 != None and vol_exp_de_meses['7'] != None):
                volumen7 = ((float(nreal['7']) / 1000) * obj.coeficiente_infiltracion * obj.area * 1000000) / (
                        obj.coeficiente_almacenamiento * obj.area * 1000000)
                delta_z = self.calcular_delta_z( id, vol_exp_de_meses['7'])
                nivel_real_lluvia = nivel_real7 - (volumen7 - delta_z)
                res['7'] = round(nivel_real_lluvia, 2)
            else:
                res['7'] = None
            nivel_real8 = self.calcular_nivel_real( id, 8, anno, pozo_ids, metodo)
            if (nreal.get('8') and nreal['8'] != None and nivel_real8 != None and vol_exp_de_meses['8'] != None):
                volumen8 = ((float(nreal['8']) / 1000) * obj.coeficiente_infiltracion * obj.area * 1000000) / (
                        obj.coeficiente_almacenamiento * obj.area * 1000000)
                delta_z = self.calcular_delta_z( id, vol_exp_de_meses['8'])
                nivel_real_lluvia = nivel_real8 - (volumen8 - delta_z)
                res['8'] = round(nivel_real_lluvia, 2)
            else:
                res['8'] = None
            nivel_real9 = self.calcular_nivel_real( id, 9, anno, pozo_ids, metodo)
            if (nreal.get('9') and nreal['9'] != None and nivel_real9 != None and vol_exp_de_meses['9'] != None):
                volumen9 = ((float(nreal['9']) / 1000) * obj.coeficiente_infiltracion * obj.area * 1000000) / (
                        obj.coeficiente_almacenamiento * obj.area * 1000000)
                delta_z = self.calcular_delta_z( id, vol_exp_de_meses['9'])
                nivel_real_lluvia = nivel_real9 - (volumen9 - delta_z)
                res['9'] = round(nivel_real_lluvia, 2)
            else:
                res['9'] = None
            nivel_real10 = self.calcular_nivel_real( id, 10, anno, pozo_ids, metodo)
            if (nreal.get('10') and nreal['10'] != None and nivel_real10 != None and vol_exp_de_meses[
                '10'] != None):
                volumen10 = ((float(nreal['10']) / 1000) * obj.coeficiente_infiltracion * obj.area * 1000000) / (
                        obj.coeficiente_almacenamiento * obj.area * 1000000)
                delta_z = self.calcular_delta_z( id, vol_exp_de_meses['10'])
                nivel_real_lluvia = nivel_real10 - (volumen10 - delta_z)
                res['10'] = round(nivel_real_lluvia, 2)
                nreal
            else:
                res['10'] = None
        return res

    def calcular_explotacion_plan(self, id, anno, tipo):
        explotacion = None
        if tipo == 'bloque':
            string_objeto_id = 'bloque_id'
            # obj = self.pool.get('df.bloque')
            obj_plan_explotacion = self.env['df.explotacion.bloque.plan']
        elif tipo == 'sector':
            string_objeto_id = 'sector_id'
            # obj = self.pool.get('df.sector.hidrologico')
            obj_plan_explotacion = self.env['df.explotacion.sector.plan']
        res = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
        # obj_plan_explotacion = self.pool.get('df.plan.explotacion.anual.pozo')
        # obj = self.browse(cr, uid, [id])[0]
        explotacion_anual_ids = obj_plan_explotacion.search([('anno', '=', anno), (string_objeto_id, '=', id)]).ids
        if explotacion_anual_ids:
            explotacion_anual = obj_plan_explotacion.browse( explotacion_anual_ids)[0]
            if explotacion_anual.media_hiperanual_mayo != -999999.11:
                res['5'] = explotacion_anual.media_hiperanual_mayo
            if explotacion_anual.media_hiperanual_junio != -999999.11:
                res['6'] = explotacion_anual.media_hiperanual_junio
            if explotacion_anual.media_hiperanual_julio != -999999.11:
                res['7'] = explotacion_anual.media_hiperanual_julio
            if explotacion_anual.media_hiperanual_agosto != -999999.11:
                res['8'] = explotacion_anual.media_hiperanual_agosto
            if explotacion_anual.media_hiperanual_septiembre != -999999.11:
                res['9'] = explotacion_anual.media_hiperanual_septiembre
            if explotacion_anual.media_hiperanual_octubre != -999999.11:
                res['10'] = explotacion_anual.media_hiperanual_octubre
            return res
        else:
             raise UserError(_('Debe de existir la explotación del elemento para el año seleccionado!'))
             # raise osv.except_osv(_('Advertencia'),
             #                      _('Debe de existir la explotación del elemento para el año seleccionado!'))

    def calcular_probabilidad(self, id, tipo):
        if tipo == 'bloque':
            string_objeto_id = 'bloque_id'
            # obj = self.pool.get('df.bloque')
            obj_plan_explotacion = self.env['df.probabilidad.bloque']
            tabla_agrupamiento = 'df_probabilidad_bloque'
            sql = """ select anno
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                          where tabla_objeto.bloque_id = '""" + str(id) + """'
                          ORDER BY anno DESC;"""
        elif tipo == 'sector':
            string_objeto_id = 'sector_id'
            # obj = self.pool.get('df.sector.hidrologico')
            obj_plan_explotacion = self.env['df.probabilidad.sector']
            tabla_agrupamiento = 'df_probabilidad_sector'
            sql = """ select anno
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                          where tabla_objeto.sector_id = '""" + str(id) + """'
                          ORDER BY anno DESC;"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.dictfetchall()

        res = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
        lluvia = {'50': None, '75': None, '95': None}
        obj_probabilidad = self.pool.get('df.probabilidad.pozo')
        obj = self.browse( [id])[0]
        probabilidad_ids_50 = []
        probabilidad_ids_75 = []
        probabilidad_ids_95 = []
        if datos_vistas:
            anno = datos_vistas[0]['anno']
            probabilidad_ids_50 = obj_plan_explotacion.search( [('probabilidad', '=', '50%'),
                                                                             (string_objeto_id, '=', id),
                                                                             ('anno', '=', anno)]).ids
            probabilidad_ids_75 = obj_plan_explotacion.search( [('probabilidad', '=', '75%'),
                                                                             (string_objeto_id, '=', id),
                                                                             ('anno', '=', anno)]).ids
            probabilidad_ids_95 = obj_plan_explotacion.search( [('probabilidad', '=', '95%'),
                                                                             (string_objeto_id, '=', id),
                                                                             ('anno', '=', anno)]).ids
        if probabilidad_ids_50 and probabilidad_ids_75 and probabilidad_ids_95:
            probabilidad_50 = obj_plan_explotacion.browse( probabilidad_ids_50)[0]
            probabilidad_75 = obj_plan_explotacion.browse( probabilidad_ids_75)[0]
            probabilidad_95 = obj_plan_explotacion.browse( probabilidad_ids_95)[0]
            lluvia['50'] = probabilidad_50.media_hiperanual_mayo
            lluvia['75'] = probabilidad_75.media_hiperanual_mayo
            lluvia['95'] = probabilidad_95.media_hiperanual_mayo
            res['5'] = lluvia
            lluvia = {'50': None, '75': None, '95': None}
            lluvia['50'] = probabilidad_50.media_hiperanual_junio
            lluvia['75'] = probabilidad_75.media_hiperanual_junio
            lluvia['95'] = probabilidad_95.media_hiperanual_junio
            res['6'] = lluvia
            lluvia = {'50': None, '75': None, '95': None}
            lluvia['50'] = probabilidad_50.media_hiperanual_julio
            lluvia['75'] = probabilidad_75.media_hiperanual_julio
            lluvia['95'] = probabilidad_95.media_hiperanual_julio
            res['7'] = lluvia
            lluvia = {'50': None, '75': None, '95': None}
            lluvia['50'] = probabilidad_50.media_hiperanual_agosto
            lluvia['75'] = probabilidad_75.media_hiperanual_agosto
            lluvia['95'] = probabilidad_95.media_hiperanual_agosto
            res['8'] = lluvia
            lluvia = {'50': None, '75': None, '95': None}
            lluvia['50'] = probabilidad_50.media_hiperanual_septiembre
            lluvia['75'] = probabilidad_75.media_hiperanual_septiembre
            lluvia['95'] = probabilidad_95.media_hiperanual_septiembre
            res['9'] = lluvia
            lluvia = {'50': None, '75': None, '95': None}
            lluvia['50'] = probabilidad_50.media_hiperanual_octubre
            lluvia['75'] = probabilidad_75.media_hiperanual_octubre
            lluvia['95'] = probabilidad_95.media_hiperanual_octubre
            res['10'] = lluvia
            return res
        else:
            raise UserError(_('Debe de existir la probabilidad del 50%,75% y 95% para el elemento seleccionado!'))
        #     raise osv.except_osv(_('Advertencia'),
        #                          _('Debe de existir la probabilidad del 50%,75% y 95% para el elemento seleccionado!'))

    def formar_diccionario(self, id, anno, tipo):
        if tipo == 'bloque':
            string_objeto_id = 'bloque_id'
            # obj = self.pool.get('df.bloque')
            obj_lluvia_real = self.env['df.lluvia.real.bloque']
        elif tipo == 'sector':
            string_objeto_id = 'sector_id'
            # obj = self.pool.get('df.sector.hidrologico')
            obj_lluvia_real = self.env['df.lluvia.real.sector']
        # lluvia_real_obj = self.pool.get('df.lluvia.real.pozo')
        lluvia_real_ids = obj_lluvia_real.search( [(string_objeto_id, '=', id), ('anno', '=', anno)]).ids
        nreal = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
        if lluvia_real_ids:
            lluvia_real_meses = obj_lluvia_real.browse( lluvia_real_ids)
            if lluvia_real_meses[0].media_hiperanual_mayo != 0.0:
                nreal['5'] = lluvia_real_meses[0].media_hiperanual_mayo
            else:
                nreal['5'] = None
            if lluvia_real_meses[0].media_hiperanual_junio != 0.0:
                nreal['6'] = lluvia_real_meses[0].media_hiperanual_junio
            else:
                nreal['6'] = None
            if lluvia_real_meses[0].media_hiperanual_julio != 0.0:
                nreal['7'] = lluvia_real_meses[0].media_hiperanual_julio
            else:
                nreal['7'] = None
            if lluvia_real_meses[0].media_hiperanual_agosto != 0.0:
                nreal['8'] = lluvia_real_meses[0].media_hiperanual_agosto
            else:
                nreal['8'] = None
            if lluvia_real_meses[0].media_hiperanual_septiembre != 0.0:
                nreal['9'] = lluvia_real_meses[0].media_hiperanual_septiembre
            else:
                nreal['9'] = None
            if lluvia_real_meses[0].media_hiperanual_octubre != 0.0:
                nreal['10'] = lluvia_real_meses[0].media_hiperanual_octubre
            else:
                nreal['10'] = None
        return nreal

    @api.model
    def calcular_niveles_pronosticos_reales(self, id, anno1, nreal, pronostico, tipo, metodo, pozo_ids=None):
        """ SEGUN SE LLENAN LOS REALES SE UTILIZA ESE VALOR EN EL MES CORRESPONDIENTE

            calculo de nivel_pronostico_% = nivel_inicial - (delta_h_% - delta_z/delta_tiempo)

        :param vol_exp_de_meses: diccionario con los vol_exp de los meses mayo-octubre
               EJEMPLO: {'5': 26.7, '6': None, '7': 25.59, '8': 26.7, '9': None, '10': 25.59}
        :param lluvias_de_meses: diccionario con las lluvias a los diferentes porcientos para los meses mayo-octubre
                EJEMPLO: {'5': {'50': 26.7, '75': None, '95': 25.59}, '6': {'50': 26.7, '75': None, '95': 25.59}, '7': {'50': 26.7, '75': None, '95': 25.59},
                '8': {'50': 26.7, '75': None, '95': 25.59}, '9': {'50': 26.7, '75': None, '95': 25.59}, '10': {'50': 26.7, '75': None, '95': 25.59}}
        :param nivel_inicial: valor numerico obligatorio
        :param lluvias_del_mes: diccionario con los valores a los diferentes porcientos,
               EJEMPLO: {'50': 26.7, '75': None, '95': 25.59}
        :param cr:
        :param uid:
        :param id:
        :param anno:
        :param pozo_ids:
        :param context:
        :return: diccionario con los niveles pronosticos a los diferentes porcientos para los meses mayo-octubre
        """
        res = [None, None, None, None, None, None]
        fecha_str = time.strftime('%Y%m')
        fecha_actual = int(fecha_str)
        vol_exp_de_meses = self.calcular_explotacion_plan( id, anno1, tipo)
        lluvias_de_meses = self.calcular_probabilidad( id, tipo)
        nivel_abril = self.calcular_nivel_real( id, 4, anno1, pozo_ids, metodo)
        nreal = self.formar_diccionario( id, anno1, tipo)
        nivel_lluvia_real = self.calcular_nivel_lluvia_real( id, nreal, vol_exp_de_meses, anno1, pozo_ids,
                                                            metodo)
        nivel_inicial_porcientos = {'50': nivel_abril, '75': nivel_abril, '95': nivel_abril}
        if nivel_abril:
            nivel_mayo = self.calcular_nivel_real( id, 5, anno1, pozo_ids, metodo)
            anno = int(anno1)
            date = datetime.datetime(anno, 5, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes5 = int(date_substr[0])
            if (nivel_mayo or nivel_abril != None) and pronostico != 'puro':
                if fecha_mes5 > fecha_actual:
                    nivel_pron_mayo = self.calcular_niveles_pronosticos_mes( id, nivel_inicial_porcientos,
                                                                            vol_exp_de_meses['5'], 5, anno,
                                                                            lluvias_de_meses['5'])
                else:
                    nivel_pron_mayo = {'50': None, '75': None, '95': None}
            else:
                nivel_pron_mayo = self.calcular_niveles_pronosticos_mes( id, nivel_inicial_porcientos,
                                                                        vol_exp_de_meses['5'], 5, anno,
                                                                        lluvias_de_meses['5'])
            res[0] = nivel_pron_mayo
            # anno=anno
            date = datetime.datetime(anno, 6, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes6 = int(date_substr[0])
            nivel_junio = self.calcular_nivel_real( id, 6, anno, pozo_ids, metodo)
            if (nivel_junio or nivel_mayo != None) and pronostico != 'puro':
                if fecha_mes6 > fecha_actual:
                    nivel_pron_mayo = {'50': nivel_mayo, '75': nivel_mayo, '95': nivel_mayo}
                    nivel_pron_junio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_mayo,
                                                                             vol_exp_de_meses['6'], 6, anno,
                                                                             lluvias_de_meses['6'])
                else:
                    nivel_pron_junio = {'50': None, '75': None, '95': None}
            elif nivel_pron_mayo:
                nivel_pron_junio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_mayo,
                                                                         vol_exp_de_meses['6'], 6, anno,
                                                                         lluvias_de_meses['6'])
            res[1] = nivel_pron_junio
            # anno=anno
            date = datetime.datetime(anno, 7, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes7 = int(date_substr[0])
            nivel_julio = self.calcular_nivel_real( id, 7, anno, pozo_ids, metodo)
            if (nivel_julio or nivel_junio != None) and pronostico != 'puro':
                if fecha_mes7 > fecha_actual:
                    nivel_pron_junio = {'50': nivel_junio, '75': nivel_junio, '95': nivel_junio}
                    nivel_pron_julio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_junio,
                                                                             vol_exp_de_meses['7'], 7, anno,
                                                                             lluvias_de_meses['7'])
                else:
                    nivel_pron_julio = {'50': None, '75': None, '95': None}
            elif nivel_pron_junio:
                nivel_pron_julio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_junio,
                                                                         vol_exp_de_meses['7'], 7, anno,
                                                                         lluvias_de_meses['7'])
            res[2] = nivel_pron_julio
            # anno=anno
            date = datetime.datetime(anno, 8, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes8 = int(date_substr[0])
            nivel_agosto = self.calcular_nivel_real( id, 8, anno, pozo_ids, metodo)
            if (nivel_agosto or nivel_julio != None) and pronostico != 'puro':
                if fecha_mes8 > fecha_actual:
                    nivel_pron_julio = {'50': nivel_julio, '75': nivel_julio, '95': nivel_julio}
                    nivel_pron_agosto = self.calcular_niveles_pronosticos_mes( id, nivel_pron_julio,
                                                                              vol_exp_de_meses['8'], 8, anno,
                                                                              lluvias_de_meses['8'])
                else:
                    nivel_pron_agosto = {'50': None, '75': None, '95': None}
            elif nivel_pron_julio:
                nivel_pron_agosto = self.calcular_niveles_pronosticos_mes( id, nivel_pron_julio,
                                                                          vol_exp_de_meses['8'], 8, anno,
                                                                          lluvias_de_meses['8'])
            res[3] = nivel_pron_agosto
            # anno=anno
            date = datetime.datetime(anno, 9, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes9 = int(date_substr[0])
            nivel_septiembre = self.calcular_nivel_real( id, 9, anno, pozo_ids, metodo)
            if (nivel_septiembre or nivel_agosto != None) and pronostico != 'puro':
                if fecha_mes9 > fecha_actual:
                    nivel_pron_agosto = {'50': nivel_agosto, '75': nivel_agosto, '95': nivel_agosto}
                    nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes( id, nivel_pron_agosto,
                                                                                  vol_exp_de_meses['9'], 9, anno,
                                                                                  lluvias_de_meses['9'])
                else:
                    nivel_pron_septiembre = {'50': None, '75': None, '95': None}
            elif nivel_pron_agosto:
                nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes( id, nivel_pron_agosto,
                                                                              vol_exp_de_meses['9'], 9, anno,
                                                                              lluvias_de_meses['9'])
            res[4] = nivel_pron_septiembre
            # anno=anno
            date = datetime.datetime(anno, 10, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes10 = int(date_substr[0])
            nivel_octubre = self.calcular_nivel_real( id, 10, anno, pozo_ids, metodo)
            if (nivel_octubre or nivel_septiembre != None) and pronostico != 'puro':
                if fecha_mes10 > fecha_actual:
                    nivel_pron_septiembre = {'50': nivel_septiembre, '75': nivel_septiembre, '95': nivel_septiembre}
                    nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( id, nivel_pron_septiembre,
                                                                               vol_exp_de_meses['10'], 10, anno,
                                                                               lluvias_de_meses['10'])
                else:
                    nivel_pron_octubre = {'50': None, '75': None, '95': None}
            elif nivel_pron_septiembre:
                nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( id, nivel_pron_septiembre,
                                                                           vol_exp_de_meses['10'], 10, anno,
                                                                           lluvias_de_meses['10'])
            res[5] = nivel_pron_octubre
        else:
             raise UserError(_('Nivel de abril debe de existir para iniciar el pronóstico!'))
             #raise osv.except_osv(_('Advertencia'), _('Nivel de abril debe de existir para iniciar el pronóstico!'))
        obj = self.browse( [id])[0]
        result = {
            'year': anno,
            'z': self.calcular_delta_z( id, vol_exp_de_meses['5']),
            'sigla': obj.sigla,
            'object': '',
            'categoryAxis': [],
            'yAxis': [{'minimo': 0, 'maximo': 1000, 'promedio_h_historico': 0}],
            'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 1000}],
            'series': [
                {'name': 'Nivel medido',
                 'data': [('May', self.calcular_nivel_real( id, 5, anno, pozo_ids, metodo)),
                          ('Jun', self.calcular_nivel_real( id, 6, anno, pozo_ids, metodo)),
                          ('Jul', self.calcular_nivel_real( id, 7, anno, pozo_ids, metodo)),
                          ('Agto', self.calcular_nivel_real( id, 8, anno, pozo_ids, metodo)),
                          ('Sep', self.calcular_nivel_real( id, 9, anno, pozo_ids, metodo)),
                          ('Oct', self.calcular_nivel_real( id, 10, anno, pozo_ids, metodo))]},
                {'name': 'Nivel lluvia real', 'data': [('May', nivel_lluvia_real['5']), ('Jun', nivel_lluvia_real['6']),
                                                       ('Jul', nivel_lluvia_real['7']), ('Ago', nivel_lluvia_real['8']),
                                                       ('Sep', nivel_lluvia_real['9']),
                                                       ('Oct', nivel_lluvia_real['10'])]},
                # {'name': 'Nivel lluvia real', 'data': [('May',nreal['5']),('Jun',nreal['6']),('Jul',nreal['7']),('Ago',nreal['8']),('Sep',nreal['9']),('Oct',nreal['10'])]},
                {'name': 'Nivel lluvia 50%',
                 'data': [('May', res[0]['50']), ('Jun', res[1]['50']), ('Jul', res[2]['50']), ('Ago', res[3]['50']),
                          ('Sep', res[4]['50']), ('Oct', res[5]['50'])]},
                {'name': 'Nivel lluvia 75%',
                 'data': [('May', res[0]['75']), ('Jun', res[1]['75']), ('Jul', res[2]['75']), ('Ago', res[3]['75']),
                          ('Sep', res[4]['75']), ('Oct', res[5]['75'])]},
                {'name': 'Nivel lluvia 95%',
                 'data': [('May', res[0]['95']), ('Jun', res[1]['95']), ('Jul', res[2]['95']), ('Ago', res[3]['95']),
                          ('Sep', res[4]['95']), ('Oct', res[5]['95'])]},
            ]}
        return result

    def calcular_niveles_pronosticos_realesUnion(self, idd, anno1, vol_exp_de_meses, nreal, pronostico,
                                                 tipo, lluvias_de_meses, nivel_abril, metodo, cont, meses1,
                                                 pozo_ids=None):

        res = [None, None, None, None, None, None]

        # nivel_abril = self.calcular_nivel_real(cr, uid, idd, 4, anno, pozo_ids)
        fecha_str = time.strftime('%Y%m')
        fecha_actual = int(fecha_str)
        nreal = self.formar_diccionario( idd, anno1, tipo)
        nivel_lluvia_real = self.calcular_nivel_lluvia_real( idd, nreal, vol_exp_de_meses, anno1, pozo_ids,
                                                            metodo)
        nivel_inicial_porcientos = {'50': nivel_abril, '75': nivel_abril, '95': nivel_abril}
        if nivel_abril:
            nivel_mayo = self.calcular_nivel_real( idd, 5, anno1, pozo_ids, metodo)
            anno = anno1
            date = datetime.datetime(anno, 5, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes5 = int(date_substr[0])
            if (nivel_mayo or nivel_abril != None) and pronostico != 'puro':
                # if fecha_mes5 > fecha_actual:
                nivel_pron_mayo = self.calcular_niveles_pronosticos_mes( idd, nivel_inicial_porcientos,
                                                                        vol_exp_de_meses['5'], 5, anno,
                                                                        lluvias_de_meses['5'])
            # else:
            #     nivel_pron_mayo = {'50': None, '75': None, '95': None}
            else:
                nivel_pron_mayo = self.calcular_niveles_pronosticos_mes( idd, nivel_inicial_porcientos,
                                                                        vol_exp_de_meses['5'], 5, anno,
                                                                        lluvias_de_meses['5'])
            res[0] = nivel_pron_mayo
            # anno=anno
            date = datetime.datetime(anno, 6, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes6 = int(date_substr[0])
            nivel_junio = self.calcular_nivel_real( idd, 6, anno, pozo_ids, metodo)
            if (nivel_junio or nivel_mayo != None) and pronostico != 'puro':
                # if fecha_mes6 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 5:
                    nivel_pron_mayo = {'50': nivel_mayo, '75': nivel_mayo, '95': nivel_mayo}
                nivel_pron_junio = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_mayo,
                                                                         vol_exp_de_meses['6'], 6, anno,
                                                                         lluvias_de_meses['6'])
                # else:
                #     nivel_pron_junio = {'50': None, '75': None, '95': None}
            elif nivel_pron_mayo:
                nivel_pron_junio = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_mayo,
                                                                         vol_exp_de_meses['6'], 6, anno,
                                                                         lluvias_de_meses['6'])
            res[1] = nivel_pron_junio
            # anno=anno
            date = datetime.datetime(anno, 7, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes7 = int(date_substr[0])
            nivel_julio = self.calcular_nivel_real( idd, 7, anno, pozo_ids, metodo)
            if (nivel_julio or nivel_junio != None) and pronostico != 'puro':
                # if fecha_mes7 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 6:
                    nivel_pron_junio = {'50': nivel_junio, '75': nivel_junio, '95': nivel_junio}
                #     nivel_pron_junio = {'50': nivel_junio, '75': nivel_junio, '95': nivel_junio}
                nivel_pron_julio = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_junio,
                                                                         vol_exp_de_meses['7'], 7, anno,
                                                                         lluvias_de_meses['7'])
                # else:
                #     nivel_pron_julio = {'50': None, '75': None, '95': None}
            elif nivel_pron_junio:
                nivel_pron_julio = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_junio,
                                                                         vol_exp_de_meses['7'], 7, anno,
                                                                         lluvias_de_meses['7'])
            res[2] = nivel_pron_julio
            # anno=anno
            date = datetime.datetime(anno, 8, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes8 = int(date_substr[0])
            nivel_agosto = self.calcular_nivel_real( idd, 8, anno, pozo_ids, metodo)
            if (nivel_agosto or nivel_julio != None) and pronostico != 'puro':
                # if fecha_mes8 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 7:
                    nivel_pron_julio = {'50': nivel_julio, '75': nivel_julio, '95': nivel_julio}
                nivel_pron_agosto = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_julio,
                                                                          vol_exp_de_meses['8'], 8, anno,
                                                                          lluvias_de_meses['8'])
                # else:
                #     nivel_pron_agosto = {'50': None, '75': None, '95': None}
            elif nivel_pron_julio:
                nivel_pron_agosto = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_julio,
                                                                          vol_exp_de_meses['8'], 8, anno,
                                                                          lluvias_de_meses['8'])
            res[3] = nivel_pron_agosto
            # anno=anno
            date = datetime.datetime(anno, 9, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes9 = int(date_substr[0])
            nivel_septiembre = self.calcular_nivel_real( idd, 9, anno, pozo_ids, metodo)
            if (nivel_septiembre or nivel_agosto != None) and pronostico != 'puro':
                # if fecha_mes9 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 8:
                    nivel_pron_agosto = {'50': nivel_agosto, '75': nivel_agosto, '95': nivel_agosto}
                nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_agosto,
                                                                              vol_exp_de_meses['9'], 9, anno,
                                                                              lluvias_de_meses['9'])
                # else:
                #     nivel_pron_septiembre = {'50': None, '75': None, '95': None}
            elif nivel_pron_agosto:
                nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_agosto,
                                                                              vol_exp_de_meses['9'], 9, anno,
                                                                              lluvias_de_meses['9'])
            res[4] = nivel_pron_septiembre
            # anno=anno
            date = datetime.datetime(anno, 10, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes10 = int(date_substr[0])
            nivel_octubre = self.calcular_nivel_real( idd, 10, anno, pozo_ids, metodo)
            if (nivel_octubre or nivel_septiembre != None) and pronostico != 'puro':
                # if fecha_mes10 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 9:
                    nivel_pron_septiembre = {'50': nivel_septiembre, '75': nivel_septiembre, '95': nivel_septiembre}
                nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_septiembre,
                                                                           vol_exp_de_meses['10'], 10, anno,
                                                                           lluvias_de_meses['10'])
                # else:
                #     nivel_pron_octubre = {'50': None, '75': None, '95': None}
            elif nivel_pron_septiembre:
                nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_septiembre,
                                                                           vol_exp_de_meses['10'], 10, anno,
                                                                           lluvias_de_meses['10'])
            res[5] = nivel_pron_octubre
        else:
             raise UserError(_('Nivel de abril debe de existir para iniciar el pronóstico!'))
             #raise osv.except_osv(_('Advertencia'), _('Nivel de abril debe de existir para iniciar el pronóstico!'))
        obj = self.browse( [idd])[0]
        result = {
            'year': anno,
            'z': self.calcular_delta_z( idd, vol_exp_de_meses['5']),
            'sigla': obj.sigla,
            'object': '',
            'categoryAxis': [],
            'yAxis': [{'minimo': 0, 'maximo': 1000, 'promedio_h_historico': 0}],
            'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 1000}],
            'series': [
                {'name': 'Nivel medido',
                 'data': [('May', self.calcular_nivel_real( idd, 5, anno, pozo_ids, metodo)),
                          ('Jun', self.calcular_nivel_real( idd, 6, anno, pozo_ids, metodo)),
                          ('Jul', self.calcular_nivel_real( idd, 7, anno, pozo_ids, metodo)),
                          ('Agto', self.calcular_nivel_real( idd, 8, anno, pozo_ids, metodo)),
                          ('Sep', self.calcular_nivel_real( idd, 9, anno, pozo_ids, metodo)),
                          ('Oct', self.calcular_nivel_real( idd, 10, anno, pozo_ids, metodo))]},
                {'name': 'Nivel lluvia real', 'data': [('May', nivel_lluvia_real['5']), ('Jun', nivel_lluvia_real['6']),
                                                       ('Jul', nivel_lluvia_real['7']), ('Ago', nivel_lluvia_real['8']),
                                                       ('Sep', nivel_lluvia_real['9']),
                                                       ('Oct', nivel_lluvia_real['10'])]},
                # {'name': 'Nivel lluvia real', 'data': [('May',nreal['5']),('Jun',nreal['6']),('Jul',nreal['7']),('Ago',nreal['8']),('Sep',nreal['9']),('Oct',nreal['10'])]},
                {'name': 'Nivel lluvia 50%',
                 'data': [('May', res[0]['50']), ('Jun', res[1]['50']), ('Jul', res[2]['50']), ('Ago', res[3]['50']),
                          ('Sep', res[4]['50']), ('Oct', res[5]['50'])]},
                {'name': 'Nivel lluvia 75%',
                 'data': [('May', res[0]['75']), ('Jun', res[1]['75']), ('Jul', res[2]['75']), ('Ago', res[3]['75']),
                          ('Sep', res[4]['75']), ('Oct', res[5]['75'])]},
                {'name': 'Nivel lluvia 95%',
                 'data': [('May', res[0]['95']), ('Jun', res[1]['95']), ('Jul', res[2]['95']), ('Ago', res[3]['95']),
                          ('Sep', res[4]['95']), ('Oct', res[5]['95'])]},
            ]}
        return result

    def calcular_niveles_pronosticos_reales1(self, id, anno1, nreal, pronostico, abril, tipo, metodo, duracion,
                                             pozo_ids=None):
        """ SEGUN SE LLENAN LOS REALES SE UTILIZA ESE VALOR EN EL MES CORRESPONDIENTE

            calculo de nivel_pronostico_% = nivel_inicial - (delta_h_% - delta_z/delta_tiempo)

        :param vol_exp_de_meses: diccionario con los vol_exp de los meses mayo-octubre
               EJEMPLO: {'5': 26.7, '6': None, '7': 25.59, '8': 26.7, '9': None, '10': 25.59}
        :param lluvias_de_meses: diccionario con las lluvias a los diferentes porcientos para los meses mayo-octubre
                EJEMPLO: {'5': {'50': 26.7, '75': None, '95': 25.59}, '6': {'50': 26.7, '75': None, '95': 25.59}, '7': {'50': 26.7, '75': None, '95': 25.59},
                '8': {'50': 26.7, '75': None, '95': 25.59}, '9': {'50': 26.7, '75': None, '95': 25.59}, '10': {'50': 26.7, '75': None, '95': 25.59}}
        :param nivel_inicial: valor numerico obligatorio
        :param lluvias_del_mes: diccionario con los valores a los diferentes porcientos,
               EJEMPLO: {'50': 26.7, '75': None, '95': 25.59}
        :param cr:
        :param uid:
        :param id:
        :param anno:
        :param pozo_ids:
        :param context:
        :return: diccionario con los niveles pronosticos a los diferentes porcientos para los meses mayo-octubre
        """
        res = [None, None, None, None, None, None]
        cont = 0
        ok = False
        obj = self.browse( [id])[0]
        vol_exp_de_meses = self.calcular_explotacion_plan( id, anno1, tipo)
        result = {
            'year': anno1,
            'z': self.calcular_delta_z( id, vol_exp_de_meses['5']),
            'sigla': str(obj.sigla),
            'object': '',
            'categoryAxis': [],
            'yAxis': [{'minimo': 0, 'maximo': 1000, 'promedio_h_historico': 0}],
            'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 1000}],
            # 'series': [
            #     {'name': 'Nivel medido', 'data': [('May.'+str(anno),self.calcular_nivel_real(cr, uid, id, 5, anno)),('Jun.'+str(anno),self.calcular_nivel_real(cr, uid, id, 6, anno)),('Jul.'+str(anno),self.calcular_nivel_real(cr, uid, id, 7, anno)),('Agto.'+str(anno),self.calcular_nivel_real(cr, uid, id, 8, anno)),('Sep.'+str(anno),self.calcular_nivel_real(cr, uid, id, 9, anno)),('Oct.'+str(anno),self.calcular_nivel_real(cr, uid, id, 10, anno))]},
            #     {'name': 'Nivel lluvia real', 'data': [('May',nivel_lluvia_real['5']),('Jun',nivel_lluvia_real['6']),('Jul',nivel_lluvia_real['7']),('Ago',nivel_lluvia_real['8']),('Sep',nivel_lluvia_real['9']),('Oct',nivel_lluvia_real['10'])]},
            #     {'name': 'Nivel lluvia 50%', 'data': [('May',res[0]['50']),('Jun',res[1]['50']),('Jul',res[2]['50']),('Ago',res[3]['50']),('Sep',res[4]['50']),('Oct',res[5]['50'])]},
            #     {'name': 'Nivel lluvia 75%', 'data': [('May',res[0]['75']),('Jun',res[1]['75']),('Jul',res[2]['75']),('Ago',res[3]['75']),('Sep',res[4]['75']),('Oct',res[5]['75'])]},
            #     {'name': 'Nivel lluvia 95%', 'data': [('May',res[0]['95']),('Jun',res[1]['95']),('Jul',res[2]['95']),('Ago',res[3]['95']),('Sep',res[4]['95']),('Oct',res[5]['95'])]},
            # ],
            'series': [
                {'name': 'Nivel medido', 'data': []},
                {'name': 'Nivel lluvia real', 'data': []},
                {'name': 'Nivel lluvia 50%', 'data': []},  # 2
                {'name': 'Nivel lluvia 75%', 'data': []},  # 3
                {'name': 'Nivel lluvia 95%', 'data': []},  # 4
            ]
        }
        pozo_ids = pozo_ids[0][2]
        while cont < 2:
            if duracion == 'Y':
                if ok == True:
                    break
            fecha_str = time.strftime('%Y%m')
            fecha_actual = int(fecha_str)
            anno = anno1 + 1
            # pozo_ids = pozo_ids[0][2]
            lluvias_de_meses = self.calcular_probabilidad( id, tipo)
            nivel_abril = abril[0]
            nreal = self.formar_diccionario( id, anno, tipo)
            nivel_lluvia_real = self.calcular_nivel_lluvia_real( id, nreal, vol_exp_de_meses, anno,
                                                                pozo_ids,
                                                                metodo)
            nivel_inicial_porcientos = {'50': nivel_abril, '75': nivel_abril, '95': nivel_abril}
            if nivel_abril:
                nivel_mayo = self.calcular_nivel_real( id, 5, anno, pozo_ids, metodo)
                # anno=anno
                date = datetime.datetime(anno, 5, 1)
                fecha_parte = date.strftime("%Y%m %H:%M:%S")
                date_substr = fecha_parte.split()
                fecha_mes5 = int(date_substr[0])
                if (nivel_mayo or nivel_abril != None) and pronostico != 'puro':
                    if fecha_mes5 > fecha_actual:
                        nivel_pron_mayo = self.calcular_niveles_pronosticos_mes( id,
                                                                                nivel_inicial_porcientos,
                                                                                vol_exp_de_meses['5'], 5, anno,
                                                                                lluvias_de_meses['5'])
                    else:
                        nivel_pron_mayo = {'50': None, '75': None, '95': None}
                else:
                    nivel_pron_mayo = self.calcular_niveles_pronosticos_mes( id, nivel_inicial_porcientos,
                                                                            vol_exp_de_meses['5'], 5, anno,
                                                                            lluvias_de_meses['5'])
                res[0] = nivel_pron_mayo
                # anno=anno
                date = datetime.datetime(anno, 6, 1)
                fecha_parte = date.strftime("%Y%m %H:%M:%S")
                date_substr = fecha_parte.split()
                fecha_mes6 = int(date_substr[0])
                nivel_junio = self.calcular_nivel_real( id, 6, anno, pozo_ids, metodo)
                if (nivel_junio or nivel_mayo != None) and pronostico != 'puro':
                    if fecha_mes6 > fecha_actual:
                        nivel_pron_mayo = {'50': nivel_mayo, '75': nivel_mayo, '95': nivel_mayo}
                        nivel_pron_junio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_mayo,
                                                                                 vol_exp_de_meses['6'], 6, anno,
                                                                                 lluvias_de_meses['6'])
                    else:
                        nivel_pron_junio = {'50': None, '75': None, '95': None}
                elif nivel_pron_mayo:
                    nivel_pron_junio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_mayo,
                                                                             vol_exp_de_meses['6'], 6, anno,
                                                                             lluvias_de_meses['6'])
                res[1] = nivel_pron_junio
                # anno=anno
                date = datetime.datetime(anno, 7, 1)
                fecha_parte = date.strftime("%Y%m %H:%M:%S")
                date_substr = fecha_parte.split()
                fecha_mes7 = int(date_substr[0])
                nivel_julio = self.calcular_nivel_real( id, 7, anno, pozo_ids, metodo)
                if (nivel_julio or nivel_junio != None) and pronostico != 'puro':
                    if fecha_mes7 > fecha_actual:
                        nivel_pron_junio = {'50': nivel_junio, '75': nivel_junio, '95': nivel_junio}
                        nivel_pron_julio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_junio,
                                                                                 vol_exp_de_meses['7'], 7, anno,
                                                                                 lluvias_de_meses['7'])
                    else:
                        nivel_pron_julio = {'50': None, '75': None, '95': None}
                elif nivel_pron_junio:
                    nivel_pron_julio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_junio,
                                                                             vol_exp_de_meses['7'], 7, anno,
                                                                             lluvias_de_meses['7'])
                res[2] = nivel_pron_julio
                # anno=anno
                date = datetime.datetime(anno, 8, 1)
                fecha_parte = date.strftime("%Y%m %H:%M:%S")
                date_substr = fecha_parte.split()
                fecha_mes8 = int(date_substr[0])
                nivel_agosto = self.calcular_nivel_real( id, 8, anno, pozo_ids, metodo)
                if (nivel_agosto or nivel_julio != None) and pronostico != 'puro':
                    if fecha_mes8 > fecha_actual:
                        nivel_pron_julio = {'50': nivel_julio, '75': nivel_julio, '95': nivel_julio}
                        nivel_pron_agosto = self.calcular_niveles_pronosticos_mes( id, nivel_pron_julio,
                                                                                  vol_exp_de_meses['8'], 8, anno,
                                                                                  lluvias_de_meses['8'])
                    else:
                        nivel_pron_agosto = {'50': None, '75': None, '95': None}
                elif nivel_pron_julio:
                    nivel_pron_agosto = self.calcular_niveles_pronosticos_mes( id, nivel_pron_julio,
                                                                              vol_exp_de_meses['8'], 8, anno,
                                                                              lluvias_de_meses['8'])
                res[3] = nivel_pron_agosto
                # anno=anno
                date = datetime.datetime(anno, 9, 1)
                fecha_parte = date.strftime("%Y%m %H:%M:%S")
                date_substr = fecha_parte.split()
                fecha_mes9 = int(date_substr[0])
                nivel_septiembre = self.calcular_nivel_real( id, 9, anno, pozo_ids, metodo)
                if (nivel_septiembre or nivel_agosto != None) and pronostico != 'puro':
                    if fecha_mes9 > fecha_actual:
                        nivel_pron_agosto = {'50': nivel_agosto, '75': nivel_agosto, '95': nivel_agosto}
                        nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes( id,
                                                                                      nivel_pron_agosto,
                                                                                      vol_exp_de_meses['9'], 9, anno,
                                                                                      lluvias_de_meses['9'])
                    else:
                        nivel_pron_septiembre = {'50': None, '75': None, '95': None}
                elif nivel_pron_agosto:
                    nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes( id, nivel_pron_agosto,
                                                                                  vol_exp_de_meses['9'], 9, anno,
                                                                                  lluvias_de_meses['9'])
                res[4] = nivel_pron_septiembre
                # anno=anno
                date = datetime.datetime(anno, 10, 1)
                fecha_parte = date.strftime("%Y%m %H:%M:%S")
                date_substr = fecha_parte.split()
                fecha_mes10 = int(date_substr[0])
                nivel_octubre = self.calcular_nivel_real( id, 10, anno, pozo_ids, metodo)
                if (nivel_octubre or nivel_septiembre != None) and pronostico != 'puro':
                    if fecha_mes10 > fecha_actual:
                        nivel_pron_septiembre = {'50': nivel_septiembre, '75': nivel_septiembre, '95': nivel_septiembre}
                        nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( id,
                                                                                   nivel_pron_septiembre,
                                                                                   vol_exp_de_meses['10'], 10, anno,
                                                                                   lluvias_de_meses['10'])
                    else:
                        nivel_pron_octubre = {'50': None, '75': None, '95': None}
                elif nivel_pron_septiembre:
                    nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( id, nivel_pron_septiembre,
                                                                               vol_exp_de_meses['10'], 10, anno,
                                                                               lluvias_de_meses['10'])
                res[5] = nivel_pron_octubre
            else:
                 raise UserError(_('Nivel de abril debe de existir para iniciar el pronóstico!'))
                 #raise osv.except_osv(_('Advertencia'), _('Nivel de abril debe de existir para iniciar el pronóstico!'))
            # result = {
            #     'year': anno,
            #     'z': self.calcular_delta_z(cr, uid, id,  vol_exp_de_meses['5']),
            #     'sigla': obj.sigla,
            #     'object':'',
            #     'categoryAxis': [],
            #     'yAxis': [{'minimo':0,'maximo':1000,'promedio_h_historico':0}],
            #     'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 1000}],
            #     'series': [
            #         {'name': 'Nivel medido', 'data': [('May.'+str(anno),self.calcular_nivel_real(cr, uid, id, 5, anno, pozo_ids,metodo)),('Jun.'+str(anno),self.calcular_nivel_real(cr, uid, id, 6, anno, pozo_ids,metodo)),('Jul.'+str(anno),self.calcular_nivel_real(cr, uid, id, 7, anno, pozo_ids,metodo)),('Agto.'+str(anno),self.calcular_nivel_real(cr, uid, id, 8, anno, pozo_ids,metodo)),('Sep.'+str(anno),self.calcular_nivel_real(cr, uid, id, 9, anno, pozo_ids,metodo)),('Oct.'+str(anno),self.calcular_nivel_real(cr, uid, id, 10, anno, pozo_ids,metodo))]},
            #         {'name': 'Nivel lluvia real', 'data': [('May',nivel_lluvia_real['5']),('Jun',nivel_lluvia_real['6']),('Jul',nivel_lluvia_real['7']),('Ago',nivel_lluvia_real['8']),('Sep',nivel_lluvia_real['9']),('Oct',nivel_lluvia_real['10'])]},
            #         # {'name': 'Nivel lluvia real', 'data': [('May',nreal['5']),('Jun',nreal['6']),('Jul',nreal['7']),('Ago',nreal['8']),('Sep',nreal['9']),('Oct',nreal['10'])]},
            #         {'name': 'Nivel lluvia 50%', 'data': [('May',res[0]['50']),('Jun',res[1]['50']),('Jul',res[2]['50']),('Ago',res[3]['50']),('Sep',res[4]['50']),('Oct',res[5]['50'])]},
            #         {'name': 'Nivel lluvia 75%', 'data': [('May',res[0]['75']),('Jun',res[1]['75']),('Jul',res[2]['75']),('Ago',res[3]['75']),('Sep',res[4]['75']),('Oct',res[5]['75'])]},
            #         {'name': 'Nivel lluvia 95%', 'data': [('May',res[0]['95']),('Jun',res[1]['95']),('Jul',res[2]['95']),('Ago',res[3]['95']),('Sep',res[4]['95']),('Oct',res[5]['95'])]},
            #     ]}
            result['series'][0]['data'].append(
                ['May.' + str(anno), self.calcular_nivel_real( id, 5, anno, pozo_ids, metodo)])
            result['series'][0]['data'].append(
                ['Jun.' + str(anno), self.calcular_nivel_real( id, 6, anno, pozo_ids, metodo)])
            result['series'][0]['data'].append(
                ['Jul.' + str(anno), self.calcular_nivel_real( id, 7, anno, pozo_ids, metodo)])
            result['series'][0]['data'].append(
                ['Agto.' + str(anno), self.calcular_nivel_real( id, 8, anno, pozo_ids, metodo)])
            result['series'][0]['data'].append(
                ['Sep.' + str(anno), self.calcular_nivel_real( id, 9, anno, pozo_ids, metodo)])
            result['series'][0]['data'].append(
                ['Oct.' + str(anno), self.calcular_nivel_real( id, 10, anno, pozo_ids, metodo)])
            result['series'][1]['data'].append(['May', nivel_lluvia_real['5']])
            result['series'][1]['data'].append(['Jun', nivel_lluvia_real['6']])
            result['series'][1]['data'].append(['Jul', nivel_lluvia_real['7']])
            result['series'][1]['data'].append(['Agto', nivel_lluvia_real['8']])
            result['series'][1]['data'].append(['Sep', nivel_lluvia_real['9']])
            result['series'][1]['data'].append(['Oct', nivel_lluvia_real['10']])
            result['series'][2]['data'].append(['May', res[0]['50']])
            result['series'][2]['data'].append(['Jun', res[1]['50']])
            result['series'][2]['data'].append(['Jul', res[2]['50']])
            result['series'][2]['data'].append(['Agto', res[3]['50']])
            result['series'][2]['data'].append(['Sep', res[4]['50']])
            result['series'][2]['data'].append(['Oct', res[5]['50']])
            result['series'][3]['data'].append(['May', res[0]['75']])
            result['series'][3]['data'].append(['Jun', res[1]['75']])
            result['series'][3]['data'].append(['Jul', res[2]['75']])
            result['series'][3]['data'].append(['Agto', res[3]['75']])
            result['series'][3]['data'].append(['Sep', res[4]['75']])
            result['series'][3]['data'].append(['Oct', res[5]['75']])
            result['series'][4]['data'].append(['May', res[0]['95']])
            result['series'][4]['data'].append(['Jun', res[1]['95']])
            result['series'][4]['data'].append(['Jul', res[2]['95']])
            result['series'][4]['data'].append(['Agto', res[3]['95']])
            result['series'][4]['data'].append(['Sep', res[4]['95']])
            result['series'][4]['data'].append(['Oct', res[5]['95']])
            cont += 1
            ok = True
        return result

    @api.model
    def create(self, vals):
        if vals.get('coeficiente_almacenamiento', None):
            vals.update({'coeficiente_almacenamiento_string': str(vals['coeficiente_almacenamiento'])})
        return super(df_tramo, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('coeficiente_almacenamiento', None):
            vals.update({'coeficiente_almacenamiento_string': str(vals['coeficiente_almacenamiento'])})
        return super(df_tramo, self).write(vals)


class df_sector_hidrologico(models.Model):
    _name = 'df.sector.hidrologico'
    _inherit = 'df.tramo'
    _rec_name = 'sigla'
    _auto = True
    _description = "HC Hydrogeological sector"

    def _valores_rango_fechas(self, id, pozo_ids, anno):

        query = """SELECT
                          df_nivel_anual_pozo.anno,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_enero, -999999.110)) as total_enero,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_febrero, -999999.110)) as total_febrero,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_marzo, -999999.110)) as total_marzo,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_abril, -999999.110)) as total_abril,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_mayo, -999999.110)) as total_mayo,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_junio, -999999.110)) as total_junio,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_julio, -999999.110)) as total_julio,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_agosto, -999999.110)) as total_agosto,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_septiembre, -999999.110)) as total_septiembre,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_octubre, -999999.110)) as total_octubre,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_noviembre, -999999.110)) as total_noviembre,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_diciembre, -999999.110)) as total_diciembre,

                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_enero, -999999.110)) as cant_enero,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_febrero, -999999.110)) as cant_febrero,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_marzo, -999999.110)) as cant_marzo,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_abril, -999999.110)) as cant_abril,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_mayo, -999999.110)) as cant_mayo,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_junio, -999999.110)) as cant_junio,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_julio, -999999.110)) as cant_julio,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_agosto, -999999.110)) as cant_agosto,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_septiembre, -999999.110)) as cant_septiembre,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_octubre, -999999.110)) as cant_octubre,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_noviembre, -999999.110)) as cant_noviembre,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_diciembre, -999999.110)) as cant_diciembre
                        FROM
                          df_pozo,
                          df_sector_hidrologico, """

        bloque_obj = self.env['df.bloque']
        bloque_ids = bloque_obj.search( []).ids
        if bloque_ids:
            query += """df_bloque,
                          df_nivel_anual_pozo
                        WHERE
                          df_sector_hidrologico.id = %s AND
                          df_nivel_anual_pozo.pozo_id = df_pozo.id AND
                          ((df_pozo.bloque_id = df_bloque.id AND df_bloque.sector_id = df_sector_hidrologico.id) OR
                          df_pozo.sector_hidrologico_id = df_sector_hidrologico.id) AND """
        else:
            query += """df_nivel_anual_pozo
                        WHERE
                          df_sector_hidrologico.id = %s AND
                          df_nivel_anual_pozo.pozo_id = df_pozo.id AND
                          df_pozo.sector_hidrologico_id = df_sector_hidrologico.id AND """

        if pozo_ids:
            query += """df_pozo.id in %s AND
            df_nivel_anual_pozo.anno = %s
            GROUP BY df_sector_hidrologico.id, df_nivel_anual_pozo.anno"""
            self.env.cr.execute(query, (id, tuple(pozo_ids), anno))
        else:
            query += """df_nivel_anual_pozo.anno = %s
            GROUP BY df_sector_hidrologico.id, df_nivel_anual_pozo.anno"""
            self.env.cr.execute(query, (id, anno))
        return self.env.cr.dictfetchall()

    def _valores_sin_rango_fechas(self, id, pozo_ids):

        query = """SELECT
                          df_sector_hidrologico.id,
                          df_nivel_anual_pozo.anno,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_enero, -999999.110)) as media_enero,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_febrero, -999999.110)) as media_febrero,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_marzo, -999999.110)) as media_marzo,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_abril, -999999.110)) as media_abril,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_mayo, -999999.110)) as media_mayo,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_junio, -999999.110)) as media_junio,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_julio, -999999.110)) as media_julio,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_agosto, -999999.110)) as media_agosto,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_septiembre, -999999.110)) as media_septiembre,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_octubre, -999999.110)) as media_octubre,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_noviembre, -999999.110)) as media_noviembre,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_diciembre, -999999.110)) as media_diciembre
                        FROM
                          df_pozo,
                          df_sector_hidrologico, """

        bloque_obj = self.env['df.bloque']
        bloque_ids = bloque_obj.search( []).ids
        if bloque_ids:
            query += """df_bloque,
                          df_nivel_anual_pozo
                        WHERE
                          df_sector_hidrologico.id = %s AND
                          df_nivel_anual_pozo.pozo_id = df_pozo.id AND
                          ((df_pozo.bloque_id = df_bloque.id AND df_bloque.sector_id = df_sector_hidrologico.id) OR
                          df_pozo.sector_hidrologico_id = df_sector_hidrologico.id) """
        else:
            query += """df_nivel_anual_pozo
                        WHERE
                          df_sector_hidrologico.id = %s AND
                          df_nivel_anual_pozo.pozo_id = df_pozo.id AND
                          df_pozo.sector_hidrologico_id = df_sector_hidrologico.id """

        if pozo_ids:
            query += """AND df_pozo.id in %s
                GROUP BY df_sector_hidrologico.id, df_nivel_anual_pozo.anno"""
            self.env.cr.execute(query, (id, (tuple(pozo_ids))))
        else:
            query += """GROUP BY df_sector_hidrologico.id, df_nivel_anual_pozo.anno"""
            self.env.cr.execute(query, (id,))
        return self.env.cr.dictfetchall()

    def _calcular_media_sector_rango_fecha(self, ids, pozo_ids, fecha_inicio, fecha_fin):
        res = []
        anno_inicio = fecha_inicio.year
        anno_fin = fecha_fin.year
        mes_inicio = fecha_inicio.month
        mes_fin = fecha_fin.month
        for id in ids:
            current_year = fecha_inicio.year
            arreglo_sector = []
            while current_year <= anno_fin:
                datos = self._valores_rango_fechas( id, pozo_ids, current_year)
                dict_media = {}
                if datos:
                    if datos[0]['anno'] == anno_inicio:
                        if mes_inicio < 2:
                            if anno_inicio == anno_fin and mes_fin < 1:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_enero'] and datos[0]['cant_enero'] != 0:
                                dict_media['1'] = datos[0]['total_enero'] / datos[0]['cant_enero']
                        if mes_inicio < 3:
                            if anno_inicio == anno_fin and mes_fin < 2:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_febrero'] and datos[0]['cant_febrero'] != 0:
                                dict_media['2'] = datos[0]['total_febrero'] / datos[0]['cant_febrero']
                        if mes_inicio < 4:
                            if anno_inicio == anno_fin and mes_fin < 3:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_marzo'] and datos[0]['cant_marzo'] != 0:
                                dict_media['3'] = datos[0]['total_marzo'] / datos[0]['cant_marzo']
                        if mes_inicio < 5:
                            if anno_inicio == anno_fin and mes_fin < 4:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_abril'] and datos[0]['cant_abril'] != 0:
                                dict_media['4'] = datos[0]['total_abril'] / datos[0]['cant_abril']
                        if mes_inicio < 6:
                            if anno_inicio == anno_fin and mes_fin < 5:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_mayo'] and datos[0]['cant_mayo'] != 0:
                                dict_media['5'] = datos[0]['total_mayo'] / datos[0]['cant_mayo']
                        if mes_inicio < 7:
                            if anno_inicio == anno_fin and mes_fin < 6:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_junio'] and datos[0]['cant_junio'] != 0:
                                dict_media['6'] = datos[0]['total_junio'] / datos[0]['cant_junio']
                        if mes_inicio < 8:
                            if anno_inicio == anno_fin and mes_fin < 7:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_julio'] and datos[0]['cant_julio'] != 0:
                                dict_media['7'] = datos[0]['total_julio'] / datos[0]['cant_julio']
                        if mes_inicio < 9:
                            if anno_inicio == anno_fin and mes_fin < 8:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_agosto'] and datos[0]['cant_agosto'] != 0:
                                dict_media['8'] = datos[0]['total_agosto'] / datos[0]['cant_agosto']
                        if mes_inicio < 10:
                            if anno_inicio == anno_fin and mes_fin < 9:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_septiembre'] and datos[0]['cant_septiembre'] != 0:
                                dict_media['9'] = datos[0]['total_septiembre'] / datos[0]['cant_septiembre']
                        if mes_inicio < 11:
                            if anno_inicio == anno_fin and mes_fin < 10:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_octubre'] and datos[0]['cant_octubre'] != 0:
                                dict_media['10'] = datos[0]['total_octubre'] / datos[0]['cant_octubre']
                        if mes_inicio < 12:
                            if anno_inicio == anno_fin and mes_fin < 11:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_noviembre'] and datos[0]['cant_noviembre'] != 0:
                                dict_media['11'] = datos[0]['total_noviembre'] / datos[0]['cant_noviembre']
                        if mes_inicio < 13:
                            if anno_inicio == anno_fin and mes_fin < 12:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_sector.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_diciembre'] and datos[0]['cant_diciembre'] != 0:
                                dict_media['12'] = datos[0]['total_diciembre'] / datos[0]['cant_diciembre']

                    if datos[0]['anno'] > anno_inicio and datos[0]['anno'] < anno_fin:
                        if datos[0]['total_enero'] and datos[0]['cant_enero'] != 0:
                            dict_media['1'] = datos[0]['total_enero'] / datos[0]['cant_enero']
                        if datos[0]['total_febrero'] and datos[0]['cant_febrero'] != 0:
                            dict_media['2'] = datos[0]['total_febrero'] / datos[0]['cant_febrero']
                        if datos[0]['total_marzo'] and datos[0]['cant_marzo'] != 0:
                            dict_media['3'] = datos[0]['total_marzo'] / datos[0]['cant_marzo']
                        if datos[0]['total_abril'] and datos[0]['cant_abril'] != 0:
                            dict_media['4'] = datos[0]['total_abril'] / datos[0]['cant_abril']
                        if datos[0]['total_mayo'] and datos[0]['cant_mayo'] != 0:
                            dict_media['5'] = datos[0]['total_mayo'] / datos[0]['cant_mayo']
                        if datos[0]['total_junio'] and datos[0]['cant_junio'] != 0:
                            dict_media['6'] = datos[0]['total_junio'] / datos[0]['cant_junio']
                        if datos[0]['total_julio'] and datos[0]['cant_julio'] != 0:
                            dict_media['7'] = datos[0]['total_julio'] / datos[0]['cant_julio']
                        if datos[0]['total_agosto'] and datos[0]['cant_agosto'] != 0:
                            dict_media['8'] = datos[0]['total_agosto'] / datos[0]['cant_agosto']
                        if datos[0]['total_septiembre'] and datos[0]['cant_septiembre'] != 0:
                            dict_media['9'] = datos[0]['total_septiembre'] / datos[0]['cant_septiembre']
                        if datos[0]['total_octubre'] and datos[0]['cant_octubre'] != 0:
                            dict_media['10'] = datos[0]['total_octubre'] / datos[0]['cant_octubre']
                        if datos[0]['total_noviembre'] and datos[0]['cant_noviembre'] != 0:
                            dict_media['11'] = datos[0]['total_noviembre'] / datos[0]['cant_noviembre']
                        if datos[0]['total_diciembre'] and datos[0]['cant_diciembre'] != 0:
                            dict_media['12'] = datos[0]['total_diciembre'] / datos[0]['cant_diciembre']

                    if datos[0]['anno'] == anno_fin and anno_inicio != anno_fin:
                        if mes_fin > 0:
                            if datos[0]['total_enero'] and datos[0]['cant_enero'] != 0:
                                dict_media['1'] = datos[0]['total_enero'] / datos[0]['cant_enero']
                        if mes_fin > 1:
                            if datos[0]['total_febrero'] and datos[0]['cant_febrero'] != 0:
                                dict_media['2'] = datos[0]['total_febrero'] / datos[0]['cant_febrero']
                        if mes_fin > 2:
                            if datos[0]['total_marzo'] and datos[0]['cant_marzo'] != 0:
                                dict_media['3'] = datos[0]['total_marzo'] / datos[0]['cant_marzo']
                        if mes_fin > 3:
                            if datos[0]['total_abril'] and datos[0]['cant_abril'] != 0:
                                dict_media['4'] = datos[0]['total_abril'] / datos[0]['cant_abril']
                        if mes_fin > 4:
                            if datos[0]['total_mayo'] and datos[0]['cant_mayo'] != 0:
                                dict_media['5'] = datos[0]['total_mayo'] / datos[0]['cant_mayo']
                        if mes_fin > 5:
                            if datos[0]['total_junio'] and datos[0]['cant_junio'] != 0:
                                dict_media['6'] = datos[0]['total_junio'] / datos[0]['cant_junio']
                        if mes_fin > 6:
                            if datos[0]['total_julio'] and datos[0]['cant_julio'] != 0:
                                dict_media['7'] = datos[0]['total_julio'] / datos[0]['cant_julio']
                        if mes_fin > 7:
                            if datos[0]['total_agosto'] and datos[0]['cant_agosto'] != 0:
                                dict_media['8'] = datos[0]['total_agosto'] / datos[0]['cant_agosto']
                        if mes_fin > 8:
                            if datos[0]['total_septiembre'] and datos[0]['cant_septiembre'] != 0:
                                dict_media['9'] = datos[0]['total_septiembre'] / datos[0]['cant_septiembre']
                        if mes_fin > 9:
                            if datos[0]['total_octubre'] and datos[0]['cant_octubre'] != 0:
                                dict_media['10'] = datos[0]['total_octubre'] / datos[0]['cant_octubre']
                        if mes_fin > 10:
                            if datos[0]['total_noviembre'] and datos[0]['cant_noviembre'] != 0:
                                dict_media['11'] = datos[0]['total_noviembre'] / datos[0]['cant_noviembre']
                        if mes_fin > 11:
                            if datos[0]['total_diciembre'] and datos[0]['cant_diciembre'] != 0:
                                dict_media['12'] = datos[0]['total_diciembre'] / datos[0]['cant_diciembre']
                dict_media['anno'] = current_year
                dict_media['id'] = id
                arreglo_sector.append(dict_media)
                current_year += 1
            res.append(arreglo_sector)
        return res

    def _calcular_media_sector_sin_rango_fecha(self, ids, pozo_ids):
        res = []
        for id in ids:
            arreglo_sector = []
            datos = self._valores_sin_rango_fechas(id, pozo_ids)
            cant = len(datos)
            cont = 0
            while cont < cant:
                dict_media = {}
                dict_media['anno'] = datos[cont]['anno']
                dict_media['id'] = id
                if datos[cont]['media_enero']:
                    dict_media['1'] = datos[cont]['media_enero']
                if datos[cont]['media_febrero']:
                    dict_media['2'] = datos[cont]['media_febrero']
                if datos[cont]['media_marzo']:
                    dict_media['3'] = datos[cont]['media_marzo']
                if datos[cont]['media_abril']:
                    dict_media['4'] = datos[cont]['media_abril']
                if datos[cont]['media_mayo']:
                    dict_media['5'] = datos[cont]['media_mayo']
                if datos[cont]['media_junio']:
                    dict_media['6'] = datos[cont]['media_junio']
                if datos[cont]['media_julio']:
                    dict_media['7'] = datos[cont]['media_julio']
                if datos[cont]['media_agosto']:
                    dict_media['8'] = datos[cont]['media_agosto']
                if datos[cont]['media_septiembre']:
                    dict_media['9'] = datos[cont]['media_septiembre']
                if datos[cont]['media_octubre']:
                    dict_media['10'] = datos[cont]['media_octubre']
                if datos[cont]['media_noviembre']:
                    dict_media['11'] = datos[cont]['media_noviembre']
                if datos[cont]['media_diciembre']:
                    dict_media['12'] = datos[cont]['media_diciembre']
                cont += 1
                arreglo_sector.append(dict_media)
            res.append(arreglo_sector)
        return res

    def calcular_media_aritmetica(self, ids, pozo_ids, fecha_inicio, fecha_fin):
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                temp = fecha_fin
                fecha_fin = fecha_inicio
                fecha_inicio = temp
            res = self._calcular_media_sector_rango_fecha(ids, pozo_ids, fecha_inicio, fecha_fin)
        else:
            res = self._calcular_media_sector_sin_rango_fecha(ids, pozo_ids)
        return res

    def calcular_media_por_formula(self, ids, pozo_ids, fecha_inicio, fecha_fin):
        obj = self.browse(ids)[0]
        sigla = str(obj.sigla)
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                temp = fecha_fin
                fecha_fin = fecha_inicio
                fecha_inicio = temp
            res = self._calcular_media_sector_rango_fecha(ids, pozo_ids, fecha_inicio, fecha_fin)
        else:
            res = self._calcular_media_sector_sin_rango_fecha(ids, pozo_ids)
        cantidad = len(res)
        contador = 0
        while contador < cantidad:
            cant = len(res[contador])
            cont = 0
            while cont < cant:
                cont_meses = 1
                while cont_meses <= 12:
                    if res[contador][cont].get(str(cont_meses)):
                        a_cero = a_uno = 0
                        if res[contador][cont].get('id'):
                            obj_id = res[contador][cont]['id']
                            obj = self.browse( obj_id)
                            a_cero = obj.a0
                            a_uno = obj.a1
                        if sigla == 'CA-I-5':
                            valor = (a_uno * res[contador][cont][str(cont_meses)]) - a_cero
                        else:
                            valor = a_cero + a_uno * res[contador][cont][str(cont_meses)]
                        res[contador][cont][str(cont_meses)] = valor
                    cont_meses += 1
                cont += 1
            contador += 1
        return res

    def max_min(self, ids, pozo_ids, fecha_inicio, fecha_fin, tipo):
        res = {'id': '', 'nombre': '', 'valor_min': 999999.11, 'valor_max': 999999.11}
        existe = False
        variable = 0
        #global encontro
        encontro = 0
        temp = 0
        datos_generales = []
        if tipo == 'aritmetica':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio, fecha_fin)
        if tipo == 'formula':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio, fecha_fin)
        if datos_vistas:
            for id in ids:
                cont = 0
                pos = variable
                while cont < len(datos_vistas[pos]):
                    if encontro == 1:
                        break
                    valor = 0
                    if len(datos_vistas[pos][cont]) > 2:
                        for llave in datos_vistas[pos][cont]:
                            if llave != 'anno' and llave != 'id':
                                min = list(datos_vistas[pos][cont].values())[valor]
                                anno_minimo = datos_vistas[pos][cont]['anno']
                                mes_minimo = list(datos_vistas[pos][cont].keys())[valor]
                                anno_maximo = datos_vistas[pos][cont]['anno']
                                mes_maximo = list(datos_vistas[pos][cont].keys())[valor]
                                max = 0.0
                                existe = True
                                encontro = 1
                                break
                            valor += 1
                        cont += 1
                    else:
                        cont += 1
                if existe:
                    for datos_vista in datos_vistas[temp]:
                        if len(datos_vista) > 2:
                            aux = -1
                            aux1 = -1
                            for var in datos_vista.keys():
                                if var == 'anno':
                                    aux += 1
                                    break
                                else:
                                    aux += 1
                            clave = list(datos_vista.keys())
                            clave.pop(aux)
                            clave_temp = clave
                            for var in clave_temp:
                                if var == 'id':
                                    aux1 += 1
                                    break
                                else:
                                    aux1 += 1
                            clave.pop(aux1)
                            listas = []
                            for clave_aux in clave:
                                valor_clave = int(clave_aux)
                                listas.append(valor_clave)
                            listas.sort()
                            for lista in listas:
                                valor = datos_vista[str(lista)]
                                if valor < min:
                                    min = valor
                                    anno_minimo = datos_vista['anno']
                                    mes_minimo = lista
                                if valor > max:
                                    max = valor
                                    anno_maximo = datos_vista['anno']
                                    mes_maximo = lista
                    res = {'valor_min': min, 'valor_max': max, 'Amin': anno_minimo, 'Mmin': mes_minimo,
                           'Amax': anno_maximo, 'Mmax': mes_maximo, 'id': id}
                    variable += 1
                    temp += 1
                    datos_generales.append(res)
                    existe = False
                    encontro = 0
                else:
                    datos_generales.append(res)
                    variable += 1
                    temp += 1
                    existe = False
                    encontro = 0
        else:
            datos_generales.append(res)
        encontro = 0
        return datos_generales

    def altura(self, ids, pozo_ids, fecha_inicio, fecha_fin, tipo):
        datos_generales = []
        temp = 0
        if tipo == 'aritmetica':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio, fecha_fin)
        if tipo == 'formula':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio, fecha_fin)
        if datos_vistas:
            for id in ids:
                if fecha_inicio == None and fecha_fin == None:
                    dict_max = self.max_min([id], pozo_ids, None, None, tipo)
                else:
                    dict_max = self.max_min([id], pozo_ids, fecha_inicio, fecha_fin, tipo)
                max = dict_max[0]['valor_max']
                max_fijo = self.browse(id).maximo_h_periodo_fijo
                for datos_vista in datos_vistas[temp]:
                    dict_altura = {}
                    if datos_vista.get('1'):
                        if max_fijo <= 0.0:
                            dict_altura['1'] = max - datos_vista['1']
                        else:
                            dict_altura['1'] = max_fijo - datos_vista['1']
                    if datos_vista.get('2'):
                        if max_fijo <= 0.0:
                            dict_altura['2'] = max - datos_vista['2']
                        else:
                            dict_altura['2'] = max_fijo - datos_vista['2']
                    if datos_vista.get('3'):
                        if max_fijo <= 0.0:
                            dict_altura['3'] = max - datos_vista['3']
                        else:
                            dict_altura['3'] = max_fijo - datos_vista['3']
                    if datos_vista.get('4'):
                        if max_fijo <= 0.0:
                            dict_altura['4'] = max - datos_vista['4']
                        else:
                            dict_altura['4'] = max_fijo - datos_vista['4']
                    if datos_vista.get('5'):
                        if max_fijo <= 0.0:
                            dict_altura['5'] = max - datos_vista['5']
                        else:
                            dict_altura['5'] = max_fijo - datos_vista['5']
                    if datos_vista.get('6'):
                        if max_fijo <= 0.0:
                            dict_altura['6'] = max - datos_vista['6']
                        else:
                            dict_altura['6'] = max_fijo - datos_vista['6']
                    if datos_vista.get('7'):
                        if max_fijo <= 0.0:
                            dict_altura['7'] = max - datos_vista['7']
                        else:
                            dict_altura['7'] = max_fijo - datos_vista['7']
                    if datos_vista.get('8'):
                        if max_fijo <= 0.0:
                            dict_altura['8'] = max - datos_vista['8']
                        else:
                            dict_altura['8'] = max_fijo - datos_vista['8']
                    if datos_vista.get('9'):
                        if max_fijo <= 0.0:
                            dict_altura['9'] = max - datos_vista['9']
                        else:
                            dict_altura['9'] = max_fijo - datos_vista['9']
                    if datos_vista.get('10'):
                        if max_fijo <= 0.0:
                            dict_altura['10'] = max - datos_vista['10']
                        else:
                            dict_altura['10'] = max_fijo - datos_vista['10']
                    if datos_vista.get('11'):
                        if max_fijo <= 0.0:
                            dict_altura['11'] = max - datos_vista['11']
                        else:
                            dict_altura['11'] = max_fijo - datos_vista['11']
                    if datos_vista.get('12'):
                        if max_fijo <= 0.0:
                            dict_altura['12'] = max - datos_vista['12']
                        else:
                            dict_altura['12'] = max_fijo - datos_vista['12']
                    dict_altura['anno'] = datos_vista['anno']
                    dict_altura['id'] = id
                    datos_generales.append(dict_altura)
                temp += 1
        return datos_generales

    def volumen(self, ids, pozo_ids, fecha_inicio, fecha_fin, tipo):
        datos_generales = []
        temp = 0
        if tipo == 'aritmetica':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio, fecha_fin)
        if tipo == 'formula':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio, fecha_fin)
        if datos_vistas:
            for id in ids:
                coeficiente_no_calculado = self.browse(id).coeficiente_almacenamiento
                cof_aprov = self.browse(id).coeficiente_aprovechamiento_hidraulico
                area = self.browse(id).area
                max_fijo = self.browse( id).maximo_h_periodo_fijo
                if fecha_inicio == None and fecha_fin == None:
                    dict_max = self.max_min([id], pozo_ids, None, None, tipo)
                else:
                    dict_max = self.max_min([id], pozo_ids, fecha_inicio, fecha_fin, tipo)
                max = dict_max[0]['valor_max']
                rec_explotable = self.browse(id).recurso_explotable
                if tipo == 'formula':
                    deltaH = 2 * (self.browse(id).promedio_h_periodo_formula)
                    coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000)
                else:
                    deltaH = 2 * (self.browse(id).promedio_h_periodo)
                    coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000)
                if coeficiente_no_calculado > 0.0:
                    coeficiente = round(coeficiente_no_calculado, 3)
                else:
                    coeficiente = round(coeficiente_calculado, 3)
                for datos_vista in datos_vistas[temp]:
                    dict_altura = {}
                    if datos_vista.get('1'):
                        if max_fijo <= 0.0:
                            dict_altura['1'] = ((coeficiente * (max - datos_vista['1']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['1'] = ((coeficiente * (max_fijo - datos_vista['1']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('2'):
                        if max_fijo <= 0.0:
                            dict_altura['2'] = ((coeficiente * (max - datos_vista['2']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['2'] = ((coeficiente * (max_fijo - datos_vista['2']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('3'):
                        if max_fijo <= 0.0:
                            dict_altura['3'] = ((coeficiente * (max - datos_vista['3']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['3'] = ((coeficiente * (max_fijo - datos_vista['3']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('4'):
                        if max_fijo <= 0.0:
                            dict_altura['4'] = ((coeficiente * (max - datos_vista['4']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['4'] = ((coeficiente * (max_fijo - datos_vista['4']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('5'):
                        if max_fijo <= 0.0:
                            dict_altura['5'] = ((coeficiente * (max - datos_vista['5']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['5'] = ((coeficiente * (max_fijo - datos_vista['5']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('6'):
                        if max_fijo <= 0.0:
                            dict_altura['6'] = ((coeficiente * (max - datos_vista['6']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['6'] = ((coeficiente * (max_fijo - datos_vista['6']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('7'):
                        if max_fijo <= 0.0:
                            dict_altura['7'] = ((coeficiente * (max - datos_vista['7']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['7'] = ((coeficiente * (max_fijo - datos_vista['7']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('8'):
                        if max_fijo <= 0.0:
                            dict_altura['8'] = ((coeficiente * (max - datos_vista['8']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['8'] = ((coeficiente * (max_fijo - datos_vista['8']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('9'):
                        if max_fijo <= 0.0:
                            dict_altura['9'] = ((coeficiente * (max - datos_vista['9']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['9'] = ((coeficiente * (max_fijo - datos_vista['9']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('10'):
                        if max_fijo <= 0.0:
                            dict_altura['10'] = ((coeficiente * (max - datos_vista['10']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['10'] = ((coeficiente * (max_fijo - datos_vista['10']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('11'):
                        if max_fijo <= 0.0:
                            dict_altura['11'] = ((coeficiente * (max - datos_vista['11']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['11'] = ((coeficiente * (max_fijo - datos_vista['11']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista.get('12'):
                        if max_fijo <= 0.0:
                            dict_altura['12'] = ((coeficiente * (max - datos_vista['12']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_altura['12'] = ((coeficiente * (max_fijo - datos_vista['12']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                    dict_altura['anno'] = datos_vista['anno']
                    dict_altura['id'] = id
                    datos_generales.append(dict_altura)
                temp += 1
        return datos_generales

    #
    #
    # ##EXPLOTACION REAL
    # ###metodo viejo que hala de pozos los datos
    # # def _valores_explotacion(self, cr, uid, id, pozo_ids, anno=None, context=None):
    # #
    # #     query = """SELECT
    # #                       df_explotacion_anual_pozo.anno,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_enero, -999999.110)) as total_enero,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_febrero, -999999.110)) as total_febrero,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_marzo, -999999.110)) as total_marzo,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_abril, -999999.110)) as total_abril,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_mayo, -999999.110)) as total_mayo,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_junio, -999999.110)) as total_junio,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_julio, -999999.110)) as total_julio,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_agosto, -999999.110)) as total_agosto,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_septiembre, -999999.110)) as total_septiembre,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_octubre, -999999.110)) as total_octubre,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_noviembre, -999999.110)) as total_noviembre,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_diciembre, -999999.110)) as total_diciembre
    # #                     FROM
    # #                       df_pozo,
    # #                       df_sector_hidrologico, """
    # #
    # #     bloque_obj = self.pool.get('df.bloque')
    # #     bloque_ids = bloque_obj.search(cr, uid, [])
    # #     if bloque_ids:
    # #         query += """df_bloque,
    # #                       df_explotacion_anual_pozo
    # #                     WHERE
    # #                       df_sector_hidrologico.id = %s AND
    # #                       df_explotacion_anual_pozo.pozo_id = df_pozo.id AND
    # #                       ((df_pozo.bloque_id = df_bloque.id AND df_bloque.sector_id = df_sector_hidrologico.id) OR
    # #                       df_pozo.sector_hidrologico_id = df_sector_hidrologico.id) """
    # #     else:
    # #         query += """df_explotacion_anual_pozo
    # #                     WHERE
    # #                       df_sector_hidrologico.id = %s AND
    # #                       df_explotacion_anual_pozo.pozo_id = df_pozo.id AND
    # #                       df_pozo.sector_hidrologico_id = df_sector_hidrologico.id """
    # #
    # #     if pozo_ids:
    # #         query +=""" AND df_pozo.id in %s"""
    # #     if anno:
    # #         query += """ AND df_explotacion_anual_pozo.anno = %s"""
    # #     query += """ GROUP BY df_sector_hidrologico.id, df_explotacion_anual_pozo.anno"""
    # #
    # #     if pozo_ids and anno:
    # #         cr.execute(query, (id, (tuple(pozo_ids)),anno))
    # #     elif pozo_ids or anno:
    # #         if pozo_ids:
    # #             cr.execute(query, (id, (tuple(pozo_ids))))
    # #         elif anno:
    # #             cr.execute(query, (id,anno))
    # #     else:
    # #         cr.execute(query, (id))
    # #     return cr.dictfetchall()
    #

    # ###metodo nuevo que hala del obj en cuestion
    def _valores_explotacion(self, id, anno=None):

        query = """SELECT
                          df_explotacion_sector_real.anno,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_enero, -999999.110)) as total_enero,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_febrero, -999999.110)) as total_febrero,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_marzo, -999999.110)) as total_marzo,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_abril, -999999.110)) as total_abril,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_mayo, -999999.110)) as total_mayo,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_junio, -999999.110)) as total_junio,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_julio, -999999.110)) as total_julio,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_agosto, -999999.110)) as total_agosto,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_septiembre, -999999.110)) as total_septiembre,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_octubre, -999999.110)) as total_octubre,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_noviembre, -999999.110)) as total_noviembre,
                          SUM(NULLIF(df_explotacion_sector_real.media_hiperanual_diciembre, -999999.110)) as total_diciembre
                        FROM
                          df_sector_hidrologico,
                          df_explotacion_sector_real
                        WHERE
                          df_sector_hidrologico.id = %s AND
                          df_explotacion_sector_real.sector_id = df_sector_hidrologico.id"""
        if anno:
            query += """ AND df_explotacion_sector_real.anno = %s"""
        query += """ GROUP BY df_sector_hidrologico.id, df_explotacion_sector_real.anno"""

        if anno:
            self.env.cr.execute(query, (id, anno))
        else:
            self.env.cr.execute(query, str(id))
        return self.env.cr.dictfetchall()

    # # def _calcular_explotacion_rango_fecha(self, cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context=None):
    def _calcular_explotacion_rango_fecha(self, ids, fecha_inicio, fecha_fin):
        res = []
        anno_inicio = fecha_inicio.year
        anno_fin = fecha_fin.year
        mes_inicio = fecha_inicio.month
        mes_fin = fecha_fin.month
        for id in ids:
            current_year = fecha_inicio.year
            arreglo_sector = []
            while current_year <= anno_fin:
                # datos = self._valores_explotacion(cr, uid, id, pozo_ids, current_year, context)
                datos = self._valores_explotacion(id, current_year)
                dict_explotacion = {}
                if datos:
                    if datos[0]['anno'] == anno_inicio:
                        if mes_inicio < 2:
                            if anno_inicio == anno_fin and mes_fin < 1:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_enero'] != 0:
                                dict_explotacion['1'] = datos[0]['total_enero']
                        if mes_inicio < 3:
                            if anno_inicio == anno_fin and mes_fin < 2:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_febrero'] != 0:
                                dict_explotacion['2'] = datos[0]['total_febrero']
                        if mes_inicio < 4:
                            if anno_inicio == anno_fin and mes_fin < 3:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_marzo'] != 0:
                                dict_explotacion['3'] = datos[0]['total_marzo']
                        if mes_inicio < 5:
                            if anno_inicio == anno_fin and mes_fin < 4:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_abril'] != 0:
                                dict_explotacion['4'] = datos[0]['total_abril']
                        if mes_inicio < 6:
                            if anno_inicio == anno_fin and mes_fin < 5:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_mayo'] != 0:
                                dict_explotacion['5'] = datos[0]['total_mayo']
                        if mes_inicio < 7:
                            if anno_inicio == anno_fin and mes_fin < 6:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_junio'] != 0:
                                dict_explotacion['6'] = datos[0]['total_junio']
                        if mes_inicio < 8:
                            if anno_inicio == anno_fin and mes_fin < 7:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_julio'] != 0:
                                dict_explotacion['7'] = datos[0]['total_julio']
                        if mes_inicio < 9:
                            if anno_inicio == anno_fin and mes_fin < 8:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_agosto'] != 0:
                                dict_explotacion['8'] = datos[0]['total_agosto']
                        if mes_inicio < 10:
                            if anno_inicio == anno_fin and mes_fin < 9:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_septiembre'] != 0:
                                dict_explotacion['9'] = datos[0]['total_septiembre']
                        if mes_inicio < 11:
                            if anno_inicio == anno_fin and mes_fin < 10:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_octubre'] != 0:
                                dict_explotacion['10'] = datos[0]['total_octubre']
                        if mes_inicio < 12:
                            if anno_inicio == anno_fin and mes_fin < 11:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_noviembre'] != 0:
                                dict_explotacion['11'] = datos[0]['total_noviembre']
                        if mes_inicio < 13:
                            if anno_inicio == anno_fin and mes_fin < 12:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_diciembre'] != 0:
                                dict_explotacion['12'] = datos[0]['total_diciembre']

                    if datos[0]['anno'] > anno_inicio and datos[0]['anno'] < anno_fin:
                        if datos[0]['total_enero'] != 0:
                            dict_explotacion['1'] = datos[0]['total_enero']
                        if datos[0]['total_febrero'] != 0:
                            dict_explotacion['2'] = datos[0]['total_febrero']
                        if datos[0]['total_marzo'] != 0:
                            dict_explotacion['3'] = datos[0]['total_marzo']
                        if datos[0]['total_abril'] != 0:
                            dict_explotacion['4'] = datos[0]['total_abril']
                        if datos[0]['total_mayo'] != 0:
                            dict_explotacion['5'] = datos[0]['total_mayo']
                        if datos[0]['total_junio'] != 0:
                            dict_explotacion['6'] = datos[0]['total_junio']
                        if datos[0]['total_julio'] != 0:
                            dict_explotacion['7'] = datos[0]['total_julio']
                        if datos[0]['total_agosto'] != 0:
                            dict_explotacion['8'] = datos[0]['total_agosto']
                        if datos[0]['total_septiembre'] != 0:
                            dict_explotacion['9'] = datos[0]['total_septiembre']
                        if datos[0]['total_octubre'] != 0:
                            dict_explotacion['10'] = datos[0]['total_octubre']
                        if datos[0]['total_noviembre'] != 0:
                            dict_explotacion['11'] = datos[0]['total_noviembre']
                        if datos[0]['total_diciembre'] != 0:
                            dict_explotacion['12'] = datos[0]['total_diciembre']

                    if datos[0]['anno'] == anno_fin and anno_inicio != anno_fin:
                        if mes_fin > 0:
                            if datos[0]['total_enero'] != 0:
                                dict_explotacion['1'] = datos[0]['total_enero']
                        if mes_fin > 1:
                            if datos[0]['total_febrero'] != 0:
                                dict_explotacion['2'] = datos[0]['total_febrero']
                        if mes_fin > 2:
                            if datos[0]['total_marzo'] != 0:
                                dict_explotacion['3'] = datos[0]['total_marzo']
                        if mes_fin > 3:
                            if datos[0]['total_abril'] != 0:
                                dict_explotacion['4'] = datos[0]['total_abril']
                        if mes_fin > 4:
                            if datos[0]['total_mayo'] != 0:
                                dict_explotacion['5'] = datos[0]['total_mayo']
                        if mes_fin > 5:
                            if datos[0]['total_junio'] != 0:
                                dict_explotacion['6'] = datos[0]['total_junio']
                        if mes_fin > 6:
                            if datos[0]['total_julio'] != 0:
                                dict_explotacion['7'] = datos[0]['total_julio']
                        if mes_fin > 7:
                            if datos[0]['total_agosto'] != 0:
                                dict_explotacion['8'] = datos[0]['total_agosto']
                        if mes_fin > 8:
                            if datos[0]['total_septiembre'] != 0:
                                dict_explotacion['9'] = datos[0]['total_septiembre']
                        if mes_fin > 9:
                            if datos[0]['total_octubre'] != 0:
                                dict_explotacion['10'] = datos[0]['total_octubre']
                        if mes_fin > 10:
                            if datos[0]['total_noviembre'] != 0:
                                dict_explotacion['11'] = datos[0]['total_noviembre']
                        if mes_fin > 11:
                            if datos[0]['total_diciembre'] != 0:
                                dict_explotacion['12'] = datos[0]['total_diciembre']
                dict_explotacion['anno'] = current_year
                dict_explotacion['id'] = id
                arreglo_sector.append(dict_explotacion)
                current_year += 1
            res.append(arreglo_sector)
        return res

    # # def _calcular_explotacion_sin_rango_fecha(self, cr, uid, ids, pozo_ids, context=None):
    def _calcular_explotacion_sin_rango_fecha(self):
        res = []
        for id in self:
            arreglo_sector = []
            # datos = self._valores_explotacion(cr, uid, id, pozo_ids, None, context)
            datos = self._valores_explotacion( id, None)
            cant = len(datos)
            cont = 0
            while cont < cant:
                dict_explotacion = {}
                dict_explotacion['anno'] = datos[cont]['anno']
                dict_explotacion['id'] = id
                if datos[cont]['total_enero']:
                    dict_explotacion['1'] = datos[cont]['total_enero']
                if datos[cont]['total_febrero']:
                    dict_explotacion['2'] = datos[cont]['total_febrero']
                if datos[cont]['total_marzo']:
                    dict_explotacion['3'] = datos[cont]['total_marzo']
                if datos[cont]['total_abril']:
                    dict_explotacion['4'] = datos[cont]['total_abril']
                if datos[cont]['total_mayo']:
                    dict_explotacion['5'] = datos[cont]['total_mayo']
                if datos[cont]['total_junio']:
                    dict_explotacion['6'] = datos[cont]['total_junio']
                if datos[cont]['total_julio']:
                    dict_explotacion['7'] = datos[cont]['total_julio']
                if datos[cont]['total_agosto']:
                    dict_explotacion['8'] = datos[cont]['total_agosto']
                if datos[cont]['total_septiembre']:
                    dict_explotacion['9'] = datos[cont]['total_septiembre']
                if datos[cont]['total_octubre']:
                    dict_explotacion['10'] = datos[cont]['total_octubre']
                if datos[cont]['total_noviembre']:
                    dict_explotacion['11'] = datos[cont]['total_noviembre']
                if datos[cont]['total_diciembre']:
                    dict_explotacion['12'] = datos[cont]['total_diciembre']
                cont += 1
                arreglo_sector.append(dict_explotacion)
            res.append(arreglo_sector)
        return res

    # # def calcular_explotacion_acumulada(self, cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context=None):
    def calcular_explotacion_acumulada(self, ids, fecha_inicio, fecha_fin):
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                temp = fecha_fin
                fecha_fin = fecha_inicio
                fecha_inicio = temp
            # res = self._calcular_explotacion_rango_fecha(cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context)
            res = self._calcular_explotacion_rango_fecha(ids, fecha_inicio, fecha_fin)
        else:
            # res = self._calcular_explotacion_sin_rango_fecha(cr, uid, ids, pozo_ids, context)
            res = self._calcular_explotacion_sin_rango_fecha(ids)
        return res

    # ##PLAN EXPLOTACION
    # # def _valores_plan_explotacion(self, cr, uid, id, pozo_ids, anno=None, context=None):
    # #
    # #     query = """SELECT
    # #                       df_plan_explotacion_anual_pozo.anno,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_enero, -999999.110)) as total_enero,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_febrero, -999999.110)) as total_febrero,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_marzo, -999999.110)) as total_marzo,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_abril, -999999.110)) as total_abril,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_mayo, -999999.110)) as total_mayo,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_junio, -999999.110)) as total_junio,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_julio, -999999.110)) as total_julio,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_agosto, -999999.110)) as total_agosto,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_septiembre, -999999.110)) as total_septiembre,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_octubre, -999999.110)) as total_octubre,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_noviembre, -999999.110)) as total_noviembre,
    # #                       SUM(NULLIF(df_plan_explotacion_anual_pozo.media_hiperanual_diciembre, -999999.110)) as total_diciembre
    # #                     FROM
    # #                       df_pozo,
    # #                       df_sector_hidrologico, """
    # #
    # #     bloque_obj = self.pool.get('df.bloque')
    # #     bloque_ids = bloque_obj.search(cr, uid, [])
    # #     if bloque_ids:
    # #         query += """df_bloque,
    # #                       df_plan_explotacion_anual_pozo
    # #                     WHERE
    # #                       df_sector_hidrologico.id = %s AND
    # #                       df_plan_explotacion_anual_pozo.pozo_id = df_pozo.id AND
    # #                       ((df_pozo.bloque_id = df_bloque.id AND df_bloque.sector_id = df_sector_hidrologico.id) OR
    # #                       df_pozo.sector_hidrologico_id = df_sector_hidrologico.id) """
    # #     else:
    # #         query += """df_plan_explotacion_anual_pozo
    # #                     WHERE
    # #                       df_sector_hidrologico.id = %s AND
    # #                       df_plan_explotacion_anual_pozo.pozo_id = df_pozo.id AND
    # #                       df_pozo.sector_hidrologico_id = df_sector_hidrologico.id """
    # #
    # #     if pozo_ids:
    # #         query +=""" AND df_pozo.id in %s"""
    # #     if anno:
    # #         query += """ AND df_plan_explotacion_anual_pozo.anno = %s"""
    # #     query += """ GROUP BY df_sector_hidrologico.id, df_plan_explotacion_anual_pozo.anno"""
    # #
    # #     if pozo_ids and anno:
    # #         cr.execute(query, (id, (tuple(pozo_ids)),anno))
    # #     elif pozo_ids or anno:
    # #         if pozo_ids:
    # #             cr.execute(query, (id, (tuple(pozo_ids))))
    # #         elif anno:
    # #             cr.execute(query, (id,anno))
    # #     else:
    # #         cr.execute(query, (id))
    # #     return cr.dictfetchall()

    # ###metodo nuevo
    def _valores_plan_explotacion(self, id, anno=None):

        query = """SELECT
                          df_explotacion_sector_plan.anno,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_enero, -999999.110)) as total_enero,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_febrero, -999999.110)) as total_febrero,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_marzo, -999999.110)) as total_marzo,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_abril, -999999.110)) as total_abril,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_mayo, -999999.110)) as total_mayo,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_junio, -999999.110)) as total_junio,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_julio, -999999.110)) as total_julio,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_agosto, -999999.110)) as total_agosto,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_septiembre, -999999.110)) as total_septiembre,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_octubre, -999999.110)) as total_octubre,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_noviembre, -999999.110)) as total_noviembre,
                          SUM(NULLIF(df_explotacion_sector_plan.media_hiperanual_diciembre, -999999.110)) as total_diciembre
                        FROM
                          df_sector_hidrologico,
                          df_explotacion_sector_plan
                        WHERE
                          df_sector_hidrologico.id = %s AND
                          df_explotacion_sector_plan.sector_id = df_sector_hidrologico.id"""
        if anno:
            query += """ AND df_explotacion_sector_plan.anno = %s"""
        query += """ GROUP BY df_sector_hidrologico.id, df_explotacion_sector_plan.anno"""

        if anno:
            self.env.cr.execute(query, (id, anno))
        else:
            self.env.cr.execute(query, str(id))
        return self.env.cr.dictfetchall()

    # # def _plan_explotacion_rango_fecha(self, cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context=None):
    def _plan_explotacion_rango_fecha(self, ids, fecha_inicio, fecha_fin):
        res = []
        anno_inicio = fecha_inicio.year
        anno_fin = fecha_fin.year
        mes_inicio = fecha_inicio.month
        mes_fin = fecha_fin.month
        for id in ids:
            current_year = fecha_inicio.year
            arreglo_sector = []
            while current_year <= anno_fin:
                # datos = self._valores_plan_explotacion(cr, uid, id, pozo_ids, current_year, context)
                datos = self._valores_plan_explotacion(id, current_year)
                dict_explotacion = {}
                if datos:
                    if datos[0]['anno'] == anno_inicio:
                        if mes_inicio < 2:
                            if anno_inicio == anno_fin and mes_fin < 1:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_enero'] != 0:
                                dict_explotacion['1'] = datos[0]['total_enero']
                        if mes_inicio < 3:
                            if anno_inicio == anno_fin and mes_fin < 2:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_febrero'] != 0:
                                dict_explotacion['2'] = datos[0]['total_febrero']
                        if mes_inicio < 4:
                            if anno_inicio == anno_fin and mes_fin < 3:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_marzo'] != 0:
                                dict_explotacion['3'] = datos[0]['total_marzo']
                        if mes_inicio < 5:
                            if anno_inicio == anno_fin and mes_fin < 4:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_abril'] != 0:
                                dict_explotacion['4'] = datos[0]['total_abril']
                        if mes_inicio < 6:
                            if anno_inicio == anno_fin and mes_fin < 5:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_mayo'] != 0:
                                dict_explotacion['5'] = datos[0]['total_mayo']
                        if mes_inicio < 7:
                            if anno_inicio == anno_fin and mes_fin < 6:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_junio'] != 0:
                                dict_explotacion['6'] = datos[0]['total_junio']
                        if mes_inicio < 8:
                            if anno_inicio == anno_fin and mes_fin < 7:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_julio'] != 0:
                                dict_explotacion['7'] = datos[0]['total_julio']
                        if mes_inicio < 9:
                            if anno_inicio == anno_fin and mes_fin < 8:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_agosto'] != 0:
                                dict_explotacion['8'] = datos[0]['total_agosto']
                        if mes_inicio < 10:
                            if anno_inicio == anno_fin and mes_fin < 9:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_septiembre'] != 0:
                                dict_explotacion['9'] = datos[0]['total_septiembre']
                        if mes_inicio < 11:
                            if anno_inicio == anno_fin and mes_fin < 10:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_octubre'] != 0:
                                dict_explotacion['10'] = datos[0]['total_octubre']
                        if mes_inicio < 12:
                            if anno_inicio == anno_fin and mes_fin < 11:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_noviembre'] != 0:
                                dict_explotacion['11'] = datos[0]['total_noviembre']
                        if mes_inicio < 13:
                            if anno_inicio == anno_fin and mes_fin < 12:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_sector.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_diciembre'] != 0:
                                dict_explotacion['12'] = datos[0]['total_diciembre']

                    if datos[0]['anno'] > anno_inicio and datos[0]['anno'] < anno_fin:
                        if datos[0]['total_enero'] != 0:
                            dict_explotacion['1'] = datos[0]['total_enero']
                        if datos[0]['total_febrero'] != 0:
                            dict_explotacion['2'] = datos[0]['total_febrero']
                        if datos[0]['total_marzo'] != 0:
                            dict_explotacion['3'] = datos[0]['total_marzo']
                        if datos[0]['total_abril'] != 0:
                            dict_explotacion['4'] = datos[0]['total_abril']
                        if datos[0]['total_mayo'] != 0:
                            dict_explotacion['5'] = datos[0]['total_mayo']
                        if datos[0]['total_junio'] != 0:
                            dict_explotacion['6'] = datos[0]['total_junio']
                        if datos[0]['total_julio'] != 0:
                            dict_explotacion['7'] = datos[0]['total_julio']
                        if datos[0]['total_agosto'] != 0:
                            dict_explotacion['8'] = datos[0]['total_agosto']
                        if datos[0]['total_septiembre'] != 0:
                            dict_explotacion['9'] = datos[0]['total_septiembre']
                        if datos[0]['total_octubre'] != 0:
                            dict_explotacion['10'] = datos[0]['total_octubre']
                        if datos[0]['total_noviembre'] != 0:
                            dict_explotacion['11'] = datos[0]['total_noviembre']
                        if datos[0]['total_diciembre'] != 0:
                            dict_explotacion['12'] = datos[0]['total_diciembre']

                    if datos[0]['anno'] == anno_fin and anno_inicio != anno_fin:
                        if mes_fin > 0:
                            if datos[0]['total_enero'] != 0:
                                dict_explotacion['1'] = datos[0]['total_enero']
                        if mes_fin > 1:
                            if datos[0]['total_febrero'] != 0:
                                dict_explotacion['2'] = datos[0]['total_febrero']
                        if mes_fin > 2:
                            if datos[0]['total_marzo'] != 0:
                                dict_explotacion['3'] = datos[0]['total_marzo']
                        if mes_fin > 3:
                            if datos[0]['total_abril'] != 0:
                                dict_explotacion['4'] = datos[0]['total_abril']
                        if mes_fin > 4:
                            if datos[0]['total_mayo'] != 0:
                                dict_explotacion['5'] = datos[0]['total_mayo']
                        if mes_fin > 5:
                            if datos[0]['total_junio'] != 0:
                                dict_explotacion['6'] = datos[0]['total_junio']
                        if mes_fin > 6:
                            if datos[0]['total_julio'] != 0:
                                dict_explotacion['7'] = datos[0]['total_julio']
                        if mes_fin > 7:
                            if datos[0]['total_agosto'] != 0:
                                dict_explotacion['8'] = datos[0]['total_agosto']
                        if mes_fin > 8:
                            if datos[0]['total_septiembre'] != 0:
                                dict_explotacion['9'] = datos[0]['total_septiembre']
                        if mes_fin > 9:
                            if datos[0]['total_octubre'] != 0:
                                dict_explotacion['10'] = datos[0]['total_octubre']
                        if mes_fin > 10:
                            if datos[0]['total_noviembre'] != 0:
                                dict_explotacion['11'] = datos[0]['total_noviembre']
                        if mes_fin > 11:
                            if datos[0]['total_diciembre'] != 0:
                                dict_explotacion['12'] = datos[0]['total_diciembre']
                dict_explotacion['anno'] = current_year
                dict_explotacion['id'] = id
                arreglo_sector.append(dict_explotacion)
                current_year += 1
            res.append(arreglo_sector)
        return res

    # # def _plan_explotacion_sin_rango_fecha(self, cr, uid, ids, pozo_ids, context=None):
    def _plan_explotacion_sin_rango_fecha(self, ids):
        res = []
        for id in ids:
            arreglo_sector = []
            # datos = self._valores_plan_explotacion(cr, uid, id, pozo_ids, None, context)
            datos = self._valores_plan_explotacion( id, None)
            cant = len(datos)
            cont = 0
            while cont < cant:
                dict_explotacion = {}
                dict_explotacion['anno'] = datos[cont]['anno']
                dict_explotacion['id'] = id
                if datos[cont]['total_enero']:
                    dict_explotacion['1'] = datos[cont]['total_enero']
                if datos[cont]['total_febrero']:
                    dict_explotacion['2'] = datos[cont]['total_febrero']
                if datos[cont]['total_marzo']:
                    dict_explotacion['3'] = datos[cont]['total_marzo']
                if datos[cont]['total_abril']:
                    dict_explotacion['4'] = datos[cont]['total_abril']
                if datos[cont]['total_mayo']:
                    dict_explotacion['5'] = datos[cont]['total_mayo']
                if datos[cont]['total_junio']:
                    dict_explotacion['6'] = datos[cont]['total_junio']
                if datos[cont]['total_julio']:
                    dict_explotacion['7'] = datos[cont]['total_julio']
                if datos[cont]['total_agosto']:
                    dict_explotacion['8'] = datos[cont]['total_agosto']
                if datos[cont]['total_septiembre']:
                    dict_explotacion['9'] = datos[cont]['total_septiembre']
                if datos[cont]['total_octubre']:
                    dict_explotacion['10'] = datos[cont]['total_octubre']
                if datos[cont]['total_noviembre']:
                    dict_explotacion['11'] = datos[cont]['total_noviembre']
                if datos[cont]['total_diciembre']:
                    dict_explotacion['12'] = datos[cont]['total_diciembre']
                cont += 1
                arreglo_sector.append(dict_explotacion)
            res.append(arreglo_sector)
        return res

    # # def plan_explotacion(self, cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context=None):
    def plan_explotacion(self, ids, fecha_inicio, fecha_fin):
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                temp = fecha_fin
                fecha_fin = fecha_inicio
                fecha_inicio = temp
            # res = self._plan_explotacion_rango_fecha(cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context)
            res = self._plan_explotacion_rango_fecha(ids, fecha_inicio, fecha_fin)
        else:
            # res = self._plan_explotacion_sin_rango_fecha(cr, uid, ids, pozo_ids, context)
            res = self._plan_explotacion_sin_rango_fecha(ids)
        return res

    def buscar_anno(self, pozo_ids):
        if pozo_ids:
            tabla_agrupamiento = 'df_nivel_anual_pozo'
            sql = """ select anno
                             from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                             where tabla_objeto.pozo_id in %s
                             ORDER BY anno ASC"""
            self.env.cr.execute(sql, (tuple(pozo_ids),))
            datos_vistas = self.env.cr.dictfetchall()
            return datos_vistas
        else:
             raise UserError(_('Debe de seleccionar los pozos.'))
             #raise osv.except_osv(_("Alerta !"), _("Debe de seleccionar los pozos."))

    def obtener(self, valor_anterior, lista):
        if lista:
            cont_asc = 0
            dict_resultados = {}
            # min=lista[0]['valor']
            max = lista[0]['valor']
            max_temporal = lista[0]['valor']
            anno_maximo = lista[0]['anno']
            mes_maximo = lista[0]['mes']
            for maximo in lista:
                if maximo['valor'] > max:
                    max = maximo['valor']
                    anno_maximo = maximo['anno']
                    mes_maximo = maximo['mes']
            for maximo in lista:
                if maximo['valor'] < max_temporal:
                    cont_asc += 1
                max_temporal = maximo['valor']
            if cont_asc == 3:
                if valor_anterior and valor_anterior['valor'] > lista[0]['valor']:
                    dict_resultados['valor'] = valor_anterior['valor']
                    dict_resultados['anno'] = valor_anterior['anno']
                    dict_resultados['mes'] = valor_anterior['mes']
                    dict_resultados['ok'] = 1
                else:
                    dict_resultados['valor'] = max
                    dict_resultados['anno'] = anno_maximo
                    dict_resultados['mes'] = mes_maximo
                    dict_resultados['ok'] = 1
                return dict_resultados
            else:
                temp = 2
                aux = 1
                lista_asc = []
                cont_desc = 0
                cont = 1
                max_ascendentes = lista[1]['valor']
                temp_asc = lista[3]
                while cont < 3:
                    if max_ascendentes > lista[temp]['valor']:
                        cont_desc += 1
                        if cont_desc <= 2:
                            lista_asc.append(lista[aux])
                            max_ascendentes = lista[aux]['valor']
                            temp += 1
                            cont += 1
                            aux += 1
                        else:
                            break
                    else:
                        # lista_asc=[]
                        # break
                        aux += 1
                        max_ascendentes = lista[aux]['valor']
                        temp += 1
                        cont += 1
                        # cont_desc+=1
                if cont_desc == 2:
                    # lista_asc.append(lista[1])
                    lista_asc.append(temp_asc)
                    valor_anterior = lista[1]
                else:
                    # lista_asc.append(lista[2])
                    lista_asc.append(temp_asc)
                    valor_anterior = lista[2]
                dict_resultados['ok'] = 2
                dict_resultados['anno'] = anno_maximo
                dict_resultados['mes'] = mes_maximo
                dict_resultados['lista'] = lista_asc
                dict_resultados['valor_anterior'] = valor_anterior
                return dict_resultados

    def buscar(self, recorrido_actual, list_recorridos, lista):
        lista_fechas = []
        recorridos_posteriores = []
        lista_strines = []
        lista_strines_posteriores = []
        encontro_recorrido = 0
        ok = 0
        for list_recorrido in list_recorridos:
            lista_fechas.append(list_recorrido)
        for lista_fecha in lista_fechas:
            if recorrido_actual != lista_fecha:
                recorridos_posteriores.append(lista_fecha)
        for valor in lista:
            anno = str(valor['anno'])
            mes = str(valor['mes'])
            fecha_string = anno + mes
            lista_strines.append(fecha_string)
        for recorridos_posteriore in recorridos_posteriores:
            lista_strines_posteriores.append(str(recorridos_posteriore.year) + str(recorridos_posteriore.month))
        for lista_strines_posteriore in lista_strines_posteriores:
            pos = 0
            for lista_strine in lista_strines:
                pos += 1
                if lista_strines_posteriore == lista_strine:
                    ok = pos
                    encontro_recorrido += 1
        if encontro_recorrido == 0:
            return 1
        else:
            contador = 1
            contador_aux = 1
            list_no_rango = []
            dict_resultados = {}
            max = lista[0]['valor']
            mes_maximo = lista[0]['mes']
            anno_maximo = lista[0]['anno']
            for maximo in lista:
                if contador < ok:
                    if maximo['valor'] > max:
                        max = maximo['valor']
                        anno_maximo = maximo['anno']
                        mes_maximo = maximo['mes']
                contador += 1
            for minimo in lista:
                if contador_aux >= ok:
                    list_no_rango.append(minimo)
                contador_aux += 1
            dict_resultados['valor'] = max
            dict_resultados['anno'] = anno_maximo
            dict_resultados['mes'] = mes_maximo
            dict_resultados['ok'] = 1
            dict_resultados['lista'] = list_no_rango
            return dict_resultados

    def buscar_valor_maximo(self, ultimos_4_valores):
        max = ultimos_4_valores[0]['valor']
        anno_maximo = ultimos_4_valores[0]['anno']
        mes_maximo = ultimos_4_valores[0]['mes']
        for maximo in ultimos_4_valores:
            if maximo['valor'] > max:
                max = maximo['valor']
                anno_maximo = maximo['anno']
                mes_maximo = maximo['mes']
        dict_max = {}
        dict_max['valor'] = max
        dict_max['anno'] = anno_maximo
        dict_max['mes'] = mes_maximo
        return dict_max

    def ordenar_diccionario(self, niveles_ordenados):
        # lista=[None,None,None,None,None,None,None,None,None,None,None,None,None]
        datos_vistas = []
        for niveles_ordenado in niveles_ordenados:
            lista = [None, None, None, None, None, None, None, None, None, None, None, None, None]
            if niveles_ordenado.get('1'):
                lista[1] = niveles_ordenado['1']
            if niveles_ordenado.get('2'):
                lista[2] = niveles_ordenado['2']
            if niveles_ordenado.get('3'):
                lista[3] = niveles_ordenado['3']
            if niveles_ordenado.get('4'):
                lista[4] = niveles_ordenado['4']
            if niveles_ordenado.get('5'):
                lista[5] = niveles_ordenado['5']
            if niveles_ordenado.get('6'):
                lista[6] = niveles_ordenado['6']
            if niveles_ordenado.get('7'):
                lista[7] = niveles_ordenado['7']
            if niveles_ordenado.get('8'):
                lista[8] = niveles_ordenado['8']
            if niveles_ordenado.get('9'):
                lista[9] = niveles_ordenado['9']
            if niveles_ordenado.get('10'):
                lista[10] = niveles_ordenado['10']
            if niveles_ordenado.get('11'):
                lista[11] = niveles_ordenado['11']
            if niveles_ordenado.get('12'):
                lista[12] = niveles_ordenado['12']
            lista[0] = niveles_ordenado['anno']
            datos_vistas.append(tuple(lista))
        return datos_vistas

    def menor_proximo_valor(self, lista_sobrecarga):
        if lista_sobrecarga[1]['valor'] < lista_sobrecarga[0]['valor']:
            return True
        else:
            return False

    def buscar_sobrecarga(self, lista_sobrecarga, diferencia_sobrecarga):
        if lista_sobrecarga:
            valor = 0
            dict_resultados = {}
            if lista_sobrecarga[1]['valor'] != None and lista_sobrecarga[0]['valor'] != None:
                valor = abs(lista_sobrecarga[1]['valor'] - lista_sobrecarga[0]['valor'])
            if valor >= diferencia_sobrecarga:
                dict_resultados['valor'] = lista_sobrecarga[0]['valor']
                dict_resultados['anno'] = lista_sobrecarga[0]['anno']
                dict_resultados['mes'] = lista_sobrecarga[0]['mes']
                dict_resultados['sobrecarga'] = 1
            else:
                dict_resultados['valor'] = lista_sobrecarga[1]['valor']
                dict_resultados['anno'] = lista_sobrecarga[1]['anno']
                dict_resultados['mes'] = lista_sobrecarga[1]['mes']
                dict_resultados['sobrecarga'] = 2
        return dict_resultados

    def obtener_fin_recorridos(self, pozo_ids, recorridos, exepcion, tipo, ):
        fecha_fin = datetime.datetime.now()
        fecha_inicio = recorridos
        lista_recorridos = []
        # diferencia_sobrecarga=0.5
        global encontro
        for id in self:
            cont_recorrido = 0
            diferencia_sobrecarga = self.browse( id).valor_precision
            buscar = self.buscar_anno(pozo_ids)
            if len(buscar) > 0:
                anno_inicio = buscar[0]['anno']
                anno_fin = fecha_fin.year
                # anno_inicio=1999
                while anno_inicio <= anno_fin:
                    temp = 0
                    mes_valor = 0
                    contador = 1
                    contador4 = 0
                    lista = []
                    lista_sobrecarga = []
                    valor_anterior = {}
                    orden_recorrido = 0
                    for recorrido in recorridos:
                        orden_recorrido += 1
                        encontro = 0
                        contador_meses = 0
                        if anno_inicio == recorrido.year:
                            if tipo == 'aritmetica':
                                if fecha_inicio == None and fecha_fin == None:
                                    datos = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
                                    niveles_ordenados = sorted(datos[temp], key=lambda tup: tup['anno'])
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                                else:
                                    datos = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio[0],
                                                                           fecha_fin)
                                    niveles_ordenados = sorted(datos[temp], key=lambda tup: tup['anno'])
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                            if tipo == 'formula':
                                if fecha_inicio == None and fecha_fin == None:
                                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)
                                    niveles_ordenados = sorted(datos_vistas[temp], key=lambda tup: tup['anno'])
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                                else:
                                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids,
                                                                                   fecha_inicio[0], fecha_fin)
                                    niveles_ordenados = sorted(datos_vistas[temp], key=lambda tup: tup['anno'])
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                            for datos_vista in datos_vistas:
                                if encontro == 1:
                                    break
                                temporal = {}
                                for valor in datos_vista:
                                    if temp >= 1:
                                        mes_valor += 1
                                    temp += 1
                                    dict_general = {}
                                    if contador >= (recorrido.month + 1) and contador > 1:
                                        if len(temporal) > 0:
                                            lista.append(temporal)
                                            temporal = {}
                                            contador4 += 1
                                        if mes_valor >= 1:
                                            dict_general['valor'] = valor
                                            dict_general['anno'] = datos_vista[0]
                                            dict_general['mes'] = mes_valor
                                            lista.append(dict_general)
                                            lista_sobrecarga.append(dict_general)
                                            contador_meses += 1
                                            contador4 += 1
                                    if contador4 == 4:
                                        recorrido_actual = recorrido
                                        list_recorridos = exepcion
                                        coencide = self.buscar(recorrido_actual, list_recorridos, lista)
                                        if coencide != 1:
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            # max=ultimos_4_valores[0]['valor']
                                            # anno_maximo = ultimos_4_valores[0]['anno']
                                            # mes_maximo =ultimos_4_valores[0]['mes']
                                            # for maximo in ultimos_4_valores:
                                            #     if maximo['valor']>max:
                                            #         max=maximo['valor']
                                            #         anno_maximo= maximo['anno']
                                            #         mes_maximo=maximo['mes']
                                            # dict_max={}
                                            # dict_max['valor'] = max
                                            # dict_max['anno'] = anno_maximo
                                            # dict_max['mes'] = mes_maximo
                                            ultimos_4_valores = lista
                                            dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                            if dict_max['valor'] <= coencide['valor']:
                                                dic_recorridos['mes'] = coencide['mes']
                                                dic_recorridos['anno'] = coencide['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            else:
                                                dic_recorridos['mes'] = dict_max['mes']
                                                dic_recorridos['anno'] = dict_max['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            lista = []
                                            temporal = dict_general
                                            contador4 = 0
                                            encontro = 1
                                            break
                                        ultimos_4_valores = []
                                        ultimos_4_valores = lista
                                        existe = self.obtener(valor_anterior, lista)
                                        if existe['ok'] == 1:
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            # max=ultimos_4_valores[0]['valor']
                                            # anno_maximo = ultimos_4_valores[0]['anno']
                                            # mes_maximo =ultimos_4_valores[0]['mes']
                                            # for maximo in ultimos_4_valores:
                                            #     if maximo['valor']>max:
                                            #         max=maximo['valor']
                                            #         anno_maximo= maximo['anno']
                                            #         mes_maximo=maximo['mes']
                                            # dict_max={}
                                            # dict_max['valor'] = max
                                            # dict_max['anno'] = anno_maximo
                                            # dict_max['mes'] = mes_maximo
                                            dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                            if dict_max['valor'] <= existe['valor']:
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            else:
                                                dic_recorridos['mes'] = dict_max['mes']
                                                dic_recorridos['anno'] = dict_max['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                # dic_recorridos['mes']=existe['mes']
                                            # dic_recorridos['anno']=existe['anno']
                                            # dic_recorridos['orden_recorrido']=orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            lista = []
                                            temporal = dict_general
                                            contador4 = 0
                                            encontro = 1
                                            break
                                        if existe['ok'] == 2:
                                            lista = []
                                            cont_temp = 0
                                            for valor in existe['lista']:
                                                lista.append(valor)
                                                cont_temp += 1
                                            contador4 = cont_temp
                                            valor_anterior = existe['valor_anterior']
                                    if len(lista_sobrecarga) == 2:
                                        verdadero = self.menor_proximo_valor(lista_sobrecarga)
                                        sobrecarga = self.buscar_sobrecarga(lista_sobrecarga,
                                                                            diferencia_sobrecarga)
                                        if verdadero:
                                            if sobrecarga['sobrecarga'] == 1:
                                                dic_recorridos = {}
                                                dic_recorridos['mes'] = sobrecarga['mes']
                                                dic_recorridos['anno'] = sobrecarga['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                lista = []
                                                lista_sobrecarga = []
                                                temporal = dict_general
                                                contador4 = 0
                                                encontro = 1
                                                break
                                            else:
                                                lista_sobrecarga = []
                                                dict_general['valor'] = sobrecarga['valor']
                                                dict_general['anno'] = sobrecarga['anno']
                                                dict_general['mes'] = sobrecarga['mes']
                                                lista_sobrecarga.append(dict_general)
                                        else:
                                            lista_sobrecarga = []
                                            lista_sobrecarga.append(dict_general)
                                    if contador_meses == 24:
                                        if len(lista) == 4:
                                            # max=ultimos_4_valores[0]['valor']
                                            # anno_maximo = ultimos_4_valores[0]['anno']
                                            # mes_maximo =ultimos_4_valores[0]['mes']
                                            # for maximo in ultimos_4_valores:
                                            #     if maximo['valor']>max:
                                            #         max=maximo['valor']
                                            #         anno_maximo= maximo['anno']
                                            #         mes_maximo=maximo['mes']
                                            # dict_max={}
                                            # dict_max['valor'] = max
                                            # dict_max['anno'] = anno_maximo
                                            # dict_max['mes'] = mes_maximo
                                            dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                            lista.append(dict_max)
                                            existe = self.obtener(valor_anterior, lista)
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            dic_recorridos['mes'] = existe['mes']
                                            dic_recorridos['anno'] = existe['anno']
                                            dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            encontro = 1
                                            break
                                        else:
                                            if len(lista) == 1:
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    lista.append(ultimos_4_valore)
                                                    # max=ultimos_4_valores[0]['valor']
                                                # anno_maximo = ultimos_4_valores[0]['anno']
                                                # mes_maximo =ultimos_4_valores[0]['mes']
                                                # for maximo in ultimos_4_valores:
                                                #     if maximo['valor']>max:
                                                #         max=maximo['valor']
                                                #         anno_maximo= maximo['anno']
                                                #         mes_maximo=maximo['mes']
                                                # dict_max={}
                                                # dict_max['valor'] = max
                                                # dict_max['anno'] = anno_maximo
                                                # dict_max['mes'] = mes_maximo
                                                dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                                lista.append(dict_max)
                                                existe = self.obtener(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                            if len(lista) == 2:
                                                contadorv = 0
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    if contadorv >= 1:
                                                        lista.append(ultimos_4_valore)
                                                    contadorv += 1
                                                    # max=ultimos_4_valores[0]['valor']
                                                # anno_maximo = ultimos_4_valores[0]['anno']
                                                # mes_maximo =ultimos_4_valores[0]['mes']
                                                # for maximo in ultimos_4_valores:
                                                #     if maximo['valor']>max:
                                                #         max=maximo['valor']
                                                #         anno_maximo= maximo['anno']
                                                #         mes_maximo=maximo['mes']
                                                # dict_max={}
                                                # dict_max['valor'] = max
                                                # dict_max['anno'] = anno_maximo
                                                # dict_max['mes'] = mes_maximo
                                                dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                                lista.append(dict_max)
                                                existe = self.obtener(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                            if len(lista) == 3:
                                                contadorv = 0
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    if contadorv >= 2:
                                                        lista.append(ultimos_4_valore)
                                                    contadorv += 1
                                                    # max=ultimos_4_valores[0]['valor']
                                                # anno_maximo = ultimos_4_valores[0]['anno']
                                                # mes_maximo =ultimos_4_valores[0]['mes']
                                                # for maximo in ultimos_4_valores:
                                                #     if maximo['valor']>max:
                                                #         max=maximo['valor']
                                                #         anno_maximo= maximo['anno']
                                                #         mes_maximo=maximo['mes']
                                                # dict_max={}
                                                # dict_max['valor'] = max
                                                # dict_max['anno'] = anno_maximo
                                                # dict_max['mes'] = mes_maximo
                                                dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                                lista.append(dict_max)
                                                existe = self.obtener(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                    contador += 1
                                mes_valor = 0
                                temp = 0
                            contador = 1
                    anno_inicio += 1
        niveles_ordenados = sorted(lista_recorridos, key=lambda tup: tup['orden_recorrido'])
        return niveles_ordenados

    def buscar_inicio(self, recorrido_actual, list_recorridos, lista):
        lista_fechas = []
        recorridos_posteriores = []
        lista_strines = []
        lista_strines_posteriores = []
        encontro_recorrido = 0
        ok = 0
        for list_recorrido in list_recorridos:
            lista_fechas.append(list_recorrido)
        for lista_fecha in lista_fechas:
            if recorrido_actual != lista_fecha:
                recorridos_posteriores.append(lista_fecha)
        for valor in lista:
            anno = str(valor['anno'])
            mes = str(valor['mes'])
            fecha_string = anno + mes
            lista_strines.append(fecha_string)
        for recorridos_posteriore in recorridos_posteriores:
            lista_strines_posteriores.append(str(recorridos_posteriore.year) + str(recorridos_posteriore.month))
        for lista_strines_posteriore in lista_strines_posteriores:
            pos = 0
            for lista_strine in lista_strines:
                pos += 1
                if lista_strines_posteriore == lista_strine:
                    ok = pos
                    encontro_recorrido += 1
        if encontro_recorrido == 0:
            return 1
        else:
            contador = 1
            contador_aux = 1
            list_no_rango = []
            dict_resultados = {}
            min = lista[0]['valor']
            mes_minimo = lista[0]['mes']
            anno_minimo = lista[0]['anno']
            for minimo in lista:
                if contador < ok:
                    if minimo['valor'] < min:
                        min = minimo['valor']
                        anno_minimo = minimo['anno']
                        mes_minimo = minimo['mes']
                contador += 1
            for minimo in lista:
                if contador_aux >= ok:
                    list_no_rango.append(minimo)
                contador_aux += 1
            dict_resultados['valor'] = min
            dict_resultados['anno'] = anno_minimo
            dict_resultados['mes'] = mes_minimo
            dict_resultados['ok'] = 1
            dict_resultados['lista'] = list_no_rango
            return dict_resultados

    def obtener_inicio(self, valor_anterior, lista):
        if lista:
            cont_desc = 0
            dict_resultados = {}
            # min=lista[0]['valor']
            min = lista[0]['valor']
            max_temporal = lista[0]['valor']
            anno_minimo = lista[0]['anno']
            mes_minimo = lista[0]['mes']
            for minimo in lista:
                if minimo['valor'] < min:
                    min = minimo['valor']
                    anno_minimo = minimo['anno']
                    mes_minimo = minimo['mes']
            for maximo in lista:
                if maximo['valor'] > max_temporal:
                    cont_desc += 1
                max_temporal = maximo['valor']
            if cont_desc == 3:
                if valor_anterior and valor_anterior['valor'] < lista[0]['valor']:
                    dict_resultados['valor'] = valor_anterior['valor']
                    dict_resultados['anno'] = valor_anterior['anno']
                    dict_resultados['mes'] = valor_anterior['mes']
                    dict_resultados['ok'] = 1
                else:
                    dict_resultados['valor'] = min
                    dict_resultados['anno'] = anno_minimo
                    dict_resultados['mes'] = mes_minimo
                    dict_resultados['ok'] = 1
                return dict_resultados
            else:
                temp = 2
                aux = 1
                lista_asc = []
                cont_desc = 0
                cont = 1
                max_ascendentes = lista[1]['valor']
                temp_asc = lista[3]
                while cont < 3:
                    if max_ascendentes < lista[temp]['valor']:
                        cont_desc += 1
                        if cont_desc <= 2:
                            lista_asc.append(lista[aux])
                            max_ascendentes = lista[aux]['valor']
                            temp += 1
                            cont += 1
                            aux += 1
                        else:
                            break
                    else:
                        # lista_asc=[]
                        # break
                        aux += 1
                        max_ascendentes = lista[aux]['valor']
                        temp += 1
                        cont += 1
                        # cont_desc+=1
                if cont_desc == 2:
                    # lista_asc.append(lista[1])
                    lista_asc.append(temp_asc)
                    valor_anterior = lista[1]
                else:
                    # lista_asc.append(lista[2])
                    lista_asc.append(temp_asc)
                    valor_anterior = lista[2]
                dict_resultados['ok'] = 2
                dict_resultados['anno'] = anno_minimo
                dict_resultados['mes'] = mes_minimo
                dict_resultados['lista'] = lista_asc
                dict_resultados['valor_anterior'] = valor_anterior
                return dict_resultados

    def buscar_valor_minimo(self, ultimos_4_valores):
        min = ultimos_4_valores[0]['valor']
        anno_minimo = ultimos_4_valores[0]['anno']
        mes_minimo = ultimos_4_valores[0]['mes']
        for minimo in ultimos_4_valores:
            if minimo['valor'] < min:
                min = minimo['valor']
                anno_minimo = minimo['anno']
                mes_minimo = minimo['mes']
        dict_min = {}
        dict_min['valor'] = min
        dict_min['anno'] = mes_minimo
        dict_min['mes'] = anno_minimo
        return dict_min

    def menor_proximo_valor_inicio(self, lista_sobrecarga):
        if lista_sobrecarga[1]['valor'] > lista_sobrecarga[0]['valor']:
            return True
        else:
            return False

    def buscar_sobrecarga_inicio(self, lista_sobrecarga, diferencia_sobrecarga):
        if lista_sobrecarga:
            valor = 0
            dict_resultados = {}
            if lista_sobrecarga[1]['valor'] != None and lista_sobrecarga[0]['valor'] != None:
                valor = abs(lista_sobrecarga[1]['valor'] - lista_sobrecarga[0]['valor'])
            if valor >= diferencia_sobrecarga:
                dict_resultados['valor'] = lista_sobrecarga[0]['valor']
                dict_resultados['anno'] = lista_sobrecarga[0]['anno']
                dict_resultados['mes'] = lista_sobrecarga[0]['mes']
                dict_resultados['sobrecarga'] = 1
            else:
                dict_resultados['valor'] = lista_sobrecarga[1]['valor']
                dict_resultados['anno'] = lista_sobrecarga[1]['anno']
                dict_resultados['mes'] = lista_sobrecarga[1]['mes']
                dict_resultados['sobrecarga'] = 2
        return dict_resultados

    def obtener_inicio_recorridos(self, pozo_ids, recorridos, exepcion, tipo):
        fecha_actual = datetime.datetime.now()
        fecha_fin = recorridos
        lista_recorridos = []
        # diferencia_sobrecarga=0.5
        global encontro
        for id in self:
            cont_recorrido = 0
            diferencia_sobrecarga = self.browse( id).valor_precision
            buscar = self.buscar_anno(pozo_ids)
            if len(buscar) > 0:
                anno_inicio = buscar[0]['anno']
                dia = 1
                mes = 1
                fecha_inicio = datetime.datetime(anno_inicio, mes, dia)
                anno_fin = fecha_fin[0].year
                # anno_fin=2010
                while anno_fin >= anno_inicio:
                    temp = 0
                    temporal = {}
                    mes_valor = 0
                    contador = 1
                    contador4 = 0
                    lista = []
                    lista_sobrecarga = []
                    valor_anterior = {}
                    orden_recorrido = 0
                    for recorrido in recorridos:
                        posicion = recorrido.month
                        orden_recorrido += 1
                        encontro = 0
                        contador_meses = 0
                        if anno_fin == recorrido.year:
                            if tipo == 'aritmetica':
                                if fecha_inicio == None and fecha_fin == None:
                                    datos = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
                                    niveles_ordenados = sorted(datos[temp], key=lambda tup: tup['anno'], reverse=True)
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                                else:
                                    datos = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio,
                                                                           fecha_fin[0])
                                    niveles_ordenados = sorted(datos[temp], key=lambda tup: tup['anno'], reverse=True)
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                            if tipo == 'formula':
                                if fecha_inicio == None and fecha_fin == None:
                                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)

                                    niveles_ordenados = sorted(datos_vistas[temp], key=lambda tup: tup['anno'],
                                                               reverse=True)
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                                else:
                                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio,
                                                                                   fecha_fin[0])
                                    niveles_ordenados = sorted(datos_vistas[temp], key=lambda tup: tup['anno'],
                                                               reverse=True)
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                                # datos_vistas = self.obtener_niveles_acotados_asc(cr,pozo.id,anno_inicio,recorrido.year)
                            for datos_vista in datos_vistas:
                                if encontro == 1:
                                    break
                                while posicion >= 1:
                                    if len(temporal) > 0:
                                        lista.append(temporal)
                                        temporal = {}
                                        contador4 += 1
                                    dict_general = {}
                                    dict_general['valor'] = datos_vista[posicion]
                                    dict_general['anno'] = datos_vista[0]
                                    dict_general['mes'] = posicion
                                    lista.append(dict_general)
                                    lista_sobrecarga.append(dict_general)
                                    contador_meses += 1
                                    contador4 += 1
                                    posicion -= 1
                                    if contador4 == 4:
                                        recorrido_actual = recorrido
                                        list_recorridos = exepcion
                                        coencide = self.buscar_inicio(recorrido_actual, list_recorridos, lista)
                                        # lista=[]
                                        if coencide != 1:
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            # min=ultimos_4_valores[0]['valor']
                                            # anno_minimo = ultimos_4_valores[0]['anno']
                                            # mes_minimo =ultimos_4_valores[0]['mes']
                                            # for minimo in ultimos_4_valores:
                                            #     if minimo['valor']<min:
                                            #         min=minimo['valor']
                                            #         anno_minimo= minimo['anno']
                                            #         mes_minimo=minimo['mes']
                                            # dict_min={}
                                            # dict_min['valor'] = min
                                            # dict_min['anno'] = mes_minimo
                                            # dict_min['mes'] = anno_minimo
                                            ultimos_4_valores = lista
                                            dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                            if dict_min['valor'] >= coencide['valor']:
                                                dic_recorridos['mes'] = coencide['mes']
                                                dic_recorridos['anno'] = coencide['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            else:
                                                dic_recorridos['mes'] = dict_min['mes']
                                                dic_recorridos['anno'] = dict_min['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            lista = []
                                            temporal = dict_general
                                            contador4 = 0
                                            encontro = 1
                                            break
                                            # contador4=0
                                        # temporal= dict_general
                                        ultimos_4_valores = []
                                        ultimos_4_valores = lista
                                        existe = self.obtener_inicio(valor_anterior, lista)
                                        if existe['ok'] == 1:
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            # min=ultimos_4_valores[0]['valor']
                                            # anno_minimo = ultimos_4_valores[0]['anno']
                                            # mes_minimo =ultimos_4_valores[0]['mes']
                                            # for minimo in ultimos_4_valores:
                                            #     if minimo['valor']<min:
                                            #         min=minimo['valor']
                                            #         anno_minimo= minimo['anno']
                                            #         mes_minimo=minimo['mes']
                                            # dict_min={}
                                            # dict_min['valor'] = min
                                            # dict_min['anno'] = mes_minimo
                                            # dict_min['mes'] = anno_minimo
                                            dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                            if dict_min['valor'] >= existe['valor']:
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            else:
                                                dic_recorridos['mes'] = dict_min['mes']
                                                dic_recorridos['anno'] = dict_min['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            # dic_recorridos['mes']=existe['mes']
                                            # dic_recorridos['anno']=existe['anno']
                                            # dic_recorridos['orden_recorrido']=orden_recorrido
                                            # lista_recorridos.append(dic_recorridos)
                                            lista = []
                                            temporal = dict_general
                                            contador4 = 0
                                            encontro = 1
                                            break
                                        if existe['ok'] == 2:
                                            lista = []
                                            cont_temp = 0
                                            for valor in existe['lista']:
                                                lista.append(valor)
                                                cont_temp += 1
                                            contador4 = cont_temp
                                            valor_anterior = existe['valor_anterior']
                                    if len(lista_sobrecarga) == 2:
                                        verdadero = self.menor_proximo_valor_inicio(lista_sobrecarga)
                                        sobrecarga = self.buscar_sobrecarga_inicio(lista_sobrecarga,
                                                                                   diferencia_sobrecarga)
                                        if verdadero:
                                            if sobrecarga['sobrecarga'] == 1:
                                                dic_recorridos = {}
                                                dic_recorridos['mes'] = sobrecarga['mes']
                                                dic_recorridos['anno'] = sobrecarga['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                lista = []
                                                lista_sobrecarga = []
                                                temporal = dict_general
                                                contador4 = 0
                                                encontro = 1
                                                break
                                            else:
                                                lista_sobrecarga = []
                                                dict_general['valor'] = sobrecarga['valor']
                                                dict_general['anno'] = sobrecarga['anno']
                                                dict_general['mes'] = sobrecarga['mes']
                                                lista_sobrecarga.append(dict_general)
                                        else:
                                            lista_sobrecarga = []
                                            lista_sobrecarga.append(dict_general)
                                    if contador_meses == 24:
                                        if len(lista) == 4:
                                            # min=ultimos_4_valores[0]['valor']
                                            # anno_minimo = ultimos_4_valores[0]['anno']
                                            # mes_minimo =ultimos_4_valores[0]['mes']
                                            # for minimo in ultimos_4_valores:
                                            #     if minimo['valor']<min:
                                            #         min=minimo['valor']
                                            #         anno_minimo= minimo['anno']
                                            #         mes_minimo=minimo['mes']
                                            # dict_min={}
                                            # dict_min['valor'] = min
                                            # dict_min['anno'] = mes_minimo
                                            # dict_min['mes'] = anno_minimo
                                            dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                            lista.append(dict_min)
                                            existe = self.obtener_inicio(valor_anterior, lista)
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            dic_recorridos['mes'] = existe['mes']
                                            dic_recorridos['anno'] = existe['anno']
                                            dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            encontro = 1
                                            break
                                        else:
                                            if len(lista) == 1:
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    lista.append(ultimos_4_valore)
                                                    # min=ultimos_4_valores[0]['valor']
                                                # anno_minimo = ultimos_4_valores[0]['anno']
                                                # mes_minimo =ultimos_4_valores[0]['mes']
                                                # for minimo in ultimos_4_valores:
                                                #     if minimo['valor']<min:
                                                #         min=minimo['valor']
                                                #         anno_minimo= minimo['anno']
                                                #         mes_minimo=minimo['mes']
                                                # dict_min={}
                                                # dict_min['valor'] = min
                                                # dict_min['anno'] = mes_minimo
                                                # dict_min['mes'] = anno_minimo
                                                dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                                lista.append(dict_min)
                                                existe = self.obtener_inicio(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                            if len(lista) == 2:
                                                contadorv = 0
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    if contadorv >= 1:
                                                        lista.append(ultimos_4_valore)
                                                    contadorv += 1
                                                    # min=ultimos_4_valores[0]['valor']
                                                # anno_minimo = ultimos_4_valores[0]['anno']
                                                # mes_minimo =ultimos_4_valores[0]['mes']
                                                # for minimo in ultimos_4_valores:
                                                #     if minimo['valor']<min:
                                                #         min=minimo['valor']
                                                #         anno_minimo= minimo['anno']
                                                #         mes_minimo=minimo['mes']
                                                # dict_min={}
                                                # dict_min['valor'] = min
                                                # dict_min['anno'] = mes_minimo
                                                # dict_min['mes'] = anno_minimo
                                                dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                                lista.append(dict_min)
                                                existe = self.obtener_inicio(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                            if len(lista) == 3:
                                                contadorv = 0
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    if contadorv >= 2:
                                                        lista.append(ultimos_4_valore)
                                                    contadorv += 1
                                                    # min=ultimos_4_valores[0]['valor']
                                                # anno_minimo = ultimos_4_valores[0]['anno']
                                                # mes_minimo =ultimos_4_valores[0]['mes']
                                                # for minimo in ultimos_4_valores:
                                                #     if minimo['valor']<min:
                                                #         min=minimo['valor']
                                                #         anno_minimo= minimo['anno']
                                                #         mes_minimo=minimo['mes']
                                                # dict_min={}
                                                # dict_min['valor'] = min
                                                # dict_min['anno'] = mes_minimo
                                                # dict_min['mes'] = anno_minimo
                                                dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                                lista.append(dict_min)
                                                existe = self.obtener_inicio(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                posicion = 12
                    anno_fin -= 1
        niveles_ordenados = sorted(lista_recorridos, key=lambda tup: tup['orden_recorrido'])
        return niveles_ordenados

    def buscar_sectores_directo(self, pozo_ids):
        if pozo_ids:
            sql = """ SELECT
                          df_sector_hidrologico.id AS sector_ids
                        FROM
                          public.df_pozo,
                          public.df_sector_hidrologico
                        WHERE
                          df_pozo.sector_hidrologico_id = df_sector_hidrologico.id
                            AND
                          df_pozo.id in %s AND df_pozo.representativo=True"""
            self.env.cr.execute(sql, (tuple(pozo_ids),))
            datos_vistas = self.env.cr.dictfetchall()
            lista = []
            for datos_vista in datos_vistas:
                lista.append(datos_vista['sector_ids'])
            lista = list(set(lista))
            return lista

    def buscar_sectores_indirecto(self, pozo_ids):
        if pozo_ids:
            sql = """ SELECT
                          df_sector_hidrologico.id AS sector_ids
                        FROM
                          public.df_pozo,
                          public.df_sector_hidrologico,
                          public.df_bloque
                        WHERE
                          df_pozo.bloque_id = df_bloque.id AND
                          df_bloque.sector_id = df_sector_hidrologico.id
                            AND
                          df_pozo.id in %s AND df_pozo.representativo=True"""
            self.env.cr.execute(sql, (tuple(pozo_ids),))
            datos_vistas = self.env.cr.dictfetchall()
            lista = []
            for datos_vista in datos_vistas:
                lista.append(datos_vista['sector_ids'])
            lista = list(set(lista))
            return lista

    def obtener_promedio_alturas(self, pozo_ids_actualizar, ok):
        if ok:
            sectores_directo = self.buscar_sectores_directo( pozo_ids_actualizar)
            sectores_indirecto = self.buscar_sectores_indirecto( pozo_ids_actualizar)
            sectores_directo.extend([element for element in sectores_indirecto if element not in sectores_directo])
        # ids=sector_obj.search(cr, uid, [])
        else:
            sectores_directo = pozo_ids_actualizar
        sector_obj = self.env['df.sector.hidrologico']
        pozo_obj = self.env['df.pozo']
        cont = 0
        for sector in self.browse( sectores_directo):
            vals = {}
            suma_h_periodo = 0
            cantidad_h_periodo = 0
            obj_bloque = self.env['df.bloque']
            # bloque_ids = obj_bloque.search(cr, uid, [('bloque_id.sector_id', 'in', [sector.id])])
            bloque_ids = obj_bloque.search( [('sector_id', 'in', [sector.id])]).ids
            pozo_ids = pozo_obj.search( [('bloque_id', 'in', bloque_ids), ('representativo', '=', True)]).ids
            pozo_ids1 = pozo_obj.search(
                                        [('representativo', '=', True), ('sector_hidrologico_id', 'in', [sector.id])]).ids
            pozo_ids.extend([element for element in pozo_ids1 if element not in pozo_ids])
            if pozo_ids:
                inicio = self.formar_fecha_inicio(pozo_ids)
                fin = self.formar_fecha_fin(pozo_ids)
                if inicio != False and fin != False:
                    elementos = self.calcular_media_aritmetica([sector.id], pozo_ids, inicio, fin)
                    if elementos:
                        vals = {}
                        min = list(elementos[0][0].values())[0]
                        max = 0.0
                        suma_h_periodo = 0
                        cantidad_h_periodo = 0
                        contador_elementos = 0
                        suma_descargas_secuencia = 0
                        valores_recarga = []
                        valor_precision = 0.001
                        verificando_annos = []
                        ultima_recarga = None
                        # dia = 01
                        # mes = 01
                        # anno_inicio=2013
                        # inicio = datetime.datetime(anno_inicio,mes,dia)
                        while inicio <= fin:
                            tiempo = time.strptime(str(inicio.year) + '-' + str(inicio.month) + '-' + str(1),
                                                   "%Y-%m-%d")
                            tiempo_milisegundos = time.mktime(tiempo) * 1000
                            # valor = float("%.3f" % float(elementos[0][contador_elementos][self._mes_numero(inicio.month)]))
                            if elementos[0][contador_elementos].get(str(inicio.month)):
                                valor = float("%.3f" % float(elementos[0][contador_elementos][str(inicio.month)]))
                            if valor != -999999.110:
                                if valor < min:
                                    min = valor
                                if valor > max:
                                    max = valor
                                    # ---------BUSCANDO RECARGAS
                            if len(valores_recarga) > 0:  # si existen valores en analisis
                                valor_anterior = valores_recarga[len(valores_recarga) - 1]['valor']
                                # ------------ VERIFICANO PEQUENNAS DESCARGAS EN SECUENCIA QUE AL FINAL PUEDEN CONLLEVAR A UN DELTA ALTO
                                if valor - valor_anterior <= valor_precision and valor - valor_anterior > 0:
                                    suma_descargas_secuencia += valor - valor_anterior
                                else:
                                    suma_descargas_secuencia = 0
                                if (valor_anterior > valor or (
                                        valor - valor_anterior <= valor_precision and valor - valor_anterior > 0)) and suma_descargas_secuencia < valor_precision:
                                    # lo apilo
                                    valores_recarga.append({'tiempo_milisegundos': tiempo_milisegundos, 'valor': valor})
                                elif len(valores_recarga) > 1:
                                    suma_descargas_secuencia = 0

                                    # --------------------------------------------- DESAPILO VALORES BASURA
                                    # desapilo valores basura del fin
                                    indice_desapilo = len(valores_recarga) - 1
                                    valores_recarga_punto_mas_alto = \
                                        sorted(valores_recarga, key=lambda tup: tup['valor'])[0]['valor']
                                    while indice_desapilo >= 0:
                                        if valores_recarga[indice_desapilo]['valor'] > \
                                                valores_recarga[indice_desapilo - 1]['valor'] or \
                                                valores_recarga[indice_desapilo][
                                                    'valor'] > valores_recarga_punto_mas_alto:
                                            del valores_recarga[indice_desapilo]
                                            indice_desapilo -= 1
                                        else:
                                            break;
                                        if len(valores_recarga) == 1:
                                            valores_recarga = []
                                            break;

                                    # desapilo valores basura del inicio
                                    if len(valores_recarga) > 1:
                                        indice_desapilo = 0
                                        valores_recarga_punto_mas_bajo = \
                                            sorted(valores_recarga, key=lambda tup: tup['valor'], reverse=True)[0][
                                                'valor']
                                        while indice_desapilo < len(valores_recarga):
                                            if valores_recarga[indice_desapilo]['valor'] < \
                                                    valores_recarga[indice_desapilo + 1]['valor'] or \
                                                    valores_recarga[indice_desapilo][
                                                        'valor'] < valores_recarga_punto_mas_bajo:
                                                del valores_recarga[indice_desapilo]
                                            else:
                                                break;
                                            if len(valores_recarga) == 1:
                                                valores_recarga = []
                                                break;
                                                # --------------------------------------------- fin DESAPILO VALORES BASURA

                                    if len(valores_recarga) > 1:
                                        # punto delta_h
                                        # proximo IF para no tomar pequennas series insignificantes que no cumplen con el margen de error
                                        if (abs(valores_recarga[len(valores_recarga) - 1]['valor'] - valores_recarga[0][
                                            'valor']) > valor_precision):
                                            if not (abs(valores_recarga[0]['valor'] -
                                                        valores_recarga[len(valores_recarga) - 1][
                                                            'valor']) == 0):
                                                suma_h_periodo += abs(valores_recarga[0]['valor'] -
                                                                      valores_recarga[len(valores_recarga) - 1][
                                                                          'valor'])
                                                anno_delta_h = datetime.datetime.fromtimestamp(
                                                    valores_recarga[len(valores_recarga) - 1][
                                                        'tiempo_milisegundos'] / 1000.0).year
                                                if verificando_annos.count(anno_delta_h) == 0:
                                                    verificando_annos.append(anno_delta_h)
                                                    cantidad_h_periodo += 1
                                    valores_recarga = []
                                    valores_recarga.append({'valor': valor})
                                else:
                                    valores_recarga = []
                                    valores_recarga.append({'valor': valor})
                            else:
                                valores_recarga.append({'valor': valor})

                            if inicio.month == 12:
                                contador_elementos += 1
                            inicio = inicio + relativedelta(months=1)
                        if cantidad_h_periodo != 0:
                            # promedio=suma_h_periodo / len(elementos[0])
                            promedio = suma_h_periodo / len(verificando_annos)
                        else:
                            promedio = 0.0
                        vals['promedio_h_periodo'] = promedio
                        vals['minimo_h_periodo'] = min
                        vals['maximo_h_periodo'] = max
                        rec_explotable = self.browse( sector.id).recurso_explotable
                        area = self.browse( sector.id).area
                        deltaH = 2 * promedio
                        coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000) if (deltaH * area * 1000000) > 0 else 0
                        vals['coeficiente_almacenamiento_calculado'] = coeficiente_calculado
                        if sector.id:
                            #sector_obj.browse(sector.id).write(vals)
                            sector.write(vals)
                        else:
                            sector_obj.create(vals)
                        cont += 1
        return True

    def obtener_promedio_alturas_formula(self, pozo_ids_actualizar, ok):
        if ok:
            sectores_directo = self.buscar_sectores_directo( pozo_ids_actualizar)
            sectores_indirecto = self.buscar_sectores_indirecto( pozo_ids_actualizar)
            sectores_directo.extend([element for element in sectores_indirecto if element not in sectores_directo])
        # ids=sector_obj.search(cr, uid, [])
        else:
            sectores_directo = pozo_ids_actualizar
        sector_obj = self.env['df.sector.hidrologico']
        pozo_obj = self.env['df.pozo']
        cont = 0
        for sector in self.browse( sectores_directo):
            vals = {}
            suma_h_periodo = 0
            cantidad_h_periodo = 0
            obj_bloque = self.env['df.bloque']
            # bloque_ids = obj_bloque.search(cr, uid, [('bloque_id.sector_id', 'in', [sector.id])])
            bloque_ids = obj_bloque.search( [('sector_id', 'in', [sector.id])]).ids
            pozo_ids = pozo_obj.search( [('bloque_id', 'in', bloque_ids), ('representativo', '=', True)]).ids
            pozo_ids1 = pozo_obj.search(
                                        [('representativo', '=', True), ('sector_hidrologico_id', 'in', [sector.id])]).ids
            pozo_ids.extend([element for element in pozo_ids1 if element not in pozo_ids])
            if pozo_ids:
                inicio = self.formar_fecha_inicio(pozo_ids)
                fin = self.formar_fecha_fin(pozo_ids)
                if inicio != False and fin != False:
                    elementos = self.calcular_media_por_formula([sector.id], pozo_ids, inicio, fin)
                    if elementos:
                        vals = {}
                        min = list(elementos[0][0].values())[0]
                        max = 0.0
                        suma_h_periodo = 0
                        cantidad_h_periodo = 0
                        contador_elementos = 0
                        suma_descargas_secuencia = 0
                        valores_recarga = []
                        valor_precision = 0.001
                        verificando_annos = []
                        ultima_recarga = None
                        # dia = 01
                        # mes = 01
                        # anno_inicio=2013
                        # inicio = datetime.datetime(anno_inicio,mes,dia)
                        while inicio <= fin:
                            tiempo = time.strptime(str(inicio.year) + '-' + str(inicio.month) + '-' + str(1),
                                                   "%Y-%m-%d")
                            tiempo_milisegundos = time.mktime(tiempo) * 1000
                            # valor = float("%.3f" % float(elementos[0][contador_elementos][self._mes_numero(inicio.month)]))
                            #if elementos[0][contador_elementos].get(str(inicio.month)):
                            if str(inicio.month) in elementos[0][contador_elementos]:
                                valor = float("%.3f" % float(elementos[0][contador_elementos][str(inicio.month)]))
                            if valor != -999999.110:
                                if valor < min:
                                    min = valor
                                if valor > max:
                                    max = valor
                                    # ---------BUSCANDO RECARGAS
                            if len(valores_recarga) > 0:  # si existen valores en analisis
                                valor_anterior = valores_recarga[len(valores_recarga) - 1]['valor']
                                # ------------ VERIFICANO PEQUENNAS DESCARGAS EN SECUENCIA QUE AL FINAL PUEDEN CONLLEVAR A UN DELTA ALTO
                                if valor - valor_anterior <= valor_precision and valor - valor_anterior > 0:
                                    suma_descargas_secuencia += valor - valor_anterior
                                else:
                                    suma_descargas_secuencia = 0
                                if (valor_anterior > valor or (
                                        valor - valor_anterior <= valor_precision and valor - valor_anterior > 0)) and suma_descargas_secuencia < valor_precision:
                                    # lo apilo
                                    valores_recarga.append({'tiempo_milisegundos': tiempo_milisegundos, 'valor': valor})
                                elif len(valores_recarga) > 1:
                                    suma_descargas_secuencia = 0

                                    # --------------------------------------------- DESAPILO VALORES BASURA
                                    # desapilo valores basura del fin
                                    indice_desapilo = len(valores_recarga) - 1
                                    valores_recarga_punto_mas_alto = \
                                        sorted(valores_recarga, key=lambda tup: tup['valor'])[0]['valor']
                                    while indice_desapilo >= 0:
                                        if valores_recarga[indice_desapilo]['valor'] > \
                                                valores_recarga[indice_desapilo - 1]['valor'] or \
                                                valores_recarga[indice_desapilo][
                                                    'valor'] > valores_recarga_punto_mas_alto:
                                            del valores_recarga[indice_desapilo]
                                            indice_desapilo -= 1
                                        else:
                                            break;
                                        if len(valores_recarga) == 1:
                                            valores_recarga = []
                                            break;

                                    # desapilo valores basura del inicio
                                    if len(valores_recarga) > 1:
                                        indice_desapilo = 0
                                        valores_recarga_punto_mas_bajo = \
                                            sorted(valores_recarga, key=lambda tup: tup['valor'], reverse=True)[0][
                                                'valor']
                                        while indice_desapilo < len(valores_recarga):
                                            if valores_recarga[indice_desapilo]['valor'] < \
                                                    valores_recarga[indice_desapilo + 1]['valor'] or \
                                                    valores_recarga[indice_desapilo][
                                                        'valor'] < valores_recarga_punto_mas_bajo:
                                                del valores_recarga[indice_desapilo]
                                            else:
                                                break;
                                            if len(valores_recarga) == 1:
                                                valores_recarga = []
                                                break;
                                                # --------------------------------------------- fin DESAPILO VALORES BASURA

                                    if len(valores_recarga) > 1:
                                        # punto delta_h
                                        # proximo IF para no tomar pequennas series insignificantes que no cumplen con el margen de error
                                        if (abs(valores_recarga[len(valores_recarga) - 1]['valor'] - valores_recarga[0][
                                            'valor']) > valor_precision):
                                            if not (abs(valores_recarga[0]['valor'] -
                                                        valores_recarga[len(valores_recarga) - 1][
                                                            'valor']) == 0):
                                                suma_h_periodo += abs(valores_recarga[0]['valor'] -
                                                                      valores_recarga[len(valores_recarga) - 1][
                                                                          'valor'])
                                                anno_delta_h = datetime.datetime.fromtimestamp(
                                                    valores_recarga[len(valores_recarga) - 1][
                                                        'tiempo_milisegundos'] / 1000.0).year
                                                if verificando_annos.count(anno_delta_h) == 0:
                                                    verificando_annos.append(anno_delta_h)
                                                    cantidad_h_periodo += 1
                                    valores_recarga = []
                                    valores_recarga.append({'valor': valor})
                                else:
                                    valores_recarga = []
                                    valores_recarga.append({'valor': valor})
                            else:
                                valores_recarga.append({'valor': valor})

                            if inicio.month == 12:
                                contador_elementos += 1
                            inicio = inicio + relativedelta(months=1)
                        if cantidad_h_periodo != 0:
                            # promedio=suma_h_periodo / len(elementos[0])
                            promedio = suma_h_periodo / len(verificando_annos)
                        else:
                            promedio = 0.0
                        vals['promedio_h_periodo_formula'] = promedio
                        vals['minimo_h_periodo_formula'] = min
                        vals['maximo_h_periodo_formula'] = max
                        rec_explotable = self.browse( sector.id).recurso_explotable
                        area = self.browse( sector.id).area
                        deltaH = 2 * promedio
                        coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000) if (deltaH * area * 1000000) > 0 else 0
                        vals['coeficiente_almacenamiento_calculado_formula'] = coeficiente_calculado
                        if sector.id:
                            sector_obj.browse(sector.id).write(vals)
                        else:
                            sector_obj.create( vals)
                        cont += 1
        return True

    def obtener_cotas_tramos(self, ids, pozo_ids, fecha_inicio, fecha_fin, tipo):
        # res = {'id': '', 'nombre': '', 'valor_min': 999999.11, 'valor_max': 999999.11}
        # existe = False
        # variable=0
        # global encontro
        temp = 0
        # tipo = 'aritmetica'
        # fecha_inicio =None
        # fecha_fin = None
        datos_generales = []
        for id in ids:
            cota_topografica = self.browse(id).cota_topografica
            if tipo == 'aritmetica':
                if fecha_inicio == None and fecha_fin == None:
                    datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
                else:
                    datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio, fecha_fin)

            if tipo == 'formula':
                if fecha_inicio == None and fecha_fin == None:
                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)
                else:
                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio, fecha_fin)

            if datos_vistas:
                for datos_vista in datos_vistas[temp]:
                    dict_cota = {}
                    if datos_vista.get('1'):
                        dict_cota['cota_agua_enero'] = cota_topografica - datos_vista['1']
                    if datos_vista.get('2'):
                        dict_cota['cota_agua_febrero'] = cota_topografica - datos_vista['2']
                    if datos_vista.get('3'):
                        dict_cota['cota_agua_marzo'] = cota_topografica - datos_vista['3']
                    if datos_vista.get('4'):
                        dict_cota['cota_agua_abril'] = cota_topografica - datos_vista['4']
                    if datos_vista.get('5'):
                        dict_cota['cota_agua_mayo'] = cota_topografica - datos_vista['5']
                    if datos_vista.get('6'):
                        dict_cota['cota_agua_junio'] = cota_topografica - datos_vista['6']
                    if datos_vista.get('7'):
                        dict_cota['cota_agua_julio'] = cota_topografica - datos_vista['7']
                    if datos_vista.get('8'):
                        dict_cota['cota_agua_agosto'] = cota_topografica - datos_vista['8']
                    if datos_vista.get('9'):
                        dict_cota['cota_agua_septiembre'] = cota_topografica - datos_vista['9']
                    if datos_vista.get('10'):
                        dict_cota['cota_agua_octubre'] = cota_topografica - datos_vista['10']
                    if datos_vista.get('11'):
                        dict_cota['cota_agua_noviembre'] = cota_topografica - datos_vista['11']
                    if datos_vista.get('12'):
                        dict_cota['cota_agua_diciembre'] = cota_topografica - datos_vista['12']
                    if datos_vista.get('anno'):
                        dict_cota['anno'] = datos_vista['anno']
                    if datos_vista.get('id'):
                        dict_cota['id'] = id
                    datos_generales.append(dict_cota)
                temp += 1
        return datos_generales

    def _estado_sector(self):
        sector_obj = self.env['df.sector.hidrologico']
        pozo_obj = self.env['df.pozo']
        res = {}
        objeto_sectores = sector_obj.browse(self.ids)
        # encontro=0
        posicion = 11
        for objeto_sector in objeto_sectores:
            vals = {}
            vals['id'] = objeto_sector.id
            temp = 0
            obj_bloque = self.env['df.bloque']
            bloque_ids = obj_bloque.search([('sector_id', 'in', [objeto_sector.id])]).ids
            pozo_ids = pozo_obj.search([('bloque_id', 'in', bloque_ids), ('representativo', '=', True)]).ids
            pozo_ids1 = pozo_obj.search([('representativo', '=', True),
                                                       ('sector_hidrologico_id', 'in', [objeto_sector.id])]).ids
            pozo_ids.extend([element for element in pozo_ids1 if element not in pozo_ids])
            encontro = 0
            if pozo_ids:
                elementos = self.calcular_media_aritmetica([objeto_sector.id], pozo_ids, None, None)
                niveles_ordenados = sorted(elementos[temp], key=lambda tup: tup['anno'], reverse=True)
                datos_vistas = self.ordenar_diccionario(niveles_ordenados)
                deltah = self.browse(objeto_sector.id).promedio_h_periodo
                min_fijo = self.browse(objeto_sector.id).minimo_h_periodo_fijo
                min_calculado = self.browse(objeto_sector.id).minimo_h_periodo
                max_fijo = self.browse(objeto_sector.id).maximo_h_periodo_fijo
                max_calculado = self.browse(objeto_sector.id).maximo_h_periodo
                if min_fijo <= 0:
                    min = min_calculado
                else:
                    min = min_fijo
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
                                if datos_vista[posicion] >= nivel_alerta and datos_vista[posicion] <= nivel_alarma:
                                    objeto_sector.estado = 'desfavorable'
                                    vals['estado1'] = 'desfavorable'
                                elif datos_vista[posicion] >= nivel_alarma and datos_vista[posicion] <= max:
                                    objeto_sector.estado = 'muy desfavorable'
                                    vals['estado1'] = 'muy desfavorable'
                                elif datos_vista[posicion] <= nivel_alerta and datos_vista[posicion] >= (min + deltah):
                                    objeto_sector.estado = 'favorable'
                                    vals['estado1'] = 'favorable'
                                elif datos_vista[posicion] <= (min + deltah) and datos_vista[posicion] >= min:
                                    objeto_sector.estado = 'muy favorable'
                                    vals['estado1'] = 'muy favorable'
                                elif datos_vista[posicion] >= max:
                                    objeto_sector.estado = u'crítico'
                                    vals['estado1'] = u'crítico'
                                else:
                                    objeto_sector.estado = 'no hay nivel'
                                    vals['estado1'] = 'no hay nivel'
                                # sector_obj.write(cr,uid,objeto_sector.id,vals,context)
                                encontro = 1
                                break
                            posicion -= 1
                        posicion = 11
                else:
                    objeto_sector.estado = 'no hay nivel'
                    vals['estado1'] = 'no hay nivel'
                    # sector_obj.write(cr,uid,objeto_sector.id,vals,context)
            else:
                objeto_sector.estado = 'no hay nivel'
                vals['estado1'] = 'no hay nivel'
                # sector_obj.write(cr,uid,objeto_sector.id,vals,context)
        #return res

    cuenca_subterranea_id = fields.Many2one('df.cuenca.subterranea', 'Underground basin', required=True)

    # provincia_id = fields.Many2one(related='cuenca_subterranea_id.provincia_id',string='Country state', store=True,help="This field has the same value of field with the same name in 'Underground basin'")
    # Este campo provincia_id es de otro modulo que no se ha hecho todavía en ODOO 12

    nivel_ids = fields.One2many('df.nivel.anual.sector.hidrologico', 'sector_id', string='Levels', required=False)
    estado = fields.Char(compute='_estado_sector', string="State")
    estado1 = fields.Char(string='State', size=64, required=False)
    seguridad_compania = fields.Char(compute='_seguridad_compania')

    @api.model
    def create(self, vals):
        vals['active'] = True
        return super(df_sector_hidrologico, self).create(vals)

    @api.multi
    def write(self, vals):
        cuenca_obj = self.env['df.cuenca.subterranea']
        sector_obj = self.env['df.sector.hidrologico']
        bloque_obj = self.env['df.bloque']
        pozo_obj = self.env['df.pozo']
        super(df_sector_hidrologico, self).write(vals)
        if vals.get('a0', None) or vals.get('a1', None) or vals.get('valor_precision', None) or vals.get(
                'recurso_explotable', None):
            pozo_ids_actualizar = self.ids
            ok = False
            if pozo_ids_actualizar:
                # pozo_obj.obtener_promedio_alturas(cr,uid,pozo_ids_actualizar,ok)
                # bloque_obj.obtener_promedio_alturas(cr,uid,pozo_ids_actualizar,ok)
                # bloque_obj.obtener_promedio_alturas_formula(cr,uid,pozo_ids_actualizar,ok)
                sector_obj.obtener_promedio_alturas( pozo_ids_actualizar, ok)
                sector_obj.obtener_promedio_alturas_formula( pozo_ids_actualizar, ok)
                # cuenca_obj.obtener_promedio_alturas(cr,uid,pozo_ids_actualizar,ok)
                # cuenca_obj.obtener_promedio_alturas_formula(cr,uid,pozo_ids_actualizar,ok)
        return True

    # ##METODOS PARA CALCULO DE NIVELES PRONOSTICOS ... en tramo estan los restantes
    #
    def calcular_nivel_real(self, idd, mes, anno, pozo_ids, metodo):
        """Calcula nivel dado un mes"""
        if type(idd) != int:
            idd = idd[0]
        fecha_inicio = datetime.date(anno, mes, 1)
        end_day = self._lengthmonth(anno, mes)
        fecha_fin = datetime.date(anno, mes, end_day)
        res = None
        if metodo:
            media_aritmetica = self.calcular_media_por_formula([idd], pozo_ids, fecha_inicio, fecha_fin)

        else:
            media_aritmetica = self.calcular_media_aritmetica([idd], pozo_ids, fecha_inicio, fecha_fin)

        if media_aritmetica:
            if media_aritmetica[0][0].get(str(mes)):
                if media_aritmetica[0][0][str(mes)] != -999999.11:
                    res = round(media_aritmetica[0][0][str(mes)], 2)
        return res


class df_bloque(models.Model):
    _name = 'df.bloque'
    _inherit = 'df.tramo'
    _rec_name = 'sigla'
    _auto = True
    _description = "HC Block"

    def _valores_rango_fechas(self, id, pozo_ids, anno):

        query = """SELECT
                          df_nivel_anual_pozo.anno,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_enero, -999999.110)) as total_enero,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_febrero, -999999.110)) as total_febrero,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_marzo, -999999.110)) as total_marzo,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_abril, -999999.110)) as total_abril,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_mayo, -999999.110)) as total_mayo,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_junio, -999999.110)) as total_junio,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_julio, -999999.110)) as total_julio,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_agosto, -999999.110)) as total_agosto,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_septiembre, -999999.110)) as total_septiembre,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_octubre, -999999.110)) as total_octubre,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_noviembre, -999999.110)) as total_noviembre,
                          SUM(NULLIF(df_nivel_anual_pozo.media_hiperanual_diciembre, -999999.110)) as total_diciembre,

                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_enero, -999999.110)) as cant_enero,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_febrero, -999999.110)) as cant_febrero,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_marzo, -999999.110)) as cant_marzo,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_abril, -999999.110)) as cant_abril,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_mayo, -999999.110)) as cant_mayo,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_junio, -999999.110)) as cant_junio,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_julio, -999999.110)) as cant_julio,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_agosto, -999999.110)) as cant_agosto,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_septiembre, -999999.110)) as cant_septiembre,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_octubre, -999999.110)) as cant_octubre,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_noviembre, -999999.110)) as cant_noviembre,
                          COUNT(NULLIF(df_nivel_anual_pozo.media_hiperanual_diciembre, -999999.110)) as cant_diciembre
                        FROM
                          df_pozo,
                          df_bloque,
                          df_nivel_anual_pozo
                        WHERE
                          df_bloque.id = %s AND
                          df_pozo.bloque_id = df_bloque.id AND
                          df_nivel_anual_pozo.pozo_id = df_pozo.id AND """
        if pozo_ids:
            query += """df_pozo.id in %s AND
            df_nivel_anual_pozo.anno = %s
            GROUP BY df_bloque.id, df_nivel_anual_pozo.anno"""
            self.env.cr.execute(query, (id, (tuple(pozo_ids)), anno))
        else:
            query += """df_nivel_anual_pozo.anno = %s
            GROUP BY df_bloque.id, df_nivel_anual_pozo.anno"""
            self.env.cr.execute(query, (id, anno))
        return self.env.cr.dictfetchall()

    def _valores_sin_rango_fechas(self, id, pozo_ids):

        query = """SELECT
                          df_nivel_anual_pozo.anno,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_enero, -999999.110)) as media_enero,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_febrero, -999999.110)) as media_febrero,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_marzo, -999999.110)) as media_marzo,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_abril, -999999.110)) as media_abril,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_mayo, -999999.110)) as media_mayo,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_junio, -999999.110)) as media_junio,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_julio, -999999.110)) as media_julio,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_agosto, -999999.110)) as media_agosto,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_septiembre, -999999.110)) as media_septiembre,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_octubre, -999999.110)) as media_octubre,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_noviembre, -999999.110)) as media_noviembre,
                          AVG(NULLIF(df_nivel_anual_pozo.media_hiperanual_diciembre, -999999.110)) as media_diciembre
                        FROM
                          df_pozo,
                          df_bloque,
                          df_nivel_anual_pozo
                        WHERE
                          df_bloque.id = %s AND
                          df_pozo.bloque_id = df_bloque.id AND
                          df_nivel_anual_pozo.pozo_id = df_pozo.id """

        if pozo_ids:
            query += """ AND df_pozo.id in %s
            GROUP BY df_bloque.id, df_nivel_anual_pozo.anno"""
            self.env.cr.execute(query, (id, (tuple(pozo_ids))))
        else:
            query += """ GROUP BY df_bloque.id, df_nivel_anual_pozo.anno"""
            self.env.cr.execute(query, (id,))
        return self.env.cr.dictfetchall()

    def _calcular_media_bloque_rango_fecha(self, ids, pozo_ids, fecha_inicio, fecha_fin):
        res = []
        anno_inicio = fecha_inicio.year
        anno_fin = fecha_fin.year
        mes_inicio = fecha_inicio.month
        mes_fin = fecha_fin.month
        for id in ids:
            current_year = fecha_inicio.year
            arreglo_bloque = []
            while current_year <= anno_fin:
                datos = self._valores_rango_fechas(id, pozo_ids, current_year)
                dict_media = {}
                if datos:
                    if datos[0]['anno'] == anno_inicio:
                        if mes_inicio < 2:
                            if anno_inicio == anno_fin and mes_fin < 1:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_enero'] and datos[0]['cant_enero'] != 0:
                                dict_media['1'] = datos[0]['total_enero'] / datos[0]['cant_enero']
                        if mes_inicio < 3:
                            if anno_inicio == anno_fin and mes_fin < 2:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_febrero'] and datos[0]['cant_febrero'] != 0:
                                dict_media['2'] = datos[0]['total_febrero'] / datos[0]['cant_febrero']
                        if mes_inicio < 4:
                            if anno_inicio == anno_fin and mes_fin < 3:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_marzo'] and datos[0]['cant_marzo'] != 0:
                                dict_media['3'] = datos[0]['total_marzo'] / datos[0]['cant_marzo']
                        if mes_inicio < 5:
                            if anno_inicio == anno_fin and mes_fin < 4:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_abril'] and datos[0]['cant_abril'] != 0:
                                dict_media['4'] = datos[0]['total_abril'] / datos[0]['cant_abril']
                        if mes_inicio < 6:
                            if anno_inicio == anno_fin and mes_fin < 5:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_mayo'] and datos[0]['cant_mayo'] != 0:
                                dict_media['5'] = datos[0]['total_mayo'] / datos[0]['cant_mayo']
                        if mes_inicio < 7:
                            if anno_inicio == anno_fin and mes_fin < 6:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_junio'] and datos[0]['cant_junio'] != 0:
                                dict_media['6'] = datos[0]['total_junio'] / datos[0]['cant_junio']
                        if mes_inicio < 8:
                            if anno_inicio == anno_fin and mes_fin < 7:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_julio'] and datos[0]['cant_julio'] != 0:
                                dict_media['7'] = datos[0]['total_julio'] / datos[0]['cant_julio']
                        if mes_inicio < 9:
                            if anno_inicio == anno_fin and mes_fin < 8:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_agosto'] and datos[0]['cant_agosto'] != 0:
                                dict_media['8'] = datos[0]['total_agosto'] / datos[0]['cant_agosto']
                        if mes_inicio < 10:
                            if anno_inicio == anno_fin and mes_fin < 9:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_septiembre'] and datos[0]['cant_septiembre'] != 0:
                                dict_media['9'] = datos[0]['total_septiembre'] / datos[0]['cant_septiembre']
                        if mes_inicio < 11:
                            if anno_inicio == anno_fin and mes_fin < 10:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_octubre'] and datos[0]['cant_octubre'] != 0:
                                dict_media['10'] = datos[0]['total_octubre'] / datos[0]['cant_octubre']
                        if mes_inicio < 12:
                            if anno_inicio == anno_fin and mes_fin < 11:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_noviembre'] and datos[0]['cant_noviembre'] != 0:
                                dict_media['11'] = datos[0]['total_noviembre'] / datos[0]['cant_noviembre']
                        if mes_inicio < 13:
                            if anno_inicio == anno_fin and mes_fin < 12:
                                dict_media['anno'] = current_year
                                dict_media['id'] = id
                                arreglo_bloque.append(dict_media)
                                current_year += 1
                                continue
                            if datos[0]['total_diciembre'] and datos[0]['cant_diciembre'] != 0:
                                dict_media['12'] = datos[0]['total_diciembre'] / datos[0]['cant_diciembre']

                    if datos[0]['anno'] > anno_inicio and datos[0]['anno'] < anno_fin:
                        if datos[0]['total_enero'] and datos[0]['cant_enero'] != 0:
                            dict_media['1'] = datos[0]['total_enero'] / datos[0]['cant_enero']
                        if datos[0]['total_febrero'] and datos[0]['cant_febrero'] != 0:
                            dict_media['2'] = datos[0]['total_febrero'] / datos[0]['cant_febrero']
                        if datos[0]['total_marzo'] and datos[0]['cant_marzo'] != 0:
                            dict_media['3'] = datos[0]['total_marzo'] / datos[0]['cant_marzo']
                        if datos[0]['total_abril'] and datos[0]['cant_abril'] != 0:
                            dict_media['4'] = datos[0]['total_abril'] / datos[0]['cant_abril']
                        if datos[0]['total_mayo'] and datos[0]['cant_mayo'] != 0:
                            dict_media['5'] = datos[0]['total_mayo'] / datos[0]['cant_mayo']
                        if datos[0]['total_junio'] and datos[0]['cant_junio'] != 0:
                            dict_media['6'] = datos[0]['total_junio'] / datos[0]['cant_junio']
                        if datos[0]['total_julio'] and datos[0]['cant_julio'] != 0:
                            dict_media['7'] = datos[0]['total_julio'] / datos[0]['cant_julio']
                        if datos[0]['total_agosto'] and datos[0]['cant_agosto'] != 0:
                            dict_media['8'] = datos[0]['total_agosto'] / datos[0]['cant_agosto']
                        if datos[0]['total_septiembre'] and datos[0]['cant_septiembre'] != 0:
                            dict_media['9'] = datos[0]['total_septiembre'] / datos[0]['cant_septiembre']
                        if datos[0]['total_octubre'] and datos[0]['cant_octubre'] != 0:
                            dict_media['10'] = datos[0]['total_octubre'] / datos[0]['cant_octubre']
                        if datos[0]['total_noviembre'] and datos[0]['cant_noviembre'] != 0:
                            dict_media['11'] = datos[0]['total_noviembre'] / datos[0]['cant_noviembre']
                        if datos[0]['total_diciembre'] and datos[0]['cant_diciembre'] != 0:
                            dict_media['12'] = datos[0]['total_diciembre'] / datos[0]['cant_diciembre']

                    if datos[0]['anno'] == anno_fin and anno_inicio != anno_fin:
                        if mes_fin > 0:
                            if datos[0]['total_enero'] and datos[0]['cant_enero'] != 0:
                                dict_media['1'] = datos[0]['total_enero'] / datos[0]['cant_enero']
                        if mes_fin > 1:
                            if datos[0]['total_febrero'] and datos[0]['cant_febrero'] != 0:
                                dict_media['2'] = datos[0]['total_febrero'] / datos[0]['cant_febrero']
                        if mes_fin > 2:
                            if datos[0]['total_marzo'] and datos[0]['cant_marzo'] != 0:
                                dict_media['3'] = datos[0]['total_marzo'] / datos[0]['cant_marzo']
                        if mes_fin > 3:
                            if datos[0]['total_abril'] and datos[0]['cant_abril'] != 0:
                                dict_media['4'] = datos[0]['total_abril'] / datos[0]['cant_abril']
                        if mes_fin > 4:
                            if datos[0]['total_mayo'] and datos[0]['cant_mayo'] != 0:
                                dict_media['5'] = datos[0]['total_mayo'] / datos[0]['cant_mayo']
                        if mes_fin > 5:
                            if datos[0]['total_junio'] and datos[0]['cant_junio'] != 0:
                                dict_media['6'] = datos[0]['total_junio'] / datos[0]['cant_junio']
                        if mes_fin > 6:
                            if datos[0]['total_julio'] and datos[0]['cant_julio'] != 0:
                                dict_media['7'] = datos[0]['total_julio'] / datos[0]['cant_julio']
                        if mes_fin > 7:
                            if datos[0]['total_agosto'] and datos[0]['cant_agosto'] != 0:
                                dict_media['8'] = datos[0]['total_agosto'] / datos[0]['cant_agosto']
                        if mes_fin > 8:
                            if datos[0]['total_septiembre'] and datos[0]['cant_septiembre'] != 0:
                                dict_media['9'] = datos[0]['total_septiembre'] / datos[0]['cant_septiembre']
                        if mes_fin > 9:
                            if datos[0]['total_octubre'] and datos[0]['cant_octubre'] != 0:
                                dict_media['10'] = datos[0]['total_octubre'] / datos[0]['cant_octubre']
                        if mes_fin > 10:
                            if datos[0]['total_noviembre'] and datos[0]['cant_noviembre'] != 0:
                                dict_media['11'] = datos[0]['total_noviembre'] / datos[0]['cant_noviembre']
                        if mes_fin > 11:
                            if datos[0]['total_diciembre'] and datos[0]['cant_diciembre'] != 0:
                                dict_media['12'] = datos[0]['total_diciembre'] / datos[0]['cant_diciembre']
                dict_media['anno'] = current_year
                dict_media['id'] = id
                arreglo_bloque.append(dict_media)
                current_year += 1
            res.append(arreglo_bloque)
        return res

    def _calcular_media_bloque_sin_rango_fecha(self, ids, pozo_ids):
        res = []
        for id in ids:
            arreglo_bloque = []
            datos = self._valores_sin_rango_fechas(id, pozo_ids)
            cant = len(datos)
            cont = 0
            while cont < cant:
                dict_media = {}
                dict_media['anno'] = datos[cont]['anno']
                dict_media['id'] = id
                if datos[cont]['media_enero']:
                    dict_media['1'] = datos[cont]['media_enero']
                if datos[cont]['media_febrero']:
                    dict_media['2'] = datos[cont]['media_febrero']
                if datos[cont]['media_marzo']:
                    dict_media['3'] = datos[cont]['media_marzo']
                if datos[cont]['media_abril']:
                    dict_media['4'] = datos[cont]['media_abril']
                if datos[cont]['media_mayo']:
                    dict_media['5'] = datos[cont]['media_mayo']
                if datos[cont]['media_junio']:
                    dict_media['6'] = datos[cont]['media_junio']
                if datos[cont]['media_julio']:
                    dict_media['7'] = datos[cont]['media_julio']
                if datos[cont]['media_agosto']:
                    dict_media['8'] = datos[cont]['media_agosto']
                if datos[cont]['media_septiembre']:
                    dict_media['9'] = datos[cont]['media_septiembre']
                if datos[cont]['media_octubre']:
                    dict_media['10'] = datos[cont]['media_octubre']
                if datos[cont]['media_noviembre']:
                    dict_media['11'] = datos[cont]['media_noviembre']
                if datos[cont]['media_diciembre']:
                    dict_media['12'] = datos[cont]['media_diciembre']
                cont += 1
                arreglo_bloque.append(dict_media)
            res.append(arreglo_bloque)
        return res

    def calcular_media_aritmetica(self, ids, pozo_ids, fecha_inicio, fecha_fin):
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                temp = fecha_fin
                fecha_fin = fecha_inicio
                fecha_inicio = temp
            res = self._calcular_media_bloque_rango_fecha(ids, pozo_ids, fecha_inicio, fecha_fin)
        else:
            res = self._calcular_media_bloque_sin_rango_fecha(ids, pozo_ids)
        return res

    def calcular_media_por_formula(self, ids, pozo_ids, fecha_inicio, fecha_fin):
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                temp = fecha_fin
                fecha_fin = fecha_inicio
                fecha_inicio = temp
            res = self._calcular_media_bloque_rango_fecha(ids, pozo_ids, fecha_inicio, fecha_fin)
        else:
            res = self._calcular_media_bloque_sin_rango_fecha(ids, pozo_ids)
        cantidad = len(res)
        contador = 0
        while contador < cantidad:
            cant = len(res[contador])
            cont = 0
            while cont < cant:
                cont_meses = 1
                while cont_meses <= 12:
                    if res[contador][cont].get(str(cont_meses)):
                        a_cero = a_uno = 0
                        if res[contador][cont].get('id'):
                            obj_id = res[contador][cont]['id']
                            obj = self.browse(obj_id)
                            a_cero = obj.a0
                            a_uno = obj.a1
                        valor = a_cero + a_uno * res[contador][cont][str(cont_meses)]
                        res[contador][cont][str(cont_meses)] = valor
                    cont_meses += 1
                cont += 1
            contador += 1
        return res

    def max_min(self, ids, pozo_ids, fecha_inicio, fecha_fin, tipo):
        res = {'id': '', 'nombre': '', 'valor_min': 999999.11, 'valor_max': 999999.11}
        existe = False
        variable = 0
        #global encontro
        encontro = 0
        temp = 0
        # tipo = 'aritmetica'
        # fecha_inicio =None
        # fecha_fin = None
        datos_generales = []
        if tipo == 'aritmetica':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio, fecha_fin)
        if tipo == 'formula':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio, fecha_fin)
        if datos_vistas:
            for id in ids:
                cont = 0
                pos = variable
                while cont < len(datos_vistas[pos]):
                    if encontro == 1:
                        break
                    valor = 0
                    if len(datos_vistas[pos][cont]) > 2:
                        for llave in datos_vistas[pos][cont]:
                            if llave != 'anno' and llave != 'id':
                                min = list(datos_vistas[pos][cont].values())[valor]
                                anno_minimo = datos_vistas[pos][cont]['anno']
                                mes_minimo = list(datos_vistas[pos][cont].keys())[valor]
                                anno_maximo = datos_vistas[pos][cont]['anno']
                                mes_maximo = list(datos_vistas[pos][cont].keys())[valor]
                                max = 0.0
                                existe = True
                                encontro = 1
                                break
                            valor += 1
                        cont += 1
                    else:
                        cont += 1
                if existe:
                    for datos_vista in datos_vistas[temp]:
                        if len(datos_vista) > 2:
                            aux = -1
                            aux1 = -1
                            for var in datos_vista.keys():
                                if var == 'anno':
                                    aux += 1
                                    break
                                else:
                                    aux += 1
                            clave = list(datos_vista.keys())
                            clave.pop(aux)
                            clave_temp = clave
                            for var in clave_temp:
                                if var == 'id':
                                    aux1 += 1
                                    break
                                else:
                                    aux1 += 1
                            clave.pop(aux1)
                            listas = []
                            for clave_aux in clave:
                                valor_clave = int(clave_aux)
                                listas.append(valor_clave)
                            listas.sort()
                            for lista in listas:
                                valor = datos_vista[str(lista)]
                                if valor < min:
                                    min = valor
                                    anno_minimo = datos_vista['anno']
                                    mes_minimo = lista
                                if valor > max:
                                    max = valor
                                    anno_maximo = datos_vista['anno']
                                    mes_maximo = lista
                    res = {'valor_min': min, 'valor_max': max, 'Amin': anno_minimo, 'Mmin': mes_minimo,
                           'Amax': anno_maximo, 'Mmax': mes_maximo, 'id': id}
                    variable += 1
                    temp += 1
                    datos_generales.append(res)
                    existe = False
                    encontro = 0
                else:
                    datos_generales.append(res)
                    variable += 1
                    temp += 1
                    existe = False
                    encontro = 0
        else:
            datos_generales.append(res)
        encontro = 0
        return datos_generales

    def altura(self, ids, pozo_ids, fecha_inicio, fecha_fin, tipo):
        datos_generales = []
        temp = 0
        if tipo == 'aritmetica':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio, fecha_fin)
        if tipo == 'formula':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio, fecha_fin)
        if datos_vistas:
            for id in self:
                if fecha_inicio == None and fecha_fin == None:
                    dict_max = self.max_min( [id], pozo_ids, None, None, tipo)
                else:
                    dict_max = self.max_min( [id], pozo_ids, fecha_inicio, fecha_fin, tipo)
                max = dict_max[0]['valor_max']
                max_fijo = self.browse( id).maximo_h_periodo_fijo
                for datos_vista in datos_vistas[temp]:
                    dict_altura = {}
                    if datos_vista.get('1'):
                        if max_fijo <= 0.0:
                            dict_altura['1'] = max - datos_vista['1']
                        else:
                            dict_altura['1'] = max_fijo - datos_vista['1']
                    if datos_vista.get('2'):
                        if max_fijo <= 0.0:
                            dict_altura['2'] = max - datos_vista['2']
                        else:
                            dict_altura['2'] = max_fijo - datos_vista['2']
                    if datos_vista.get('3'):
                        if max_fijo <= 0.0:
                            dict_altura['3'] = max - datos_vista['3']
                        else:
                            dict_altura['3'] = max_fijo - datos_vista['3']
                    if datos_vista.get('4'):
                        if max_fijo <= 0.0:
                            dict_altura['4'] = max - datos_vista['4']
                        else:
                            dict_altura['4'] = max_fijo - datos_vista['4']
                    if datos_vista.get('5'):
                        if max_fijo <= 0.0:
                            dict_altura['5'] = max - datos_vista['5']
                        else:
                            dict_altura['5'] = max_fijo - datos_vista['5']
                    if datos_vista.get('6'):
                        if max_fijo <= 0.0:
                            dict_altura['6'] = max - datos_vista['6']
                        else:
                            dict_altura['6'] = max_fijo - datos_vista['6']
                    if datos_vista.get('7'):
                        if max_fijo <= 0.0:
                            dict_altura['7'] = max - datos_vista['7']
                        else:
                            dict_altura['7'] = max_fijo - datos_vista['7']
                    if datos_vista.get('8'):
                        if max_fijo <= 0.0:
                            dict_altura['8'] = max - datos_vista['8']
                        else:
                            dict_altura['8'] = max_fijo - datos_vista['8']
                    if datos_vista.get('9'):
                        if max_fijo <= 0.0:
                            dict_altura['9'] = max - datos_vista['9']
                        else:
                            dict_altura['9'] = max_fijo - datos_vista['9']
                    if datos_vista.get('10'):
                        if max_fijo <= 0.0:
                            dict_altura['10'] = max - datos_vista['10']
                        else:
                            dict_altura['10'] = max_fijo - datos_vista['10']
                    if datos_vista.get('11'):
                        if max_fijo <= 0.0:
                            dict_altura['11'] = max - datos_vista['11']
                        else:
                            dict_altura['11'] = max_fijo - datos_vista['11']
                    if datos_vista.get('12'):
                        if max_fijo <= 0.0:
                            dict_altura['12'] = max - datos_vista['12']
                        else:
                            dict_altura['12'] = max_fijo - datos_vista['12']
                    dict_altura['anno'] = datos_vista['anno']
                    dict_altura['id'] = id
                    datos_generales.append(dict_altura)
                temp += 1
        return datos_generales

    def volumen(self, ids, pozo_ids, fecha_inicio, fecha_fin, tipo):
        datos_generales = []
        temp = 0
        if tipo == 'aritmetica':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio, fecha_fin)
        if tipo == 'formula':
            if fecha_inicio == None and fecha_fin == None:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)
            else:
                datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio, fecha_fin)
        if datos_vistas:
            for id in ids:
                coeficiente_no_calculado = self.browse(id).coeficiente_almacenamiento
                cof_aprov = self.browse(id).coeficiente_aprovechamiento_hidraulico
                area = self.browse(id).area
                max_fijo = self.browse(id).maximo_h_periodo_fijo
                if fecha_inicio == None and fecha_fin == None:
                    dict_max = self.max_min([id], pozo_ids, None, None, tipo)
                else:
                    dict_max = self.max_min([id], pozo_ids, fecha_inicio, fecha_fin, tipo)
                max = dict_max[0]['valor_max']
                rec_explotable = self.browse(id).recurso_explotable
                if tipo == 'formula':
                    deltaH = 2 * (self.browse(id).promedio_h_periodo_formula)
                    coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000)
                else:
                    deltaH = 2 * (self.browse(id).promedio_h_periodo)
                    coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000)
                if coeficiente_calculado > 0.0:
                    coeficiente = round(coeficiente_calculado, 3)
                else:
                    coeficiente = round(coeficiente_no_calculado, 3)
                for datos_vista in datos_vistas[temp]:
                    dict_altura = {}
                    if datos_vista.get('1'):
                        if max_fijo <= 0.0:
                            dict_altura['1'] = (coeficiente * (max - datos_vista['1']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['1'] = (coeficiente * (max_fijo - datos_vista['1']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('2'):
                        if max_fijo <= 0.0:
                            dict_altura['2'] = (coeficiente * (max - datos_vista['2']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['2'] = (coeficiente * (max_fijo - datos_vista['2']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('3'):
                        if max_fijo <= 0.0:
                            dict_altura['3'] = (coeficiente * (max - datos_vista['3']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['3'] = (coeficiente * (max_fijo - datos_vista['3']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('4'):
                        if max_fijo <= 0.0:
                            dict_altura['4'] = (coeficiente * (max - datos_vista['4']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['4'] = (coeficiente * (max_fijo - datos_vista['4']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('5'):
                        if max_fijo <= 0.0:
                            dict_altura['5'] = (coeficiente * (max - datos_vista['5']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['5'] = (coeficiente * (max_fijo - datos_vista['5']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('6'):
                        if max_fijo <= 0.0:
                            dict_altura['6'] = (coeficiente * (max - datos_vista['6']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['6'] = (coeficiente * (max_fijo - datos_vista['6']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('7'):
                        if max_fijo <= 0.0:
                            dict_altura['7'] = (coeficiente * (max - datos_vista['7']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['7'] = (coeficiente * (max_fijo - datos_vista['7']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('8'):
                        if max_fijo <= 0.0:
                            dict_altura['8'] = (coeficiente * (max - datos_vista['8']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['8'] = (coeficiente * (max_fijo - datos_vista['8']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('9'):
                        if max_fijo <= 0.0:
                            dict_altura['9'] = (coeficiente * (max - datos_vista['9']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['9'] = (coeficiente * (max_fijo - datos_vista['9']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('10'):
                        if max_fijo <= 0.0:
                            dict_altura['10'] = (coeficiente * (max - datos_vista['10']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['10'] = (coeficiente * (max_fijo - datos_vista['10']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('11'):
                        if max_fijo <= 0.0:
                            dict_altura['11'] = (coeficiente * (max - datos_vista['11']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['11'] = (coeficiente * (max_fijo - datos_vista['11']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista.get('12'):
                        if max_fijo <= 0.0:
                            dict_altura['12'] = (coeficiente * (max - datos_vista['12']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                        else:
                            dict_altura['12'] = (coeficiente * (max_fijo - datos_vista['12']) * (
                                    area * 1000000)) / 1000000 * cof_aprov
                    dict_altura['anno'] = datos_vista['anno']
                    dict_altura['id'] = id
                    datos_generales.append(dict_altura)
                temp += 1
        return datos_generales

    #
    # ###metodo viejo que hala los valores de los pozos
    # # def _valores_explotacion(self, cr, uid, id, pozo_ids, anno, context=None):
    # #
    # #     query = """SELECT
    # #                       df_explotacion_anual_pozo.anno,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_enero, -999999.110)) as total_enero,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_febrero, -999999.110)) as total_febrero,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_marzo, -999999.110)) as total_marzo,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_abril, -999999.110)) as total_abril,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_mayo, -999999.110)) as total_mayo,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_junio, -999999.110)) as total_junio,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_julio, -999999.110)) as total_julio,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_agosto, -999999.110)) as total_agosto,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_septiembre, -999999.110)) as total_septiembre,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_octubre, -999999.110)) as total_octubre,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_noviembre, -999999.110)) as total_noviembre,
    # #                       SUM(NULLIF(df_explotacion_anual_pozo.media_hiperanual_diciembre, -999999.110)) as total_diciembre
    # #                     FROM
    # #                       df_pozo,
    # #                       df_bloque,
    # #                       df_explotacion_anual_pozo
    # #                     WHERE
    # #                       df_bloque.id = %s AND
    # #                       df_pozo.bloque_id = df_bloque.id AND
    # #                       df_explotacion_anual_pozo.pozo_id = df_pozo.id AND """
    # #     if pozo_ids:
    # #         query += """df_pozo.id in %s"""
    # #     if anno:
    # #         query+= """ AND df_explotacion_anual_pozo.anno = %s"""
    # #     query += """ GROUP BY df_bloque.id, df_explotacion_anual_pozo.anno"""
    # #
    # #     if pozo_ids and anno:
    # #         cr.execute(query, (id, (tuple(pozo_ids)),anno))
    # #     elif pozo_ids or anno:
    # #         if pozo_ids:
    # #             cr.execute(query, (id, (tuple(pozo_ids))))
    # #         elif anno:
    # #             cr.execute(query, (id,anno))
    # #     else:
    # #         cr.execute(query, (id))
    # #
    # #     return cr.dictfetchall()
    #
    #
    # ###metodo nuevo que hala los datos del objeto en cuestion
    def _valores_explotacion(self, id, anno):

        query = """SELECT
                          df_explotacion_bloque_real.anno,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_enero, -999999.110)) as total_enero,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_febrero, -999999.110)) as total_febrero,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_marzo, -999999.110)) as total_marzo,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_abril, -999999.110)) as total_abril,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_mayo, -999999.110)) as total_mayo,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_junio, -999999.110)) as total_junio,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_julio, -999999.110)) as total_julio,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_agosto, -999999.110)) as total_agosto,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_septiembre, -999999.110)) as total_septiembre,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_octubre, -999999.110)) as total_octubre,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_noviembre, -999999.110)) as total_noviembre,
                          SUM(NULLIF(df_explotacion_bloque_real.media_hiperanual_diciembre, -999999.110)) as total_diciembre
                        FROM
                          df_bloque,
                          df_explotacion_bloque_real
                        WHERE
                          df_bloque.id = %s AND
                          df_explotacion_bloque_real.bloque_id = df_bloque.id"""
        if anno:
            query += """ AND df_explotacion_bloque_real.anno = %s"""
        query += """ GROUP BY df_bloque.id, df_explotacion_bloque_real.anno"""

        if anno:
            self.env.cr.execute(query, (id, anno))
        else:
            self.env.cr.execute(query, str(id))

        return self.env.cr.dictfetchall()

    #
    # # def _calcular_explotacion_rango_fecha(self, cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context=None):
    def _calcular_explotacion_rango_fecha(self, ids, fecha_inicio, fecha_fin):
        res = []
        anno_inicio = fecha_inicio.year
        anno_fin = fecha_fin.year
        mes_inicio = fecha_inicio.month
        mes_fin = fecha_fin.month
        for id in ids:
            current_year = fecha_inicio.year
            arreglo_bloque = []
            while current_year <= anno_fin:
                # datos = self._valores_explotacion(cr, uid, id, pozo_ids, current_year, context)
                datos = self._valores_explotacion(id, current_year)
                dict_explotacion = {}
                if datos:
                    if datos[0]['anno'] == anno_inicio:
                        if mes_inicio < 2:
                            if anno_inicio == anno_fin and mes_fin < 1:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_enero'] != 0:
                                dict_explotacion['1'] = datos[0]['total_enero']
                        if mes_inicio < 3:
                            if anno_inicio == anno_fin and mes_fin < 2:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_febrero'] != 0:
                                dict_explotacion['2'] = datos[0]['total_febrero']
                        if mes_inicio < 4:
                            if anno_inicio == anno_fin and mes_fin < 3:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_marzo'] != 0:
                                dict_explotacion['3'] = datos[0]['total_marzo']
                        if mes_inicio < 5:
                            if anno_inicio == anno_fin and mes_fin < 4:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_abril'] != 0:
                                dict_explotacion['4'] = datos[0]['total_abril']
                        if mes_inicio < 6:
                            if anno_inicio == anno_fin and mes_fin < 5:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_mayo'] != 0:
                                dict_explotacion['5'] = datos[0]['total_mayo']
                        if mes_inicio < 7:
                            if anno_inicio == anno_fin and mes_fin < 6:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_junio'] != 0:
                                dict_explotacion['6'] = datos[0]['total_junio']
                        if mes_inicio < 8:
                            if anno_inicio == anno_fin and mes_fin < 7:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_julio'] != 0:
                                dict_explotacion['7'] = datos[0]['total_julio']
                        if mes_inicio < 9:
                            if anno_inicio == anno_fin and mes_fin < 8:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_agosto'] != 0:
                                dict_explotacion['8'] = datos[0]['total_agosto']
                        if mes_inicio < 10:
                            if anno_inicio == anno_fin and mes_fin < 9:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_septiembre'] != 0:
                                dict_explotacion['9'] = datos[0]['total_septiembre']
                        if mes_inicio < 11:
                            if anno_inicio == anno_fin and mes_fin < 10:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_octubre'] != 0:
                                dict_explotacion['10'] = datos[0]['total_octubre']
                        if mes_inicio < 12:
                            if anno_inicio == anno_fin and mes_fin < 11:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_noviembre'] != 0:
                                dict_explotacion['11'] = datos[0]['total_noviembre']
                        if mes_inicio < 13:
                            if anno_inicio == anno_fin and mes_fin < 12:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_diciembre'] != 0:
                                dict_explotacion['12'] = datos[0]['total_diciembre']

                    if datos[0]['anno'] > anno_inicio and datos[0]['anno'] < anno_fin:
                        if datos[0]['total_enero'] != 0:
                            dict_explotacion['1'] = datos[0]['total_enero']
                        if datos[0]['total_febrero'] != 0:
                            dict_explotacion['2'] = datos[0]['total_febrero']
                        if datos[0]['total_marzo'] != 0:
                            dict_explotacion['3'] = datos[0]['total_marzo']
                        if datos[0]['total_abril'] != 0:
                            dict_explotacion['4'] = datos[0]['total_abril']
                        if datos[0]['total_mayo'] != 0:
                            dict_explotacion['5'] = datos[0]['total_mayo']
                        if datos[0]['total_junio'] != 0:
                            dict_explotacion['6'] = datos[0]['total_junio']
                        if datos[0]['total_julio'] != 0:
                            dict_explotacion['7'] = datos[0]['total_julio']
                        if datos[0]['total_agosto'] != 0:
                            dict_explotacion['8'] = datos[0]['total_agosto']
                        if datos[0]['total_septiembre'] != 0:
                            dict_explotacion['9'] = datos[0]['total_septiembre']
                        if datos[0]['total_octubre'] != 0:
                            dict_explotacion['10'] = datos[0]['total_octubre']
                        if datos[0]['total_noviembre'] != 0:
                            dict_explotacion['11'] = datos[0]['total_noviembre']
                        if datos[0]['total_diciembre'] != 0:
                            dict_explotacion['12'] = datos[0]['total_diciembre']

                    if datos[0]['anno'] == anno_fin and anno_inicio != anno_fin:
                        if mes_fin > 0:
                            if datos[0]['total_enero'] != 0:
                                dict_explotacion['1'] = datos[0]['total_enero']
                        if mes_fin > 1:
                            if datos[0]['total_febrero'] != 0:
                                dict_explotacion['2'] = datos[0]['total_febrero']
                        if mes_fin > 2:
                            if datos[0]['total_marzo'] != 0:
                                dict_explotacion['3'] = datos[0]['total_marzo']
                        if mes_fin > 3:
                            if datos[0]['total_abril'] != 0:
                                dict_explotacion['4'] = datos[0]['total_abril']
                        if mes_fin > 4:
                            if datos[0]['total_mayo'] != 0:
                                dict_explotacion['5'] = datos[0]['total_mayo']
                        if mes_fin > 5:
                            if datos[0]['total_junio'] != 0:
                                dict_explotacion['6'] = datos[0]['total_junio']
                        if mes_fin > 6:
                            if datos[0]['total_julio'] != 0:
                                dict_explotacion['7'] = datos[0]['total_julio']
                        if mes_fin > 7:
                            if datos[0]['total_agosto'] != 0:
                                dict_explotacion['8'] = datos[0]['total_agosto']
                        if mes_fin > 8:
                            if datos[0]['total_septiembre'] != 0:
                                dict_explotacion['9'] = datos[0]['total_septiembre']
                        if mes_fin > 9:
                            if datos[0]['total_octubre'] != 0:
                                dict_explotacion['10'] = datos[0]['total_octubre']
                        if mes_fin > 10:
                            if datos[0]['total_noviembre'] != 0:
                                dict_explotacion['11'] = datos[0]['total_noviembre']
                        if mes_fin > 11:
                            if datos[0]['total_diciembre'] != 0:
                                dict_explotacion['12'] = datos[0]['total_diciembre']
                dict_explotacion['anno'] = current_year
                dict_explotacion['id'] = id
                arreglo_bloque.append(dict_explotacion)
                current_year += 1
            res.append(arreglo_bloque)
        return res

    #
    # # def _calcular_explotacion_sin_rango_fecha(self, cr, uid, ids, pozo_ids, context=None):
    def _calcular_explotacion_sin_rango_fecha(self, ids):
        res = []
        for id in ids:
            arreglo_bloque = []
            datos = self._valores_explotacion( id, None)
            cant = len(datos)
            cont = 0
            while cont < cant:
                dict_explotacion = {}
                dict_explotacion['anno'] = datos[cont]['anno']
                dict_explotacion['id'] = id
                if datos[cont]['total_enero']:
                    dict_explotacion['1'] = datos[cont]['total_enero']
                if datos[cont]['total_febrero']:
                    dict_explotacion['2'] = datos[cont]['total_febrero']
                if datos[cont]['total_marzo']:
                    dict_explotacion['3'] = datos[cont]['total_marzo']
                if datos[cont]['total_abril']:
                    dict_explotacion['4'] = datos[cont]['total_abril']
                if datos[cont]['total_mayo']:
                    dict_explotacion['5'] = datos[cont]['total_mayo']
                if datos[cont]['total_junio']:
                    dict_explotacion['6'] = datos[cont]['total_junio']
                if datos[cont]['total_julio']:
                    dict_explotacion['7'] = datos[cont]['total_julio']
                if datos[cont]['total_agosto']:
                    dict_explotacion['8'] = datos[cont]['total_agosto']
                if datos[cont]['total_septiembre']:
                    dict_explotacion['9'] = datos[cont]['total_septiembre']
                if datos[cont]['total_octubre']:
                    dict_explotacion['10'] = datos[cont]['total_octubre']
                if datos[cont]['total_noviembre']:
                    dict_explotacion['11'] = datos[cont]['total_noviembre']
                if datos[cont]['total_diciembre']:
                    dict_explotacion['12'] = datos[cont]['total_diciembre']
                cont += 1
                arreglo_bloque.append(dict_explotacion)
            res.append(arreglo_bloque)
        return res

    #
    # # def calcular_explotacion_acumulada(self, cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context=None):
    def calcular_explotacion_acumulada(self, ids, fecha_inicio, fecha_fin):
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                temp = fecha_fin
                fecha_fin = fecha_inicio
                fecha_inicio = temp
            # res = self._calcular_explotacion_rango_fecha(cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context)
            res = self._calcular_explotacion_rango_fecha(ids, fecha_inicio, fecha_fin)
        else:
            # res = self._calcular_explotacion_sin_rango_fecha(cr, uid, ids, pozo_ids, context)
            res = self._calcular_explotacion_sin_rango_fecha(ids)
        return res

    #
    #
    # # def _valores_plan_explotacion(self, cr, uid, id, pozo_ids, anno, context=None):
    def _valores_plan_explotacion(self, id, anno):

        query = """SELECT
                          df_explotacion_bloque_plan.anno,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_enero, -999999.110)) as total_enero,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_febrero, -999999.110)) as total_febrero,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_marzo, -999999.110)) as total_marzo,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_abril, -999999.110)) as total_abril,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_mayo, -999999.110)) as total_mayo,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_junio, -999999.110)) as total_junio,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_julio, -999999.110)) as total_julio,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_agosto, -999999.110)) as total_agosto,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_septiembre, -999999.110)) as total_septiembre,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_octubre, -999999.110)) as total_octubre,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_noviembre, -999999.110)) as total_noviembre,
                          SUM(NULLIF(df_explotacion_bloque_plan.media_hiperanual_diciembre, -999999.110)) as total_diciembre
                        FROM
                          df_bloque,
                          df_explotacion_bloque_plan
                        WHERE
                          df_bloque.id = %s AND
                          df_explotacion_bloque_plan.bloque_id = df_bloque.id"""
        if anno:
            query += """ AND df_explotacion_bloque_plan.anno = %s"""
        query += """ GROUP BY df_bloque.id, df_explotacion_bloque_plan.anno"""

        if anno:
            self.env.cr.execute(query, (id, anno))
        else:
            self.env.cr.execute(query, str(id))

        return self.env.cr.dictfetchall()

    #
    # # def _plan_explotacion_rango_fecha(self, cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context=None):
    def _plan_explotacion_rango_fecha(self, ids, fecha_inicio, fecha_fin):
        res = []
        anno_inicio = fecha_inicio.year
        anno_fin = fecha_fin.year
        mes_inicio = fecha_inicio.month
        mes_fin = fecha_fin.month
        for id in ids:
            current_year = fecha_inicio.year
            arreglo_bloque = []
            while current_year <= anno_fin:
                # datos = self._valores_plan_explotacion(cr, uid, id, pozo_ids, current_year, context)
                datos = self._valores_plan_explotacion(id, current_year)
                dict_explotacion = {}
                if datos:
                    if datos[0]['anno'] == anno_inicio:
                        if mes_inicio < 2:
                            if anno_inicio == anno_fin and mes_fin < 1:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_enero'] != 0:
                                dict_explotacion['1'] = datos[0]['total_enero']
                        if mes_inicio < 3:
                            if anno_inicio == anno_fin and mes_fin < 2:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_febrero'] != 0:
                                dict_explotacion['2'] = datos[0]['total_febrero']
                        if mes_inicio < 4:
                            if anno_inicio == anno_fin and mes_fin < 3:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_marzo'] != 0:
                                dict_explotacion['3'] = datos[0]['total_marzo']
                        if mes_inicio < 5:
                            if anno_inicio == anno_fin and mes_fin < 4:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_abril'] != 0:
                                dict_explotacion['4'] = datos[0]['total_abril']
                        if mes_inicio < 6:
                            if anno_inicio == anno_fin and mes_fin < 5:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_mayo'] != 0:
                                dict_explotacion['5'] = datos[0]['total_mayo']
                        if mes_inicio < 7:
                            if anno_inicio == anno_fin and mes_fin < 6:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_junio'] != 0:
                                dict_explotacion['6'] = datos[0]['total_junio']
                        if mes_inicio < 8:
                            if anno_inicio == anno_fin and mes_fin < 7:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_julio'] != 0:
                                dict_explotacion['7'] = datos[0]['total_julio']
                        if mes_inicio < 9:
                            if anno_inicio == anno_fin and mes_fin < 8:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_agosto'] != 0:
                                dict_explotacion['8'] = datos[0]['total_agosto']
                        if mes_inicio < 10:
                            if anno_inicio == anno_fin and mes_fin < 9:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_septiembre'] != 0:
                                dict_explotacion['9'] = datos[0]['total_septiembre']
                        if mes_inicio < 11:
                            if anno_inicio == anno_fin and mes_fin < 10:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_octubre'] != 0:
                                dict_explotacion['10'] = datos[0]['total_octubre']
                        if mes_inicio < 12:
                            if anno_inicio == anno_fin and mes_fin < 11:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_noviembre'] != 0:
                                dict_explotacion['11'] = datos[0]['total_noviembre']
                        if mes_inicio < 13:
                            if anno_inicio == anno_fin and mes_fin < 12:
                                dict_explotacion['anno'] = current_year
                                dict_explotacion['id'] = id
                                arreglo_bloque.append(dict_explotacion)
                                current_year += 1
                                continue
                            if datos[0]['total_diciembre'] != 0:
                                dict_explotacion['12'] = datos[0]['total_diciembre']

                    if datos[0]['anno'] > anno_inicio and datos[0]['anno'] < anno_fin:
                        if datos[0]['total_enero'] != 0:
                            dict_explotacion['1'] = datos[0]['total_enero']
                        if datos[0]['total_febrero'] != 0:
                            dict_explotacion['2'] = datos[0]['total_febrero']
                        if datos[0]['total_marzo'] != 0:
                            dict_explotacion['3'] = datos[0]['total_marzo']
                        if datos[0]['total_abril'] != 0:
                            dict_explotacion['4'] = datos[0]['total_abril']
                        if datos[0]['total_mayo'] != 0:
                            dict_explotacion['5'] = datos[0]['total_mayo']
                        if datos[0]['total_junio'] != 0:
                            dict_explotacion['6'] = datos[0]['total_junio']
                        if datos[0]['total_julio'] != 0:
                            dict_explotacion['7'] = datos[0]['total_julio']
                        if datos[0]['total_agosto'] != 0:
                            dict_explotacion['8'] = datos[0]['total_agosto']
                        if datos[0]['total_septiembre'] != 0:
                            dict_explotacion['9'] = datos[0]['total_septiembre']
                        if datos[0]['total_octubre'] != 0:
                            dict_explotacion['10'] = datos[0]['total_octubre']
                        if datos[0]['total_noviembre'] != 0:
                            dict_explotacion['11'] = datos[0]['total_noviembre']
                        if datos[0]['total_diciembre'] != 0:
                            dict_explotacion['12'] = datos[0]['total_diciembre']

                    if datos[0]['anno'] == anno_fin and anno_inicio != anno_fin:
                        if mes_fin > 0:
                            if datos[0]['total_enero'] != 0:
                                dict_explotacion['1'] = datos[0]['total_enero']
                        if mes_fin > 1:
                            if datos[0]['total_febrero'] != 0:
                                dict_explotacion['2'] = datos[0]['total_febrero']
                        if mes_fin > 2:
                            if datos[0]['total_marzo'] != 0:
                                dict_explotacion['3'] = datos[0]['total_marzo']
                        if mes_fin > 3:
                            if datos[0]['total_abril'] != 0:
                                dict_explotacion['4'] = datos[0]['total_abril']
                        if mes_fin > 4:
                            if datos[0]['total_mayo'] != 0:
                                dict_explotacion['5'] = datos[0]['total_mayo']
                        if mes_fin > 5:
                            if datos[0]['total_junio'] != 0:
                                dict_explotacion['6'] = datos[0]['total_junio']
                        if mes_fin > 6:
                            if datos[0]['total_julio'] != 0:
                                dict_explotacion['7'] = datos[0]['total_julio']
                        if mes_fin > 7:
                            if datos[0]['total_agosto'] != 0:
                                dict_explotacion['8'] = datos[0]['total_agosto']
                        if mes_fin > 8:
                            if datos[0]['total_septiembre'] != 0:
                                dict_explotacion['9'] = datos[0]['total_septiembre']
                        if mes_fin > 9:
                            if datos[0]['total_octubre'] != 0:
                                dict_explotacion['10'] = datos[0]['total_octubre']
                        if mes_fin > 10:
                            if datos[0]['total_noviembre'] != 0:
                                dict_explotacion['11'] = datos[0]['total_noviembre']
                        if mes_fin > 11:
                            if datos[0]['total_diciembre'] != 0:
                                dict_explotacion['12'] = datos[0]['total_diciembre']
                dict_explotacion['anno'] = current_year
                dict_explotacion['id'] = id
                arreglo_bloque.append(dict_explotacion)
                current_year += 1
            res.append(arreglo_bloque)
        return res

    #
    # # def _plan_explotacion_sin_rango_fecha(self, cr, uid, ids, pozo_ids, context=None):
    def _plan_explotacion_sin_rango_fecha(self, ids):
        res = []
        for id in ids:
            arreglo_bloque = []
            # datos = self._valores_plan_explotacion(cr, uid, id, pozo_ids, None, context)
            datos = self._valores_plan_explotacion( id, None)
            cant = len(datos)
            cont = 0
            while cont < cant:
                dict_explotacion = {}
                dict_explotacion['anno'] = datos[cont]['anno']
                dict_explotacion['id'] = id
                if datos[cont]['total_enero']:
                    dict_explotacion['1'] = datos[cont]['total_enero']
                if datos[cont]['total_febrero']:
                    dict_explotacion['2'] = datos[cont]['total_febrero']
                if datos[cont]['total_marzo']:
                    dict_explotacion['3'] = datos[cont]['total_marzo']
                if datos[cont]['total_abril']:
                    dict_explotacion['4'] = datos[cont]['total_abril']
                if datos[cont]['total_mayo']:
                    dict_explotacion['5'] = datos[cont]['total_mayo']
                if datos[cont]['total_junio']:
                    dict_explotacion['6'] = datos[cont]['total_junio']
                if datos[cont]['total_julio']:
                    dict_explotacion['7'] = datos[cont]['total_julio']
                if datos[cont]['total_agosto']:
                    dict_explotacion['8'] = datos[cont]['total_agosto']
                if datos[cont]['total_septiembre']:
                    dict_explotacion['9'] = datos[cont]['total_septiembre']
                if datos[cont]['total_octubre']:
                    dict_explotacion['10'] = datos[cont]['total_octubre']
                if datos[cont]['total_noviembre']:
                    dict_explotacion['11'] = datos[cont]['total_noviembre']
                if datos[cont]['total_diciembre']:
                    dict_explotacion['12'] = datos[cont]['total_diciembre']
                cont += 1
                arreglo_bloque.append(dict_explotacion)
            res.append(arreglo_bloque)
        return res

    #
    # # def plan_explotacion(self, cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context=None):
    def plan_explotacion(self, ids, fecha_inicio, fecha_fin):
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                temp = fecha_fin
                fecha_fin = fecha_inicio
                fecha_inicio = temp
            # res = self._plan_explotacion_rango_fecha(cr, uid, ids, pozo_ids, fecha_inicio, fecha_fin, context)
            res = self._plan_explotacion_rango_fecha(ids, fecha_inicio, fecha_fin)
        else:
            # res = self._plan_explotacion_sin_rango_fecha(cr, uid, ids, pozo_ids, context)
            res = self._plan_explotacion_sin_rango_fecha(ids)
        return res

    #
    def buscar_anno(self, pozo_ids):
        if pozo_ids:
            tabla_agrupamiento = 'df_nivel_anual_pozo'
            sql = """ select anno
                             from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                             where tabla_objeto.pozo_id in %s
                             ORDER BY anno ASC"""
            self.env.cr.execute(sql, (tuple(pozo_ids),))
            datos_vistas = self.env.cr.dictfetchall()
            return datos_vistas
        else:
             raise UserError(_('Debe de seleccionar los pozos.'))
             #raise osv.except_osv(_("Alerta !"), _("Debe de seleccionar los pozos."))

    def obtener(self, valor_anterior, lista):
        if lista:
            cont_asc = 0
            dict_resultados = {}
            # min=lista[0]['valor']
            max = lista[0]['valor']
            max_temporal = lista[0]['valor']
            anno_maximo = lista[0]['anno']
            mes_maximo = lista[0]['mes']
            for maximo in lista:
                if maximo['valor'] > max:
                    max = maximo['valor']
                    anno_maximo = maximo['anno']
                    mes_maximo = maximo['mes']
            for maximo in lista:
                if maximo['valor'] < max_temporal:
                    cont_asc += 1
                max_temporal = maximo['valor']
            if cont_asc == 3:
                if valor_anterior and valor_anterior['valor'] > lista[0]['valor']:
                    dict_resultados['valor'] = valor_anterior['valor']
                    dict_resultados['anno'] = valor_anterior['anno']
                    dict_resultados['mes'] = valor_anterior['mes']
                    dict_resultados['ok'] = 1
                else:
                    dict_resultados['valor'] = max
                    dict_resultados['anno'] = anno_maximo
                    dict_resultados['mes'] = mes_maximo
                    dict_resultados['ok'] = 1
                return dict_resultados
            else:
                temp = 2
                aux = 1
                lista_asc = []
                cont_desc = 0
                cont = 1
                max_ascendentes = lista[1]['valor']
                temp_asc = lista[3]
                while cont < 3:
                    if max_ascendentes > lista[temp]['valor']:
                        cont_desc += 1
                        if cont_desc <= 2:
                            lista_asc.append(lista[aux])
                            max_ascendentes = lista[aux]['valor']
                            temp += 1
                            cont += 1
                            aux += 1
                        else:
                            break
                    else:
                        # lista_asc=[]
                        # break
                        aux += 1
                        max_ascendentes = lista[aux]['valor']
                        temp += 1
                        cont += 1
                        # cont_desc+=1
                if cont_desc == 2:
                    # lista_asc.append(lista[1])
                    lista_asc.append(temp_asc)
                    valor_anterior = lista[1]
                else:
                    # lista_asc.append(lista[2])
                    lista_asc.append(temp_asc)
                    valor_anterior = lista[2]
                dict_resultados['ok'] = 2
                dict_resultados['anno'] = anno_maximo
                dict_resultados['mes'] = mes_maximo
                dict_resultados['lista'] = lista_asc
                dict_resultados['valor_anterior'] = valor_anterior
                return dict_resultados

    def buscar(self, recorrido_actual, list_recorridos, lista):
        lista_fechas = []
        recorridos_posteriores = []
        lista_strines = []
        lista_strines_posteriores = []
        encontro_recorrido = 0
        ok = 0
        for list_recorrido in list_recorridos:
            lista_fechas.append(list_recorrido)
        for lista_fecha in lista_fechas:
            if recorrido_actual != lista_fecha:
                recorridos_posteriores.append(lista_fecha)
        for valor in lista:
            anno = str(valor['anno'])
            mes = str(valor['mes'])
            fecha_string = anno + mes
            lista_strines.append(fecha_string)
        for recorridos_posteriore in recorridos_posteriores:
            lista_strines_posteriores.append(str(recorridos_posteriore.year) + str(recorridos_posteriore.month))
        for lista_strines_posteriore in lista_strines_posteriores:
            pos = 0
            for lista_strine in lista_strines:
                pos += 1
                if lista_strines_posteriore == lista_strine:
                    ok = pos
                    encontro_recorrido += 1
        if encontro_recorrido == 0:
            return 1
        else:
            contador = 1
            contador_aux = 1
            list_no_rango = []
            dict_resultados = {}
            max = lista[0]['valor']
            mes_maximo = lista[0]['mes']
            anno_maximo = lista[0]['anno']
            for maximo in lista:
                if contador < ok:
                    if maximo['valor'] > max:
                        max = maximo['valor']
                        anno_maximo = maximo['anno']
                        mes_maximo = maximo['mes']
                contador += 1
            for minimo in lista:
                if contador_aux >= ok:
                    list_no_rango.append(minimo)
                contador_aux += 1
            dict_resultados['valor'] = max
            dict_resultados['anno'] = anno_maximo
            dict_resultados['mes'] = mes_maximo
            dict_resultados['ok'] = 1
            dict_resultados['lista'] = list_no_rango
            return dict_resultados

    def buscar_valor_maximo(self, ultimos_4_valores):
        max = ultimos_4_valores[0]['valor']
        anno_maximo = ultimos_4_valores[0]['anno']
        mes_maximo = ultimos_4_valores[0]['mes']
        for maximo in ultimos_4_valores:
            if maximo['valor'] > max:
                max = maximo['valor']
                anno_maximo = maximo['anno']
                mes_maximo = maximo['mes']
        dict_max = {}
        dict_max['valor'] = max
        dict_max['anno'] = anno_maximo
        dict_max['mes'] = mes_maximo
        return dict_max

    def ordenar_diccionario(self, niveles_ordenados):
        # lista=[None,None,None,None,None,None,None,None,None,None,None,None,None]
        datos_vistas = []
        for niveles_ordenado in niveles_ordenados:
            lista = [None, None, None, None, None, None, None, None, None, None, None, None, None]
            if niveles_ordenado.get('1'):
                lista[1] = niveles_ordenado['1']
            if niveles_ordenado.get('2'):
                lista[2] = niveles_ordenado['2']
            if niveles_ordenado.get('3'):
                lista[3] = niveles_ordenado['3']
            if niveles_ordenado.get('4'):
                lista[4] = niveles_ordenado['4']
            if niveles_ordenado.get('5'):
                lista[5] = niveles_ordenado['5']
            if niveles_ordenado.get('6'):
                lista[6] = niveles_ordenado['6']
            if niveles_ordenado.get('7'):
                lista[7] = niveles_ordenado['7']
            if niveles_ordenado.get('8'):
                lista[8] = niveles_ordenado['8']
            if niveles_ordenado.get('9'):
                lista[9] = niveles_ordenado['9']
            if niveles_ordenado.get('10'):
                lista[10] = niveles_ordenado['10']
            if niveles_ordenado.get('11'):
                lista[11] = niveles_ordenado['11']
            if niveles_ordenado.get('12'):
                lista[12] = niveles_ordenado['12']
            lista[0] = niveles_ordenado['anno']
            datos_vistas.append(tuple(lista))
        return datos_vistas

    def menor_proximo_valor(self, lista_sobrecarga):
        if lista_sobrecarga[1]['valor'] < lista_sobrecarga[0]['valor']:
            return True
        else:
            return False

    def buscar_sobrecarga(self, lista_sobrecarga, diferencia_sobrecarga):
        if lista_sobrecarga:
            valor = 0
            dict_resultados = {}
            if lista_sobrecarga[1]['valor'] != None and lista_sobrecarga[0]['valor'] != None:
                valor = abs(lista_sobrecarga[1]['valor'] - lista_sobrecarga[0]['valor'])
            if valor >= diferencia_sobrecarga:
                dict_resultados['valor'] = lista_sobrecarga[0]['valor']
                dict_resultados['anno'] = lista_sobrecarga[0]['anno']
                dict_resultados['mes'] = lista_sobrecarga[0]['mes']
                dict_resultados['sobrecarga'] = 1
            else:
                dict_resultados['valor'] = lista_sobrecarga[1]['valor']
                dict_resultados['anno'] = lista_sobrecarga[1]['anno']
                dict_resultados['mes'] = lista_sobrecarga[1]['mes']
                dict_resultados['sobrecarga'] = 2
        return dict_resultados

    def obtener_fin_recorridos(self, ids, pozo_ids, recorridos, exepcion, tipo):
        fecha_fin = datetime.datetime.now()
        fecha_inicio = recorridos
        lista_recorridos = []
        # diferencia_sobrecarga=0.5
        global encontro
        for id in ids:
            cont_recorrido = 0
            diferencia_sobrecarga = self.browse( id).valor_precision
            buscar = self.buscar_anno(pozo_ids)
            if len(buscar) > 0:
                anno_inicio = buscar[0]['anno']
                anno_fin = fecha_fin.year
                # anno_inicio=1999
                while anno_inicio <= anno_fin:
                    temp = 0
                    mes_valor = 0
                    contador = 1
                    contador4 = 0
                    lista = []
                    lista_sobrecarga = []
                    valor_anterior = {}
                    orden_recorrido = 0
                    for recorrido in recorridos:
                        orden_recorrido += 1
                        encontro = 0
                        contador_meses = 0
                        if anno_inicio == recorrido.year:
                            if tipo == 'aritmetica':
                                if fecha_inicio == None and fecha_fin == None:
                                    datos = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
                                    niveles_ordenados = sorted(datos[temp], key=lambda tup: tup['anno'])
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                                else:
                                    datos = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio[0],
                                                                           fecha_fin)
                                    niveles_ordenados = sorted(datos[temp], key=lambda tup: tup['anno'])
                                    datos_vistas = self.ordenar_diccionario(niveles_ordenados)
                            if tipo == 'formula':
                                if fecha_inicio == None and fecha_fin == None:
                                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)

                                    niveles_ordenados = sorted(datos_vistas[temp], key=lambda tup: tup['anno'])
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                                else:
                                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids,
                                                                                   fecha_inicio[0], fecha_fin)
                                    niveles_ordenados = sorted(datos_vistas[temp], key=lambda tup: tup['anno'])
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                            for datos_vista in datos_vistas:
                                if encontro == 1:
                                    break
                                temporal = {}
                                for valor in datos_vista:
                                    if temp >= 1:
                                        mes_valor += 1
                                    temp += 1
                                    dict_general = {}
                                    if contador >= (recorrido.month + 1) and contador > 1:
                                        if len(temporal) > 0:
                                            lista.append(temporal)
                                            temporal = {}
                                            contador4 += 1
                                        if mes_valor >= 1:
                                            dict_general['valor'] = valor
                                            dict_general['anno'] = datos_vista[0]
                                            dict_general['mes'] = mes_valor
                                            lista.append(dict_general)
                                            lista_sobrecarga.append(dict_general)
                                            contador_meses += 1
                                            contador4 += 1
                                    if contador4 == 4:
                                        recorrido_actual = recorrido
                                        list_recorridos = exepcion
                                        coencide = self.buscar(recorrido_actual, list_recorridos, lista)
                                        if coencide != 1:
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            # max=ultimos_4_valores[0]['valor']
                                            # anno_maximo = ultimos_4_valores[0]['anno']
                                            # mes_maximo =ultimos_4_valores[0]['mes']
                                            # for maximo in ultimos_4_valores:
                                            #     if maximo['valor']>max:
                                            #         max=maximo['valor']
                                            #         anno_maximo= maximo['anno']
                                            #         mes_maximo=maximo['mes']
                                            # dict_max={}
                                            # dict_max['valor'] = max
                                            # dict_max['anno'] = anno_maximo
                                            # dict_max['mes'] = mes_maximo
                                            ultimos_4_valores = lista
                                            dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                            if dict_max['valor'] <= coencide['valor']:
                                                dic_recorridos['mes'] = coencide['mes']
                                                dic_recorridos['anno'] = coencide['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            else:
                                                dic_recorridos['mes'] = dict_max['mes']
                                                dic_recorridos['anno'] = dict_max['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            lista = []
                                            temporal = dict_general
                                            contador4 = 0
                                            encontro = 1
                                            break
                                        ultimos_4_valores = []
                                        ultimos_4_valores = lista
                                        existe = self.obtener(valor_anterior, lista)
                                        if existe['ok'] == 1:
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            # max=ultimos_4_valores[0]['valor']
                                            # anno_maximo = ultimos_4_valores[0]['anno']
                                            # mes_maximo =ultimos_4_valores[0]['mes']
                                            # for maximo in ultimos_4_valores:
                                            #     if maximo['valor']>max:
                                            #         max=maximo['valor']
                                            #         anno_maximo= maximo['anno']
                                            #         mes_maximo=maximo['mes']
                                            # dict_max={}
                                            # dict_max['valor'] = max
                                            # dict_max['anno'] = anno_maximo
                                            # dict_max['mes'] = mes_maximo
                                            dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                            if dict_max['valor'] <= existe['valor']:
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            else:
                                                dic_recorridos['mes'] = dict_max['mes']
                                                dic_recorridos['anno'] = dict_max['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                # dic_recorridos['mes']=existe['mes']
                                            # dic_recorridos['anno']=existe['anno']
                                            # dic_recorridos['orden_recorrido']=orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            lista = []
                                            temporal = dict_general
                                            contador4 = 0
                                            encontro = 1
                                            break
                                        if existe['ok'] == 2:
                                            lista = []
                                            cont_temp = 0
                                            for valor in existe['lista']:
                                                lista.append(valor)
                                                cont_temp += 1
                                            contador4 = cont_temp
                                            valor_anterior = existe['valor_anterior']
                                    if len(lista_sobrecarga) == 2:
                                        verdadero = self.menor_proximo_valor(lista_sobrecarga)
                                        sobrecarga = self.buscar_sobrecarga(lista_sobrecarga,
                                                                            diferencia_sobrecarga)
                                        if verdadero:
                                            if sobrecarga['sobrecarga'] == 1:
                                                dic_recorridos = {}
                                                dic_recorridos['mes'] = sobrecarga['mes']
                                                dic_recorridos['anno'] = sobrecarga['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                lista = []
                                                lista_sobrecarga = []
                                                temporal = dict_general
                                                contador4 = 0
                                                encontro = 1
                                                break
                                            else:
                                                lista_sobrecarga = []
                                                dict_general['valor'] = sobrecarga['valor']
                                                dict_general['anno'] = sobrecarga['anno']
                                                dict_general['mes'] = sobrecarga['mes']
                                                lista_sobrecarga.append(dict_general)
                                        else:
                                            lista_sobrecarga = []
                                            lista_sobrecarga.append(dict_general)
                                    if contador_meses == 24:
                                        if len(lista) == 4:
                                            # max=ultimos_4_valores[0]['valor']
                                            # anno_maximo = ultimos_4_valores[0]['anno']
                                            # mes_maximo =ultimos_4_valores[0]['mes']
                                            # for maximo in ultimos_4_valores:
                                            #     if maximo['valor']>max:
                                            #         max=maximo['valor']
                                            #         anno_maximo= maximo['anno']
                                            #         mes_maximo=maximo['mes']
                                            # dict_max={}
                                            # dict_max['valor'] = max
                                            # dict_max['anno'] = anno_maximo
                                            # dict_max['mes'] = mes_maximo
                                            dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                            lista.append(dict_max)
                                            existe = self.obtener(valor_anterior, lista)
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            dic_recorridos['mes'] = existe['mes']
                                            dic_recorridos['anno'] = existe['anno']
                                            dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            encontro = 1
                                            break
                                        else:
                                            if len(lista) == 1:
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    lista.append(ultimos_4_valore)
                                                    # max=ultimos_4_valores[0]['valor']
                                                # anno_maximo = ultimos_4_valores[0]['anno']
                                                # mes_maximo =ultimos_4_valores[0]['mes']
                                                # for maximo in ultimos_4_valores:
                                                #     if maximo['valor']>max:
                                                #         max=maximo['valor']
                                                #         anno_maximo= maximo['anno']
                                                #         mes_maximo=maximo['mes']
                                                # dict_max={}
                                                # dict_max['valor'] = max
                                                # dict_max['anno'] = anno_maximo
                                                # dict_max['mes'] = mes_maximo
                                                dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                                lista.append(dict_max)
                                                existe = self.obtener(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                            if len(lista) == 2:
                                                contadorv = 0
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    if contadorv >= 1:
                                                        lista.append(ultimos_4_valore)
                                                    contadorv += 1
                                                    # max=ultimos_4_valores[0]['valor']
                                                # anno_maximo = ultimos_4_valores[0]['anno']
                                                # mes_maximo =ultimos_4_valores[0]['mes']
                                                # for maximo in ultimos_4_valores:
                                                #     if maximo['valor']>max:
                                                #         max=maximo['valor']
                                                #         anno_maximo= maximo['anno']
                                                #         mes_maximo=maximo['mes']
                                                # dict_max={}
                                                # dict_max['valor'] = max
                                                # dict_max['anno'] = anno_maximo
                                                # dict_max['mes'] = mes_maximo
                                                dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                                lista.append(dict_max)
                                                existe = self.obtener(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                            if len(lista) == 3:
                                                contadorv = 0
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    if contadorv >= 2:
                                                        lista.append(ultimos_4_valore)
                                                    contadorv += 1
                                                    # max=ultimos_4_valores[0]['valor']
                                                # anno_maximo = ultimos_4_valores[0]['anno']
                                                # mes_maximo =ultimos_4_valores[0]['mes']
                                                # for maximo in ultimos_4_valores:
                                                #     if maximo['valor']>max:
                                                #         max=maximo['valor']
                                                #         anno_maximo= maximo['anno']
                                                #         mes_maximo=maximo['mes']
                                                # dict_max={}
                                                # dict_max['valor'] = max
                                                # dict_max['anno'] = anno_maximo
                                                # dict_max['mes'] = mes_maximo
                                                dict_max = self.buscar_valor_maximo(ultimos_4_valores)
                                                lista.append(dict_max)
                                                existe = self.obtener(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                    contador += 1
                                mes_valor = 0
                                temp = 0
                            contador = 1
                    anno_inicio += 1
        niveles_ordenados = sorted(lista_recorridos, key=lambda tup: tup['orden_recorrido'])
        return niveles_ordenados

    def buscar_inicio(self, recorrido_actual, list_recorridos, lista):
        lista_fechas = []
        recorridos_posteriores = []
        lista_strines = []
        lista_strines_posteriores = []
        encontro_recorrido = 0
        ok = 0
        for list_recorrido in list_recorridos:
            lista_fechas.append(list_recorrido)
        for lista_fecha in lista_fechas:
            if recorrido_actual != lista_fecha:
                recorridos_posteriores.append(lista_fecha)
        for valor in lista:
            anno = str(valor['anno'])
            mes = str(valor['mes'])
            fecha_string = anno + mes
            lista_strines.append(fecha_string)
        for recorridos_posteriore in recorridos_posteriores:
            lista_strines_posteriores.append(str(recorridos_posteriore.year) + str(recorridos_posteriore.month))
        for lista_strines_posteriore in lista_strines_posteriores:
            pos = 0
            for lista_strine in lista_strines:
                pos += 1
                if lista_strines_posteriore == lista_strine:
                    ok = pos
                    encontro_recorrido += 1
        if encontro_recorrido == 0:
            return 1
        else:
            contador = 1
            contador_aux = 1
            list_no_rango = []
            dict_resultados = {}
            min = lista[0]['valor']
            mes_minimo = lista[0]['mes']
            anno_minimo = lista[0]['anno']
            for minimo in lista:
                if contador < ok:
                    if minimo['valor'] < min:
                        min = minimo['valor']
                        anno_minimo = minimo['anno']
                        mes_minimo = minimo['mes']
                contador += 1
            for minimo in lista:
                if contador_aux >= ok:
                    list_no_rango.append(minimo)
                contador_aux += 1
            dict_resultados['valor'] = min
            dict_resultados['anno'] = anno_minimo
            dict_resultados['mes'] = mes_minimo
            dict_resultados['ok'] = 1
            dict_resultados['lista'] = list_no_rango
            return dict_resultados

    def obtener_inicio(self, valor_anterior, lista):
        if lista:
            cont_desc = 0
            dict_resultados = {}
            # min=lista[0]['valor']
            min = lista[0]['valor']
            max_temporal = lista[0]['valor']
            anno_minimo = lista[0]['anno']
            mes_minimo = lista[0]['mes']
            for minimo in lista:
                if minimo['valor'] < min:
                    min = minimo['valor']
                    anno_minimo = minimo['anno']
                    mes_minimo = minimo['mes']
            for maximo in lista:
                if maximo['valor'] > max_temporal:
                    cont_desc += 1
                max_temporal = maximo['valor']
            if cont_desc == 3:
                if valor_anterior and valor_anterior['valor'] < lista[0]['valor']:
                    dict_resultados['valor'] = valor_anterior['valor']
                    dict_resultados['anno'] = valor_anterior['anno']
                    dict_resultados['mes'] = valor_anterior['mes']
                    dict_resultados['ok'] = 1
                else:
                    dict_resultados['valor'] = min
                    dict_resultados['anno'] = anno_minimo
                    dict_resultados['mes'] = mes_minimo
                    dict_resultados['ok'] = 1
                return dict_resultados
            else:
                temp = 2
                aux = 1
                lista_asc = []
                cont_desc = 0
                cont = 1
                max_ascendentes = lista[1]['valor']
                temp_asc = lista[3]
                while cont < 3:
                    if max_ascendentes < lista[temp]['valor']:
                        cont_desc += 1
                        if cont_desc <= 2:
                            lista_asc.append(lista[aux])
                            max_ascendentes = lista[aux]['valor']
                            temp += 1
                            cont += 1
                            aux += 1
                        else:
                            break
                    else:
                        # lista_asc=[]
                        # break
                        aux += 1
                        max_ascendentes = lista[aux]['valor']
                        temp += 1
                        cont += 1
                        # cont_desc+=1
                if cont_desc == 2:
                    # lista_asc.append(lista[1])
                    lista_asc.append(temp_asc)
                    valor_anterior = lista[1]
                else:
                    # lista_asc.append(lista[2])
                    lista_asc.append(temp_asc)
                    valor_anterior = lista[2]
                dict_resultados['ok'] = 2
                dict_resultados['anno'] = anno_minimo
                dict_resultados['mes'] = mes_minimo
                dict_resultados['lista'] = lista_asc
                dict_resultados['valor_anterior'] = valor_anterior
                return dict_resultados

    def buscar_valor_minimo(self, ultimos_4_valores):
        min = ultimos_4_valores[0]['valor']
        anno_minimo = ultimos_4_valores[0]['anno']
        mes_minimo = ultimos_4_valores[0]['mes']
        for minimo in ultimos_4_valores:
            if minimo['valor'] < min:
                min = minimo['valor']
                anno_minimo = minimo['anno']
                mes_minimo = minimo['mes']
        dict_min = {}
        dict_min['valor'] = min
        dict_min['anno'] = mes_minimo
        dict_min['mes'] = anno_minimo
        return dict_min

    def menor_proximo_valor_inicio(self, lista_sobrecarga):
        if lista_sobrecarga[1]['valor'] > lista_sobrecarga[0]['valor']:
            return True
        else:
            return False

    def buscar_sobrecarga_inicio(self, lista_sobrecarga, diferencia_sobrecarga):
        if lista_sobrecarga:
            valor = 0
            dict_resultados = {}
            if lista_sobrecarga[1]['valor'] != None and lista_sobrecarga[0]['valor'] != None:
                valor = abs(lista_sobrecarga[1]['valor'] - lista_sobrecarga[0]['valor'])
            if valor >= diferencia_sobrecarga:
                dict_resultados['valor'] = lista_sobrecarga[0]['valor']
                dict_resultados['anno'] = lista_sobrecarga[0]['anno']
                dict_resultados['mes'] = lista_sobrecarga[0]['mes']
                dict_resultados['sobrecarga'] = 1
            else:
                dict_resultados['valor'] = lista_sobrecarga[1]['valor']
                dict_resultados['anno'] = lista_sobrecarga[1]['anno']
                dict_resultados['mes'] = lista_sobrecarga[1]['mes']
                dict_resultados['sobrecarga'] = 2
        return dict_resultados

    def obtener_inicio_recorridos(self, ids, pozo_ids, recorridos, exepcion, tipo):
        fecha_actual = datetime.datetime.now()
        fecha_fin = recorridos
        lista_recorridos = []
        # diferencia_sobrecarga=0.5
        global encontro
        for id in ids:
            cont_recorrido = 0
            diferencia_sobrecarga = self.browse( id).valor_precision
            buscar = self.buscar_anno(pozo_ids)
            if len(buscar) > 0:
                anno_inicio = buscar[0]['anno']
                dia = 1
                mes = 1
                fecha_inicio = datetime.datetime(anno_inicio, mes, dia)
                anno_fin = fecha_fin[0].year
                # anno_fin=2010
                while anno_fin >= anno_inicio:
                    temp = 0
                    temporal = {}
                    mes_valor = 0
                    contador = 1
                    contador4 = 0
                    lista = []
                    lista_sobrecarga = []
                    valor_anterior = {}
                    orden_recorrido = 0
                    for recorrido in recorridos:
                        posicion = recorrido.month
                        orden_recorrido += 1
                        encontro = 0
                        contador_meses = 0
                        if anno_fin == recorrido.year:
                            if tipo == 'aritmetica':
                                if fecha_inicio == None and fecha_fin == None:
                                    datos = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
                                    niveles_ordenados = sorted(datos[temp], key=lambda tup: tup['anno'], reverse=True)
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                                else:
                                    datos = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio,
                                                                           fecha_fin[0])
                                    niveles_ordenados = sorted(datos[temp], key=lambda tup: tup['anno'], reverse=True)
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                            if tipo == 'formula':
                                if fecha_inicio == None and fecha_fin == None:
                                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)

                                    niveles_ordenados = sorted(datos_vistas[temp], key=lambda tup: tup['anno'],
                                                               reverse=True)
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                                else:
                                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio,
                                                                                   fecha_fin[0])
                                    niveles_ordenados = sorted(datos_vistas[temp], key=lambda tup: tup['anno'],
                                                               reverse=True)
                                    datos_vistas = self.ordenar_diccionario( niveles_ordenados)
                            # datos_vistas = self.obtener_niveles_acotados_asc(cr,pozo.id,anno_inicio,recorrido.year)
                            for datos_vista in datos_vistas:
                                if encontro == 1:
                                    break
                                while posicion >= 1:
                                    if len(temporal) > 0:
                                        lista.append(temporal)
                                        temporal = {}
                                        contador4 += 1
                                    dict_general = {}
                                    dict_general['valor'] = datos_vista[posicion]
                                    dict_general['anno'] = datos_vista[0]
                                    dict_general['mes'] = posicion
                                    lista.append(dict_general)
                                    lista_sobrecarga.append(dict_general)
                                    contador_meses += 1
                                    contador4 += 1
                                    posicion -= 1
                                    if contador4 == 4:
                                        recorrido_actual = recorrido
                                        list_recorridos = exepcion
                                        coencide = self.buscar_inicio(recorrido_actual, list_recorridos, lista)
                                        # lista=[]
                                        if coencide != 1:
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            # min=ultimos_4_valores[0]['valor']
                                            # anno_minimo = ultimos_4_valores[0]['anno']
                                            # mes_minimo =ultimos_4_valores[0]['mes']
                                            # for minimo in ultimos_4_valores:
                                            #     if minimo['valor']<min:
                                            #         min=minimo['valor']
                                            #         anno_minimo= minimo['anno']
                                            #         mes_minimo=minimo['mes']
                                            # dict_min={}
                                            # dict_min['valor'] = min
                                            # dict_min['anno'] = mes_minimo
                                            # dict_min['mes'] = anno_minimo
                                            ultimos_4_valores = lista
                                            dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                            if dict_min['valor'] >= coencide['valor']:
                                                dic_recorridos['mes'] = coencide['mes']
                                                dic_recorridos['anno'] = coencide['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            else:
                                                dic_recorridos['mes'] = dict_min['mes']
                                                dic_recorridos['anno'] = dict_min['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            lista = []
                                            temporal = dict_general
                                            contador4 = 0
                                            encontro = 1
                                            break
                                            # contador4=0
                                        # temporal= dict_general
                                        ultimos_4_valores = []
                                        ultimos_4_valores = lista
                                        existe = self.obtener_inicio(valor_anterior, lista)
                                        if existe['ok'] == 1:
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            # min=ultimos_4_valores[0]['valor']
                                            # anno_minimo = ultimos_4_valores[0]['anno']
                                            # mes_minimo =ultimos_4_valores[0]['mes']
                                            # for minimo in ultimos_4_valores:
                                            #     if minimo['valor']<min:
                                            #         min=minimo['valor']
                                            #         anno_minimo= minimo['anno']
                                            #         mes_minimo=minimo['mes']
                                            # dict_min={}
                                            # dict_min['valor'] = min
                                            # dict_min['anno'] = mes_minimo
                                            # dict_min['mes'] = anno_minimo
                                            dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                            if dict_min['valor'] >= existe['valor']:
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            else:
                                                dic_recorridos['mes'] = dict_min['mes']
                                                dic_recorridos['anno'] = dict_min['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            # dic_recorridos['mes']=existe['mes']
                                            # dic_recorridos['anno']=existe['anno']
                                            # dic_recorridos['orden_recorrido']=orden_recorrido
                                            # lista_recorridos.append(dic_recorridos)
                                            lista = []
                                            temporal = dict_general
                                            contador4 = 0
                                            encontro = 1
                                            break
                                        if existe['ok'] == 2:
                                            lista = []
                                            cont_temp = 0
                                            for valor in existe['lista']:
                                                lista.append(valor)
                                                cont_temp += 1
                                            contador4 = cont_temp
                                            valor_anterior = existe['valor_anterior']
                                    if len(lista_sobrecarga) == 2:
                                        verdadero = self.menor_proximo_valor_inicio(lista_sobrecarga)
                                        sobrecarga = self.buscar_sobrecarga_inicio(lista_sobrecarga,
                                                                                   diferencia_sobrecarga)
                                        if verdadero:
                                            if sobrecarga['sobrecarga'] == 1:
                                                dic_recorridos = {}
                                                dic_recorridos['mes'] = sobrecarga['mes']
                                                dic_recorridos['anno'] = sobrecarga['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                lista = []
                                                lista_sobrecarga = []
                                                temporal = dict_general
                                                contador4 = 0
                                                encontro = 1
                                                break
                                            else:
                                                lista_sobrecarga = []
                                                dict_general['valor'] = sobrecarga['valor']
                                                dict_general['anno'] = sobrecarga['anno']
                                                dict_general['mes'] = sobrecarga['mes']
                                                lista_sobrecarga.append(dict_general)
                                        else:
                                            lista_sobrecarga = []
                                            lista_sobrecarga.append(dict_general)
                                    if contador_meses == 24:
                                        if len(lista) == 4:
                                            # min=ultimos_4_valores[0]['valor']
                                            # anno_minimo = ultimos_4_valores[0]['anno']
                                            # mes_minimo =ultimos_4_valores[0]['mes']
                                            # for minimo in ultimos_4_valores:
                                            #     if minimo['valor']<min:
                                            #         min=minimo['valor']
                                            #         anno_minimo= minimo['anno']
                                            #         mes_minimo=minimo['mes']
                                            # dict_min={}
                                            # dict_min['valor'] = min
                                            # dict_min['anno'] = mes_minimo
                                            # dict_min['mes'] = anno_minimo
                                            dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                            lista.append(dict_min)
                                            existe = self.obtener_inicio(valor_anterior, lista)
                                            dic_recorridos = {}
                                            cont_recorrido += 1
                                            dic_recorridos['mes'] = existe['mes']
                                            dic_recorridos['anno'] = existe['anno']
                                            dic_recorridos['orden_recorrido'] = orden_recorrido
                                            lista_recorridos.append(dic_recorridos)
                                            encontro = 1
                                            break
                                        else:
                                            if len(lista) == 1:
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    lista.append(ultimos_4_valore)
                                                    # min=ultimos_4_valores[0]['valor']
                                                # anno_minimo = ultimos_4_valores[0]['anno']
                                                # mes_minimo =ultimos_4_valores[0]['mes']
                                                # for minimo in ultimos_4_valores:
                                                #     if minimo['valor']<min:
                                                #         min=minimo['valor']
                                                #         anno_minimo= minimo['anno']
                                                #         mes_minimo=minimo['mes']
                                                # dict_min={}
                                                # dict_min['valor'] = min
                                                # dict_min['anno'] = mes_minimo
                                                # dict_min['mes'] = anno_minimo
                                                dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                                lista.append(dict_min)
                                                existe = self.obtener_inicio(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                            if len(lista) == 2:
                                                contadorv = 0
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    if contadorv >= 1:
                                                        lista.append(ultimos_4_valore)
                                                    contadorv += 1
                                                    # min=ultimos_4_valores[0]['valor']
                                                # anno_minimo = ultimos_4_valores[0]['anno']
                                                # mes_minimo =ultimos_4_valores[0]['mes']
                                                # for minimo in ultimos_4_valores:
                                                #     if minimo['valor']<min:
                                                #         min=minimo['valor']
                                                #         anno_minimo= minimo['anno']
                                                #         mes_minimo=minimo['mes']
                                                # dict_min={}
                                                # dict_min['valor'] = min
                                                # dict_min['anno'] = mes_minimo
                                                # dict_min['mes'] = anno_minimo
                                                dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                                lista.append(dict_min)
                                                existe = self.obtener_inicio(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                            if len(lista) == 3:
                                                contadorv = 0
                                                for ultimos_4_valore in ultimos_4_valores:
                                                    if contadorv >= 2:
                                                        lista.append(ultimos_4_valore)
                                                    contadorv += 1
                                                    # min=ultimos_4_valores[0]['valor']
                                                # anno_minimo = ultimos_4_valores[0]['anno']
                                                # mes_minimo =ultimos_4_valores[0]['mes']
                                                # for minimo in ultimos_4_valores:
                                                #     if minimo['valor']<min:
                                                #         min=minimo['valor']
                                                #         anno_minimo= minimo['anno']
                                                #         mes_minimo=minimo['mes']
                                                # dict_min={}
                                                # dict_min['valor'] = min
                                                # dict_min['anno'] = mes_minimo
                                                # dict_min['mes'] = anno_minimo
                                                dict_min = self.buscar_valor_minimo(ultimos_4_valores)
                                                lista.append(dict_min)
                                                existe = self.obtener_inicio(valor_anterior, lista)
                                                lista = []
                                                dic_recorridos = {}
                                                cont_recorrido += 1
                                                dic_recorridos['mes'] = existe['mes']
                                                dic_recorridos['anno'] = existe['anno']
                                                dic_recorridos['orden_recorrido'] = orden_recorrido
                                                lista_recorridos.append(dic_recorridos)
                                                encontro = 1
                                                break
                                posicion = 12
                    anno_fin -= 1
        niveles_ordenados = sorted(lista_recorridos, key=lambda tup: tup['orden_recorrido'])
        return niveles_ordenados

    def buscar_sectores_directo(self, pozo_ids):
        if pozo_ids:
            sql = """ SELECT
                              df_bloque.id AS bloque_ids
                            FROM
                              public.df_pozo,
                              public.df_bloque

                            WHERE
                              df_pozo.bloque_id = df_bloque.id AND
                              df_pozo.id in %s AND df_pozo.representativo=True"""
            self.env.cr.execute(sql, (tuple(pozo_ids),))
            datos_vistas = self.env.cr.dictfetchall()
            lista = []
            for datos_vista in datos_vistas:
                lista.append(datos_vista['bloque_ids'])
            lista = list(set(lista))
            return lista

    # # def buscar_sectores_indirecto(self, cr, uid,pozo_ids,context=None):
    # #     if pozo_ids:
    # #         sql = """ SELECT
    # #                       df_sector_hidrologico.id AS sector_ids
    # #                     FROM
    # #                       public.df_pozo,
    # #                       public.df_sector_hidrologico,
    # #                       public.df_bloque
    # #                     WHERE
    # #                       df_pozo.bloque_id = df_bloque.id AND
    # #                       df_bloque.sector_id = df_sector_hidrologico.id
    # #                         AND
    # #                       df_pozo.id in %s AND df_pozo.representativo=True"""
    # #         cr.execute(sql,(tuple(pozo_ids),))
    # #         datos_vistas = cr.dictfetchall()
    # #         lista=[]
    # #         for datos_vista in datos_vistas:
    # #             lista.append(datos_vista['sector_ids'])
    # #         lista = list(set(lista))
    # #         return lista

    def obtener_promedio_alturas(self, pozo_ids_actualizar, ok):
        if ok:
            # ids=bloque_obj.search(cr, uid, [])
            ids = self.buscar_sectores_directo( pozo_ids_actualizar)
        else:
            ids = pozo_ids_actualizar
        bloque_obj = self.env['df.bloque']
        pozo_obj = self.env['df.pozo']
        cont = 0
        for bloque in self.browse(ids):
            # vals={}
            # suma_h_periodo = 0
            # cantidad_h_periodo = 0
            pozo_ids = pozo_obj.search([('representativo', '=', True), ('bloque_id', 'in', [bloque.id])]).ids
            if pozo_ids:
                inicio = self.formar_fecha_inicio(pozo_ids)
                fin = self.formar_fecha_fin(pozo_ids)
                if inicio != False and fin != False:
                    elementos = self.calcular_media_aritmetica([bloque.id], pozo_ids, inicio, fin)
                    if elementos:
                        vals = {}
                        min = list(elementos[0][0].values())[0]
                        max = 0.0
                        suma_h_periodo = 0
                        cantidad_h_periodo = 0
                        contador_elementos = 0
                        suma_descargas_secuencia = 0
                        valores_recarga = []
                        verificando_annos = []
                        valor_precision = 0.001
                        ultima_recarga = None
                        # dia = 01
                        # mes = 01
                        # anno_inicio=2013
                        # inicio = datetime.datetime(anno_inicio,mes,dia)
                        while inicio <= fin:
                            tiempo = time.strptime(str(inicio.year) + '-' + str(inicio.month) + '-' + str(1),
                                                   "%Y-%m-%d")
                            tiempo_milisegundos = time.mktime(tiempo) * 1000
                            # valor = float("%.3f" % float(elementos[0][contador_elementos][self._mes_numero(inicio.month)]))
                            if elementos[0][contador_elementos].get(str(inicio.month)):
                                valor = float("%.3f" % float(elementos[0][contador_elementos][str(inicio.month)]))
                            if valor != -999999.110:
                                if valor < min:
                                    min = valor
                                if valor > max:
                                    max = valor
                                # ---------BUSCANDO RECARGAS
                            if len(valores_recarga) > 0:  # si existen valores en analisis
                                valor_anterior = valores_recarga[len(valores_recarga) - 1]['valor']
                                # ------------ VERIFICANO PEQUENNAS DESCARGAS EN SECUENCIA QUE AL FINAL PUEDEN CONLLEVAR A UN DELTA ALTO
                                if valor - valor_anterior <= valor_precision and valor - valor_anterior > 0:
                                    suma_descargas_secuencia += valor - valor_anterior
                                else:
                                    suma_descargas_secuencia = 0
                                if (valor_anterior > valor or (
                                        valor - valor_anterior <= valor_precision and valor - valor_anterior > 0)) and suma_descargas_secuencia < valor_precision:
                                    # lo apilo
                                    valores_recarga.append({'tiempo_milisegundos': tiempo_milisegundos, 'valor': valor})
                                elif len(valores_recarga) > 1:
                                    suma_descargas_secuencia = 0

                                    # --------------------------------------------- DESAPILO VALORES BASURA
                                    # desapilo valores basura del fin
                                    indice_desapilo = len(valores_recarga) - 1
                                    valores_recarga_punto_mas_alto = \
                                        sorted(valores_recarga, key=lambda tup: tup['valor'])[0]['valor']
                                    while indice_desapilo >= 0:
                                        if valores_recarga[indice_desapilo]['valor'] > \
                                                valores_recarga[indice_desapilo - 1]['valor'] or \
                                                valores_recarga[indice_desapilo][
                                                    'valor'] > valores_recarga_punto_mas_alto:
                                            del valores_recarga[indice_desapilo]
                                            indice_desapilo -= 1
                                        else:
                                            break;
                                        if len(valores_recarga) == 1:
                                            valores_recarga = []
                                            break;

                                    # desapilo valores basura del inicio
                                    if len(valores_recarga) > 1:
                                        indice_desapilo = 0
                                        valores_recarga_punto_mas_bajo = \
                                            sorted(valores_recarga, key=lambda tup: tup['valor'], reverse=True)[0][
                                                'valor']
                                        while indice_desapilo < len(valores_recarga):
                                            if valores_recarga[indice_desapilo]['valor'] < \
                                                    valores_recarga[indice_desapilo + 1]['valor'] or \
                                                    valores_recarga[indice_desapilo][
                                                        'valor'] < valores_recarga_punto_mas_bajo:
                                                del valores_recarga[indice_desapilo]
                                            else:
                                                break;
                                            if len(valores_recarga) == 1:
                                                valores_recarga = []
                                                break;
                                                # --------------------------------------------- fin DESAPILO VALORES BASURA

                                    if len(valores_recarga) > 1:
                                        # punto delta_h
                                        # proximo IF para no tomar pequennas series insignificantes que no cumplen con el margen de error
                                        if (abs(valores_recarga[len(valores_recarga) - 1]['valor'] - valores_recarga[0][
                                            'valor']) > valor_precision):
                                            if not (abs(valores_recarga[0]['valor'] -
                                                        valores_recarga[len(valores_recarga) - 1][
                                                            'valor']) == 0):
                                                suma_h_periodo += abs(valores_recarga[0]['valor'] -
                                                                      valores_recarga[len(valores_recarga) - 1][
                                                                          'valor'])
                                                anno_delta_h = datetime.datetime.fromtimestamp(
                                                    valores_recarga[len(valores_recarga) - 1][
                                                        'tiempo_milisegundos'] / 1000.0).year
                                                if verificando_annos.count(anno_delta_h) == 0:
                                                    verificando_annos.append(anno_delta_h)
                                                    cantidad_h_periodo += 1
                                    valores_recarga = []
                                    valores_recarga.append({'valor': valor})
                                else:
                                    valores_recarga = []
                                    valores_recarga.append({'valor': valor})
                            else:
                                valores_recarga.append({'valor': valor})

                            if inicio.month == 12:
                                contador_elementos += 1
                            inicio = inicio + relativedelta(months=1)
                        if cantidad_h_periodo != 0:
                            # promedio=suma_h_periodo / len(elementos[0])
                            promedio = suma_h_periodo / len(verificando_annos)
                        else:
                            promedio = 0.0
                        vals['promedio_h_periodo'] = promedio
                        vals['minimo_h_periodo'] = min
                        vals['maximo_h_periodo'] = max
                        rec_explotable = self.browse( bloque.id).recurso_explotable
                        area = self.browse( bloque.id).area
                        deltaH = 2 * promedio
                        coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000) if (
                                                                                                                  deltaH * area * 1000000) > 0 else 0
                        vals['coeficiente_almacenamiento_calculado'] = coeficiente_calculado
                        if bloque.id:
                            #bloque_obj.write( [bloque.id], vals)
                            bloque.write(vals)
                        else:
                            bloque_obj.create(vals)
                        cont += 1
        return True

    def obtener_promedio_alturas_formula(self, pozo_ids_actualizar, ok):
        if ok:
            # ids=bloque_obj.search(cr, uid, [])
            ids = self.buscar_sectores_directo( pozo_ids_actualizar)
        else:
            ids = pozo_ids_actualizar
        bloque_obj = self.env['df.bloque']
        pozo_obj = self.env['df.pozo']
        cont = 0
        for bloque in self.browse(ids):
            # vals={}
            # suma_h_periodo = 0
            # cantidad_h_periodo = 0
            pozo_ids = pozo_obj.search( [('representativo', '=', True), ('bloque_id', 'in', [bloque.id])]).ids
            if pozo_ids:
                inicio = self.formar_fecha_inicio(pozo_ids)
                fin = self.formar_fecha_fin(pozo_ids)
                if inicio != False and fin != False:
                    elementos = self.calcular_media_por_formula([bloque.id], pozo_ids, inicio, fin)
                    if elementos:
                        vals = {}
                        min = list(elementos[0][0].values())[0]
                        max = 0.0
                        suma_h_periodo = 0
                        cantidad_h_periodo = 0
                        contador_elementos = 0
                        suma_descargas_secuencia = 0
                        valores_recarga = []
                        verificando_annos = []
                        valor_precision = 0.001
                        ultima_recarga = None
                        # dia = 01
                        # mes = 01
                        # anno_inicio=2013
                        # inicio = datetime.datetime(anno_inicio,mes,dia)
                        while inicio <= fin:
                            tiempo = time.strptime(str(inicio.year) + '-' + str(inicio.month) + '-' + str(1),
                                                   "%Y-%m-%d")
                            tiempo_milisegundos = time.mktime(tiempo) * 1000
                            # valor = float("%.3f" % float(elementos[0][contador_elementos][self._mes_numero(inicio.month)]))
                            if elementos[0][contador_elementos].get(str(inicio.month)):
                                valor = float("%.3f" % float(elementos[0][contador_elementos][str(inicio.month)]))
                            if valor != -999999.110:
                                if valor < min:
                                    min = valor
                                if valor > max:
                                    max = valor
                                    # ---------BUSCANDO RECARGAS
                            if len(valores_recarga) > 0:  # si existen valores en analisis
                                valor_anterior = valores_recarga[len(valores_recarga) - 1]['valor']
                                # ------------ VERIFICANO PEQUENNAS DESCARGAS EN SECUENCIA QUE AL FINAL PUEDEN CONLLEVAR A UN DELTA ALTO
                                if valor - valor_anterior <= valor_precision and valor - valor_anterior > 0:
                                    suma_descargas_secuencia += valor - valor_anterior
                                else:
                                    suma_descargas_secuencia = 0
                                if (valor_anterior > valor or (
                                        valor - valor_anterior <= valor_precision and valor - valor_anterior > 0)) and suma_descargas_secuencia < valor_precision:
                                    # lo apilo
                                    valores_recarga.append({'tiempo_milisegundos': tiempo_milisegundos, 'valor': valor})
                                elif len(valores_recarga) > 1:
                                    suma_descargas_secuencia = 0

                                    # --------------------------------------------- DESAPILO VALORES BASURA
                                    # desapilo valores basura del fin
                                    indice_desapilo = len(valores_recarga) - 1
                                    valores_recarga_punto_mas_alto = \
                                        sorted(valores_recarga, key=lambda tup: tup['valor'])[0]['valor']
                                    while indice_desapilo >= 0:
                                        if valores_recarga[indice_desapilo]['valor'] > \
                                                valores_recarga[indice_desapilo - 1]['valor'] or \
                                                valores_recarga[indice_desapilo][
                                                    'valor'] > valores_recarga_punto_mas_alto:
                                            del valores_recarga[indice_desapilo]
                                            indice_desapilo -= 1
                                        else:
                                            break;
                                        if len(valores_recarga) == 1:
                                            valores_recarga = []
                                            break;

                                    # desapilo valores basura del inicio
                                    if len(valores_recarga) > 1:
                                        indice_desapilo = 0
                                        valores_recarga_punto_mas_bajo = \
                                            sorted(valores_recarga, key=lambda tup: tup['valor'], reverse=True)[0][
                                                'valor']
                                        while indice_desapilo < len(valores_recarga):
                                            if valores_recarga[indice_desapilo]['valor'] < \
                                                    valores_recarga[indice_desapilo + 1]['valor'] or \
                                                    valores_recarga[indice_desapilo][
                                                        'valor'] < valores_recarga_punto_mas_bajo:
                                                del valores_recarga[indice_desapilo]
                                            else:
                                                break;
                                            if len(valores_recarga) == 1:
                                                valores_recarga = []
                                                break;
                                                # --------------------------------------------- fin DESAPILO VALORES BASURA

                                    if len(valores_recarga) > 1:
                                        # punto delta_h
                                        # proximo IF para no tomar pequennas series insignificantes que no cumplen con el margen de error
                                        if (abs(valores_recarga[len(valores_recarga) - 1]['valor'] - valores_recarga[0][
                                            'valor']) > valor_precision):
                                            if not (abs(valores_recarga[0]['valor'] -
                                                        valores_recarga[len(valores_recarga) - 1][
                                                            'valor']) == 0):
                                                suma_h_periodo += abs(valores_recarga[0]['valor'] -
                                                                      valores_recarga[len(valores_recarga) - 1][
                                                                          'valor'])
                                                anno_delta_h = datetime.datetime.fromtimestamp(
                                                    valores_recarga[len(valores_recarga) - 1][
                                                        'tiempo_milisegundos'] / 1000.0).year
                                                if verificando_annos.count(anno_delta_h) == 0:
                                                    verificando_annos.append(anno_delta_h)
                                                    cantidad_h_periodo += 1
                                    valores_recarga = []
                                    valores_recarga.append({'valor': valor})
                                else:
                                    valores_recarga = []
                                    valores_recarga.append({'valor': valor})
                            else:
                                valores_recarga.append({'valor': valor})

                            if inicio.month == 12:
                                contador_elementos += 1
                            inicio = inicio + relativedelta(months=1)
                        if cantidad_h_periodo != 0:
                            # promedio=suma_h_periodo / len(elementos[0])
                            promedio = suma_h_periodo / len(verificando_annos)
                        else:
                            promedio = 0.0
                        vals['promedio_h_periodo_formula'] = promedio
                        vals['minimo_h_periodo_formula'] = min
                        vals['maximo_h_periodo_formula'] = max
                        rec_explotable = bloque.recurso_explotable
                        area = bloque.area
                        deltaH = 2 * promedio
                        coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000) if (deltaH * area * 1000000) > 0 else 0
                        vals['coeficiente_almacenamiento_calculado_formula'] = coeficiente_calculado
                        if bloque.id:
                            #bloque_obj.write( [bloque.id], vals)
                            bloque.write(vals)
                        else:
                            bloque_obj.create(vals)
                        cont += 1
        return True

    def obtener_cotas_tramos(self, ids, pozo_ids, fecha_inicio, fecha_fin, tipo):
        # res = {'id': '', 'nombre': '', 'valor_min': 999999.11, 'valor_max': 999999.11}
        # existe = False
        # variable=0
        # global encontro
        temp = 0
        # tipo = 'aritmetica'
        # fecha_inicio =None
        # fecha_fin = None
        datos_generales = []
        for id in ids:
            cota_topografica = self.browse( id).cota_topografica
            if tipo == 'aritmetica':
                if fecha_inicio == None and fecha_fin == None:
                    datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, None, None)
                else:
                    datos_vistas = self.calcular_media_aritmetica(ids, pozo_ids, fecha_inicio, fecha_fin)

            if tipo == 'formula':
                if fecha_inicio == None and fecha_fin == None:
                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, None, None)
                else:
                    datos_vistas = self.calcular_media_por_formula(ids, pozo_ids, fecha_inicio, fecha_fin)

            if datos_vistas:
                for datos_vista in datos_vistas[temp]:
                    dict_cota = {}
                    if datos_vista.get('1'):
                        dict_cota['cota_agua_enero'] = cota_topografica - datos_vista['1']
                    if datos_vista.get('2'):
                        dict_cota['cota_agua_febrero'] = cota_topografica - datos_vista['2']
                    if datos_vista.get('3'):
                        dict_cota['cota_agua_marzo'] = cota_topografica - datos_vista['3']
                    if datos_vista.get('4'):
                        dict_cota['cota_agua_abril'] = cota_topografica - datos_vista['4']
                    if datos_vista.get('5'):
                        dict_cota['cota_agua_mayo'] = cota_topografica - datos_vista['5']
                    if datos_vista.get('6'):
                        dict_cota['cota_agua_junio'] = cota_topografica - datos_vista['6']
                    if datos_vista.get('7'):
                        dict_cota['cota_agua_julio'] = cota_topografica - datos_vista['7']
                    if datos_vista.get('8'):
                        dict_cota['cota_agua_agosto'] = cota_topografica - datos_vista['8']
                    if datos_vista.get('9'):
                        dict_cota['cota_agua_septiembre'] = cota_topografica - datos_vista['9']
                    if datos_vista.get('10'):
                        dict_cota['cota_agua_octubre'] = cota_topografica - datos_vista['10']
                    if datos_vista.get('11'):
                        dict_cota['cota_agua_noviembre'] = cota_topografica - datos_vista['11']
                    if datos_vista.get('12'):
                        dict_cota['cota_agua_diciembre'] = cota_topografica - datos_vista['12']
                    if datos_vista.get('anno'):
                        dict_cota['anno'] = datos_vista['anno']
                    if datos_vista.get('id'):
                        dict_cota['id'] = id
                    datos_generales.append(dict_cota)
                temp += 1
        return datos_generales

    #
    # ##METODOS PARA CALCULO DE NIVELES PRONOSTICOS ... en tramo estan los restantes
    #
    def calcular_nivel_real(self, idd, mes, anno, pozo_ids, metodo):
        """Calcula nivel dado un mes"""
        if type(idd) != int:
            idd = idd[0]
        fecha_inicio = datetime.date(anno, mes, 1)
        end_day = self._lengthmonth(anno, mes)
        fecha_fin = datetime.date(anno, mes, end_day)
        res = None
        if metodo:
            media_aritmetica = self.calcular_media_por_formula([idd], pozo_ids, fecha_inicio, fecha_fin)

        else:
            media_aritmetica = self.calcular_media_aritmetica([idd], pozo_ids, fecha_inicio, fecha_fin)

        if media_aritmetica:
            if media_aritmetica[0][0].get(str(mes)):
                if media_aritmetica[0][0][str(mes)] != -999999.11:
                    res = media_aritmetica[0][0][str(mes)]
        return res

    def _estado_bloque(self):
        bloque_obj = self.env['df.bloque']
        pozo_obj = self.env['df.pozo']
        res = {}
        objeto_bloques = bloque_obj.browse(self.ids)
        # encontro=0
        posicion = 11
        for objeto_bloque in objeto_bloques:
            vals = {}
            vals['id'] = objeto_bloque.id
            temp = 0
            pozo_ids = pozo_obj.search([('representativo', '=', True), ('bloque_id', 'in', [objeto_bloque.id])]).ids
            encontro = 0
            if pozo_ids:
                elementos = self.calcular_media_aritmetica([objeto_bloque.id], pozo_ids, None, None)
                niveles_ordenados = sorted(elementos[temp], key=lambda tup: tup['anno'], reverse=True)
                datos_vistas = self.ordenar_diccionario(niveles_ordenados)
                deltah = self.browse(objeto_bloque.id).promedio_h_periodo
                min_fijo = self.browse(objeto_bloque.id).minimo_h_periodo_fijo
                min_calculado = self.browse(objeto_bloque.id).minimo_h_periodo
                max_fijo = self.browse(objeto_bloque.id).maximo_h_periodo_fijo
                max_calculado = self.browse(objeto_bloque.id).maximo_h_periodo
                if min_fijo <= 0:
                    min = min_calculado
                else:
                    min = min_fijo
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
                                if datos_vista[posicion] >= nivel_alerta and datos_vista[posicion] <= nivel_alarma:
                                    objeto_bloque.estado = 'desfavorable'
                                    vals['estado1'] = 'desfavorable'
                                elif datos_vista[posicion] >= nivel_alarma and datos_vista[posicion] <= max:
                                    objeto_bloque.estado = 'muy desfavorable'
                                    vals['estado1'] = 'muy desfavorable'
                                elif datos_vista[posicion] <= nivel_alerta and datos_vista[posicion] >= (min + deltah):
                                    objeto_bloque.estado = 'favorable'
                                    vals['estado1'] = 'favorable'
                                elif datos_vista[posicion] <= (min + deltah) and datos_vista[posicion] >= min:
                                    objeto_bloque.estado = 'muy favorable'
                                    vals['estado1'] = 'muy favorable'
                                elif datos_vista[posicion] >= max:
                                    objeto_bloque.estado = u'crítico'
                                    vals['estado1'] = u'crítico'
                                else:
                                    objeto_bloque.estado = 'no hay nivel'
                                    vals['estado1'] = 'no hay nivel'
                                # bloque_obj.write(cr,uid,objeto_bloque.id,vals,context)
                                encontro = 1
                                break
                            posicion -= 1
                        posicion = 11
                else:
                    objeto_bloque.estado = 'no hay nivel'
                    vals['estado1'] = 'no hay nivel'
                    # bloque_obj.write(cr,uid,objeto_bloque.id,vals,context)
            else:
                objeto_bloque.estado = 'no hay nivel'
                vals['estado1'] = 'no hay nivel'
                # bloque_obj.write(cr,uid,objeto_bloque.id,vals,context)
        #return res

    sector_id = fields.Many2one('df.sector.hidrologico', string='Hydrogeological sector', required=True)
    provincia_id =fields.Many2one(related='sector_id.provincia_id', readonly=True, string='Country state', store=True, help="This field has the same value of field with the same name in 'Hydrogeological sector'")
    # Este campo provincia_id es de otro modulo que no se ha hecho todavía en ODOO 12

    estado = fields.Char(compute='_estado_bloque', string="State")
    estado1 = fields.Char(string='State', size=64, required=False)

    # equipo_ids =fields.Many2many('df.hc.rain.base.equipment', 'df_equipo_bloque', 'fk_bloque_id', 'fk_equipo_id',string='Pluviometers')
    equipo_ids =fields.Many2many('df.hc.rain.base.equipment', 'df_equipo_bloque', 'fk_bloque_id', 'fk_equipo_id',string='Pluviometers')
    # Este campo equipo_ids es de otro modulo que no se ha hecho todavía en ODOO 12
    seguridad_compania = fields.Char(compute='_seguridad_compania')

    @api.multi
    def write(self, vals):
        cuenca_obj = self.env['df.cuenca.subterranea']
        sector_obj = self.env['df.sector.hidrologico']
        bloque_obj = self.env['df.bloque']
        pozo_obj = self.env['df.pozo']
        super(df_bloque, self).write( vals)
        if vals.get('a0') or vals.get('a1') or vals.get('valor_precision') or vals.get(
                'recurso_explotable'):
            pozo_ids_actualizar = self.ids
            ok = False
            if pozo_ids_actualizar:
                # pozo_obj.obtener_promedio_alturas(cr,uid,pozo_ids_actualizar,ok)
                bloque_obj.obtener_promedio_alturas( pozo_ids_actualizar, ok)
                bloque_obj.obtener_promedio_alturas_formula( pozo_ids_actualizar, ok)
                # sector_obj.obtener_promedio_alturas(cr,uid,pozo_ids_actualizar,ok)
                # sector_obj.obtener_promedio_alturas_formula(cr,uid,pozo_ids_actualizar,ok)
                # cuenca_obj.obtener_promedio_alturas(cr,uid,pozo_ids_actualizar,ok)
                # cuenca_obj.obtener_promedio_alturas_formula(cr,uid,pozo_ids_actualizar,ok)
        return True

    # # def write(self, cr, uid, ids, vals, context=None):
    # #     ids=[1]
    # #     a_cero=1
    # #     a_uno=1
    # #     pozo_ids=[3,10]
    # #     tipo = 'aritmetica'
    # #     fecha_inicio =None
    # #     fecha_fin = None
    # #     datos=self.obtener_cotas_tramos(cr, uid, ids, pozo_ids,fecha_inicio, fecha_fin,tipo,context)
    # #     # datos=self.volumen(cr, uid, ids, pozo_ids,None, None,tipo,a_cero, a_uno,context)
    # #     4
    # #     4
    # #     return super(df_bloque, self).write(cr, uid, ids, vals, context=context)


class df_nivel_anual_sector_hidrologico(models.Model):
    _name = 'df.nivel.anual.sector.hidrologico'
    _inherit = 'df.norma.anual'
    # NO SE PUSO A HEREDAR porque estaba dando error

    _description = "HC Annual level of section"

    anno = fields.Integer(string='Year', required=False)
    sector_id = fields.Many2one('df.sector.hidrologico', string='Sector', required=True)
