from flask import Flask, current_app
import numpy
import math
import json
from random import random
from bisect import bisect
app = Flask(__name__)
from flask_cors import CORS
from scripts import haversine
import datetime
CORS(app)

class AllRoutes:
    all_routes = json.loads(open("routes.json", "r").read())
    junction_data = dict()

class GlobalRouteHandler(object):

    def get_current_load(self, coords):
        traffic_load = 0
        for current_datetime in AllRoutes.junction_data.keys():
            # extract out the current coordinates by accessing the object in the dict
            if AllRoutes.junction_data.get(current_datetime) == coords:
                junc_time = AllRoutes.junction_data[current_datetime]
                if current_datetime > datetime.datetime.now()-datetime.timedelta(seconds=8):
                    traffic_load += 6
                else:
                    AllRoutes.junction_data.pop(current_datetime)
        if traffic_load > 100:
            traffic_load = 99
        return traffic_load

    def search_route(self, lat, lon):
        coords = str(lat) + '//' + str(lon)
        try:
            current_junc = AllRoutes.all_routes["junctions"][coords]
        except KeyError as e:
            current_junc = False
        if current_junc != False:
            current_datetime = datetime.datetime.now()
            AllRoutes.junction_data[current_datetime] = coords
            traffic_load = self.get_current_load(coords)
            AllRoutes.all_routes["junctions"][coords]["traffic_load"] = traffic_load

        #self.route = current_route
        return current_junc

    def return_all_junctions(self):
        _all_routes = AllRoutes.all_routes["junctions"]
        junc_list = []
        #print self._junction_data
        for junc in _all_routes:
            #print junc
            j = JunctionHandler()
            lat, lon = j.process_lat_lon(junc)
            junction = {"junction":_all_routes[junc],"lat":lat,"lon":lon}
            junc_list.append(junction)
        return junc_list

class JunctionHandler(object):
    """This class handles the data of the current junction """


    def __init__(self, current_route=None):
        """Default speed is 30 as this is the most common"""
        ## automatically inherit all variables from GlobalRouteHandler class
        super(JunctionHandler, self).__init__()
        if current_route == None:
            self._all_routes = AllRoutes.all_routes
            # this is a method call inside the constructure, not ideal but 
            # current route variable needs to be filled.
            self.current_route = self.pick_random_edge_route()
            # current coords is a seperate variable as this is the 'title' for the 
            # object rather than a variable
            self.current_coords = self.process_lat_lon(self.current_route[0])
            self.current_junc = self.current_route[1]
        else:
            if len(current_route) == 2:
                self.current_junc = globalRoute.search_route(current_route[0], current_route[1])
                self.current_coords = current_route[0], current_route[1]

        if self.current_junc != False:
            self.junction_name = self.current_junc["junction_name"]
            self.speed = self.current_junc["speed"]
            self.lat = self.current_coords[0]
            self.lon = self.current_coords[1]
            self.route = self.current_junc["routes"]

    
    def check_if_route_exists(self):
        #print self.route[0]
        if self.current_junc != False and self.route[0] != {}:
            return True
        else:
            return False

    def weighted_junc_search(self):
        potential_routes = self.route
        road_type_list = []
        i = 0
        if len(potential_routes) != 1:
            for route in potential_routes:
                road_type = route["road_type"]
                if road_type == 1:
                    road_type = 50
                elif road_type == 2:
                    road_type = 30
                elif road_type == 3:
                    road_type = 15
                else:
                    road_type = 5
                route_with_weighting = [i, road_type]
                road_type_list.append(route_with_weighting)
                i += 1
                #print road_type
            number = self.weighted_choice(road_type_list)
        else:
            number = 0
        return number

    def weighted_choice(self, choices):
        ''' This function ensures that each route 
        has a weighted choice so traffic keeps to 
        trunk roads '''
        print choices
        total = 0
        cum_weights = []
        for choice in choices:
            total += choice[1]
            cum_weights.append(total)
        x = random() * total
        i = bisect(cum_weights, x)
        return i


    def process_lat_lon(self, latlon):
        coords = latlon.replace("//", " ").split()
        lat = coords[0]
        lon = coords[1]
        return lat, lon

    def pick_random_edge_route(self):
        routeslist = AllRoutes.all_routes["junctions_edge"][0]
        # select a random 'route' according to the number
        selection_number = numpy.random.randint(0, len(routeslist))
        # select a junction at random to generate traffic
        selected_route_key = routeslist.keys()
        selected_route_key = selected_route_key[selection_number]
        # pick the junction according to the selected route key
        selected_junction = routeslist[selected_route_key]
        return [selected_route_key, selected_junction]

    def calculate_junction_distance_time(self, newroute, traffic_load):
        distanceM = haversine.get_distance_haversine([float(self.lat), float(self.lon)], [float(newroute['lat']), float(newroute['lon'])])
        # calculate the time needed to get to the junction 
        # by Distance over speed
        time = distanceM / self.speed
        if traffic_load >= 90:
            time = time * 7
        elif traffic_load > 75:
            new_exp = traffic_load - 75
            #traffic_load = traffic_load * time
            new_time = math.exp(new_exp) / 2
            print time
            time = new_time
        else:
            time = time * 1.25
        return time

    def generate_route(self):
        """This generates a random route, calling the time function"""
        potential_routes = self.route
        #select a random 'route' according to the number
        selection_number = self.weighted_junc_search()
        newroute = potential_routes[selection_number]
        traffic_load = globalRoute.get_current_load(self.lat + "//" + self.lon)
        # this will be the time to reach destination
        time = self.calculate_junction_distance_time(newroute, traffic_load)
        route = {"lat": str(self.lat), "lon": str(self.lon), "time": time, "route": {"lat":str(newroute["lat"]), "lon":str(newroute["lon"])}}
        return route


