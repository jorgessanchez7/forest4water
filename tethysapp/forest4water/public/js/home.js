var map;
var feature_layer;
let $loading = $('#view-file-loading');

function init_map() {

	var base_layer = new ol.layer.Tile({
		source: new ol.source.BingMaps({
			key: 'eLVu8tDRPeQqmBlKAjcw~82nOqZJe2EpKmqd-kQrSmg~AocUZ43djJ-hMBHQdYDyMbT-Enfsk0mtUIGws1WeDuOvjY4EXCH-9OK3edNLDgkc',
			imagerySet: 'Road'
			//            imagerySet: 'AerialWithLabels'
		})
	});

	var stations = new ol.layer.Image({
		source: new ol.source.ImageWMS({
			url: 'https://multi-tethys.byu.edu/geoserver/forest4water/wms',
			params: { 'LAYERS': 'qlStations_points' },
			serverType: 'geoserver',
			crossOrigin: 'Anonymous'
		})
	});

	feature_layer = stations;

	map = new ol.Map({
		target: 'map',
		layers: [base_layer, stations],
		view: new ol.View({
			center: ol.proj.fromLonLat([-74.08083, 4.598889]),
			zoom: 5
		})
	});

}

let ajax_url = 'https://multi-tethys.byu.edu/geoserver/forest4water/wfs?request=GetCapabilities';

let capabilities = $.ajax(ajax_url, {
	type: 'GET',
	data:{
		service: 'WFS',
		version: '1.0.0',
		request: 'GetCapabilities',
		outputFormat: 'text/javascript'
	},
	success: function() {
		let x = capabilities.responseText
		.split('<FeatureTypeList>')[1]
		.split('forest4water:qlStations_points')[1]
		.split('LatLongBoundingBox ')[1]
		.split('/></FeatureType>')[0];

		let minx = Number(x.split('"')[1]);
		let miny = Number(x.split('"')[3]);
		let maxx = Number(x.split('"')[5]);
		let maxy = Number(x.split('"')[7]);

		minx = minx + 2;
		miny = miny + 2;
		maxx = maxx - 2;
		maxy = maxy - 2;

		let extent = ol.proj.transform([minx, miny], 'EPSG:4326', 'EPSG:3857').concat(ol.proj.transform([maxx, maxy], 'EPSG:4326', 'EPSG:3857'));

		map.getView().fit(extent, map.getSize());
	}
});

