import json

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
        for junction in self.all_routes['junctions_edge']:
            junc = self.all_routes['junctions_edge'][junction]
            source_lat, source_lon = junction.split('//')
            for route in junc['routes']:
                one_route = route

                print one_route
            print junc
        print self.all_routes

    def grab_all_routes(self):
        return self.all_routes

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