# -*- coding: utf-8 -*-
try:
    import json
except ImportError:
    import simplejson as json

try:
    import xlwt
except ImportError:
    xlwt = None

from xlwt import *
from odoo.modules import module
from odoo import http, _
from odoo.http import request, route
import os
import re


class df_hc_exportar_niveles(http.Controller):

    def obtener_niveles(self, pozo):
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
        request.env.cr.execute(sql)
        datos_vistas = request.env.cr.fetchall()
        return datos_vistas


    @http.route('/web/export/xls_levels_view', type='http', auth="user")
    def index(self, data, token):
        values = json.loads(data)
        model = values.get('model', "")
        ids = values.get('ids', [])
        pozo_obj = request.env[model]
        existe=0
        wb = xlwt.Workbook()
        style = xlwt.easyxf('font: name Arial, colour black, bold on;'
                            'pattern: pattern solid, fore_colour light_blue;'
                            'align: vertical center, horizontal center;'
                            'border: left thick, top thick,right thick')
        style1 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                             'align: vertical center, horizontal center;'
                             'border: left thick, top thick,right thick')
        encabezados=[u'Año','Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sept','Oct','Nov','Dic']
        pozos = pozo_obj.browse(ids)
        for pozo in pozos:
            fila=2
            columna=0
            fila_axu=1
            columna_aux=0
            datos_vistas = self.obtener_niveles(cr,pozo.id)
            if datos_vistas:
                ws = wb.add_sheet(pozo.sigla,cell_overwrite_ok=True)
                for datos_vista in datos_vistas:
                    if existe==0:
                        for encabezado in encabezados:
                            ws.write(fila_axu, columna_aux,encabezado,style)
                            columna_aux+=1
                        fila_axu+=1
                        columna_aux=0
                        existe=1
                    for valor in datos_vista:
                        if valor ==-999999.110:
                            ws.write(fila, columna,None,style1)
                        else:
                            ws.write(fila, columna,valor,style1)
                        columna+=1
                    fila+=1
                    columna=0
                existe=0
        path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp', 'niveles.xlsx')
        wb.save(path)
        nombre='Niveles por pozos' + '.xls'
        return request.make_response(open(path, 'rb'),
                             headers=[('Content-Disposition', 'attachment; filename="%s"' % nombre),
                                      ('Content-Type', 'application/vnd.ms-excel')],
                             cookies={'fileToken': token})