function map_events() {
	map.on('pointermove', function(evt) {
		if (evt.dragging) {
			return;
		}
		var pixel = map.getEventPixel(evt.originalEvent);
		var hit = map.forEachLayerAtPixel(pixel, function(layer) {
			if (layer == feature_layer) {
				current_layer = layer;
				return true;
			}
			});
		map.getTargetElement().style.cursor = hit ? 'pointer' : '';
	});

	map.on("singleclick", function(evt) {

		if (map.getTargetElement().style.cursor == "pointer") {

			var view = map.getView();
			var viewResolution = view.getResolution();
			var wms_url = current_layer.getSource().getGetFeatureInfoUrl(evt.coordinate, viewResolution, view.getProjection(), { 'INFO_FORMAT': 'application/json' });

			if (wms_url) {
				$("#obsgraph").modal('show');
				$('#observed-chart-Q').addClass('hidden');
				$('#observed-chart-S').addClass('hidden');
				$('#observed-chart-T').addClass('hidden');
				$('#observed-chart-P').addClass('hidden');
				$('#observed-chart-FC').addClass('hidden');
				$('#mean-chart-Q').addClass('hidden');
				$('#std-chart-Q').addClass('hidden');
				$('#max-chart-Q').addClass('hidden');
				$('#min-chart-Q').addClass('hidden');
				$('#mean-chart-S').addClass('hidden');
				$('#std-chart-S').addClass('hidden');
				$('#annual-chart-Q-FC').addClass('hidden');
				$('#annual-chart-S-FC').addClass('hidden');
				$('#observed-loading-Q').removeClass('hidden');
				$('#observed-loading-S').removeClass('hidden');
				$('#observed-loading-T').removeClass('hidden');
				$('#observed-loading-P').removeClass('hidden');
				$('#observed-loading-FC').removeClass('hidden');
				$('#mean-loading-Q').removeClass('hidden');
				$('#std-loading-Q').removeClass('hidden');
				$('#max-loading-Q').removeClass('hidden');
				$('#min-loading-Q').removeClass('hidden');
				$('#mean-loading-S').removeClass('hidden');
				$('#std-loading-S').removeClass('hidden');
				$('#annual-loading-Q-FC').removeClass('hidden');
				$('#annual-loading-S-FC').removeClass('hidden');
				$("#station-info").empty()

				$.ajax({
					type: "GET",
					url: wms_url,
					dataType: 'json',
					success: function (result) {
		         		var startdate = '';
		         		stationcode = result["features"][0]["properties"]["CODIGO"];
		         		stationname = result["features"][0]["properties"]["ESTACION"];
		         		stream = result["features"][0]["properties"]["CORRIENTE"];
		         		$("#station-info").append('<h3 id="Station-Name-Tab">Current Station: '+ stationname
                        			+ '</h3><h5 id="Station-Code-Tab">Station Code: '
                        			+ stationcode + '</h5><h5>Stream: '+ stream);
                        get_discharge_info (stationcode, stationname);
                        get_sediments_info (stationcode, stationname);
                        get_temperature_info (stationcode, stationname);
                        get_precipitation_info (stationcode, stationname);
                        get_forest_cover_info (stationcode, stationname);
                        get_monthly_mean_discharge_data (stationcode, stationname);
                        get_monthly_std_discharge_data (stationcode, stationname);
                        get_monthly_max_discharge_data (stationcode, stationname);
                        get_monthly_min_discharge_data (stationcode, stationname);
                        get_monthly_mean_sediments_data (stationcode, stationname);
                        get_monthly_std_sediments_data (stationcode, stationname);
                        get_scatterPlot_Q_FC (stationcode, stationname);
                        get_scatterPlot_S_FC (stationcode, stationname);
                    }
                });
			}
		}

	});
}

