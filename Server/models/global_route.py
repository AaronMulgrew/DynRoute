import all_routes
allroutes = all_routes.AllRoutes()
allroutes.populate_all_routes()
import datetime
from scripts import haversine
import traffic_heuristics

class GlobalRouteHandler(object):

    def __init__(self, *args, **kwargs):
        self.all_routes = allroutes

    def get_current_load(self, coords):
        traffic_load = 0
        junction_data = self.all_routes.grab_junction_data()
        routes = self.all_routes.grab_all_routes()
        # interate over all of the junction keys
        for current_datetime in allroutes.junction_data.keys():
            # extract out the current coordinates by accessing the object in the dict
            if junction_data.get(current_datetime) == coords:

                # make sure the junction is in timerange
                if current_datetime > datetime.datetime.now()-datetime.timedelta(seconds=8):
                    traffic_load += 4
                else:
                    # pop the current time from the model
                    self.all_routes.pop_route(current_datetime)
        if traffic_load > 100:
            # make sure that the traffic load never exceeds 100%
            traffic_load = 99
        return traffic_load

    def process_lat_lon(self, latlon):
        coords = latlon.replace("//", " ").split()
        lat = coords[0]
        lon = coords[1]
        return lat, lon


    def calculate_junction_distance_time(self, source_lat, source_lon, speed, newroute, traffic_load):
        distanceM = haversine.get_distance_haversine([float(source_lat), float(source_lon)], [float(newroute['lat']), float(newroute['lon'])])
        # calculate the time needed to get to the junction 
        # by Distance over speed
        time = distanceM / speed
        
        time = traffic_heuristics.handle_time(newroute, time, traffic_load)
        # make sure the current time gets added to the current state
        self.update_current_time(source_lat, source_lon, newroute['lat'], newroute['lon'], time)
        return time

    def return_all_junctions(self):
        _all_routes = self.all_routes.grab_all_routes()
        _all_routes = _all_routes['junctions']
        junc_list = []
        #print self._junction_data
        for junc in _all_routes:
            #print junc
            lat, lon = self.process_lat_lon(junc)
            junction = {"junction":_all_routes[junc],"lat":lat,"lon":lon}
            junc_list.append(junction)
        return junc_list

    def search_route(self, lat, lon):
        # split the coords
        coords = str(lat) + '//' + str(lon)
        try:
            routes = self.all_routes.grab_all_routes()
            current_junc = routes["junctions"][coords]
        except KeyError as e:
            current_junc = False
        if current_junc != False:
            current_datetime = datetime.datetime.now()
            allroutes.add_junction_data(current_datetime, coords)
            ## AllRoutes.junction_data[current_datetime] = coords
            traffic_load = self.get_current_load(coords)
            allroutes.update_traffic_load(coords, traffic_load)
            
            #AllRoutes.all_routes["junctions"][coords]["traffic_load"] = traffic_load

        #self.route = current_route
        return current_junc

    def update_current_time(self, lat, lon, route_lat, route_lon, time):
        result = allroutes.update_current_time(lat, lon, route_lat, route_lon, time)
        return result