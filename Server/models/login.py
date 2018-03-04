import sys,os
# unfortunately a bit 'hacky' but only way to properly import
# server.__init__.py
sys.path.insert(0, os.path.abspath(".."))
from Server.__init__ import bcrypt
from scripts import UserDB
from scripts import API_auth
import datetime

def check_login(username, password):
    data = UserDB.User.query.filter_by(username=username).first()
    if data:
        check = bcrypt.check_password_hash(data.password, password)
        # make sure that the check is True
        if check:
            # make sure we return the password hash not the 
            # actual password
            return {'password':data.password}
    return False


def check_auth_token(auth_token):
    success = False
    return_value = ""
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
                success = True
            else:
                return_value = "Token has expired."
        else:
            return_value = "Wrong token!"
    elif return_value == None:
        return_value = "Wrong token!"
    return [return_value, success]