function get_discharge_info (stationcode, stationname) {
	$('#observed-loading-Q').removeClass('hidden');
    $.ajax({
        url: 'get-discharge-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed discharge data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#observed-loading-Q').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#observed-chart-Q').removeClass('hidden');
                $('#observed-chart-Q').html(data);

                //resize main graph
                Plotly.Plots.resize($("#observed-chart-Q .js-plotly-plot")[0]);
                Plotly.relayout($("#observed-chart-Q .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Discharge Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_sediments_info (stationcode, stationname) {
	$('#observed-loading-S').removeClass('hidden');
    $.ajax({
        url: 'get-sediments-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed sediments data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#observed-loading-S').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#observed-chart-S').removeClass('hidden');
                $('#observed-chart-S').html(data);

                //resize main graph
                Plotly.Plots.resize($("#observed-chart-S .js-plotly-plot")[0]);
                Plotly.relayout($("#observed-chart-S .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Sediments Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_temperature_info (stationcode, stationname) {
	$('#observed-loading-T').removeClass('hidden');
    $.ajax({
        url: 'get-temperature-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed temperature data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#observed-loading-T').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#observed-chart-T').removeClass('hidden');
                $('#observed-chart-T').html(data);

                //resize main graph
                Plotly.Plots.resize($("#observed-chart-T .js-plotly-plot")[0]);
                Plotly.relayout($("#observed-chart-T .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Temperature Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_precipitation_info (stationcode, stationname) {
	$('#observed-loading-P').removeClass('hidden');
    $.ajax({
        url: 'get-precipitation-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed precipitation data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#observed-loading-P').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#observed-chart-P').removeClass('hidden');
                $('#observed-chart-P').html(data);

                //resize main graph
                Plotly.Plots.resize($("#observed-chart-P .js-plotly-plot")[0]);
                Plotly.relayout($("#observed-chart-P .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Precipitation Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_forest_cover_info (stationcode, stationname) {
	$('#observed-loading-FC').removeClass('hidden');
    $.ajax({
        url: 'get-forest-cover-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed forest cover data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#observed-loading-FC').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#observed-chart-FC').removeClass('hidden');
                $('#observed-chart-FC').html(data);

                //resize main graph
                Plotly.Plots.resize($("#observed-chart-FC .js-plotly-plot")[0]);
                Plotly.relayout($("#observed-chart-FC .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Forest Cover Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_monthly_mean_discharge_data (stationcode, stationname) {
	$('#mean-loading-Q').removeClass('hidden');
    $.ajax({
        url: 'get-monthly-mean-discharge-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed discharge data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#mean-loading-Q').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#mean-chart-Q').removeClass('hidden');
                $('#mean-chart-Q').html(data);

                //resize main graph
                Plotly.Plots.resize($("#mean-chart-Q .js-plotly-plot")[0]);
                Plotly.relayout($("#mean-chart-Q .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Discharge Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_monthly_std_discharge_data (stationcode, stationname) {
	$('#std-loading-Q').removeClass('hidden');
    $.ajax({
        url: 'get-monthly-std-discharge-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed discharge data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#std-loading-Q').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#std-chart-Q').removeClass('hidden');
                $('#std-chart-Q').html(data);

                //resize main graph
                Plotly.Plots.resize($("#std-chart-Q .js-plotly-plot")[0]);
                Plotly.relayout($("#std-chart-Q .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Discharge Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_monthly_max_discharge_data (stationcode, stationname) {
	$('#max-loading-Q').removeClass('hidden');
    $.ajax({
        url: 'get-monthly-max-discharge-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed discharge data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#max-loading-Q').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#max-chart-Q').removeClass('hidden');
                $('#max-chart-Q').html(data);

                //resize main graph
                Plotly.Plots.resize($("#max-chart-Q .js-plotly-plot")[0]);
                Plotly.relayout($("#max-chart-Q .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Discharge Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_monthly_min_discharge_data (stationcode, stationname) {
	$('#min-loading-Q').removeClass('hidden');
    $.ajax({
        url: 'get-monthly-min-discharge-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed discharge data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#min-loading-Q').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#min-chart-Q').removeClass('hidden');
                $('#min-chart-Q').html(data);

                //resize main graph
                Plotly.Plots.resize($("#min-chart-Q .js-plotly-plot")[0]);
                Plotly.relayout($("#min-chart-Q .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Discharge Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_monthly_mean_sediments_data (stationcode, stationname) {
	$('#mean-loading-S').removeClass('hidden');
    $.ajax({
        url: 'get-monthly-mean-sediments-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed sediments data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#mean-loading-S').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#mean-chart-S').removeClass('hidden');
                $('#mean-chart-S').html(data);

                //resize main graph
                Plotly.Plots.resize($("#mean-chart-S .js-plotly-plot")[0]);
                Plotly.relayout($("#mean-chart-S .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Sediments Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_monthly_std_sediments_data (stationcode, stationname) {
	$('#std-loading-S').removeClass('hidden');
    $.ajax({
        url: 'get-monthly-std-sediments-data',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed sediments data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#std-loading-S').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#std-chart-S').removeClass('hidden');
                $('#std-chart-S').html(data);

                //resize main graph
                Plotly.Plots.resize($("#std-chart-S .js-plotly-plot")[0]);
                Plotly.relayout($("#std-chart-S .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Sediments Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_scatterPlot_Q_FC (stationcode, stationname) {
	$('#annual-loading-Q-FC').removeClass('hidden');
    $.ajax({
        url: 'get-scatterPlot-Q-FC',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the observed discharge and/or forecast cover data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#annual-loading-Q-FC').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#annual-chart-Q-FC').removeClass('hidden');
                $('#annual-chart-Q-FC').html(data);

                //resize main graph
                Plotly.Plots.resize($("#annual-chart-Q-FC .js-plotly-plot")[0]);
                Plotly.relayout($("#annual-chart-Q-FC .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Observed Discharge and/or Forecast Cover Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function get_scatterPlot_S_FC (stationcode, stationname) {
	$('#annual-loading-S-FC').removeClass('hidden');
    $.ajax({
        url: 'get-scatterPlot-S-FC',
        type: 'GET',
        data: {'stationcode' : stationcode, 'stationname': stationname},
        error: function () {
            $('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the sediments and/or forecast cover data</strong></p>');
            $('#info').removeClass('hidden');

            setTimeout(function () {
                $('#info').addClass('hidden')
            }, 5000);
        },
        success: function (data) {
            if (!data.error) {
                $('#annual-loading-S-FC').addClass('hidden');
                $('#dates').removeClass('hidden');
                $loading.addClass('hidden');
                $('#annual-chart-S-FC').removeClass('hidden');
                $('#annual-chart-S-FC').html(data);

                //resize main graph
                Plotly.Plots.resize($("#annual-chart-S-FC .js-plotly-plot")[0]);
                Plotly.relayout($("#annual-chart-S-FC .js-plotly-plot")[0], {
                	'xaxis.autorange': true,
                	'yaxis.autorange': true
                });

            } else if (data.error) {
            	$('#info').html('<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the Sediments and/or Forecast Cover Data</strong></p>');
            	$('#info').removeClass('hidden');

            	setTimeout(function() {
            		$('#info').addClass('hidden')
                }, 5000);

            } else {
            	$('#info').html('<p><strong>An unexplainable error occurred.</strong></p>').removeClass('hidden');
            }
        }
    });
};

function resize_graphs() {
    $("#observed_tab_link").click(function() {
        Plotly.Plots.resize($("#observed-chart-Q .js-plotly-plot")[0]);
        Plotly.relayout($("#observed-chart-Q .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#observed-chart-S .js-plotly-plot")[0]);
        Plotly.relayout($("#observed-chart-S .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#observed-chart-T .js-plotly-plot")[0]);
        Plotly.relayout($("#observed-chart-T .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#observed-chart-P .js-plotly-plot")[0]);
        Plotly.relayout($("#observed-chart-P .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#observed-chart-FC .js-plotly-plot")[0]);
        Plotly.relayout($("#observed-chart-FC .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
    });

    $("#monthlyAnalysis_tab_link").click(function() {
        Plotly.Plots.resize($("#mean-chart-Q .js-plotly-plot")[0]);
        Plotly.relayout($("#mean-chart-Q .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#std-chart-Q .js-plotly-plot")[0]);
        Plotly.relayout($("#std-chart-Q .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#max-chart-Q .js-plotly-plot")[0]);
        Plotly.relayout($("#max-chart-Q .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#min-chart-Q .js-plotly-plot")[0]);
        Plotly.relayout($("#min-chart-Q .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#mean-chart-S .js-plotly-plot")[0]);
        Plotly.relayout($("#mean-chart-S .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#std-chart-S .js-plotly-plot")[0]);
        Plotly.relayout($("#std-chart-S .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
    });

    $("#annualAnalysis_tab_link").click(function() {
        Plotly.Plots.resize($("#annual-chart-Q-FC .js-plotly-plot")[0]);
        Plotly.relayout($("#annual-chart-Q-FC .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });
        Plotly.Plots.resize($("#annual-chart-S-FC .js-plotly-plot")[0]);
        Plotly.relayout($("#annual-chart-S-FC .js-plotly-plot")[0], {
        	'xaxis.autorange': true,
        	'yaxis.autorange': true
        });

    });
};



$(function() {

    $("#app-content-wrapper").removeClass('show-nav');
	$(".toggle-nav").removeClass('toggle-nav');

	//make sure active Plotly plots resize on window resize
    window.onresize = function() {
        $('#graph .modal-body .tab-pane.active .js-plotly-plot').each(function(){
            Plotly.Plots.resize($(this)[0]);
        });
    };

    init_map();
    map_events();
    resize_graphs();
});