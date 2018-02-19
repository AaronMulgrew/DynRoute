

var token;

function init(authToken)
{
    token = AuthToken;
}

function removeMarker(selectedMarker) {
    if (selectedMarker) {
        map.removeLayer(selectedMarker);
    }
}

function HideJunctions() {
    clearInterval(JuncInterval);
    for (var i = 0; i < markers.length; i++) {
        map.removeLayer(markers[i]);
    }
    showJunctions = false;
    markers = []
}



function PrepShowJunction() {
    JuncInterval = window.setInterval(function () {
        ShowJunction();
    }, 1000);
}

// this is a general cleanup function
// incase a marker timesout
var interval = window.setInterval(function () {
    var TwentySecs = 20 * 1000; /* ms */
    var TimeNow = Date.now();
    for (var i = 0; i < markers.length; i++) {
        var MarkerTimestamp = markers[i][1]
        if (TimeNow - MarkerTimestamp > TwentySecs)
        {
            // this removes the marker from the map
            // if the marker hasn't reached a new junction
            // within 20 seconds.
            map.removeLayer(markers[i][0]);
        }
        //console.log(markers[i]);
    }
}, 2000);

function ShowJunction(JunctionMarkerBind=false) {
    if (JunctionMarkerBind == false)
    {
        if (showJunctions == false)
        {
            for (var i = 0; i < markers.length; i++)
            {
                map.removeLayer(markers[i]);
            }
            // make sure we clear the markers array
            markers = []
        }
    }
    showJunctions = true
    httpGetAsync("/all_juncts", ProcessJunctions, null, null, null, JunctionMarkerBind)
}



function ProcessJunctions(JunctionData, JunctionMarkerBind=false) {
    JunctionData = JSON.parse(JunctionData);
    var i;
    for (i in JunctionData) {
        var lat = Number(JunctionData[i].lat);
        var lon = Number(JunctionData[i].lon);
        var pos = markers.indexOf(lat + ":" + lon);
        if (pos == -1) {
            if (JunctionMarkerBind != false)
            {
                var myMarker = new customMarkerRoute([lat, lon], {
                    icon: juncIcon,
                    CustomData: JunctionData[i].junction.junction_name,
                    CustomLatLon: JunctionData[i].lat+'//'+JunctionData[i].lon
                }).on('click', JunctionMarkerBind).addTo(map);
                //marker = L.marker([lat, lon], { icon: juncIcon }, { 'title': 'title' }).on('click', JunctionMarkerBind).addTo(map);
            }
            else
            {
                marker = L.marker([lat, lon], { icon: juncIcon }).addTo(map);
                marker.bindPopup("<b>" + JunctionData[i].junction.junction_name + "</b>" + "<br>" + "traffic load:" + JunctionData[i].junction.traffic_load);
                markers.push(marker, lat + ":" + lon);
            }
            //var marker = L.marker([40.68510, -73.94136]).addTo(map);
        }
        else {
            // this is minus one because we have added both the marker and the latitude/longitude values
            marker = markers[pos - 1]
            marker._popup.setContent("<b>" + JunctionData[i].junction.junction_name + "</b>" + "<br>" + "traffic load:" + JunctionData[i].junction.traffic_load);
        }

    }
    //console.log(JunctionData);
}

function httpGetAsync(theUrl, callback, marker = null, header = null, value = null, JunctionMarkerBind = null) {
    /// this is handler for getting HTTP requests with a callback function
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function ()
    {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
        {
            //console.log(xmlHttp.responseText);
            if (marker)
            {
                callback(xmlHttp.responseText, marker);
            }
            else
            {
                if (JunctionMarkerBind) {
                    callback(xmlHttp.responseText, JunctionMarkerBind)
                }
                else
                {
                    callback(xmlHttp.responseText);
                }
            }
        }
    }
    xmlHttp.open("GET", theUrl, true);
    if (header) {
        xmlHttp.setRequestHeader(header, value)
    }
    xmlHttp.send(null);
}


function process_coord(data, myMovingMarker = null) {
    if (data === "false" || !data) {
        removeMarker(myMovingMarker);
    }
    else {
        if (myMovingMarker) {
            removeMarker(myMovingMarker);
        }
        var obj = JSON.parse(data);

        // convert the time in miliseconds to seconds
        timeSecs = obj.time * 1000;

        //console.log(obj);
        if (showJunctions != true) {
            var myMovingMarker = L.Marker.movingMarker([[obj.lat, obj.lon], [obj.route.lat, obj.route.lon]],
                [timeSecs]).addTo(map);
            markers.push([myMovingMarker, Date.now()]);
            myMovingMarker.start();
        }
        setTimeout(NewCoords, timeSecs, [obj.route.lat, obj.route.lon], myMovingMarker);
    }
}

function CheckJson(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}


function NewCoords(latlon, marker) {
    latitude = latlon[0];
    longitude = latlon[1];
    httpGetAsync("/coordinates/" + latitude + ":" + longitude, process_coord, marker);
    //console.log(latlon);
}

function GenerateEmergency() {
    //console.log(sessionStorage);
    httpGetAsync("/generate_emergency", ProcessEmergency,null,'auth_token', AuthToken);
}

function ProcessEmergency(message)
{
    if (CheckJson(message))
    {
        message = JSON.parse(message);
        console.log(message);
        //var latlngs = [
        //    [Number(message.lat), Number(message.lon)],
        //    [Number(message.route.lat), Number(message.route.lon)]
        //];
        var polyline = L.polyline(message, { color: 'red' }).addTo(map);
    }
    else
    {
        alert(message);
    }
}

