odoo.define('df_hc_acuifero.gis', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var framework = require('web.framework');
    var session = require('web.session');
    var _t = core._t;
    var QWeb = core.qweb;

    var mapa_ubicacion_pozos = AbstractAction.extend({
        template: "df_hc_acuifero_mapa_ubicacion_pozos_view",

        init: function (parent, params) {
            this._super.apply(this, arguments)
            this.action_manager = parent;
            this.params = params;
        },

        start: function () {
            var self = this;
            self.$el.find("#td_prov").hide();
            self.$el.find("#td_mun").hide();

            var nivel = 0;
            var nivel_list = [
                {
                    'value': 0,
                    'text': 'Nacional'
                },
                {
                    'value': 1,
                    'text': 'Provincial'
                },
                {
                    'value': 2,
                    'text': 'Municipal'
                }
            ]
            var nivel_it;
            for (nivel_it of nivel_list) {
                this.$el.find('#cmb_nivel').append("<option value=" + nivel_it.value + ">" + nivel_it.text + "</option>");
            }

            var set_datasource_selection = function (model_name, method_name, selection_id, params_list = []) {
                self._rpc({
                    model: model_name,
                    method: method_name,
                    args: params_list
                }, []).then(function (result) {
                    self.$el.find(selection_id).empty()
                    $.each(result, function (index) {
                        self.$el.find(selection_id).append("<option value=" + result[index]["value"] + ">" + result[index]["text"] + "</option>");
                    });
                }).done(function () {
                });
            }

            set_datasource_selection('df.pozo', 'get_country_state', "#cmb_province")

            self.$el.find("#cmb_nivel").bind("change", function () {
                if (self.$el.find("#cmb_nivel").val() == 0) {
                    self.$el.find("#td_prov").hide();
                    self.$el.find("#cmb_province").hide();
                    self.$el.find("#td_mun").hide();
                    self.$el.find("#cmb_municipio").hide();
                    nivel = 0;
                } else if (self.$el.find("#cmb_nivel").val() == 1) {
                    self.$el.find("#td_prov").show();
                    self.$el.find("#cmb_province").show();
                    self.$el.find("#td_mun").hide();
                    self.$el.find("#cmb_municipio").hide();
                    nivel = 1;
                } else {
                    self.$el.find("#td_prov").show();
                    self.$el.find("#cmb_province").show();
                    set_datasource_selection('df.pozo', 'get_municipios', "#cmb_municipio", [parseInt(self.$el.find("#cmb_province").val())])
                    self.$el.find("#td_mun").show();
                    self.$el.find("#cmb_municipio").show();
                    nivel = 2;
                }
            });

            self.$el.find("#cmb_province").bind("change", function () {
                if (self.$el.find("#cmb_nivel").val() == 2) {
                    set_datasource_selection('df.pozo', 'get_municipios', "#cmb_municipio", [parseInt(self.$el.find("#cmb_province").val())])
                    self.$el.find("#td_mun").show();
                    self.$el.find("#cmb_municipio").show()
                } else {
                    self.$el.find("#td_mun").hide();
                }
            });

            var get_code_map = function (nivel, prov_code, mun_code) {
                if (nivel == 0)
                    return 'cuba-provinces'
                else if (nivel == 1) {
                    return {
                        '21': 'cu/pinar_del_rio', '22': 'cu/artemisa', '23': 'cu/la_habana', '24': 'cu/mayabeque',
                        '25': 'cu/matanzas', '26': 'cu/villa_clara', '27': 'cu/cienfuegos', '28': 'cu/sancti_spiritus',
                        '29': 'cu/ciego_de_avila', '30': 'cu/camaguey', '31': 'cu/las_tunas', '32': 'cu/holguin',
                        '33': 'cu/granma', '34': 'cu/santiago_de_cuba', '35': 'cu/guantanamo', '40': 'cu/isla_juventud'
                    }[prov_code]
                } else {
                    return {
                        '35': {
                            '3501': 'cu/guantanamo/el_salvador',
                            '3502': 'cu/guantanamo/manuel_tames',
                            '3503': 'cu/guantanamo/yateras',
                            '3504': 'cu/guantanamo/baracoa',
                            '3505': 'cu/guantanamo/maisi',
                            '3506': 'cu/guantanamo/imias',
                            '3507': 'cu/guantanamo/san_antonio_del_sur',
                            '3508': 'cu/guantanamo/caimanera',
                            '3509': 'cu/guantanamo/guantanamo',
                            '3510': 'cu/guantanamo/niceto_perez',

                        },
                        '34': {
                            '3401': 'cu/santiago_de_cuba/contramaestre',
                            '3402': 'cu/santiago_de_cuba/mella',
                            '3403': 'cu/santiago_de_cuba/san_luis',
                            '3404': 'cu/santiago_de_cuba/segundo_frente',
                            '3405': 'cu/santiago_de_cuba/songo-la_maya',
                            '3406': 'cu/santiago_de_cuba/santiago_de_cuba',
                            '3407': 'cu/santiago_de_cuba/palma_soriano',
                            '3408': 'cu/santiago_de_cuba/tercer_frente',
                            '3409': 'cu/santiago_de_cuba/guama',
                        },
                        '33': {
                            '3301': 'cu/granma/rio_cauto',
                            '3302': 'cu/granma/cauto_cristo',
                            '3303': 'cu/granma/jiguani',
                            '3304': 'cu/granma/bayamo',
                            '3305': 'cu/granma/yara',
                            '3306': 'cu/granma/manzanillo',
                            '3307': 'cu/granma/campechuela',
                            '3308': 'cu/granma/media_luna',
                            '3309': 'cu/granma/niquero',
                            '3310': 'cu/granma/pilon',
                            '3311': 'cu/granma/bartolome_maso',
                            '3312': 'cu/granma/buey_arriba',
                            '3313': 'cu/granma/guisa',

                        },
                        '32': {
                            '3201': 'cu/holguin/gibara',
                            '3202': 'cu/holguin/rafael_freyre',
                            '3203': 'cu/holguin/banes',
                            '3204': 'cu/holguin/antilla',
                            '3205': 'cu/holguin/baguanos',
                            '3206': 'cu/holguin/holguin',
                            '3207': 'cu/holguin/calixto_garcia',
                            '3208': 'cu/holguin/cacocum',
                            '3209': 'cu/holguin/urbano_noris',
                            '3210': 'cu/holguin/cueto',
                            '3211': 'cu/holguin/mayari',
                            '3212': 'cu/holguin/frank_pais',
                            '3213': 'cu/holguin/sagua_de_tanamo',
                            '3214': 'cu/holguin/moa',
                        },
                        '31': {
                            '3101': 'cu/las_tunas/manati',
                            '3102': 'cu/las_tunas/puerto_padre',
                            '3103': 'cu/las_tunas/jesus_menendez',
                            '3104': 'cu/las_tunas/majibacoa',
                            '3105': 'cu/las_tunas/las_tunas',
                            '3106': 'cu/las_tunas/jobabo',
                            '3107': 'cu/las_tunas/colombia',
                            '3108': 'cu/las_tunas/amancio',
                        },
                        '30': {
                            '3001': 'cu/camaguey/carlos_manuel_de_cespedes',
                            '3002': 'cu/camaguey/esmeralda',
                            '3003': 'cu/camaguey/sierra_de_cubitas',
                            '3004': 'cu/camaguey/minas',
                            '3005': 'cu/camaguey/nuevitas',
                            '3006': 'cu/camaguey/guaimaro',
                            '3007': 'cu/camaguey/sibanicu',
                            '3008': 'cu/camaguey/camaguey',
                            '3009': 'cu/camaguey/florida',
                            '3010': 'cu/camaguey/vertientes',
                            '3011': 'cu/camaguey/jimaguayu',
                            '3012': 'cu/camaguey/najasa',
                            '3013': 'cu/camaguey/santa_cruz_del_sur',
                        },
                        '29': {
                            '2901': 'cu/ciego_de_avila/chambas',
                            '2902': 'cu/ciego_de_avila/moron',
                            '2903': 'cu/ciego_de_avila/bolivia',
                            '2904': 'cu/ciego_de_avila/primero_de_enero',
                            '2905': 'cu/ciego_de_avila/ciro_redondo',
                            '2906': 'cu/ciego_de_avila/florencia',
                            '2907': 'cu/ciego_de_avila/majagua',
                            '2908': 'cu/ciego_de_avila/ciego_de_avila',
                            '2909': 'cu/ciego_de_avila/venezuela',
                            '2910': 'cu/ciego_de_avila/baragua',
                        },
                        '28': {
                            '2801': 'cu/sancti_spiritus/yaguajay',
                            '2802': 'cu/sancti_spiritus/jatibonico',
                            '2803': 'cu/sancti_spiritus/taguasco',
                            '2804': 'cu/sancti_spiritus/cabaiguan',
                            '2805': 'cu/sancti_spiritus/fomento',
                            '2806': 'cu/sancti_spiritus/trinidad',
                            '2807': 'cu/sancti_spiritus/sancti_spiritus',
                            '2808': 'cu/sancti_spiritus/la_sierpe',
                        },
                        '27': {
                            '2701': 'cu/cienfuegos/aguada_de_pasajeros',
                            '2702': 'cu/cienfuegos/rodas',
                            '2703': 'cu/cienfuegos/palmira',
                            '2704': 'cu/cienfuegos/lajas',
                            '2705': 'cu/cienfuegos/cruces',
                            '2706': 'cu/cienfuegos/cumanayagua',
                            '2707': 'cu/cienfuegos/cienfuegos',
                            '2708': 'cu/cienfuegos/abreus',

                        },
                        '26': {
                            '2601': 'cu/villa_clara/corralillo',
                            '2602': 'cu/villa_clara/quemado_de_guines',
                            '2603': 'cu/villa_clara/sagua_la_grande',
                            '2604': 'cu/villa_clara/encrucijada',
                            '2605': 'cu/villa_clara/camajuani',
                            '2606': 'cu/villa_clara/caibarien',
                            '2607': 'cu/villa_clara/remedios',
                            '2608': 'cu/villa_clara/placetas',
                            '2609': 'cu/villa_clara/santa_clara',
                            '2610': 'cu/villa_clara/cifuentes',
                            '2611': 'cu/villa_clara/santo_domingo',
                            '2612': 'cu/villa_clara/ranchuelo',
                            '2613': 'cu/villa_clara/manicaragua',

                        },
                        '25': {
                            '2501': 'cu/matanzas/matanzas',
                            '2502': 'cu/matanzas/cardenas',
                            '2503': 'cu/matanzas/marti',
                            '2504': 'cu/matanzas/colon',
                            '2505': 'cu/matanzas/perico',
                            '2506': 'cu/matanzas/jovellanos',
                            '2507': 'cu/matanzas/pedro_betancourt',
                            '2508': 'cu/matanzas/limonar',
                            '2509': 'cu/matanzas/union_de_reyes',
                            '2510': 'cu/matanzas/cienaga_de_zapata',
                            '2511': 'cu/matanzas/jaguey_grande',
                            '2512': 'cu/matanzas/Calimete',
                            '2513': 'cu/matanzas/los_arabos'
                        },
                        '24': {
                            '2401': 'cu/mayabeque/bejucal',
                            '2402': 'cu/mayabeque/san_jose_de_las_lajas',
                            '2403': 'cu/mayabeque/jaruco',
                            '2404': 'cu/mayabeque/santa_cruz_del_norte',
                            '2405': 'cu/mayabeque/madruga',
                            '2406': 'cu/mayabeque/nueva_paz',
                            '2407': 'cu/mayabeque/san_nicolas',
                            '2408': 'cu/mayabeque/guines',
                            '2409': 'cu/mayabeque/melena_del_sur',
                            '2410': 'cu/mayabeque/batabano',
                            '2411': 'cu/mayabeque/quivican',
                        },
                        '23': {
                            '2301': 'cu/la_habana/playa',
                            '2302': 'cu/la_habana/plaza_de_la_revolucion',
                            '2303': 'cu/la_habana/centro_habana',
                            '2304': 'cu/la_habana/la_habana_vieja',
                            '2305': 'cu/la_habana/regla',
                            '2306': 'cu/la_habana/la_habana_del_este',
                            '2307': 'cu/la_habana/guanabacoa',
                            '2308': 'cu/la_habana/san_miguel_del_padron',
                            '2309': 'cu/la_habana/diez_de_octubre',
                            '2310': 'cu/la_habana/cerro',
                            '2311': 'cu/la_habana/marianao',
                            '2312': 'cu/la_habana/la_lisa',
                            '2313': 'cu/la_habana/boyeros',
                            '2314': 'cu/la_habana/arroyo_naranjo',
                            '2315': 'cu/la_habana/cotorro',
                        },
                        '22': {
                            '2201': 'cu/artemisa/bahia_honda',
                            '2202': 'cu/artemisa/mariel',
                            '2203': 'cu/artemisa/guanajay',
                            '2204': 'cu/artemisa/caimito',
                            '2205': 'cu/artemisa/bauta',
                            '2206': 'cu/artemisa/san_antonio',
                            '2207': 'cu/artemisa/guira_de_melena',
                            '2208': 'cu/artemisa/alquizar',
                            '2209': 'cu/artemisa/artemisa',
                            '2210': 'cu/artemisa/candelaria',
                            '2211': 'cu/artemisa/san_cristobal',
                        },
                        '21': {
                            '2101': 'cu/pinar_del_rio/sandino',
                            '2102': 'cu/pinar_del_rio/mantua',
                            '2103': 'cu/pinar_del_rio/minas_de_matahambre',
                            '2104': 'cu/pinar_del_rio/vinales',
                            '2105': 'cu/pinar_del_rio/la_palma',
                            '2106': 'cu/pinar_del_rio/los_palacios',
                            '2107': 'cu/pinar_del_rio/consolacion_del_sur',
                            '2108': 'cu/pinar_del_rio/pinar_del_rio',
                            '2109': 'cu/pinar_del_rio/san luis',
                            '2110': 'cu/pinar_del_rio/san_suan_y_martinez',
                            '2111': 'cu/pinar_del_rio/guane',
                        },
                        '40': {
                            '401': 'cu/isla_juventud'
                        }

                    }[prov_code][mun_code]
                }
            }

            var graficar = function (data_source, nivel, land_name) {
                var mapa_data = get_code_map(nivel, data_source['prov_code'], data_source['mun_code']);

                var series = [
                    {
                        name: 'Basemap',
                        borderColor: '#A0A0A0',
                        //nullColor: 'rgba(170,211,223, 0.5)',//azul marino
                        nullColor: 'rgba(99, 251, 28, 0.3)',//verde
                        showInLegend: false
                    },
                ]
                var estado;
                for (estado in data_source['pozos']) {
                    series.push(
                        {
                            // Specify points using lat/lon
                            type: 'mappoint',
                            name: data_source['estado_desc_series'][estado],
                            //color: Highcharts.getOptions().colors[2],
//                                color: 'rgb(51, 112, 204)',
                            color: data_source['estado_color'][estado],
                            data: data_source['pozos'][estado],
                            marker: {
                                //height:'24px',
                                //width:'24px',
                                symbol: 'diamond',
                                //symbol: 'url(/df_hc_base/static/src/img/redhidrogeol.png)'
                            },
                            dataLabels: {
                                enabled: true,
                                format: '{point.sigla}',
                                style: {
                                    width: '120px' // force line-wrap
                                }
                            }

                        }
                    )
                }


                // Initiate the chart
                var contenedor = self.$el.find("#div_mapa")[0];
                Highcharts.mapChart(contenedor, {

                    chart: {
                        map: mapa_data,
                        backgroundColor: {
                            linearGradient: [0, 0, 500, 500],
                            stops: [
                                [0, 'rgb(255, 255, 255)'],
                                [1, 'rgb(240, 240, 255)']
                            ]
                            //linearGradient: [0, 0, 500, 500],
                            //stops: [
                            //    [0, 'rgb(255, 255, 255)'],
                            //    [1, 'rgb(100, 210, 250)'],
                            //    [2, 'rgb(111, 214, 255)']
                            //]
                        },
                    },

                    title: {
                        text: 'Pozos ' + (nivel == 0 ? 'de ' : (nivel == 1 ? ' de la provincia ' : 'del municipio ')) + land_name
                    },
                    mapNavigation: {
                        enabled: true
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.75)',
                        animation: true,
                        borderWidth: 1,
                        shadow: false,
                        useHTML: true,
                        padding: 10,
                        pointFormat: '<span style="vertical-align: middle !important;"><span class="flag {point.properties.hc-key}">' +
                            '</span><b>{point.sigla}{point.name}</b></span><br>' +
                            '<span>Lat: {point.latp}, Lon: {point.lonp}</span><br>' +
                            '<span>Nivel: <b>{point.nivel}</b>, Periodo: <b>{point.periodo}</b></span><br>' +
                            '<span style="color:{point.color_estado}  !important;">Estado: <b>{point.estado}</b></span><br>',
                        //positioner: function () {
                        //    return {x: 780, y: 12};
                        //}
                    },
                    plotOptions: {
                        series: {
                            turboThreshold: 10000, //set it to a larger threshold, it is by default to 1000
                            stickyTracking: false
                        }
                    },

                    series: series,

                    exporting:
                        {
                            buttons: {
                                contextButton: {
                                    menuItems: [
                                        {
                                            text: _t('Imprimir mapa'),
                                            onclick: function () {
                                                this.print();
                                            }
                                        },
                                        {
                                            text: _t('Exportar a PNG'),
                                            onclick: function () {
                                                this.exportChartLocal();
                                            }
                                        },
                                        {
                                            text: _t('Exportar a PDF'),
                                            onclick: function () {
                                                // $('#div_mapa').highcharts().exportChartLocal('image/svg+xml');
                                                this.exportChartLocal({
                                                    type: 'application/pdf'
                                                });
                                            }
                                        }
                                    ]
                                }
                            }
                        },

                    // versión inicial en una sola serie
//                    series: [
//                        {
//                            name: 'Basemap',
//                            borderColor: '#A0A0A0',
//                            //nullColor: 'rgba(170,211,223, 0.5)',//azul marino
//                            nullColor: 'rgba(99, 251, 28, 0.3)',//verde
//                            showInLegend: false
//                        },
//                        {
//                            // Specify points using lat/lon
//                            type: 'mappoint',
//                            name: 'Pozos',
//                            //color: Highcharts.getOptions().colors[2],
//                            color: 'rgb(51, 112, 204)',
//                            data: data_source['pozos'],
//                            marker: {
//                                //height:'24px',
//                                //width:'24px',
//                                symbol: 'diamond',
//                                //symbol: 'url(/df_hc_base/static/src/img/redhidrogeol.png)'
//                            },
//                            dataLabels: {
//                                enabled: true,
//                                format: '{point.sigla}',
//                                style: {
//                                    width: '120px' // force line-wrap
//                                }
//                            }
//
//                        },
//
//
//                        {
//                            name: 'Separators',
//                            type: 'mapline',
//                            nullColor: '#707070',
//                            showInLegend: false,
//                            enableMouseTracking: false
//                        },
//
//                    ]
                });
            }

            self.$el.find("#btn_mostrar").bind("click", function () {
//                if ($("#cmb_province").val() == null || $("#cmb_province").val() == '')
//                    self.do_warn(_t("Note"), _t("Must be a hidraulic joint selected"));
//                else {
                var prov_id = -1;
                var mun_id = -1;
                var land_name = 'Cuba';
                if (nivel == 1) {
                    prov_id = self.$el.find("#cmb_province").val()
                    land_name = self.$el.find("#cmb_province option:selected").text()
                } else if (nivel == 2) {
                    prov_id = self.$el.find("#cmb_province").val()
                    mun_id = self.$el.find("#cmb_municipio").val()
                    land_name = self.$el.find("#cmb_municipio option:selected").text()
                }

                self._rpc({
                    model: 'df.pozo',
                    method: 'get_ubicacion_pozos_mapa',
                    args: [prov_id, mun_id]
                }, []).then(function (data_source) {
                    if ( Object.keys(data_source.pozos).length == 0) {
                        if (nivel == 0)
                            self.do_warn('Información', ("No existen pozos registrados en el sistema."));
                        else if (nivel == 1)
                            self.do_warn('Información', ("No existen pozos registrados para la provincia especificada."));
                        else
                            self.do_warn('Información', ("No existen pozos registrados para el municipio especificado."));
                    }

                    self.$el.find("#div_mapa").attr({'style': ' height: 650px'});
                    graficar(data_source, nivel, land_name);

                }).done(function () {
                });

            });

        }
    });

    var mapa_estado_actual_prov = AbstractAction.extend({
        template: "df_hc_acuifero_mapa_estado_actual_prov_view",

        init: function (parent, params) {
            this._super.apply(this, arguments)
            this.action_manager = parent;
            this.params = params;
            var self = this

            this._rpc({
                model: 'df.pozo',
                method: 'get_estado_actual_prov',
                args: []
            }, []).then(function (data_source) {
                var contenedor = self.$el.find("#div_mapa")[0];
                self.$el.find("#div_mapa").attr({'style': ' height: 650px'});
                Highcharts.mapChart(contenedor, {
                    chart: {
                        map: 'cuba-provinces',
                    },

                    title: {
                        text: 'Estado actual de las provincias'
                    },

                    legend: {
                        align: 'rigth',
                        //backgroundColor: 'rgba(100, 210, 250,0.8)',
                        floating: true,
                        layout: 'vertical',
                        verticalAlign: 'bottom',
                        reversed: true
                        // enabled: false,
                    },
                    mapNavigation: {
                        enabled: true,
                        buttonOptions: {
                            verticalAlign: 'top',
                            Alain: 'rigth'
                        }
                    },

                    plotOptions: {
                        map: {
                            allAreas: false,
                            joinBy: ['hc-key', 'code'],
                            dataLabels: {
                                enabled: true,
                                color: '#FFFFFF',
                                style: {
                                    fontWeight: 'bold'
                                },
                                // Only show dataLabels for areas with high label rank
                                format: null,
                                formatter: function () {
                                    return this.point.properties['postal-code'];
//                                    return this.point.name;
                                }
                            },
                            tooltip: {
                                headerFormat: '',
                                pointFormat: '{point.name}: <b>{series.name}</b>'
                            }
                        }
                    },
                    series: [
                        {
                            name: 'Crítico',
                            data: data_source['crítico'].map(function (code) {
                                return {code: code};
                            }),
                            color: 'red',
                            showInLegend: false
                        }, {
                            name: 'Desfavorable',
                            data: data_source['desfavorable'].map(function (code) {
                                return {code: code};
                            }),
                            color: 'orange',
                            showInLegend: false
                        },
                        {
                            name: 'Muy desfavorable',
                            data: data_source['muy desfavorable'].map(function (code) {
                                return {code: code};
                            }),
                            color: 'violet',
                            showInLegend: false
                        }, {
                            name: 'No hay nivel',
                            data: data_source['no hay nivel'].map(function (code) {
                                return {code: code};
                            }),
                            color: 'blue',
                            showInLegend: false
                        }, {
                            name: 'Favorable',
                            data: data_source['favorable'].map(function (code) {
                                return {code: code};
                            }),
                            color: 'green',
                            showInLegend: false
                        }

                    ],
                    exporting:
                        {
                            buttons: {
                                contextButton: {
                                    menuItems: [
                                        {
                                            text: _t('Imprimir mapa'),
                                            onclick: function () {
                                                this.print();
                                            }
                                        },
                                        {
                                            text: _t('Exportar a PNG'),
                                            onclick: function () {
                                                this.exportChartLocal();
                                            }
                                        },
                                        {
                                            text: _t('Exportar a PDF'),
                                            onclick: function () {
                                                // $('#div_mapa').highcharts().exportChartLocal('image/svg+xml');
                                                this.exportChartLocal({
                                                    type: 'application/pdf'
                                                });
                                            }
                                        }
                                    ]
                                }
                            }
                        },
                });
                $('#tr_estados').show();

            }).done(function () {
                // self.start()
            });

        },

        start: function () {
        }
    });

    core.action_registry.add('df_hc_acuifero_mapa_ubicacion_pozos', mapa_ubicacion_pozos);
    core.action_registry.add('df_hc_acuifero_mapa_estado_actual_prov', mapa_estado_actual_prov);
// return mapa_ubicacion_pozos;

})
;


