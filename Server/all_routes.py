import json

class AllRoutes(object):
    def __init__(self):
        self.all_routes = json.loads(open("routes.json", "r").read())
        # this is the 'live' junction data dictionary
        self.junction_data = dict()

    def grab_all_routes(self):
        return self.all_routes

    def grab_junction_data(self):
        return self.junction_data

    def update_traffic_load(self, coords, traffic_load):
        self.all_routes["junctions"][coords]["traffic_load"] = traffic_load
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