import all_routes
import global_route
from scripts import haversine
import numpy
from bisect import bisect
from random import random

class JunctionHandler(object):
    """This class handles the data of the current junction """


    def __init__(self, current_route=None):
        """Default speed is 30 as this is the most common"""
        self.globalRoutes = global_route.GlobalRouteHandler()

        if current_route == None:
            allroutes = all_routes.AllRoutes()
            self._all_routes = allroutes.grab_all_routes()
            # this is a method call inside the constructor, not ideal but 
            # current route variable needs to be filled.
            self.current_route = self.pick_random_edge_route()
            # current coords is a seperate variable as this is the 'title' for the 
            # object rather than a variable
            self.current_coords = self.process_lat_lon(self.current_route[0])
            self.current_junc = self.current_route[1]
        else:
            if len(current_route) == 2:
                self.is_valid_junc = self.check_coords_valid(current_route[0], current_route[1])
                if self.is_valid_junc:
                    self.current_junc = self.globalRoutes.search_route(current_route[0], current_route[1])
                    self.current_coords = current_route[0], current_route[1]
                else:
                    self.current_junc = False

        if self.current_junc != False:
            self.junction_name = self.current_junc["junction_name"]
            # convert to int incase of accidental parsing as unicode
            self.speed = int(self.current_junc["speed"])
            self.lat = self.current_coords[0]
            self.lon = self.current_coords[1]
            self.route = self.current_junc["routes"]

    def check_coords_valid(self, lat, lon):
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return False
        valid = False
        if lat >= -90 and lat <= +90 and lon >= -180 and lon <= +180:
            valid = True
        return valid

    def check_if_route_exists(self):
        #print self.route[0]
        if self.current_junc != False and self.route[0] != {}:
            return True
        else:
            if self.is_valid_junc:
                return False
            else:
                return "Invalid data format"

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
        total = 0
        cum_weights = []
        for choice in choices:
            total += choice[1]
            cum_weights.append(total)
        x = random() * total
        # this bisects the weight by probability
        i = bisect(cum_weights, x)
        return i


    def process_lat_lon(self, latlon):
        coords = latlon.replace("//", " ").split()
        lat = coords[0]
        lon = coords[1]
        return lat, lon

    def pick_random_edge_route(self):
        allroutes = all_routes.AllRoutes()
        routes = allroutes.grab_all_routes()
        routeslist = routes["junctions_edge"]
        # select a random 'route' according to the number
        selection_number = numpy.random.randint(0, len(routeslist))
        # select a junction at random to generate traffic
        selected_route_key = routeslist.keys()
        selected_route_key = selected_route_key[selection_number]
        # pick the junction according to the selected route key
        selected_junction = routeslist[selected_route_key]
        return [selected_route_key, selected_junction]

    def generate_route(self):
        """This generates a random route, calling the time function"""
        potential_routes = self.route
        #select a random 'route' according to the number
        selection_number = self.weighted_junc_search()
        newroute = potential_routes[selection_number]
        traffic_load = self.globalRoutes.get_current_load(self.lat + "//" + self.lon, newroute['lat'] + "//" + newroute['lon'])
        self.globalRoutes.add_junction_data(str(self.lat + "//" + self.lon + "//" + str(newroute['lat']) + "//" + str(newroute['lon'])))
        self.globalRoutes.update_traffic_load(self.lat + '//' + self.lon, newroute['lat'], newroute['lon'], traffic_load)
        # this will be the time to reach destination
        time = self.globalRoutes.calculate_junction_distance_time(self.lat, self.lon, self.speed, newroute, traffic_load)
        route = {"lat": str(self.lat), "lon": str(self.lon), "time": time, "route": {"lat":str(newroute["lat"]), "lon":str(newroute["lon"])}}
        return route