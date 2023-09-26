/*
    GRAFICO CGBAS
    PAVEL DANIEL LOPEZ CASTILLO
    2020
 */
odoo.define('df_hc_acuifero.grafico_acuifero', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var framework = require('web.framework');
    var session = require('web.session');


    var _t = core._t;
    var QWeb = core.qweb;

    //var lang = odoo.session_info.user_context.lang;
    //Highcharts.setOptions({
    //    lang: {
    //        rangeSelectorZoom: "Aumentar",
    //        resetZoom: 'Restablecer tamaño',
    //        contextButtonTitle: "Menu contextual",
    //        printChart: "Imprimir mapa",
    //        downloadPNG: "Descargar como PNG",
    //        downloadJPEG: "Descargar como JPEG",
    //        downloadPDF: "Descargar como PDF"
    //
    //
    //    }
    //});


    var grafico_acuifero = AbstractAction.extend({
        template: "df_hc_acuifero_grafico_acuifero_view",

        init: function (parent, context) {
            this._super(parent, context);
            var options = context.params || {};
            this.params = options;
        },

        start: function () {
            var self = this;

            var graficar = function (result) {
                self.grafico = Highcharts.chart('container', {
                    chart: {
                        height: 550,
                        zoomType: 'x',
                        spacingRight: 20,
                        type: 'spline'
                    },
                    scrollbar: {
                        enabled: true
                    },
                    title: {
                        text: _t("Underground hydraulic set limnigrama graphic") + ' ' + result['object']
                    },
                    subtitle: {
                        text: document.ontouchstart === undefined ?
                            _t('Click and drag in the plot area to zoom in') :
                            _t('Drag your finger over the plot to zoom in')
                    },
                    xAxis: {
                        type: 'datetime'
                    },
                    yAxis: {
                        max: result['yAxis'][0]['maximo'] + 1,
                        title: {
                            text: 'm'
                        },
                        reversed: true,
                        lineWidth: 2,
                        labels: {
                            style: {
                                fontWeight: 'bold',
                                fontSize: '13px'
                            }
                        },
                        plotBands: [
                            {
                                label: {
                                    style: {
                                        fontWeight: 'bold',
                                        fontSize: '15px'
                                    },
                                    text: 'EMF'
                                },
                                from: result['yAxis'][0]['minimo'],
                                to: result['yAxis'][0]['minimo'] + result['yAxis'][0]['promedio_h_historico'],
                                color: 'rgba(0, 255, 0, 0.1)'
                            },
                            {
                                label: {
                                    style: {
                                        fontWeight: 'bold',
                                        fontSize: '15px'
                                    },
                                    text: 'EF'
                                },
                                from: result['yAxis'][0]['minimo'] + result['yAxis'][0]['promedio_h_historico'],
                                to: result['yAxis'][0]['maximo'] - result['yAxis'][0]['promedio_h_historico'],
                                color: 'rgba(0, 0, 255, 0.1)'
                            },
                            {
                                label: {
                                    style: {
                                        fontWeight: 'bold',
                                        fontSize: '15px'
                                    },
                                    text: 'ED'
                                },
                                from: result['yAxis'][0]['maximo'] - result['yAxis'][0]['promedio_h_historico'],
                                to: result['yAxis'][0]['maximo'] - (result['yAxis'][0]['promedio_h_historico'] / 2),
                                color: 'rgba(255, 0, 0, 0.1)'
                            },
                            {
                                label: {
                                    style: {
                                        fontWeight: 'bold',
                                        fontSize: '15px'
                                    },
                                    text: 'EMD'
                                },
                                from: result['yAxis'][0]['maximo'] - (result['yAxis'][0]['promedio_h_historico'] / 2),
                                to: result['yAxis'][0]['maximo'],
                                color: 'rgba(255, 0, 0, 0.1)'
                            }
                        ]
                    },
                    tooltip: {
                        crosshairs: true,
                        shared: true,
                        valueSuffix: 'm',
                        xDateFormat: '%B %Y'
                    },
                    plotOptions: {
                        line: {
                            dataLabels: {
                                enabled: true
                            },
                            enableMouseTracking: false,
                            lineWidth: 3,
                            states: {
                                hover: {
                                    lineWidth: 4
                                }
                            },
                            marker: {
                                enabled: false
                            }
                        }
                    },

                    series: [
                        {
                            pointInterval: 24 * 3600 * 1000,
                            name: result['series'][0]['name'],
                            data: result['series'][0]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#083695',
                        },
                        {
                            pointInterval: 24 * 3600 * 1000,
                            name: result['series'][1]['name'],
                            data: result['series'][1]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#054e05',
                        },
                        {
                            name: result['series'][5]['name'],
                            data: result['series'][5]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#e5c700'
                        },
                        {
                            name: result['series'][4]['name'],
                            data: result['series'][4]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#dc00d4'

                        },
                        {
                            name: result['series'][12]['name'],
                            data: result['series'][12]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#ff0000'
                        },
                        {
                            type: 'line',
                            name: result['series'][6]['name'],
                            data: result['series'][6]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: 'rgba(255, 0, 0, 0.3)'
                            //color: '#FFB2B2'
                        },
//
                        {
                            name: result['series'][8]['name'],
                            data: result['series'][8]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            lineWidth: 1,
                            color: 'rgba(22, 200, 44, 1)',
                            visible: false,
                            enableMouseTracking: true
                        },
                        {
                            name: result['series'][9]['name'],
                            data: result['series'][9]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            lineWidth: 1,
                            color: 'rgba(255, 0, 0, 1)',
                            visible: false,
                            enableMouseTracking: true
                        },
                        {
                            type: 'line',
                            name: result['series'][10]['name'],
                            data: result['series'][10]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            lineWidth: 1,
                            color: '#000000',
                            visible: false,
                            enableMouseTracking: true
                        },
                        {
                            name: result['series'][13]['name'],
                            data: result['series'][13]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#ff0000'
                        },
                        {
                            name: result['series'][14]['name'],
                            data: result['series'][14]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#000000'
                        },
                        {
                            name: result['series'][15]['name'],
                            data: result['series'][15]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: 'brown'
                        },
                        {
                            name: result['series'][16]['name'],
                            data: result['series'][16]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: 'orange'
                        }
//
                    ],

                    exporting: {
                        buttons: {
                            contextButton: {
                                menuItems: [
                                    {
                                        text: _t('Imprimir Gr\u00E1fico'),
                                        onclick: function () {
                                            this.print();
                                        }
                                    },
                                    {
                                        text: _t('Descargar PNG'),
                                        onclick: function () {
                                            this.exportChartLocal({
                                                 filename: 'Gráfico GCBAS'
                                            });
                                        }
                                    },
                                    {
                                        text: _t('Descargar PDF'),
                                        onclick: function () {
                                            this.exportChartLocal({
                                                type: 'application/pdf',
                                                filename: 'Gráfico GCBAS'
                                            });
                                        }
                                    }
                                ]
                            }
                        }
                    }
                });
            }
            var hc_exportar_grafica = function () {

                var html = $("#tbl_resumen").html();
                $.blockUI()
                //framework.blockUI();
                session.get_file({
                    url: '/web/export/xls_gcbas_view',
                    data: {
                        data: JSON.stringify({
                            html: html,
                            name: _t("Underground hydraulic set limnigrama graphic")
                        })
                    },
                    complete: $.unblockUI
                });
            }

            ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                model: 'df.limnigrama.acuifero',
                method: 'graficar_limnigrama',
                args: [],
                kwargs: {
                    values: {
                        'desde': this.params['desde'],
                        'hasta': this.params['hasta'],
                        'elemento_graficar': this.params['elemento_graficar'],
                        'duracion_graficar': this.params['duracion_graficar'],
                        'pozo_id': this.params['pozo_id'],
                        'pozo_bloque_ids': this.params['pozo_bloque_ids'],
                        'pozo_cuenca_ids': this.params['pozo_cuenca_ids'],
                        'pozo_sector_ids': this.params['pozo_sector_ids'],
                        'metodo_formula': this.params['metodo_formula'],
                        'pronostico': this.params['pronostico'],
                        'presage': this.params['presage'],
                        'meses': this.params['meses'],
                        'bloque_id': this.params['bloque_id'],
                        'sector_id': this.params['sector_id'],
                        'cuenca_id': this.params['cuenca_id'],
                    },
                },
            }).then(function (result) {
                graficar(result);

                $("#tbl_resumen tr").remove();
                var nuevaFila = "<tr><td class='tabla_cabezera'><b><span style='color:white;mso-themecolor:background1'>A&#241;o</span></b></td><td class='tabla_cabezera'><b><span style='color:white;mso-themecolor:background1'>&#916;h</span></b></td><td class='tabla_cabezera'><b><span style='color:white;mso-themecolor:background1'>&#916;zh</span></b></td><td class='tabla_cabezera'><b><span style='color:white;mso-themecolor:background1'>&#916;zs</span></b></td><td class='tabla_cabezera'><b><span style='color:white;mso-themecolor:background1'>&#916;H</span></b></td><td class='tabla_cabezera'><b><span style='color:white;mso-themecolor:background1'>&#916;Z</span></b></td></tr>"
                $("#tbl_resumen").append(nuevaFila);
                var cantidad_filas = result['series'][11]['data'].length
                for (var index = 0; index < cantidad_filas - 2; ++index) {
                    var nuevaFila = "<tr>";
                    var delta_H = (parseFloat(result['series'][11]['data'][index]['delta_h']) + parseFloat(result['series'][11]['data'][index]['delta_zh'])).toFixed(2)
                    var delta_Z = (parseFloat(result['series'][11]['data'][index]['delta_zs']) + parseFloat(result['series'][11]['data'][index]['delta_zh'])).toFixed(2)
                    var beta = (parseFloat(result['yAxis'][0]['maximo'] - result['yAxis'][0]['minimo']) / delta_H).toFixed(2)
                    nuevaFila += "<td class='tabla_cuerpo'>" + result['series'][11]['data'][index]['anno'] + "</td>";
                    nuevaFila += "<td class='tabla_cuerpo'>" + parseFloat(result['series'][11]['data'][index]['delta_h']).toFixed(2) + "</td>";
                    nuevaFila += "<td class='tabla_cuerpo'>" + parseFloat(result['series'][11]['data'][index]['delta_zh']).toFixed(2) + "</td>";
                    nuevaFila += "<td class='tabla_cuerpo'>" + parseFloat(result['series'][11]['data'][index]['delta_zs']).toFixed(2) + "</td>";
                    nuevaFila += "<td class='tabla_cuerpo'>" + delta_H + "</td>";
                    nuevaFila += "<td class='tabla_cuerpo'>" + delta_Z + "</td>";
                    nuevaFila += "</tr>";
                    $("#tbl_resumen").append(nuevaFila);
                }
                var nuevaFila = "<tr>";
                var prom_delta_h = 0.0, prom_delta_zh = 0.0, prom_delta_zs = 0.0;
                if (parseFloat(result['series'][11]['data'][0]['delta_h']).toFixed(2) == 0)
                    prom_delta_h = parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_h']).toFixed(2) / (cantidad_filas - 3);
                else
                    prom_delta_h = parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_h']).toFixed(2) / (cantidad_filas - 2);
                if (parseFloat(result['series'][11]['data'][0]['delta_zh']).toFixed(2) == 0)
                    prom_delta_zh = parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_zh']).toFixed(2) / (cantidad_filas - 3);
                else
                    prom_delta_zh = parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_zh']).toFixed(2) / (cantidad_filas - 2);
                if (parseFloat(result['series'][11]['data'][0]['delta_zs']).toFixed(2) == 0)
                    prom_delta_zs = parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_zs']).toFixed(2) / (cantidad_filas - 3);
                else
                    prom_delta_zs = parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_zs']).toFixed(2) / (cantidad_filas - 2);
                delta_H = parseFloat(prom_delta_h * 2).toFixed(2);
                delta_Z = parseFloat(prom_delta_zs * 2).toFixed(2);
                beta = (parseFloat(result['yAxis'][0]['maximo'] - result['yAxis'][0]['minimo_calculado']) / delta_H).toFixed(2)
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + result['series'][11]['data'][cantidad_filas - 2]['anno'] + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + prom_delta_h.toFixed(2) + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + prom_delta_zh.toFixed(2) + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + prom_delta_zs.toFixed(2) + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + delta_H + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + delta_Z + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + '&#946;' + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + 'Estado' + "</span></b></td>";
                nuevaFila += "</tr>";
                $("#tbl_resumen").append(nuevaFila);
                var nuevaFila = "<tr>";
                delta_H = (parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_h']) + parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_zh'])).toFixed(2)
                delta_Z = (parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_zs']) + parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_zh'])).toFixed(2)
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + result['series'][11]['data'][cantidad_filas - 1]['anno'] + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_h']).toFixed(2) + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_zh']).toFixed(2) + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + parseFloat(result['series'][11]['data'][cantidad_filas - 1]['delta_zs']).toFixed(2) + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + delta_H + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + delta_Z + "</span></b></td>";
                nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + beta + "</span></b></td>";
                if (beta <= 1.95) {
                    nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + _t("Underexploted") + "</span></b></td>";
                }
                else {
                    nuevaFila += "<td class='tabla_sumario' <b><span style='color:white;mso-themecolor:background1'>" + _t("Overexploted") + "</span></b></td>";
                }
                nuevaFila += "</tr>";
                $("#tbl_resumen").append(nuevaFila);

            });

            this.$el.find('#b_grafico').bind("click", function () {
                $('#d_grafico').show();
                $('#d_tabla').hide();
            });
            this.$el.find('#b_tabla').bind("click", function () {
                $('#d_tabla').show();
                $('#d_grafico').hide();
            });
            this.$el.find("#btn_exportar").bind("click", function () {
                hc_exportar_grafica();
            });
        }
    });


    core.action_registry.add('grafico_acuifero_view', grafico_acuifero);

    return grafico_acuifero;

});


