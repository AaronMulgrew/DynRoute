''' This is the base server.py file,
mainly used for endpoint redirection to the models and scripts folders
'''
import json
from flask import (current_app, url_for, \
render_template, redirect, session)
from flask_api import status
from __init__ import app, bcrypt, request, junction_handler, global_route
from scripts import API_auth

import settings

from models import emergency_route
from OpenSSL import SSL
from scripts import UserDB
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('certs/domain.crt', 'certs/domain.key')






@app.route('/coordinates/<coordinates>', methods = ['GET'])
def coords(coordinates):
    lat_lon = coordinates.split(":")
    lat = str(lat_lon[0])
    lon = str(lat_lon[1])
    Junction = junction_handler.JunctionHandler([lat,lon])
    routeExists = Junction.check_if_route_exists()
    if routeExists != False:
        route = Junction.generate_route()
        return json.dumps(route)
    else:
        return json.dumps(False)

@app.route('/index.html')
def send_homepage():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		print session['username']
		return render_template('index.html', data=session['username'])


@app.route('/config.html')
def send_config():
	return render_template('config.html')

@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('send_homepage'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        data = UserDB.User.query.filter_by(username=name).first()
        if data:		
            check = bcrypt.check_password_hash(data.password, passw)
            print data.password
            print check
            if check:
                token = API_auth.encode(name, data.password)
                session['logged_in'] = True
                session['auth_token'] = token
                session['username'] = name
                return redirect(url_for('send_homepage'))
        else:
            return render_template('index.html', error='Wrong username or password!')

@app.route('/junc_icon.png')
def send_junc_icon():
    return current_app.send_static_file('junc_icon.png')

@app.route('/all_juncts')
def return_all_junctions():
    routehandler = global_route.GlobalRouteHandler()
    all_junctions = routehandler.return_all_junctions()
    return json.dumps(all_junctions)

@app.route('/MovingMarker.js')
def send_javascript():
    return current_app.send_static_file('MovingMarker.js')


@app.route('/generate_emergency')
def generate_emergency_route():
    ## simple check to see if the auth token is in the request 
    ## header
    if 'auth-token' in request.headers:
        # this is the end point for the generate emergency token
        auth_token = request.headers['auth-token']
        response_content = emergency_route.emergency_route(auth_token)
        content = response_content[0]
        success = response_content[1]
        if success == True:
            return content
        else:
            return content, status.HTTP_401_UNAUTHORIZED
    else:
        return "No auth token", status.HTTP_401_UNAUTHORIZED


@app.route('/')
def generate_edge_coords():
    junc = junction_handler.JunctionHandler()
    route = junc.generate_route()
    #lat = gen_coord_lat()
    #lon = gen_coord_lon()
    return json.dumps(route)

#def GetRoutes():

#    #globalRoutes = GlobalRouteHandler()
#    #print globalRoutes.search_route(52.634169, -1.149998)

#    # load the global variable
#    global _ALL_ROUTES
#    _ALL_ROUTES = open("routes.json", "r").read()
#    # this checks to see that the JSON file is valid.
#    try:
#        _ALL_ROUTES = json.loads(_ALL_ROUTES)
#    except ValueError:
#        print "\"Routes.json\" is not a valid JSON file."
#        exit(1)


if __name__ == "__main__":
    app.secret_key = settings.SECRET_KEY
    app.run(debug=False, ssl_context=context)