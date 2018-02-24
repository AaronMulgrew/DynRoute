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
    
    def __init__(self, current_route = None):
        super(EmergencyHandler, self).__init__(current_route)
        # underscore before var name signifies it's private
        # to this class
        self._all_routes = ""


    def generate_emergency(self):
        self._all_routes = self.all_routes.grab_all_routes()
        dijkstra = dijkstra_algorithm.Dijkstra()
        dijkstra.reprocess_data(self._all_routes)
        result = dijkstra.compute_shortest_route('52.632930//-1.161572', '52.637952//-1.123362')
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



def emergency_route(auth_token):
    return_value = ""
    success = False
    try:
        decoded = API_auth.decode(auth_token)
        username = decoded['username']
        password_hash = decoded['password_hash']
        timestamp = decoded['timestamp']
        timestamp = datetime.datetime.fromtimestamp(timestamp)
        # Not raw SQL to protect against Injection attacks
        data = UserDB.User.query.filter_by(username=username).first()
    except KeyError:
        return_value = "No auth token"
    # this if statement checks to see if data has been initialised
    # it is safer than using "if data:"
    if 'data' in locals():
        # this checks to see that the decrypted password
        # is the same as the password hash for the login
        if data.password == password_hash:
            # verify the timestamp for the next 90 minutes
            if timestamp > datetime.datetime.now()-datetime.timedelta(minutes=90):
                Emergency = EmergencyHandler()
                route = Emergency.generate_emergency()
                return_value = json.dumps(route)
                success = True
            else:
                return_value = "Token has expired."
        else:
            return_value = "Wrong token!"
    elif return_value == None:
        return_value = "Wrong token!"
    return [return_value, success]