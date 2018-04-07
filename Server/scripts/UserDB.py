import sys, os
# unfortunately a bit 'hacky' but only way to properly import
# server.__init__.py
sys.path.insert(0, os.path.abspath(".."))
from Server.__init__ import db, bcrypt, settings, app
from flask import Flask
import __init__
from flask_sqlalchemy import SQLAlchemy
#db = __init__.db
#bcrypt = __init__.bcrypt

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    isAdmin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, isAdmin, username, password):
        self.isAdmin = isAdmin
        self.username = username
        #self.password = password
        pw_hash = bcrypt.generate_password_hash(password)
        self.password = pw_hash
def setup():
    admin_user = User.query.filter_by(username="Admin").first()
    passw = settings.admin_password
    pwhash = bcrypt.generate_password_hash(passw)
    check_passw_hash = bcrypt.check_password_hash(admin_user.password, passw)
    if not check_passw_hash:
        # this is a threadsafe way of getting the user object
        local_object = db.session.merge(admin_user)
        local_object.password = pwhash
        db.session.commit()
        print (' Warning! '.center(80, '*'))
        print (' Admin password changed in configuration. '.center(80, '*'))



#admin = User(True, 'Admin','123456')
#db.session.add(admin)
#db.create_all()
#db.session.commit()