// this is the global variable for the emergency vehicle
var EmergencyLine;
// this is the global token for the authenticated user to activate an emergency
var token;
var EmergencyInterval;
// this is the Non dynamic route stored in the browser for the time function
var OldRoute;

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
            // this creates the 'default' junction icon
            var juncIcon = L.icon({
                iconUrl: '../junc_icondefault.png',
                iconSize: [32, 32],
                shadowSize: [0, 0]
            });
            if (JunctionMarkerBind != false)
            {
                /// this if statement runs if the user is in ADD JUNCTION mode.
                var myMarker = new customMarkerRoute([lat, lon], {
                    icon: juncIcon,
                    CustomData: JunctionData[i].junction.junction_name,
                    CustomLatLon: JunctionData[i].lat+'//'+JunctionData[i].lon
                }).on('click', JunctionMarkerBind).addTo(map);
                //marker = L.marker([lat, lon], { icon: juncIcon }, { 'title': 'title' }).on('click', JunctionMarkerBind).addTo(map);
            }
            else
            {
                juncIcon = L.icon({
                    iconUrl: 'junc_icon' + JunctionData[i].junction.routes[0].traffic_load + '.png',
                    iconSize: [32, 32],
                    shadowSize: [0, 0]
                });
                marker = L.marker([lat, lon], { icon: juncIcon }).addTo(map);
                marker.bindPopup("<b>" + JunctionData[i].junction.junction_name + "</b>" + "<br>" + "traffic load:" + JunctionData[i].junction.routes[0].traffic_load);
                markers.push(marker, lat + ":" + lon);
            }
            //var marker = L.marker([40.68510, -73.94136]).addTo(map);
        }
        else
        {
            var juncIcon = L.icon({
                iconUrl: 'junc_icon' + JunctionData[i].junction.routes[0].traffic_load + '.png',
                iconSize: [32, 32],
                shadowSize: [0, 0]
            });
            // this is minus one because we have added both the marker and the latitude/longitude values
            marker = markers[pos - 1];
            marker.setIcon(juncIcon);
            marker._popup.setContent("<b>" + JunctionData[i].junction.junction_name + "</b>" + "<br>" + "traffic load:" + JunctionData[i].junction.routes[0].traffic_load);
        }

    }
    //console.log(JunctionData);
}

function httpGetAsync(theUrl, callback, marker = null, header = null, value = null, JunctionMarkerBind = null) {
    /// this is handler for getting HTTP requests with a callback function
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function ()
    {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            //console.log(xmlHttp.responseText);
            if (marker) {
                callback(xmlHttp.responseText, marker);
            }
            else {
                if (JunctionMarkerBind) {
                    callback(xmlHttp.responseText, JunctionMarkerBind)
                }
                else {
                    callback(xmlHttp.responseText);
                }
            }
        }
        else if (xmlHttp.status == 401)
        {
            alert("Token Expired or no token provided!");
        }
        else if (xmlHttp.status != 200)
        {
            console.log("Error!", xmlHttp.status.toString());
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

function ProcessRouteTime(time) {
    time = JSON.parse(time);
    document.getElementById('time_taken_non_dynamic').innerHTML = time.toString();

}

function GenerateEmergency() {
    //console.log(sessionStorage);
    if (EmergencyLine) {
        httpGetAsync("/generate_emergency", ProcessEmergency, null, 'auth_token', AuthToken, null, EmergencyLine);
        httpGetAsync("/calculate_time", ProcessRouteTime, null, "route", JSON.stringify(OldRoute))
    }
    else
    {
        httpGetAsync("/generate_emergency", ProcessEmergency, null, 'auth_token', AuthToken);
    }
    if (EmergencyInterval) {}
    else
    {
        EmergencyInterval = window.setInterval(function () {
            GenerateEmergency();
        }, 4000);
    }
}

function ProcessEmergency(message)
{
    if (CheckJson(message))
    {
        message = JSON.parse(message);
        route = message.route;
        time_taken = message.time;
        document.getElementById('TimeTaken').style.display = "block";
        if (EmergencyLine)
        {
            map.removeLayer(EmergencyLine);
            EmergencyLine = L.polyline(route, { color: 'green' }).addTo(map);
            document.getElementById('time_taken').innerHTML = time_taken.toString();
        }
        else
        {
            OldRoute = route;
            var oldemergency = L.polyline(route, { color: 'red' }).addTo(map);
            EmergencyLine = L.polyline(route, { color: 'green' }).addTo(map);
            document.getElementById('time_taken_non_dynamic').innerHTML = time_taken.toString();
        }
    }
    else
    {
        alert(message);
    }
}

