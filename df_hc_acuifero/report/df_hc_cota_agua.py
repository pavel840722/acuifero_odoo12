from odoo import api, models

class df_hc_cota_agua(models.AbstractModel):
    _name = 'report.df_hc_acuifero.parte_cota_agua_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        lista_obj = []
        d = {}

        result = []

        obj_s = self.browse(docids)
        for ob in obj_s:
            valores=self.env['df.report.cota.agua'].search([('id','=',ob.id)])
            datos = {}
            datos['sigla'] = valores['sigla']
            datos['anno'] = valores['anno']
            datos['enero'] = valores['cota_agua_enero'] if valores['cota_agua_enero']!=str(str(-999999.11)) else  ' '
            datos['febrero'] = valores['cota_agua_febrero']  if valores['cota_agua_febrero']!=str(-999999.11) else ' '
            datos['marzo'] = valores['cota_agua_marzo']  if valores['cota_agua_marzo']!=str(-999999.11) else ' '
            datos['abril'] = valores['cota_agua_abril']  if valores['cota_agua_abril']!=str(-999999.11) else ' '
            datos['mayo'] = valores['cota_agua_mayo']  if valores['cota_agua_mayo']!=str(-999999.11) else ' '
            datos['junio'] = valores['cota_agua_junio']  if valores['cota_agua_junio']!=str(-999999.11) else ' '
            datos['julio'] = valores['cota_agua_julio']  if valores['cota_agua_julio']!=str(-999999.11) else ' '
            datos['agosto'] = valores['cota_agua_agosto']  if valores['cota_agua_agosto']!=str(-999999.11) else ' '
            datos['septiembre'] = valores['cota_agua_septiembre']  if valores['cota_agua_septiembre']!=str(-999999.11) else ' '
            datos['octubre'] = valores['cota_agua_octubre']  if valores['cota_agua_octubre']!=str(-999999.11) else ' '
            datos['noviembre'] = valores['cota_agua_noviembre']  if valores['cota_agua_noviembre']!=str(-999999.11) else ' '
            datos['diciembre'] = valores['cota_agua_diciembre']  if valores['cota_agua_diciembre']!=str(-999999.11) else ' '
            result.append(datos)




        # d[0] = 's1'
        # d[1] = '2019'
        # d[2] = '1'
        # d[3] = '2'
        # d[4] = '3'
        # d[5] = '4'
        # d[6] = '5'
        # d[7] = '6'
        # d[8] = '7'
        # d[9] = '8'
        # d[10] = '9'
        # d[11] = '10'
        # d[12] = '11'
        # d[13] = '12'
        # d[14] = '13'
        # lista_obj.append(d)

        docargs = {
            'doc_ids': docids,
            #'doc_model': 'df.config.agrupacion',
            'docs': self,
            'lista': result,
            #'nombre_ueb': nombre_ueb,
            #'year': data['form']['year'],
            #'um_id_name': data['form']['um_id'][1],
            #'stated_id': data['form']['state_id'][1]
        }
        return docargs

