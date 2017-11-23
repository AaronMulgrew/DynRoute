from flask import Flask, current_app
import numpy
import json
app = Flask(__name__)
from flask_cors import CORS
from scripts import haversine
CORS(app)

_ALL_ROUTES = None

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
            self.current_coords = self.process_latlon(self.current_route[0])
            self.current_junc = self.current_route[1]
        else:
            if len(current_route) == 2:
                print _ALL_ROUTES
                self._all_routes = _ALL_ROUTES['junctions']
                self.current_coords = current_route
                coords = str(current_route[0]) + '//' + str(current_route[1])
                try:
                    self.current_junc = self._all_routes[coords]
                except KeyError as e:
                    self.current_junc = False
                self.current_route = 222
                self.route = current_route
        self.junction_name = self.current_junc["junction_name"]
        self.speed = self.current_junc["speed"]
        self.lat = self.current_coords[0]
        self.lon = self.current_coords[1]
        self.route = self.current_junc["routes"]

    def process_latlon(self, latlon):
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
        route = {"lat": self.lat, "lon": self.lon, "time": time, "route": {"lat":newroute["lat"], "lon":newroute["lon"]}}
        return route


class GenerateData(object):

    def __init__(self, *args, **kwargs):
        # load the routes file
        routes = open("routes.json", "r").read()
        print routes
        # this checks to see that the JSON file is valid.
        try:
            self.routes = json.loads(routes)
        except ValueError:
            print "\"Routes.json\" is not a valid JSON file."
            exit(1)
        return super(GenerateData, self).__init__(*args, **kwargs)

    def gen_rand_data(self):
        routes = self.routes
        routeslist = routes["junctions_edge"][0]
        # select a random 'route' according to the number
        selection_number = numpy.random.randint(0, len(routeslist))
        # select a junction at random to generate traffic
        selected_route_key = routeslist.keys()
        selected_route_key = selected_route_key[selection_number]
        #for key in selected_route_key:
        #    if '//' in key:
        #selected_route_key = key
        #routeslist = routeslist[selection_number]
        route_data = self.process_routes(routeslist, selected_route_key)
        return route_data

    def process_routes(self, routeslist, selected_route_key):
        try:
            selected_route = routeslist[selected_route_key]
        except KeyError:
            return False

        selection_number = numpy.random.randint(0, len(potential_routes))
        speed = selected_route['speed']
        selected_route = potential_routes[selection_number]
        print len(selected_route)
        coords = selected_route_key.replace("//", " ").split()
        latitude = coords[0]
        longtitude = coords[1]
        return latitude, longtitude, selected_route

    def get_rand_junct_data(self, lat, lon):
        routes = self.routes
        routeslist = routes["junctions"]
        coords = str(lat) + '//' + str(lon)
        # select a random 'route' according to the number
        #selection_number = numpy.random.randint(0, len(routeslist))
        selected_route = routeslist
        self.junction([lat, lon])
        print self.junction
        route_data = self.process_routes(selected_route, coords)
        return route_data


@app.route('/coordinates/<coordinates>', methods = ['GET'])
def coords(coordinates):
    lat_lon = coordinates.split(":")
    lat = str(lat_lon[0])
    lon = str(lat_lon[1])
    Junction = JunctionHandler([lat,lon])
    route = Junction.generate_route()
    return json.dumps(route)

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

if __name__ == "__main__":
    #gen = GenerateData()
    #r = gen.gen_rand_data()
    # load the routes file
    _ALL_ROUTES = open("routes.json", "r").read()
    # this checks to see that the JSON file is valid.
    try:
        _ALL_ROUTES = json.loads(_ALL_ROUTES)
    except ValueError:
        print "\"Routes.json\" is not a valid JSON file."
        exit(1)
    app.run()