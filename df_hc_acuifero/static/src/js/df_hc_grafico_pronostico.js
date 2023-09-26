/*
 GRAFICO PRONOSTICO HUMEDO
 PAVEL DANIEL LOPEZ CASTILLO
 2020
 */
odoo.define('df_hc_acuifero.grafico_pronostico_humedo', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var framework = require('web.framework');
    var session = require('web.session');


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

    var grafico_pronostico = AbstractAction.extend({
        template: "df_hc_acuifero_grafico_pronostico_view",

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
                        type: 'line'
                    },
                    //scrollbar: {
                    //    enabled: true
                    //},
                    title: {
                        text: _t('Pron\u00F3stico h\u00FAmedo ' + result['year'] + ' ' + result['sigla'])
                    },
                    //subtitle: {
                    //    text: document.ontouchstart === undefined ?
                    //        _t('Click and drag in the plot area to zoom in') :
                    //        _t('Drag your finger over the plot to zoom in')
                    //},
                    xAxis: {
                        categories: ['May', 'Jun', 'Jul', 'Agto', 'Sep', 'Oct'],
                        //categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
                        //title: {
                        //    text: null
                        //}
                    },
                    yAxis: [
                        {
                            title: {
                                text: _t('Level (m)')
                            },
                            reversed: true,
                            lineWidth: 2,
                            labels: {
                                style: {
                                    fontWeight: 'bold',
                                    fontSize: '13px'
                                }
                            }
                        }
                    ],
                    tooltip: {
                        crosshairs: true,
                        shared: true,
                        valueSuffix: 'm'
                    },
//                        plotOptions: {
//                            line: {
//                                dataLabels: {
//                                    enabled: true
//                                },
//                                enableMouseTracking: false,
//                                lineWidth: 3,
//                                states: {
//                                    hover: {
//                                        lineWidth: 4
//                                    }
//                                },
//                                marker: {
//                                    enabled: false
//                                }
//                            }
//                        },
                    series: [
                        {
//                                pointInterval: 30 * 24 * 3600 * 1000,
                            name: result['series'][0]['name'],
                            data: result['series'][0]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            color: 'blue',
                            marker: {
                                enabled: true
                            }
                        },
                        {
//                                pointInterval: 24 * 3600 * 1000,
                            name: result['series'][1]['name'],
                            data: result['series'][1]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            color: 'green',
                            marker: {
                                enabled: true
                            }
                        },
                        {
//                                pointInterval: 24 * 3600 * 1000,
                            name: result['series'][2]['name'],
                            data: result['series'][2]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            color: 'black',
                            marker: {
                                enabled: true
                            }
                        },
                        {
//                                pointInterval: 24 * 3600 * 1000,
                            name: result['series'][3]['name'],
                            data: result['series'][3]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            color: 'brown',
                            marker: {
                                enabled: true
                            }
                        },
                        {
//                                pointInterval: 24 * 3600 * 1000,
                            name: result['series'][4]['name'],
                            data: result['series'][4]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            color: 'orange',
                            marker: {
                                enabled: true
                            }
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
                                                 filename: 'Gr\u00E1fico pron\u00F3stico h\u00FAmedo'
                                            });
                                        }
                                    },
                                    {
                                        text: _t('Descargar PDF'),
                                        onclick: function () {
                                            this.exportChartLocal({
                                                type: 'application/pdf',
                                                filename: 'Gr\u00E1fico pron\u00F3stico h\u00FAmedo'
                                            });
                                        }
                                    }
                                ]
                            }
                        }
                    }
                });
            }


            var nreal = {'5': null, '6': null, '7': null, '8': null, '9': null, '10': null};
            for (var i = 5; i <= 10; i++) {
                if ($('table.grid_pronostico tr#Nreal td#Nreal_' + i).html() != 0) {
                    nreal['' + i + ''] = parseFloat($('table.grid_pronostico tr#Nreal td#Nreal_' + i).html())
                }

            }

            if (this.params['elemento_graficar'] == "pozo") {

                ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                    model: 'df.pozo',
                    method: 'calcular_niveles_pronosticos_reales',
                    args: [],
                    kwargs: {
                        'id': this.params['pozo_id'],
                        'anno1': this.params['year'],
                        'nreal': nreal,
                        'pronostico': this.params['pronostico'],
                    },
                }).then(function (result) {
                    $("#xxxx").empty();
                    $("#xxxx").empty();
                    $("#prono").html("Pron\u00F3stico Per\u00EDodo H\u00FAmedo " + result['sigla']);
                    var nuevaFila = "";
                    var cantidad_series = result['series'].length;

                    for (var m = 0; m < 6; m++) {
                        var nuevaFila = "<tr><td>" + result['series'][0]['data'][m][0] + "</td>";
                        var dif_12 = 1;
                        var dif_13 = 1;
                        var dif_14 = 1;
                        var dif_15 = 1;
                        for (var c_s = 0; c_s < cantidad_series; c_s++) {
                            if (result['series'][c_s]['data'][m][1] == null)
                                nuevaFila += "<td></td>";
                            else
                                nuevaFila += "<td>" + result['series'][c_s]['data'][m][1] + "</td>";
                        }
                        if (result['series'][0]['data'][m][1] == null || result['series'][1]['data'][m][1] == null)
                            dif_12 = '';
                        else
                            dif_12 = Number((result['series'][0]['data'][m][1] - result['series'][1]['data'][m][1]).toFixed(2));
                        if (result['series'][0]['data'][m][1] == null || result['series'][2]['data'][m][1] == null)
                            dif_13 = '';
                        else
                            dif_13 = Number((result['series'][0]['data'][m][1] - result['series'][2]['data'][m][1]).toFixed(2));
                        if (result['series'][0]['data'][m][1] == null || result['series'][3]['data'][m][1] == null)
                            dif_14 = '';
                        else
                            dif_14 = Number((result['series'][0]['data'][m][1] - result['series'][3]['data'][m][1]).toFixed(2));
                        if (result['series'][0]['data'][m][1] == null || result['series'][4]['data'][m][1] == null)
                            dif_15 = '';
                        else
                            dif_15 = Number((result['series'][0]['data'][m][1] - result['series'][4]['data'][m][1]).toFixed(2));

                        //  nuevaFila += "<td>"+Number((dif_12).toFixed(2))+"</td><td>"+Number((dif_13).toFixed(2))+"</td><td>"+Number((dif_14).toFixed(2))+"</td><td>"+Number((dif_15).toFixed(2))+"</td>";
                        nuevaFila += "<td>" + dif_12 + "</td><td>" + dif_13 + "</td><td>" + dif_14 + "</td><td>" + dif_15 + "</td>";
                        nuevaFila += "</tr>";

                        $("#xxxx").append(nuevaFila);
                    }
                    graficar(result);

                });
            }
            if (this.params['elemento_graficar'] == "sector") {
                var tipo = "sector";
                ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                    model: 'df.sector.hidrologico',
                    method: 'calcular_niveles_pronosticos_reales',
                    args: [],
                    kwargs: {
                        'id': this.params['sector_id'],
                        'anno1': this.params['year'],
                        'nreal': nreal,
                        'pronostico': this.params['pronostico'],
                        'tipo': tipo,
                        'metodo': this.params['metodo_formula'],
                        'pozo_ids': this.params['pozo_sector_ids'],
                    },
                }).then(function (result) {
                    $("#xxxx").empty();
                    $("#xxxx").empty();
                    $("#prono").html("Pron\u00F3stico Per\u00EDodo H\u00FAmedo " + result['sigla']);
                    var nuevaFila = "";
                    var cantidad_series = result['series'].length;

                    for (var m = 0; m < 6; m++) {
                        var nuevaFila = "<tr><td>" + result['series'][0]['data'][m][0] + "</td>";
                        var dif_12 = 1;
                        var dif_13 = 1;
                        var dif_14 = 1;
                        var dif_15 = 1;
                        for (var c_s = 0; c_s < cantidad_series; c_s++) {
                            if (result['series'][c_s]['data'][m][1] == null)
                                nuevaFila += "<td></td>";
                            else
                                nuevaFila += "<td>" + result['series'][c_s]['data'][m][1] + "</td>";
                        }
                        if (result['series'][0]['data'][m][1] == null || result['series'][1]['data'][m][1] == null)
                            dif_12 = '';
                        else
                            dif_12 = Number((result['series'][0]['data'][m][1] - result['series'][1]['data'][m][1]).toFixed(2));
                        if (result['series'][0]['data'][m][1] == null || result['series'][2]['data'][m][1] == null)
                            dif_13 = '';
                        else
                            dif_13 = Number((result['series'][0]['data'][m][1] - result['series'][2]['data'][m][1]).toFixed(2));
                        if (result['series'][0]['data'][m][1] == null || result['series'][3]['data'][m][1] == null)
                            dif_14 = '';
                        else
                            dif_14 = Number((result['series'][0]['data'][m][1] - result['series'][3]['data'][m][1]).toFixed(2));
                        if (result['series'][0]['data'][m][1] == null || result['series'][4]['data'][m][1] == null)
                            dif_15 = '';
                        else
                            dif_15 = Number((result['series'][0]['data'][m][1] - result['series'][4]['data'][m][1]).toFixed(2));

                        //  nuevaFila += "<td>"+Number((dif_12).toFixed(2))+"</td><td>"+Number((dif_13).toFixed(2))+"</td><td>"+Number((dif_14).toFixed(2))+"</td><td>"+Number((dif_15).toFixed(2))+"</td>";
                        nuevaFila += "<td>" + dif_12 + "</td><td>" + dif_13 + "</td><td>" + dif_14 + "</td><td>" + dif_15 + "</td>";
                        nuevaFila += "</tr>";

                        $("#xxxx").append(nuevaFila);
                    }

                    graficar(result);

                });

            }
            if (this.params['elemento_graficar'] == "cuenca") {
                var tipo = "cuenca";
                ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                    model: 'df.cuenca.subterranea',
                    method: 'calcular_niveles_pronosticos_reales',
                    args: [],
                    kwargs: {
                        'id': this.params['cuenca_id'],
                        'anno1': this.params['year'],
                        'nreal': nreal,
                        'pronostico': this.params['pronostico'],
                        'tipo': tipo,
                        'metodo': this.params['metodo_formula'],
                        'pozo_ids': this.params['pozo_cuenca_ids'],
                    },
                }).then(function (result) {
                    $("#xxxx").empty();
                    $("#xxxx").empty();
                    $("#prono").html("Pron\u00F3stico Per\u00EDodo H\u00FAmedo " + result['sigla']);
                    var nuevaFila = "";
                    var cantidad_series = result['series'].length;

                    for (var m = 0; m < 6; m++) {
                        var nuevaFila = "<tr><td>" + result['series'][0]['data'][m][0] + "</td>";
                        var dif_12 = 1;
                        var dif_13 = 1;
                        var dif_14 = 1;
                        var dif_15 = 1;
                        for (var c_s = 0; c_s < cantidad_series; c_s++) {
                            if (result['series'][c_s]['data'][m][1] == null)
                                nuevaFila += "<td></td>";
                            else
                                nuevaFila += "<td>" + result['series'][c_s]['data'][m][1] + "</td>";
                        }
                        if (result['series'][0]['data'][m][1] == null || result['series'][1]['data'][m][1] == null)
                            dif_12 = '';
                        else
                            dif_12 = Number((result['series'][0]['data'][m][1] - result['series'][1]['data'][m][1]).toFixed(2));
                        if (result['series'][0]['data'][m][1] == null || result['series'][2]['data'][m][1] == null)
                            dif_13 = '';
                        else
                            dif_13 = Number((result['series'][0]['data'][m][1] - result['series'][2]['data'][m][1]).toFixed(2));
                        if (result['series'][0]['data'][m][1] == null || result['series'][3]['data'][m][1] == null)
                            dif_14 = '';
                        else
                            dif_14 = Number((result['series'][0]['data'][m][1] - result['series'][3]['data'][m][1]).toFixed(2));
                        if (result['series'][0]['data'][m][1] == null || result['series'][4]['data'][m][1] == null)
                            dif_15 = '';
                        else
                            dif_15 = Number((result['series'][0]['data'][m][1] - result['series'][4]['data'][m][1]).toFixed(2));

                        //  nuevaFila += "<td>"+Number((dif_12).toFixed(2))+"</td><td>"+Number((dif_13).toFixed(2))+"</td><td>"+Number((dif_14).toFixed(2))+"</td><td>"+Number((dif_15).toFixed(2))+"</td>";
                        nuevaFila += "<td>" + dif_12 + "</td><td>" + dif_13 + "</td><td>" + dif_14 + "</td><td>" + dif_15 + "</td>";
                        nuevaFila += "</tr>";

                        $("#xxxx").append(nuevaFila);
                    }

                    graficar(result);

                });

            }

            this.$el.find('#b_grafico').bind("click", function () {
                $('#d_grafico').show();
                $('#d_tabla').hide();
            });
            this.$el.find('#b_tabla').bind("click", function () {
                $('#d_tabla').show();
                $('#d_grafico').hide();
            });
        }
    });


    core.action_registry.add('grafico_pronostico_view', grafico_pronostico);
    return grafico_pronostico;

});