from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from sqlalchemy import exc
from models import junction_handler, global_route, add_junction
import settings
app = Flask(__name__, static_url_path='/static')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prod.db'
# this is disabled to supress the warnings about track modifications
# deprecation
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
db.create_all()