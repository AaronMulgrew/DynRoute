import all_routes
allroutes = all_routes.AllRoutes()
import datetime

class GlobalRouteHandler(object):

    def get_current_load(self, coords):
        traffic_load = 0
        junction_data = allroutes.grab_junction_data()
        routes = allroutes.grab_all_routes()
        # interate over all of the junction keys
        for current_datetime in allroutes.junction_data.keys():
            # extract out the current coordinates by accessing the object in the dict
            if junction_data.get(current_datetime) == coords:
                print "at junction data if statement"

                # make sure the junction is in timerange
                if current_datetime > datetime.datetime.now()-datetime.timedelta(seconds=8):
                    traffic_load += 4
                else:
                    # pop the current time from the model
                    allroutes.pop_route(current_datetime)
        if traffic_load > 100:
            # make sure that the traffic load never exceeds 100%
            traffic_load = 99
        return traffic_load

    def search_route(self, lat, lon):
        # split the coords
        coords = str(lat) + '//' + str(lon)
        try:
            routes = allroutes.grab_all_routes()
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

    def return_all_junctions(self):
        _all_routes = AllRoutes.all_routes["junctions"]
        junc_list = []
        #print self._junction_data
        for junc in _all_routes:
            #print junc
            j = JunctionHandler()
            lat, lon = j.process_lat_lon(junc)
            junction = {"junction":_all_routes[junc],"lat":lat,"lon":lon}
            junc_list.append(junction)
        return junc_list

