# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api


class df_report_cota_agua(models.Model):
    _name = 'df.report.cota.agua'
    _description = "Monhtly transfer data"
    _auto = False
    # _rec_name = 'sigla'

    sigla = fields.Char(string='Abbreviation', size=64, required=False)
    anno = fields.Integer(string='Year', required=False)
    pozo_id = fields.Many2one('df.pozo', string='Well', readonly=True)
    cota_agua_enero = fields.Char(string='January', size=64, required=False)
    cota_agua_febrero = fields.Char(string='February', size=64, required=False)
    cota_agua_marzo = fields.Char(string='March', size=64, required=False)
    cota_agua_abril = fields.Char(string='April', size=64, required=False)
    cota_agua_mayo = fields.Char(string='May', size=64, required=False)
    cota_agua_junio = fields.Char(string='June', size=64, required=False)
    cota_agua_julio = fields.Char(string='July', size=64, required=False)
    cota_agua_agosto = fields.Char(string='August', size=64, required=False)
    cota_agua_septiembre = fields.Char(string='September', size=64, required=False)
    cota_agua_octubre = fields.Char(string='October', size=64, required=False)
    cota_agua_noviembre = fields.Char(string='November', size=64, required=False)
    cota_agua_diciembre = fields.Char(string='December', size=64, required=False)

    @api.model_cr  # cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self._cr.execute("""
            create or replace view df_report_cota_agua as (
                    select
                         df_pozo.sigla as sigla,
                         df_nivel_anual_pozo.anno as anno,
                         df_nivel_anual_pozo.id as id,
                         df_pozo.id as pozo_id,
		                 CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_enero = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_enero)
			                END
                            as cota_agua_enero,
                         CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_febrero = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_febrero)
			                END
                            as cota_agua_febrero,
			            CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_marzo = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_marzo)
			                END
                            as cota_agua_marzo,
                        CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_abril = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_abril)
			                END
                            as cota_agua_abril,
                        CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_mayo = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_mayo)
			                END
                            as cota_agua_mayo,
                        CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_junio = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_junio)
			                END
                            as cota_agua_junio,
                        CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_julio = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_julio)
			                END
                            as cota_agua_julio,
                        CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_agosto = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_agosto)
			                END
                            as cota_agua_agosto,
                        CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_septiembre = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_septiembre)
			                END
                            as cota_agua_septiembre,
                        CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_octubre = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_octubre)
			                END
                            as cota_agua_octubre,
                        CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_noviembre = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_noviembre)
			                END
                            as cota_agua_noviembre,
                        CASE
			                WHEN df_nivel_anual_pozo.media_hiperanual_diciembre = -999999.110 THEN -999999.110
			                ELSE (df_pozo.cota_topografica-df_nivel_anual_pozo.media_hiperanual_diciembre)
			                END
                            as cota_agua_diciembre
		        from df_nivel_anual_pozo,df_pozo
		        where df_pozo.id = df_nivel_anual_pozo.pozo_id
		        group by df_pozo.sigla,df_pozo.id,df_nivel_anual_pozo.anno,df_nivel_anual_pozo.id,cota_agua_enero,cota_agua_febrero,cota_agua_marzo,cota_agua_abril,cota_agua_mayo,cota_agua_junio,cota_agua_julio,cota_agua_agosto,cota_agua_septiembre,cota_agua_octubre,cota_agua_noviembre,cota_agua_diciembre
		        order by df_pozo.sigla asc

            )""")

    @api.model
    def report_cota_agua(self,cota_agua_ids):
        return cota_agua_ids[0]

    # metodo para imprimir
    @api.multi
    def print_report(self):
        self.ensure_one()
        datas = {
            'ids': self.env.context.get('active_ids', []),
        }
        return self.env.ref('df_hc_acuifero.action_parte_cota_agua').report_action([], data=datas)