class df_hc_exportar_explotacion(http.Controller):
    def obtener_explotacion(self, pozo):
        sql = """ select df_plan_explotacion_anual_pozo.anno,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_enero) as plan_enero,
                            (df_explotacion_anual_pozo.media_hiperanual_enero) as real_enero,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_febrero) as plan_febrero,
                            (df_explotacion_anual_pozo.media_hiperanual_febrero) as real_febrero,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_marzo) as plan_marzo,
                            (df_explotacion_anual_pozo.media_hiperanual_marzo) as real_marzo,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_abril) as plan_abril,
                            (df_explotacion_anual_pozo.media_hiperanual_abril) as real_abril,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_mayo) as plan_mayo,
                            (df_explotacion_anual_pozo.media_hiperanual_mayo) as real_mayo,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_junio) as plan_junio,
                            (df_explotacion_anual_pozo.media_hiperanual_junio) as real_junio,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_julio) as plan_julio,
                            (df_explotacion_anual_pozo.media_hiperanual_julio) as real_julio,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_agosto) as plan_agosto,
                            (df_explotacion_anual_pozo.media_hiperanual_agosto) as real_agosto,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_septiembre) as plan_septiembre,
                            (df_explotacion_anual_pozo.media_hiperanual_septiembre) as septiembre,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_octubre) as plan_octubre,
                            (df_explotacion_anual_pozo.media_hiperanual_octubre) as real_octubre,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_noviembre) as plan_noviembre,
                            (df_explotacion_anual_pozo.media_hiperanual_noviembre) as real_noviembre,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_diciembre) as plan_diciembre,
                            (df_explotacion_anual_pozo.media_hiperanual_diciembre) as real_diciembre
                    from public.df_plan_explotacion_anual_pozo,public.df_explotacion_anual_pozo
                    where df_plan_explotacion_anual_pozo.anno = df_explotacion_anual_pozo.anno and
                           df_plan_explotacion_anual_pozo.pozo_id = df_explotacion_anual_pozo.pozo_id and
                           df_plan_explotacion_anual_pozo.pozo_id ='""" + str(pozo) + """'
                    GROUP BY df_plan_explotacion_anual_pozo.anno,
                           df_plan_explotacion_anual_pozo.media_hiperanual_enero,
                           df_explotacion_anual_pozo.media_hiperanual_enero,
                           df_plan_explotacion_anual_pozo.media_hiperanual_febrero,
                           df_explotacion_anual_pozo.media_hiperanual_febrero,
                           df_plan_explotacion_anual_pozo.media_hiperanual_marzo,
                           df_explotacion_anual_pozo.media_hiperanual_marzo,
                           df_plan_explotacion_anual_pozo.media_hiperanual_abril,
                           df_explotacion_anual_pozo.media_hiperanual_abril,
                           df_plan_explotacion_anual_pozo.media_hiperanual_mayo,
                           df_explotacion_anual_pozo.media_hiperanual_mayo,
                           df_plan_explotacion_anual_pozo.media_hiperanual_junio,
                           df_explotacion_anual_pozo.media_hiperanual_junio,
                           df_plan_explotacion_anual_pozo.media_hiperanual_julio,
                           df_explotacion_anual_pozo.media_hiperanual_julio,
                           df_plan_explotacion_anual_pozo.media_hiperanual_agosto,
                           df_explotacion_anual_pozo.media_hiperanual_agosto,
                           df_plan_explotacion_anual_pozo.media_hiperanual_septiembre,
                           df_explotacion_anual_pozo.media_hiperanual_septiembre,
                           df_plan_explotacion_anual_pozo.media_hiperanual_octubre,
                           df_explotacion_anual_pozo.media_hiperanual_octubre,
                           df_plan_explotacion_anual_pozo.media_hiperanual_noviembre,
                           df_explotacion_anual_pozo.media_hiperanual_noviembre,
                           df_plan_explotacion_anual_pozo.media_hiperanual_diciembre,
                           df_explotacion_anual_pozo.media_hiperanual_diciembre
                    ORDER BY anno ASC;"""
        request.env.cr.execute(sql)
        datos_vistas = request.env.cr.fetchall()
        return datos_vistas

    @http.route('/web/export/xls_exploitation_view', type='http', auth="user")
    def index(self, data, token):
        values = json.loads(data)
        model = values.get('model', "")
        ids = values.get('ids', [])
        pozo_obj = request.env[model]
        existe=0
        existe1=0
        wb = xlwt.Workbook()
        style = xlwt.easyxf('font: name Arial, colour black, bold on;'
                            'pattern: pattern solid, fore_colour red ;'
                            'align: vertical center, horizontal center;'
                            )
        style1 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                             'align: vertical center, horizontal center;'
                             'border: left thick, top thick,right thick')
        style2 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                            'pattern: pattern solid, fore_colour light_blue;'
                            'align: vertical center, horizontal center;'
                            'border: left thick, top thick,right thick')
        encabezados=['Ene',' ','Feb',' ','Mar',' ','Abr',' ','May',' ','Jun',' ','Jul',' ','Ago',' ','Sept',' ','Oct',' ','Nov',' ','Dic',' ',]
        encabezados1=[u'Año','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real']
        pozos = pozo_obj.browse(ids)
        for pozo in pozos:
            fila=3
            columna=0
            fila_axu=1
            columna_aux=1
            fila_axu1=2
            columna_aux1=0
            datos_vistas = self.obtener_explotacion(pozo.id)
            if datos_vistas:
                ws = wb.add_sheet(pozo.sigla,cell_overwrite_ok=True)
                for datos_vista in datos_vistas:
                    if existe1==0:
                        for encabezado1 in encabezados1:
                            ws.write(fila_axu1, columna_aux1,encabezado1,style2)
                            columna_aux1+=1
                        fila_axu1+=1
                        columna_aux1=0
                        existe1=1
                    if existe==0:
                        for encabezado in encabezados:
                            ws.write(fila_axu, columna_aux,encabezado,style)
                            columna_aux+=1
                        fila_axu+=1
                        columna_aux=0
                        existe=1
                    for valor in datos_vista:
                        if valor ==-999999.110:
                            ws.write(fila, columna,None,style1)
                        else:
                            ws.write(fila, columna,valor,style1)
                        columna+=1
                    fila+=1
                    columna=0
                existe=0
                existe1=0
        path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp', u'explotación.xlsx')
        wb.save(path)
        nombre='Explotación por pozos' + '.xls'
        return request.make_response(open(path, 'rb'),
                                 headers=[('Content-Disposition', 'attachment; filename="%s"' % nombre),
                                          ('Content-Type', 'application/vnd.ms-excel')],
                                 cookies={'fileToken': token})

