/*
 GRAFICO CURVA DE AGOTAMIENTO
 PAVEL DANIEL LOPEZ CASTILLO
 2020
 */
odoo.define('df_hc_acuifero.grafico_recorridos', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var core = require('web.core');
    var ajax = require('web.ajax');
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
    var grafico_recorridos = AbstractAction.extend({
        template: "df_hc_acuifero_grafico_recorridos_view",

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
                        type: 'spline'
                    },

                    scrollbar: {
                        enabled: true
                    },
                    title: {
//                            text: _t("Underground hydraulic set Level-Explotation combined")
                        text: _t("Conjunto hidraúlico subterráneo nivel - explotación combinado")
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
//                                height: 300,
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
                            color: '#083695',
                            marker: {
                                enabled: false
                            },
                        },
                        {
                            name: result['series'][1]['name'],
                            data: result['series'][1]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            marker: {
                                enabled: true
                            },
                            lineWidth: 3,
                            color: '#e10f0f'
                        },
                        {
                            name: result['series'][2]['name'],
                            data: result['series'][2]['data'],
                            dataLabels: {
                                enabled: false
                            },
                            lineWidth: 2,
                            marker: {
                                enabled: true
                            },
                            color: '#e8c741'
                        }
//                            {
//                                name: result['series'][3]['name'],
//                                data: result['series'][3]['data'],
//                                dataLabels: {
//                                    enabled: true
//                                },
//                                lineWidth: 2,
//                                marker: {
//                                    enabled: true
//                                },
//                                color: '#1aa203'
//                            },
//                            {
//                                name: result['series'][4]['name'],
//                                data: result['series'][4]['data'],
//                                dataLabels: {
//                                    enabled: false
//                                },
//                                marker: {
//                                    enabled: false
//                                },
//                                color: '#1aa203'
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
                                                 filename: 'Gráfico curva de agotamiento'
                                            });
                                        }
                                    },
                                    {
                                        text: _t('Descargar PDF'),
                                        onclick: function () {
                                            this.exportChartLocal({
                                                type: 'application/pdf',
                                                filename: 'Gráfico curva de agotamiento'
                                            });
                                        }
                                    }
                                ]
                            }
                        }
                    }
                });
                var char_recorrido_1 = new Highcharts.Chart({
                    chart: {
                        zoomType: 'x',
                        spacingRight: 20,
                        type: 'spline',
                        renderTo: 'div_chart_recorrido_cota_1'
                    },

                    scrollbar: {
                        enabled: true
                    },
                    title: {
                        text: _t("Curva CA")
                    },
                    xAxis: {
//                            type: 'datetime',
                        alternateGridColor: '#f2f2f2',
                        labels: {
                            style: {
                                fontWeight: 'bold',
                                fontSize: '13px'
                            }
                        },
                        title: {
                            text: _t('Tiempo (meses)')
                        }
                    },
                    yAxis: [
                        {
                            title: {
                                text: _t('Cota (m)')
                            },
//                                reversed: true,
//                                height: 300,
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
                            regressionSettings: {
                                type: 'exponential',
                                color: 'rgba(223, 83, 83, .9)',
                            },
//                                type:'scatter',
                            regression: true,
                            id: 'primaria',
                            pointInterval: 1,
                            name: result['series'][9]['name'],
                            data: result['series'][9]['data'],
                            dataLabels: {
                                enabled: false
                            }
                        },
                        //{
                        //    type: "linearRegression",
                        //    linkedTo: "base",
                        //    zIndex: -1,
                        //    params: {
                        //        period: 5
                        //    }
                        //},
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
                                            this.exportChartLocal();
                                        }
                                    },
                                    {
                                        text: _t('Descargar PDF'),
                                        onclick: function () {
                                            this.exportChartLocal({
                                                type: 'application/pdf'
                                            });
                                        }
                                    }
                                ]
                            }
                        }
                    }
                });

                var char_recorrido_2 = new Highcharts.Chart({
                    chart: {
                        zoomType: 'x',
                        spacingRight: 20,
                        type: 'spline',
                        renderTo: 'div_chart_recorrido_cota_2'
                    },

                    scrollbar: {
                        enabled: true
                    },
                    title: {
                        text: _t("CA Curve")
                    },
                    xAxis: {
//                            type: 'datetime',
                        alternateGridColor: '#f2f2f2',
                        labels: {
                            style: {
                                fontWeight: 'bold',
                                fontSize: '13px'
                            }
                        },
                        title: {
                            text: _t('Tiempo (meses)')
                        },
                    },
                    yAxis: [
                        {
                            title: {
                                text: _t('Cota (m)')
                            },
//                                reversed: true,
//                                height: 300,
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
                            regressionSettings: {
                                type: 'exponential',
                                color: 'rgba(223, 83, 83, .9)',
                            },
//                                type:'scatter',
                            regression: true,
                            id: 'primaria',
                            pointInterval: 1,
                            name: result['series'][10]['name'],
                            data: result['series'][10]['data'],
                            dataLabels: {
                                enabled: false
                            }
                        },
                        //{
                        //    type: "linearRegression",
                        //    linkedTo: "base",
                        //    zIndex: -1,
                        //    params: {
                        //        period: 5
                        //    }
                        //},
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
                                            this.exportChartLocal();
                                        }
                                    },
                                    {
                                        text: _t('Descargar PDF'),
                                        onclick: function () {
                                            this.exportChartLocal({
                                                type: 'application/pdf'
                                            });
                                        }
                                    }
                                ]
                            }
                        }
                    }
                });
                var r_recorrido_1 = char_recorrido_1.legend.allItems[1].name.split('R:')[1] * 1
                var r_recorrido_2 = char_recorrido_2.legend.allItems[1].name.split('R:')[1] * 1
                //var r_recorrido_1 = 0.9869;
                //var r_recorrido_2 = 0.9698;
                var mas_preciso = 0
                var char_preciso = 0
                if (r_recorrido_1 > r_recorrido_2) {
                    char_preciso = []
                    mas_preciso = 1
                    var index = 0
                    while (index < char_recorrido_1['series'][1]['data'].length) {
                        char_preciso.push(char_recorrido_1['series'][1]['data'][index])
                        index += 1
                    }
                }
                else {
                    char_preciso = []
                    index = 0
                    while (index < char_recorrido_2['series'][1]['data'].length) {
                        char_preciso.push(char_recorrido_2['series'][1]['data'][index])
                        index += 1
                    }
                    mas_preciso = 2
                }

                $("#tbl_cota_regresion_1 tr").remove();
                var nuevaFila = "<tr><td colspan='3' class='tabla_cabezera_secundaria'><b><span style='color:white;mso-themecolor:background1'>" + _t('More exactly travel: ') + mas_preciso.toString() + "</span> </b></td></tr>"
                $("#tbl_cota_regresion_1").append(nuevaFila);
                var nuevaFila = "<tr><td class='tabla_cabezera_secundaria'><b><span style='color:white;mso-themecolor:background1'>" + _t('Time') + "</span></b></td><td class='tabla_cabezera_secundaria'><b><span style='color:white;mso-themecolor:background1'>" + _t('Regression') + "</span></b></td><td class='tabla_cabezera_secundaria'><b><span style='color:white;mso-themecolor:background1'>Z/T</span></b></td></tr>"
                $("#tbl_cota_regresion_1").append(nuevaFila);

                var data_cota_zt = []

                for (index = 0; index < char_preciso.length; ++index) {
                    var zt = 0
                    var nuevaFila = "<tr>";
                    nuevaFila += "<td class='tabla_cuerpo'>" + char_preciso[index].x + "</td>";
                    nuevaFila += "<td class='tabla_cuerpo'>" + parseFloat(char_preciso[index].y).toFixed(2) + "</td>";
//                        nuevaFila1+="<td class='tabla_cuerpo'>"+ parseFloat(char.series[0].data[index].y).toFixed(2) + "</td>";
                    if (index == 0) {
                        var zt0 = (parseFloat(char_preciso[0].y).toFixed(2) - parseFloat(char_preciso[1].y).toFixed(2)).toFixed(4);
                        var zt1 = (parseFloat(char_preciso[1].y).toFixed(2) - parseFloat(char_preciso[2].y).toFixed(2)).toFixed(4);
                        zt = (zt0 - (zt1 - zt0)).toFixed(2);
                    }
                    else
                        zt = (parseFloat(char_preciso[index - 1].y).toFixed(2) * 1 - parseFloat(char_preciso[index].y).toFixed(2) * 1).toFixed(2);
                    nuevaFila += "<td class='tabla_cuerpo'>" + zt + "</td>";
                    nuevaFila += "</tr>";
                    $("#tbl_cota_regresion_1").append(nuevaFila);

                    data_cota_zt.push([parseFloat(char_preciso[index].y).toFixed(2) * 1, zt * 1])
                }
                //alert(data_cota_zt);
                var char_zt = new Highcharts.Chart('div_chart_zt', {
                    chart: {
                        zoomType: 'x',
                        spacingRight: 20,
                        type: 'spline',
                        //renderTo: 'div_chart_zt'
                    },
                    scrollbar: {
                        enabled: true
                    },
                    title: {
                        text: _t("Depletion curve of ∆Z/∆t vs CA Russpoli")
                    },
                    xAxis: {
                        alternateGridColor: '#f2f2f2',
                        title: {
                            text: _t('Cota (m)')
                        },
                        reversed: true
                    },
                    yAxis: [
                        {
                            title: {
                                text: _t('∆Z/∆t(m)')
                            },
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
//                            shared: true,
//                            valueSuffix: 'm'
                    },
//                        plotOptions: {
//                            line: {
//                                dataLabels: {
//                                    enabled: true
//                                },
//                                enableMouseTracking: true,
//                                lineWidth: 3,
//                                states: {
//                                    hover: {
//                                        lineWidth: 4
//                                    }
//                                },
//                                marker: {
//                                    enabled: true
//                                }
//                            }
//                        },
                    series: [
                        {
                            regressionSettings: {
                                type: 'exponential',
                                color: 'rgba(223, 83, 83, .9)'
                            },
                            regression: true,
//                                pointInterval: 1,
                            name: 'Z/t (m)',
                            data: data_cota_zt,
                            dataLabels: {
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
                                            this.exportChartLocal();
                                        }
                                    },
                                    {
                                        text: _t('Descargar PDF'),
                                        onclick: function () {
                                            this.exportChartLocal({
                                                type: 'application/pdf'
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
                session.get_file({
                    url: '/web/export/xls_recorridos_view',
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
                method: 'graficar_limnigrama_recorridos',
                args: [],
                kwargs: {
                    values: {
                        'desde': this.params['desde'],
                        'hasta': this.params['hasta'],
                        'elemento_graficar': this.params['elemento_graficar'],
                        'metodo_aritmetico': this.params['metodo_aritmetico'],
                        'metodo_formula': this.params['metodo_formula'],
                        'valor_precision': this.params['valor_precision'],
                        'rango_limpieza': this.params['rango_limpieza'],
                        'pozo_id': this.params['pozo_id'],
                        'bloque_id': this.params['bloque_id'],
                        'sector_id': this.params['sector_id'],
                        'cuenca_id': this.params['cuenca_id'],
                        'pozo_bloque_ids': this.params['pozo_bloque_ids'],
                        'pozo_cuenca_ids': this.params['pozo_cuenca_ids'],
                        'pozo_sector_ids': this.params['pozo_sector_ids'],
                    },
                },
            }).then(function (result) {
                $("#tbl_resumen tr").remove();
                var nuevaFila = "<tr><td class='tabla_cabezera' colspan='3'><b><span style='color:white;mso-themecolor:background1'>" + _t('Travel 1') + "</span></b></td><td class='tabla_cabezera' colspan='3'><b><span style='color:white;mso-themecolor:background1'>" + _t('Travel 2') + "</span></b></td></tr>"
                $("#tbl_resumen").append(nuevaFila);
                var nuevaFila = "<tr><td class='tabla_2da_cabezera'>" + _t('Months') + "</td><td class='tabla_2da_cabezera'>N.E(m)</td><td class='tabla_2da_cabezera'>C.A(m)</td><td class='tabla_2da_cabezera'>" + _t('Months') + "</td><td class='tabla_2da_cabezera'>N.E(m)</td><td class='tabla_2da_cabezera'>C.A(m)</td></tr>"
                $("#tbl_resumen").append(nuevaFila);
                var max_length = result['series'][5]['data'].length;
                if (max_length < result['series'][6]['data'].length)
                    max_length = result['series'][6]['data'].length
                if (max_length < result['series'][7]['data'].length)
                    max_length = result['series'][7]['data'].length
                for (var index = 0; index < max_length; ++index) {
                    var trs = $("#tbl_resumen tr").length; //Nro de filas
                    var nuevaFila = "<tr>";
                    if (result['series'][5]['data'].length > index) {
                        nuevaFila += "<td class='tabla_2da_cabezera'>" + result['series'][5]['data'][index][0] + "</td>";
                        nuevaFila += "<td class='tabla_cuerpo'>" + parseFloat(result['series'][5]['data'][index][1]).toFixed(2) + "</td>";
                        nuevaFila += "<td class='tabla_cuerpo'>" + parseFloat(result['series'][5]['data'][index][2]).toFixed(2) + "</td>";
                    }
                    else {
                        nuevaFila += "<td class='tabla_2da_cabezera'></td>";
                        nuevaFila += "<td class='tabla_cuerpo'></td>";
                        nuevaFila += "<td class='tabla_cuerpo'></td>";
                    }
                    if (result['series'][6]['data'].length > index) {
                        nuevaFila += "<td class='tabla_2da_cabezera'>" + result['series'][6]['data'][index][0] + "</td>";
                        nuevaFila += "<td class='tabla_cuerpo'>" + parseFloat(result['series'][6]['data'][index][1]).toFixed(2) + "</td>";
                        nuevaFila += "<td class='tabla_cuerpo'>" + parseFloat(result['series'][6]['data'][index][2]).toFixed(2) + "</td>";
                    }
                    else {
                        nuevaFila += "<td class='tabla_2da_cabezera'></td>";
                        nuevaFila += "<td class='tabla_cuerpo'></td>";
                        nuevaFila += "<td class='tabla_cuerpo'></td>";
                    }

                    $("#tbl_resumen").append(nuevaFila);
                }
                graficar(result);


            });

            var hc_salvar_regresion_zt = function () {
                var global_objeto_tipo = self.params['elemento_graficar'];
                var global_objeto_id;
                var fromm = self.params['desde'];
                var too = self.params['hasta'];
                if (self.params['elemento_graficar'] == 'pozo') {
                    global_objeto_id = self.params['pozo_id'];
                }
                else if (self.params['elemento_graficar'] == 'bloque') {
                    global_objeto_id = self.params['bloque_id'];
                }
                else if (self.params['elemento_graficar'] == 'sector') {
                    global_objeto_id = self.params['sector_id'];
                }
                else if (self.params['elemento_graficar'] == 'cuenca') {
                    global_objeto_id = self.params['cuenca_id'];
                }
                var values = {'data': []};
                for (var index = 2; index < tbl_cota_regresion_1.rows.length; ++index) {
                    var fila_tabla = tbl_cota_regresion_1.rows[index]
                    var fila = {
                        'objeto_tipo': global_objeto_tipo,
                        'objeto_id': global_objeto_id,
                        'tiempo': parseInt(fila_tabla.cells[0].innerHTML),
                        'regresion': parseFloat(fila_tabla.cells[1].innerHTML),
                        'zt': parseFloat(fila_tabla.cells[2].innerHTML),
                        'desde': fromm,
                        'hasta': too
                    }
                    values['data'].push(fila)
                }
                ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                    model: 'df.tabla.regresion',
                    method: 'guardar',
                    args: [],
                    kwargs: {
                        vals: values
                    },
                }).then(function (result) {
                    alert('Datos guardados satisfactoriamente');
                });


                //$.when(new openerp.web.Model('df.tabla.regresion').get_func("create")(values).pipe(function (result) {
                //}).then(function () {
                //}));
            }


            this.$el.find("#btn_save_rec1").bind("click", function () {
                hc_salvar_regresion_zt();
            });

            this.$el.find("#btn_exportar").bind("click", function () {
                hc_exportar_grafica();
            });

            this.$el.find('#b_grafico').bind("click", function () {
                $('#d_grafico').show();
                $('#d_tabla_recorridos').hide();
                $('#d_regresion').hide();
                $('#d_z_t').hide();
            });
            this.$el.find('#b_tabla').bind("click", function () {
                $('#d_tabla_recorridos').show();
                $('#d_grafico').hide();
                $('#d_regresion').hide();
                $('#d_z_t').hide();
            });
            this.$el.find('#b_regresion').bind("click", function () {
                $('#d_regresion').show();
                $('#d_tabla_recorridos').hide();
                $('#d_grafico').hide();
                $('#d_z_t').hide();
            });
            this.$el.find('#b_z_t').bind("click", function () {
                $('#d_z_t').show();
                $('#d_tabla_recorridos').hide();
                $('#d_grafico').hide();
                $('#d_regresion').hide();
            });
        }
    });
    core.action_registry.add('grafico_recorridos_view', grafico_recorridos);
    return grafico_recorridos;
});