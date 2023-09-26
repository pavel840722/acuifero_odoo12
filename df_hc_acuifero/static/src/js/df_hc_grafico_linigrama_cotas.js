/*
 GRAFICO CON ESCALA
 PAVEL DANIEL LOPEZ CASTILLO
 2020
 */
odoo.define('df_hc_acuifero.grafico_limnigrama_cotas', function (require) {
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

    var grafico_limnigrama_cotas = AbstractAction.extend({
        template: "df_hc_acuifero_grafico_limnigrama_cotas_view",

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
                    title: {
                        text: _t("Conjunto hidraúlico subterráneo nivel, volumen, con combinado")
                    },
                    xAxis: {
                        type: 'datetime',

                        scrollbar: {
                            enabled: true
                        },
                    },
                    yAxis: [
                        {
                            title: {
                                text: _t('Nivel m'),
                                style: {
                                    color: '#083695'
                                }
                            },
                            reversed: true,
                            height: 290,
                            lineWidth: 2,
                            labels: {
                                style: {
                                    fontWeight: 'bold',
                                    fontSize: '13px',
                                    color: '#083695'
                                }
                            }
                        },
                        {
                            opposite: true,
                            title: {
                                text: _t('Volumen hm³'),
                                style: {
                                    color: '#236120'
                                }
                            },
                            height: 290,
                            lineWidth: 2,
                            labels: {
                                style: {
                                    fontWeight: 'bold',
                                    fontSize: '13px',
                                    color: '#236120'
                                }
                            }
                        },
                        {
                            title: {
                                text: _t('Altura'),
                                style: {
                                    color: '#ba0000'
                                }
                            },
                            top: 370,
                            height: 140,
                            offset: 0,
                            lineWidth: 2,
                            labels: {
                                style: {
                                    fontWeight: 'bold',
                                    fontSize: '13px',
                                    color: '#ba0000'
                                }
                            }
                        },
                        {
                            opposite: true,
                            title: {
                                text: _t('Cuna agua m'),
                                style: {
                                    color: '#0a1d44'
                                }
                            },
                            top: 370,
                            height: 140,
                            paddingBottom: 100,
                            offset: 0,
                            lineWidth: 2,
                            valueSuffix: 'm234',
                            labels: {
                                style: {
                                    fontWeight: 'bold',
                                    fontSize: '13px',
                                    color: '#0a1d44'
                                }
                            }

                        }
                    ],

                    tooltip: {
                        crosshairs: true,
                        shared: true,
                        xDateFormat: '%B %Y'

                    },
                    legend: { // configuración de la leyenda
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom',
                        borderWidth: 0

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
                            },

                        },
                        series: {
                            cursor: 'pointer',
                            point: {
                                events: {
                                    click: function () {
                                        var chart = this;
                                        var series = chart.series.chart.options.series;
                                        var xvalue = chart.series.xData[this.index];
                                        var date = new Date(xvalue);

                                        $('#tr_data')[0].cells[0].innerText = date.getFullYear()
                                        $('#tr_data')[0].cells[1].innerText = date.getMonth() + 1
                                        if (series[3].data[this.index])
                                            $('#tr_data')[0].cells[2].innerText = series[3].data[this.index][1]
                                        else
                                            $('#tr_data')[0].cells[2].innerText = ''

                                        if (series[0].data[this.index])
                                            $('#tr_data')[0].cells[3].innerText = series[0].data[this.index][1]
                                        else
                                            $('#tr_data')[0].cells[3].innerText = ''

                                        if (series[1].data[this.index])
                                            $('#tr_data')[0].cells[4].innerText = series[1].data[this.index][1]
                                        else
                                            $('#tr_data')[0].cells[4].innerText = ''

                                        if (series[2].data[this.index])
                                            $('#tr_data')[0].cells[5].innerText = series[2].data[this.index][1]
                                        else
                                            $('#tr_data')[0].cells[5].innerText = ''
                                    }
                                }
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
                            name: result['series'][2]['name'],
                            data: result['series'][2]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#ba0000'
                        },
                        {
                            yAxis: 3,
                            type: 'column',
                            name: result['series'][3]['name'],
                            data: result['series'][3]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: false
                            },
                            color: '#0a1d44'
                        }
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
                                                 filename: 'Gr\u00E1fico con escala'
                                            });
                                        }
                                    },
                                    {
                                        text: _t('Descargar PDF'),
                                        onclick: function () {
                                            this.exportChartLocal({
                                                type: 'application/pdf',
                                                filename: 'Gr\u00E1fico con escala'
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
                method: 'graficar_limnigrama_cotas',
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

    core.action_registry.add('grafico_limnigrama_cotas_view', grafico_limnigrama_cotas);
    return grafico_limnigrama_cotas;

});
