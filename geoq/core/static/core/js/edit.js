//requires leaflet_helper.js, underscore, jquery, leaflet

var aoi_feature_edit = {};

aoi_feature_edit.options={
    drawControlLocation:"topleft"
}

aoi_feature_edit.init = function(aoi_id, aoi_map_json, aoi_extent, job_features_geojson, feature_types, create_feature_url){
    aoi_feature_edit.aoi_id = aoi_id;
    aoi_feature_edit.aoi_map_json = aoi_map_json;
    aoi_feature_edit.aoi_extents_geojson = aoi_extent;
    aoi_feature_edit.job_features_geojson = job_features_geojson;
    aoi_feature_edit.feature_types = feature_types;
    aoi_feature_edit.create_feature_url = create_feature_url;
    aoi_feature_edit.drawcontrol = null;
}

aoi_feature_edit.get_feature_type = function(i){
    return aoi_feature_edit.feature_types[i]
}

aoi_feature_edit.map_init = function(map, bounds){
    custom_map = aoi_feature_edit.aoi_map_json;
    aoi_feature_edit.map = map;

    var baseLayers = {}
    var layerSwitcher = {};
    //var editableLayers = new L.FeatureGroup();

    if (custom_map.hasOwnProperty("layers")){
        _.each(custom_map.layers, function(l){
            n = leaflet_helper.layer_conversion(l);

            if (n!==undefined){
                if (l.isBaseLayer){
                    baseLayers[l.name]=n
                    console.log("Added " + l.name + "as a base layer.")
                }else{
                    layerSwitcher[l.name]= n;
                    console.log("Added " + l.name + "as a layer.")
                }
            }
        });
    }

    L.control.layers(baseLayers, layerSwitcher).addTo(aoi_feature_edit.map);

    aoi_extents=L.geoJson(aoi_feature_edit.aoi_extents_geojson,
            {style: leaflet_helper.styles.extentStyle,
             zIndex:1000
            });

    aoi_extents.addTo(aoi_feature_edit.map);

    features = L.geoJson(aoi_feature_edit.job_features_geojson,
            {style: function(feature){
                feature_type = aoi_feature_edit.feature_types[feature.properties.template];
                if (feature_type && feature_type.hasOwnProperty("style")){
                  return feature_type.style;
                };
            }

            }).addTo(aoi_feature_edit.map);

    setTimeout(function(){aoi_feature_edit.map.fitBounds(aoi_extents.getBounds())}, 1);

    var drawnItems = new L.FeatureGroup();
    aoi_feature_edit.map.addLayer(drawnItems);

    drawControl = new L.Control.Draw({
        draw: {
            position: aoi_feature_edit.options.drawControlLocation,
            polygon: {
                title: 'Draw a polygon!',
                allowIntersection: false,
                drawError: {
                    color: '#b00b00',
                    timeout: 1000
                },
                shapeOptions: aoi_feature_edit.get_feature_type(aoi_feature_edit.current_feature_type_id).style,
                showArea: true
            },
            circle: false,
            rectangle: {
                shapeOptions: aoi_feature_edit.feature_types[aoi_feature_edit.current_feature_type_id].style
            }
        },
        edit: {
            featureGroup: drawnItems
        }
    });

    aoi_feature_edit.map.addControl(drawControl);
    aoi_feature_edit.drawcontrol=drawControl;

    map.on('draw:created', function (e) {
        var type = e.layerType;
        var	layer = e.layer;

        geojson = e.layer.toGeoJSON();
        geojson.properties.template=aoi_feature_edit.current_feature_type_id;
        geojson = JSON.stringify(geojson);

        $.ajax({
                  type: "POST",
                  url: aoi_feature_edit.create_feature_url,
                  data: { aoi: aoi_feature_edit.aoi_id,
                          geometry: geojson
                  },
                  success: alert,
                  dataType: "json"
                });

        //layer.bindPopup('Feature Created!');
        drawnItems.addLayer(layer);
    });

}

// Changes current features to match the selected style.
aoi_feature_edit.updateDrawOptions = function(i){
    aoi_feature_edit.drawcontrol.setDrawingOptions({ polygon: { shapeOptions:  aoi_feature_edit.feature_types[i].style },
                                                     rectangle: { shapeOptions:  aoi_feature_edit.feature_types[i].style}
    });
}


aoi_feature_edit.getDrawConsole = function(){

    var geometry_type = null;

    if (aoi_feature_edit.hasOwnProperty("current_feature_type_id")){
        feature_id = aoi_feature_edit.current_feature_type_id;
        geometry_type = aoi_feature_edit.feature_types[feature_id].type;
    }

    if (geometry_type){
        if (geometry_type!="Polygon"){
            marker = false;
        }
        if (geometry_type==="Point"){
            polygon = false;
            rectangle = false;
        }
    }

}

// Filters the draw control to allow acceptable feature types.
aoi_feature_edit.filterDrawConsole = function(){
    control = aoi_feature_edit.drawcontrol;
    geometry_type = aoi_feature_edit.feature_types[aoi_feature_edit.current_feature_type_id].type;
    map = control._map;
    map.removeControl(control);
}

aoi_feature_edit.addOptions=function(feature, div){
    t = _.template("<option value='{{id}}'>{{name}}</option>")
    $("#"+div).append(t(feature));
}


