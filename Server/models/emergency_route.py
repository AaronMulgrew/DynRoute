from __init__ import request
import datetime
import json
from scripts import UserDB
from scripts import API_auth
from junction_handler import JunctionHandler

class EmergencyHandler(JunctionHandler):

    def generate_emergency(self):
        route = self.generate_route()
        return route

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
        data = UserDB.User.query.filter_by(username=username).first()
    except KeyError:
        return_value = "No auth token"
    # this if statement checks to see if data has been initialised
    # it is safer than using "if data:"
    if 'data' in locals():
        # this checks to see that the decrypted password
        # is the same as the password hash for the login
        if data.password == password_hash:
            if timestamp > datetime.datetime.now()-datetime.timedelta(seconds=60):
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