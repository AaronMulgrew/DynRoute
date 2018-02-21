import json
from shutil import copyfile
import global_route
import datetime

class AddJunction(object):
    def __init__(self, *args, **kwargs):
        self.lat = ""
        self.lon = ""
        self.speed = 0
        self.junction_name = ""
        self.new_junction_name = ""
        self.all_routes = ""
        self.road_type = 1
        return super(AddJunction, self).__init__(*args, **kwargs)

    def process_lat_lon_float(self, latlon):
        decimal_point = latlon.find('.')
        # trim latitude down to six decimal places 
        # as this matches the JSON file.
        # whereas the standard of accuracy is higher in the browser.
        latlon = latlon[:decimal_point+7]
        return latlon

    ''' this function takes a request object
    and manipulates it based upon the values passed
    via the API '''
    def add_junction(self, request):
        
        print request
        lat_lon = request['NewLatLon']
        speed = int(request['Speed'])
        junction_name = request['SelectedJunction']
        new_junction_name = request['JuncName']
        old_lat_lon = request['OldLatLon']
        road_type = int(request['RoadType'])
        lat, lon = lat_lon.split('//')
        old_lat, old_lon = old_lat_lon.split('//')
        lat = self.process_lat_lon_float(lat)
        lon = self.process_lat_lon_float(lon)
        self.lat = lat
        self.lon = lon
        self.old_lat = str(old_lat)
        self.old_lon = old_lon
        self.speed = int(speed)
        self.junction_name = junction_name
        self.road_type = road_type
        self.new_junction_name = new_junction_name
        result = self.add_to_json()

        return result

    def add_to_json(self):
        self.all_routes = json.loads(open("routes.json", "r").read())
        result = self.search_by_route_name()
        return result
    
    def write_to_file(self):
        #always create a backup of the json file before writing data
        backup_filename = 'routes_backup_' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        copyfile('routes.json',backup_filename)
        try:
            with open("routes.json","w") as outfile:
                outfile.write(json.dumps(self.all_routes))
            return True
        except Exception as e:
            return False

    def search_by_route_name(self):
        lat_lon = str(self.old_lat) + '//' + str(self.old_lon)
        new_lat_lon = str(self.lat) + '//' + str(self.lon)
        current_junc = self.all_routes['junctions'].get(lat_lon)
        newroute = {'lat':self.lat, 'lon':self.lon, 'road_type':self.road_type, 'time':0, 'traffic_load': 0}
        newjunction = {'junction_name': self.new_junction_name, 'speed': self.speed,
                       'routes':[{}]}
        if current_junc:
            if current_junc['junction_name'] == self.junction_name:
                if self.all_routes['junctions'][lat_lon]['routes'] == [{}]:
                    self.all_routes['junctions'][lat_lon]['routes'] = [newroute]
                else:
                    self.all_routes['junctions'][lat_lon]['routes'].append(newroute)
                self.current_junc = current_junc
                self.all_routes['junctions'][new_lat_lon] = newjunction
                result = self.write_to_file()
                return result
            else:
                return False
        else:
            return False

