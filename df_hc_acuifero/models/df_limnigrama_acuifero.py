# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime, time
from datetime import date
import odoo.tools
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

try:
    from collections import OrderedDict
except ImportError:
    from df_hc_base.ordereddict import OrderedDict


class df_limnigrama_acuifero(models.TransientModel):
    _name = "df.limnigrama.acuifero"
    _description = "Limnigrama"

    @api.model
    def graficar_limnigrama(self, values):
        # datos = [[107, 31, 635, 203, 2],[133, 156, 947, 408, 6],[814, 841, 3714, 727, 31],[1216, 1001, 4436, 738, 40]]
        # return datos
        promedio_h = 0
        promedio_zh = 0
        promedio_zs = 0
        cantidad_h = 0
        cantidad_zh = 0
        cantidad_zs = 0
        serie_temporal_descarga = []
        try:
            result = {
                'object': '',
                'categoryAxis': [],
                'yAxis': [{'minimo': 0, 'maximo': 1000, 'promedio_h_historico': 0, 'minimo_calculado': 0}],
                'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 1000}],
                'series': [
                    {'name': 'Nivel', 'data': []},
                    {'name': 'Nivel Min', 'data': []},
                    {'name': 'Nivel Max', 'data': []},  # 2
                    {'name': 'Delta h medio', 'data': []},  # 3
                    {'name': 'Nivel muy Desfavorable', 'data': []},  # 4
                    {'name': 'Nivel Desfavorable', 'data': []},  # 5
                    {'name': 'Zona de Entrega Restringida', 'data': []},  # 6
                    {'name': 'Zona de Entrega Aumentada', 'data': []},  # 7
                    {'name': 'Delta h', 'data': []},  # 8
                    {'name': 'Delta zs', 'data': []},  # 9
                    {'name': 'Delta zh', 'data': []},  # 10
                    {'name': 'Ano', 'data': []},  # 11
                    {'name': 'Nivel Crítico', 'data': []},  # 12
                    {'name': 'Pronóstico Seco', 'data': []},  # 13
                    {'name': 'Pronóstico 50%', 'data': []},  # 14
                    {'name': 'Pronóstico 75%', 'data': []},  # 15
                    {'name': 'Pronóstico 95%', 'data': []},  # 16
                ]}

            # -------------------------------------CAPTURANDO DATOS DE LA VISTA
            tipo_objeto = values['elemento_graficar']
            duracion = values['duracion_graficar']
            fecha_inicio = values['desde']
            fecha_fin = values['hasta']
            inicio = datetime.datetime(int(fecha_inicio.split('-')[0]), int(fecha_inicio.split('-')[1]), 1)
            fin = datetime.datetime(int(fecha_fin.split('-')[0]), int(fecha_fin.split('-')[1]), 1)

            pozo_obj = self.env['df.pozo']
            # valor_precision = values['valor_precision']
            valor_precision = 0.001


            # -------------------------------------------------- DATA DEL LIMNIGRAMA
            objeto = None
            pozo_ids = None
            if tipo_objeto == 'pozo':
                objeto = values['pozo_id']
                pozo_obj.obtener_promedio_alturas([objeto], True)
                sql = '''SELECT
                anno,
                media_hiperanual_enero_string AS enero,
                media_hiperanual_febrero_string AS febrero,
                media_hiperanual_marzo_string AS marzo,
                media_hiperanual_abril_string AS abril,
                media_hiperanual_mayo_string AS mayo,
                media_hiperanual_junio_string AS junio,
                media_hiperanual_julio_string AS julio,
                media_hiperanual_agosto_string AS agosto,
                media_hiperanual_septiembre_string AS septiembre,
                media_hiperanual_octubre_string AS octubre,
                media_hiperanual_noviembre_string AS noviembre,
                media_hiperanual_diciembre_string AS diciembre
                FROM df_nivel_anual_pozo
                WHERE
                pozo_id = ''' + str(objeto) + ''' AND
                anno BETWEEN ''' + str(inicio.year) + ''' AND ''' + str(fin.year) + '''
                ORDER BY anno ASC'''
                self._cr.execute(sql)
                elementos = self._cr.dictfetchall()
                pozo = pozo_obj.browse(objeto)
                result['object'] = _(' del pozo: ') + pozo.sigla
                promedio_h_historico = pozo.promedio_h_periodo if pozo.promedio_h_periodo_fijo <= 0 else pozo.promedio_h_periodo_fijo
                max_historico = pozo.maximo_h_periodo if pozo.maximo_h_periodo_fijo <= 0 else pozo.maximo_h_periodo_fijo
                min_historico = pozo.minimo_h_periodo if pozo.minimo_h_periodo_fijo <= 0 else pozo.minimo_h_periodo_fijo
                minimo_calculado = pozo.minimo_h_periodo
                result['yAxis'][0]['minimo'] = min_historico
                result['yAxis'][0]['maximo'] = max_historico
                result['yAxis'][0]['promedio_h_historico'] = promedio_h_historico
                result['yAxis'][0]['minimo_calculado'] = minimo_calculado
            else:
                # ------------------------------------SI DE AGRUPAMIENTO CAPTURO LOS POZOS A TENER EN CUENTO
                if len(values['pozo_bloque_ids']) != 0:  # cambiado por Pavel
                    pozo_ids = values['pozo_bloque_ids']
                elif len(values['pozo_sector_ids']) != 0:
                    pozo_ids = values['pozo_sector_ids']
                elif len(values['pozo_cuenca_ids']) != 0:
                    pozo_ids = values['pozo_cuenca_ids']
                else:
                    pozo_ids = None


                # ------------------------------------OBTENGO LOS VALORES DEL AGRUPAMIENTO
                if tipo_objeto == 'bloque':
                    pool_obj = 'df.bloque'
                    objeto = values['bloque_id']
                    if not pozo_ids:
                        pozo_ids = pozo_obj.with_context({'exportar_filtro': 'bloque',
                                                          'filtro': [[0, False, [objeto]]]}).search(
                            [('representativo', '=', True)]).ids

                    result['object'] = _(' del bloque: ') + self.env[pool_obj].search(
                        [('id', '=', objeto)]).sigla  # cambio
                elif tipo_objeto == 'sector':
                    pool_obj = 'df.sector.hidrologico'
                    objeto = values['sector_id']
                    if not pozo_ids:
                        pozo_ids = pozo_obj.with_context({'exportar_filtro': 'sector',
                                                          'filtro': [[0, False, [objeto]]]}).search(
                            [('representativo', '=', True)]).ids

                        # pozo_ids = pozo_obj.search(
                        #     [('representativo', '=', True), ('sector_hidrologico_id', '=', objeto)]).ids
                    result['object'] = _(' del sector: ') + self.env[pool_obj].search(
                        [('id', '=', objeto)]).sigla  # cambio
                elif tipo_objeto == 'cuenca':
                    pool_obj = 'df.cuenca.subterranea'
                    objeto = values['cuenca_id']
                    if not pozo_ids:
                        pozo_ids = pozo_obj.with_context({'exportar_filtro': 'cuenca',
                                                          'filtro': [[0, False, [objeto]]]}).search(
                            [('representativo', '=', True)]).ids

                        # pozo_ids = pozo_obj.search(
                        #     [('representativo', '=', True), ('cuenca_subterranea_id', '=', objeto)]).ids
                    result['object'] = _(' de la cuenca: ') + self.env[pool_obj].search(
                        [('id', '=', objeto)]).codigo  # cambio

                instancia = self.env[pool_obj].browse([objeto])[0]
                bloque_obj = self.env['df.bloque']
                sector_obj = self.env['df.sector.hidrologico']
                cuenca_obj = self.env['df.cuenca.subterranea']
                if values['metodo_formula']:
                    elementos = self.env[pool_obj].calcular_media_por_formula([objeto], pozo_ids, inicio, fin)
                    promedio_h_historico = instancia.promedio_h_periodo_formula if instancia.promedio_h_periodo_fijo <= 0 else instancia.promedio_h_periodo_fijo
                    max_historico = instancia.maximo_h_periodo_formula if instancia.maximo_h_periodo_fijo <= 0 else instancia.maximo_h_periodo_fijo
                    min_historico = instancia.minimo_h_periodo_formula if instancia.minimo_h_periodo_fijo <= 0 else instancia.minimo_h_periodo_fijo
                    bloque_obj.obtener_promedio_alturas_formula(pozo_ids, True)
                    sector_obj.obtener_promedio_alturas_formula(pozo_ids, True)
                    cuenca_obj.obtener_promedio_alturas_formula(pozo_ids, True)
                    minimo_calculado = instancia.minimo_h_periodo_formula
                else:
                    elementos = self.env[pool_obj].calcular_media_aritmetica([objeto], pozo_ids, inicio, fin)
                    promedio_h_historico = instancia.promedio_h_periodo if instancia.promedio_h_periodo_fijo <= 0 else instancia.promedio_h_periodo_fijo
                    max_historico = instancia.maximo_h_periodo if instancia.maximo_h_periodo_fijo <= 0 else instancia.maximo_h_periodo_fijo
                    min_historico = instancia.minimo_h_periodo if instancia.minimo_h_periodo_fijo <= 0 else instancia.minimo_h_periodo_fijo
                    bloque_obj.obtener_promedio_alturas(pozo_ids, True)
                    sector_obj.obtener_promedio_alturas(pozo_ids, True)
                    cuenca_obj.obtener_promedio_alturas(pozo_ids, True)
                    minimo_calculado = instancia.minimo_h_periodo

                result['yAxis'][0]['minimo'] = min_historico
                result['yAxis'][0]['maximo'] = max_historico
                result['yAxis'][0]['promedio_h_historico'] = promedio_h_historico
                result['yAxis'][0]['minimo_calculado'] = minimo_calculado
            # -------------------------------------------------- fin DATA DEL LIMNIGRAMA

            if elementos:
                if tipo_objeto != 'pozo':
                    elementos = elementos[0]
                contador_elementos = 0
                h = 0
                suma_descargas_secuencia = 0
                valores_recarga = []
                verificando_annos = []
                ultima_recarga = None
                while inicio <= fin:
                    h = 0
                    tiempo = time.strptime(str(inicio.year) + '-' + str(inicio.month) + '-' + str(1),
                                           "%Y-%m-%d")
                    tiempo_milisegundos = time.mktime(tiempo) * 1000
                    try:
                        if inicio.year == 1991:
                            a = 5
                        if tipo_objeto == 'pozo':
                            valor = float(
                                "%.3f" % float(elementos[contador_elementos].get(self._mes_numero(inicio.month))))
                        else:
                            valor = float("%.3f" % float(elementos[contador_elementos].get(str(inicio.month))))
                    except Exception:
                        raise UserError(_(
                            'En el rango de fechas seleccionado algunos años no tienen los datos requeridos para graficar. Por favor complete la información.'))
                        # raise osv.except_osv(_('Advertencia'), _(
                        #     'En el rango de fechas seleccionado algunos años no tienen los datos requeridos para graficar. Por favor complete la información.'))

                    # -------------------------- NIVEL
                    if valor < min_historico:
                        valor = min_historico
                    result['series'][0]['data'].append([tiempo_milisegundos, valor])
                    result['series'][1]['data'].append([tiempo_milisegundos, min_historico])
                    result['series'][12]['data'].append([tiempo_milisegundos, float("%.3f" % float(max_historico))])
                    result['series'][4]['data'].append(
                        [tiempo_milisegundos, float("%.3f" % float(max_historico - promedio_h_historico / 2.0))])
                    result['series'][5]['data'].append(
                        [tiempo_milisegundos, float("%.3f" % float(max_historico - promedio_h_historico))])

                    # ---------LLENANDO VALORES DEL AREA DE ENTREGA AUMENTADA
                    if inicio.month == 4:
                        result['series'][7]['data'].append([tiempo_milisegundos, float("%.3f" % float(min_historico))])
                        result['series'][6]['data'].append([tiempo_milisegundos, float("%.3f" % float(max_historico))])
                    elif inicio.month == 10:
                        result['series'][7]['data'].append(
                            [tiempo_milisegundos, float("%.3f" % float(min_historico + promedio_h_historico))])
                        result['series'][6]['data'].append(
                            [tiempo_milisegundos, float("%.3f" % float(max_historico - promedio_h_historico))])

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
                            valores_recarga_punto_mas_alto = sorted(valores_recarga, key=lambda tup: tup['valor'])[0][
                                'valor']
                            while indice_desapilo >= 0:
                                if valores_recarga[indice_desapilo]['valor'] > valores_recarga[indice_desapilo - 1][
                                    'valor'] or valores_recarga[indice_desapilo][
                                    'valor'] > valores_recarga_punto_mas_alto:
                                    del valores_recarga[indice_desapilo]
                                    indice_desapilo -= 1
                                else:
                                    break
                                if len(valores_recarga) == 1:
                                    valores_recarga = []
                                    break

                            # desapilo valores basura del inicio
                            if len(valores_recarga) > 1:
                                indice_desapilo = 0
                                valores_recarga_punto_mas_bajo = \
                                    sorted(valores_recarga, key=lambda tup: tup['valor'], reverse=True)[0]['valor']
                                while indice_desapilo < len(valores_recarga):
                                    if valores_recarga[indice_desapilo]['valor'] < valores_recarga[indice_desapilo + 1][
                                        'valor'] or valores_recarga[indice_desapilo][
                                        'valor'] < valores_recarga_punto_mas_bajo:
                                        del valores_recarga[indice_desapilo]
                                    else:
                                        break
                                    if len(valores_recarga) == 1:
                                        valores_recarga = []
                                        break
                            # --------------------------------------------- fin DESAPILO VALORES BASURA

                            if len(valores_recarga) > 1:
                                # punto delta_h
                                # proximo IF para no tomar pequennas series insignificantes que no cumplen con el margen de error
                                if (abs(valores_recarga[len(valores_recarga) - 1]['valor'] - valores_recarga[0][
                                    'valor']) > valor_precision):
                                    # -----------------AGREGANDO RECARGA
                                    result['series'][8]['data'].append(
                                        [valores_recarga[0]['tiempo_milisegundos'], valores_recarga[0]['valor']])
                                    result['series'][8]['data'].append(
                                        [valores_recarga[len(valores_recarga) - 1]['tiempo_milisegundos'],
                                         valores_recarga[0]['valor']])
                                    result['series'][8]['data'].append(
                                        [valores_recarga[len(valores_recarga) - 1]['tiempo_milisegundos'],
                                         valores_recarga[len(valores_recarga) - 1]['valor']])
                                    result['series'][8]['data'].append(
                                        [valores_recarga[len(valores_recarga) - 1]['tiempo_milisegundos'] + 2678400000,
                                         None])

                                    h = abs(valores_recarga[0]['valor'] - valores_recarga[len(valores_recarga) - 1][
                                        'valor'])
                                    if not (h == 0 and len(result['series'][11]['data']) == 0):
                                        promedio_h += h
                                        cantidad_h += 1
                                    anno_delta_h = datetime.datetime.fromtimestamp(
                                        valores_recarga[len(valores_recarga) - 1]['tiempo_milisegundos'] / 1000.0).year
                                    if verificando_annos.count(anno_delta_h) == 0:
                                        verificando_annos.append(anno_delta_h)
                                        result['series'][11]['data'].append(
                                            {'anno': anno_delta_h, 'delta_h': float("%.3f" % float(h)), 'delta_zh': 0,
                                             'delta_zs': 0})
                                    else:
                                        indice_anno = verificando_annos.index(anno_delta_h)
                                        result['series'][11]['data'][indice_anno]['delta_h'] += float("%.3f" % float(h))

                                    if ultima_recarga:  # AGREGANDO DESCARGA
                                        fecha_inicio_descarga = datetime.datetime.fromtimestamp(
                                            ultima_recarga[0] / 1000.0)
                                        fecha_fin_descarga = datetime.datetime.fromtimestamp(
                                            valores_recarga[0]['tiempo_milisegundos'] / 1000.0)

                                        diff_fechas_descarga_meses = abs(
                                            (fecha_fin_descarga - fecha_inicio_descarga).days) / 30
                                        if (
                                                    fecha_fin_descarga - fecha_inicio_descarga).days >= 28 and diff_fechas_descarga_meses == 0:
                                            diff_fechas_descarga_meses = 1
                                        m_ultima_descarga = abs(ultima_recarga[1] - valores_recarga[0][
                                            'valor']) / diff_fechas_descarga_meses
                                        serie_temporal_descarga.append({'fecha_inicio': ultima_recarga[0],
                                                                        'fecha_fin': valores_recarga[0][
                                                                            'tiempo_milisegundos'],
                                                                        'valor_inicio': ultima_recarga[1],
                                                                        'valor_fin': valores_recarga[0]['valor']})
                                        # AGREGANDO DELTA ZH
                                        fecha_inicio_recarga = datetime.datetime.fromtimestamp(
                                            valores_recarga[0]['tiempo_milisegundos'] / 1000.0)
                                        fecha_fin_recarga = datetime.datetime.fromtimestamp(
                                            valores_recarga[len(valores_recarga) - 1]['tiempo_milisegundos'] / 1000.0)

                                        diff_fechas_recarga_meses = abs(
                                            (fecha_fin_recarga - fecha_inicio_recarga).days) / 30
                                        if (
                                                    fecha_fin_descarga - fecha_inicio_descarga).days >= 28 and diff_fechas_recarga_meses == 0:
                                            diff_fechas_recarga_meses = 1
                                        result['series'][10]['data'].append(
                                            [valores_recarga[0]['tiempo_milisegundos'], valores_recarga[0]['valor']])
                                        result['series'][10]['data'].append(
                                            [valores_recarga[len(valores_recarga) - 1]['tiempo_milisegundos'], float(
                                                "%.3f" % (valores_recarga[0][
                                                              'valor'] + diff_fechas_recarga_meses * m_ultima_descarga))])
                                        result['series'][10]['data'].append(
                                            [valores_recarga[len(valores_recarga) - 1]['tiempo_milisegundos'],
                                             valores_recarga[0]['valor']])
                                        result['series'][10]['data'].append([valores_recarga[len(valores_recarga) - 1][
                                                                                 'tiempo_milisegundos'] + 2678400000,
                                                                             None])

                                    # actualizando ultima recarga para tomar como inicio para la descarga
                                    ultima_recarga = [valores_recarga[len(valores_recarga) - 1]['tiempo_milisegundos'],
                                                      valores_recarga[len(valores_recarga) - 1]['valor']]
                            valores_recarga = []
                            valores_recarga.append({'tiempo_milisegundos': tiempo_milisegundos, 'valor': valor})
                        else:
                            valores_recarga = []
                            valores_recarga.append({'tiempo_milisegundos': tiempo_milisegundos, 'valor': valor})
                    else:
                        valores_recarga.append({'tiempo_milisegundos': tiempo_milisegundos, 'valor': valor})

                    if inicio.month == 12:
                        contador_elementos += 1
                    inicio = inicio + relativedelta(months=1)


            # --------------------------- CHECKEANDO DELTA Z PARA ENCONTRAR DELTA ZH
            incremento_descarga = 0
            while incremento_descarga < len(serie_temporal_descarga):
                fecha_inicio_descarga = datetime.datetime.fromtimestamp(
                    serie_temporal_descarga[incremento_descarga]['fecha_inicio'] / 1000.0)
                fecha_fin_descarga = datetime.datetime.fromtimestamp(
                    serie_temporal_descarga[incremento_descarga]['fecha_fin'] / 1000.0)
                diff_fechas_descarga_meses = abs((fecha_fin_descarga - fecha_inicio_descarga).days) / 30

                cantidad_cortes_descarga = diff_fechas_descarga_meses / 12
                if cantidad_cortes_descarga == 0:
                    result['series'][9]['data'].append([serie_temporal_descarga[incremento_descarga]['fecha_inicio'],
                                                        serie_temporal_descarga[incremento_descarga]['valor_inicio']])
                    result['series'][9]['data'].append([serie_temporal_descarga[incremento_descarga]['fecha_fin'],
                                                        serie_temporal_descarga[incremento_descarga]['valor_inicio']])
                    result['series'][9]['data'].append([serie_temporal_descarga[incremento_descarga]['fecha_fin'],
                                                        serie_temporal_descarga[incremento_descarga]['valor_fin']])
                    result['series'][9]['data'].append(
                        [serie_temporal_descarga[incremento_descarga]['fecha_fin'] + 2678400000, None])
                else:
                    if fecha_inicio_descarga.month < 4 or fecha_inicio_descarga.month > 6:
                        result['series'][9]['data'].append(
                            [serie_temporal_descarga[incremento_descarga]['fecha_inicio'],
                             serie_temporal_descarga[incremento_descarga]['valor_inicio']])
                    ultimo_punto = [serie_temporal_descarga[incremento_descarga]['fecha_inicio'],
                                    serie_temporal_descarga[incremento_descarga]['valor_inicio']]
                    while fecha_inicio_descarga <= fecha_fin_descarga:
                        diff_fechas_descarga_meses = abs((fecha_fin_descarga - fecha_inicio_descarga).days) / 30
                        if fecha_inicio_descarga.month == 4:  # encontre DELTA ZH
                            nivel_encontrado = None
                            tiempo = time.strptime(
                                str(fecha_inicio_descarga.year) + '-' + str(fecha_inicio_descarga.month) + '-' + str(1),
                                "%Y-%m-%d")
                            tiempo_milisegundos = time.mktime(tiempo) * 1000
                            result['series'][9]['data'].append([ultimo_punto[0], ultimo_punto[1]])
                            if diff_fechas_descarga_meses >= 5:
                                result['series'][9]['data'].append([tiempo_milisegundos, ultimo_punto[1]])
                                for nivel in result['series'][0]['data']:
                                    if nivel[0] == tiempo_milisegundos:
                                        nivel_encontrado = nivel[1]
                                        break

                                ultimo_punto = [tiempo_milisegundos, nivel_encontrado]
                                result['series'][9]['data'].append(ultimo_punto)
                                result['series'][9]['data'].append([ultimo_punto[0] + 31 * 24 * 60 * 60 * 1000, None])
                            else:
                                result['series'][9]['data'].append(
                                    [serie_temporal_descarga[incremento_descarga]['fecha_fin'], ultimo_punto[1]])
                                result['series'][9]['data'].append(
                                    [serie_temporal_descarga[incremento_descarga]['fecha_fin'],
                                     serie_temporal_descarga[incremento_descarga]['valor_fin']])
                                result['series'][9]['data'].append(
                                    [serie_temporal_descarga[incremento_descarga]['fecha_fin'] + 2678400000, None])
                                fecha_inicio_descarga = fecha_fin_descarga

                        elif fecha_inicio_descarga.month == 10:  # encontre DELTA ZH
                            nivel_encontrado = None
                            tiempo = time.strptime(
                                str(fecha_inicio_descarga.year) + '-' + str(fecha_inicio_descarga.month) + '-' + str(1),
                                "%Y-%m-%d")
                            tiempo_milisegundos = time.mktime(tiempo) * 1000
                            result['series'][10]['data'].append(ultimo_punto)
                            result['series'][10]['data'].append([tiempo_milisegundos, ultimo_punto[1]])
                            for nivel in result['series'][0]['data']:
                                if nivel[0] == tiempo_milisegundos:
                                    nivel_encontrado = nivel[1]
                                    break

                            ultimo_punto = [tiempo_milisegundos, nivel_encontrado]
                            result['series'][10]['data'].append(ultimo_punto)
                            result['series'][10]['data'].append([ultimo_punto[0] + 2678400000, None])

                        fecha_inicio_descarga = fecha_inicio_descarga + relativedelta(months=1)

                incremento_descarga += 1


            # ---------------- ANNADIENDO RESUMENES ---------------------------------------------------------------------
            indice_descarga = 1
            while (indice_descarga < len(result['series'][10]['data'])):
                delta = abs(result['series'][10]['data'][indice_descarga][1] -
                            result['series'][10]['data'][indice_descarga + 1][1])
                anno_delta = datetime.datetime.fromtimestamp(
                    result['series'][10]['data'][indice_descarga][0] / 1000.0).year
                if not (delta == 0 and len(result['series'][11]['data']) == 0):
                    promedio_zh += delta
                    cantidad_zh += 1
                if verificando_annos.count(anno_delta) == 0:
                    verificando_annos.append(anno_delta)
                    result['series'][11]['data'].append(
                        {'anno': anno_delta, 'delta_h': 0, 'delta_zs': 0, 'delta_zh': float("%.3f" % float(delta))})
                else:
                    posicion_anno = verificando_annos.index(anno_delta)
                    result['series'][11]['data'][posicion_anno]['delta_zh'] = float(
                        "%.3f" % (result['series'][11]['data'][posicion_anno]['delta_zh'] + float(delta)))
                indice_descarga += 4

            indice_descarga = 0
            while (indice_descarga < len(result['series'][9]['data'])):
                if result['series'][9]['data'][indice_descarga][1] == None:
                    delta = abs(result['series'][9]['data'][indice_descarga - 1][1] -
                                result['series'][9]['data'][indice_descarga - 2][1])
                    anno_delta = datetime.datetime.fromtimestamp(
                        result['series'][9]['data'][indice_descarga - 1][0] / 1000.0).year
                    if not (delta == 0 and len(result['series'][11]['data']) == 0):
                        promedio_zs += delta
                        cantidad_zs += 1
                    if verificando_annos.count(anno_delta) == 0:
                        verificando_annos.append(anno_delta)
                        result['series'][11]['data'].append(
                            {'anno': anno_delta, 'delta_h': 0, 'delta_zs': 0, 'delta_zh': float("%.3f" % float(delta))})
                    else:
                        posicion_anno = verificando_annos.index(anno_delta)
                        # result['series'][11]['data'][posicion_anno]['delta_zs'] = float("%.3f" % (result['series'][11]['data'][posicion_anno]['delta_zh'] + float(delta)))
                        result['series'][11]['data'][posicion_anno]['delta_zs'] = float("%.3f" % (float(delta)))
                indice_descarga += 1

            # indice_descarga = 1
            # while(indice_descarga < len(result['series'][9]['data'])):
            #    if result['series'][9]['data'][indice_descarga][1] == None:
            #        delta = abs(result['series'][9]['data'][indice_descarga][1] - result['series'][9]['data'][indice_descarga+1][1])
            #        anno_delta = datetime.datetime.fromtimestamp(result['series'][9]['data'][indice_descarga][0]/1000.0).year
            #        promedio_zs += delta
            #        cantidad_zs += 1
            #        if verificando_annos.count(anno_delta) == 0:
            #            verificando_annos.append(anno_delta)
            #            result['series'][11]['data'].append({'anno':anno_delta,'delta_h':0,'delta_zh':0,'delta_zs':float("%.3f" % float(delta))})
            #        else:
            #            posicion_anno = verificando_annos.index(anno_delta)
            #            result['series'][11]['data'][posicion_anno]['delta_zs'] = float("%.3f" % (result['series'][11]['data'][posicion_anno]['delta_zs'] + float(delta)))
            #    indice_descarga += 4

            result['series'][11]['data'] = sorted(result['series'][11]['data'], key=lambda tup: tup['anno'])
            lista = []
            for i in range(len(result['series'][11]['data'])):
                dic1 = result['series'][11]['data'][i]
                if dic1['delta_h'] == 0:
                    lista.append(i)
            c = 0
            for lis in lista:
                if c > 0:
                    pos = lis - c
                else:
                    pos = lis
                result['series'][11]['data'].__delitem__(pos)
                c += 1
            result['series'][11]['data'].append(
                {'anno': _('Promedio'), 'delta_h': float("%.3f" % float(promedio_h / cantidad_h)),
                 'delta_zh': float("%.3f" % float(promedio_zh / cantidad_zh)),
                 'delta_zs': float("%.3f" % float(promedio_zs / cantidad_zs))})
            result['series'][11]['data'].append({'anno': _('Total'), 'delta_h': float("%.3f" % float(promedio_h)),
                                                 'delta_zh': float("%.3f" % float(promedio_zh)),
                                                 'delta_zs': float("%.3f" % float(promedio_zs))})
            # ---------------- fin de ANNADIENDO RESUMENES ---------------------------------------------------------------------
            # Pronostico
            if values['presage']:
                fecha_inicio = values['desde']
                pronos = values['pronostico']
                meses = values['meses']
                start_month = fecha_inicio.split('-')
                range_start = datetime.datetime(int(start_month[0]), int(start_month[1]), int(start_month[2]))
                range_end = fin
                _year = range_end.year
                _month = range_end.month
                october_exist = False
                month_diff = 0
                while range_start <= range_end:
                    _month = range_end.month
                    if _month == 10:
                        october_exist = True
                        break
                    if _month == 1:
                        _year -= 1
                    _month = (range_end.month - 1) if (range_end.month - 1) >= 1 else 12
                    range_end = datetime.datetime(_year, int(_month), 1)
                    month_diff += 1
                if october_exist is True:
                    dict_len = len(result['series'][0]['data']) - month_diff
                    for i in range(dict_len):
                        result['series'][13]['data'].append([result['series'][0]['data'][i][0], None])
                        result['series'][14]['data'].append([result['series'][0]['data'][i][0], None])
                        result['series'][15]['data'].append([result['series'][0]['data'][i][0], None])
                        result['series'][16]['data'].append([result['series'][0]['data'][i][0], None])
                    # real_rain = {'5': values['may'], '6': values['june'], '7': values['july'], '8': values['august'],
                    #              '9': values['september'], '10': values['october']}
                    real_rain = {'5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0}
                    if duracion == 'P':
                        periodo = 'P'
                    elif duracion == 'Y':
                        periodo = 'Y'
                    elif duracion == '2Y':
                        periodo = '2Y'

                    presage_dict = {'year': _year, 'objeto_tipo': tipo_objeto, 'recurso_explotable': False,
                                    'objeto_id': objeto, 'pozo_ids': [[None, None, pozo_ids]], 'lluv_nreal': real_rain,
                                    'metodo': 'EX',
                                    'duracion': periodo, 'formula': values['metodo_formula'], 'pronostico': pronos,
                                    'meses': meses}
                    value_data = {'data': []}
                    value_data['data'].append(presage_dict)
                    presage_data = self.calcular_pronostico_seco(value_data)
                    _month1 = _month2 = _month
                    _year1 = _year2 = _year
                    for j in presage_data['series'][0]['data']:
                        _month1 = (_month1 + 1) if _month1 < 12 else 1
                        if _month1 == 1:
                            _year1 += 1
                        tiempo = time.strptime(str(_year1) + '-' + str(_month1) + '-' + str(1), "%Y-%m-%d")
                        tiempo_milisegundos = time.mktime(tiempo) * 1000
                        result['series'][13]['data'].append([tiempo_milisegundos, j])
                    if duracion == 'Y':
                        tiempo = 12
                    else:
                        tiempo = 24
                    for k in range(tiempo):
                        _month = (_month + 1) if _month < 12 else 1
                        if _month == 1:
                            _year += 1
                        tiempo = time.strptime(str(_year) + '-' + str(_month) + '-' + str(1), "%Y-%m-%d")
                        tiempo_milisegundos = time.mktime(tiempo) * 1000
                        result['series'][14]['data'].append([tiempo_milisegundos, presage_data['series'][4]['data'][k]])
                        result['series'][15]['data'].append([tiempo_milisegundos, presage_data['series'][5]['data'][k]])
                        result['series'][16]['data'].append([tiempo_milisegundos, presage_data['series'][6]['data'][k]])
                        result['series'][1]['data'].append([tiempo_milisegundos, result['series'][1]['data'][0][1]])
                        result['series'][4]['data'].append([tiempo_milisegundos, result['series'][4]['data'][0][1]])
                        result['series'][5]['data'].append([tiempo_milisegundos, result['series'][5]['data'][0][1]])
                        result['series'][12]['data'].append([tiempo_milisegundos, result['series'][12]['data'][0][1]])
                        # result['series'][0]['data'].append([tiempo_milisegundos, presage_data['series'][1]['data'][k]])
                    if 10 > fin.month >= 4:
                        p_len = 1
                        _month2 = (_month2 + 6) if (_month2 + 6) < 12 else 4
                        if _month2 == 4:
                            _year2 += 1
                    else:
                        p_len = 2
                    for l1 in range(p_len):
                        _month2 = (_month2 + 6) if (_month2 + 6) < 12 else 4
                        if _month2 == 4:
                            _year2 += 1
                        tiempo2 = time.strptime(str(_year2) + '-' + str(_month2) + '-' + str(1), "%Y-%m-%d")
                        tiempo_milisegundos2 = time.mktime(tiempo2) * 1000
                        data_len = len(result['series'][6]['data'])
                        result['series'][6]['data'].append(
                            [tiempo_milisegundos2, result['series'][6]['data'][data_len - 2][1]])
            return result
        except:
            raise UserError(
                _("Ha sido encontrado un error y el proceso de elaboración de la gráfica ha sido detenido.\n"
                  "Los motivos posibles pueden ser:\n"
                  "Datos diarios vacíos o nulos.\n"
                  "Datos de comportamiento históricos vacíos o nulos."))

            #     # raise osv.except_osv(_('Error: '), (
            #     #     "Ha sido encontrado un error y el proceso de elaboración de la gráfica ha sido detenido.\n"
            #     #     "Los motivos posibles pueden ser:\n"
            #     #     "Datos diarios vacíos o nulos\n"
            #     #     "Datos de comportamiento históricos vacíos o nulos"))

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

    def valor_mas_cercano(self, valor, lista):
        if len(lista) == 0:
            raise UserError(_(
                "Ha sido encontrado un error y el proceso de elaboración de la gráfica ha sido detenido.\n"
                "Los motivos posibles pueden ser:\n"
                "No ha guardado latabla ∆Z/∆t de curvas de agotamiento.\n"
                "Datos vacíos o nulos en la fecha seleccionada.\n"))
        data = 0
        arr_reg = []
        arr_zt = []
        for i in lista:
            arr_reg.append(valor - i['regresion'])
            arr_zt.append(i['zt'])
        data = arr_zt[self.posicion_menor(arr_reg)]
        return data

    def posicion_menor(self, lista):
        tam = len(lista)
        temp = -1
        menor = 999999999999
        for i in range(0, tam):
            if lista[i] < menor:
                menor = lista[i]
                temp = i
        return temp

    # pronostico seco
    @api.model
    def calcular_pronostico_seco(self, values):
        result = {'object': '',
                  'recu': '',
                  'dura': '',
                  'year': 2000,
                  'annofin': 2000,
                  'series': [
                      {'name': 'Nivel Pronóstico', 'data': []},
                      {'name': 'Nivel Real', 'data': []},
                      {'name': 'Meses', 'data': []},  # 2
                      {'name': 'Nivel Lluvia Real', 'data': []},  # 3
                      {'name': 'Nivel Pronóstico 50%', 'data': []},  # 4
                      {'name': 'Nivel Pronóstico 75%', 'data': []},  # 5
                      {'name': 'Nivel Pronóstico 95%', 'data': []},  # 6
                      {'name': 'Nivel Abril', 'data': []},  # 7
                  ]}
        tipo = (values['data'][0]['objeto_tipo'])
        idd = (values['data'][0]['objeto_id'])
        year = values['data'][0]['year']
        result['year'] = year
        duracion = values['data'][0]['duracion']

        meses1 = int(values['data'][0]['meses'])
        metodo = values['data'][0]['metodo']
        nreal = values['data'][0]['lluv_nreal']
        formula = False
        pronostico = values['data'][0]['pronostico']
        if values['data'][0].get('formula'):
            formula = values['data'][0]['formula']
        meses = []
        if metodo == 'CA':
            result['recu'] += ' | Método: Curvas de Agotamiento'
        else:
            result['recu'] += ' | Método: Explotación'
        if duracion == 'P':
            result['dura'] += ' | Pronóstico: Período Seco |'
            result['annofin'] = year + 1
        elif duracion == 'Y':
            result['dura'] += ' | Pronóstico: Período Un Año |'
            result['annofin'] = year + 1
        elif duracion == '2Y':
            result['dura'] += ' | Pronóstico: Período Dos Años |'
            result['annofin'] = year + 2
        pronos75 = 0
        cont = 0
        mes10 = False
        ok = False
        while cont < 2:
            if duracion == 'P':
                if ok == True:
                    break
                meses = [10, 11, 12, 1, 2, 3, 4]
            elif duracion == 'Y':
                if ok == True:
                    break
                meses = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            elif duracion == '2Y':
                meses = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            mmcs = [5, 6, 7, 8, 9, 10]
            vol_exp_de_meses1 = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
            lluvias_de_meses = None
            deltaZs = 0
            if duracion == 'Y' or duracion == '2Y':
                lluvias_de_meses = self.obtener_dic_pronostico_lluvia(tipo, idd)
            coef_almac = None
            area = None
            coef_aprob_hid = None
            pozo_ids = []
            nivel = 0
            cota_t = 0
            ca = 0
            val_mes = 0
            val_octubre = 0
            ree = {}
            deltzt = self.datos_tabla_recorridos_zt(tipo, idd)
            pozoobj = self.env['df.pozo']
            sectorobj = self.env['df.sector.hidrologico']
            bloqueobj = self.env['df.bloque']
            cuencaobj = self.env['df.cuenca.subterranea']
            tam = len(meses)
            vaar = ''
            if tipo == 'pozo':
                vaar = 'Pozo '
                vaar += str(pozoobj.browse(idd).sigla)
            elif tipo == 'bloque':
                vaar = 'Bloque '
                vaar += str(bloqueobj.browse(idd).sigla)
            elif tipo == 'sector':
                vaar = 'Sector '
                vaar += str(sectorobj.browse(idd).sigla)
            else:
                vaar = 'Cuenca '
                vaar += str(cuencaobj.browse(idd).codigo)
            # if metodo == 'CA':
            #     result['recu'] += ' | Método: Curvas de Agotamiento'
            # else:
            #     result['recu'] += ' | Método: Explotación'
            # if duracion == 'P':
            #     result['dura'] += ' | Pronóstico: Período Seco'
            # else:
            #     result['dura'] += ' | Pronóstico: Período Dos Años'
            result['object'] = vaar
            nivel_real = None
            last = None
            last1 = None
            for i in range(0, tam - 1):
                if str(tipo) == 'pozo':
                    nivel1 = pozoobj.browse(idd)
                    area = nivel1.area
                    coef_almac = nivel1.coeficiente_almacenamiento
                    coef_aprob_hid = nivel1.coeficiente_aprovechamiento_hidraulico

                    if meses[i] == 10:
                        if cont == 1:
                            if pronostico == 'real':
                                if str(tipo) == 'pozo':
                                    # val_octubre = nivel1.calcular_nivel_real(10, year + 1)
                                    val_octubre = pronos75[1]
                                    result['series'][0]['data'].append(None)
                                else:
                                    # val_octubre = nivel1.calcular_nivel_real(10, year + 1, pozo_ids,formula)
                                    val_octubre = pronos75[1]
                                    result['series'][0]['data'].append(None)
                            else:
                                val_octubre = pronos75[1]  # cambio
                                result['series'][0]['data'].append(None)
                                # year+1
                        else:
                            val_octubre = nivel1.calcular_nivel_real(nivel1.id, meses[i], year)
                    else:
                        if meses[i] == 11 or meses[i] == 12:
                            if cont == 1:
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 1)  # cambio
                            else:
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year)
                                # if pronostico=='real':
                                #     val_octubre = nivel1.calcular_nivel_real(meses[i], year)
                                # if mes10==False:
                                #     result['series'][0]['data'].append(None)
                                #     mes10=True
                        else:
                            if meses[i] == 3:
                                if cont == 1:
                                    last = nivel1.calcular_nivel_real(nivel1.id, 4, year + 2)
                                else:
                                    last = nivel1.calcular_nivel_real(nivel1.id, 4, year + 1)
                            if cont == 1:
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 2)
                            else:
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 1)
                                # if meses[i] == 4:
                                #     if cont ==1:
                                #         nivel_real = nivel1.calcular_nivel_real(5, year + 2)

                    cota_t = pozoobj.browse(idd).cota_topografica
                else:
                    #pozo_ids = values['data'][0]['pozo_ids'][0][2] #cambio
                    pozo_ids = values['data'][0]['pozo_ids']
                    if str(tipo) == 'sector':
                        nivel1 = sectorobj.browse(idd)
                        area = nivel1.area
                        coef_almac = nivel1.coeficiente_almacenamiento
                        coef_aprob_hid = nivel1.coeficiente_aprovechamiento_hidraulico
                        if meses[i] == 10:
                            if cont == 1:
                                if pronostico == 'real':
                                    val_octubre = pronos75[1]
                                    # val_octubre = nivel1.calcular_nivel_real(10, year + 1, pozo_ids,formula)
                                    result['series'][0]['data'].append(None)
                                else:
                                    val_octubre = pronos75[1]  # cambio
                                    result['series'][0]['data'].append(None)
                            else:
                                val_octubre = nivel1.calcular_nivel_real(nivel1.id, meses[i], year, pozo_ids, formula)
                        else:
                            if meses[i] == 11 or meses[i] == 12:
                                if cont == 1:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 1, pozo_ids,
                                                                            formula)
                                else:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year, pozo_ids,
                                                                            formula)
                            else:
                                if meses[i] == 3:
                                    if cont == 1:
                                        last = nivel1.calcular_nivel_real(nivel1.id, 4, year + 2, pozo_ids, formula)
                                    else:
                                        last = nivel1.calcular_nivel_real(nivel1.id, 4, year + 1, pozo_ids, formula)
                                if cont == 1:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 2, pozo_ids,
                                                                            formula)
                                else:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 1, pozo_ids,
                                                                            formula)
                        cota_t = nivel1.cota_topografica
                    elif str(tipo) == 'bloque':
                        nivel1 = bloqueobj.browse(idd)
                        area = nivel1.area
                        coef_almac = nivel1.coeficiente_almacenamiento
                        coef_aprob_hid = nivel1.coeficiente_aprovechamiento_hidraulico
                        if meses[i] == 10:
                            if cont == 1:
                                if pronostico == 'real':
                                    val_octubre = pronos75[1]
                                    # val_octubre = nivel1.calcular_nivel_real(10, year + 1, pozo_ids,formula)
                                    result['series'][0]['data'].append(None)
                                else:
                                    val_octubre = pronos75[1]  # cambio
                                    result['series'][0]['data'].append(None)
                            else:
                                val_octubre = nivel1.calcular_nivel_real(nivel1.id, meses[i], year, pozo_ids, formula)
                        else:
                            if meses[i] == 11 or meses[i] == 12:
                                if cont == 1:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 1, pozo_ids,
                                                                            formula)
                                else:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year, pozo_ids,
                                                                            formula)
                            else:
                                if meses[i] == 3:
                                    if cont == 1:
                                        last = nivel1.calcular_nivel_real(nivel1.id, 4, year + 2, pozo_ids, formula)
                                    else:
                                        last = nivel1.calcular_nivel_real(nivel1.id, 4, year + 1, pozo_ids, formula)
                                if cont == 1:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 2, pozo_ids,
                                                                            formula)
                                else:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 1, pozo_ids,
                                                                            formula)
                        cota_t = nivel1.cota_topografica
                    else:
                        nivel1 = cuencaobj.browse(idd)
                        area = nivel1.area
                        coef_almac = nivel1.coeficiente_almacenamiento
                        coef_aprob_hid = nivel1.coeficiente_aprovechamiento_hidraulico
                        if meses[i] == 10:
                            if cont == 1:
                                if pronostico == 'real':
                                    val_octubre = pronos75[1]
                                    # val_octubre = nivel1.calcular_nivel_real(10, year + 1, pozo_ids,formula)
                                    result['series'][0]['data'].append(None)
                                else:
                                    val_octubre = pronos75[1]  # cambio
                                    result['series'][0]['data'].append(None)
                            else:
                                val_octubre = nivel1.calcular_nivel_real(nivel1.id, meses[i], year, pozo_ids, formula)
                        else:
                            if meses[i] == 11 or meses[i] == 12:
                                if cont == 1:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 1, pozo_ids,
                                                                            formula)
                                else:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year, pozo_ids,
                                                                            formula)
                            else:
                                if meses[i] == 3:
                                    if cont == 1:
                                        last = nivel1.calcular_nivel_real(nivel1.id, 4, year + 2, pozo_ids, formula)
                                    else:
                                        last = nivel1.calcular_nivel_real(nivel1.id, 4, year + 1, pozo_ids, formula)
                                if cont == 1:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 2, pozo_ids,
                                                                            formula)
                                else:
                                    nivel_real = nivel1.calcular_nivel_real(nivel1.id, meses[i], year + 1, pozo_ids,
                                                                            formula)
                        cota_t = nivel1.cota_topografica
                if duracion == 'Y' or duracion == '2Y':
                    for tt in mmcs:
                        # if cont ==1:
                        #     exp = self.obtener_explotacion(cr,uid,tt,year+2,tipo,idd,'P')
                        # else:
                        exp = self.obtener_explotacion(tt, year + 1, tipo, idd, 'P')
                        if exp == -999999.11:
                            raise UserError(_(
                                'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                                    year)))
                            # raise osv.except_osv(_('Advertencia'), _(
                            #     'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                            #         year)))
                        vol_exp_de_meses1[str(tt)] = exp
                if meses[i] == 10:
                    mes10 = True
                    if metodo == 'CA':
                        if cota_t and val_octubre:
                            if cota_t != 0 and val_octubre != 0:
                                ca = cota_t - val_octubre
                            else:
                                raise UserError(_(
                                    'Debe entrar la cota topográfica y el nivel de los pozos seleccionados para el mes de Octubre del año en cuestión.'))
                                # raise osv.except_osv(_('Advertencia'), _(
                                #     'Debe entrar la cota topográfica y el nivel de los pozos seleccionados para el mes de Octubre del año en cuestión.'))
                        else:
                            raise UserError(_(
                                'Debe entrar la cota topográfica y el nivel de los pozos seleccionados para el mes de Octubre del año en cuestión.'))
                            # raise osv.except_osv(_('Advertencia'), _(
                            #     'Debe entrar la cota topográfica y el nivel de los pozos seleccionados para el mes de Octubre del año en cuestión.'))
                        nivel = val_octubre + self.valor_mas_cercano(ca, deltzt)
                    else:
                        if cont == 1:
                            nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, val_octubre, 'P')
                        else:
                            nivel = self.nivel_explotacion(meses[i], year, tipo, idd, val_octubre, 'P')
                    nivel = round(nivel, 2)
                    result['series'][0]['data'].append(nivel)
                    if cont != 1:
                        result['series'][2]['data'].append('Nov.' + str(year))
                    else:
                        result['series'][2]['data'].append('Nov.' + str(year + 1))
                    if duracion == 'Y' or duracion == '2Y':
                        result['series'][3]['data'].append(None)
                        result['series'][4]['data'].append(None)
                        result['series'][5]['data'].append(None)
                        result['series'][6]['data'].append(None)
                elif meses[i] == 11:
                    if metodo == 'CA':
                        ca = cota_t - nivel
                        nivel = nivel + self.valor_mas_cercano(ca, deltzt)
                    else:
                        if pronostico == 'real' and nivel_real != 0 and nivel_real is not None:
                            if meses1 == 11:
                                if cont == 0:
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel_real, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                            else:
                                if cont == 0:
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                        else:
                            if cont == 0:
                                nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                            else:
                                nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                    nivel = round(nivel, 2)
                    result['series'][0]['data'].append(nivel)
                    if nivel_real != 0 and nivel_real is not None:
                        result['series'][1]['data'].append(round(nivel_real, 2))
                    else:
                        result['series'][1]['data'].append(None)
                    if cont != 1:
                        result['series'][2]['data'].append('Dic.' + str(year))
                    else:
                        result['series'][2]['data'].append('Dic.' + str(year + 1))
                    if duracion == 'Y' or duracion == '2Y':
                        result['series'][3]['data'].append(None)
                        result['series'][4]['data'].append(None)
                        result['series'][5]['data'].append(None)
                        result['series'][6]['data'].append(None)
                elif meses[i] == 12:
                    if metodo == 'CA':
                        ca = cota_t - nivel
                        nivel = nivel + self.valor_mas_cercano(ca, deltzt)
                    else:
                        if pronostico == 'real' and nivel_real != 0 and nivel_real is not None:
                            if meses1 == 12:
                                if cont == 0:
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel_real, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                            else:
                                if cont == 0:
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                        else:
                            if cont == 0:
                                nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                            else:
                                nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                    nivel = round(nivel, 2)
                    result['series'][0]['data'].append(nivel)
                    if nivel_real != 0 and nivel_real is not None:
                        result['series'][1]['data'].append(round(nivel_real, 2))
                    else:
                        result['series'][1]['data'].append(None)
                    if cont != 1:
                        result['series'][2]['data'].append('Ene.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('Ene.' + str(year + 2))
                    if duracion == 'Y' or duracion == '2Y':
                        result['series'][3]['data'].append(None)
                        result['series'][4]['data'].append(None)
                        result['series'][5]['data'].append(None)
                        result['series'][6]['data'].append(None)
                elif meses[i] == 1:
                    if metodo == 'CA':
                        ca = cota_t - nivel
                        nivel = nivel + self.valor_mas_cercano(ca, deltzt)
                    else:
                        if pronostico == 'real' and nivel_real != 0 and nivel_real is not None:
                            if meses1 == 1:
                                if cont == 0:
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel_real, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                            else:
                                if cont == 0:
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                        else:
                            if cont == 0:
                                nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                            else:
                                nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                    nivel = round(nivel, 2)
                    result['series'][0]['data'].append(nivel)
                    if nivel_real != 0 and nivel_real:
                        result['series'][1]['data'].append(round(nivel_real, 2))
                    else:
                        result['series'][1]['data'].append(None)
                    if cont != 1:
                        result['series'][2]['data'].append('Feb.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('Feb.' + str(year + 2))
                    if duracion == 'Y' or duracion == '2Y':
                        result['series'][3]['data'].append(None)
                        result['series'][4]['data'].append(None)
                        result['series'][5]['data'].append(None)
                        result['series'][6]['data'].append(None)
                elif meses[i] == 2:
                    if metodo == 'CA':
                        ca = cota_t - nivel
                        nivel = nivel + self.valor_mas_cercano(ca, deltzt)
                    else:
                        if pronostico == 'real' and nivel_real != 0 and nivel_real is not None:
                            if meses1 == 2:
                                if cont == 0:
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel_real, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                            else:
                                if cont == 0:
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                        else:
                            if cont == 0:
                                nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                            else:
                                nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                    nivel = round(nivel, 2)
                    result['series'][0]['data'].append(nivel)
                    if nivel_real != 0 and nivel_real is not None:
                        result['series'][1]['data'].append(round(nivel_real, 2))
                    else:
                        result['series'][1]['data'].append(None)
                    if cont != 1:
                        result['series'][2]['data'].append('Mar.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('Mar.' + str(year + 2))
                    if duracion == 'Y' or duracion == '2Y':
                        result['series'][3]['data'].append(None)
                        result['series'][4]['data'].append(None)
                        result['series'][5]['data'].append(None)
                        result['series'][6]['data'].append(None)
                elif meses[i] == 3:
                    if metodo == 'CA':
                        ca = cota_t - nivel
                        nivel = nivel + self.valor_mas_cercano(ca, deltzt)
                    else:
                        if pronostico == 'real' and nivel_real != 0 and nivel_real is not None:
                            if meses1 == 3:  # Trabajo apartir de aqui con el real si es abril el mes de inicio
                                if cont == 0:
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, last, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                            else:
                                if cont == 0:  # Pronostico apartir de aqui con el pronostico que viene del mes anterior
                                    nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                                else:
                                    nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                        else:
                            if cont == 0:
                                nivel = self.nivel_explotacion(meses[i], year, tipo, idd, nivel, 'P')
                            else:
                                nivel = self.nivel_explotacion(meses[i], year + 1, tipo, idd, nivel, 'P')
                    nivel = round(nivel, 2)
                    result['series'][0]['data'].append(nivel)
                    if nivel_real != 0 and nivel_real is not None:
                        result['series'][1]['data'].append(round(nivel_real, 2))
                    else:
                        result['series'][1]['data'].append(None)
                    if last != None:
                        result['series'][1]['data'].append(round(last, 2))
                    else:
                        result['series'][1]['data'].append(None)
                    if cont != 1:
                        result['series'][2]['data'].append('Abr.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('Abr.' + str(year + 2))
                    if duracion == 'Y' or duracion == '2Y':
                        result['series'][3]['data'].append(None)
                        result['series'][4]['data'].append(None)
                        result['series'][5]['data'].append(None)
                        result['series'][6]['data'].append(None)
                    deltaZs = val_octubre - (result['series'][0]['data'][5])  # REVIZAR AKI
                    if duracion == 'Y' or duracion == '2Y':
                        if cont != 1:
                            if pronostico == 'real':
                                if str(tipo) == 'pozo':
                                    # pronAbril = nivel1.calcular_nivel_real(4, year + 1)
                                    pronAbril = result['series'][0]['data'][5]
                                else:
                                    pronAbril = result['series'][0]['data'][5]
                                    # pronAbril = nivel1.calcular_nivel_real(4, year + 1, pozo_ids,formula)
                            else:
                                pronAbril = result['series'][0]['data'][5]
                        else:
                            if pronostico == 'real':
                                if str(tipo) == 'pozo':
                                    pronAbril = result['series'][0]['data'][17]
                                    # pronAbril = nivel1.calcular_nivel_real(4, year + 2)
                                else:
                                    pronAbril = result['series'][0]['data'][17]
                                    # pronAbril = nivel1.calcular_nivel_real(4, year + 2, pozo_ids,formula)
                            else:
                                pronAbril = result['series'][0]['data'][17]
                        result['series'][7]['data'].append(pronAbril)
                        if cont == 1:
                            anno = year + 2
                        else:
                            anno = year + 1
                        if tipo == 'pozo':
                            ree = pozoobj.browse(idd).calcular_niveles_pronosticos_realesUnion(idd, anno,
                                                                                               vol_exp_de_meses1,
                                                                                               nreal,
                                                                                               pronostico,
                                                                                               lluvias_de_meses,
                                                                                               pronAbril, cont,
                                                                                               meses1)
                            pronos75 = ree['series'][3]['data'][5]
                        elif tipo == 'cuenca':
                            ree = cuencaobj.browse(idd).calcular_niveles_pronosticos_realesUnion(idd, anno,
                                                                                                 vol_exp_de_meses1,
                                                                                                 nreal,
                                                                                                 pronostico,
                                                                                                 tipo,
                                                                                                 lluvias_de_meses,
                                                                                                 pronAbril,
                                                                                                 formula, cont,
                                                                                                 meses1,
                                                                                                 pozo_ids)
                            pronos75 = ree['series'][3]['data'][5]
                        elif tipo == 'sector':
                            ree = sectorobj.browse(idd).calcular_niveles_pronosticos_realesUnion(idd, anno,
                                                                                                 vol_exp_de_meses1,
                                                                                                 nreal,
                                                                                                 pronostico,
                                                                                                 tipo,
                                                                                                 lluvias_de_meses,
                                                                                                 pronAbril,
                                                                                                 formula, cont,
                                                                                                 meses1,
                                                                                                 pozo_ids)
                            pronos75 = ree['series'][3]['data'][5]
                        else:
                            ree = bloqueobj.browse(idd).calcular_niveles_pronosticos_realesUnion(idd, anno,
                                                                                                 vol_exp_de_meses1,
                                                                                                 nreal,
                                                                                                 pronostico,
                                                                                                 tipo,
                                                                                                 lluvias_de_meses,
                                                                                                 pronAbril,
                                                                                                 formula, cont,
                                                                                                 meses1,
                                                                                                 pozo_ids)
                            pronos75 = ree['series'][3]['data'][5]
                        vol_exp_de_meses1 = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
                        for r in ree['series']:
                            if r['name'] == 'Nivel lluvia 50%':
                                result['series'][4]['data'].append(r['data'][0][1])
                                result['series'][4]['data'].append(r['data'][1][1])
                                result['series'][4]['data'].append(r['data'][2][1])
                                result['series'][4]['data'].append(r['data'][3][1])
                                result['series'][4]['data'].append(r['data'][4][1])
                                result['series'][4]['data'].append(r['data'][5][1])
                            if r['name'] == 'Nivel lluvia 75%':
                                result['series'][5]['data'].append(r['data'][0][1])
                                result['series'][5]['data'].append(r['data'][1][1])
                                result['series'][5]['data'].append(r['data'][2][1])
                                result['series'][5]['data'].append(r['data'][3][1])
                                result['series'][5]['data'].append(r['data'][4][1])
                                result['series'][5]['data'].append(r['data'][5][1])
                            if r['name'] == 'Nivel lluvia 95%':
                                result['series'][6]['data'].append(r['data'][0][1])
                                result['series'][6]['data'].append(r['data'][1][1])
                                result['series'][6]['data'].append(r['data'][2][1])
                                result['series'][6]['data'].append(r['data'][3][1])
                                result['series'][6]['data'].append(r['data'][4][1])
                                result['series'][6]['data'].append(r['data'][5][1])
                            if r['name'] == 'Nivel lluvia real':
                                result['series'][3]['data'].append(r['data'][0][1])
                                result['series'][3]['data'].append(r['data'][1][1])
                                result['series'][3]['data'].append(r['data'][2][1])
                                result['series'][3]['data'].append(r['data'][3][1])
                                result['series'][3]['data'].append(r['data'][4][1])
                                result['series'][3]['data'].append(r['data'][5][1])
                            if r['name'] == 'Nivel medido' and cont != 1:
                                result['series'][1]['data'].append(r['data'][0][1])
                                result['series'][1]['data'].append(r['data'][1][1])
                                result['series'][1]['data'].append(r['data'][2][1])
                                result['series'][1]['data'].append(r['data'][3][1])
                                result['series'][1]['data'].append(r['data'][4][1])
                                result['series'][1]['data'].append(r['data'][5][1])
                            if r['name'] == 'Nivel medido' and cont == 1 and tipo == 'pozo':
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 5, year + 2)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 6, year + 2)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 7, year + 2)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 8, year + 2)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 9, year + 2)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 10, year + 2)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                            if r['name'] == 'Nivel medido' and cont == 1 and tipo != 'pozo':
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 5, year + 2, pozo_ids, formula)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 6, year + 2, pozo_ids, formula)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 7, year + 2, pozo_ids, formula)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 8, year + 2, pozo_ids, formula)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 9, year + 2, pozo_ids, formula)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)
                                nivel_real = nivel1.calcular_nivel_real(nivel1.id, 10, year + 2, pozo_ids, formula)
                                if nivel_real != None:
                                    result['series'][1]['data'].append(round(nivel_real, 2))
                                else:
                                    result['series'][1]['data'].append(None)

                elif meses[i] == 4:
                    if cont != 1:
                        result['series'][2]['data'].append('May.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('May.' + str(year + 2))
                    result['series'][0]['data'].append(None)
                elif meses[i] == 5:
                    if cont != 1:
                        result['series'][2]['data'].append('Jun.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('Jun.' + str(year + 2))
                    result['series'][0]['data'].append(None)
                elif meses[i] == 6:
                    if cont != 1:
                        result['series'][2]['data'].append('Jul.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('Jul.' + str(year + 2))
                    result['series'][0]['data'].append(None)
                elif meses[i] == 7:
                    if cont != 1:
                        result['series'][2]['data'].append('Ago.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('Ago.' + str(year + 2))
                    result['series'][0]['data'].append(None)
                elif meses[i] == 8:
                    if cont != 1:
                        result['series'][2]['data'].append('Sep.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('Sep.' + str(year + 2))
                    if cont != 1:
                        result['series'][2]['data'].append('Oct.' + str(year + 1))
                    else:
                        result['series'][2]['data'].append('Oct.' + str(year + 2))
                    result['series'][0]['data'].append(None)

            if values['data'][0]['recurso_explotable']:
                if area != 0 and coef_aprob_hid != 0 and coef_almac != 0:
                    v = deltaZs * area * coef_almac
                    result['recu'] = ' | Recurso Explotable: ' + str(abs(round((v * coef_aprob_hid), 2)))
                else:
                    raise UserError(_(
                        'Debe entrar valores a los campos: (área, coeficiente de almacenamiento'
                        ' y coeficiente de aprobechamiento hidráulico) '
                        'correspondientes al elemento seleccionado.'))
                    # raise osv.except_osv(_('Advertencia'),
                    #                      _('Debe entrar valores a los campos: (área, coeficiente de almacenamiento'
                    #                        ' y coeficiente de aprobechamiento hidráulico) '
                    #                        'correspondientes al elemento seleccionado.'))

            cont += 1
            ok = True

        result['series'][0]['data'].append(None)
        return result


    def obtener_dic_pronostico_lluvia(self, tipo, objetoid):
        probabilidad_Obj = None
        idd = None
        if tipo == 'pozo':
            probabilidad_Obj = self.env['df.probabilidad.pozo']
            tabla_agrupamiento = 'df_probabilidad_pozo'
            sql = """ select anno
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                          where tabla_objeto.pozo_id = '""" + str(objetoid) + """'
                          ORDER BY anno DESC;"""
            self._cr.execute(sql)
            datos_vistas = self._cr.dictfetchall()
            if datos_vistas:
                year = datos_vistas[0]['anno']
                idd = probabilidad_Obj.search([('pozo_id', '=', objetoid), ('anno', '=', year)]).ids
            else:
                raise UserError(_('Debe entrar la probabilidad del pozo'))
                # raise osv.except_osv(_('Advertencia'), _(
                #     'Debe entrar la probalidad del pozo'))

        elif tipo == 'bloque':
            probabilidad_Obj = self.env['df.probabilidad.bloque']
            tabla_agrupamiento = 'df_probabilidad_bloque'
            sql = """ select anno
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                          where tabla_objeto.bloque_id = '""" + str(objetoid) + """'
                          ORDER BY anno DESC;"""
            self._cr.execute(sql)
            datos_vistas = self._cr.dictfetchall()
            if datos_vistas:
                year = datos_vistas[0]['anno']
                idd = probabilidad_Obj.search([('bloque_id', '=', objetoid), ('anno', '=', year)]).ids
            else:
                raise UserError(_('Debe entrar la probabilidad del bloque'))
                # raise osv.except_osv(_('Advertencia'), _(
                #     'Debe entrar la probalidad del bloque'))
        elif tipo == 'sector':
            probabilidad_Obj = self.env['df.probabilidad.sector']
            tabla_agrupamiento = 'df_probabilidad_sector'
            sql = """ select anno
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                          where tabla_objeto.sector_id = '""" + str(objetoid) + """'
                          ORDER BY anno DESC;"""
            self._cr.execute(sql)

            datos_vistas = self._cr.dictfetchall()
            if datos_vistas:
                year = datos_vistas[0].get('anno')
                idd = probabilidad_Obj.search([('sector_id', '=', objetoid), ('anno', '=', year)]).ids
            else:
                raise UserError(_('Debe entrar la probabilidad del sector'))
                # raise osv.except_osv(_('Advertencia'), _(
                #     'Debe entrar la probalidad del sector'))
        else:
            probabilidad_Obj = self.env['df.probabilidad.cuenca']
            tabla_agrupamiento = 'df_probabilidad_cuenca'
            sql = """ select anno
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                          where tabla_objeto.cuenca_id = '""" + str(objetoid) + """'
                          ORDER BY anno DESC;"""
            self._cr.execute(sql)
            datos_vistas = self._cr.dictfetchall()
            if datos_vistas:
                year = datos_vistas[0]['anno']
                idd = probabilidad_Obj.search([('cuenca_id', '=', objetoid), ('anno', '=', year)]).ids
            else:
                raise UserError(_('Debe entrar la probabilidad de la cuenca'))
                # raise osv.except_osv(_('Advertencia'), _(
                #     'Debe entrar la probalidad de la cuenca'))
        mmcs = [5, 6, 7, 8, 9, 10]
        proba = ['50%', '75%', '95%']
        lluvias_de_meses = {'5': {'50': None, '75': None, '95': None}, '6': {'50': None, '75': None, '95': None},
                            '7': {'50': None, '75': None, '95': None},
                            '8': {'50': None, '75': None, '95': None}, '9': {'50': None, '75': None, '95': None},
                            '10': {'50': None, '75': None, '95': None}}
        #        last_idd = idd[len(idd)-1]
        for obj in probabilidad_Obj.browse(idd):
            for p in proba:
                if obj.probabilidad == p and p == '50%':
                    for i in mmcs:
                        if i == 5:
                            lluvias_de_meses['5']['50'] = obj.media_hiperanual_mayo
                        elif i == 6:
                            lluvias_de_meses['6']['50'] = obj.media_hiperanual_junio
                        elif i == 7:
                            lluvias_de_meses['7']['50'] = obj.media_hiperanual_julio
                        elif i == 8:
                            lluvias_de_meses['8']['50'] = obj.media_hiperanual_agosto
                        elif i == 9:
                            lluvias_de_meses['9']['50'] = obj.media_hiperanual_septiembre
                        else:
                            lluvias_de_meses['10']['50'] = obj.media_hiperanual_octubre
                elif obj.probabilidad == p and p == '75%':
                    for i in mmcs:
                        if i == 5:
                            lluvias_de_meses['5']['75'] = obj.media_hiperanual_mayo
                        elif i == 6:
                            lluvias_de_meses['6']['75'] = obj.media_hiperanual_junio
                        elif i == 7:
                            lluvias_de_meses['7']['75'] = obj.media_hiperanual_julio
                        elif i == 8:
                            lluvias_de_meses['8']['75'] = obj.media_hiperanual_agosto
                        elif i == 9:
                            lluvias_de_meses['9']['75'] = obj.media_hiperanual_septiembre
                        else:
                            lluvias_de_meses['10']['75'] = obj.media_hiperanual_octubre
                elif obj.probabilidad == p and p == '95%':
                    for i in mmcs:
                        if i == 5:
                            lluvias_de_meses['5']['95'] = obj.media_hiperanual_mayo
                        elif i == 6:
                            lluvias_de_meses['6']['95'] = obj.media_hiperanual_junio
                        elif i == 7:
                            lluvias_de_meses['7']['95'] = obj.media_hiperanual_julio
                        elif i == 8:
                            lluvias_de_meses['8']['95'] = obj.media_hiperanual_agosto
                        elif i == 9:
                            lluvias_de_meses['9']['95'] = obj.media_hiperanual_septiembre
                        else:
                            lluvias_de_meses['10']['95'] = obj.media_hiperanual_octubre
        return lluvias_de_meses


    def datos_tabla_recorridos_zt(self, tipo, id):
        sql = """
                    SELECT
                      df_tabla_regresion.tiempo,
                      df_tabla_regresion.regresion,
                      df_tabla_regresion.zt
                    FROM
                      public.df_tabla_regresion
                    WHERE
                      df_tabla_regresion.objeto_tipo = '""" + str(tipo) + """' AND
                      df_tabla_regresion.objeto_id = '""" + str(id) + """'
                    """
        self._cr.execute(sql)
        data = self._cr.dictfetchall()
        return data


    def obtener_explotacion(self, mes, year, tipo, idtipo, t_exp):
        explotacion = 0
        if t_exp == 'P':
            exp_planificada_pozo_obj = self.env['df.plan.explotacion.anual.pozo']
            exp_planificada_bloque_obj = self.env['df.explotacion.bloque.plan']
            exp_planificada_sector_obj = self.env['df.explotacion.sector.plan']
            exp_planificada_cuenca_obj = self.env['df.explotacion.cuenca.plan']
        if t_exp == 'R':
            exp_planificada_pozo_obj = self.env['df.explotacion.anual.pozo']
            exp_planificada_bloque_obj = self.env['df.explotacion.bloque.real']
            exp_planificada_sector_obj = self.env['df.explotacion.sector.real']
            exp_planificada_cuenca_obj = self.env['df.explotacion.cuenca.real']

        if tipo == 'pozo':
            idd = exp_planificada_pozo_obj.search([('anno', '=', year), ('pozo_id', '=', idtipo)]).id
            if idd:
                if mes == 1:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_enero
                elif mes == 2:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_febrero
                elif mes == 3:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_marzo
                elif mes == 4:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_abril
                elif mes == 5:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_mayo
                elif mes == 6:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_junio
                elif mes == 7:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_julio
                elif mes == 8:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_agosto
                elif mes == 9:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_septiembre
                elif mes == 10:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_octubre
                elif mes == 11:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_noviembre
                else:
                    explotacion = exp_planificada_pozo_obj.browse(idd)[0].media_hiperanual_diciembre
            else:
                raise UserError(_(
                    'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                        year)))
                # raise osv.except_osv(_('Advertencia'), _(
                # 'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                #     year)))
        elif tipo == 'bloque':
            idd = exp_planificada_bloque_obj.search([('anno', '=', year), ('bloque_id', '=', idtipo)]).id
            if idd:
                if mes == 1:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_enero
                elif mes == 2:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_febrero
                elif mes == 3:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_marzo
                elif mes == 4:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_abril
                elif mes == 5:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_mayo
                elif mes == 6:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_junio
                elif mes == 7:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_julio
                elif mes == 8:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_agosto
                elif mes == 9:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_septiembre
                elif mes == 10:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_octubre
                elif mes == 11:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_noviembre
                else:
                    explotacion = exp_planificada_bloque_obj.browse(idd)[0].media_hiperanual_diciembre
            else:
                raise UserError(_(
                    'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                        year)))
                # raise osv.except_osv(_('Advertencia'), _(
                # 'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                #     year)))
        elif tipo == 'sector':
            idd = exp_planificada_sector_obj.search([('anno', '=', year), ('sector_id', '=', idtipo)]).id
            if idd:
                if mes == 1:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_enero
                elif mes == 2:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_febrero
                elif mes == 3:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_marzo
                elif mes == 4:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_abril
                elif mes == 5:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_mayo
                elif mes == 6:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_junio
                elif mes == 7:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_julio
                elif mes == 8:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_agosto
                elif mes == 9:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_septiembre
                elif mes == 10:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_octubre
                elif mes == 11:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_noviembre
                else:
                    explotacion = exp_planificada_sector_obj.browse(idd)[0].media_hiperanual_diciembre
            else:
                raise UserError(_(
                    'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                        year)))
                # raise osv.except_osv(_('Advertencia'), _(
                # 'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                #     year)))
        else:
            idd = exp_planificada_cuenca_obj.search([('anno', '=', year), ('cuenca_id', '=', idtipo)]).id
            if idd:
                if mes == 1:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_enero
                elif mes == 2:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_febrero
                elif mes == 3:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_marzo
                elif mes == 4:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_abril
                elif mes == 5:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_mayo
                elif mes == 6:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_junio
                elif mes == 7:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_julio
                elif mes == 8:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_agosto
                elif mes == 9:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_septiembre
                elif mes == 10:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_octubre
                elif mes == 11:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_noviembre
                else:
                    explotacion = exp_planificada_cuenca_obj.browse(idd)[0].media_hiperanual_diciembre
            else:
                raise UserError(_(
                    'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                        year)))
                # raise osv.except_osv(_('Advertencia'), _(
                # 'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                #     year)))

        return explotacion


    def nivel_explotacion(self, mes, year, tipo, idtipo, nivel_anterior, t_exp):
        nivel = -1
        delta_h = 0
        delta_z = 0
        delta_t = 1
        explotacion = 0
        pozo_obj = self.env['df.pozo']
        bloque_obj = self.env['df.bloque']
        sector_obj = self.env['df.sector.hidrologico']
        cuenca_obj = self.env['df.cuenca.subterranea']
        # ESTOY SUMANDO 1 AL MES PARA QUE LA PRIMERA SEA NOVIEMBRE
        explotacion = self.obtener_explotacion(mes + 1, year, tipo, idtipo, t_exp)
        if explotacion == -999999.11:
            raise UserError(_(
                'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
                    year)))
            # raise osv.except_osv(_('Advertencia'), _(
            #     'Debe entrar la explotación planificada de todos los meses del objeto seleccionado para el año ' + str(
            #         year)))
        if tipo == 'pozo':
            idd = pozo_obj.search([('id', '=', idtipo)]).id
            delta_z = pozo_obj.browse(idd)[0].calcular_delta_z1(explotacion, idtipo)
        elif tipo == 'bloque':
            idd = bloque_obj.search([('id', '=', idtipo)]).id
            delta_z = bloque_obj.browse(idd)[0].calcular_delta_z1(explotacion, idtipo, tipo)
        elif tipo == 'sector':
            idd = sector_obj.search([('id', '=', idtipo)]).id
            delta_z = sector_obj.browse(idd)[0].calcular_delta_z1(explotacion, idtipo, tipo)
        else:
            idd = cuenca_obj.search([('id', '=', idtipo)]).id
            delta_z = cuenca_obj.browse(idd)[0].calcular_delta_z1(explotacion, idtipo)
        if nivel_anterior == None:
            raise UserError(
                _('No se puede realizar el pronóstico debido a que falta el nivel del mes de octubre para el año' + str(
                    year)))
            # raise osv.except_osv(_('Advertencia'), _(
            #     'No se puede realizar el pronóstico debido a que falta el nivel del mes de octubre para el año' + str(
            #         year)))
        nivel = nivel_anterior - (delta_h - delta_z / delta_t)

        return nivel


    @api.model
    def graficar_limnigrama_cotas(self, values):
        try:
            result = {
                'categoryAxis': [],
                'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 100}],
                'series': [
                    {'name': 'Nivel', 'data': []},
                    {'name': 'V', 'data': []},
                    {'name': 'H', 'data': []},
                    {'name': 'Cota', 'data': []},
                ]}
            tipo_objeto = values['elemento_graficar']
            fecha_inicio = values['desde']
            fecha_fin = values['hasta']
            pozo_obj = self.env['df.pozo']
            if len(values['pozo_bloque_ids']) != 0:
                pozo_ids = values['pozo_bloque_ids']
            elif len(values['pozo_sector_ids']) != 0:
                pozo_ids = values['pozo_sector_ids']
            elif len(values['pozo_cuenca_ids']) != 0:
                pozo_ids = values['pozo_cuenca_ids']
            else:
                pozo_ids = None
            if values.get('a0'):
                a0 = values['a0']
            else:
                a0 = 0
            if values.get('a1'):
                a1 = values['a1']
            else:
                a1 = 0

            inicio = datetime.datetime(int(fecha_inicio.split('-')[0]), int(fecha_inicio.split('-')[1]), 1)
            fin = datetime.datetime(int(fecha_fin.split('-')[0]), int(fecha_fin.split('-')[1]), 1)
            if tipo_objeto == 'pozo':
                objeto = values['pozo_id']
                pozo = pozo_obj.browse(objeto)

                sql = '''SELECT * FROM df_nivel_anual_pozo
                             WHERE
                               pozo_id = ''' + str(objeto) + ''' AND
                               anno BETWEEN ''' + str(inicio.year) + ''' AND ''' + str(fin.year) + '''
                             ORDER BY anno ASC'''
                self.env.cr.execute(sql)
                elementos = self.env.cr.dictfetchall()

                sql = """SELECT * FROM df_report_cota_agua
                             WHERE
                                sigla = '""" + str(pozo.sigla) + """' AND
                                anno BETWEEN """ + str(inicio.year) + """ AND """ + str(fin.year) + """
                             ORDER BY anno ASC"""
                self.env.cr.execute(sql)
                cotas = self.env.cr.dictfetchall()

                volumenes = pozo_obj.volumen([values['pozo_id']], inicio, fin)
                alturas = pozo_obj.altura([values['pozo_id']], inicio, fin)
            else:
                if tipo_objeto == 'bloque':
                    pool_obj = 'df.bloque'
                    objeto = values['bloque_id']
                elif tipo_objeto == 'sector':
                    pool_obj = 'df.sector.hidrologico'
                    objeto = values['sector_id']
                elif tipo_objeto == 'cuenca':
                    pool_obj = 'df.cuenca.subterranea'
                    objeto = values['cuenca_id']

                volumenes = self.env[pool_obj].volumen([objeto], pozo_ids, inicio, fin,
                                                       ("formula" if (values['metodo_formula']) else "aritmetica"))
                alturas = self.env[pool_obj].altura([objeto], pozo_ids, inicio, fin,
                                                    ("formula" if (values['metodo_formula']) else "aritmetica"))

                if values['metodo_formula']:
                    elementos = self.env[pool_obj].calcular_media_por_formula([objeto], pozo_ids, inicio, fin)
                else:
                    elementos = self.env[pool_obj].calcular_media_aritmetica([objeto], pozo_ids, inicio, fin)

                cotas = self.env[pool_obj].obtener_cotas_tramos([objeto], pozo_ids,
                                                                datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d"),
                                                                datetime.datetime.strptime(fecha_fin, "%Y-%m-%d"),
                                                                ("formula" if (
                                                                    values['metodo_formula']) else "aritmetica"))

            if elementos:
                iterador_meses = inicio.month
                if tipo_objeto != 'pozo':
                    elementos = elementos[0]
                for elemento in elementos:
                    while iterador_meses <= 12 and (iterador_meses <= fin.month or elemento['anno'] < fin.year):
                        times = time.strptime(str((elemento['anno'])) + '-' + str(iterador_meses) + '-' + str(1),
                                              "%Y-%m-%d")
                        times_milisecond = time.mktime(times) * 1000
                        for cota in cotas:
                            if cota['anno'] == elemento['anno']:
                                if cota.get('cota_agua_' + self._mes_numero_full(iterador_meses)) and cota[
                                            'cota_agua_' + self._mes_numero_full(iterador_meses)] != -999999.11:
                                    result['series'][3]['data'].append([times_milisecond, float(
                                        "%.3f" % float(cota['cota_agua_' + self._mes_numero_full(iterador_meses)]))])
                                else:
                                    break;
                        for volumen in volumenes:
                            if volumen['anno'] == elemento['anno']:
                                if volumen.get(str(iterador_meses)):
                                    result['series'][1]['data'].append(
                                        [times_milisecond, float("%.3f" % float(volumen[str(iterador_meses)]))])
                                else:
                                    break;
                        for altura in alturas:
                            if altura['anno'] == elemento['anno']:
                                if altura.get(str(iterador_meses)):
                                    result['series'][2]['data'].append(
                                        [times_milisecond, float("%.3f" % float(altura[str(iterador_meses)]))])
                                else:
                                    break;

                        if tipo_objeto == 'pozo':
                            valor_string = str(
                                elemento['media_hiperanual_' + self._mes_numero_full(iterador_meses) + '_string'])
                        else:
                            if elemento.get(str(iterador_meses)):
                                valor_string = str(elemento[str(iterador_meses)])
                            else:
                                valor_string = None

                        if valor_string != '' and valor_string != False and valor_string != None:
                            result['series'][0]['data'].append([times_milisecond, float("%.3f" % float(valor_string))])
                        else:
                            result['series'][0]['data'].append([times_milisecond, None])
                        iterador_meses += 1
                    iterador_meses = 1
            return result
        except:
            raise UserError(
                _("Ha sido encontrado un error y el proceso de elaboración de la gráfica ha sido detenido.\n"
                  "Los motivos posibles pueden ser:\n"
                  "Datos diarios vacíos o nulos.\n"
                  "Datos de comportamiento históricos vacíos o nulos."))


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


    @api.model
    def graficar_limnigrama_explotacion(self, values):
        try:
            tipo_objeto = values['elemento_graficar']
            result = {
                'categoryAxis': [],
                'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 100}],
                'series': [
                    {'name': 'Nivel', 'data': []},
                    {'name': 'Explotación real', 'data': []},
                    {'name': 'Explotación plan', 'data': []},
                    {'name': 'LLuvia Acumulada', 'data': []},
                    {'name': 'Rango', 'data': []}
                ]}
            fecha_inicio = values['desde']
            fecha_fin = values['hasta']
            start_month = fecha_inicio.split('-')
            end_month = fecha_fin.split('-')
            pozo_obj = self.env['df.pozo']
            if len(values['pozo_bloque_ids']) != 0:
                pozo_ids = values['pozo_bloque_ids']
            elif len(values['pozo_sector_ids']) != 0:
                pozo_ids = values['pozo_sector_ids']
            elif len(values['pozo_cuenca_ids']) != 0:
                pozo_ids = values['pozo_cuenca_ids']
            else:
                pozo_ids = None
            if values.get('a0'):
                a0 = values['a0']
            else:
                a0 = 0
            if values.get('a1'):
                a1 = values['a1']
            else:
                a1 = 0
            if tipo_objeto == 'pozo':
                pozo_ids_aux = []
                pozo_ids_aux.append(values['pozo_id'])
            else:
                pozo_ids_aux = pozo_ids
            equipment_ids = self.search_equipmenets(pozo_ids_aux)  # Comentariado mientras no se migre lluvia (Pavel)
            user = self.env['res.users'].browse(self._uid)
            _date_dict = []
            range_start = datetime.datetime(int(start_month[0]), int(start_month[1]), int(start_month[2]))
            range_end = datetime.datetime(int(end_month[0]), int(end_month[1]), int(end_month[2]))
            _year = range_start.year
            while range_start <= range_end:
                _date_dict.append({'mes': range_start.month, 'anio': _year})
                _month = range_start.month + 1 if range_start.month < 12 else 1
                if _month == 1:
                    _year += 1
                range_start = datetime.datetime(_year, int(_month), int(start_month[2]))
            rain_dict = self.env['df.hc.rain.base.integracion'].lecturas_equip_red_mensual(equipment_ids,
                                                                                           _date_dict)  # Comentariado mientras no se migre lluvia (Pavel)
            for _rain_list in rain_dict:
                times = _rain_list['_times']
                # times_milisecond = time.mktime(_rain_list['_date']) * 1000
                times_milisecond = time.mktime(times) * 1000
                # _mayor = float("%.3f" % float(_rain_list['mayor'])) if float(_rain_list['mayor']) > 0 else None
                # _menor = float("%.3f" % float(_rain_list['menor'])) if float(_rain_list['menor']) > 0 else None
                result['series'][3]['data'].append([times_milisecond, float("%.3f" % float(_rain_list['acumulado']))])
                result['series'][4]['data'].append([times_milisecond, float("%.3f" % float(_rain_list['menor'])),
                                                    float("%.3f" % float(_rain_list['mayor']))])
            # list_rain = []
            # for dat in rain_dict:
            #     list_rain.append(dat)
            # list_ordenada = sorted(list_rain, key=lambda tup: tup['year'])
            # for list1 in list_ordenada:
            #     for i in range(1, 12):
            #         a = 0

            inicio = datetime.datetime(int(fecha_inicio.split('-')[0]), int(fecha_inicio.split('-')[1]), 1)
            fin = datetime.datetime(int(fecha_fin.split('-')[0]), int(fecha_fin.split('-')[1]), 1)
            if tipo_objeto == 'pozo':
                objeto = values['pozo_id']
                pozo = pozo_obj.browse(objeto)

                sql = '''SELECT * FROM df_nivel_anual_pozo
                   WHERE
                   pozo_id = ''' + str(objeto) + ''' AND
                   anno BETWEEN ''' + str(inicio.year) + ''' AND ''' + str(fin.year) + '''
                   ORDER BY anno ASC'''
                self.env.cr.execute(sql)
                elementos = self.env.cr.dictfetchall()

                sql = """SELECT
                               anno,
                               (NULLIF(media_hiperanual_enero, -999999.110)) as enero,
                               (NULLIF(media_hiperanual_febrero, -999999.110)) as febrero,
                               (NULLIF(media_hiperanual_marzo, -999999.110)) as marzo,
                               (NULLIF(media_hiperanual_abril, -999999.110)) as abril,
                               (NULLIF(media_hiperanual_mayo, -999999.110)) as mayo,
                               (NULLIF(media_hiperanual_junio, -999999.110)) as junio,
                               (NULLIF(media_hiperanual_julio, -999999.110)) as julio,
                               (NULLIF(media_hiperanual_agosto, -999999.110)) as agosto,
                               (NULLIF(media_hiperanual_septiembre, -999999.110)) as septiembre,
                               (NULLIF(media_hiperanual_octubre, -999999.110)) as octubre,
                               (NULLIF(media_hiperanual_noviembre, -999999.110)) as noviembre,
                               (NULLIF(media_hiperanual_diciembre, -999999.110)) as diciembre
                   FROM df_explotacion_anual_pozo
                   WHERE
                   pozo_id = '""" + str(pozo.id) + """' AND
                   anno BETWEEN """ + str(inicio.year) + """ AND """ + str(fin.year) + """
                   ORDER BY anno ASC"""
                self.env.cr.execute(sql)
                explotaciones = self.env.cr.dictfetchall()

                sql = """SELECT
                               anno,
                               (NULLIF(media_hiperanual_enero, -999999.110)) as enero,
                               (NULLIF(media_hiperanual_febrero, -999999.110)) as febrero,
                               (NULLIF(media_hiperanual_marzo, -999999.110)) as marzo,
                               (NULLIF(media_hiperanual_abril, -999999.110)) as abril,
                               (NULLIF(media_hiperanual_mayo, -999999.110)) as mayo,
                               (NULLIF(media_hiperanual_junio, -999999.110)) as junio,
                               (NULLIF(media_hiperanual_julio, -999999.110)) as julio,
                               (NULLIF(media_hiperanual_agosto, -999999.110)) as agosto,
                               (NULLIF(media_hiperanual_septiembre, -999999.110)) as septiembre,
                               (NULLIF(media_hiperanual_octubre, -999999.110)) as octubre,
                               (NULLIF(media_hiperanual_noviembre, -999999.110)) as noviembre,
                               (NULLIF(media_hiperanual_diciembre, -999999.110)) as diciembre
                   FROM df_plan_explotacion_anual_pozo
                   WHERE
                   pozo_id = '""" + str(pozo.id) + """' AND
                   anno BETWEEN """ + str(inicio.year) + """ AND """ + str(fin.year) + """
                   ORDER BY anno ASC"""
                self.env.cr.execute(sql)
                plan_explotaciones = self.env.cr.dictfetchall()
            else:
                if tipo_objeto == 'bloque':
                    pool_obj = 'df.bloque'
                    objeto = values['bloque_id']
                elif tipo_objeto == 'sector':
                    pool_obj = 'df.sector.hidrologico'
                    objeto = values['sector_id']
                elif tipo_objeto == 'cuenca':
                    pool_obj = 'df.cuenca.subterranea'
                    objeto = values['cuenca_id']

                explotaciones = self.env[pool_obj].calcular_explotacion_acumulada([objeto], inicio, fin)
                explotaciones = explotaciones[0]

                plan_explotaciones = self.env[pool_obj].plan_explotacion([objeto], inicio, fin)
                plan_explotaciones = plan_explotaciones[0]

                # equipos_lluvia_ids = []
                # for pozo_id in self.pool.get('df.pozo').browse(cr, uid, pozo_ids):
                #     for equipo_id in pozo_id.equipo_ids:
                #         equipos_lluvia_ids.append(equipo_id.id)
                #
                # user = self.pool.get('res.users').browse(cr, uid, uid)
                # equipos_lluvia_ids = str(equipos_lluvia_ids).replace('[', '(').replace(']', ')')
                # lluvias = self.pool.get('df.hc.rain.base.integracion').lecturas_equip_red_mensual(cr, uid,
                #                                                                                   str(user.company_id.id),
                #                                                                                   equipos_lluvia_ids,
                #                                                                                   inicio.month, fin.month,
                #                                                                                   inicio.year, fin.year)

                # plan_explotaciones = plan_explotaciones

                if values['metodo_formula']:
                    elementos = self.env[pool_obj].calcular_media_por_formula([objeto], pozo_ids, inicio, fin)
                else:
                    elementos = self.env[pool_obj].calcular_media_aritmetica([objeto], pozo_ids, inicio, fin)

            if elementos:
                iterador_meses = inicio.month
                if tipo_objeto != 'pozo':
                    elementos = elementos[0]
                for elemento in elementos:
                    while iterador_meses <= 12 and (iterador_meses <= fin.month or elemento['anno'] < fin.year):
                        times = time.strptime(str((elemento['anno'])) + '-' + str(iterador_meses) + '-' + str(1),
                                              "%Y-%m-%d")
                        times_milisecond = time.mktime(times) * 1000

                        if tipo_objeto == 'pozo':
                            for explotacion in explotaciones:
                                if explotacion['anno'] == elemento['anno']:
                                    nombre_mes = self._mes_numero_full(iterador_meses)
                                    if explotacion.get(nombre_mes):
                                        result['series'][1]['data'].append(
                                            [times_milisecond, float("%.3f" % float(explotacion[nombre_mes]))])
                                    break;
                            for explotacion in plan_explotaciones:
                                if explotacion['anno'] == elemento['anno']:
                                    nombre_mes = self._mes_numero_full(iterador_meses)
                                    if explotacion.get(nombre_mes):
                                        result['series'][2]['data'].append(
                                            [times_milisecond, float("%.3f" % float(explotacion[nombre_mes]))])
                                    break;
                        else:
                            for explotacion in explotaciones:
                                if explotacion['anno'] == elemento['anno']:
                                    if explotacion.get(str(iterador_meses)):
                                        result['series'][1]['data'].append(
                                            [times_milisecond, float("%.3f" % float(explotacion[str(iterador_meses)]))])
                                    break;
                            for explotacion in plan_explotaciones:
                                if explotacion['anno'] == elemento['anno']:
                                    if explotacion.get(str(iterador_meses)):
                                        result['series'][2]['data'].append(
                                            [times_milisecond, float("%.3f" % float(explotacion[str(iterador_meses)]))])
                                    break;
                        if tipo_objeto == 'pozo':
                            valor_string = str(
                                elemento['media_hiperanual_' + self._mes_numero_full(iterador_meses) + '_string'])
                        else:
                            if elemento.get(str(iterador_meses)):
                                valor_string = str(elemento[str(iterador_meses)])
                            else:
                                valor_string = None

                        if valor_string != '' and valor_string != False and valor_string != None:
                            result['series'][0]['data'].append([times_milisecond, float("%.3f" % float(valor_string))])
                        else:
                            result['series'][0]['data'].append([times_milisecond, None])
                        iterador_meses += 1
                    iterador_meses = 1
            return result
        except:
            raise UserError(
                _("Ha sido encontrado un error y el proceso de elaboración de la gráfica ha sido detenido.\n"
                  "Los motivos posibles pueden ser:\n"
                  "Datos diarios vacíos o nulos.\n"
                  "Datos de comportamiento históricos vacíos o nulos."))

    def search_equipmenets(self, values):
        array_eq = []
        for value in values:
            sql = """
                    SELECT
                      e.id
                    FROM df_hc_rain_base_equipment e
                        inner join df_equipo_pozo ep on ep.fk_equipo_id = e.id inner join df_pozo p on ep.fk_pozo_id = p.id

                    where
                        p.id = """ + str(value) + """
                """
            self.env.cr.execute(sql)
            equipments = self.env.cr.fetchall()
            # array_eq = []
            for i in equipments:
                array_eq.append(i[0])
        return array_eq


    @api.model
    def graficar_limnigrama_recorridos(self, values):
        try:
            result = {
                'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 100}],
                'series': [
                    {'name': 'Nivel', 'data': []},
                    {'name': 'Recorrido 1', 'data': []},
                    {'name': 'Recorrido 2', 'data': []},
                    {'name': 'Recorrido 3', 'data': []},
                    {'name': _('Lower travel'), 'data': []},
                    {'name': _('Cota (m)'), 'data': []},
                    {'name': _('Cota (m)'), 'data': []},
                    {'name': _('Cota (m)'), 'data': []},
                    {'name': _('Travel 1 Time (months)'), 'data': []},
                    {'name': _('Cota (m)'), 'data': []},
                    {'name': _('Cota (m)'), 'data': []},
                ]}
            tipo_objeto = values['elemento_graficar']
            fecha_inicio = values['desde']
            fecha_fin = values['hasta']
            pozo_obj = self.env['df.pozo']
            if len(values['pozo_bloque_ids']) != 0:
                pozo_ids = values['pozo_bloque_ids']
            elif len(values['pozo_sector_ids']) != 0:
                pozo_ids = values['pozo_sector_ids']
            elif len(values['pozo_cuenca_ids']) != 0:
                pozo_ids = values['pozo_cuenca_ids']
            else:
                pozo_ids = None
            if values.get('a0'):
                a0 = values['a0']
            else:
                a0 = 0
            if values.get('a1'):
                a1 = values['a1']
            else:
                a1 = 0

            inicio = datetime.datetime(int(fecha_inicio.split('-')[0]), int(fecha_inicio.split('-')[1]), 1)
            fin = datetime.datetime(int(fecha_fin.split('-')[0]), int(fecha_fin.split('-')[1]), 1)
            if tipo_objeto == 'pozo':
                objeto = values['pozo_id']
                sql = '''SELECT * FROM df_nivel_anual_pozo
            WHERE
            pozo_id = ''' + str(objeto) + ''' AND
            anno BETWEEN ''' + str(inicio.year) + ''' AND ''' + str(fin.year) + '''
            ORDER BY anno ASC'''
                self.env.cr.execute(sql)
                elementos = self.env.cr.dictfetchall()
                pozo = pozo_obj.browse(objeto)
                result['object'] = _(' del pozo: ') + pozo.sigla
                max_historico = pozo.maximo_h_periodo if pozo.maximo_h_periodo_fijo <= 0 else pozo.maximo_h_periodo_fijo
                min_historico = pozo.minimo_h_periodo if pozo.minimo_h_periodo_fijo <= 0 else pozo.minimo_h_periodo_fijo

            else:
                if tipo_objeto == 'bloque':
                    pool_obj = 'df.bloque'
                    objeto = values['bloque_id']
                elif tipo_objeto == 'sector':
                    pool_obj = 'df.sector.hidrologico'
                    objeto = values['sector_id']
                elif tipo_objeto == 'cuenca':
                    pool_obj = 'df.cuenca.subterranea'
                    objeto = values['cuenca_id']
                instancia = self.env[pool_obj].browse([objeto])[0]
                if values['metodo_formula']:
                    elementos = self.env[pool_obj].calcular_media_por_formula([objeto], pozo_ids, inicio, fin)

                    max_historico = instancia.maximo_h_periodo_formula if instancia.maximo_h_periodo_fijo <= 0 else instancia.maximo_h_periodo_fijo
                    min_historico = instancia.minimo_h_periodo_formula if instancia.minimo_h_periodo_fijo <= 0 else instancia.minimo_h_periodo_fijo

                else:
                    elementos = self.env[pool_obj].calcular_media_aritmetica([objeto], pozo_ids, inicio, fin)

                    max_historico = instancia.maximo_h_periodo if instancia.maximo_h_periodo_fijo <= 0 else instancia.maximo_h_periodo_fijo
                    min_historico = instancia.minimo_h_periodo if instancia.minimo_h_periodo_fijo <= 0 else instancia.minimo_h_periodo_fijo

            if elementos:
                iterador_meses = inicio.month
                if tipo_objeto != 'pozo':
                    elementos = elementos[0]

                if tipo_objeto == 'pozo':
                    diccionario_extremos_historicos = self.env['df.pozo'].max_min([int(objeto)], None, None)
                elif tipo_objeto == 'bloque':
                    diccionario_extremos_historicos = \
                        self.env['df.bloque'].max_min([int(objeto)], pozo_ids, None, None, 'aritmetica', None)[0]
                elif tipo_objeto == 'sector':
                    diccionario_extremos_historicos = \
                        self.env['df.sector.hidrologico'].max_min([int(objeto)], pozo_ids, None, None, 'aritmetica', None)[
                            0]
                elif tipo_objeto == 'cuenca':
                    diccionario_extremos_historicos = \
                        self.env['df.cuenca.subterranea'].max_min([int(objeto)], pozo_ids, None, None, 'aritmetica', None)[
                            0]

                result['valueAxis'][0]['max'] = diccionario_extremos_historicos['valor_max']
                result['valueAxis'][0]['min'] = diccionario_extremos_historicos['valor_min']
                tres_puntos_altos = []

                for elemento in elementos:
                    while iterador_meses <= 12 and (iterador_meses <= fin.month or elemento['anno'] < fin.year):

                        times = time.strptime(str((elemento['anno'])) + '-' + str(iterador_meses) + '-' + str(1),
                                              "%Y-%m-%d")
                        times_milisecond = time.mktime(times) * 1000

                        if tipo_objeto == 'pozo':
                            valor_string = str(
                                elemento['media_hiperanual_' + self._mes_numero_full(iterador_meses) + '_string'])
                        else:
                            if elemento.get(str(iterador_meses)):
                                valor_string = str(elemento[str(iterador_meses)])
                            else:
                                valor_string = None

                        if valor_string != '' and valor_string != False and valor_string != None:
                            valor = float("%.3f" % float(valor_string))
                            if valor < min_historico:
                                valor = min_historico
                            result['series'][0]['data'].append([times_milisecond, valor])
                        else:
                            result['series'][0]['data'].append([times_milisecond, None])
                        iterador_meses += 1
                    iterador_meses = 1

            niveles_ordenados = sorted(result['series'][0]['data'], key=lambda tup: (tup[1]))
            niveles_ordenados_1 = sorted(result['series'][0]['data'], key=lambda tup: (tup[1], +tup[0]))

            # punto mas bajo
            fin_recorrido_punto_mas_bajo = niveles_ordenados[len(niveles_ordenados) - 1]
            fin_recorridos_datetime = [
                datetime.datetime.fromtimestamp(float(fin_recorrido_punto_mas_bajo[0]) / 1000.0)
            ]
            if tipo_objeto == 'pozo':
                inicio_recorrido_punto_mas_bajo = self.env['df.pozo'].obtener_inicio_recorridos([int(objeto)],
                                                                                                fin_recorridos_datetime,
                                                                                                [])
            else:
                if values['metodo_formula']:
                    inicio_recorrido_punto_mas_bajo = self.env[pool_obj].obtener_fin_recorridos([int(objeto)],
                                                                                                pozo_ids,
                                                                                                fin_recorridos_datetime,
                                                                                                [], 'formula',
                                                                                                None)
                else:
                    inicio_recorrido_punto_mas_bajo = self.env[pool_obj].obtener_fin_recorridos([int(objeto)],
                                                                                                pozo_ids,
                                                                                                fin_recorridos_datetime,
                                                                                                [], 'aritmetica',
                                                                                                None)

            indice_niveles = 0
            while indice_niveles < len(result['series'][0]['data']):
                punto_nivel = result['series'][0]['data'][indice_niveles]
                try:
                    if punto_nivel[0] >= inicio_recorrido_punto_mas_bajo and punto_nivel[0] <= fin_recorrido_punto_mas_bajo[
                        0]:
                        result['series'][4]['data'].append(punto_nivel)
                    indice_niveles += 1
                except:
                    break




            # punto mas alto recorrido 1
            punto = niveles_ordenados[0]
            punto_referencia = None
            tiempo_milisegundos = punto[0]
            # inicio_recorrido_punto_mas_bajo = tiempo_milisegundos
            recorridos_ya_marcados = []

            while punto[1] < fin_recorrido_punto_mas_bajo[1] and tiempo_milisegundos != fin_recorrido_punto_mas_bajo[0]:
                if punto_referencia:
                    punto = punto_referencia
                punto_referencia = None

                # INICIO Y FIN DEL RECORRIDO DEL PUNTO
                inicio_recorridos_datetime = [
                    datetime.datetime.fromtimestamp(float(punto[0]) / 1000.0)
                ]
                if tipo_objeto == 'pozo':
                    fin_recorridos = self.env['df.pozo'].obtener_fin_recorridos([int(objeto)],
                                                                                inicio_recorridos_datetime, [])

                else:
                    if values['metodo_formula']:
                        fin_recorridos = self.env[pool_obj].obtener_fin_recorridos([int(objeto)],
                                                                                   pozo_ids,
                                                                                   inicio_recorridos_datetime, [],
                                                                                   'formula', None)
                    else:
                        fin_recorridos = self.env[pool_obj].obtener_fin_recorridos([int(objeto)],
                                                                                   pozo_ids,
                                                                                   inicio_recorridos_datetime, [],
                                                                                   'aritmetica', None)

                tiempo = time.strptime(
                    str((fin_recorridos[0]['anno'])) + '-' + str((fin_recorridos[0]['mes'])) + '-' + str(1), "%Y-%m-%d")
                tiempo_milisegundos = time.mktime(tiempo) * 1000

                if tiempo_milisegundos != fin_recorrido_punto_mas_bajo[0]:
                    recorridos_ya_marcados.append([punto[0], tiempo_milisegundos])
                # fin de INICIO Y FIN DEL RECORRIDO DEL PUNTO

                indice_niveles = 0
                serie_temp = []
                while indice_niveles < len(result['series'][0]['data']):
                    if result['series'][0]['data'][indice_niveles][0] >= punto[0] and \
                                    result['series'][0]['data'][indice_niveles][0] <= tiempo_milisegundos:
                        if (result['series'][0]['data'][indice_niveles - 1][1] <=
                                result['series'][0]['data'][indice_niveles][1]) or (
                                    result['series'][0]['data'][indice_niveles - 1][0] < punto[0]):
                            serie_temp.append(result['series'][0]['data'][indice_niveles])
                    indice_niveles += 1
                if len(serie_temp) > 1:
                    result['series'][1]['data'].extend(serie_temp)
                indice_niveles_ordenados = 0
                while indice_niveles_ordenados < len(niveles_ordenados) - 1:
                    if datetime.datetime.fromtimestamp(
                                    float(tiempo_milisegundos) / 1000.0) == datetime.datetime.fromtimestamp(
                                float(niveles_ordenados[indice_niveles_ordenados][0]) / 1000.0):
                        punto = niveles_ordenados[indice_niveles_ordenados + 1]
                        break
                    indice_niveles_ordenados += 1

            # limpiando puntos de diferencia minima
            indice_limpieza = 0
            if values.get('rango_limpieza') and values['rango_limpieza'] > 0:
                while indice_limpieza < len(result['series'][1]['data']) - 2:
                    if abs(result['series'][1]['data'][indice_limpieza][1] -
                                   result['series'][1]['data'][indice_limpieza + 1][1]) < values['rango_limpieza']:
                        result['series'][1]['data'].pop(indice_limpieza + 1)
                    else:
                        indice_limpieza += 1
            if result['series'][1]['data'][len(result['series'][1]['data']) - 1][0] != fin_recorrido_punto_mas_bajo[0]:
                result['series'][1]['data'].append(fin_recorrido_punto_mas_bajo)



            # punto mas alto recorrido 2
            punto = niveles_ordenados_1[0]
            punto_referencia = None
            tiempo_milisegundos = 1

            while punto[1] < fin_recorrido_punto_mas_bajo[1] and tiempo_milisegundos != fin_recorrido_punto_mas_bajo[0]:
                if punto_referencia:
                    punto = punto_referencia
                punto_referencia = None

                # INICIO Y FIN DEL RECORRIDO DEL PUNTO
                inicio_recorridos_datetime = [
                    datetime.datetime.fromtimestamp(float(punto[0]) / 1000.0)
                ]
                if tipo_objeto == 'pozo':
                    fin_recorridos = self.env['df.pozo'].obtener_fin_recorridos([int(objeto)],
                                                                                inicio_recorridos_datetime, [])

                else:
                    if values['metodo_formula']:
                        fin_recorridos = self.env[pool_obj].obtener_fin_recorridos([int(objeto)],
                                                                                   pozo_ids,
                                                                                   inicio_recorridos_datetime, [],
                                                                                   'formula', None)
                    else:
                        fin_recorridos = self.env[pool_obj].obtener_fin_recorridos([int(objeto)],
                                                                                   pozo_ids,
                                                                                   inicio_recorridos_datetime, [],
                                                                                   'aritmetica', None)

                tiempo = time.strptime(
                    str((fin_recorridos[0]['anno'])) + '-' + str((fin_recorridos[0]['mes'])) + '-' + str(1), "%Y-%m-%d")
                tiempo_milisegundos = time.mktime(tiempo) * 1000
                # fin de INICIO Y FIN DEL RECORRIDO DEL PUNTO

                indice_niveles = 0
                serie_temp = []

                marcado = False
                if len(result['series'][2]['data']) is not 0:
                    for recorridos_ya_marcado in recorridos_ya_marcados:
                        if recorridos_ya_marcado[0] == punto[0] and recorridos_ya_marcado[1] == tiempo_milisegundos:
                            marcado = True
                            break
                while indice_niveles < len(result['series'][0]['data']) and not marcado:
                    if result['series'][0]['data'][indice_niveles][0] >= punto[0] and \
                                    result['series'][0]['data'][indice_niveles][0] <= tiempo_milisegundos:
                        if (result['series'][0]['data'][indice_niveles - 1][1] <=
                                result['series'][0]['data'][indice_niveles][1]) or (
                                    result['series'][0]['data'][indice_niveles - 1][0] < punto[0]):
                            serie_temp.append(result['series'][0]['data'][indice_niveles])
                    indice_niveles += 1
                if len(serie_temp) > 1:
                    result['series'][2]['data'].extend(serie_temp)
                else:
                    A = 5
                indice_niveles_ordenados = 0
                if not marcado:
                    while indice_niveles_ordenados < len(niveles_ordenados_1) - 1:
                        if niveles_ordenados_1[indice_niveles_ordenados][0] == tiempo_milisegundos:
                            punto = niveles_ordenados_1[indice_niveles_ordenados + 1]
                            break
                        indice_niveles_ordenados += 1
                else:
                    while indice_niveles_ordenados < len(niveles_ordenados_1) - 1:
                        if punto[0] == niveles_ordenados_1[indice_niveles_ordenados][0]:
                            punto = niveles_ordenados_1[indice_niveles_ordenados + 1]
                            break
                        indice_niveles_ordenados += 1

            # limpiando puntos de diferencia minima
            indice_limpieza = 0
            while indice_limpieza < len(result['series'][2]['data']) - 2:
                # if abs(result['series'][2]['data'][indice_limpieza][1] - result['series'][2]['data'][indice_limpieza + 1][1]) < 0.3:
                if abs(result['series'][2]['data'][indice_limpieza][1] -
                               result['series'][2]['data'][indice_limpieza + 1][1]) < values['rango_limpieza']:
                    result['series'][2]['data'].pop(indice_limpieza + 1)
                else:
                    indice_limpieza += 1
            if result['series'][2]['data'][len(result['series'][2]['data']) - 1][0] != fin_recorrido_punto_mas_bajo[0]:
                result['series'][2]['data'].append(fin_recorrido_punto_mas_bajo)

            if result['series'][1]['data'][len(result['series'][1]['data']) - 1][0] != punto[0] and \
                            result['series'][1]['data'][len(result['series'][1]['data']) - 1][1] < punto[1]:
                result['series'][1]['data'].append(punto)
            if result['series'][2]['data'][len(result['series'][2]['data']) - 1][0] != punto[0] and \
                            result['series'][2]['data'][len(result['series'][2]['data']) - 1][1] < punto[1]:
                result['series'][2]['data'].append(punto)

            # --------------------NIVELES COTA PARA LA TABLA
            if tipo_objeto == 'pozo':
                # RECORRIDO 1
                sql = """
                    SELECT
                      df_report_cota_agua.pozo_id,
                      df_report_cota_agua.sigla,
                      df_report_cota_agua.anno,
                      df_report_cota_agua.cota_agua_enero,
                      df_report_cota_agua.cota_agua_febrero,
                      df_report_cota_agua.cota_agua_marzo,
                      df_report_cota_agua.cota_agua_abril,
                      df_report_cota_agua.cota_agua_mayo,
                      df_report_cota_agua.cota_agua_junio,
                      df_report_cota_agua.cota_agua_julio,
                      df_report_cota_agua.cota_agua_agosto,
                      df_report_cota_agua.cota_agua_septiembre,
                      df_report_cota_agua.cota_agua_octubre,
                      df_report_cota_agua.cota_agua_noviembre,
                      df_report_cota_agua.cota_agua_diciembre,
                      df_nivel_anual_pozo.media_hiperanual_enero_string AS nivel_enero,
                      df_nivel_anual_pozo.media_hiperanual_febrero_string AS nivel_febrero,
                      df_nivel_anual_pozo.media_hiperanual_marzo_string AS nivel_marzo,
                      df_nivel_anual_pozo.media_hiperanual_abril_string AS nivel_abril,
                      df_nivel_anual_pozo.media_hiperanual_mayo_string AS nivel_mayo,
                      df_nivel_anual_pozo.media_hiperanual_junio_string AS nivel_junio,
                      df_nivel_anual_pozo.media_hiperanual_julio_string AS nivel_julio,
                      df_nivel_anual_pozo.media_hiperanual_agosto_string AS nivel_agosto,
                      df_nivel_anual_pozo.media_hiperanual_septiembre_string AS nivel_septiembre,
                      df_nivel_anual_pozo.media_hiperanual_octubre_string AS nivel_octubre,
                      df_nivel_anual_pozo.media_hiperanual_noviembre_string AS nivel_noviembre,
                      df_nivel_anual_pozo.media_hiperanual_diciembre_string AS nivel_diciembre
                    FROM
                      public.df_report_cota_agua,
                      public.df_nivel_anual_pozo
                    WHERE
                      df_report_cota_agua.anno = df_nivel_anual_pozo.anno AND
                      df_nivel_anual_pozo.pozo_id = df_report_cota_agua.pozo_id AND
                      sigla = '""" + str(pozo.sigla) + """' AND
                      df_report_cota_agua.anno BETWEEN """ + str(inicio.year) + """ AND """ + str(fin.year) + """
                    ORDER BY
                      df_report_cota_agua.anno ASC;
                    """
                self.env.cr.execute(sql)
                cotas = self.env.cr.dictfetchall()
            else:
                cotas = self.env[pool_obj].obtener_cotas_tramos(cr, uid, [objeto], pozo_ids,
                                                                datetime.datetime.strptime(fecha_inicio,
                                                                                           "%Y-%m-%d"),
                                                                datetime.datetime.strptime(fecha_fin, "%Y-%m-%d"),
                                                                ("formula" if (
                                                                    values['metodo_formula']) else "aritmetica"),
                                                                None)

            contador = 1
            for punto in result['series'][1]['data']:
                fecha_punto = datetime.datetime.fromtimestamp(punto[0] / 1000.0)
                for cota in cotas:
                    if cota['anno'] == fecha_punto.year:
                        mes_numero = self._mes_numero_full(fecha_punto.month)
                        indice = 'cota_agua_' + mes_numero
                        if cota.get(indice) and cota[indice] != -999999.11:
                            result['series'][5]['data'].append([contador, punto[1], cota[indice]])
                            result['series'][9]['data'].append([contador, cota[indice]])
                            contador += 1
                        else:
                            break;
            contador = 1
            for punto in result['series'][2]['data']:
                fecha_punto = datetime.datetime.fromtimestamp(punto[0] / 1000.0)
                for cota in cotas:
                    if cota['anno'] == fecha_punto.year:
                        mes_numero = self._mes_numero_full(fecha_punto.month)
                        indice = 'cota_agua_' + mes_numero
                        if cota.get(indice) and cota[indice] != -999999.11:
                            result['series'][6]['data'].append([contador, punto[1], cota[indice]])
                            result['series'][10]['data'].append([contador, cota[indice]])
                            contador += 1
                        else:
                            break;
            cont = 0
            longitud = len(result['series'][5]['data'])
            for datos in result['series'][5]['data']:
                if datos[1] > max_historico:
                    break
                cont += 1
            del result['series'][5]['data'][cont:longitud]
            result['series'][5]['data'] = result['series'][5]['data']
            cont1 = 0
            longitud1 = len(result['series'][6]['data'])
            for datos1 in result['series'][6]['data']:
                if datos1[1] > max_historico:
                    break
                cont1 += 1
            del result['series'][6]['data'][cont1:longitud1]
            result['series'][6]['data'] = result['series'][6]['data']
            return result
        except:
            # raise osv.except_osv(_('Error: '), (
            #     "Ha sido encontrado un error y el proceso de elaboración de la gráfica ha sido detenido.\n"
            #     "Los motivos posibles pueden ser:\n"
            #     "Datos diarios vacíos o nulos\n"
            #     "Datos de comportamiento históricos vacíos o nulos\n"))
            raise UserError(
                _("Ha sido encontrado un error y el proceso de elaboración de la gráfica ha sido detenido.\n"
                  "Los motivos posibles pueden ser:\n"
                  "Datos diarios vacíos o nulos.\n"
                  "Datos de comportamiento históricos vacíos o nulos."))
