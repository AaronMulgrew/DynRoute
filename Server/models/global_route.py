import all_routes
allroutes = all_routes.AllRoutes()
import datetime
from scripts import haversine
import traffic_heuristics

class GlobalRouteHandler(object):

    def __init__(self, *args, **kwargs):
        self.all_routes = allroutes

    def get_current_load(self, coords, routecoords):
        traffic_load = 0
        junction_data = self.all_routes.grab_junction_data()
        routes = self.all_routes.grab_all_routes()
        # interate over all of the junction keys
        for current_datetime in allroutes.junction_data.keys():
            # extract out the current coordinates by accessing the object in the dict
            if junction_data.get(current_datetime) == coords+routecoords:
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
        try:
            distanceM = haversine.get_distance_haversine([float(source_lat), float(source_lon), float(newroute['lat']), float(newroute['lon'])])
        except KeyError:
            # sometimes throws exception due to unicode error
            distanceM = haversine.get_distance_haversine([float(source_lat), float(source_lon), float(newroute[u'lat']), float(newroute[u'lon'])])
        # calculate the time needed to get to the junction 
        # by Distance over speed
        time = distanceM / speed
        
        newtime = traffic_heuristics.handle_time(newroute, time, traffic_load)
        # make sure the current time gets added to the current state
        self.update_current_time(source_lat, source_lon, newroute['lat'], newroute['lon'], newtime)
        return time

    def return_all_junctions(self):
        _all_routes = self.all_routes.grab_all_routes()
        _all_routes = _all_routes['junctions']
        junc_list = []
        #print self._junction_data
        for junc in _all_routes:
            for route in _all_routes[junc]['routes']:
                if route:
                    updated_traffic_load =self.get_current_load(junc, route[u'lat'] + '//' + route[u'lon'])
                    route['traffic_load'] = updated_traffic_load
            #print junc
            lat, lon = self.process_lat_lon(junc)
            junction = {"junction":_all_routes[junc],"lat":lat,"lon":lon}
            junc_list.append(junction)
        return junc_list

    def search_route(self, lat, lon):
        _all_routes = self.all_routes.grab_all_routes()
        lat_lon = lat+'//'+lon
        if lat_lon in _all_routes['junctions']:
            junc = _all_routes['junctions'][lat+'//'+lon]
        else:
            try:
                junc = _all_routes['junctions_edge'][lat+'//'+lon]
            except KeyError:
                return False
        return junc

    def refresh_all_routes(self):
        ''' this is an interface to the all_routes.py
        file '''
        result = allroutes.refresh_all_routes()
        return result

    def update_current_time(self, lat, lon, route_lat, route_lon, time):
        result = allroutes.update_current_time(lat, lon, route_lat, route_lon, time)
        return result

    def add_junction_data(self, coords):
        timenow = datetime.datetime.now()
        result = allroutes.add_junction_data(timenow, coords)
        return result

    def calculate_time_route(self, coords):
        time = 0
        for index, item in enumerate(coords):
            lat = str(item['lat'])
            lon = str(item['lon'])
            junction = self.search_route(lat, lon)
            routes = junction['routes']
            for route in routes:
                if route.get('lat'):
                    lat = route['lat']
                    lon = route['lon']
                    # do a direct comparison to the next route in the list
                    # as the list will always be sequential
                    if lat == coords[index+1]['lat'] and lon == coords[index+1]['lon']:
                        time = time + route['time']
        return time

    def update_traffic_load(self, source_latlon, route_lat, route_lon, traffic_load):
        allroutes.update_traffic_load(source_latlon, route_lat, route_lon, traffic_load)