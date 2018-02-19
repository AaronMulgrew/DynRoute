import json
from scripts import haversine
from models import traffic_heuristics

class AllRoutes(object):
    def __init__(self):
        self.all_routes = json.loads(open("routes.json", "r").read())
        # this is the 'live' junction data dictionary
        # it contains a series of dateTime entries
        # that will iterated over from the code
        self.junction_data = dict()

    ''' this is a module that populates the default time values
    to ensure the emergency vehicle algorithm works as expected.'''
    def populate_all_routes(self):
        for lat_lon in self.all_routes['junctions_edge']:
            junc = self.all_routes['junctions_edge'][lat_lon]
            source_lat, source_lon = lat_lon.split('//')
            for route in junc['routes']:
                # get the distance in meters
                distanceM = haversine.get_distance_haversine([source_lat, source_lon, route['lat'], route['lon']])
                time = distanceM / junc['speed']
                # this code runs on startup so default value will be 0
                traffic_load = 0
                time = traffic_heuristics.handle_time(route, time, traffic_load)
                self.update_current_time(source_lat, source_lon, route['lat'], route['lon'], time)
        for lat_lon in self.all_routes['junctions']:
            junc = self.all_routes['junctions'][lat_lon]
            source_lat, source_lon = lat_lon.split('//')
            for route in junc['routes']:
                try:
                    # get the distance in meters
                    distanceM = haversine.get_distance_haversine([source_lat, source_lon, route['lat'], route['lon']])
                except KeyError:
                    continue
                time = distanceM / float(junc['speed'])
                # this code runs on startup so default value will be 0
                traffic_load = 0
                time = traffic_heuristics.handle_time(route, time, traffic_load)
                self.update_current_time(source_lat, source_lon, route['lat'], route['lon'], time)

            print junc
        print self.all_routes

    def grab_all_routes(self):
        return self.all_routes

    def refresh_all_routes(self):
        ''' this function reloads the routes file incase of a new update
        '''
        try:
            self.all_routes = json.loads(open("routes.json", "r").read())
            return True
        except Exception:
            return False

    def grab_junction_data(self):
        return self.junction_data

    def update_traffic_load(self, coords, traffic_load):
        try:
            self.all_routes["junctions"][coords]["traffic_load"] = traffic_load
        except TypeError:
            return False
        return True

    def update_current_time(self, lat, lon, route_lat, route_lon, time):
        coords = str(lat) + '//' + str(lon)
        # check to see which dict the junction is within
        if coords in self.all_routes["junctions_edge"]:
            junction = self.all_routes["junctions_edge"][coords]
        else:
            try:
                junction = self.all_routes["junctions"][coords]
            except TypeError:
                # return false as all avenues have been explored
                return False


        # make sure we iterate over the routes in the junction
        for element in junction["routes"]:
            if route_lat == element['lat']:
                print route_lat
                element["time"] = time
        return True

    def add_junction_data(self, datetime, coords):
        self.junction_data[datetime] = coords
        return True

    def pop_route(self, datetime):
        try:
            self.junction_data.pop(datetime)
            return True
        except KeyError:
            return False