# -*- coding: utf-8 -*-
{
    'name': "acuifero",

    'summary': """
       """,

    'description': """
           """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly

    'depends': ['base','df_hc_embalse','df_hc_rain_base'],

    # always loaded
    'data': [
        'security/df_hc_acuifero_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/df_cuenca_subterranea_inherit_view.xml',
        'views/df_pozo_view.xml',
        'views/df_nivel_anual_pozo_view.xml',
        'views/df_probabilidad_cuenca_view.xml',
        'views/df_probabilidad_sector_view.xml',
        'views/df_probabilidad_bloque_view.xml',
        'views/df_probabilidad_pozo_view.xml',
        #'views/df_zona_hidrografica_pluviometro_view.xml',
        #     # 'views/df_tramo_view.xml',
        'views/df_lluvia_real_pozo_view.xml',
        'views/df_lluvia_real_bloque_view.xml',
        'views/df_lluvia_real_sector_view.xml',
        'views/df_lluvia_real_cuenca_view.xml',
        'views/df_sector_hidrologico_view.xml',
        'views/df_bloque_view.xml',
        'views/df_explotacion_real_view.xml',
        'views/df_explotacion_anual_pozo_view.xml',
        'views/df_provincia_cuenca_view.xml',
        'views/df_exportar_media.xml',
        'views/df_graficos_acuifero.xml',
        'wizard/df_importar_pozos.xml',
        'wizard/df_importar_niveles_pozos.xml',
        'wizard/df_importar_explotacion.xml',
        'wizard/df_importar_probabilidad_lluvia.xml',
        'wizard/df_importar_lluvia_real.xml',
		'wizard/df_configurar_grafica_gcbas.xml',
		'wizard/df_configurar_grafica.xml',
		'wizard/df_configurar_grafica_pronostico.xml',
        'wizard/df_configurar_grafica_explotacion.xml',
		'wizard/df_configurar_grafica_recorridos.xml',
		'wizard/df_config_grafica_pronostico_seco.xml',
        'wizard/df_acuifero_integracion.xml',
		'report/df_report_cota_agua_view.xml',
        'report/report_view.xml',
        'report/df_hc_cota_agua.xml',
        'views/df_acuerifero_main_view.xml',
    ],
	# only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'application': True,
    'icon': "/df_hc_acuifero/static/src/img/icon.png",
}
