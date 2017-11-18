from flask import Flask, current_app
import numpy
import json
app = Flask(__name__)
from flask_cors import CORS
CORS(app)

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
        route_data = self.return_data(routeslist, selected_route_key)
        return route_data

    def return_data(self, routeslist, selected_route_key):
        try:
            selected_route = routeslist[selected_route_key]["routes"]
        except KeyError:
            return False
        selection_number = numpy.random.randint(0, len(selected_route))
        selected_route = selected_route[selection_number]
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
        route_data = self.return_data(selected_route, coords)
        return route_data


@app.route('/coordinates/<coordinates>', methods = ['GET'])
def coords(coordinates):
    lat_lon = coordinates.split(":")
    lat = str(lat_lon[0])
    lon = str(lat_lon[1])
    l = GenerateData()
    coords = l.get_rand_junct_data(lat, lon)
    if isinstance(coords, bool):
        return json.dumps(False)
    else:
        return json.dumps({"lat":coords[0], "lon":coords[1], "route":{"lat":coords[2]["lat"], "lon":coords[2]["lon"]}})

@app.route('/index.html')
def send_homepage():
    return current_app.send_static_file('index.html')

@app.route('/MovingMarker.js')
def send_javascript():
    return current_app.send_static_file('MovingMarker.js')

@app.route('/')
def generate_edge_coords():
    gen = GenerateData()
    coords = gen.gen_rand_data()
    #lat = gen_coord_lat()
    #lon = gen_coord_lon()
    print coords[2]
    return json.dumps({"lat":coords[0], "lon":coords[1], "route":{"lat":coords[2]["lat"], "lon":coords[2]["lon"]}})

if __name__ == "__main__":
    #gen = GenerateData()
    #r = gen.gen_rand_data()
    app.run()