class EmergencyHandler(JunctionHandler):

    def __init__(self, *args, **kwargs):
        return super(EmergencyHandler, self).__init__(*args, **kwargs)

    def generate_emergency(self):
        route = self.generate_route()
        print "not implemented yet."



@app.route('/coordinates/<coordinates>', methods = ['GET'])
def coords(coordinates):
    lat_lon = coordinates.split(":")
    lat = str(lat_lon[0])
    lon = str(lat_lon[1])
    Junction = JunctionHandler([lat,lon])
    routeExists = Junction.check_if_route_exists()
    if routeExists != False:
        route = Junction.generate_route()
        return json.dumps(route)
    else:
        return json.dumps(False)

@app.route('/index.html')
def send_homepage():
    return current_app.send_static_file('index.html')

@app.route('/junc_icon.png')
def send_junc_icon():
    return current_app.send_static_file('junc_icon.png')

@app.route('/all_juncts')
def return_all_junctions():
    all_junctions = globalRoute.return_all_junctions()
    return json.dumps(all_junctions)

@app.route('/MovingMarker.js')
def send_javascript():
    return current_app.send_static_file('MovingMarker.js')


@app.route('/generate_emergency')
def generate_emergency_route():
    return json.dumps({"hello":"world"})


@app.route('/')
def generate_edge_coords():
    junc = JunctionHandler()
    route = junc.generate_route()
    #lat = gen_coord_lat()
    #lon = gen_coord_lon()
    return json.dumps(route)

def GetRoutes():

    #globalRoutes = GlobalRouteHandler()
    #print globalRoutes.search_route(52.634169, -1.149998)

    # load the global variable
    global _ALL_ROUTES
    _ALL_ROUTES = open("routes.json", "r").read()
    # this checks to see that the JSON file is valid.
    try:
        _ALL_ROUTES = json.loads(_ALL_ROUTES)
    except ValueError:
        print "\"Routes.json\" is not a valid JSON file."
        exit(1)

globalRoute = GlobalRouteHandler()
if __name__ == "__main__":
    #gen = GenerateData()
    #r = gen.gen_rand_data()
    # load the routes file
    app.run(host='0.0.0.0')