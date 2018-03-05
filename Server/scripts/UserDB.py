import sys, os
# unfortunately a bit 'hacky' but only way to properly import
# server.__init__.py
sys.path.insert(0, os.path.abspath(".."))
from Server.__init__ import db, bcrypt
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

#admin = User(True, 'Admin','123456')
#db.session.add(admin)
#db.create_all()
#db.session.commit()