class df_hc_exportar_gcbas(http.Controller):
    def obtener_niveles(self, pozo):
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
        request.env.cr.execute(sql)
        datos_vistas = request.env.cr.fetchall()
        return datos_vistas

    @http.route(['/web/export/xls_gcbas_view'], type='http', auth="user")
    def index(self, data, token):
        values = json.loads(data)
        cant = values['html'].count('tr')
        cant_filas=cant/2
        var='html'
        cont=2
        totales=[]
        encabezados=[u'Año',u'∆h',u'∆zh',u'∆zs',u'∆H',u'∆Z']
        while cont <= cant_filas - 2:
            aux =-1
            lista=str((values['html'].split('<tr>')[cont])).replace('</tr>','').replace('</td>','').replace('</tbody>','').split('<td>')
            clave_temp = lista
            temp=clave_temp[0].replace('td','').replace('class="tabla_cuerpo"' ,'').replace('<',' ').split(' >')
            for var in temp:
                if var == ' ':
                    aux += 1
                    break
                else:
                    aux += 1
            temp.pop(aux)
            totales.append(temp)
            cont+= 1
        ini = int(cant_filas - 1)
        fin = int(cant_filas)
        promedioss = []
        while ini <=  fin:
            pph = ((values['html'].split('<tr>')[ini])).replace('</tr>','').replace('</td>','').replace('</tbody>','').split('<td>')
            pph1 = pph[0].replace('td','').replace('class="tabla_cuerpo"' ,'').replace('<','').replace('>','').replace('class="tabla_sumario" b=""','').replace('style="color:white;mso-themecolor:background1"','').replace('span','').split('/')
            promedioss.append(pph1)
            ini += 1
        wb = xlwt.Workbook()
        style = xlwt.easyxf('font: name Arial, colour blue, bold on')
        style = xlwt.easyxf('font: name Arial, colour black, bold on;'
                            'pattern: pattern solid, fore_colour light_blue;'
                            'align: vertical center, horizontal center;'
                            'border: left thick, top thick,right thick')
        style1 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                             'align: vertical center, horizontal center;'
                             'border: left thick, top thick,right thick')
        fila=0
        columna=0
        ws = wb.add_sheet('GCBAS',cell_overwrite_ok=True)
        for encabezado in encabezados:
            ws.write(fila, columna,encabezado,style)
            columna+=1
        fila+=1
        for total in totales:
            columna=0
            for tot in total:
                if tot ==' ':
                    ws.write(fila, columna,None,style1)
                else:
                    ws.write(fila, columna,tot,style1)
                    columna+=1
            fila+=1

        for prom in promedioss:
            columna = 0
            for cl in prom:
                if cl != '':
                    ws.write(fila, columna, cl, style1)
                    columna += 1
            fila += 1

        path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp', 'GCBAS.xlsx')
        wb.save(path)
        nombre='GCBAS' + '.xls'
        return request.make_response(open(path, 'rb'),
                                 headers=[('Content-Disposition', 'attachment; filename="%s"' % nombre),
                                          ('Content-Type', 'application/vnd.ms-excel')],
                                  cookies={'fileToken': token})


class df_hc_exportar_recorridos(http.Controller):
    def obtener_niveles(self, pozo):
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
        request.env.cr.execute(sql)
        datos_vistas = request.env.cr.fetchall()
        return datos_vistas

    @http.route('/web/export/xls_recorridos_view', type='http', auth="user")
    def index(self, data, token):
        values = json.loads(data)
        cant = values['html'].count('tr')
        cant_filas=cant/2
        var='html'
        cont=2
        totales=[]
        encabezados=[' ','Recorrido 1',' ',' ','Recorrido 2',' ']
        while cont <= cant_filas:
            aux =-1
            lista=str((values['html'].split('<tr>')[cont])).replace('</tr>','').replace('</td>','').replace('</tbody>','').split('<td>')
            clave_temp = lista
            if cont==2:
                temp=clave_temp[0].replace('td','').replace('class="tabla_2da_cabezera"' ,'').replace('<',' ').split(' >')
            else:
                temp=clave_temp[0].replace('td','').replace('class="tabla_2da_cabezera"' ,'').replace('class="tabla_cuerpo"' ,'').replace('<',' ').split(' >')
            for var in temp:
                if var == ' ':
                    aux += 1
                    break
                else:
                    aux += 1
            temp.pop(aux)
            totales.append(temp)
            cont+= 1
        wb = xlwt.Workbook()
        style = xlwt.easyxf('font: name Arial, colour blue, bold on')
        style = xlwt.easyxf('font: name Arial, colour black, bold on;'
                            'pattern: pattern solid, fore_colour light_blue;'
                            'align: vertical center, horizontal center;'
                            'border: left thick, top thick,right thick')
        style1 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                             'align: vertical center, horizontal center;'
                             'border: left thick, top thick,right thick')
        fila=0
        columna=0
        ws = wb.add_sheet('GCBAS',cell_overwrite_ok=True)
        for encabezado in encabezados:
            ws.write(fila, columna,encabezado,style)
            columna+=1
        fila+=1
        for total in totales:
            columna=0
            for tot in total:
                if tot =='':
                    ws.write(fila, columna,None,style1)
                else:
                    ws.write(fila, columna,tot,style1)
                    columna+=1
            fila+=1
        path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp', 'GCBAS.xlsx')
        wb.save(path)
        nombre='GCBAS' + '.xls'
        return request.make_response(open(path, 'rb'),
                                 headers=[('Content-Disposition', 'attachment; filename="%s"' % nombre),
                                          ('Content-Type', 'application/vnd.ms-excel')],
                                 cookies={'fileToken': token})
