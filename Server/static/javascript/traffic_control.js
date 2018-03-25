// this is the global variable for the emergency vehicle
var EmergencyLine;
// this is the global token for the authenticated user to activate an emergency
var token;
var EmergencyInterval;
// this is the Non dynamic route stored in the browser for the time function
var OldRoute;

var showJunctions = false;


self.addEventListener('Start Emergency', function (e) {
    // code to be run
    GenerateEmergency();
});

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
    //clearInterval(JuncInterval);
    for (var i = 0; i < markers.length; i++) {
        map.removeLayer(markers[i]);
    }
    showJunctions = false;
    //markers = []
}



/// this is the prepShowJunction handler 
// with a parameter for usage by the add_junction page.
function PrepShowJunction(JunctionMarkerBind = false) {
    showJunctions = true;
    if (JunctionMarkerBind == false) {
        JuncInterval = window.setInterval(function () {
            ShowJunction();
        }, 1000);
    }
    else {
        // this runs if the parameter has been added
        ShowJunction(JunctionMarkerBind);
    }
}

var images = new Array()
/// this is our pre loading function
/// for all of our junction icons.
function PreLoad() {
    function preload() {
        for (i = 0; i < preload.arguments.length; i++) {
            // this is so that the image is pre loaded
            var img = new Image();
            img.src = preload.arguments[i];
            var juncIcon = L.icon({
                iconUrl: preload.arguments[i],
                iconSize: [32, 32],
                shadowSize: [0, 0]
            });
            images[i] = juncIcon
        }
    }
    preload(
        "../junc_icon9.png",
        "../junc_icon35.png",
        "../junc_icon70.png",
        "../junc_icon95.png",
        "../junc_iconundefined.png"
    )
}

PreLoad()


if (typeof markers !== 'undefined') {
    // markers is defined
    // this is used as not everything utilises 
    // the mapping stuff

    // this is a general cleanup function
    // incase a marker timesout
    var interval = window.setInterval(function () {
        var TwentySecs = 20 * 1000; /* ms */
        var TimeNow = Date.now();
        for (var i = 0; i < markers.length; i++) {
            var MarkerTimestamp = markers[i][1]
            if (TimeNow - MarkerTimestamp > TwentySecs) {
                // this removes the marker from the map
                // if the marker hasn't reached a new junction
                // within 20 seconds.
                map.removeLayer(markers[i][0]);
            }
            //console.log(markers[i]);
        }
    }, 2000);
}



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
    //showJunctions = true
    httpGetAsync("/all_juncts", ProcessJunctions, null, null, null, JunctionMarkerBind)
}



function ProcessJunctions(JunctionData, JunctionMarkerBind=false) {
    JunctionData = JSON.parse(JunctionData);
    var i;
    for (i in JunctionData) {
        var lat = Number(JunctionData[i].lat);
        var lon = Number(JunctionData[i].lon);
        var pos = markers.indexOf(lat + ":" + lon);
        if (showJunctions != false) {
            if (pos == -1) {
                // this creates the 'default' junction icon
                var juncIcon = L.icon({
                    iconUrl: '../junc_iconundefined.png',
                    iconSize: [32, 32],
                    shadowSize: [0, 0]
                });
                if (JunctionMarkerBind != false) {
                    /// this if statement runs if the user is in ADD JUNCTION mode.
                    var myMarker = new customMarkerRoute([lat, lon], {
                        icon: juncIcon,
                        CustomData: JunctionData[i].junction.junction_name,
                        CustomLatLon: JunctionData[i].lat + '//' + JunctionData[i].lon
                    }).on('click', JunctionMarkerBind).addTo(map);
                    //marker = L.marker([lat, lon], { icon: juncIcon }, { 'title': 'title' }).on('click', JunctionMarkerBind).addTo(map);
                }
                else {
                    traffic_load_amount = JunctionData[i].junction.routes[0].traffic_load;
                    juncIcon = L.icon({
                        iconUrl: '../junc_icon' + traffic_load_amount + '.png',
                        iconSize: [32, 32],
                        shadowSize: [0, 0]
                    });
                    marker = L.marker([lat, lon], { icon: juncIcon }).addTo(map);
                    marker.bindPopup("<b>" + JunctionData[i].junction.junction_name + "</b>" + "<br>" + "traffic load:" + JunctionData[i].junction.routes[0].traffic_load);
                    markers.push(marker, lat + ":" + lon);
                }
                //var marker = L.marker([40.68510, -73.94136]).addTo(map);
            }
            else {
                traffic_load_amount = JunctionData[i].junction.routes[0].traffic_load;
                // here we make the loads generic to stop the browser pulling many different
                // images
                var juncIcon;
                if (traffic_load_amount <= 10) {
                    juncIcon = images[0]
                }
                else if (traffic_load_amount <= 40) {
                    juncIcon = images[1]
                }
                else if (traffic_load_amount <= 75) {
                    juncIcon = images[2]
                }
                else if (traffic_load_amount <= 100) {
                    juncIcon = images[3]
                }
                else {
                    juncIcon = images[4]
                }
                //var juncIcon = L.icon({
                //    iconUrl: IconUrl,
                //    iconSize: [32, 32],
                //    shadowSize: [0, 0]
                //});
                // this is minus one because we have added both the marker and the latitude/longitude values
                marker = markers[pos - 1];
                marker.setIcon(juncIcon);
                marker._popup.setContent("<b>" + JunctionData[i].junction.junction_name + "</b>" + "<br>" + "traffic load:" + JunctionData[i].junction.routes[0].traffic_load);
            }
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
            clearInterval(EmergencyInterval);
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
    [minutes, seconds] = ProcessTimeTaken(time)
    document.getElementById('time_taken_non_dynamic_minutes').innerHTML = minutes.toString();
    document.getElementById('time_taken_non_dynamic_seconds').innerHTML = seconds.toString();
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
        }, 2000);
    }
}

