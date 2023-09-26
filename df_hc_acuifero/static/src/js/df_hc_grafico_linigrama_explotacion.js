/*
 GRAFICO COMBINADO
 PAVEL DANIEL LOPEZ CASTILLO
 2020
 */
odoo.define('df_hc_acuifero.grafico_explotacion', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var core = require('web.core');
    var ajax = require('web.ajax');


    var _t = core._t;
    var QWeb = core.qweb;

    Highcharts.setOptions({
        lang: {
            months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            weekdays: ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'],
            shortMonths: ['En', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ag', 'Sep', 'Oct', 'Nov', 'Dic'],
            rangeSelectorFrom: "Desde",
            rangeSelectorTo: "Hasta",
            rangeSelectorZoom: "Aumentar",
            resetZoom: 'Restablecer tamano',
            downloadPNG: _t('Download PNG image'),
            printChart: _t('Print chart')
        }
    });
    var grafico_explotacion = AbstractAction.extend({
        template: "df_hc_acuifero_grafico_explotacion_view",

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
                        zoomType: 'x',
                        spacingRight: 20,
                        type: 'spline',
                        height: 800,
                    },

                    scrollbar: {
                        enabled: true
                    },
                    title: {
                        text: _t("Gráfico combinado de Nivel-Explotación-Lluvia")
                    },
                    xAxis: {
                        type: 'datetime',
                        alternateGridColor: '#f2f2f2',
                        labels: {
                            style: {
                                fontWeight: 'bold',
                                fontSize: '13px'
                            }
                        }
                    },
                    yAxis: [
                        {
                            title: {
                                text: _t('Nivel m')
                            },
                            reversed: true,
                            height: 145,
                            lineWidth: 2,
                            labels: {
                                style: {
                                    fontWeight: 'bold',
                                    fontSize: '13px'
                                }
                            }
                        },
                        {
                            title: {
                                text: _t('Explotación')
                            },
                            top: 210,
                            height: 130,
                            offset: 0,
                            lineWidth: 2,
                            labels: {
                                style: {
                                    fontWeight: 'bold',
                                    fontSize: '13px'
                                }
                            }
                        },
                        {
                            title: {
                                text: _t('Lluvia acumulada')
                            },
                            top: 348,
                            height: 130,
                            offset: 0,
                            lineWidth: 2,
                            labels: {
                                formatter: function () {
                                    return this.value;
                                },
                                style: {
                                    fontWeight: 'bold',
                                    fontSize: '13px'
                                }
                            }
                        }
//                            {
//                                opposite: true,
//                                title: {
//                                    text: _t('Area m2, Cota')
//                                },
//                                reversed: true,
//                                top: 360,
//                                height: 150,
//                                offset: 0,
//                                lineWidth: 2,
//                                labels: {
//                                    style: {
//                                        fontWeight: 'bold',
//                                        fontSize: '13px'
//                                    }
//                                }
//                            }
                    ],
                    tooltip: {
                        crosshairs: true,
                        shared: true,
                        valueSuffix: 'm',
                        xDateFormat: '%B  %Y'
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
                            color: '#083695'
                        },
                        {
                            yAxis: 1,
                            type: 'column',
                            name: result['series'][2]['name'],
                            data: result['series'][2]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#e10f0f'
                        },
                        {
                            yAxis: 1,
                            type: 'column',
                            name: result['series'][1]['name'],
                            data: result['series'][1]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#236120'
                        },
                        {
                            yAxis: 2,
                            type: 'column',
                            name: result['series'][3]['name'],
                            data: result['series'][3]['data'],
                            tooltip: {
                                crosshairs: true,
                                shared: true,
                                valueSuffix: 'mm'
                            },
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#4572A7'
                        },
                        {
                            yAxis: 2,
                            type: 'errorbar',
                            name: result['series'][4]['name'],
                            data: result['series'][4]['data'],
                            tooltip: {
                                pointFormat: '(range: {point.low}-{point.high} mm)<br/>'
                            }
                        }
//                            {
//                                yAxis: 2,
//                                name: result['series'][2]['name'],
//                                data: result['series'][2]['data'],
//                                dataLabels: {
//                                    enabled: false
//                                },
//                                marker: {
//                                    enabled: false
//                                },
//                                color: '#ba0000'
//                            },
//                            {
//                                yAxis: 2,
//                                name: result['series'][3]['name'],
//                                data: result['series'][3]['data'],
//                                dataLabels: {
//                                    enabled: false
//                                },
//                                marker: {
//                                    enabled: false
//                                },
//                                 color: '#0a1d44'
//                            }
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
                                                 filename: 'Gráfico combinado'
                                            });
                                        }
                                    },
                                    {
                                        text: _t('Descargar PDF'),
                                        onclick: function () {
                                            this.exportChartLocal({
                                                type: 'application/pdf',
                                                filename: 'Gráfico combinado'
                                            });
                                        }
                                    }
                                ]
                            }
                        }
                    }
                });
            }

            ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                model: 'df.limnigrama.acuifero',
                method: 'graficar_limnigrama_explotacion',
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


            });
        }
    });

    core.action_registry.add('grafico_explotacion_view', grafico_explotacion);
    return grafico_explotacion;
});