class df_hc_exportar_explotacion_cuencas(http.Controller):
    def obtener_explotacion(self, pozo):
        sql = """ select df_plan_explotacion_anual_pozo.anno,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_enero) as plan_enero,
                            (df_explotacion_anual_pozo.media_hiperanual_enero) as real_enero,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_febrero) as plan_febrero,
                            (df_explotacion_anual_pozo.media_hiperanual_febrero) as real_febrero,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_marzo) as plan_marzo,
                            (df_explotacion_anual_pozo.media_hiperanual_marzo) as real_marzo,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_abril) as plan_abril,
                            (df_explotacion_anual_pozo.media_hiperanual_abril) as real_abril,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_mayo) as plan_mayo,
                            (df_explotacion_anual_pozo.media_hiperanual_mayo) as real_mayo,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_junio) as plan_junio,
                            (df_explotacion_anual_pozo.media_hiperanual_junio) as real_junio,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_julio) as plan_julio,
                            (df_explotacion_anual_pozo.media_hiperanual_julio) as real_julio,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_agosto) as plan_agosto,
                            (df_explotacion_anual_pozo.media_hiperanual_agosto) as real_agosto,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_septiembre) as plan_septiembre,
                            (df_explotacion_anual_pozo.media_hiperanual_septiembre) as septiembre,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_octubre) as plan_octubre,
                            (df_explotacion_anual_pozo.media_hiperanual_octubre) as real_octubre,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_noviembre) as plan_noviembre,
                            (df_explotacion_anual_pozo.media_hiperanual_noviembre) as real_noviembre,
                            (df_plan_explotacion_anual_pozo.media_hiperanual_diciembre) as plan_diciembre,
                            (df_explotacion_anual_pozo.media_hiperanual_diciembre) as real_diciembre
                    from public.df_plan_explotacion_anual_pozo,public.df_explotacion_anual_pozo
                    where df_plan_explotacion_anual_pozo.anno = df_explotacion_anual_pozo.anno and
                           df_plan_explotacion_anual_pozo.pozo_id = df_explotacion_anual_pozo.pozo_id and
                           df_plan_explotacion_anual_pozo.pozo_id ='""" + str(pozo) + """'
                    GROUP BY df_plan_explotacion_anual_pozo.anno,
                           df_plan_explotacion_anual_pozo.media_hiperanual_enero,
                           df_explotacion_anual_pozo.media_hiperanual_enero,
                           df_plan_explotacion_anual_pozo.media_hiperanual_febrero,
                           df_explotacion_anual_pozo.media_hiperanual_febrero,
                           df_plan_explotacion_anual_pozo.media_hiperanual_marzo,
                           df_explotacion_anual_pozo.media_hiperanual_marzo,
                           df_plan_explotacion_anual_pozo.media_hiperanual_abril,
                           df_explotacion_anual_pozo.media_hiperanual_abril,
                           df_plan_explotacion_anual_pozo.media_hiperanual_mayo,
                           df_explotacion_anual_pozo.media_hiperanual_mayo,
                           df_plan_explotacion_anual_pozo.media_hiperanual_junio,
                           df_explotacion_anual_pozo.media_hiperanual_junio,
                           df_plan_explotacion_anual_pozo.media_hiperanual_julio,
                           df_explotacion_anual_pozo.media_hiperanual_julio,
                           df_plan_explotacion_anual_pozo.media_hiperanual_agosto,
                           df_explotacion_anual_pozo.media_hiperanual_agosto,
                           df_plan_explotacion_anual_pozo.media_hiperanual_septiembre,
                           df_explotacion_anual_pozo.media_hiperanual_septiembre,
                           df_plan_explotacion_anual_pozo.media_hiperanual_octubre,
                           df_explotacion_anual_pozo.media_hiperanual_octubre,
                           df_plan_explotacion_anual_pozo.media_hiperanual_noviembre,
                           df_explotacion_anual_pozo.media_hiperanual_noviembre,
                           df_plan_explotacion_anual_pozo.media_hiperanual_diciembre,
                           df_explotacion_anual_pozo.media_hiperanual_diciembre
                    ORDER BY anno ASC;"""
        request.env.cr.execute(sql)
        datos_vistas = request.env.cr.fetchall()
        return datos_vistas
    def obtener_explotacion_cuenca(self, cuenca):
        sql = """ select df_explotacion_cuenca_plan.anno,
                            (df_explotacion_cuenca_plan.media_hiperanual_enero) as plan_enero,
                            (df_explotacion_cuenca_real.media_hiperanual_enero) as real_enero,
                            (df_explotacion_cuenca_plan.media_hiperanual_febrero) as plan_febrero,
                            (df_explotacion_cuenca_real.media_hiperanual_febrero) as real_febrero,
                            (df_explotacion_cuenca_plan.media_hiperanual_marzo) as plan_marzo,
                            (df_explotacion_cuenca_real.media_hiperanual_marzo) as real_marzo,
                            (df_explotacion_cuenca_plan.media_hiperanual_abril) as plan_abril,
                            (df_explotacion_cuenca_real.media_hiperanual_abril) as real_abril,
                            (df_explotacion_cuenca_plan.media_hiperanual_mayo) as plan_mayo,
                            (df_explotacion_cuenca_real.media_hiperanual_mayo) as real_mayo,
                            (df_explotacion_cuenca_plan.media_hiperanual_junio) as plan_junio,
                            (df_explotacion_cuenca_real.media_hiperanual_junio) as real_junio,
                            (df_explotacion_cuenca_plan.media_hiperanual_julio) as plan_julio,
                            (df_explotacion_cuenca_real.media_hiperanual_julio) as real_julio,
                            (df_explotacion_cuenca_plan.media_hiperanual_agosto) as plan_agosto,
                            (df_explotacion_cuenca_real.media_hiperanual_agosto) as real_agosto,
                            (df_explotacion_cuenca_plan.media_hiperanual_septiembre) as plan_septiembre,
                            (df_explotacion_cuenca_real.media_hiperanual_septiembre) as septiembre,
                            (df_explotacion_cuenca_plan.media_hiperanual_octubre) as plan_octubre,
                            (df_explotacion_cuenca_real.media_hiperanual_octubre) as real_octubre,
                            (df_explotacion_cuenca_plan.media_hiperanual_noviembre) as plan_noviembre,
                            (df_explotacion_cuenca_real.media_hiperanual_noviembre) as real_noviembre,
                            (df_explotacion_cuenca_plan.media_hiperanual_diciembre) as plan_diciembre,
                            (df_explotacion_cuenca_real.media_hiperanual_diciembre) as real_diciembre
                    from public.df_explotacion_cuenca_plan,public.df_explotacion_cuenca_real
                    where df_explotacion_cuenca_plan.anno = df_explotacion_cuenca_real.anno and
                           df_explotacion_cuenca_plan.cuenca_id = df_explotacion_cuenca_real.cuenca_id and
                           df_explotacion_cuenca_plan.cuenca_id ='""" + str(cuenca) + """'
                    GROUP BY df_explotacion_cuenca_plan.anno,
			                df_explotacion_cuenca_plan.media_hiperanual_enero,
                            df_explotacion_cuenca_real.media_hiperanual_enero,
                            df_explotacion_cuenca_plan.media_hiperanual_febrero,
                            df_explotacion_cuenca_real.media_hiperanual_febrero,
                            df_explotacion_cuenca_plan.media_hiperanual_marzo,
                            df_explotacion_cuenca_real.media_hiperanual_marzo,
                            df_explotacion_cuenca_plan.media_hiperanual_abril,
                            df_explotacion_cuenca_real.media_hiperanual_abril,
                            df_explotacion_cuenca_plan.media_hiperanual_mayo,
                            df_explotacion_cuenca_real.media_hiperanual_mayo,
                            df_explotacion_cuenca_plan.media_hiperanual_junio,
                            df_explotacion_cuenca_real.media_hiperanual_junio,
                            df_explotacion_cuenca_plan.media_hiperanual_julio,
                            df_explotacion_cuenca_real.media_hiperanual_julio,
                            df_explotacion_cuenca_plan.media_hiperanual_agosto,
                            df_explotacion_cuenca_real.media_hiperanual_agosto,
                            df_explotacion_cuenca_plan.media_hiperanual_septiembre,
                            df_explotacion_cuenca_real.media_hiperanual_septiembre,
                            df_explotacion_cuenca_plan.media_hiperanual_octubre,
                            df_explotacion_cuenca_real.media_hiperanual_octubre,
                            df_explotacion_cuenca_plan.media_hiperanual_noviembre,
                            df_explotacion_cuenca_real.media_hiperanual_noviembre,
                            df_explotacion_cuenca_plan.media_hiperanual_diciembre,
                            df_explotacion_cuenca_real.media_hiperanual_diciembre
                    ORDER BY anno ASC;"""
        request.env.cr.execute(sql)
        datos_vistas = request.env.cr.fetchall()
        return datos_vistas
    def obtener_explotacion_sector(self, sector):
        sql = """ select df_explotacion_sector_plan.anno,
                            (df_explotacion_sector_plan.media_hiperanual_enero) as plan_enero,
                            (df_explotacion_sector_real.media_hiperanual_enero) as real_enero,
                            (df_explotacion_sector_plan.media_hiperanual_febrero) as plan_febrero,
                            (df_explotacion_sector_real.media_hiperanual_febrero) as real_febrero,
                            (df_explotacion_sector_plan.media_hiperanual_marzo) as plan_marzo,
                            (df_explotacion_sector_real.media_hiperanual_marzo) as real_marzo,
                            (df_explotacion_sector_plan.media_hiperanual_abril) as plan_abril,
                            (df_explotacion_sector_real.media_hiperanual_abril) as real_abril,
                            (df_explotacion_sector_plan.media_hiperanual_mayo) as plan_mayo,
                            (df_explotacion_sector_real.media_hiperanual_mayo) as real_mayo,
                            (df_explotacion_sector_plan.media_hiperanual_junio) as plan_junio,
                            (df_explotacion_sector_real.media_hiperanual_junio) as real_junio,
                            (df_explotacion_sector_plan.media_hiperanual_julio) as plan_julio,
                            (df_explotacion_sector_real.media_hiperanual_julio) as real_julio,
                            (df_explotacion_sector_plan.media_hiperanual_agosto) as plan_agosto,
                            (df_explotacion_sector_real.media_hiperanual_agosto) as real_agosto,
                            (df_explotacion_sector_plan.media_hiperanual_septiembre) as plan_septiembre,
                            (df_explotacion_sector_real.media_hiperanual_septiembre) as septiembre,
                            (df_explotacion_sector_plan.media_hiperanual_octubre) as plan_octubre,
                            (df_explotacion_sector_real.media_hiperanual_octubre) as real_octubre,
                            (df_explotacion_sector_plan.media_hiperanual_noviembre) as plan_noviembre,
                            (df_explotacion_sector_real.media_hiperanual_noviembre) as real_noviembre,
                            (df_explotacion_sector_plan.media_hiperanual_diciembre) as plan_diciembre,
                            (df_explotacion_sector_real.media_hiperanual_diciembre) as real_diciembre
                    from public.df_explotacion_sector_plan,public.df_explotacion_sector_real
                    where df_explotacion_sector_plan.anno = df_explotacion_sector_real.anno and
                           df_explotacion_sector_plan.sector_id = df_explotacion_sector_real.sector_id and
                           df_explotacion_sector_plan.sector_id ='""" + str(sector) + """'
                    GROUP BY df_explotacion_sector_plan.anno,
			                df_explotacion_sector_plan.media_hiperanual_enero,
                            df_explotacion_sector_real.media_hiperanual_enero,
                            df_explotacion_sector_plan.media_hiperanual_febrero,
                            df_explotacion_sector_real.media_hiperanual_febrero,
                            df_explotacion_sector_plan.media_hiperanual_marzo,
                            df_explotacion_sector_real.media_hiperanual_marzo,
                            df_explotacion_sector_plan.media_hiperanual_abril,
                            df_explotacion_sector_real.media_hiperanual_abril,
                            df_explotacion_sector_plan.media_hiperanual_mayo,
                            df_explotacion_sector_real.media_hiperanual_mayo,
                            df_explotacion_sector_plan.media_hiperanual_junio,
                            df_explotacion_sector_real.media_hiperanual_junio,
                            df_explotacion_sector_plan.media_hiperanual_julio,
                            df_explotacion_sector_real.media_hiperanual_julio,
                            df_explotacion_sector_plan.media_hiperanual_agosto,
                            df_explotacion_sector_real.media_hiperanual_agosto,
                            df_explotacion_sector_plan.media_hiperanual_septiembre,
                            df_explotacion_sector_real.media_hiperanual_septiembre,
                            df_explotacion_sector_plan.media_hiperanual_octubre,
                            df_explotacion_sector_real.media_hiperanual_octubre,
                            df_explotacion_sector_plan.media_hiperanual_noviembre,
                            df_explotacion_sector_real.media_hiperanual_noviembre,
                            df_explotacion_sector_plan.media_hiperanual_diciembre,
                            df_explotacion_sector_real.media_hiperanual_diciembre
                    ORDER BY anno ASC;"""
        request.env.cr.execute(sql)
        datos_vistas = request.env.cr.fetchall()
        return datos_vistas
    def obtener_explotacion_bloque(self, bloque):
        sql = """ select df_explotacion_bloque_plan.anno,
                            (df_explotacion_bloque_plan.media_hiperanual_enero) as plan_enero,
                            (df_explotacion_bloque_real.media_hiperanual_enero) as real_enero,
                            (df_explotacion_bloque_plan.media_hiperanual_febrero) as plan_febrero,
                            (df_explotacion_bloque_real.media_hiperanual_febrero) as real_febrero,
                            (df_explotacion_bloque_plan.media_hiperanual_marzo) as plan_marzo,
                            (df_explotacion_bloque_real.media_hiperanual_marzo) as real_marzo,
                            (df_explotacion_bloque_plan.media_hiperanual_abril) as plan_abril,
                            (df_explotacion_bloque_real.media_hiperanual_abril) as real_abril,
                            (df_explotacion_bloque_plan.media_hiperanual_mayo) as plan_mayo,
                            (df_explotacion_bloque_real.media_hiperanual_mayo) as real_mayo,
                            (df_explotacion_bloque_plan.media_hiperanual_junio) as plan_junio,
                            (df_explotacion_bloque_real.media_hiperanual_junio) as real_junio,
                            (df_explotacion_bloque_plan.media_hiperanual_julio) as plan_julio,
                            (df_explotacion_bloque_real.media_hiperanual_julio) as real_julio,
                            (df_explotacion_bloque_plan.media_hiperanual_agosto) as plan_agosto,
                            (df_explotacion_bloque_real.media_hiperanual_agosto) as real_agosto,
                            (df_explotacion_bloque_plan.media_hiperanual_septiembre) as plan_septiembre,
                            (df_explotacion_bloque_real.media_hiperanual_septiembre) as septiembre,
                            (df_explotacion_bloque_plan.media_hiperanual_octubre) as plan_octubre,
                            (df_explotacion_bloque_real.media_hiperanual_octubre) as real_octubre,
                            (df_explotacion_bloque_plan.media_hiperanual_noviembre) as plan_noviembre,
                            (df_explotacion_bloque_real.media_hiperanual_noviembre) as real_noviembre,
                            (df_explotacion_bloque_plan.media_hiperanual_diciembre) as plan_diciembre,
                            (df_explotacion_bloque_real.media_hiperanual_diciembre) as real_diciembre
                    from public.df_explotacion_bloque_plan,public.df_explotacion_bloque_real
                    where df_explotacion_bloque_plan.anno = df_explotacion_bloque_real.anno and
                           df_explotacion_bloque_plan.bloque_id = df_explotacion_bloque_real.bloque_id and
                           df_explotacion_bloque_plan.bloque_id ='""" + str(bloque) + """'
                    GROUP BY df_explotacion_bloque_plan.anno,
			                df_explotacion_bloque_plan.media_hiperanual_enero,
                            df_explotacion_bloque_real.media_hiperanual_enero,
                            df_explotacion_bloque_plan.media_hiperanual_febrero,
                            df_explotacion_bloque_real.media_hiperanual_febrero,
                            df_explotacion_bloque_plan.media_hiperanual_marzo,
                            df_explotacion_bloque_real.media_hiperanual_marzo,
                            df_explotacion_bloque_plan.media_hiperanual_abril,
                            df_explotacion_bloque_real.media_hiperanual_abril,
                            df_explotacion_bloque_plan.media_hiperanual_mayo,
                            df_explotacion_bloque_real.media_hiperanual_mayo,
                            df_explotacion_bloque_plan.media_hiperanual_junio,
                            df_explotacion_bloque_real.media_hiperanual_junio,
                            df_explotacion_bloque_plan.media_hiperanual_julio,
                            df_explotacion_bloque_real.media_hiperanual_julio,
                            df_explotacion_bloque_plan.media_hiperanual_agosto,
                            df_explotacion_bloque_real.media_hiperanual_agosto,
                            df_explotacion_bloque_plan.media_hiperanual_septiembre,
                            df_explotacion_bloque_real.media_hiperanual_septiembre,
                            df_explotacion_bloque_plan.media_hiperanual_octubre,
                            df_explotacion_bloque_real.media_hiperanual_octubre,
                            df_explotacion_bloque_plan.media_hiperanual_noviembre,
                            df_explotacion_bloque_real.media_hiperanual_noviembre,
                            df_explotacion_bloque_plan.media_hiperanual_diciembre,
                            df_explotacion_bloque_real.media_hiperanual_diciembre
                    ORDER BY anno ASC;"""
        request.env.cr.execute(sql)
        datos_vistas = request.env.cr.fetchall()
        return datos_vistas

    @http.route('/web/export/xls_exploitation_cuencas_view', type='http', auth="user")
    def index(self, data, token):
        values = json.loads(data)
        model = str(values.get('model', ""))
        ids = values.get('ids', [])
        model_manager = request.env[model]
        existe=0
        existe1=0
        wb = xlwt.Workbook()
        style = xlwt.easyxf('font: name Arial, colour black, bold on;'
                            'pattern: pattern solid, fore_colour red ;'
                            'align: vertical center, horizontal center;'
                            )
        style1 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                             'align: vertical center, horizontal center;'
                             'border: left thick, top thick,right thick')
        style2 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                            'pattern: pattern solid, fore_colour light_blue;'
                            'align: vertical center, horizontal center;'
                            'border: left thick, top thick,right thick')
        encabezados=['Ene',' ','Feb',' ','Mar',' ','Abr',' ','May',' ','Jun',' ','Jul',' ','Ago',' ','Sept',' ','Oct',' ','Nov',' ','Dic',' ',]
        encabezados1=[u'Año','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real','Plan','Real']
        model_managers = model_manager.browse(ids)
        for model_manager in model_managers:
            fila=3
            columna=0
            fila_axu=1
            columna_aux=1
            fila_axu1=2
            columna_aux1=0
            if model=='df.pozo':
                datos_vistas = self.obtener_explotacion(model_manager.id)
                ws = wb.add_sheet(model_manager.sigla,cell_overwrite_ok=True)
            if model=='df.bloque':
                datos_vistas = self.obtener_explotacion_bloque(model_manager.id)
                ws = wb.add_sheet(model_manager.sigla,cell_overwrite_ok=True)
            if model=='df.sector.hidrologico':
                datos_vistas = self.obtener_explotacion_sector(model_manager.id)
                ws = wb.add_sheet(model_manager.sigla,cell_overwrite_ok=True)
            if model=='df.cuenca.subterranea':
                datos_vistas = self.obtener_explotacion_cuenca(model_manager.id)
                ws = wb.add_sheet(model_manager.nombre,cell_overwrite_ok=True)
            if datos_vistas:
                for datos_vista in datos_vistas:
                    if existe1==0:
                        for encabezado1 in encabezados1:
                            ws.write(fila_axu1, columna_aux1,encabezado1,style2)
                            columna_aux1+=1
                        fila_axu1+=1
                        columna_aux1=0
                        existe1=1
                    if existe==0:
                        for encabezado in encabezados:
                            ws.write(fila_axu, columna_aux,encabezado,style)
                            columna_aux+=1
                        fila_axu+=1
                        columna_aux=0
                        existe=1
                    for valor in datos_vista:
                        if valor ==-999999.110:
                            ws.write(fila, columna,None,style1)
                        else:
                            ws.write(fila, columna,valor,style1)
                        columna+=1
                    fila+=1
                    columna=0
                existe=0
                existe1=0
        path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp', u'explotación.xlsx')
        wb.save(path)
        titulo=['Explotación de pozos' + '.xls','Explotación de bloques' + '.xls','Explotación de sectores' + '.xls','Explotación de cuencas' + '.xls']
        if model=='df.pozo':
           nombre=titulo[0]
        if model=='df.bloque':
           nombre=titulo[1]
        if model=='df.sector.hidrologico':
           nombre=titulo[2]
        if model=='df.cuenca.subterranea':
           nombre=titulo[3]
        return request.make_response(open(path, 'rb'),
                                 headers=[('Content-Disposition', 'attachment; filename="%s"' % nombre),
                                          ('Content-Type', 'application/vnd.ms-excel')],
                                 cookies={'fileToken': token})
