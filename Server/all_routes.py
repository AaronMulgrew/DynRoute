import json

class AllRoutes(object):
    def __init__(self):
        self.all_routes = json.loads(open("routes.json", "r").read())
        # this is the 'live' junction data dictionary
        # it contains a series of dateTime entries
        # that will iterated over from the code
        self.junction_data = dict()

    def grab_all_routes(self):
        #for key, value in self.all_routes['junctions'].iteritems():
        #    valsss = value["traffic_load"]
        #    print "Traffic Load: " + str(valsss)
        return self.all_routes

    def grab_junction_data(self):
        return self.junction_data

    def update_traffic_load(self, coords, traffic_load):
        try:
            self.all_routes["junctions"][coords]["traffic_load"] = traffic_load
        except TypeError:
            return False
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