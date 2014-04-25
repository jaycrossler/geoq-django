//converts leaflet layer to WKT
//requires Leaflet, Leaflet ArcGIS plugin,
leaflet_helper = {}

leaflet_helper.styles = {};
leaflet_helper.styles.extentStyle = {"weight":2,"color":"red","fill":null,"opacity":1};
leaflet_helper.styles.completed = {"weight":2,"color":"green","fillColor":"green","fillOpacity":.9,"opacity":1};
leaflet_helper.styles.in_work = {"weight":2,"color":"yellow","fillColor":"orange","fillOpacity":.9,"opacity":1};
leaflet_helper.styles.assigned = {"weight":2,"color":"orange","fillColor":"orange","fillOpacity":.9,"opacity":1};
leaflet_helper.proxy_path = "/geoq/proxy/";


leaflet_helper.layer_conversion = function(lyr){


    options = {
        layers: lyr.layer,
        format: lyr.format,
        transparent: lyr.transparent,
        attribution: lyr.attribution,
        subdomains: lyr.subdomains,
        opacity: lyr.opacity,
        zIndex: lyr.zIndex,
        visibile: lyr.shown
        }
    var layerParams = lyr.layerParams;

    console.log(layerParams);

    var esriPluginInstalled = L.hasOwnProperty('esri');
    var ajaxPluginInstalled = L.hasOwnProperty('ajax');

    if (!esriPluginInstalled){
        console.log('Esri Leaflet plugin not installed.  Esri layer types disabled.');
    }

    if (lyr.type=='WMS'){

        layerOptions = _.extend(options, layerParams);

        return new L.tileLayer.wms(lyr.url, layerOptions);
    }

    if (lyr.type=='ESRI Tiled Map Service' && esriPluginInstalled){

        layerOptions = options;

        return new L.esri.tiledMapLayer(lyr.url, layerOptions);
    }

    if (lyr.type=='ESRI Dynamic Map Layer' && esriPluginInstalled){

        layerOptions = options;

        return new L.esri.dynamicMapLayer(lyr.url, layerOptions);
    }

    if (lyr.type=='ESRI Feature Layer' && esriPluginInstalled){

        layerOptions = options;

        return new L.esri.featureLayer(lyr.url, layerOptions);
    }

    if (lyr.type=='GeoJSON'){
        layerOptions = options;

        var result = $.ajax({
            type: 'GET',
            url: leaflet_helper.proxy_path + encodeURI(lyr.url),
            dataType: 'json',
            async: false
        });

        if ( result.status == 200 ) {
            return new L.GeoJSON(JSON.parse(result.responseText), layerOptions);
        } else {
            return undefined;
        }

    }

    if (lyr.type=='KML') {
        layerOptions = options;
        layerOptions['async'] = true;

        return new L.KML(leaflet_helper.proxy_path + encodeURI(lyr.url), layerOptions);
    }

    if (lyr.type=='KMZ') {
        layerOptions = options;
        return new L.KMZ(leaflet_helper.proxy_path + encodeURI(lyr.url), layerOptions);

/*        function readData(data) {
            var unzip = new JSUnzip();
            unzip.open(data);
            for (f in unzip.files) {
                if (f.lastIndexOf("kml") > 0 ) {
                    var data = unzip.data(f);
                    var reader = new FileReader();
                }
            }

            alert('unzipped file');
        }

        var xhr = new XMLHttpRequest();
        xhr.open("GET", leaflet_helper.proxy_path + encodeURI(lyr.url), true);
        xhr.overrideMimeType("text/plain; charset=x-user-defined");

        xhr.onreadystatechange = function(e) {
            if ( this.readyState == 4 && this.status == 200 ) {
                var kmz = this.responseText;
                readData(kmz);
            }
        };*/

/*        function readData(datablob) {
            var unzipper = new JSUnzip(datablob);
            if (unzipper.isZipFile()) {
                unzipper.readEntries();
                for (var i = 0; i < unzipper.entries.length; i++ ) {
                    var data;
                    if (unzipper.entries[i].compressionMethod === 8 ) {
                        data = JSInflate.inflate(unzipper.entries[i].data);
                    } else {
                        // uncompressed
                        data = unzipper.entries[i].data;
                    }

                    // save to a file location
                    if (filesystem) {
                        filesystem.root.getFile(unzipper.entries[i].fileName, {create: true}, function(fileEntry) {
                            fileEntry.createWriter(function(fileWriter) {
                                fileWriter.onwriteend = function(e) {
                                    return
                                }
                            })
                        }, errorHandler);
                    }

                    console.log("entry:" + unzipper.entries[i].fileName);
                }
            }
        }

        var xhr = new XMLHttpRequest();
        xhr.open("GET", leaflet_helper.proxy_path + encodeURI(lyr.url), true);
        xhr.responseType = 'blob';

        xhr.onload = function(e) {
            if (this.status == 200 ) {
                var datablob = this.response;
                var reader = new window.FileReader();
                reader.readAsBinaryString(datablob);
                reader.onloadend = function() {
                    readData(reader.result);
                }
            }
        }

        xhr.send();*/

    }

}

//TODO: Add MULTIPOLYGON support and commit back to https://gist.github.com/bmcbride/4248238
leaflet_helper.toWKT = function(layer) {
    var lng, lat, coords = [];
    if (layer instanceof L.Polygon || layer instanceof L.Polyline) {
        var latlngs = layer.getLatLngs();
        for (var i = 0; i < latlngs.length; i++) {
	    	latlngs[i]
	    	coords.push(latlngs[i].lng + " " + latlngs[i].lat);
	        if (i === 0) {
	        	lng = latlngs[i].lng;
	        	lat = latlngs[i].lat;
	        }
	};
        if (layer instanceof L.Polygon) {
            return "POLYGON((" + coords.join(",") + "," + lng + " " + lat + "))";
        } else if (layer instanceof L.Polyline) {
            return "LINESTRING(" + coords.join(",") + ")";
        }
    } else if (layer instanceof L.Marker) {
        return "POINT(" + layer.getLatLng().lng + " " + layer.getLatLng().lat + ")";
    }
}


