from flask import Flask, current_app
import numpy
import json
app = Flask(__name__)
from flask_cors import CORS
from scripts import haversine
CORS(app)

_ALL_ROUTES = None


class GlobalRouteHandler(object):
    def __init__(self, *args, **kwargs):
        self._all_routes = open("routes.json", "r").read()
        # this checks to see that the JSON file is valid.
        try:
            self._all_routes = json.loads(self._all_routes)
        except ValueError:
            print "\"Routes.json\" is not a valid JSON file."
            exit(1)
        return super(GlobalRouteHandler, self).__init__(*args, **kwargs)

    def search_route(self, lat, lon):
        self.current_coords = current_route
        coords = str(lat) + '//' + str(lat)
        try:
            self.current_junc = self._all_routes["junctions"][coords]
        except KeyError as e:
            self.current_junc = False
        self.route = current_route
        return current_route

class JunctionHandler(object):
    """This class handles the data of the current junction """

    def __init__(self, current_route=None):
        """Default speed is 30 as this is the most common"""
        if current_route == None:
            self._all_routes = _ALL_ROUTES
            # this is a method call inside the constructure, not ideal but 
            # current route variable needs to be filled.
            self.current_route = self.pick_random_edge_route()
            # current coords is a seperate variable as this is the 'title' for the 
            # object rather than a variable
            self.current_coords = self.process_lat_lon(self.current_route[0])
            self.current_junc = self.current_route[1]
        else:
            if len(current_route) == 2:
                self._all_routes = _ALL_ROUTES['junctions']
                self.current_coords = current_route
                coords = str(current_route[0]) + '//' + str(current_route[1])
                try:
                    self.current_junc = self._all_routes[coords]
                except KeyError as e:
                    self.current_junc = False
                self.route = current_route
        if self.current_junc != False:
            self.junction_name = self.current_junc["junction_name"]
            self.speed = self.current_junc["speed"]
            self.lat = self.current_coords[0]
            self.lon = self.current_coords[1]
            self.route = self.current_junc["routes"]

    def check_if_route_exists(self):
        if self.current_junc != False:
            return True
        else:
            return False

    def process_lat_lon(self, latlon):
        coords = latlon.replace("//", " ").split()
        lat = coords[0]
        lon = coords[1]
        return lat, lon

    def pick_random_edge_route(self):
        routeslist = self._all_routes["junctions_edge"][0]
        # select a random 'route' according to the number
        selection_number = numpy.random.randint(0, len(routeslist))
        # select a junction at random to generate traffic
        selected_route_key = routeslist.keys()
        selected_route_key = selected_route_key[selection_number]
        # pick the junction according to the selected route key
        selected_junction = routeslist[selected_route_key]
        return [selected_route_key, selected_junction]

    def calculate_junction_distance_time(self, newroute):
        distanceM = haversine.get_distance_haversine([float(self.lat), float(self.lon)], [float(newroute['lat']), float(newroute['lon'])])
        # calculate the time needed to get to the junction 
        # by Distance over speed
        time = distanceM / self.speed
        return time

    def generate_route(self):
        """This generates a random route, calling the time function"""
        potential_routes = self.route
        #select a random 'route' according to the number
        selection_number = numpy.random.randint(0, len(potential_routes))
        newroute = potential_routes[selection_number]
        # this will be the time to reach destination
        time = self.calculate_junction_distance_time(newroute)
        route = {"lat": str(self.lat), "lon": str(self.lon), "time": time, "route": {"lat":str(newroute["lat"]), "lon":str(newroute["lon"])}}
        return route




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

@app.route('/MovingMarker.js')
def send_javascript():
    return current_app.send_static_file('MovingMarker.js')

@app.route('/')
def generate_edge_coords():
    junc = JunctionHandler()
    route = junc.generate_route()
    #lat = gen_coord_lat()
    #lon = gen_coord_lon()
    return json.dumps(route)

def GetRoutes():

    globalRoutes = GlobalRouteHandler()
    globalRoutes.search_route(52.632930, -1.161572)

    # load the global variable
    global _ALL_ROUTES
    _ALL_ROUTES = open("routes.json", "r").read()
    # this checks to see that the JSON file is valid.
    try:
        _ALL_ROUTES = json.loads(_ALL_ROUTES)
    except ValueError:
        print "\"Routes.json\" is not a valid JSON file."
        exit(1)

if __name__ == "__main__":
    #gen = GenerateData()
    #r = gen.gen_rand_data()
    # load the routes file
    GetRoutes()
    app.run()