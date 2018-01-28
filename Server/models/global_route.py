from all_routes import AllRoutes
import datetime

class GlobalRouteHandler(object):

    def get_current_load(self, coords):
        traffic_load = 0
        for current_datetime in AllRoutes.junction_data.keys():
            # extract out the current coordinates by accessing the object in the dict
            if AllRoutes.junction_data.get(current_datetime) == coords:
                junc_time = AllRoutes.junction_data[current_datetime]
                if current_datetime > datetime.datetime.now()-datetime.timedelta(seconds=8):
                    traffic_load += 6
                else:
                    AllRoutes.junction_data.pop(current_datetime)
        if traffic_load > 100:
            traffic_load = 99
        return traffic_load

    def search_route(self, lat, lon):
        coords = str(lat) + '//' + str(lon)
        try:
            current_junc = AllRoutes.all_routes["junctions"][coords]
        except KeyError as e:
            current_junc = False
        if current_junc != False:
            current_datetime = datetime.datetime.now()
            AllRoutes.junction_data[current_datetime] = coords
            traffic_load = self.get_current_load(coords)
            AllRoutes.all_routes["junctions"][coords]["traffic_load"] = traffic_load

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

