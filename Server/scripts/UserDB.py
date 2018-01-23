from flask import Flask
import __init__
from flask_sqlalchemy import SQLAlchemy

db = __init__.db
bcrypt = __init__.bcrypt

class User(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		#self.password = password
		pw_hash = bcrypt.generate_password_hash(password)
		self.password = pw_hash