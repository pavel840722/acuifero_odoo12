# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError
import time, datetime
from dateutil.relativedelta import relativedelta
from odoo.addons.df_hc_base.models import df_hc_gis

class df_pozo(models.Model):
    _name = 'df.pozo'
    _description = "HC Well"
    _rec_name = 'sigla'

    def _country_id(self):
        pais_id = self.env['res.country'].search([('name', '=', 'Cuba')])
        return pais_id.id

    def _seguridad_provincial(self):
        provincia_ids = []
        user = self.env.user
        es_de_grupo_nacional = es_de_grupo_provincial = False
        if (user.name == 'Administrator'):
            es_de_grupo_nacional = True
        else:
            es_de_grupo_provincial = True

        provincia_obj = self.env['res.country.state']
        if es_de_grupo_nacional:
            return provincia_obj.search([]).ids
        elif es_de_grupo_provincial:
            provincia_usuario_id = user.company_id.state_id.id
            return provincia_obj.search([('id', '=', provincia_usuario_id)])

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self._context is None:
            context = {}
        else:
            context = dict(self._context).copy()
        if context.get('tipo_filtro'):
            if not context['filtro']:
                context['filtro'] = []
            elif type(context['filtro']) == type(2):
                context['filtro'] = [context['filtro']]

            args.append(('representativo','=',True))
            if context['tipo_filtro'] == 'bloque':
                args.append(('bloque_id','in',context['filtro']))
            elif context['tipo_filtro'] == 'sector':
                ### asi lo tenia rafa
                #args.append(('sector_hidrologico_id','in',context['filtro']))

                ### probando a ver
                args.append('|')
                args.append(('sector_hidrologico_id', 'in', context['filtro']))
                args.append(('bloque_id.sector_id', 'in', context['filtro']))

            elif context['tipo_filtro'] == 'cuenca':
                #args=[('representativo','=',True),'|',('cuenca_subterranea_id', 'in', context['filtro']),('sector_hidrologico_id.cuenca_subterranea_id', 'in', context['filtro'])]

                ### asi lo tenia rafa
                #args.append(('representativo','=',True))
                #args.append('|')
                #args.append(('cuenca_subterranea_id', 'in', context['filtro']))
                #args.append(('sector_hidrologico_id.cuenca_subterranea_id', 'in', context['filtro']))

                ### probando a ver
                obj_bloque = self.env['df.bloque']
                bloque_ids = obj_bloque.search([('sector_id.cuenca_subterranea_id', 'in', context['filtro'])]).ids
                obj_sector = self.env['df.sector.hidrologico']
                sector_ids = obj_sector.search([('cuenca_subterranea_id', 'in', context['filtro'])]).ids
                pozo_ids = super(df_pozo, self).search(['|', ('bloque_id', 'in', bloque_ids), ('sector_hidrologico_id', 'in', sector_ids)]).ids
                # args = ['|', ('cuenca_subterranea_id', 'in', context['filtro'][0][2]), ('id', 'in', pozo_ids)]
                args.append('|')
                args.append(('cuenca_subterranea_id', 'in', context['filtro']))
                args.append(('id', 'in', pozo_ids))

        if context.get('exportar_filtro'):
            if context['exportar_filtro'] == 'bloque':
                args.append(('bloque_id','in',context['filtro'][0][2]))
            elif context['exportar_filtro'] == 'sector':
                #args = ['|', ('sector_hidrologico_id', 'in', context['filtro'][0][2]), ('bloque_id.sector_id', 'in', context['filtro'][0][2])]
                args.append('|')
                args.append(('sector_hidrologico_id', 'in', context['filtro'][0][2]))
                args.append(('bloque_id.sector_id', 'in', context['filtro'][0][2]))
            elif context['exportar_filtro'] == 'cuenca':
                obj_bloque = self.env['df.bloque']
                bloque_ids = obj_bloque.search([('sector_id.cuenca_subterranea_id', 'in', context['filtro'][0][2])]).ids
                obj_sector = self.env['df.sector.hidrologico']
                sector_ids = obj_sector.search([('cuenca_subterranea_id', 'in', context['filtro'][0][2])]).ids
                pozo_ids = super(df_pozo, self).search(['|', ('bloque_id', 'in', bloque_ids), ('sector_hidrologico_id', 'in', sector_ids)]).ids
                #args = ['|', ('cuenca_subterranea_id', 'in', context['filtro'][0][2]), ('id', 'in', pozo_ids)]
                args.append('|')
                args.append(('cuenca_subterranea_id', 'in', context['filtro'][0][2]))
                args.append(('id', 'in', pozo_ids))

        return super(df_pozo, self).search(args, offset, limit, order, count=count)


    def obtener_niveles_totales(self, pozo):   #trabaje aqui GJBL
       tabla_agrupamiento = 'df_nivel_anual_pozo'

       sql = """ select (media_hiperanual_enero)as enero,
                        (media_hiperanual_febrero)as febrero,
                        (media_hiperanual_marzo)as marzo,
                        (media_hiperanual_abril)as abril,
                        (media_hiperanual_mayo)as mayo,
                        (media_hiperanual_junio)as junio,
                        (media_hiperanual_julio)as julio,
                        (media_hiperanual_agosto)as agosto,
                        (media_hiperanual_septiembre)as septiembre,
                        (media_hiperanual_octubre)as octubre,
                        (media_hiperanual_noviembre)as noviembre,
                        (media_hiperanual_diciembre)as diciembre,anno
                   from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                   where tabla_objeto.pozo_id = '""" + str(pozo) + """'
                   ORDER BY anno ASC;"""
       self.env.cr.execute(sql)
       datos_vistas = self.env.cr.fetchall()
       return datos_vistas

    def obtener_niveles_totales_dec(self, pozo):    #trabaje aqui GJBL
       tabla_agrupamiento = 'df_nivel_anual_pozo'

       sql = """ select (media_hiperanual_enero)as enero,
                        (media_hiperanual_febrero)as febrero,
                        (media_hiperanual_marzo)as marzo,
                        (media_hiperanual_abril)as abril,
                        (media_hiperanual_mayo)as mayo,
                        (media_hiperanual_junio)as junio,
                        (media_hiperanual_julio)as julio,
                        (media_hiperanual_agosto)as agosto,
                        (media_hiperanual_septiembre)as septiembre,
                        (media_hiperanual_octubre)as octubre,
                        (media_hiperanual_noviembre)as noviembre,
                        (media_hiperanual_diciembre)as diciembre
                   from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                   where tabla_objeto.pozo_id = '""" + str(pozo) + """'
                   ORDER BY anno DESC;"""
       self.env.cr.execute(sql)
       datos_vistas = self.env.cr.fetchall()
       return datos_vistas

    @api.model
    def obtener_niveles_acotados(self, pozo, anno_inicio, anno_fin):  #trabaje aqui GJBL
        tabla_agrupamiento = 'df_nivel_anual_pozo'

        sql = """ select anno,(media_hiperanual_enero)as enero,
                         (media_hiperanual_febrero)as febrero,
                         (media_hiperanual_marzo)as marzo,
                         (media_hiperanual_abril)as abril,
                         (media_hiperanual_mayo)as mayo,
                         (media_hiperanual_junio)as junio,
                         (media_hiperanual_julio)as julio,
                         (media_hiperanual_agosto)as agosto,
                         (media_hiperanual_septiembre)as septiembre,
                         (media_hiperanual_octubre)as octubre,
                         (media_hiperanual_noviembre)as noviembre,
                         (media_hiperanual_diciembre)as diciembre
                    from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                    where anno BETWEEN '""" + str(anno_inicio) + """' AND '""" + str(anno_fin) + """' AND
                    tabla_objeto.pozo_id = '""" + str(pozo) + """'
                    ORDER BY anno ASC;"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.fetchall()
        return datos_vistas


    def obtener_niveles_acotados_dic(self, pozo, anno_inicio, anno_fin):  #trabaje aqui GJBL
        tabla_agrupamiento = 'df_nivel_anual_pozo'

        sql = """ select anno,NULLIF(media_hiperanual_enero, -999999.110) as enero,
                         NULLIF(media_hiperanual_febrero, -999999.110) as febrero,
                         NULLIF(media_hiperanual_marzo, -999999.110) as marzo,
                         NULLIF(media_hiperanual_abril, -999999.110) as abril,
                         NULLIF(media_hiperanual_mayo, -999999.110) as mayo,
                         NULLIF(media_hiperanual_junio, -999999.110) as junio,
                         NULLIF(media_hiperanual_julio, -999999.110) as julio,
                         NULLIF(media_hiperanual_agosto, -999999.110) as agosto,
                         NULLIF(media_hiperanual_septiembre, -999999.110) as septiembre,
                         NULLIF(media_hiperanual_octubre, -999999.110) as octubre,
                         NULLIF(media_hiperanual_noviembre, -999999.110) as noviembre,
                         NULLIF(media_hiperanual_diciembre, -999999.110) as diciembre
                    from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                    where anno BETWEEN '""" + str(anno_inicio) + """' AND '""" + str(anno_fin) + """' AND
                    tabla_objeto.pozo_id = '""" + str(pozo) + """'
                    ORDER BY anno ASC;"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.dictfetchall()
        return datos_vistas


    def obtener_niveles_acotados_asc(self, pozo, anno_inicio, anno_fin):   #trabaje aqui GJBL
        tabla_agrupamiento = 'df_nivel_anual_pozo'

        sql = """ select anno,(media_hiperanual_enero)as enero,
                         (media_hiperanual_febrero)as febrero,
                         (media_hiperanual_marzo)as marzo,
                         (media_hiperanual_abril)as abril,
                         (media_hiperanual_mayo)as mayo,
                         (media_hiperanual_junio)as junio,
                         (media_hiperanual_julio)as julio,
                         (media_hiperanual_agosto)as agosto,
                         (media_hiperanual_septiembre)as septiembre,
                         (media_hiperanual_octubre)as octubre,
                         (media_hiperanual_noviembre)as noviembre,
                         (media_hiperanual_diciembre)as diciembre
                    from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                    where anno BETWEEN '""" + str(anno_inicio) + """' AND '""" + str(anno_fin) + """' AND
                    tabla_objeto.pozo_id = '""" + str(pozo) + """'
                    ORDER BY anno DESC;"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.fetchall()
        return datos_vistas


    def existe_pozo(self, pozo):   #trabaje aqui GJBL
        tabla_agrupamiento = 'df_nivel_anual_pozo'
        sql = """ select *
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                           where tabla_objeto.pozo_id = '""" + str(pozo) + """';"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.dictfetchall()
        return datos_vistas


    def max_min(self, ids, fecha_inicio, fecha_fin):  #trabaje aqui GJBL
        res = {'id': '', 'nombre': '', 'valor_min': 999999.11, 'valor_max': 999999.11}
        ok = 0
        # fecha_inicio='2005-07-01'
        # fecha_fin='2007-11-01'
        for pozo in self.browse(ids):
            datos_generales = []
            # fecha_inicio=None
            # fecha_fin=None
            existe = self.existe_pozo(pozo.id)
            if fecha_inicio == None or fecha_fin == None:
                datos_vistas = self.obtener_niveles_totales(pozo.id)
                if existe:
                    contador = 0
                    mes = 0
                    for datos_vista in datos_vistas:
                        for valor in datos_vista:
                            dict_general = {}
                            mes += 1
                            if valor != -999999.110 and contador <= 11:
                                dict_general['valor'] = valor
                                dict_general['anno'] = datos_vista[12]
                                dict_general['mes'] = mes
                                datos_generales.append(dict_general)
                            contador += 1
                        contador = 0
                        mes = 0
                        # var=0
                    # x=var
                    if datos_generales:
                        min = datos_generales[0]['valor']
                        max = 0.0
                        anno_minimo = datos_generales[0]['anno']
                        mes_minimo = datos_generales[0]['mes']
                        anno_maximo = datos_generales[0]['anno']
                        mes_maximo = datos_generales[0]['mes']
                        for minimo in datos_generales:
                            if minimo['valor'] < min:
                                min = minimo['valor']
                                anno_minimo = minimo['anno']
                                mes_minimo = minimo['mes']
                        for maximo in datos_generales:
                            if maximo['valor'] > max:
                                max = maximo['valor']
                                anno_maximo = maximo['anno']
                                mes_maximo = maximo['mes']
                                # res = {'id':pozo.id,'nombre':pozo.nombre,'valor_min':min,'valor_max':max}
                        res = {'id': pozo.id, 'nombre': pozo.nombre, 'valor_min': min, 'valor_max': max,
                               'Amin': anno_minimo, 'Mmin': mes_minimo, 'Amax': anno_maximo, 'Mmax': mes_maximo}
                        # res[pozo.id] ="Nombre:"+str(pozo.nombre)+": "+ "Vmin:"+str(min) +": "+"Vmax:"+str(max)+": "+"ID:"+str(pozo.id)+": "+"Amin:"+str(anno_minimo)+": "+"Mmin:"+str(mes_minimo)+": "+"Amax:"+str(anno_maximo)+": "+"Mmax:"+str(mes_maximo)
                    else:
                        res[pozo.id] = ' '
                else:
                    res[pozo.id] = ' '
            else:
                # fecha_inicio = datetime.datetime.strptime(fecha_inicio,"%Y-%m-%d")
                # fecha_fin = datetime.datetime.strptime(fecha_fin,"%Y-%m-%d")
                # temp_date_inicio.year
                # temp_date_inicio.month
                # temp_date_inicio.day
                # temp_date_fin.year
                # temp_date_fin.month
                # temp_date_fin.day
                datos_vistas = self.obtener_niveles_acotados(pozo.id, fecha_inicio.year, fecha_fin.year)
                if existe and datos_vistas:
                    mes_inicial = 1
                    mes_final = 12
                    intermedios = len(datos_vistas) - 2
                    if len(datos_vistas) == 1:
                        contador = 1
                        mes_valor = 0
                        contador = 1
                        temp = 0
                        for mes in datos_vistas[0]:
                            dict_general = {}
                            if temp >= 1:
                                mes_valor += 1
                            temp += 1
                            if contador >= (fecha_inicio.month + 1) and contador > 1 and contador <= (
                                fecha_fin.month + 1):
                                if mes != -999999.110:
                                    dict_general['valor'] = mes
                                    dict_general['anno'] = datos_vistas[0][0]
                                    dict_general['mes'] = mes_valor
                                    datos_generales.append(dict_general)
                                    # datos_generales.append(mes)
                            contador += 1
                            #    coger de datos_vistas[0] solamente el rango de meses seleccionado
                    if len(datos_vistas) >= 2:
                        mes_valor = 0
                        contador = 1
                        temp = 0
                        for mes in datos_vistas[0]:
                            dict_general = {}
                            if temp >= 1:
                                mes_valor += 1
                            temp += 1
                            if contador >= (fecha_inicio.month + 1) and contador > 1:
                                if mes != -999999.110:
                                    dict_general['valor'] = mes
                                    dict_general['anno'] = datos_vistas[0][0]
                                    dict_general['mes'] = mes_valor
                                    datos_generales.append(dict_general)
                                    # datos_generales.append(mes)
                            contador += 1
                        contador = 1
                        mes_valor = 0
                        temp = 0
                        for mes in datos_vistas[len(datos_vistas) - 1]:
                            dict_general = {}
                            if temp >= 1:
                                mes_valor += 1
                            temp += 1
                            if contador <= (fecha_fin.month + 1) and contador > 1:
                                if mes != -999999.110:
                                    dict_general['valor'] = mes
                                    dict_general['anno'] = datos_vistas[len(datos_vistas) - 1][0]
                                    dict_general['mes'] = mes_valor
                                    datos_generales.append(dict_general)
                                    # datos_generales.append(mes)
                            elif contador > (fecha_inicio.month + 1):
                                break
                            contador += 1
                    if len(datos_vistas) > 2:#annadir meses intermedios en caso de existir
                        del datos_vistas[0]
                        del datos_vistas[len(datos_vistas) - 1]
                        # de datos_vistas elimino el primer y el ultimo fila
                        while ok < intermedios:
                            cont = 0
                            mes_valor = 0
                            temp = 0
                            for mes in datos_vistas[0]:
                                dict_general = {}
                                if temp >= 1:
                                    mes_valor += 1
                                temp += 1
                                if cont >= 1:
                                    if mes != -999999.110:
                                        dict_general['valor'] = mes
                                        dict_general['anno'] = datos_vistas[0][0]
                                        dict_general['mes'] = mes_valor
                                        datos_generales.append(dict_general)
                                        # datos_generales.append(mes)
                                cont += 1
                            ok = ok + 1
                            del datos_vistas[0]
                    if datos_generales:
                        min = datos_generales[0]['valor']
                        max = 0.0
                        anno_minimo = datos_generales[0]['anno']
                        mes_minimo = datos_generales[0]['mes']
                        anno_maximo = datos_generales[0]['anno']
                        mes_maximo = datos_generales[0]['mes']
                        for minimo in datos_generales:
                            if minimo['valor'] < min:
                                min = minimo['valor']
                                mes_minimo = minimo['mes']
                                anno_minimo = minimo['anno']
                        for maximo in datos_generales:
                            if maximo['valor'] > max:
                                max = maximo['valor']
                                anno_maximo = maximo['anno']
                                mes_maximo = maximo['mes']
                        res = {'id': pozo.id, 'nombre': pozo.nombre, 'valor_min': min, 'valor_max': max,
                               'Amin': anno_minimo, 'Mmin': mes_minimo, 'Amax': anno_maximo, 'Mmax': mes_maximo}
                        # res[pozo.id] ="Nombre:"+str(pozo.nombre)+": "+ "Vmin:"+str(min) +": "+"Vmax:"+str(max)+": "+"ID:"+str(pozo.id)+": "+"Amin:"+str(anno_minimo)+": "+"Mmin:"+str(mes_minimo)+": "+"Amax:"+str(anno_maximo)+": "+"Mmax:"+str(mes_maximo)
                    else:
                        res[pozo.id] = ' '
                else:
                    res[pozo.id] = ' '
        return res


    def obtener_nivele_actual(self, pozo):   #trabaje aqui GJBL
        tabla_agrupamiento = 'df_nivel_anual_pozo'

        sql = """ select anno,(media_hiperanual_enero)as enero,
                         (media_hiperanual_febrero)as febrero,
                         (media_hiperanual_marzo)as marzo,
                         (media_hiperanual_abril)as abril,
                         (media_hiperanual_mayo)as mayo,
                         (media_hiperanual_junio)as junio,
                         (media_hiperanual_julio)as julio,
                         (media_hiperanual_agosto)as agosto,
                         (media_hiperanual_septiembre)as septiembre,
                         (media_hiperanual_octubre)as octubre,
                         (media_hiperanual_noviembre)as noviembre,
                         (media_hiperanual_diciembre)as diciembre
                    from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                    where tabla_objeto.pozo_id = '""" + str(pozo) + """'
                    ORDER BY anno DESC;"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.fetchall()
        return datos_vistas


    def obtener_nivele_actual_asc(self, pozo):  #trabaje aqui GJBL
        tabla_agrupamiento = 'df_nivel_anual_pozo'

        sql = """ select anno,(media_hiperanual_enero)as enero,
                         (media_hiperanual_febrero)as febrero,
                         (media_hiperanual_marzo)as marzo,
                         (media_hiperanual_abril)as abril,
                         (media_hiperanual_mayo)as mayo,
                         (media_hiperanual_junio)as junio,
                         (media_hiperanual_julio)as julio,
                         (media_hiperanual_agosto)as agosto,
                         (media_hiperanual_septiembre)as septiembre,
                         (media_hiperanual_octubre)as octubre,
                         (media_hiperanual_noviembre)as noviembre,
                         (media_hiperanual_diciembre)as diciembre
                    from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                    where tabla_objeto.pozo_id = '""" + str(pozo) + """'
                    ORDER BY anno ASC;"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.fetchall()
        return datos_vistas


    def nivel_estatico(self, ids):   #trabaje aqui GJBL
        res = {}
        encontro = 0
        for pozo in self.browse(ids):
            existe = self.existe_pozo(pozo.id)
            if existe:
                datos_vistas = self.obtener_nivele_actual(pozo.id)
                for datos_vista in datos_vistas:
                    if encontro == 1:
                        break
                    else:
                        cont = len(datos_vista) - 1
                        ok = 0
                    while ok < len(datos_vista) - 1:
                        actual = datos_vista[cont]
                        cont = cont - 1
                        ok = ok + 1
                        if actual != -999999.110:
                            encontro = 1
                            break
                if actual != -999999.110:
                    cota_agua = pozo.cota_topografica - actual
                    res[pozo.id] = round(cota_agua, 4)
                else:
                    res[pozo.id] = ' '
                encontro = 0
            else:
                res[pozo.id] = ' '
        return res


    def auxiliar(self, id, fecha_inicio, fecha_fin):   #trabaje aqui GJBL
        # fecha_inicio='2001-07-01'
        # fecha_fin='2002-05-01'
        ok = 0
        #fecha_inicio = datetime.datetime.strptime(fecha_inicio,"%Y-%m-%d")
        #fecha_fin = datetime.datetime.strptime(fecha_fin,"%Y-%m-%d")
        datos_generales = []
        datos_vistas = self.obtener_niveles_acotados(id, fecha_inicio.year, fecha_fin.year)
        existe = self.existe_pozo(id)
        if existe and datos_vistas:
            mes_inicial = 1
            mes_final = 12
            intermedios = len(datos_vistas) - 2
            if len(datos_vistas) == 1:
                contador = 1
                mes_valor = 0
                contador = 1
                temp = 0
                for mes in datos_vistas[0]:
                    dict_general = {}
                    if temp >= 1:
                        mes_valor += 1
                    temp += 1
                    if contador >= (fecha_inicio.month + 1) and contador > 1 and contador <= (fecha_fin.month + 1):
                        if mes != -999999.110:
                            dict_general['valor'] = mes
                            dict_general['anno'] = datos_vistas[0][0]
                            dict_general['mes'] = mes_valor
                            datos_generales.append(dict_general)
                            # datos_generales.append(mes)
                    contador += 1
                    #    coger de datos_vistas[0] solamente el rango de meses seleccionado
            if len(datos_vistas) >= 2:
                mes_valor = 0
                contador = 1
                temp = 0
                for mes in datos_vistas[0]:
                    dict_general = {}
                    if temp >= 1:
                        mes_valor += 1
                    temp += 1
                    if contador >= (fecha_inicio.month + 1) and contador > 1:
                        if mes != -999999.110:
                            dict_general['valor'] = mes
                            dict_general['anno'] = datos_vistas[0][0]
                            dict_general['mes'] = mes_valor
                            datos_generales.append(dict_general)
                            # datos_generales.append(mes)
                    contador += 1
                contador = 1
                mes_valor = 0
                temp = 0
                for mes in datos_vistas[len(datos_vistas) - 1]:
                    dict_general = {}
                    if temp >= 1:
                        mes_valor += 1
                    temp += 1
                    if contador <= (fecha_fin.month + 1) and contador > 1:
                        if mes != -999999.110:
                            dict_general['valor'] = mes
                            dict_general['anno'] = datos_vistas[len(datos_vistas) - 1][0]
                            dict_general['mes'] = mes_valor
                            datos_generales.append(dict_general)
                            # datos_generales.append(mes)
                    elif contador > (fecha_inicio.month + 1):
                        break
                    contador += 1
            if len(datos_vistas) > 2:#annadir meses intermedios en caso de existir
                del datos_vistas[0]
                del datos_vistas[len(datos_vistas) - 1]
                # de datos_vistas elimino el primer y el ultimo fila
                while ok < intermedios:
                    cont = 0
                    mes_valor = 0
                    temp = 0
                    for mes in datos_vistas[0]:
                        dict_general = {}
                        if temp >= 1:
                            mes_valor += 1
                        temp += 1
                        if cont >= 1:
                            if mes != -999999.110:
                                dict_general['valor'] = mes
                                dict_general['anno'] = datos_vistas[0][0]
                                dict_general['mes'] = mes_valor
                                datos_generales.append(dict_general)
                                # datos_generales.append(mes)
                        cont += 1
                    ok = ok + 1
                    del datos_vistas[0]
        return datos_generales


    def altura(self, ids, fecha_inicio, fecha_fin):   #trabaje aqui GJBL
        datos_generales = []
        global existe
        # fecha_inicio=None
        # fecha_fin=None
        # fecha_inicio='2001-01-01'
        # fecha_fin='2002-12-31'
        for id in ids:
            if fecha_inicio == None or fecha_fin == None:
                datos_vistas = self.obtener_niveles_totales(id)
                for datos_vista in datos_vistas:
                    dict_max = self.max_min([id], None, None)
                    max_fijo = self.browse(id).maximo_h_periodo_fijo
                    max = dict_max['valor_max']
                    dict_altura = {}
                    if datos_vista[0] != -999999.110 and max_fijo < 0.0:
                        dict_altura['1'] = max - datos_vista[0]
                    elif datos_vista[0] != -999999.110:
                        dict_altura['1'] = max_fijo - datos_vista[0]
                    if datos_vista[1] != -999999.110 and max_fijo < 0.0:
                        dict_altura['2'] = max - datos_vista[1]
                    elif datos_vista[1] != -999999.110:
                        dict_altura['2'] = max_fijo - datos_vista[1]
                    if datos_vista[2] != -999999.110 and max_fijo < 0.0:
                        dict_altura['3'] = max - datos_vista[2]
                    elif datos_vista[2] != -999999.110:
                        dict_altura['3'] = max_fijo - datos_vista[2]
                    if datos_vista[3] != -999999.110 and max_fijo < 0.0:
                        dict_altura['4'] = max - datos_vista[3]
                    elif datos_vista[3] != -999999.110:
                        dict_altura['4'] = max_fijo - datos_vista[3]
                    if datos_vista[4] != -999999.110 and max_fijo < 0.0:
                        dict_altura['5'] = max - datos_vista[4]
                    elif datos_vista[4] != -999999.110:
                        dict_altura['5'] = max_fijo - datos_vista[4]
                    if datos_vista[5] != -999999.110 and max_fijo < 0.0:
                        dict_altura['6'] = max - datos_vista[5]
                    elif datos_vista[5] != -999999.110:
                        dict_altura['6'] = max_fijo - datos_vista[5]
                    if datos_vista[6] != -999999.110 and max_fijo < 0.0:
                        dict_altura['7'] = max - datos_vista[6]
                    elif datos_vista[6] != -999999.110:
                        dict_altura['7'] = max_fijo - datos_vista[6]
                    if datos_vista[7] != -999999.110 and max_fijo < 0.0:
                        dict_altura['8'] = max - datos_vista[7]
                    elif datos_vista[7] != -999999.110:
                        dict_altura['8'] = max_fijo - datos_vista[7]
                    if datos_vista[8] != -999999.110 and max_fijo < 0.0:
                        dict_altura['9'] = max - datos_vista[8]
                    elif datos_vista[8] != -999999.110:
                        dict_altura['9'] = max_fijo - datos_vista[8]
                    if datos_vista[9] != -999999.110 and max_fijo < 0.0:
                        dict_altura['10'] = max - datos_vista[9]
                    elif datos_vista[9] != -999999.110:
                        dict_altura['10'] = max_fijo - datos_vista[9]
                    if datos_vista[10] != -999999.110 and max_fijo < 0.0:
                        dict_altura['11'] = max - datos_vista[10]
                    elif datos_vista[10] != -999999.110:
                        dict_altura['11'] = max_fijo - datos_vista[10]
                    if datos_vista[11] != -999999.110 and max_fijo < 0.0:
                        dict_altura['12'] = max - datos_vista[11]
                    elif datos_vista[11] != -999999.110:
                        dict_altura['12'] = max_fijo - datos_vista[11]
                    if datos_vista[12] != -999999.110:
                        dict_altura['anno'] = datos_vista[12]
                    dict_altura['id'] = id
                    datos_generales.append(dict_altura)
            else:
                datos_vistas = self.auxiliar(id, fecha_inicio, fecha_fin)
                if datos_vistas:
                    anno = datos_vistas[0]['anno']
                    cont = 0
                    dict_max = self.max_min([id], fecha_inicio, fecha_fin)
                    max = dict_max['valor_max']
                    max_fijo = self.browse(id).maximo_h_periodo_fijo
                    temp = 0
                    dict_altura = {}
                    existe = 0
                    for datos_vista in datos_vistas:
                        cont += 1
                        if anno != datos_vistas[temp]['anno']:
                            existe = 1
                            anno = datos_vistas[temp]['anno']
                            datos_generales.append(dict_altura)
                            if existe == 1:
                                dict_altura = {}
                        if datos_vista['mes'] == 1:
                            if max_fijo <= 0.0:
                                dict_altura['1'] = max - datos_vista['valor']
                            else:
                                dict_altura['1'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 2:
                            if max_fijo <= 0.0:
                                dict_altura['2'] = max - datos_vista['valor']
                            else:
                                dict_altura['2'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 3:
                            if max_fijo <= 0.0:
                                dict_altura['3'] = max - datos_vista['valor']
                            else:
                                dict_altura['3'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 4:
                            if max_fijo <= 0.0:
                                dict_altura['4'] = max - datos_vista['valor']
                            else:
                                dict_altura['4'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 5:
                            if max_fijo <= 0.0:
                                dict_altura['5'] = max - datos_vista['valor']
                            else:
                                dict_altura['5'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 6:
                            if max_fijo <= 0.0:
                                dict_altura['6'] = max - datos_vista['valor']
                            else:
                                dict_altura['6'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 7:
                            if max_fijo <= 0.0:
                                dict_altura['7'] = max - datos_vista['valor']
                            else:
                                dict_altura['7'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 8:
                            if max_fijo <= 0.0:
                                dict_altura['8'] = max - datos_vista['valor']
                            else:
                                dict_altura['8'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 9:
                            if max_fijo <= 0.0:
                                dict_altura['9'] = max - datos_vista['valor']
                            else:
                                dict_altura['9'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 10:
                            if max_fijo <= 0.0:
                                dict_altura['10'] = max - datos_vista['valor']
                            else:
                                dict_altura['10'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 11:
                            if max_fijo <= 0.0:
                                dict_altura['11'] = max - datos_vista['valor']
                            else:
                                dict_altura['11'] = max_fijo - datos_vista['valor']
                        if datos_vista['mes'] == 12:
                            if max_fijo <= 0.0:
                                dict_altura['12'] = max - datos_vista['valor']
                            else:
                                dict_altura['12'] = max_fijo - datos_vista['valor']
                        dict_altura['anno'] = datos_vista['anno']
                        dict_altura['id'] = id
                        temp += 1
                        if cont == len(datos_vistas):
                            datos_generales.append(dict_altura)
                    existe = 0
        return datos_generales


    def volumen(self, ids, fecha_inicio, fecha_fin):  #trabaje aqui GJBL
        global existe
        # fecha_inicio=None
        # fecha_fin=None
        # fecha_inicio='2001-01-01'
        # fecha_fin='2005-12-31'
        datos_generales = []
        for id in ids:
            coeficiente_no_calculado = self.browse(id).coeficiente_almacenamiento
            cof_aprov = self.browse(id).coeficiente_aprovechamiento_hidraulico
            rec_explotable = self.browse(id).recurso_explotable
            area = self.browse(id).area
            deltaH = 2 * (self.browse(id).promedio_h_periodo)
            max_fijo = self.browse(id).maximo_h_periodo_fijo
            coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000)
            if coeficiente_no_calculado > 0.0:
                coeficiente = round(coeficiente_no_calculado, 3)
            else:
                coeficiente = round(coeficiente_calculado, 3)
            if fecha_inicio == None or fecha_fin == None:
                datos_vistas = self.obtener_niveles_totales(id)
                for datos_vista in datos_vistas:
                    dict_max = self.max_min([id], None, None)
                    max = dict_max['valor_max']
                    dict_volumen = {}
                    if datos_vista[0] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['1'] = ((coeficiente * (max - datos_vista[0]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['1'] = ((coeficiente * (max_fijo - datos_vista[0]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[1] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['2'] = ((coeficiente * (max - datos_vista[1]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['2'] = ((coeficiente * (max_fijo - datos_vista[1]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[2] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['3'] = ((coeficiente * (max - datos_vista[2]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['3'] = ((coeficiente * (max_fijo - datos_vista[2]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[3] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['4'] = ((coeficiente * (max - datos_vista[3]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['4'] = ((coeficiente * (max_fijo - datos_vista[3]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[4] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['5'] = ((coeficiente * (max - datos_vista[4]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['5'] = ((coeficiente * (max_fijo - datos_vista[4]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[5] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['6'] = ((coeficiente * (max - datos_vista[5]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['6'] = ((coeficiente * (max_fijo - datos_vista[5]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[6] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['7'] = ((coeficiente * (max - datos_vista[6]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['7'] = ((coeficiente * (max_fijo - datos_vista[6]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[7] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['8'] = ((coeficiente * (max - datos_vista[7]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['8'] = ((coeficiente * (max_fijo - datos_vista[7]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[8] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['9'] = ((coeficiente * (max - datos_vista[8]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['9'] = ((coeficiente * (max_fijo - datos_vista[8]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[9] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['10'] = ((coeficiente * (max - datos_vista[9]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['10'] = (coeficiente * (max_fijo - datos_vista[9]) * (
                                area * 1000000)) / 1000000 * cof_aprov
                    if datos_vista[10] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['11'] = ((coeficiente * (max - datos_vista[10]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['11'] = ((coeficiente * (max_fijo - datos_vista[10]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[11] != -999999.110:
                        if max_fijo <= 0.0:
                            dict_volumen['12'] = ((coeficiente * (max - datos_vista[11]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                        else:
                            dict_volumen['12'] = ((coeficiente * (max_fijo - datos_vista[11]) * (
                                area * 1000000)) / 1000000) * cof_aprov
                    if datos_vista[12] != -999999.110:
                        dict_volumen['anno'] = (datos_vista[12])
                    dict_volumen['id'] = id
                    datos_generales.append(dict_volumen)
            else:
                datos_vistas = self.auxiliar(id, fecha_inicio, fecha_fin)
                if datos_vistas:
                    anno = datos_vistas[0]['anno']
                    cont = 0
                    dict_max = self.max_min([id], fecha_inicio, fecha_fin)
                    max = dict_max['valor_max']
                    temp = 0
                    dict_altura = {}
                    existe = 0
                    for datos_vista in datos_vistas:
                        cont += 1
                        if anno != datos_vistas[temp]['anno']:
                            existe = 1
                            anno = datos_vistas[temp]['anno']
                            datos_generales.append(dict_altura)
                            if existe == 1:
                                dict_altura = {}
                        if datos_vista['mes'] == 1:
                            if max_fijo <= 0.0:
                                dict_altura['1'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['1'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 2:
                            if max_fijo <= 0.0:
                                dict_altura['2'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['2'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 3:
                            if max_fijo <= 0.0:
                                dict_altura['3'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['3'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 4:
                            if max_fijo <= 0.0:
                                dict_altura['4'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['4'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 5:
                            if max_fijo <= 0.0:
                                dict_altura['5'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['5'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 6:
                            if max_fijo <= 0.0:
                                dict_altura['6'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['6'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 7:
                            if max_fijo <= 0.0:
                                dict_altura['7'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['7'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 8:
                            if max_fijo <= 0.0:
                                dict_altura['8'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['8'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 9:
                            if max_fijo <= 0.0:
                                dict_altura['9'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['9'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 10:
                            if max_fijo <= 0.0:
                                dict_altura['10'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['10'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 11:
                            if max_fijo <= 0.0:
                                dict_altura['11'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['11'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        if datos_vista['mes'] == 12:
                            if max_fijo <= 0.0:
                                dict_altura['12'] = ((coeficiente * (max - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                            else:
                                dict_altura['12'] = ((coeficiente * (max_fijo - datos_vista['valor']) * (
                                    area * 1000000)) / 1000000) * cof_aprov
                        dict_altura['anno'] = datos_vista['anno']
                        dict_altura['id'] = id
                        temp += 1
                        if cont == len(datos_vistas):
                            datos_generales.append(dict_altura)
                    existe = 0
        return datos_generales


    def obtener_coordenadas(self):    #trabaje aqui GJBL
       res = {}
       for pozo in self.browse(self.ids):
           base_codes = ""
           # coordenadas = conductora.coordenada_inicio_id
           if pozo.coordenadas == 'north':
               base_codes += "Coordenadas:" + str('Cuba norte') + "  " + "Norte:" + str(
                   pozo.norte) + "  " + "Este:" + str(pozo.este)
               res[pozo.id] = base_codes
           if pozo.coordenadas == 'south':
               base_codes += "Coordenadas:" + str('Cuba sur') + "  " + "Norte:" + str(
                   pozo.norte1) + "  " + "Este:" + str(pozo.este1)
               res[pozo.id] = base_codes
           if pozo.coordenadas == False:
               res[pozo.id] = ' '
       return res


    def buscar_anno(self, pozo):   #trabaje aqui GJBL
        tabla_agrupamiento = 'df_nivel_anual_pozo'
        sql = """ select anno
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                           where tabla_objeto.pozo_id = '""" + str(pozo) + """'
                           ORDER BY anno ASC;"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.dictfetchall()
        return datos_vistas


    def buscar_anno_desc(self, pozo):   #trabaje aqui GJBL
        tabla_agrupamiento = 'df_nivel_anual_pozo'
        sql = """ select anno
                          from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                           where tabla_objeto.pozo_id = '""" + str(pozo) + """'
                           ORDER BY anno DESC;"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.dictfetchall()
        return datos_vistas


    def obtener(self, valor_anterior, lista):  #trabaje aqui GJBL
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


    def buscar(self, recorrido_actual, list_recorridos, lista):   #trabaje aqui GJBL
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


    def buscar_valor_maximo(self, ultimos_4_valores):  #trabaje aqui GJBL
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


    def menor_proximo_valor(self, lista_sobrecarga):  #trabaje aqui GJBL
        if lista_sobrecarga[1]['valor'] < lista_sobrecarga[0]['valor']:
            return True
        else:
            return False


    def buscar_sobrecarga(self, lista_sobrecarga, diferencia_sobrecarga):  #trabaje aqui GJBL
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


    def obtener_fin_recorridos(self, ids, recorridos, exepcion):   #trabaje aqui GJBL
        # fecha_r1 ='2008-08-01'
        # fecha_r2='2005-06-01'
        # fecha_r3='2010-07-01'
        # fecha_r1f = datetime.datetime.strptime(fecha_r1,"%Y-%m-%d")
        # fecha_r2f = datetime.datetime.strptime(fecha_r2,"%Y-%m-%d")
        # fecha_r3f= datetime.datetime.strptime(fecha_r3,"%Y-%m-%d")
        # reco=[fecha_r1f,fecha_r2f,fecha_r3f]
        # buscar1= self.obtener_inicio_recorridos(cr,uid,ids,reco,context)
        # a=[None,None,None,None,None,None,None,None,None,None,None,None]
        # a[0]=9
        # a[1]=8
        # tuple(a)
        # ee=[]
        # ee.append(tuple(a))
        fecha_actual = datetime.datetime.now()
        lista_recorridos = []
        # diferencia_sobrecarga=0.5
        global encontro
        for pozo in self.browse(ids):
            cont_recorrido = 0
            diferencia_sobrecarga = pozo.valor_precision
            buscar = self.buscar_anno(pozo.id)
            if len(buscar) > 0:
                anno_inicio = buscar[0]['anno']
                anno_fin = fecha_actual.year
                # anno_inicio=1999
                while anno_inicio <= anno_fin:
                    temp = 0
                    mes_valor = 0
                    contador = 1
                    contador4 = 0
                    contador2 = 0
                    lista = []
                    lista_sobrecarga = []
                    valor_anterior = {}
                    orden_recorrido = 0
                    for recorrido in recorridos:
                        orden_recorrido += 1
                        encontro = 0
                        contador_meses = 0
                        if anno_inicio == recorrido.year:
                            datos_vistas = self.obtener_niveles_acotados(pozo.id, recorrido.year, anno_fin)
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
                                        coencide = self.buscar( recorrido_actual, list_recorridos, lista)
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
                                            dict_max = self.buscar_valor_maximo( ultimos_4_valores)
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
                                        existe = self.obtener( valor_anterior, lista)
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
                                            dict_max = self.buscar_valor_maximo( ultimos_4_valores)
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
                                        verdadero = self.menor_proximo_valor( lista_sobrecarga)
                                        sobrecarga = self.buscar_sobrecarga( lista_sobrecarga, diferencia_sobrecarga)
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
                                            dict_max = self.buscar_valor_maximo( ultimos_4_valores)
                                            lista.append(dict_max)
                                            existe = self.obtener( valor_anterior, lista)
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
                                                dict_max = self.buscar_valor_maximo( ultimos_4_valores)
                                                lista.append(dict_max)
                                                existe = self.obtener( valor_anterior, lista)
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
                                                dict_max = self.buscar_valor_maximo( ultimos_4_valores)
                                                lista.append(dict_max)
                                                existe = self.obtener( valor_anterior, lista)
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
                                                dict_max = self.buscar_valor_maximo( ultimos_4_valores)
                                                lista.append(dict_max)
                                                existe = self.obtener( valor_anterior, lista)
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


    def buscar_inicio(self,recorrido_actual, list_recorridos, lista):  #trabaje aqui GJBL
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


    def obtener_inicio(self, valor_anterior, lista):   #trabaje aqui GJBL
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


    def buscar_valor_minimo(self, ultimos_4_valores):  #trabaje aqui GJBL
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


    def menor_proximo_valor_inicio(self, lista_sobrecarga):  #trabaje aqui GJBL
        if lista_sobrecarga[1]['valor'] > lista_sobrecarga[0]['valor']:
            return True
        else:
            return False


    def buscar_sobrecarga_inicio(self, lista_sobrecarga, diferencia_sobrecarga):  #trabaje aqui GJBL
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


    def obtener_inicio_recorridos(self, ids, recorridos, exepcion):  #trabaje aqui GJBL
       fecha_actual = datetime.datetime.now()
       lista_recorridos = []
       # diferencia_sobrecarga=0.5
       global encontro
       for pozo in self.browse(ids):
           cont_recorrido = 0
           diferencia_sobrecarga = pozo.valor_precision
           buscar = self.buscar_anno(pozo.id)
           if len(buscar) > 0:
               anno_inicio = buscar[0]['anno']
               anno_fin = fecha_actual.year
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
                           datos_vistas = self.obtener_niveles_acotados_asc( pozo.id, anno_inicio, recorrido.year)
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
                                       coencide = self.buscar_inicio( recorrido_actual, list_recorridos, lista)
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
                                           dict_min = self.buscar_valor_minimo( ultimos_4_valores)
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
                                       existe = self.obtener_inicio( valor_anterior, lista)
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
                                           dict_min = self.buscar_valor_minimo( ultimos_4_valores)
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
                                       verdadero = self.menor_proximo_valor_inicio( lista_sobrecarga)
                                       sobrecarga = self.buscar_sobrecarga_inicio( lista_sobrecarga,
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
                                           dict_min = self.buscar_valor_minimo( ultimos_4_valores)
                                           lista.append(dict_min)
                                           existe = self.obtener_inicio( valor_anterior, lista)
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
                                               dict_min = self.buscar_valor_minimo( ultimos_4_valores)
                                               lista.append(dict_min)
                                               existe = self.obtener_inicio( valor_anterior, lista)
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
                                               dict_min = self.buscar_valor_minimo( ultimos_4_valores)
                                               lista.append(dict_min)
                                               existe = self.obtener_inicio( valor_anterior, lista)
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
                                               dict_min = self.buscar_valor_minimo( ultimos_4_valores)
                                               lista.append(dict_min)
                                               existe = self.obtener_inicio( valor_anterior, lista)
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


    def obtener_niveles(self, pozo, anno_inicio, anno_fin):  #trabaje aqui GJBL
       tabla_agrupamiento = 'df_nivel_anual_pozo'

       sql = """ select anno,(media_hiperanual_enero)as enero,
                        (media_hiperanual_febrero)as febrero,
                        (media_hiperanual_marzo)as marzo,
                        (media_hiperanual_abril)as abril,
                        (media_hiperanual_mayo)as mayo,
                        (media_hiperanual_junio)as junio,
                        (media_hiperanual_julio)as julio,
                        (media_hiperanual_agosto)as agosto,
                        (media_hiperanual_septiembre)as septiembre,
                        (media_hiperanual_octubre)as octubre,
                        (media_hiperanual_noviembre)as noviembre,
                        (media_hiperanual_diciembre)as diciembre
                   from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                   where anno BETWEEN '""" + str(anno_inicio) + """' AND '""" + str(anno_fin) + """' AND
                   tabla_objeto.pozo_id = '""" + str(pozo) + """'
                   ORDER BY anno ASC;"""
       self.env.cr.execute(sql)
       datos_vistas = self.env.cr.fetchall()
       return datos_vistas


    def _periodomonth(self, month):  #trabaje aqui GJBL
       if month >= 5 and month <= 10:
           return 'humedo'
       return 'seco'

    def _lengthmonth(self, year, month):  #trabaje aqui GJBL
       if month == 2 and ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))):
           return 29
       return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]


    def _numero_mes(self, month):  #trabaje aqui GJBL
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


    def _mes_numero(self, month):  #trabaje aqui GJBL
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


    def _mes_numero_full(self, month):  #trabaje aqui GJBL
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


    def formar_fecha_inicio(self, pozo):  #trabaje aqui GJBL
       datos_vistas = self.obtener_nivele_actual_asc(pozo)
       buscar = self.buscar_anno(pozo)
       encontro = 0
       dia = 1  # VER ESTO DESPUES
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
                   dia = 1  # VER ESTO DESPUES
                   mes = mes_valor
                   anno_inicio = datos_vista[0]
                   fecha_inicio = datetime.datetime(anno_inicio, mes, dia)
                   encontro = 1
                   break
               temp += 1
       return fecha_inicio


    def formar_fecha_fin(self, pozo):    #trabaje aqui GJBL
       datos_vistas = self.obtener_nivele_actual(pozo)
       buscar = self.buscar_anno_desc(pozo)
       encontro = 0
       posicion = 12
       dia = 1  # VER ESTO DESPUES
       mes = 12
       anno_fin = buscar[0]['anno']
       fecha_fin = datetime.datetime(anno_fin, mes, dia)
       for datos_vista in datos_vistas:
           if encontro == 1:
               break
           while posicion >= 1:
               if datos_vista[posicion] and datos_vista[posicion] != -999999.110:
                   dia = 1   # VER ESTO DESPUES
                   mes = posicion
                   anno_inicio = datos_vista[0]
                   fecha_fin = datetime.datetime(anno_inicio, mes, dia)
                   encontro = 1
                   break
               posicion -= 1
           posicion = 12
       return fecha_fin

    def obtener_promedio_alturas(self, pozo_ids_actualizar, ok):   #trabaje aqui GJBL
       pozo_obj = self.env['df.pozo']
       # ids=pozo_obj.search(cr, uid, [])
       ids = pozo_ids_actualizar
       # inicio=datetime.datetime.now()
       # fin=datetime.datetime.now()
       for pozo in self.browse(ids):
           existe = self.existe_pozo(pozo.id)
           if existe:
               inicio = self.formar_fecha_inicio(pozo.id)
               fin = self.formar_fecha_fin(pozo.id)
               elementos = self.obtener_niveles_acotados_dic(pozo.id, inicio.year, fin.year)
               if elementos:
                   vals = {}
                   if elementos[0].get('anno'):
                       del elementos[0]['anno']
                   min = list(elementos[0].values())[0]
                   max = 0.0
                   valor = 0.0
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
                       if elementos[contador_elementos][self._mes_numero(inicio.month)] != None:
                           valor = float("%.3f" % float(elementos[contador_elementos][self._mes_numero(inicio.month)]))
                           # if valor != -999999.110:
                       if valor < min:
                           min = valor
                       if valor > max:
                           max = valor
                           #---------BUSCANDO RECARGAS
                       if len(valores_recarga) > 0:  #si existen valores en analisis
                           valor_anterior = valores_recarga[len(valores_recarga) - 1]['valor']
                           #------------ VERIFICANO PEQUENNAS DESCARGAS EN SECUENCIA QUE AL FINAL PUEDEN CONLLEVAR A UN DELTA ALTO
                           if valor - valor_anterior <= valor_precision and valor - valor_anterior > 0:
                               suma_descargas_secuencia += valor - valor_anterior
                           else:
                               suma_descargas_secuencia = 0
                           if (valor_anterior > valor or (
                                           valor - valor_anterior <= valor_precision and valor - valor_anterior > 0)) and suma_descargas_secuencia < valor_precision:
                               #lo apilo
                               valores_recarga.append({'tiempo_milisegundos': tiempo_milisegundos, 'valor': valor})
                           elif len(valores_recarga) > 1:
                               suma_descargas_secuencia = 0

                               #--------------------------------------------- DESAPILO VALORES BASURA
                               #desapilo valores basura del fin
                               indice_desapilo = len(valores_recarga) - 1
                               valores_recarga_punto_mas_alto = sorted(valores_recarga, key=lambda tup: tup['valor'])[0]['valor']
                               while indice_desapilo >= 0:
                                   if valores_recarga[indice_desapilo]['valor'] > valores_recarga[indice_desapilo - 1][
                                       'valor'] or valores_recarga[indice_desapilo][
                                       'valor'] > valores_recarga_punto_mas_alto:
                                       del valores_recarga[indice_desapilo]
                                       indice_desapilo -= 1
                                   else:
                                       break;
                                   if len(valores_recarga) == 1:
                                       valores_recarga = []
                                       break;

                               #desapilo valores basura del inicio
                               if len(valores_recarga) > 1:
                                   indice_desapilo = 0
                                   valores_recarga_punto_mas_bajo = sorted(valores_recarga, key=lambda tup: tup['valor'], reverse=True)[0]['valor']
                                   while indice_desapilo < len(valores_recarga):
                                       if valores_recarga[indice_desapilo]['valor'] < valores_recarga[indice_desapilo + 1]['valor'] or valores_recarga[indice_desapilo]['valor'] < valores_recarga_punto_mas_bajo:
                                           del valores_recarga[indice_desapilo]
                                       else:
                                           break;
                                       if len(valores_recarga) == 1:
                                           valores_recarga = []
                                           break;
                                   #--------------------------------------------- fin DESAPILO VALORES BASURA

                               if len(valores_recarga) > 1:
                                   #punto delta_h
                                   #proximo IF para no tomar pequennas series insignificantes que no cumplen con el margen de error
                                   if (abs(valores_recarga[len(valores_recarga) - 1]['valor'] - valores_recarga[0][
                                       'valor']) > valor_precision):
                                       if not (
                                               abs(valores_recarga[0]['valor'] - valores_recarga[len(valores_recarga) - 1][
                                                   'valor']) == 0):
                                           suma_h_periodo += abs(
                                               valores_recarga[0]['valor'] - valores_recarga[len(valores_recarga) - 1][
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
                           # if verificando_annos.count(anno_delta_h) == 0:
                           #    verificando_annos.append(anno_delta_h)
                       inicio = inicio + relativedelta(months=1)        #VER ESTO DESPUES

                   if cantidad_h_periodo != 0:
                       # promedio=suma_h_periodo / len(elementos)
                       promedio = suma_h_periodo / len(verificando_annos)
                   else:
                       promedio = 0.0
                   vals['promedio_h_periodo'] = promedio
                   vals['minimo_h_periodo'] = min
                   vals['maximo_h_periodo'] = max
                   rec_explotable = self.browse(pozo.id).recurso_explotable
                   area = self.browse(pozo.id).area
                   deltaH = 2 * promedio
                   coeficiente_calculado = (rec_explotable * 1000000) / (deltaH * area * 1000000) if (
                                                                                                         deltaH * area * 1000000) > 0 else 0
                   vals['coeficiente_almacenamiento_calculado'] = coeficiente_calculado
                   if pozo.id:
                       #pozo_obj.write([pozo.id], vals)
                       pozo.write(vals)
                   else:
                       pozo_obj.create(vals)
               # pozo_obj promedio
       return True

    def _get_equipments(self):  # trabaje aqui GJBL
        pass
        # # user = self.env('res.users').browse(cr, uid, uid)
        # user = self.env.user
        # current_date = datetime.now().strftime('%Y-%m-%d')
        # equipment_list = self.env['df.hc.rain.base.integracion'].all_equip_red_mensual(str(user.company_id.id), current_date)
        # # TODO aqui falta el modulo df_hc_rain_base
        # response = str([e['equipment_id'] for e in equipment_list])
        # if self.ids:
        #     return dict((id, response) for id in self.ids)
        # return str(response)


    def _getprov_id(self):     #trabaje aqui GJBL
       # usuario = self.env['res.users'].browse(self.env.uid)  # usuario loggeado
       # compania_id = self.env('res.company')._company_default_get('df.hc.rain.base.station')
       #
       # compannia = self.env('res.company').browse(compania_id)
       # if compannia:
       #     prov_id = compannia.state_id
       # return prov_id.id
       user = self.env.user
       provincia_usuario_id = user.company_id.state_id.id
       return self.env['res.country.state'].search([('id', '=', provincia_usuario_id)])




    def _estado_pozo(self):   #trabaje aqui GJBL
       pozo_obj = self.env['df.pozo']
       res = {}
       objeto_pozos = pozo_obj.browse(self.ids)
       # objeto_pozos = pozo_obj.browse(cr, uid, pozo_obj.search(cr, uid, [('id','=',1042)]))
       # encontro=0
       posicion = 11
       for objeto_pozo in objeto_pozos:
           ok = False
           vals = {}
           vals['id'] = objeto_pozo.id
           encontro = 0
           deltah = self.browse(objeto_pozo.id).promedio_h_periodo  #  self.env.uid
           min_fijo = self.browse(objeto_pozo.id).minimo_h_periodo_fijo
           min_calculado = self.browse(objeto_pozo.id).minimo_h_periodo
           max_fijo = self.browse(objeto_pozo.id).maximo_h_periodo_fijo
           max_calculado = self.browse(objeto_pozo.id).maximo_h_periodo
           if min_fijo <= 0:
               min = min_calculado
           else:
               min = min_fijo
           if max_fijo <= 0:
               max = max_calculado
           else:
               max = max_fijo
           datos_vistas = self.obtener_niveles_totales_dec(objeto_pozo.id)#invocan obtener_niveles_totales_dec
           if datos_vistas:
               for datos_vista in datos_vistas:
                   if encontro == 1:
                       break
                   while posicion >= 1:
                       if datos_vista[posicion] and datos_vista[posicion] != -999999.110:
                           nivel_alerta = max - deltah
                           nivel_alarma = max - (deltah / 2)
                           if datos_vista[posicion] >= nivel_alerta and datos_vista[posicion] <= nivel_alarma:
                               objeto_pozo.estado = 'desfavorable'
                               vals['estado1'] = 'desfavorable'
                           elif datos_vista[posicion] >= nivel_alarma and datos_vista[posicion] <= max:
                               objeto_pozo.estado = 'muy desfavorable'
                               vals['estado1'] = 'muy desfavorable'
                           elif datos_vista[posicion] <= nivel_alerta and datos_vista[posicion] >= (min + deltah):
                               objeto_pozo.estado = 'favorable'
                               vals['estado1'] = 'favorable'
                           elif datos_vista[posicion] <= (min + deltah) and datos_vista[posicion] >= min:
                               objeto_pozo.estado = 'muy favorable'
                               vals['estado1'] = 'muy favorable'
                           elif datos_vista[posicion] >= max:
                               objeto_pozo.estado = u'crítico'
                               vals['estado1'] = u'crítico'
                           else:
                               objeto_pozo.estado = 'no hay nivel'
                               vals['estado1'] = 'no hay nivel'
                           pozo_obj.write(vals)
                           encontro = 1
                           ok = True
                           break
                       posicion -= 1
                   if ok == False:
                       objeto_pozo.estado = 'no hay nivel'
                       vals['estado1'] = 'no hay nivel'
                       pozo_obj.write(vals)
                   posicion = 11
           else:
               objeto_pozo.estado = 'no hay nivel'
               vals['estado1'] = 'no hay nivel'
               pozo_obj.write(vals)

       #return res

    #aqui empiezan los campos

    nombre = fields.Char(string='Name', size=64, required=False)
    area = fields.Float('Area of influence (km2)', digits=(3, 3), required=False)
    cota_topografica = fields.Float('Elevation topography (m)', digits=(3, 3), required=False)
    sigla = fields.Char(string='Abbreviation', size=64, required=True)
    profundidad_total = fields.Float('Total depth (m)', digits=(3, 3), required=False)
    diametro = fields.Float('Diameter (m)', digits=(3, 3), required=False)
    orden_sondeo = fields.Selection([('1', '|'), ('2', '||'), ('3', '|||')], 'Probe of order', required=False)
    profundidad_linea_gramo = fields.Integer(string='Depth of the gram line (m)', required=False)
    profundidad_piso_acuifero = fields.Integer(string='Depth of the aquifer floor (m)', required=False)
    abatimiento_maximo_permisible = fields.Integer(string='Maximum allowable gloom (m)', required=False)
    ubicado = fields.Selection(
        [('basin', 'Underground basin'), ('sector', 'Hydrogeological sector'), ('block', 'Block')], 'Located in',
        required=True, help="")
    representativo = fields.Boolean(string='Representative', required=False,
                                    help='This field defines whether the well is representative or not')
    sector_hidrologico_id = fields.Many2one('df.sector.hidrologico', string='Hydrogeological sector', required=False,
                                            ondelete='cascade')
    bloque_id = fields.Many2one('df.bloque', string='Block', required=False, ondelete='cascade')
    cuenca_subterranea_id = fields.Many2one('df.cuenca.subterranea', 'Underground basin', required=False,
                                            ondelete='cascade')
    nivel_ids = fields.One2many('df.nivel.anual.pozo', 'pozo_id', string='Levels', required=False)
    coordenadas = fields.Selection([('north', 'North Cuba'), ('south', 'South Cuba')], 'Coordinates', required=False,
                                   help="")
    norte = fields.Float('North', digits=(3, 3), required=False)
    este = fields.Float('East', digits=(3, 3), required=False)
    norte1 = fields.Float('North', digits=(3, 3), required=False)
    este1 = fields.Float('East', digits=(3, 3), required=False)
    coordenas_string = fields.Char(compute='obtener_coordenadas', string="Coordinates")
    coeficiente_almacenamiento = fields.Float('Coefficient of storage', digits=(3, 3), required=False)
    coeficiente_almacenamiento_string = fields.Char(string='Coefficient of storage', size=100, required=False)
    equipment_list = fields.Char(compute='_get_equipments', type='char', size=255, method=True)
    # TODO aqui falta el modulo df_hc_rain_base comentarie la funcion _get_equipments
    # equipo_ids = fields.Many2many('df.hc.rain.base.equipment', 'df_equipo_pozo', 'fk_pozo_id', 'fk_equipo_id',string='Equipments')
    equipo_ids = fields.Many2many('df.hc.rain.base.equipment', 'df_equipo_pozo', 'fk_pozo_id', 'fk_equipo_id',string='Equipments')
    # equipo_ids = fields.Many2many(comodel_name="df.equipment", relation="df_equipo_pozo", column1="fk_pozo_id", column2="fk_equipo_id", string="Equipments")
    #Este campo equipo_ids es de otro modulo que no se ha hecho todavía en ODOO 12

    promedio_h_periodo = fields.Float(string='Net reCharge', digits=(3, 3), required=False, readonly=True)
    promedio_h_periodo_fijo = fields.Float(string='Net reCharge', digits=(3, 3), required=False)
    minimo_h_periodo = fields.Float(string='Min', digits=(3, 3), required=False, readonly=True)
    maximo_h_periodo = fields.Float(string='Max', digits=(3, 3), required=False, readonly=True)
    minimo_h_periodo_fijo = fields.Float(string='Min', digits=(3, 3), required=False)
    maximo_h_periodo_fijo = fields.Float(string='Max', digits=(3, 3), required=False)
    valor_precision = fields.Float(string='Precision value', digits=(3, 3), required=False,
                                   help="Put precision level value for detection algorithm,if precision is closer to 0 then algorithm take minnor level diference as an important change")
    coeficiente_aprovechamiento_hidraulico = fields.Float(string='Coefficient of hydraulic use', digits=(3, 3),
                                                          required=False)
    coeficiente_infiltracion = fields.Float(string='Coefficient infiltration', digits=(3, 3), required=False)

    zona_ueb_id = fields.Many2one('df.zona.ueb', 'Zone', required=False)
    #Este campo zona_ueb_id es de otro modulo que no se ha hecho todavía en ODOO 12

    recurso_explotable = fields.Float('Exploitable resource Qe (hm³)', digits=(3, 3), required=False)
    coeficiente_almacenamiento_calculado = fields.Float('Coefficient of storage1', digits=(3, 3), required=False,
                                                        readonly=True)
    state_id = fields.Many2one('res.country.state', 'Country State', required=True) #default = _getprov_id
    ueb_id = fields.Many2one('df.ueb', 'Ueb', required=False)
    seco = fields.Boolean(string='Dry reservoir', help="If it's a dry reservoir or not")
    estado = fields.Char(compute='_estado_pozo', string="State")
    estado1 = fields.Char(string='State', size=64, required=False)
    mensual = fields.Boolean(string='Monthly', required=False)
    trimestral = fields.Boolean(string='Quarterly', required=False)
    semestral = fields.Boolean(string='Biannual', required=False)
    batometrico = fields.Boolean(string='Batometrico', required=False)
    seguridad_compania = fields.Char(compute='_seguridad_compania')
    municipality_id = fields.Many2one('df.municipality', string='Municipio')
    country_id = fields.Many2one('res.country', 'Country', default = _country_id,required=False)
    provincia_ids = fields.Many2many("res.country.state",default = _seguridad_provincial, store=True)

    _sql_constraints = [
        ('sigla_uniq', 'unique(sigla)', 'The Abbreviation already exists for that object!'),
    ]

    # def obtener_coordenadas(self):
    #     pass

    # def _get_equipments(self):
    #     pass

    #def _estado_pozo(self):
    #    pass

    def _seguridad_compania(self):
        pass
    
    ###METODOS PARA CALCULO DE NIVELES PRONOSTICOS
    ## def _calcular_vol_exp(self, cr, uid, id, obj_name, mes, anno):
    ##     vol_exp = None
    ##     obj_exp_anual = self.pool.get(obj_name)
    ##     exp_anual_ids = obj_exp_anual.search([('anno','=', anno), ('pozo_id', '=', id)])
    ##     if exp_anual_ids:
    ##         exp_anual = obj_exp_anual.browse(cr, uid, exp_anual_ids)
    ##         if mes == 5:
    ##             vol_exp = exp_anual.media_hiperanual_mayo
    ##         elif mes == 6:
    ##             vol_exp = exp_anual.media_hiperanual_junio
    ##         elif mes == 7:
    ##             vol_exp = exp_anual.media_hiperanual_julio
    ##         elif mes == 8:
    ##             vol_exp = exp_anual.media_hiperanual_agosto
    ##         elif mes == 9:
    ##             vol_exp = exp_anual.media_hiperanual_septiembre
    ##         elif mes == 10:
    ##             vol_exp = exp_anual.media_hiperanual_octubre
    ##     return vol_exp
    ##
    ## def calcular_delta_z(self, cr, uid, id, mes, anno, context=None):
    ##     """delta_z = vol_explotacion/coeficiente_almacenamiento*area"""
    ##     vol_exp = self._calcular_vol_exp(cr, uid, id, 'df.explotacion.anual.pozo', mes, anno)
    ##     if vol_exp == None:
    ##         vol_exp = self._calcular_vol_exp(cr, uid, id, 'df.plan.explotacion.anual.pozo', mes, anno)
    ##     if vol_exp != None:
    ##         obj_pozo = self.pool.get('df.pozo')
    ##         pozo = obj_pozo.browse(cr, uid, [id])
    ##         if pozo.coeficiente_almacenamiento != 0 and pozo.area != 0:
    ##             return vol_exp/pozo.coeficiente_almacenamiento * pozo.area
    ##     return None
    #
    def calcular_delta_z(self, id, vol_exp):   #trabaje aqui GJBL
        """delta_z = vol_explotacion/coeficiente_almacenamiento*area"""
        if vol_exp != None:
            obj_pozo = self.env['df.pozo']
            pozo = obj_pozo.browse([id])[0]
            if pozo.coeficiente_almacenamiento != 0 and pozo.area != 0:
                return round((vol_exp * 1000000) / (pozo.coeficiente_almacenamiento * pozo.area * 1000000),
                             5) # * 1000000 para llevar a m cuadrados
        return None


    def calcular_delta_z1(self, vol_exp, iddd):  #trabaje aqui GJBL
        """delta_z = vol_explotacion/coeficiente_almacenamiento*area"""
        delta_z = None
        if vol_exp != None:
            obj_pozo = self.env['df.pozo']
            pozo = obj_pozo.browse(iddd)[0]
            if pozo.coeficiente_almacenamiento != 0 and pozo.area != 0:
                delta_z = round((vol_exp * 1000000) / (pozo.coeficiente_almacenamiento * pozo.area * 1000000),2) # * 1000000 para llevar a m cuadrados
            else:
                # raise osv.except_osv(_('Advertencia'), _(
                #     'Debe entrar el área y el coeficiente de almacenamiento del pozo seleccionado.'))
                raise UserError(_('Debe entrar el área y el coeficiente de almacenamiento del pozo seleccionado.'))
        return delta_z


    def calcular_vol_probable(self, id, lluvias_del_mes):  #trabaje aqui GJBL
        """
            calculo de vol probable = lluvia * coeficiente_infiltracion * area

        :param cr:
        :param uid:
        :param id: id del pozo
        :param lluvias_del_mes: diccionario con los valores a los diferentes porcientos
        :param context:
        :return: diccionario con los vol probables a los diferentes porcientos
        """
        res = {}
        pozo = self.env['df.pozo'].browse([id])[0]
        if lluvias_del_mes['50'] != None:
            res['50'] = (float(lluvias_del_mes['50']) / 1000) * pozo.coeficiente_infiltracion * pozo.area * 1000000
        else:
            res['50'] = None
        if lluvias_del_mes['75'] != None:
            res['75'] = (float(lluvias_del_mes['75']) / 1000) * pozo.coeficiente_infiltracion * pozo.area * 1000000
        else:
            res['75'] = None
        if lluvias_del_mes['95'] != None:
            res['95'] = (float(lluvias_del_mes['95']) / 1000) * pozo.coeficiente_infiltracion * pozo.area * 1000000
        else:
            res['95'] = None
        return res


    def calcular_delta_h(self, id, mes, anno, lluvias_del_mes):  #trabaje aqui GJBL
        """delta_h_% = vol_probable_%/coeficiente_almacenamiento*area"""

        res = {}
        pozo = self.env['df.pozo'].browse([id])[0]
        vol_probables = self.calcular_vol_probable(id, lluvias_del_mes)
        if vol_probables['50'] != None and pozo.coeficiente_almacenamiento != 0 and pozo.area != 0:
            res['50'] = float(vol_probables['50']) / (pozo.coeficiente_almacenamiento * pozo.area * 1000000)
        else:
            res['50'] = None
        if vol_probables['75'] != None and pozo.coeficiente_almacenamiento != 0 and pozo.area != 0:
            res['75'] = float(vol_probables['75']) / (pozo.coeficiente_almacenamiento * pozo.area * 1000000)
        else:
            res['75'] = None
        if vol_probables['95'] != None and pozo.coeficiente_almacenamiento != 0 and pozo.area != 0:
            res['95'] = float(vol_probables['95']) / (pozo.coeficiente_almacenamiento * pozo.area * 1000000)
        else:
            res['95'] = None
        return res


    def calcular_niveles_pronosticos_mes(self, id, nivel_inicial_porcientos, vol_exp, mes, anno,
                                         lluvias_del_mes):  #trabaje aqui GJBL
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
        # delta_z = self.calcular_delta_z(cr, uid, id, mes, anno)
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


    def calcular_nivel_real(self, id, mes, anno):  #trabaje aqui GJBL
        """Calcula nivel dado un mes"""
        nivel = None
        if type(id) != int:
            id = id[0]
        obj_nivel_anual = self.env['df.nivel.anual.pozo']
        nivel_anual_ids = obj_nivel_anual.search([('anno', '=', anno), ('pozo_id', '=', id)])
        if nivel_anual_ids:
            #nivel_anual = obj_nivel_anual.browse(nivel_anual_ids)[0]
            nivel_anual = nivel_anual_ids[0]
            if mes == 1:
                if nivel_anual.media_hiperanual_enero != -999999.11:
                    nivel = nivel_anual.media_hiperanual_enero
                    # else:
                    #     nivel=0
            elif mes == 2:
                if nivel_anual.media_hiperanual_febrero != -999999.11:
                    nivel = nivel_anual.media_hiperanual_febrero
                    # else:
                    #     nivel=0
            elif mes == 3:
                if nivel_anual.media_hiperanual_marzo != -999999.11:
                    nivel = nivel_anual.media_hiperanual_marzo
                    # else:
                    #     nivel=0
            elif mes == 4:
                if nivel_anual.media_hiperanual_abril != -999999.11:
                    nivel = nivel_anual.media_hiperanual_abril
                    # else:
                    #     nivel=0
            elif mes == 5:
                if nivel_anual.media_hiperanual_mayo != -999999.11:
                    nivel = nivel_anual.media_hiperanual_mayo
                    # else:
                    #     nivel=0
            elif mes == 6:
                if nivel_anual.media_hiperanual_junio != -999999.11:
                    nivel = nivel_anual.media_hiperanual_junio
                    # else:
                    #     nivel=0
            elif mes == 7:
                if nivel_anual.media_hiperanual_julio != -999999.11:
                    nivel = nivel_anual.media_hiperanual_julio
                    # else:
                    #     nivel=0
            elif mes == 8:
                if nivel_anual.media_hiperanual_agosto != -999999.11:
                    nivel = nivel_anual.media_hiperanual_agosto
                    # else:
                    #     nivel=0
            elif mes == 9:
                if nivel_anual.media_hiperanual_septiembre != -999999.11:
                    nivel = nivel_anual.media_hiperanual_septiembre
                    # else:
                    #     nivel=0
            elif mes == 10:
                if nivel_anual.media_hiperanual_octubre != -999999.11:
                    nivel = nivel_anual.media_hiperanual_octubre
                    # else:
                    #     nivel=0
            elif mes == 11:
                if nivel_anual.media_hiperanual_noviembre != -999999.11:
                    nivel = nivel_anual.media_hiperanual_noviembre
                    # else:
                    #     nivel=0
            else:
                if nivel_anual.media_hiperanual_diciembre != -999999.11:
                    nivel = nivel_anual.media_hiperanual_diciembre
                    # else:
                    #     nivel=0

        return nivel


    def calcular_niveles_pronosticos_puros(self, anno, vol_exp_de_meses, lluvias_de_meses, pozo_ids=None,
                                           context=None):  #trabaje aqui GJBL
        """
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

        nivel_abril = self.calcular_nivel_real(id, 4, anno)
        nivel_inicial_porcientos = {'50': nivel_abril, '75': nivel_abril, '95': nivel_abril}
        if nivel_abril:
            nivel_pron_mayo = self.calcular_niveles_pronosticos_mes(id, nivel_inicial_porcientos,
                                                                    vol_exp_de_meses['5'], 5, anno,
                                                                    lluvias_de_meses['5'], context)
            res[0] = nivel_pron_mayo
            if nivel_pron_mayo:
                nivel_pron_junio = self.calcular_niveles_pronosticos_mes(id, nivel_pron_mayo,
                                                                         vol_exp_de_meses['6'], 6, anno,
                                                                         lluvias_de_meses['6'], context)
                res[1] = nivel_pron_junio
            if nivel_pron_junio:
                nivel_pron_julio = self.calcular_niveles_pronosticos_mes(id, nivel_pron_junio,
                                                                         vol_exp_de_meses['7'], 7, anno,
                                                                         lluvias_de_meses['7'], context)
                res[2] = nivel_pron_julio
            if nivel_pron_julio:
                nivel_pron_agosto = self.calcular_niveles_pronosticos_mes(id, nivel_pron_julio,
                                                                          vol_exp_de_meses['8'], 8, anno,
                                                                          lluvias_de_meses['8'], context)
                res[3] = nivel_pron_agosto
            if nivel_pron_agosto:
                nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes(id, nivel_pron_agosto,
                                                                              vol_exp_de_meses['9'], 9, anno,
                                                                              lluvias_de_meses['9'], context)
                res[4] = nivel_pron_septiembre
            if nivel_pron_septiembre:
                nivel_pron_octubre = self.calcular_niveles_pronosticos_mes(id, nivel_pron_septiembre,
                                                                           vol_exp_de_meses['10'], 10, anno,
                                                                           lluvias_de_meses['10'], context)
                res[5] = nivel_pron_octubre
        else:
            #raise osv.except_osv(_('Error'), _('Level of april must be known for prognostic calculation!'))
            raise UserError(_('Level of april must be known for prognostic calculation!'))

        result = {
            'year': anno,
            'z': self.calcular_delta_z(id, vol_exp_de_meses['5']),
            'object': '',
            'categoryAxis': [],
            'yAxis': [{'minimo': 0, 'maximo': 1000, 'promedio_h_historico': 0}],
            'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 1000}],
            'series': [
                {'name': 'Nivel medido', 'data': [('May', self.calcular_nivel_real(id, 5, anno)),
                                                  ('Jun', self.calcular_nivel_real(id, 6, anno)),
                                                  ('July', self.calcular_nivel_real(id, 7, anno)),
                                                  ('Ago', self.calcular_nivel_real(id, 8, anno)),
                                                  ('Sep', self.calcular_nivel_real(id, 9, anno)),
                                                  ('Oct', self.calcular_nivel_real(id, 10, anno))]},
                {'name': 'Nivel lluvia real',
                 'data': [('May', 25.59), ('Jun', 24.93), ('Jul', 23.74), ('Ago', 23.03), ('Sep', 22.5),
                          ('Oct', 22.11)]},
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


    def calcular_nivel_lluvia_real(self, id, nreal, vol_exp_de_meses, anno):  #trabaje aqui GJBL
        res = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
        obj_pozo = self.env['df.pozo']
        pozo_ids = obj_pozo.search([('id', '=', id)]).id
        pozo_objeto = obj_pozo.browse(pozo_ids)[0]
        nivel_real5 = self.calcular_nivel_real(id, 5, anno)
        if (pozo_objeto.coeficiente_infiltracion != 0 and pozo_objeto.area != 0 and pozo_objeto.coeficiente_almacenamiento != 0):
            if (nreal.get('5') and nreal['5'] != None and nivel_real5 != None and vol_exp_de_meses['5'] != None):
                volumen5 = ((float(
                    nreal['5']) / 1000) * pozo_objeto.coeficiente_infiltracion * pozo_objeto.area * 1000000) / (
                           pozo_objeto.coeficiente_almacenamiento * pozo_objeto.area * 1000000)
                delta_z = self.calcular_delta_z(id, vol_exp_de_meses['5'])
                nivel_real_lluvia = nivel_real5 - (volumen5 - delta_z)
                res['5'] = round(nivel_real_lluvia, 2)
            else:
                res['5'] = None
            nivel_real6 = self.calcular_nivel_real(id, 6, anno)
            if (nreal.get('6') and nreal['6'] != None and nivel_real6 != None and vol_exp_de_meses['6'] != None):
                volumen6 = ((float(
                    nreal['6']) / 1000) * pozo_objeto.coeficiente_infiltracion * pozo_objeto.area * 1000000) / (
                           pozo_objeto.coeficiente_almacenamiento * pozo_objeto.area * 1000000)
                delta_z = self.calcular_delta_z(id, vol_exp_de_meses['6'])
                nivel_real_lluvia = nivel_real6 - (volumen6 - delta_z)
                res['6'] = round(nivel_real_lluvia, 2)
            else:
                res['6'] = None
            nivel_real7 = self.calcular_nivel_real(id, 7, anno)
            if (nreal.get('7') and nreal['7'] != None and nivel_real7 != None and vol_exp_de_meses['7'] != None):
                volumen7 = ((float(
                    nreal['7']) / 1000) * pozo_objeto.coeficiente_infiltracion * pozo_objeto.area * 1000000) / (
                           pozo_objeto.coeficiente_almacenamiento * pozo_objeto.area * 1000000)
                delta_z = self.calcular_delta_z(id, vol_exp_de_meses['7'])
                nivel_real_lluvia = nivel_real7 - (volumen7 - delta_z)
                res['7'] = round(nivel_real_lluvia, 2)
            else:
                res['7'] = None
            nivel_real8 = self.calcular_nivel_real(id, 8, anno)
            if (nreal.get('8') and nreal['8'] != None and nivel_real8 != None and vol_exp_de_meses['8'] != None):
                volumen8 = ((float(
                    nreal['8']) / 1000) * pozo_objeto.coeficiente_infiltracion * pozo_objeto.area * 1000000) / (
                           pozo_objeto.coeficiente_almacenamiento * pozo_objeto.area * 1000000)
                delta_z = self.calcular_delta_z(id, vol_exp_de_meses['8'])
                nivel_real_lluvia = nivel_real8 - (volumen8 - delta_z)
                res['8'] = round(nivel_real_lluvia, 2)
            else:
                res['8'] = None
            nivel_real9 = self.calcular_nivel_real(id, 9, anno)
            if (nreal.get('9') and nreal['9'] != None and nivel_real9 != None and vol_exp_de_meses['9'] != None):
                volumen9 = ((float(
                    nreal['9']) / 1000) * pozo_objeto.coeficiente_infiltracion * pozo_objeto.area * 1000000) / (
                           pozo_objeto.coeficiente_almacenamiento * pozo_objeto.area * 1000000)
                delta_z = self.calcular_delta_z(id, vol_exp_de_meses['9'])
                nivel_real_lluvia = nivel_real9 - (volumen9 - delta_z)
                res['9'] = round(nivel_real_lluvia, 2)
            else:
                res['9'] = None
            nivel_real10 = self.calcular_nivel_real(id, 10, anno)
            if (nreal.get('10') and nreal['10'] != None and nivel_real10 != None and vol_exp_de_meses[
                '10'] != None ):
                volumen10 = ((float(
                    nreal['10']) / 1000) * pozo_objeto.coeficiente_infiltracion * pozo_objeto.area * 1000000) / (
                            pozo_objeto.coeficiente_almacenamiento * pozo_objeto.area * 1000000)
                delta_z = self.calcular_delta_z(id, vol_exp_de_meses['10'])
                nivel_real_lluvia = nivel_real10 - (volumen10 - delta_z)
                res['10'] = round(nivel_real_lluvia, 2)
                nreal
            else:
                res['10'] = None
        return res


    def calcular_explotacion_plan(self, id, anno):  #trabaje aqui GJBL
        explotacion = None
        res = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
        obj_plan_explotacion = self.env['df.plan.explotacion.anual.pozo']
        explotacion_anual_ids = obj_plan_explotacion.search([('anno', '=', anno), ('pozo_id', '=', id)]).ids
        if explotacion_anual_ids:
            explotacion_anual = obj_plan_explotacion.browse(explotacion_anual_ids)[0]
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
            # raise osv.except_osv(_('Advertencia'),
            #                      _('Debe de existir la explotación de este pozo para el año seleccionado!'))
            raise UserError(_('Debe de existir la explotación de este pozo para el año seleccionado!'))


    def calcular_probabilidad(self, id):   #trabaje aqui GJBL
        probabilidad_ids_50 = []
        probabilidad_ids_75 = []
        probabilidad_ids_95 = []
        res = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
        lluvia = {'50': None, '75': None, '95': None}
        obj_probabilidad = self.env['df.probabilidad.pozo']
        tabla_agrupamiento = 'df_probabilidad_pozo'
        sql = """ select anno
                  from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                  where tabla_objeto.pozo_id = '""" + str(id) + """'
                  ORDER BY anno DESC;"""
        self.env.cr.execute(sql)
        datos_vistas = self.env.cr.dictfetchall()
        if datos_vistas:
            anno = datos_vistas[0]['anno']
            probabilidad_ids_50 = obj_probabilidad.search([('probabilidad', '=', '50%'), ('pozo_id', '=', id),
                                                                    ('anno', '=', anno)]).ids
            probabilidad_ids_75 = obj_probabilidad.search([('probabilidad', '=', '75%'), ('pozo_id', '=', id),
                                                                    ('anno', '=', anno)]).ids
            probabilidad_ids_95 = obj_probabilidad.search([('probabilidad', '=', '95%'), ('pozo_id', '=', id),
                                                                    ('anno', '=', anno)]).ids
        if probabilidad_ids_50 and probabilidad_ids_75 and probabilidad_ids_95:
            probabilidad_50 = obj_probabilidad.browse(probabilidad_ids_50)[0]
            probabilidad_75 = obj_probabilidad.browse(probabilidad_ids_75)[0]
            probabilidad_95 = obj_probabilidad.browse(probabilidad_ids_95)[0]
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
            #raise osv.except_osv(_('Advertencia'), _('Debe de existir la probabilidad del 50%,75% y 95% para el pozo!'))
            raise UserError(_('Debe de existir la probabilidad del 50%,75% y 95% para el pozo!'))


    def formar_diccionario(self, id, anno):  #trabaje aqui GJBL
        lluvia_real_obj = self.env['df.lluvia.real.pozo']
        lluvia_real_ids = lluvia_real_obj.search([('pozo_id', '=', id), ('anno', '=', anno)]).ids
        nreal = {'5': None, '6': None, '7': None, '8': None, '9': None, '10': None}
        if lluvia_real_ids:
            lluvia_real_meses = lluvia_real_obj.browse(lluvia_real_ids)
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
    def calcular_niveles_pronosticos_reales(self, id, anno1, nreal, pronostico, pozo_ids=None):  #trabaje aqui GJBL
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
        mes = [5, 6, 7, 8, 9, 10]
        # hhh=
        fecha_str = time.strftime('%Y%m')
        fecha_actual = int(fecha_str)
        vol_exp_de_meses = self.calcular_explotacion_plan(id, anno1)
        lluvias_de_meses = self.calcular_probabilidad(id)
        nivel_abril = self.calcular_nivel_real(id, 4, anno1)
        nreal = self.formar_diccionario(id, anno1)
        # lluvia_real_obj = self.pool.get('df.lluvia.real.pozo')
        # lluvia_real_ids = lluvia_real_obj.search(cr,uid,[('pozo_id','=',id),('anno','=',anno)])
        # nreal =  {'5': None,'6': None,'7': None,'8': None,'9':None,'10':None}
        # if lluvia_real_ids:
        #     lluvia_real_meses = lluvia_real_obj.browse(cr, uid, lluvia_real_ids)
        #     if lluvia_real_meses[0].media_hiperanual_mayo !=0.0:
        #         nreal['5']=lluvia_real_meses[0].media_hiperanual_mayo
        #     else:
        #         nreal['5']=None
        #     if lluvia_real_meses[0].media_hiperanual_junio!=0.0:
        #         nreal['6']=lluvia_real_meses[0].media_hiperanual_junio
        #     else:
        #         nreal['6']=None
        #     if lluvia_real_meses[0].media_hiperanual_julio!=0.0:
        #        nreal['7']=lluvia_real_meses[0].media_hiperanual_julio
        #     else:
        #         nreal['7']=None
        #     if lluvia_real_meses[0].media_hiperanual_agosto!=0.0:
        #         nreal['8']=lluvia_real_meses[0].media_hiperanual_agosto
        #     else:
        #         nreal['8']=None
        #     if lluvia_real_meses[0].media_hiperanual_septiembre!=0.0:
        #         nreal['9'] = lluvia_real_meses[0].media_hiperanual_septiembre
        #     else:
        #         nreal['9']=None
        #     if lluvia_real_meses[0].media_hiperanual_octubre!=0.0:
        #         nreal['10']=lluvia_real_meses[0].media_hiperanual_octubre
        #     else:
        #         nreal['10']=None
        nivel_lluvia_real = self.calcular_nivel_lluvia_real(id, nreal, vol_exp_de_meses, anno1)
        nivel_inicial_porcientos = {'50': nivel_abril, '75': nivel_abril, '95': nivel_abril}
        if nivel_abril:
            nivel_mayo = self.calcular_nivel_real(id, 5, anno1)
            anno = int(anno1)
            date = datetime.datetime(anno, 5, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes5 = int(date_substr[0])
            if (nivel_mayo or nivel_abril != None) and pronostico != 'puro':
                if fecha_mes5 > fecha_actual:
                    nivel_pron_mayo = self.calcular_niveles_pronosticos_mes(id, nivel_inicial_porcientos,
                                                                            vol_exp_de_meses['5'], 5, anno,
                                                                            lluvias_de_meses['5'])
                else:
                    nivel_pron_mayo = {'50': None, '75': None, '95': None}
                    # nivel_pron_mayo = {'50': nivel_mayo, '75': nivel_mayo, '95': nivel_mayo}
            else:
                nivel_pron_mayo = self.calcular_niveles_pronosticos_mes(id, nivel_inicial_porcientos,
                                                                        vol_exp_de_meses['5'], 5, anno,
                                                                        lluvias_de_meses['5'])
            res[0] = nivel_pron_mayo
            # anno=anno
            date = datetime.datetime(anno, 6, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes6 = int(date_substr[0])
            nivel_junio = self.calcular_nivel_real(id, 6, anno)
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
            nivel_julio = self.calcular_nivel_real( id, 7, anno)
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
            nivel_agosto = self.calcular_nivel_real( id, 8, anno)
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
            nivel_septiembre = self.calcular_nivel_real( id, 9, anno)
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
            nivel_octubre = self.calcular_nivel_real( id, 10, anno)
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
            #raise osv.except_osv(_('Advertencia'), _('Nivel de abril debe de existir para iniciar el pronóstico!'))
            raise UserError(_('Nivel de abril debe de existir para iniciar el pronóstico!'))

        obj = self.browse( [id])[0]

        result = {
            'year': anno,
            'z': self.calcular_delta_z( id, vol_exp_de_meses['5']),
            'sigla': str(obj.sigla),
            'object': '',
            'categoryAxis': [],
            'yAxis': [{'minimo': 0, 'maximo': 1000, 'promedio_h_historico': 0}],
            'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 1000}],
            'series': [
                {'name': 'Nivel medido', 'data': [('May', self.calcular_nivel_real( id, 5, anno)),
                                                  ('Jun', self.calcular_nivel_real( id, 6, anno)),
                                                  ('Jul', self.calcular_nivel_real( id, 7, anno)),
                                                  ('Agto', self.calcular_nivel_real( id, 8, anno)),
                                                  ('Sep', self.calcular_nivel_real( id, 9, anno)),
                                                  ('Oct', self.calcular_nivel_real( id, 10, anno))]},
                {'name': 'Nivel lluvia real', 'data': [('May', nivel_lluvia_real['5']), ('Jun', nivel_lluvia_real['6']),
                                                       ('Jul', nivel_lluvia_real['7']), ('Ago', nivel_lluvia_real['8']),
                                                       ('Sep', nivel_lluvia_real['9']),
                                                       ('Oct', nivel_lluvia_real['10'])]},
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


    def calcular_niveles_pronosticos_realesUnion(self, idd, anno1, vol_exp_de_meses1, nreall, pronostico,
                                                 lluvias_de_meses, nivel_abril, cont, meses1):  #trabaje aqui GJBL

        res = [None, None, None, None, None, None]
        fecha_str = time.strftime('%Y%m')
        fecha_actual = int(fecha_str)
        nreall = self.formar_diccionario(idd, anno1)
        nivel_lluvia_real = self.calcular_nivel_lluvia_real(idd, nreall, vol_exp_de_meses1, anno1)
        nivel_inicial_porcientos = {'50': nivel_abril, '75': nivel_abril, '95': nivel_abril}
        if nivel_abril:
            nivel_mayo = self.calcular_nivel_real(idd, 5, anno1)
            anno = anno1
            date = datetime.datetime(anno, 5, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes5 = int(date_substr[0])
            if (nivel_mayo or nivel_abril != None) and pronostico != 'puro':
            # if fecha_mes5 > fecha_actual:
                nivel_pron_mayo = self.calcular_niveles_pronosticos_mes(idd, nivel_inicial_porcientos,
                                                                        vol_exp_de_meses1['5'], 5, anno,
                                                                        lluvias_de_meses['5'])
                # else:
                #     nivel_pron_mayo = {'50': None, '75': None, '95': None}
            else:
                nivel_pron_mayo = self.calcular_niveles_pronosticos_mes(idd, nivel_inicial_porcientos,
                                                                        vol_exp_de_meses1['5'], 5, anno,
                                                                        lluvias_de_meses['5'])
            res[0] = nivel_pron_mayo
            # anno=anno
            date = datetime.datetime(anno, 6, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes6 = int(date_substr[0])
            nivel_junio = self.calcular_nivel_real(idd, 6, anno)
            if (nivel_junio or nivel_mayo != None) and pronostico != 'puro':
                # if fecha_mes6 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 5:
                    nivel_pron_mayo = {'50': nivel_mayo, '75': nivel_mayo, '95': nivel_mayo}
                nivel_pron_junio = self.calcular_niveles_pronosticos_mes(idd, nivel_pron_mayo,
                                                                         vol_exp_de_meses1['6'], 6, anno,
                                                                         lluvias_de_meses['6'])
                # else:
                #     nivel_pron_junio = {'50': None, '75': None, '95': None}
            elif nivel_pron_mayo:
                nivel_pron_junio = self.calcular_niveles_pronosticos_mes(idd, nivel_pron_mayo,
                                                                         vol_exp_de_meses1['6'], 6, anno,
                                                                         lluvias_de_meses['6'])
            res[1] = nivel_pron_junio
            # anno=anno
            date = datetime.datetime(anno, 7, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes7 = int(date_substr[0])
            nivel_julio = self.calcular_nivel_real(idd, 7, anno)
            if (nivel_julio or nivel_junio != None) and pronostico != 'puro':
                # if fecha_mes7 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 6:
                    nivel_pron_junio = {'50': nivel_junio, '75': nivel_junio, '95': nivel_junio}
                nivel_pron_julio = self.calcular_niveles_pronosticos_mes(idd, nivel_pron_junio,
                                                                         vol_exp_de_meses1['7'], 7, anno,
                                                                         lluvias_de_meses['7'])
                # else:
                #     nivel_pron_julio = {'50': None, '75': None, '95': None}
            elif nivel_pron_junio:
                nivel_pron_julio = self.calcular_niveles_pronosticos_mes(idd, nivel_pron_junio,
                                                                         vol_exp_de_meses1['7'], 7, anno,
                                                                         lluvias_de_meses['7'])
            res[2] = nivel_pron_julio
            # anno=anno
            date = datetime.datetime(anno, 8, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes8 = int(date_substr[0])
            nivel_agosto = self.calcular_nivel_real(idd, 8, anno)
            if (nivel_agosto or nivel_julio != None) and pronostico != 'puro':
                # if fecha_mes8 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 7:
                    nivel_pron_julio = {'50': nivel_julio, '75': nivel_julio, '95': nivel_julio}
                nivel_pron_agosto = self.calcular_niveles_pronosticos_mes(idd, nivel_pron_julio,
                                                                          vol_exp_de_meses1['8'], 8, anno,
                                                                          lluvias_de_meses['8'])
                # else:
                #     nivel_pron_agosto = {'50': None, '75': None, '95': None}
            elif nivel_pron_julio:
                nivel_pron_agosto = self.calcular_niveles_pronosticos_mes(idd, nivel_pron_julio,
                                                                          vol_exp_de_meses1['8'], 8, anno,
                                                                          lluvias_de_meses['8'])
            res[3] = nivel_pron_agosto
            # anno=anno
            date = datetime.datetime(anno, 9, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes9 = int(date_substr[0])
            nivel_septiembre = self.calcular_nivel_real(idd, 9, anno)
            if (nivel_septiembre or nivel_agosto != None) and pronostico != 'puro':
                # if fecha_mes9 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 8:
                    nivel_pron_agosto = {'50': nivel_agosto, '75': nivel_agosto, '95': nivel_agosto}
                nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes(idd, nivel_pron_agosto,
                                                                              vol_exp_de_meses1['9'], 9, anno,
                                                                              lluvias_de_meses['9'])
                # else:
                #     nivel_pron_septiembre = {'50': None, '75': None, '95': None}
            elif nivel_pron_agosto:
                nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes(idd, nivel_pron_agosto,
                                                                              vol_exp_de_meses1['9'], 9, anno,
                                                                              lluvias_de_meses['9'])
            res[4] = nivel_pron_septiembre
            # anno=anno
            date = datetime.datetime(anno, 10, 1)
            fecha_parte = date.strftime("%Y%m %H:%M:%S")
            date_substr = fecha_parte.split()
            fecha_mes10 = int(date_substr[0])
            nivel_octubre = self.calcular_nivel_real(idd, 10, anno)
            if (nivel_octubre or nivel_septiembre != None) and pronostico != 'puro':
                # if fecha_mes10 > fecha_actual:
                valor = meses1 + 1
                if cont != 1 and valor == 9:
                    nivel_pron_septiembre = {'50': nivel_septiembre, '75': nivel_septiembre, '95': nivel_septiembre}
                nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_septiembre,
                                                                           vol_exp_de_meses1['10'], 10, anno,
                                                                           lluvias_de_meses['10'])
                # else:
                #     nivel_pron_octubre = {'50': None, '75': None, '95': None}
            elif nivel_pron_septiembre:
                nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( idd, nivel_pron_septiembre,
                                                                           vol_exp_de_meses1['10'], 10, anno,
                                                                           lluvias_de_meses['10'])
            res[5] = nivel_pron_octubre
        else:
            #raise osv.except_osv(_('Advertencia'), _('Nivel de abril debe de existir para iniciar el pronóstico!'))
            raise UserError(_('Nivel de abril debe de existir para iniciar el pronóstico!'))

        obj = self.browse( [idd])[0]

        result = {
            'year': anno,
            'z': self.calcular_delta_z( idd, vol_exp_de_meses1['5']),
            'sigla': str(obj.sigla),
            'object': '',
            'categoryAxis': [],
            'yAxis': [{'minimo': 0, 'maximo': 1000, 'promedio_h_historico': 0}],
            'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 1000}],
            'series': [
                {'name': 'Nivel medido', 'data': [('May', self.calcular_nivel_real( idd, 5, anno)),
                                                  ('Jun', self.calcular_nivel_real( idd, 6, anno)),
                                                  ('Jul', self.calcular_nivel_real( idd, 7, anno)),
                                                  ('Agto', self.calcular_nivel_real( idd, 8, anno)),
                                                  ('Sep', self.calcular_nivel_real( idd, 9, anno)),
                                                  ('Oct', self.calcular_nivel_real( idd, 10, anno))]},
                {'name': 'Nivel lluvia real', 'data': [('May', nivel_lluvia_real['5']), ('Jun', nivel_lluvia_real['6']),
                                                       ('Jul', nivel_lluvia_real['7']), ('Ago', nivel_lluvia_real['8']),
                                                       ('Sep', nivel_lluvia_real['9']),
                                                       ('Oct', nivel_lluvia_real['10'])]},
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

    @api.model
    def calcular_niveles_pronosticos_reales1(self, id,  anno1, nreal, pronostico, abril, duracion, pozo_ids=None):  #trabaje aqui GJBL
        """ SEGUN SE LLENAN LOS REALES SE UTILIZA ESE VALOR EN EL MES CORRESPO,NDIENTE

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
        vol_exp_de_meses = self.calcular_explotacion_plan( id, anno1)
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
                {'name': 'Nivel lluvia 50%', 'data': []}, # 2
                {'name': 'Nivel lluvia 75%', 'data': []}, # 3
                {'name': 'Nivel lluvia 95%', 'data': []}, # 4
            ]
        }
        while cont < 2:
            if duracion == 'Y':
                if ok == True:
                    break
            fecha_str = time.strftime('%Y%m')
            fecha_actual = int(fecha_str)
            anno1 = anno1 + 1
            lluvias_de_meses = self.calcular_probabilidad( id)
            nivel_abril = abril[cont]
            nreal = self.formar_diccionario( id, anno1)
            nivel_lluvia_real = self.calcular_nivel_lluvia_real( id, nreal, vol_exp_de_meses, anno1)
            nivel_inicial_porcientos = {'50': nivel_abril, '75': nivel_abril, '95': nivel_abril}
            if nivel_abril:
                nivel_mayo = self.calcular_nivel_real( id, 5, anno1)
                anno = anno1
                date = datetime.datetime(anno, 5, 1)
                fecha_parte = date.strftime("%Y%m %H:%M:%S")
                date_substr = fecha_parte.split()
                fecha_mes5 = int(date_substr[0])
                if (nivel_mayo or nivel_abril != None) and pronostico != 'puro':
                # if fecha_mes5 > fecha_actual:
                    nivel_pron_mayo = self.calcular_niveles_pronosticos_mes( id, nivel_inicial_porcientos,
                                                                            vol_exp_de_meses['5'], 5, anno,
                                                                            lluvias_de_meses['5'])
                    # else:
                    #     nivel_pron_mayo = {'50': None, '75': None, '95': None}
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
                nivel_junio = self.calcular_nivel_real( id, 6, anno)
                if (nivel_junio or nivel_mayo != None) and pronostico != 'puro':
                # if fecha_mes6 > fecha_actual:
                    nivel_pron_mayo = {'50': nivel_mayo, '75': nivel_mayo, '95': nivel_mayo}
                    nivel_pron_junio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_mayo,
                                                                             vol_exp_de_meses['6'], 6, anno,
                                                                             lluvias_de_meses['6'])
                    # else:
                    #     nivel_pron_junio = {'50': None, '75': None, '95': None}
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
                nivel_julio = self.calcular_nivel_real( id, 7, anno)
                if (nivel_julio or nivel_junio != None) and pronostico != 'puro':
                # if fecha_mes7 > fecha_actual:
                    nivel_pron_junio = {'50': nivel_junio, '75': nivel_junio, '95': nivel_junio}
                    nivel_pron_julio = self.calcular_niveles_pronosticos_mes( id, nivel_pron_junio,
                                                                             vol_exp_de_meses['7'], 7, anno,
                                                                             lluvias_de_meses['7'])
                    # else:
                    #     nivel_pron_julio = {'50': None, '75': None, '95': None}
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
                nivel_agosto = self.calcular_nivel_real( id, 8, anno)
                if (nivel_agosto or nivel_julio != None) and pronostico != 'puro':
                # if fecha_mes8 > fecha_actual:
                    nivel_pron_julio = {'50': nivel_julio, '75': nivel_julio, '95': nivel_julio}
                    nivel_pron_agosto = self.calcular_niveles_pronosticos_mes( id, nivel_pron_julio,
                                                                              vol_exp_de_meses['8'], 8, anno,
                                                                              lluvias_de_meses['8'])
                    # else:
                    #     nivel_pron_agosto = {'50': None, '75': None, '95': None}
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
                nivel_septiembre = self.calcular_nivel_real( id, 9, anno)
                if (nivel_septiembre or nivel_agosto != None) and pronostico != 'puro':
                # if fecha_mes9 > fecha_actual:
                    nivel_pron_agosto = {'50': nivel_agosto, '75': nivel_agosto, '95': nivel_agosto}
                    nivel_pron_septiembre = self.calcular_niveles_pronosticos_mes( id, nivel_pron_agosto,
                                                                                  vol_exp_de_meses['9'], 9, anno,
                                                                                  lluvias_de_meses['9'])
                    # else:
                    #     nivel_pron_septiembre = {'50': None, '75': None, '95': None}
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
                nivel_octubre = self.calcular_nivel_real( id, 10, anno)
                if (nivel_octubre or nivel_septiembre != None) and pronostico != 'puro':
                # if fecha_mes10 > fecha_actual:
                    nivel_pron_septiembre = {'50': nivel_septiembre, '75': nivel_septiembre, '95': nivel_septiembre}
                    nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( id, nivel_pron_septiembre,
                                                                               vol_exp_de_meses['10'], 10, anno,
                                                                               lluvias_de_meses['10'])
                    # else:
                    #     nivel_pron_octubre = {'50': None, '75': None, '95': None}
                elif nivel_pron_septiembre:
                    nivel_pron_octubre = self.calcular_niveles_pronosticos_mes( id, nivel_pron_septiembre,
                                                                               vol_exp_de_meses['10'], 10, anno,
                                                                               lluvias_de_meses['10'])
                res[5] = nivel_pron_octubre
            else:
                #raise osv.except_osv(_('Advertencia'), _('Nivel de abril debe de existir para iniciar el pronóstico!'))
                raise UserError(_('Nivel de abril debe de existir para iniciar el pronóstico!'))
                # result = {
            #     'year': anno,
            #     'z': self.calcular_delta_z(cr, uid, id,  vol_exp_de_meses['5']),
            #     'sigla': str(obj.sigla),
            #     'object':'',
            #     'categoryAxis': [],
            #     'yAxis': [{'minimo':0,'maximo':1000,'promedio_h_historico':0}],
            #     'valueAxis': [{'title': 'hm³', 'min': 99999999, 'max': 1000}],
            #     # 'series': [
            #     #     {'name': 'Nivel medido', 'data': [('May.'+str(anno),self.calcular_nivel_real(cr, uid, id, 5, anno)),('Jun.'+str(anno),self.calcular_nivel_real(cr, uid, id, 6, anno)),('Jul.'+str(anno),self.calcular_nivel_real(cr, uid, id, 7, anno)),('Agto.'+str(anno),self.calcular_nivel_real(cr, uid, id, 8, anno)),('Sep.'+str(anno),self.calcular_nivel_real(cr, uid, id, 9, anno)),('Oct.'+str(anno),self.calcular_nivel_real(cr, uid, id, 10, anno))]},
            #     #     {'name': 'Nivel lluvia real', 'data': [('May',nivel_lluvia_real['5']),('Jun',nivel_lluvia_real['6']),('Jul',nivel_lluvia_real['7']),('Ago',nivel_lluvia_real['8']),('Sep',nivel_lluvia_real['9']),('Oct',nivel_lluvia_real['10'])]},
            #     #     {'name': 'Nivel lluvia 50%', 'data': [('May',res[0]['50']),('Jun',res[1]['50']),('Jul',res[2]['50']),('Ago',res[3]['50']),('Sep',res[4]['50']),('Oct',res[5]['50'])]},
            #     #     {'name': 'Nivel lluvia 75%', 'data': [('May',res[0]['75']),('Jun',res[1]['75']),('Jul',res[2]['75']),('Ago',res[3]['75']),('Sep',res[4]['75']),('Oct',res[5]['75'])]},
            #     #     {'name': 'Nivel lluvia 95%', 'data': [('May',res[0]['95']),('Jun',res[1]['95']),('Jul',res[2]['95']),('Ago',res[3]['95']),('Sep',res[4]['95']),('Oct',res[5]['95'])]},
            #     # ],
            #     'series': [
            #           {'name': 'Nivel medido', 'data': []},
            #           {'name': 'Nivel lluvia real', 'data': []},
            #           {'name': 'Nivel lluvia 50%', 'data': []},  # 2
            #           {'name': 'Nivel lluvia 75%', 'data': []},  # 3
            #           {'name': 'Nivel lluvia 95%', 'data': []},  # 4
            #     ]
            #     }
            result['series'][0]['data'].append(['May.' + str(anno), self.calcular_nivel_real( id, 5, anno)])
            result['series'][0]['data'].append(['Jun.' + str(anno), self.calcular_nivel_real( id, 6, anno)])
            result['series'][0]['data'].append(['Jul.' + str(anno), self.calcular_nivel_real( id, 7, anno)])
            result['series'][0]['data'].append(['Agto.' + str(anno), self.calcular_nivel_real( id, 8, anno)])
            result['series'][0]['data'].append(['Sep.' + str(anno), self.calcular_nivel_real( id, 9, anno)])
            result['series'][0]['data'].append(['Oct.' + str(anno), self.calcular_nivel_real( id, 10, anno)])
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
        # append('Nov.' + str(year))

    @api.model
    def create(self, vals):  #trabaje aqui GJBL
       if vals.get('coeficiente_almacenamiento', None):
           vals.update({'coeficiente_almacenamiento_string': str(vals['coeficiente_almacenamiento'])})
       if vals['ubicado'] == 'basin':
           vals['sector_hidrologico_id'] = False
           vals['bloque_id'] = False
       if vals['ubicado'] == 'sector':
           vals['cuenca_subterranea_id'] = False
           vals['bloque_id'] = False
       if vals['ubicado'] == 'block':
           vals['cuenca_subterranea_id'] = False
           vals['sector_hidrologico_id'] = False
       if vals['sector_hidrologico_id'] != False or vals['bloque_id'] != False or vals[
           'cuenca_subterranea_id'] != False:
           return super(df_pozo, self).create(vals)
       else:
           raise UserError(('Error !'), ('Debe de seleccionar el sector hidrológico,bloque,o cuenca al que pertenece el pozo'))
           #return super(df_pozo, self).create( vals)

    @api.multi
    def write(self, vals):  #trabaje aqui GJBL
        if vals.get('coeficiente_almacenamiento', None):
            vals.update({'coeficiente_almacenamiento_string': str(vals['coeficiente_almacenamiento'])})
        cuenca_obj = self.env['df.cuenca.subterranea']
        sector_obj = self.env['df.sector.hidrologico']
        bloque_obj = self.env['df.bloque']
        pozo_obj = self.env['df.pozo']
        # if  vals.get('sector_hidrologico_id'):
        #     if vals['sector_hidrologico_id'] == False:
        #         raise osv.except_osv(('Error !'), ('Debe de seleccionar el sector hidrológico o bloque al que pertenece el pozo'))
        # if vals.get('bloque_id'):
        #     if vals['bloque_id'] == False:
        #         raise osv.except_osv(('Error !'), ('Debe de seleccionar el sector hidrológico o bloque al que pertenece el pozo'))
        if (vals.get('ubicado',None) and vals['ubicado'] == 'sector'):
            vals['bloque_id'] = ''
            vals['cuenca_subterranea_id'] = ''
        if (vals.get('ubicado',None) and vals['ubicado'] == 'block'):
            vals['sector_hidrologico_id'] = ''
            vals['cuenca_subterranea_id'] = ''
        if (vals.get('ubicado') and vals['ubicado'] == 'basin'):
            vals['bloque_id'] = ''
            vals['sector_hidrologico_id'] = ''
        super(df_pozo, self).write(vals)
        if vals.get('representativo', None) or vals.get('valor_precision', None) or vals.get('recurso_explotable', None):
            ok = True
            # pozo_obj.obtener_promedio_alturas( ok)
            # bloque_obj.obtener_promedio_alturas( ok)
            # bloque_obj.obtener_promedio_alturas_formula( ok)
            # sector_obj.obtener_promedio_alturas( ok)
            # sector_obj.obtener_promedio_alturas_formula( ok)
            # cuenca_obj.obtener_promedio_alturas( ok)
            # cuenca_obj.obtener_promedio_alturas_formula( ok)
        return True

    @api.model
    def get_country_state(self):
        cuba_id = self.env.ref('base.cu').id
        provincia_data = self.env['res.country.state'].search([('country_id', '=', cuba_id)])
        prov_res = []
        for prov in provincia_data:
            prov_res.append({'value': prov.id, 'text': prov.name})
        return prov_res

    @api.model
    def get_municipios(self, state_id):
        municipio_list = self.env['df.municipality'].search([('state_id', '=', state_id)], order='name')

        nombres_municipio = []
        for mun in municipio_list:
            nombres_municipio.append({'value': mun.id, 'text': mun.name})
        return nombres_municipio

    def get_nivel_per_tup(self, nivel_obj, mes):
        """
        :param nivel_obj: objeto del modelo df.nivel.anual.pozo
        :param mes:
        :return: Retorna el nivel y periodo registrados del objeto, retorna -1 en caso de no haber sido
        registrado (nivel de -999999.11)
        """
        if mes == 12:
            if nivel_obj.media_hiperanual_diciembre != -999999.11:
                return nivel_obj.media_hiperanual_diciembre, mes, nivel_obj.anno
            mes -= 1
        if mes == 11:
            if nivel_obj.media_hiperanual_noviembre != -999999.11:
                return nivel_obj.media_hiperanual_noviembre, mes, nivel_obj.anno
            mes -= 1
        if mes == 10:
            if nivel_obj.media_hiperanual_octubre != -999999.11:
                return nivel_obj.media_hiperanual_octubre, mes, nivel_obj.anno
            mes -= 1
        if mes == 9:
            if nivel_obj.media_hiperanual_septiembre != -999999.11:
                return nivel_obj.media_hiperanual_septiembre, mes, nivel_obj.anno
            mes -= 1
        if mes == 8:
            if nivel_obj.media_hiperanual_agosto != -999999.11:
                return nivel_obj.media_hiperanual_agosto, mes, nivel_obj.anno
            mes -= 1
        if mes == 7:
            if nivel_obj.media_hiperanual_julio != -999999.11:
                return nivel_obj.media_hiperanual_julio, mes, nivel_obj.anno
            mes -= 1
        if mes == 6:
            if nivel_obj.media_hiperanual_junio != -999999.11:
                return nivel_obj.media_hiperanual_junio, mes, nivel_obj.anno
            mes -= 1
        if mes == 5:
            if nivel_obj.media_hiperanual_mayo != -999999.11:
                return nivel_obj.media_hiperanual_mayo, mes, nivel_obj.anno
            mes -= 1
        if mes == 4:
            if nivel_obj.media_hiperanual_abril != - 999999.11:
                return nivel_obj.media_hiperanual_abril, mes, nivel_obj.anno
            mes -= 1
        if mes == 3:
            if nivel_obj.media_hiperanual_marzo != -999999.11:
                return nivel_obj.media_hiperanual_marzo, mes, nivel_obj.anno
        if mes == 2:
            if nivel_obj.media_hiperanual_febrero != -999999.11:
                return nivel_obj.media_hiperanual_febrero, mes, nivel_obj.anno
            mes -= 1
        else:
            if nivel_obj.media_hiperanual_enero != -999999.11:
                return nivel_obj.media_hiperanual_enero, mes, nivel_obj.anno
        return -1

    def calcular_nivel_actual_pozos(self, pozo_ids, mes, anno):
        """
        :param pozo_ids:
        :param mes:
        :param anno:
        :return: una tupla con el último nivel y el mes/año en que fue registrado
        """
        res_dict = {}
        mes_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio',
                    8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
        nivel_anual_model = self.env['df.nivel.anual.pozo']

        for nivel_obj in nivel_anual_model.search([('pozo_id', 'in', pozo_ids), ('anno', '<=', anno)],
                                                 order='anno DESC'):
            if res_dict.get(nivel_obj.pozo_id.id) is not None:
                continue
            elif nivel_obj.anno == anno:
                nivel_tup = self.get_nivel_per_tup(nivel_obj, mes)
            else:
                nivel_tup = self.get_nivel_per_tup(nivel_obj, 12)
            if nivel_tup != -1:
                res_dict[nivel_obj.pozo_id.id] = nivel_tup[0], '%s/%s' % (mes_dict[nivel_tup[1]], nivel_tup[2])
        return res_dict

    @api.model
    def get_ubicacion_pozos_mapa(self, prov_id=-1, mun_id=-1):

        import math

        def get_color_estado(estado):
            return {'favorable': 'green', 'crítico': 'red', 'desfavorable': 'orange', 'muy favorable': 'lime',
                    'no hay nivel': 'blue', 'muy desfavorable': 'violet'}[estado]

        cond = [('coordenadas', '!=', False)]
        result = {'pozos': {}, 'prov_code': None,
                  'estado_desc_series': {'favorable': 'Favorable', 'crítico': 'Crítico', 'desfavorable': 'Desfavorable',
                                         'muy favorable': 'Muy favorable', 'no hay nivel': 'No hay nivel',
                                         'muy desfavorable': 'Muy desfavorable',
                                         },
                  'estado_color': {'favorable': 'green', 'crítico': 'red', 'desfavorable': 'orange',
                                   'muy favorable': 'lime', 'no hay nivel': 'blue', 'muy desfavorable': 'violet'}
                  }
        if (prov_id != -1 or mun_id != -1):
            prov_id = int(prov_id) if isinstance(prov_id, (str)) else prov_id
            result['prov_code'] = self.env['res.country.state'].browse(prov_id).code
        if prov_id != -1 and mun_id == -1:
            cond.append(('state_id', '=', prov_id))
        elif mun_id != -1:
            mun_id = int(mun_id) if isinstance(mun_id, (str)) else mun_id
            result['mun_code'] = self.env['df.municipality'].browse(mun_id).code
            cond.append(('municipality_id', '=', mun_id))

        pozos_list = self.search(cond)

        # date_ = datetime.datetime.strptime(fecha, "%d/%m/%Y")
        date_ = datetime.date.today()
        nivel_actual_dict = self.calcular_nivel_actual_pozos(pozos_list.ids, date_.month, date_.year)
        for pozo in pozos_list:
            if pozo.coordenadas == 'north':
                if pozo.este == 0 or pozo.norte == 0:
                    continue
                long_plana = pozo.este
                lat_plana = pozo.norte
                dist_N_S = 1
            else:
                if pozo.este1 == 0 or pozo.norte1 == 0:
                    continue
                long_plana = pozo.este1
                lat_plana = pozo.norte1
                dist_N_S = 0
            long_ = long_plana * pow(10, (5 - math.floor(math.log(long_plana, 10))))
            lat_ = lat_plana * pow(10, (5 - math.floor(math.log(lat_plana, 10))))
            coord_dec = df_hc_gis.tranf_2_coord_dec_cuba(long_, lat_, dist_N_S)
            nivel_tup = nivel_actual_dict.get(pozo.id)
            # Versión inicial
            # result['pozos'].append({'sigla': pozo.sigla, 'lat': coord_dec[1], 'lon': coord_dec[0],
            #                         'name': (': ' + pozo.nombre) if pozo.nombre else '',
            #                         'lonp': long_plana, 'latp': lat_plana,
            #                         'nivel': nivel_tup[0] if nivel_tup else "No registrado",
            #                         'periodo': nivel_tup[1] if nivel_tup else "No registrado",
            #                         'estado': pozo.estado, 'color_estado': get_color_estado(pozo.estado),
            #                         })
            color = get_color_estado(pozo.estado)
            if not result['pozos'].get(pozo.estado):
                result['pozos'][pozo.estado] = []
            result['pozos'][pozo.estado].append({'sigla': pozo.sigla, 'lat': coord_dec[1], 'lon': coord_dec[0],
                                                 'name': (': ' + pozo.nombre) if pozo.nombre else '',
                                                 'lonp': long_plana, 'latp': lat_plana,
                                                 'nivel': nivel_tup[0] if nivel_tup else "No registrado",
                                                 'periodo': nivel_tup[1] if nivel_tup else "No registrado",
                                                 'estado': result['estado_desc_series'][pozo.estado],
                                                 'color_estado': color,
                                                 'color': color,
                                                 })
        return result

    @api.model
    def get_estado_actual_prov(self):

        cuba_id = self.env.ref('base.cu').id
        provincia_list = self.env['res.country.state'].search([('country_id', '=', cuba_id)])
        prov_id_code_dict = {}
        for prov_obj in provincia_list:
            prov_id_code_dict[prov_obj.id] = prov_obj.code

        result = {'desfavorable': [], 'favorable': [], 'crítico': [], 'muy desfavorable': [],
                  'muy favorable': [],
                  'no hay nivel': []}

        prov_code_keymap_dict = {
            '21': 'cu-pri', '22': 'cu-art', '23': 'cu-hab', '24': 'cu-may', '25': 'cu-mtz', '26': 'cu-vcl',
            '27': 'cu-cfg', '28': 'cu-ssp', '29': 'cu-cav', '30': 'cu-cmg', '31': 'cu-ltu', '32': 'cu-hol',
            '33': 'cu-gra', '34': 'cu-scu', '35': 'cu-gtm', '40': 'cu-ijv'
        }

        prov_estado_list = self.env['df.report.provincia.cuenca'].search([])
        if not prov_estado_list:
            result['no hay nivel'] = [val for val in prov_code_keymap_dict.values()]
        for prov_cuenca in prov_estado_list:
            result[prov_cuenca.estado].append(prov_code_keymap_dict[prov_id_code_dict[prov_cuenca.id]])

        return result
