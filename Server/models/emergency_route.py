from __init__ import request, all_routes
import datetime
import json
from models import global_route
from global_route import GlobalRouteHandler
from scripts import UserDB
from scripts import API_auth, dijkstra_algorithm
from junction_handler import JunctionHandler

class EmergencyHandler(GlobalRouteHandler):
    
    def __init__(self, current_route = None):
        super(EmergencyHandler, self).__init__(current_route)
        # underscore before var name signifies it's private
        # to this class
        self._all_routes = self.all_routes.grab_all_routes()


    def generate_emergency(self):
        print self._all_routes
        dijkstra = dijkstra_algorithm.Dijkstra()
        dijkstra.reprocess_data(self._all_routes)
        dijkstra.add_edges(self._all_routes)
        return self._all_routes





def emergency_route():
    return_value = ""
    success = False
    try:
        # this is the end point for the generate emergency token
        auth_token = request.headers['auth-token']
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
            # verify the timestamp for the next 30 minutes
            if timestamp > datetime.datetime.now()-datetime.timedelta(minutes=30):
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