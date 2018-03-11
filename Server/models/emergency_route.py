import all_routes
import datetime
import json
from models import global_route, dijkstra_algorithm
from global_route import GlobalRouteHandler
from scripts import UserDB
from scripts import API_auth
all_routes = all_routes.AllRoutes()

''' Emergency Handler inherits from the globalRouteHandler class
in order to share all the same states '''
class EmergencyHandler(GlobalRouteHandler):
    
    def __init__(self, source_lat, source_lon, dest_lat, dest_lon):
        super(EmergencyHandler, self).__init__()
        # underscore before var name signifies it's private
        # to this class
        self._all_routes = ""
        self.dest_lat = dest_lat
        self.source_lat = source_lat
        self.dest_lon = dest_lon
        self.source_lon = source_lon


    def generate_emergency(self):
        self._all_routes = self.all_routes.grab_all_routes()
        dijkstra = dijkstra_algorithm.Dijkstra()
        dijkstra.reprocess_data(self._all_routes)
        print str(self.source_lat + "//" + self.source_lon + "//" + self.dest_lat + "//" + self.dest_lon)
        result = dijkstra.compute_shortest_route(self.source_lat + "//" + self.source_lon, self.dest_lat + "//" + self.dest_lon)
        #dijkstra.add_edges(self._all_routes)
        route = self.process_route(result)
        time_taken = self.calculate_time_route(route)
        return {"route":route, "time":time_taken}

    def process_route(self, route):
        # this readies the JSON object
        # for the browser
        # to convert from our python list
        newroute = list()
        for element in route['route']:
            lat, lon = element.split('//')
            newroute.append({'lat':lat, 'lon':lon})
        return newroute

