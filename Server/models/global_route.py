import all_routes
allroutes = all_routes.AllRoutes()
import datetime

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
        if result == True:
            return True
        else:
            return False