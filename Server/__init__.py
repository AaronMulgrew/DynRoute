from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
app = Flask(__name__, static_url_path='/static')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# this is disabled to supress the warnings about track modifications
# deprecation
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
db.create_all()
