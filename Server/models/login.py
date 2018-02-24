import sys,os
# unfortunately a bit 'hacky' but only way to properly import
# server.__init__.py
sys.path.insert(0, os.path.abspath(".."))
from Server.__init__ import bcrypt
from scripts import UserDB

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