///
/// this code is for the data analytics of the results
/// 
///

//var dynamic = [];
//var non_dynamic = [];
//interval = window.setInterval(function ()
//{
//    var temp = "time_taken";
//    var obj = document.getElementById(temp).innerHTML;
//    console.log(obj);
//    dynamic.push(obj);
//    var temp = "time_taken_non_dynamic";
//    var obj = document.getElementById(temp).innerHTML;
//    console.log(obj);
//    non_dynamic.push(obj);
//    console.log(JSON.stringify(dynamic));
//    console.log(JSON.stringify(non_dynamic));
//    //console.log(document.getElementById("time_taken_non_dynamic").value)
//}, 3000)

function ProcessTimeTaken(time_taken)
{
    var minutes = Math.floor(time_taken / 60);
    // keep the integer at an acceptable two decimal places.
    var seconds = (time_taken - minutes * 60).toFixed(2);
    return [minutes, seconds]
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
            [minutes, seconds] = ProcessTimeTaken(time_taken);
            //alert("minutes"+minutes.toString()+"seconds:"+seconds.toString())
            document.getElementById('time_taken_dynamic_minutes').innerHTML = minutes.toString();
            document.getElementById('time_taken_dynamic_seconds').innerHTML = seconds.toString();
        }
        else
        {
            OldRoute = route;
            var oldemergency = L.polyline(route, { color: 'red' }).addTo(map);
            EmergencyLine = L.polyline(route, { color: 'green' }).addTo(map);
            [minutes, seconds] = ProcessTimeTaken(time_taken);
            document.getElementById('time_taken_non_dynamic_minutes').innerHTML = minutes.toString();
            //alert("minutes"+minutes.toString()+"seconds:"+seconds.toString())
            //document.getElementById('time_taken_non_dynamic_minutes').innerHTML = minutes.toString();
            //document.getElementById('time_taken_non_dynamic_seconds').innerHTML = seconds.toString();

            document.getElementById('time_taken_non_dynamic_seconds').innerHTML = seconds.toString();
            /// this needs to be repeated as it is the first time of running.
            document.getElementById('time_taken_dynamic_minutes').innerHTML = minutes.toString();
            document.getElementById('time_taken_dynamic_seconds').innerHTML = seconds.toString();

        }
    }
    else
    {
        alert(message);
    }
}




function StartSimulation()
{
    // make sure we start the generate emergency simulation aspect.
    setTimeout(GenerateEmergency, 0);
    //GenerateEmergency();
    var xhr = new XMLHttpRequest();

    new_vehicles = document.getElementById('new_vehicles').value;

    total_vehicles = document.getElementById('total_vehicles').value;

    if (!new_vehicles) {
        new_vehicles = 10
        total_vehicles = 100
    }

    xhr.open('GET', '/start_simulation', true);

    xhr.setRequestHeader('Auth-Token', AuthToken);
    xhr.setRequestHeader('New-Vehicles', new_vehicles);
    xhr.setRequestHeader('Total-Vehicles', total_vehicles);

    xhr.onreadystatechange = function ()
    {
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            // Request finished and success here
            //console.log(xhr.XMLHttpRequest);
            response = JSON.parse(xhr.responseText);
            if (response[0] == true)
            {
                console.log("Simulation Server Started");
                document.getElementById('new_vehicles').value = "";

                document.getElementById('total_vehicles').value = "";
                document.getElementById('SimulationForm').style.display = "none";
            }
            else
            {
                alert("Error" + response[1].toString())
                clearInterval(EmergencyInterval);
            }
        }
        else if (xhr.status != 200) {
            alert(xhr.responseText.toString())
        }
    }
    xhr.send(null);
}

function ShowSimulationForm() {

    document.getElementById('SimulationForm').style.display = "block";
    // make sure we scroll to the bottom of the page to show
    // new elements
    window.scrollTo(0, document.body.scrollHeight);
}