class df_hc_exportar_pozos(http.Controller):
    def obtener_pozos(self, pozo):
        tabla_agrupamiento = 'df_pozo'
        sql = """ select (nombre)as nombre,
                          (sigla)as sigla,
                          (bloque_id)as bloque,
                          (sector_hidrologico_id)as sector,
                          (cuenca_subterranea_id)as cuenca,
                          (norte)as norte,
                          (este)as este,
                          (diametro)as diametro,
                          (profundidad_total)as profundidad,
                          (cota_topografica)as cota,
                          (ubicado)as ubicado
                    from public.""" + tabla_agrupamiento + """ AS tabla_objeto
                    where tabla_objeto.id = '""" + str(pozo) + """'"""
        request.env.cr.execute(sql)
        datos_vistas = request.env.cr.dictfetchall()
        return datos_vistas

    @http.route('/web/export/xls_pozos_view', type='http', auth="user")
    def index(self, data, token):
        values = json.loads(data)
        model = values.get('model', "")
        ids = values.get('ids', [])
        pozo_obj = request.env[model]
        existe=0
        wb = xlwt.Workbook()
        style = xlwt.easyxf('font: name Arial, colour black, bold on;'
                            'pattern: pattern solid, fore_colour light_blue;'
                            'align: vertical center, horizontal center;'
                            'border: left thick, top thick,right thick')
        style1 = xlwt.easyxf('font: name Arial, colour black, bold on;'
                             'align: vertical center, horizontal center;'
                             'border: left thick, top thick,right thick')
        encabezados=['Nombre','Sigla',u'Ubicación','Coordenadas norte','Coordenadas este',u'Diámetro','Profundidad','Cota']
        pozos = pozo_obj.browse(ids)
        ws = wb.add_sheet('pozos',cell_overwrite_ok=True)
        fila_axu=0
        columna_aux=0
        for pozo in pozos:
            datos_vistas = self.obtener_pozos(pozo.id)
            if datos_vistas:
                for datos_vista in datos_vistas:
                    if existe==0:
                        for encabezado in encabezados:
                            ws.write(fila_axu, columna_aux,encabezado,style)
                            columna_aux+=1
                        fila_axu+=1
                        columna_aux=0
                        existe=1
                    if datos_vista['ubicado'] == 'block':
                        obj = pooler.get_pool(cr.dbname).get('df.bloque')
                        bloque_id=obj.search([('id', '=', datos_vista['bloque'])])
                        ubicado_obj = obj.browse(bloque_id)
                        ubicado=ubicado_obj[0].sigla
                    elif datos_vista['ubicado'] == 'sector':
                        obj = pooler.get_pool(cr.dbname).get('df.sector.hidrologico')
                        sector_id=obj.search([('id', '=', datos_vista['sector'])])
                        ubicado_obj = obj.browse(sector_id)
                        ubicado=ubicado_obj[0].sigla
                    elif datos_vista['ubicado'] == 'basin':
                        obj = pooler.get_pool(cr.dbname).get('df.cuenca.subterranea')
                        cuenca_id=obj.search([('id', '=', datos_vista['cuenca'])])
                        ubicado_obj = obj.browse(cuenca_id)
                        ubicado=ubicado_obj[0].codigo
                    nombre=datos_vista['nombre']
                    ws.write(fila_axu, columna_aux,nombre,style1)
                    columna_aux+=1
                    sigla=datos_vista['sigla']
                    ws.write(fila_axu, columna_aux,sigla,style1)
                    columna_aux+=1
                    ws.write(fila_axu, columna_aux,ubicado,style1)
                    columna_aux+=1
                    norte=datos_vista['norte']
                    ws.write(fila_axu, columna_aux,norte,style1)
                    columna_aux+=1
                    este=datos_vista['este']
                    ws.write(fila_axu, columna_aux,este,style1)
                    columna_aux+=1
                    diametro=datos_vista['diametro']
                    ws.write(fila_axu, columna_aux,diametro,style1)
                    columna_aux+=1
                    profundidad=datos_vista['profundidad']
                    ws.write(fila_axu, columna_aux,profundidad,style1)
                    columna_aux+=1
                    cota=datos_vista['cota']
                    ws.write(fila_axu, columna_aux,cota,style1)
                    fila_axu+=1
                    columna_aux=0
                existe=1
        path = os.path.join(module.get_module_path('df_hc_acuifero'), 'tmp', 'pozos.xlsx')
        wb.save(path)
        nombre='Pozos' + '.xls'
        return request.make_response(open(path, 'rb'),
                             headers=[('Content-Disposition', 'attachment; filename="%s"' % nombre),
                                      ('Content-Type', 'application/vnd.ms-excel')],
                             cookies={'fileToken': token})